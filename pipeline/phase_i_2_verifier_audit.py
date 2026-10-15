"""
phase_i_2_verifier_audit.py

Audits the ALREADY-TRAINED neural verifier. Does NOT retrain anything.
It only loads models/verifier/ and runs predictions (roughly 15-25 min on CPU).

What it measures:
  1. Reproduces Table III on the exact same validation split
     (same synthetic_pairs.json, same seed, same stratified 80/20 split).
  2. Confusion matrix and metrics for BOTH classes. phase_i reports
     precision/recall for the FAITHFUL class only (label 1); for a
     hallucination detector, recall on the HALLUCINATED class is the
     number readers care about most.
  3. Accuracy by example type: faithful, wrong value, wrong label,
     fabricated clause, multi-fact faithful, multi-fact partially wrong.
  4. Leakage check: how many validation examples share their report
     chunk / statement with a training example (the split was random
     over pairs, not by patient).
  5. Count of training statements where phase_i's regex truncated
     "HbA1c" to "c" (the marker group does not allow digits).
  6. Out-of-template stress test: new phrasings and NEW fabricated
     clauses the model never saw in training. This is the honest
     estimate of how well it generalises beyond its own templates.

Run from the MediRAG root:   python phase_i_2_verifier_audit.py
"""
import json
import random
import re

import numpy as np

from results_logger import save_result
from phase_i_neural_verifier import (
    SYNTHETIC_DATA_PATH, MODEL_OUTPUT_DIR, MAX_LENGTH, RANDOM_SEED,
    STATEMENT_PATTERN, FABRICATED_CLAUSES, wrap_realistic,
)

FAITHFUL = 1
EXPECTED_VAL_SIZE = 720          # from eval_results.json (578.3 s x 1.245 samples/s)
STRESS_TEST_STATEMENTS = 60      # statements used for the out-of-template test
BATCH_SIZE = 8

CORE_PATTERN = re.compile(
    r"Your (.+?) is ([\d.]+)\s*(%|mg/dL)?, classified as (.+?)\.")

# Paraphrase templates and fabricated clauses that do NOT appear in phase_i
NEW_FAITHFUL_TEMPLATES = [
    "Your most recent {marker} reading was {value}{unit}, which falls in the {label} range.",
    "The report lists {marker} at {value}{unit}; this is categorised as {label}.",
    "For {marker}, your result came back as {value}{unit} ({label}).",
]
NEW_FABRICATED_CLAUSES = [
    " This rise is most likely due to the festive season diet.",
    " Your thyroid levels are probably contributing to this result.",
    " This pattern usually means your kidneys are under strain.",
    " You were probably fasting for less than eight hours before this test.",
    " This reading suggests your current medicine is no longer working.",
]


# -----------------------------
# Helpers
# -----------------------------
def context_statements(context):
    """{marker_lower: (value_float, label_lower)} for every statement in a chunk."""
    out = {}
    for marker, value, unit, label in STATEMENT_PATTERN.findall(context):
        try:
            out[marker.strip().lower()] = (float(value), label.strip().lower())
        except ValueError:
            pass
    return out


def example_type(pair):
    """Infer how an example was built, from its text (phase_i did not store this)."""
    expl, label = pair["explanation"], pair["label"]
    n_claims = expl.count("classified as")
    if n_claims > 1:
        return "multi_fact_faithful" if label == FAITHFUL else "multi_fact_partial_wrong"
    if label == FAITHFUL:
        return "faithful"
    if any(clause.strip() in expl for clause in FABRICATED_CLAUSES):
        return "fabricated_clause"
    m = CORE_PATTERN.search(expl)
    if not m:
        return "unknown_negative"
    marker, value = m.group(1).strip().lower(), float(m.group(2))
    truth = context_statements(pair["context"]).get(marker)
    if truth and abs(truth[0] - value) < 1e-6:
        return "wrong_label"
    return "wrong_value"


