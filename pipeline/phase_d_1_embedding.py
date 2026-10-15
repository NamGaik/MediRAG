"""
phase_d_embeddings.py

Phase D for Medi-RAG: Embedding Generation

Converts the semantic text chunks from Phase C into vector embeddings,
using BOTH candidate models from the project brief so they can be
compared before picking one for the final system:

    Option 1: Sentence Transformers (all-MiniLM-L6-v2)  -- fast, general-purpose
    Option 2: BioClinicalBERT                             -- medical-domain (brief's
                                                              recommended choice)

What this does:
1. Loads every chunk listed in preprocessed/chunks_manifest.json
2. Generates embeddings for each chunk using both models
3. Saves both sets of vectors (+ metadata) to embeddings/
4. Runs THREE similarity comparisons, from least to most rigorous:

   a) Same-patient-inclusive nearest-neighbor agreement (original check).
      Easy to satisfy: a chunk's nearest neighbor is often just the SAME
      patient's other month, and/or the classification words ("Normal",
      "Diabetic") are literally repeated in the chunk text, so this number
      tends to be inflated and doesn't cleanly measure clinical understanding.

   b) Cross-patient nearest-neighbor agreement.
      Excludes a chunk's own patient when searching for its nearest
      neighbor, so a high score means the model found a genuinely
      DIFFERENT patient with clinically similar values -- a stronger
      signal than (a).

   c) Label-stripped nearest-neighbor agreement.
      Removes the "(Classification: ...)" text before embedding, so the
      model can't just pattern-match on the literal word "Normal" /
      "Diabetic" repeated in the chunk. A high score here means the model
      inferred clinical similarity from the raw lab values themselves --
      the most meaningful of the three checks for deciding which model
      actually understands the medical content.

   Report (c) [and ideally (b) as well] in your paper's model comparison
   table -- (a) alone overstates how "smart" the embeddings are.

Output:
    embeddings/minilm_embeddings.npy               (N x 384 float array)
    embeddings/bioclinicalbert_embeddings.npy      (N x 768 float array)
    embeddings/minilm_embeddings_stripped.npy      (N x 384, label-stripped text)
    embeddings/bioclinicalbert_embeddings_stripped.npy (N x 768, label-stripped text)
    embeddings/embeddings_metadata.json            (which row = which patient/month)
    embeddings/model_comparison_report.json        (all three agreement results)

Run this from your MediRAG root folder (same level as preprocessed/).

Requirements:
    pip install sentence-transformers torch numpy scikit-learn transformers

Note: BioClinicalBERT is a much larger model (~400MB download on first run,
needs a HuggingFace-compatible setup) and is noticeably slower than MiniLM,
especially on CPU. This is expected -- the brief recommends it specifically
because medical-domain pretraining should produce more clinically meaningful
embeddings, at the cost of speed. The comparisons below let you see whether
that tradeoff is actually worth it for your data.
"""

import os
import re
import json
import numpy as np

# -----------------------------
# Config
# -----------------------------
MANIFEST_PATH = os.path.join("preprocessed", "chunks_manifest.json")
OUT_DIR = "embeddings"

MINILM_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
BIOCLINICALBERT_MODEL_NAME = "emilyalsentzer/Bio_ClinicalBERT"

MINILM_OUT_PATH = os.path.join(OUT_DIR, "minilm_embeddings.npy")
BIOCLINICALBERT_OUT_PATH = os.path.join(OUT_DIR, "bioclinicalbert_embeddings.npy")
MINILM_STRIPPED_OUT_PATH = os.path.join(OUT_DIR, "minilm_embeddings_stripped.npy")
BIOCLINICALBERT_STRIPPED_OUT_PATH = os.path.join(OUT_DIR, "bioclinicalbert_embeddings_stripped.npy")
METADATA_PATH = os.path.join(OUT_DIR, "embeddings_metadata.json")
COMPARISON_REPORT_PATH = os.path.join(OUT_DIR, "model_comparison_report.json")

