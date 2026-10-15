"""
phase_i_neural_verifier.py

Phase I for Medi-RAG: Neural Faithfulness Verifier

Trains a small classifier that reads (report context, generated
explanation) and predicts whether the explanation is FAITHFUL (grounded
in the context) or HALLUCINATED (contradicts or fabricates beyond it).

Why synthetic data instead of waiting for more real Claude outputs:
    You currently only have a handful of saved Claude answers -- nowhere
    near enough to train a classifier. Instead, this script builds
    training pairs directly from your existing Phase C chunk text (150
    patient-months), which already contains ground-truth statements like
    "HbA1c: 7.3% (Classification: Diabetic)". Every such statement
    becomes one FAITHFUL example. We then generate three kinds of
    corrupted copies -- wrong value, wrong label, fabricated claim -- as
    HALLUCINATED examples. This gives hundreds of labeled pairs without
    any additional API calls or cost.

Three steps in this file, run in order via the functions in main():
    1. build_synthetic_dataset() -- extract statements from chunks,
       create faithful + corrupted pairs, save to
       verifier_data/synthetic_pairs.json
    2. train_verifier()          -- fine-tune BioClinicalBERT as a
       binary classifier on those pairs, save the trained model to
       models/verifier/
    3. predict_faithfulness()    -- load the trained model and score
       any new (context, explanation) pair -- this is the function
       phase_g_generation.py will eventually call to double-check
       Claude's real outputs

Run steps 1 and 2 ONCE (they take time, especially on CPU). After that,
predict_faithfulness() reuses the saved model instantly.

Run this from your MediRAG root folder (same level as preprocessed/).

Requirements:
    pip install transformers torch scikit-learn
"""

import os
import re
import json
import random

# -----------------------------
# Config
# -----------------------------
MANIFEST_PATH = os.path.join("preprocessed", "chunks_manifest.json")
SYNTHETIC_DATA_DIR = "verifier_data"
SYNTHETIC_DATA_PATH = os.path.join(SYNTHETIC_DATA_DIR, "synthetic_pairs.json")

MODEL_NAME = "emilyalsentzer/Bio_ClinicalBERT"
MODEL_OUTPUT_DIR = os.path.join("models", "verifier")

MAX_LENGTH = 512
RANDOM_SEED = 42

os.makedirs(SYNTHETIC_DATA_DIR, exist_ok=True)
os.makedirs(MODEL_OUTPUT_DIR, exist_ok=True)
random.seed(RANDOM_SEED)

# A statement pattern matching your chunk text format, e.g.:
#   "HbA1c: 7.3% (Classification: Diabetic)"
#   "Fasting Blood Sugar (FBS): 139.0 mg/dL (Classification: Diabetic)"
STATEMENT_PATTERN = re.compile(
    r"([A-Za-z][A-Za-z \-\(\)]*?):\s*([\d]+\.?[\d]*)\s*(%|mg/dL)?\s*\(Classification:\s*([A-Za-z\- ]+?)\)"
)

WRONG_LABELS_POOL = ["Normal", "Prediabetic", "Diabetic", "Borderline", "High Risk"]

FABRICATED_CLAUSES = [
    " This is likely caused by a recent viral infection.",
    " Your doctor has already adjusted your insulin dosage in response.",
    " This appears to be linked to a missed medication dose last week.",
    " Genetic factors are the primary driver of this specific reading.",
    " This value was affected by a lab equipment recalibration.",
]


# -----------------------------
# Step 1: Build the synthetic dataset
# -----------------------------
def load_chunk_texts():
    """Loads every chunk's raw text from the Phase C manifest."""
    with open(MANIFEST_PATH, "r") as f:
        manifest = json.load(f)

    chunks = []
    for entry in manifest:
        chunk_path = entry["chunk_file"].replace("\\", "/")
        if not os.path.exists(chunk_path):
            continue
        with open(chunk_path, "r") as f:
            text = f.read()
        chunks.append(text)
    return chunks


def load_chunks_by_patient():
    """
    Same as load_chunk_texts(), but grouped by Patient_ID -- needed to
    build multi-fact training examples that combine a patient's several
    months into one explanation, matching the real shape of Claude's
    actual multi-month answers.
    """
    with open(MANIFEST_PATH, "r") as f:
        manifest = json.load(f)

    chunks_by_patient = {}
    for entry in manifest:
        chunk_path = entry["chunk_file"].replace("\\", "/")
        if not os.path.exists(chunk_path):
            continue
        with open(chunk_path, "r") as f:
            text = f.read()
        patient_id = entry.get("Patient_ID", "UNKNOWN")
        chunks_by_patient.setdefault(patient_id, []).append(text)
    return chunks_by_patient