def predict_batch(tokenizer, model, contexts, explanations):
    import torch
    probs_all = []
    for i in range(0, len(contexts), BATCH_SIZE):
        enc = tokenizer(contexts[i:i + BATCH_SIZE], explanations[i:i + BATCH_SIZE],
                        truncation=True, max_length=MAX_LENGTH, padding=True,
                        return_tensors="pt")
        with torch.no_grad():
            logits = model(**enc).logits
        probs_all.append(torch.softmax(logits, dim=-1)[:, FAITHFUL].numpy())
        done = min(i + BATCH_SIZE, len(contexts))
        if done % 80 == 0 or done == len(contexts):
            print(f"  scored {done}/{len(contexts)}")
    return np.concatenate(probs_all)


def metrics(y_true, y_pred):
    from sklearn.metrics import confusion_matrix, precision_recall_fscore_support
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    p, r, f, s = precision_recall_fscore_support(y_true, y_pred, labels=[0, 1], zero_division=0)
    return {
        "n": int(len(y_true)),
        "accuracy": float((y_true == y_pred).mean()),
        "confusion": {"hallucinated_caught": int(tn), "hallucinated_missed": int(fp),
                      "faithful_wrongly_flagged": int(fn), "faithful_accepted": int(tp)},
        "faithful_class": {"precision": float(p[1]), "recall": float(r[1]), "f1": float(f[1]), "n": int(s[1])},
        "hallucinated_class": {"precision": float(p[0]), "recall": float(r[0]), "f1": float(f[0]), "n": int(s[0])},
        "macro_f1": float((f[0] + f[1]) / 2),
    }


def build_stress_test(val_pairs):
    """Out-of-template examples built from validation-set faithful statements."""
    rng = random.Random(RANDOM_SEED)
    seeds = []
    for p in val_pairs:
        if p["label"] == FAITHFUL and p["explanation"].count("classified as") == 1:
            m = CORE_PATTERN.search(p["explanation"])
            if m:
                seeds.append((p["context"], m.group(1).strip(), m.group(2), m.group(3) or "", m.group(4).strip()))
    rng.shuffle(seeds)
    seeds = seeds[:STRESS_TEST_STATEMENTS]

    items = []
    for ctx, marker, value, unit, label in seeds:
        if marker.lower() == "c":
            marker = "HbA1c"  # phase_i's regex truncates "HbA1c" to "c"; test the real name
        tmpl = rng.choice(NEW_FAITHFUL_TEMPLATES)
        faithful = tmpl.format(marker=marker, value=value, unit=unit, label=label)
        shift = rng.choice([-3, -2, -1.5, 1.5, 2, 3])
        wrong_val = round(max(float(value) + shift, 0.1), 1)
        items.append((ctx, wrap_realistic(faithful), 1, "paraphrased_faithful"))
        items.append((ctx, wrap_realistic(tmpl.format(marker=marker, value=wrong_val, unit=unit, label=label)),
                      0, "paraphrased_wrong_value"))
        items.append((ctx, wrap_realistic(faithful) + rng.choice(NEW_FABRICATED_CLAUSES),
                      0, "new_fabricated_clause"))
    return items