os.makedirs(OUT_DIR, exist_ok=True)


# -----------------------------
# Load chunks
# -----------------------------
def load_chunks():
    """Load every chunk's text + metadata, in a fixed order shared by both models."""
    with open(MANIFEST_PATH, "r") as f:
        manifest = json.load(f)

    texts = []
    metadata = []
    for entry in manifest:
        # normalize path separators so this works whether the manifest was
        # written on Windows ("preprocessed\\chunks\\...") or Linux/Mac
        chunk_path = entry["chunk_file"].replace("\\", "/")
        if not os.path.exists(chunk_path):
            print(f"  Warning: chunk file missing, skipping: {chunk_path}")
            continue
        with open(chunk_path, "r") as f:
            text = f.read()
        texts.append(text)
        metadata.append({
            "Patient_ID": entry["Patient_ID"],
            "Month": entry["Month"],
            "Overall_Status": entry.get("Overall_Status", "Unknown"),
            "Source_Quality": entry.get("Source_Quality", "Unknown"),
            "chunk_file": chunk_path,
        })

    return texts, metadata


def strip_labels(text):
    """
    Remove '(Classification: ...)' segments from a chunk so the embedding
    model can't just pattern-match on the literal word "Normal"/"Diabetic"
    repeated across the chunk. What's left is just raw values, e.g.:

        "HbA1c: 5.2%. Fasting Blood Sugar (FBS): 72.0 mg/dL. ..."

    Used only for the label-stripped comparison check -- the UNSTRIPPED
    text is still what you embed for the actual RAG knowledge base, since
    the explicit classifications are useful grounding for Phase G generation.
    """
    return re.sub(r"\(Classification:[^)]*\)", "", text).strip()