INTRO_PHRASES = [
    "Based on your recent lab report, here's what we found. ",
    "Looking at your latest results: ",
    "Here's a summary of your recent test values. ",
    "According to your most recent report, ",
    "Reviewing your lab results, we can see the following. ",
]

CLOSING_PHRASES = [
    " It would be a good idea to discuss this with your doctor to understand what it means for your care.",
    " Please consult your healthcare provider to review these results further.",
    " Your doctor can help interpret what this means for your overall health.",
    " We recommend discussing this trend with a medical professional.",
    " Consider bringing this up at your next appointment with your doctor.",
]


def wrap_realistic(core_statement):
    """
    Wraps a short factual statement in a longer, natural-sounding
    paragraph resembling real Claude output (intro + fact + doctor
    referral closing) -- this is what makes the verifier's training
    distribution actually match what it will see in production, rather
    than only ever training on bare, isolated one-line facts.
    """
    intro = random.choice(INTRO_PHRASES)
    closing = random.choice(CLOSING_PHRASES)
    return f"{intro}{core_statement}{closing}"


def make_faithful_statement(marker, value, unit, label):
    unit_str = unit if unit else ""
    core = f"Your {marker} is {value}{unit_str}, classified as {label}."
    return wrap_realistic(core)


def make_corrupted_value(marker, value, unit, label):
    """Wrong number -- shifts the value enough to plausibly change meaning."""
    try:
        original = float(value)
    except ValueError:
        original = 0.0
    shift = random.choice([-3, -2, -1.5, 1.5, 2, 3])
    corrupted_value = round(max(original + shift, 0.1), 1)
    unit_str = unit if unit else ""
    core = f"Your {marker} is {corrupted_value}{unit_str}, classified as {label}."
    return wrap_realistic(core)


def make_corrupted_label(marker, value, unit, label):
    """Correct number, wrong classification word."""
    wrong_options = [l for l in WRONG_LABELS_POOL if l.lower() != label.strip().lower()]
    wrong_label = random.choice(wrong_options)
    unit_str = unit if unit else ""
    core = f"Your {marker} is {value}{unit_str}, classified as {wrong_label}."
    return wrap_realistic(core)


def make_fabricated_claim(marker, value, unit, label):
    """Correct number and label, but with an invented, unsupported clause added."""
    base = make_faithful_statement(marker, value, unit, label)
    return base + random.choice(FABRICATED_CLAUSES)


def build_multi_fact_examples(chunks_by_patient):
    """
    Builds MULTI-FACT training examples that combine 2-3 months into one
    explanation -- matching the actual shape of real Claude answers,
    which discuss a patient's whole history at once rather than a single
    isolated fact. Without this, the verifier only ever sees single-fact
    examples during training and may learn to treat any longer,
    multi-part answer as unfamiliar/suspicious regardless of accuracy.

    For each patient with 2+ months of data:
        - FAITHFUL: an explanation combining all their real months' facts.
        - PARTIALLY HALLUCINATED: same explanation, but ONE month's value
          is corrupted while the others stay correct -- a realistic,
          harder negative example, since a real failure is more likely
          to be "2 correct months + 1 wrong number" than "everything wrong."
    """
    pairs = []

    for patient_id, patient_chunks in chunks_by_patient.items():
        if len(patient_chunks) < 2:
            continue

        statements = []
        for chunk_text in patient_chunks:
            matches = STATEMENT_PATTERN.findall(chunk_text)
            for marker, value, unit, label in matches:
                statements.append((marker.strip(), value, unit, label.strip()))

        if len(statements) < 2:
            continue

        combined_context = " ".join(patient_chunks)

        # FAITHFUL multi-fact explanation
        faithful_lines = [make_faithful_statement(m, v, u, l) for m, v, u, l in statements]
        faithful_explanation = " ".join(faithful_lines)
        pairs.append({"context": combined_context, "explanation": faithful_explanation, "label": 1})

        # PARTIALLY HALLUCINATED: corrupt exactly one statement, keep the rest correct
        corrupted_idx = random.randrange(len(statements))
        mixed_lines = []
        for i, (m, v, u, l) in enumerate(statements):
            if i == corrupted_idx:
                mixed_lines.append(make_corrupted_value(m, v, u, l))
            else:
                mixed_lines.append(make_faithful_statement(m, v, u, l))
        mixed_explanation = " ".join(mixed_lines)
        pairs.append({"context": combined_context, "explanation": mixed_explanation, "label": 0})

    return pairs