# -----------------------------
# Main
# -----------------------------
def main():
    from sklearn.model_selection import train_test_split
    from transformers import AutoTokenizer, AutoModelForSequenceClassification

    with open(SYNTHETIC_DATA_PATH) as f:
        pairs = json.load(f)
    train_pairs, val_pairs = train_test_split(
        pairs, test_size=0.2, random_state=RANDOM_SEED, stratify=[p["label"] for p in pairs])
    print(f"Pairs: {len(pairs)} | train {len(train_pairs)} | validation {len(val_pairs)}")
    if len(val_pairs) != EXPECTED_VAL_SIZE:
        print(f"WARNING: expected {EXPECTED_VAL_SIZE} validation pairs. synthetic_pairs.json may have "
              f"been rebuilt after training, so this split may not match Table III.")

    # ---- Leakage check (no model needed) ----
    train_contexts = {p["context"] for p in train_pairs}
    train_core = set()
    for p in train_pairs:
        for m in CORE_PATTERN.finditer(p["explanation"]):
            train_core.add((p["context"], m.group(1).strip().lower(), m.group(2)))
    ctx_shared = np.mean([p["context"] in train_contexts for p in val_pairs])
    stmt_shared = []
    for p in val_pairs:
        m = CORE_PATTERN.search(p["explanation"])
        if m:
            truth = context_statements(p["context"]).get(m.group(1).strip().lower())
            if truth:
                stmt_shared.append(any(k[0] == p["context"] and k[1] == m.group(1).strip().lower()
                                       for k in train_core))
    leakage = {"val_examples_whose_report_chunk_is_in_train": float(ctx_shared),
               "val_examples_whose_statement_also_appears_in_train": float(np.mean(stmt_shared)) if stmt_shared else None}
    print(f"\nLeakage: {ctx_shared:.1%} of validation examples use a report chunk seen in training; "
          f"{leakage['val_examples_whose_statement_also_appears_in_train']:.1%} test a statement "
          f"that also appears (in some form) in training.")

    truncated = sum("Your c is" in p["explanation"] for p in pairs)
    print(f"Pairs whose explanation says 'Your c is' (HbA1c truncated by regex): "
          f"{truncated} of {len(pairs)} ({truncated / len(pairs):.1%})")
    leakage["pairs_with_truncated_HbA1c_marker"] = int(truncated)

    types = [example_type(p) for p in val_pairs]
    print("Validation set composition:", {t: types.count(t) for t in sorted(set(types))})

    # ---- Load model and score the validation set ----
    print(f"\nLoading verifier from {MODEL_OUTPUT_DIR} ...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_OUTPUT_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_OUTPUT_DIR)
    model.eval()

    print("\nScoring validation set (same examples as Table III):")
    p_faith = predict_batch(tokenizer, model, [p["context"] for p in val_pairs],
                            [p["explanation"] for p in val_pairs])
    y_true = [p["label"] for p in val_pairs]
    y_pred = (p_faith >= 0.5).astype(int)
    val_metrics = metrics(y_true, y_pred)

    by_type = {}
    for t in sorted(set(types)):
        idx = [i for i, x in enumerate(types) if x == t]
        by_type[t] = {"n": len(idx),
                      "accuracy": float(np.mean([y_pred[i] == y_true[i] for i in idx]))}

    # ---- Out-of-template stress test ----
    print("\nScoring out-of-template stress test:")
    stress = build_stress_test(val_pairs)
    s_prob = predict_batch(tokenizer, model, [s[0] for s in stress], [s[1] for s in stress])
    s_true = [s[2] for s in stress]
    s_pred = (s_prob >= 0.5).astype(int)
    stress_metrics = metrics(s_true, s_pred)
    stress_by_type = {}
    for t in sorted({s[3] for s in stress}):
        idx = [i for i, s in enumerate(stress) if s[3] == t]
        stress_by_type[t] = {"n": len(idx),
                             "accuracy": float(np.mean([s_pred[i] == s_true[i] for i in idx]))}

    # ---- Report ----
    def show(title, m):
        print(f"\n{title}  (n={m['n']}, accuracy {m['accuracy']:.3f}, macro-F1 {m['macro_f1']:.3f})")
        for cls in ("hallucinated_class", "faithful_class"):
            c = m[cls]
            print(f"  {cls:<20} precision {c['precision']:.3f}  recall {c['recall']:.3f}  "
                  f"F1 {c['f1']:.3f}  (n={c['n']})")
        print(f"  confusion: {m['confusion']}")

    show("VALIDATION SET (Table III)", val_metrics)
    print("  accuracy by example type:")
    for t, v in by_type.items():
        print(f"    {t:<26} {v['accuracy']:.3f}  (n={v['n']})")
    show("OUT-OF-TEMPLATE STRESS TEST", stress_metrics)
    print("  accuracy by example type:")
    for t, v in stress_by_type.items():
        print(f"    {t:<26} {v['accuracy']:.3f}  (n={v['n']})")

    save_result("verifier", "verifier_audit", {
        "split": {"total_pairs": len(pairs), "train": len(train_pairs), "validation": len(val_pairs)},
        "leakage": leakage,
        "validation": val_metrics, "validation_by_type": by_type,
        "stress_test": stress_metrics, "stress_test_by_type": stress_by_type,
    }, notes="Table III audit: both-class metrics, per-type accuracy, leakage, out-of-template test")


if __name__ == "__main__":
    main()