# -----------------------------
# Embedding generation
# -----------------------------
def generate_minilm_embeddings(texts):
    from sentence_transformers import SentenceTransformer
    print(f"Loading {MINILM_MODEL_NAME} ...")
    model = SentenceTransformer(MINILM_MODEL_NAME)
    # bump past the model's default 256-token limit so long chunks aren't
    # truncated more aggressively than BioClinicalBERT's 512-token limit
    model.max_seq_length = 512
    print("Generating MiniLM embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    return embeddings


def generate_bioclinicalbert_embeddings(texts):
    """
    BioClinicalBERT isn't a sentence-transformers model out of the box --
    it's a raw HuggingFace transformer, so we mean-pool its token-level
    output to get one vector per chunk (the standard approach for turning
    a BERT-family model into sentence embeddings without extra fine-tuning).
    """
    import torch
    from transformers import AutoTokenizer, AutoModel

    print(f"Loading {BIOCLINICALBERT_MODEL_NAME} ...")
    tokenizer = AutoTokenizer.from_pretrained(BIOCLINICALBERT_MODEL_NAME)
    model = AutoModel.from_pretrained(BIOCLINICALBERT_MODEL_NAME)
    model.eval()

    print("Generating BioClinicalBERT embeddings...")
    embeddings = []
    with torch.no_grad():
        for i, text in enumerate(texts):
            inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
            outputs = model(**inputs)
            # mean-pool over token embeddings, masking out padding tokens
            token_embeddings = outputs.last_hidden_state
            attention_mask = inputs["attention_mask"].unsqueeze(-1)
            summed = (token_embeddings * attention_mask).sum(dim=1)
            counts = attention_mask.sum(dim=1)
            mean_pooled = (summed / counts).squeeze(0).numpy()
            embeddings.append(mean_pooled)
            if (i + 1) % 10 == 0 or (i + 1) == len(texts):
                print(f"  Processed {i + 1}/{len(texts)}")

    return np.array(embeddings)


# -----------------------------
# Comparisons
# -----------------------------
def cosine_sim_matrix(embeddings):
    from sklearn.metrics.pairwise import cosine_similarity
    return cosine_similarity(embeddings)


def evaluate_nearest_neighbor_agreement(embeddings, metadata, model_name):
    """
    (a) Same-patient-inclusive check (original).
    For each chunk, find its single nearest neighbor (excluding only itself)
    and check whether that neighbor has the same Overall_Status. Easiest of
    the three checks to satisfy -- treat as a coarse sanity check only.
    """
    sim_matrix = cosine_sim_matrix(embeddings)
    n = len(metadata)
    agreements = 0
    details = []

    for i in range(n):
        sims = sim_matrix[i].copy()
        sims[i] = -1  # exclude self
        nearest_idx = int(np.argmax(sims))

        same_status = metadata[i]["Overall_Status"] == metadata[nearest_idx]["Overall_Status"]
        agreements += int(same_status)

        details.append({
            "chunk": f"{metadata[i]['Patient_ID']}_{metadata[i]['Month']}",
            "status": metadata[i]["Overall_Status"],
            "nearest_neighbor": f"{metadata[nearest_idx]['Patient_ID']}_{metadata[nearest_idx]['Month']}",
            "neighbor_status": metadata[nearest_idx]["Overall_Status"],
            "same_status": same_status,
            "similarity_score": round(float(sims[nearest_idx]), 4),
        })

    agreement_rate = round((agreements / n) * 100, 2) if n > 0 else 0.0
    print(f"[{model_name}] (a) Same-patient-inclusive agreement: {agreement_rate}% ({agreements}/{n})")

    return {
        "check": "same_patient_inclusive",
        "model": model_name,
        "agreement_rate_percent": agreement_rate,
        "agreements": agreements,
        "total": n,
        "details": details,
    }


def evaluate_cross_patient_agreement(embeddings, metadata, model_name):
    """
    (b) Cross-patient check.
    Excludes a chunk's OWN patient (all of that patient's months) when
    searching for its nearest neighbor. A high score here means the model
    found a genuinely different patient with clinically similar values,
    rather than just recognizing "this looks like the same person."
    """
    sim_matrix = cosine_sim_matrix(embeddings)
    n = len(metadata)
    agreements = 0
    details = []

    for i in range(n):
        sims = sim_matrix[i].copy()
        for j in range(n):
            if metadata[j]["Patient_ID"] == metadata[i]["Patient_ID"]:
                sims[j] = -1  # exclude self AND same patient's other months
        nearest_idx = int(np.argmax(sims))

        same_status = metadata[i]["Overall_Status"] == metadata[nearest_idx]["Overall_Status"]
        agreements += int(same_status)

        details.append({
            "chunk": f"{metadata[i]['Patient_ID']}_{metadata[i]['Month']}",
            "status": metadata[i]["Overall_Status"],
            "nearest_neighbor": f"{metadata[nearest_idx]['Patient_ID']}_{metadata[nearest_idx]['Month']}",
            "neighbor_status": metadata[nearest_idx]["Overall_Status"],
            "same_status": same_status,
            "similarity_score": round(float(sims[nearest_idx]), 4),
        })

    agreement_rate = round((agreements / n) * 100, 2) if n > 0 else 0.0
    print(f"[{model_name}] (b) Cross-patient agreement: {agreement_rate}% ({agreements}/{n})")

    return {
        "check": "cross_patient",
        "model": model_name,
        "agreement_rate_percent": agreement_rate,
        "agreements": agreements,
        "total": n,
        "details": details,
    }


# -----------------------------
# Main
# -----------------------------
def main():
    print("Loading chunks from Phase C output...")
    texts, metadata = load_chunks()
    print(f"Loaded {len(texts)} chunks.\n")

    if len(texts) == 0:
        print("No chunks found -- check that Phase C has been run and chunks_manifest.json exists.")
        return

    stripped_texts = [strip_labels(t) for t in texts]

    comparison_results = {}

    # --- MiniLM (full text) ---
    minilm_embeddings = generate_minilm_embeddings(texts)
    np.save(MINILM_OUT_PATH, minilm_embeddings)
    print(f"Saved MiniLM embeddings: {minilm_embeddings.shape} -> {MINILM_OUT_PATH}")

    # --- MiniLM (label-stripped text, for check (c)) ---
    minilm_stripped_embeddings = generate_minilm_embeddings(stripped_texts)
    np.save(MINILM_STRIPPED_OUT_PATH, minilm_stripped_embeddings)
    print(f"Saved MiniLM (stripped) embeddings: {minilm_stripped_embeddings.shape} -> {MINILM_STRIPPED_OUT_PATH}")

    # --- BioClinicalBERT (full text + label-stripped) ---
    bioclinicalbert_available = False
    try:
        bioclinicalbert_embeddings = generate_bioclinicalbert_embeddings(texts)
        np.save(BIOCLINICALBERT_OUT_PATH, bioclinicalbert_embeddings)
        print(f"Saved BioClinicalBERT embeddings: {bioclinicalbert_embeddings.shape} -> {BIOCLINICALBERT_OUT_PATH}")

        bioclinicalbert_stripped_embeddings = generate_bioclinicalbert_embeddings(stripped_texts)
        np.save(BIOCLINICALBERT_STRIPPED_OUT_PATH, bioclinicalbert_stripped_embeddings)
        print(f"Saved BioClinicalBERT (stripped) embeddings: {bioclinicalbert_stripped_embeddings.shape} -> {BIOCLINICALBERT_STRIPPED_OUT_PATH}")

        bioclinicalbert_available = True
    except Exception as e:
        print(f"\nCould not generate BioClinicalBERT embeddings: {e}")
        print("Continuing with MiniLM results only. Install 'transformers' and 'torch' and re-run to include BioClinicalBERT.")

    # --- Save metadata (shared index for both embedding files) ---
    with open(METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"\nSaved shared metadata index: {METADATA_PATH}")

    # --- (a) Same-patient-inclusive comparison ---
    print("\n=== (a) Same-Patient-Inclusive Nearest-Neighbor Agreement ===")
    comparison_results["MiniLM_a_same_patient_inclusive"] = evaluate_nearest_neighbor_agreement(
        minilm_embeddings, metadata, "MiniLM (all-MiniLM-L6-v2)"
    )
    if bioclinicalbert_available:
        comparison_results["BioClinicalBERT_a_same_patient_inclusive"] = evaluate_nearest_neighbor_agreement(
            bioclinicalbert_embeddings, metadata, "BioClinicalBERT"
        )

    # --- (b) Cross-patient comparison ---
    print("\n=== (b) Cross-Patient Nearest-Neighbor Agreement ===")
    comparison_results["MiniLM_b_cross_patient"] = evaluate_cross_patient_agreement(
        minilm_embeddings, metadata, "MiniLM (all-MiniLM-L6-v2)"
    )
    if bioclinicalbert_available:
        comparison_results["BioClinicalBERT_b_cross_patient"] = evaluate_cross_patient_agreement(
            bioclinicalbert_embeddings, metadata, "BioClinicalBERT"
        )

    # --- (c) Label-stripped comparison (most meaningful for the paper) ---
    print("\n=== (c) Label-Stripped Nearest-Neighbor Agreement ===")
    comparison_results["MiniLM_c_label_stripped"] = evaluate_nearest_neighbor_agreement(
        minilm_stripped_embeddings, metadata, "MiniLM (label-stripped)"
    )
    if bioclinicalbert_available:
        comparison_results["BioClinicalBERT_c_label_stripped"] = evaluate_nearest_neighbor_agreement(
            bioclinicalbert_stripped_embeddings, metadata, "BioClinicalBERT (label-stripped)"
        )

    with open(COMPARISON_REPORT_PATH, "w") as f:
        json.dump(comparison_results, f, indent=2)
    print(f"\nSaved comparison report: {COMPARISON_REPORT_PATH}")

    print("\nPhase D complete. Output is ready for Phase E (Vector Database).")


if __name__ == "__main__":
    main()