def build_synthetic_dataset(quick_test=False):
    """
    Extracts every biomarker statement from every chunk and builds a
    balanced set of faithful (label=1) and hallucinated (label=0) pairs,
    PLUS multi-fact combined examples matching real Claude answer shape.

    quick_test=True builds a small subset (roughly 1/5 the data) so you
    can validate this fix trains correctly in minutes, before committing
    to a full multi-hour run on the complete dataset.
    """
    chunks = load_chunk_texts()
    chunks_by_patient = load_chunks_by_patient()
    print(f"Loaded {len(chunks)} chunks. Extracting biomarker statements...")

    pairs = []
    total_statements = 0

    for context in chunks:
        matches = STATEMENT_PATTERN.findall(context)
        for marker, value, unit, label in matches:
            marker = marker.strip()
            label = label.strip()
            total_statements += 1

            # One faithful example
            pairs.append({
                "context": context,
                "explanation": make_faithful_statement(marker, value, unit, label),
                "label": 1,
            })

            # Three corrupted (hallucinated) variants
            pairs.append({
                "context": context,
                "explanation": make_corrupted_value(marker, value, unit, label),
                "label": 0,
            })
            pairs.append({
                "context": context,
                "explanation": make_corrupted_label(marker, value, unit, label),
                "label": 0,
            })
            pairs.append({
                "context": context,
                "explanation": make_fabricated_claim(marker, value, unit, label),
                "label": 0,
            })

    # NEW: multi-fact examples matching real answer structure
    multi_fact_pairs = build_multi_fact_examples(chunks_by_patient)
    print(f"Built {len(multi_fact_pairs)} multi-fact combined examples "
          f"(matching real multi-month answer structure).")
    pairs.extend(multi_fact_pairs)

    random.shuffle(pairs)

    if quick_test:
        pairs = pairs[:max(60, len(pairs) // 5)]
        print(f"QUICK TEST MODE: using only {len(pairs)} pairs for a fast validation run.")

    with open(SYNTHETIC_DATA_PATH, "w") as f:
        json.dump(pairs, f, indent=2)

    faithful_count = sum(1 for p in pairs if p["label"] == 1)
    hallucinated_count = sum(1 for p in pairs if p["label"] == 0)
    print(f"Extracted {total_statements} real biomarker statements from your data.")
    print(f"Built {len(pairs)} training pairs ({faithful_count} faithful, {hallucinated_count} hallucinated).")
    print(f"Saved -> {SYNTHETIC_DATA_PATH}")

    return pairs


# -----------------------------
# Step 2: Train the verifier
# -----------------------------
def train_verifier(quick_test=False):
    """
    Fine-tunes BioClinicalBERT as a binary sequence-pair classifier:
    input = [context, explanation], output = faithful (1) / hallucinated (0).

    quick_test=True trains for just 1 epoch on the small quick-test
    dataset and saves to models/verifier_quicktest/ (NOT overwriting
    your real trained model) -- use this to validate the multi-fact
    fix works in a few minutes before committing to a full multi-hour
    retrain on the complete dataset.

    This will be slow on CPU (expect anywhere from 10-40+ minutes for a
    full run, depending on dataset size and your machine) -- that's
    expected for fine-tuning a BERT-family model without a GPU.
    """
    import torch
    from torch.utils.data import Dataset
    from transformers import (
        AutoTokenizer, AutoModelForSequenceClassification,
        TrainingArguments, Trainer,
    )
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, precision_recall_fscore_support

    output_dir = os.path.join("models", "verifier_quicktest") if quick_test else MODEL_OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(SYNTHETIC_DATA_PATH):
        print("No synthetic dataset found -- run build_synthetic_dataset() first.")
        return

    with open(SYNTHETIC_DATA_PATH, "r") as f:
        pairs = json.load(f)

    train_pairs, val_pairs = train_test_split(
        pairs, test_size=0.2, random_state=RANDOM_SEED,
        stratify=[p["label"] for p in pairs]
    )
    print(f"Train: {len(train_pairs)} pairs | Validation: {len(val_pairs)} pairs")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    class PairDataset(Dataset):
        def __init__(self, pairs):
            self.pairs = pairs

        def __len__(self):
            return len(self.pairs)

        def __getitem__(self, idx):
            pair = self.pairs[idx]
            encoding = tokenizer(
                pair["context"], pair["explanation"],
                truncation=True, max_length=MAX_LENGTH, padding="max_length",
            )
            item = {k: torch.tensor(v) for k, v in encoding.items()}
            item["labels"] = torch.tensor(pair["label"])
            return item

    train_dataset = PairDataset(train_pairs)
    val_dataset = PairDataset(val_pairs)

    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        predictions = logits.argmax(axis=-1)
        precision, recall, f1, _ = precision_recall_fscore_support(labels, predictions, average="binary")
        acc = accuracy_score(labels, predictions)
        return {"accuracy": acc, "precision": precision, "recall": recall, "f1": f1}

    training_args = TrainingArguments(
        output_dir=os.path.join(output_dir, "checkpoints"),
        num_train_epochs=1 if quick_test else 3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        eval_strategy="epoch",
        save_strategy="epoch",
        logging_steps=20,
        load_best_model_at_end=True,
        metric_for_best_model="f1",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
    )

    print(f"\nStarting {'QUICK TEST' if quick_test else 'full'} training...\n")
    trainer.train()

    eval_results = trainer.evaluate()
    print(f"\nFinal validation results: {eval_results}")

    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"\nSaved {'quick-test' if quick_test else 'trained'} verifier -> {output_dir}")

    with open(os.path.join(output_dir, "eval_results.json"), "w") as f:
        json.dump(eval_results, f, indent=2)


# -----------------------------
# Step 3: Inference -- use the trained verifier on new text
# -----------------------------
_verifier_cache = {}


def predict_faithfulness(context, explanation):
    """
    Loads the trained verifier (once, then cached) and scores a new
    (context, explanation) pair. Returns a dict with the predicted
    label and confidence -- this is what phase_g_generation.py would
    call after Claude generates an answer, to double-check it before
    showing it to the patient.
    """
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification

    if "model" not in _verifier_cache:
        if not os.path.exists(os.path.join(MODEL_OUTPUT_DIR, "config.json")):
            raise FileNotFoundError(
                f"No trained verifier found at {MODEL_OUTPUT_DIR} -- run train_verifier() first."
            )
        tokenizer = AutoTokenizer.from_pretrained(MODEL_OUTPUT_DIR)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_OUTPUT_DIR)
        model.eval()
        _verifier_cache["tokenizer"] = tokenizer
        _verifier_cache["model"] = model

    tokenizer = _verifier_cache["tokenizer"]
    model = _verifier_cache["model"]

    inputs = tokenizer(
        context, explanation,
        truncation=True, max_length=MAX_LENGTH, padding="max_length",
        return_tensors="pt",
    )
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1).squeeze()

    hallucinated_prob = float(probs[0])
    faithful_prob = float(probs[1])
    predicted_label = "faithful" if faithful_prob > hallucinated_prob else "hallucinated"

    return {
        "predicted_label": predicted_label,
        "faithful_confidence": round(faithful_prob, 4),
        "hallucinated_confidence": round(hallucinated_prob, 4),
    }


# -----------------------------
# Claim-level, chunk-matched verification (the confirmed-working method
# for real, multi-fact LLM answers -- see debug_verifier.py Test 6)
# -----------------------------
TREND_WORDS = ["dipped", "changed", "trend", "across", "consistently",
               "throughout", "overall", "over the", "compared to"]

# Correction/negation language -- the trained verifier only ever saw
# POSITIVE assertions during training ("Your X is Y"), never a sentence
# that REJECTS a false claim ("that's not correct", "there is no record
# of X"). It has no learned signal for this pattern and produces
# unreliable, often backwards results on it (see debug_verifier.py
# analysis of trap queries T011/T014). Rather than trust an unreliable
# classification, these claims are routed to their own category and
# excluded from the faithful/hallucinated verdict entirely.
CORRECTION_PATTERNS = [
    "not correct", "that's not", "isn't correct", "is not correct",
    "no record", "does not appear", "doesn't appear", "there is no",
    "cannot confirm", "can't confirm", "no measurement", "not quite",
    "not accurate", "doesn't match", "does not match", "no data",
    "not available", "isn't in the", "not in the", "no such value",
    "not right", "incorrect", "actually,",
]


def is_correction_claim(claim_text):
    """
    Detects whether a claim is REJECTING/correcting a false premise
    rather than asserting a positive fact -- a pattern the verifier was
    never trained on (see CORRECTION_PATTERNS docstring above).
    """
    claim_lower = claim_text.lower()
    return any(pattern in claim_lower for pattern in CORRECTION_PATTERNS)


def extract_verifiable_claims(answer_text):
    """
    Extracts individual, single-fact claims from a real (possibly long,
    multi-month) LLM answer -- keeping only lines that mention ONE
    specific month and a number, and excluding trend/summary sentences
    that reference multiple months (e.g. "your HbA1c dipped then rose
    across Month 2 and Month 3"). Trend claims inherently can't be
    verified against a single chunk and are a deliberate scope boundary
    of this method, not a limitation to work around.
    """
    claims = []
    for line in answer_text.split("\n"):
        stripped = line.strip("-* ").strip()
        if not (re.search(r"month[\s_]*\d+", stripped, re.IGNORECASE) and any(ch.isdigit() for ch in stripped)):
            continue

        month_mentions = len(re.findall(r"month[\s_]*\d+", stripped, re.IGNORECASE))
        has_trend_language = any(word in stripped.lower() for word in TREND_WORDS)

        if month_mentions > 1 or has_trend_language:
            continue  # trend/summary claim -- out of scope for single-chunk verification

        claims.append(stripped)
    return claims


def match_claim_to_chunk(claim_text, retrieved_chunks):
    """
    Finds the single retrieved chunk matching a claim's referenced
    month -- e.g. a "Month 2" claim is checked ONLY against Month 2's
    chunk, exactly mirroring how the verifier was trained (one claim,
    one matching chunk, never a multi-month concatenation). Returns
    None if no matching chunk is found (e.g. future-prediction claims
    not tied to any retrieved chunk).
    """
    match = re.search(r"month[\s_]*(\d+)", claim_text, re.IGNORECASE)
    if not match:
        return None
    month_num = match.group(1)

    for chunk in retrieved_chunks:
        chunk_month = str(chunk.get("Month", ""))
        if re.search(rf"month[\s_]*{month_num}\b", chunk_month, re.IGNORECASE):
            return chunk["text"]
    return None


def verify_answer_by_matched_chunks(answer_text, retrieved_chunks):
    """
    THE RECOMMENDED verification method for real (long, multi-fact) LLM
    answers -- confirmed working in debug_verifier.py Test 6. Checks
    each individual claim against ONLY its own matching chunk, rather
    than checking the whole answer against the full combined context
    (which the verifier was never trained to handle and performs very
    poorly on -- see debug_verifier.py Tests 1-5 for the diagnosis).

    Correction/negation claims (e.g. "that's not correct, the real
    value is X") are detected and routed to a separate bucket rather
    than run through the classifier, since it was never trained on
    negation language and produces unreliable results on it.

    Returns the overall label (hallucinated if ANY checked positive
    claim is flagged), the per-claim results, claims that couldn't be
    matched to a single chunk, AND correction claims (reported
    separately, not counted toward the verdict).
    """
    claims = extract_verifiable_claims(answer_text)
    results = []
    skipped = []
    corrections = []

    for claim in claims:
        if is_correction_claim(claim):
            corrections.append(claim)
            continue

        matched_context = match_claim_to_chunk(claim, retrieved_chunks)
        if matched_context is None:
            skipped.append(claim)
            continue
        wrapped_claim = wrap_realistic(claim)
        result = predict_faithfulness(matched_context, wrapped_claim)
        results.append({"claim": claim, **result})

    overall_label = "hallucinated" if any(
        r["predicted_label"] == "hallucinated" for r in results
    ) else ("faithful" if results else "not_verifiable")

    return {
        "overall_label": overall_label,
        "claim_results": results,
        "skipped_claims": skipped,
        "correction_claims": corrections,
    }


# -----------------------------
# Main
# -----------------------------
def main():
    print("=== Step 1: Building synthetic training dataset ===\n")
    build_synthetic_dataset()

    print("\n=== Step 2: Training the neural verifier ===\n")
    train_verifier()

    print("\n=== Step 3: Quick sanity test on a real example ===\n")
    # A genuinely faithful example, similar to what Claude produced for P032
    test_context = "Laboratory Report Summary for Patient P032 (Female, age 53) -- Month 1. HbA1c: 7.3% (Classification: Diabetic)."
    faithful_test = "Your HbA1c is 7.3%, classified as Diabetic."
    hallucinated_test = "Your HbA1c is 5.2%, classified as Normal."

    result_faithful = predict_faithfulness(test_context, faithful_test)
    result_hallucinated = predict_faithfulness(test_context, hallucinated_test)

    print(f"Faithful test case:     {result_faithful}")
    print(f"Hallucinated test case: {result_hallucinated}")

    print("\nPhase I complete. The verifier is ready to check real Claude outputs.")


if __name__ == "__main__":
    main()