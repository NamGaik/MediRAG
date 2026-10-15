"""
phase_e_vector_db.py

Phase E + F for Medi-RAG: Vector Database + Retrieval Module

Takes the embeddings saved by phase_d_embedding.py and:
1. Builds a FAISS index (Phase E) using BioClinicalBERT vectors -- the
   brief's recommended model for the final system, since Phase D's
   comparison report is what you use to justify that choice in the paper.
2. Saves the index to disk so you don't have to rebuild it every run.
3. Provides a retrieve_top_k() function (Phase F) that takes a plain-text
   query, embeds it with the SAME model/pooling method used in Phase D,
   and returns the top-k most similar chunks with their original text
   and metadata.

Why BioClinicalBERT and not MiniLM here:
    The brief recommends BioClinicalBERT for the final system. If your
    Phase D comparison report shows MiniLM actually scores higher on
    check (c) (label-stripped agreement) for your data, swap
    ACTIVE_MODEL below to "minilm" -- everything else in this file
    works either way.

Why FAISS and not ChromaDB:
    The brief recommends FAISS for research work (this project) and
    ChromaDB for deployment later. FAISS is simpler, has no server to
    run, and is what your evaluation numbers should be based on.

Output:
    vector_db/faiss_index.index        -- the saved FAISS index
    vector_db/index_to_metadata.json   -- maps FAISS row number -> chunk metadata
                                           (needed because FAISS only stores vectors,
                                           not your patient/month/text info)

Run this from your MediRAG root folder (same level as embeddings/),
AFTER phase_d_embedding.py has already produced its .npy and .json files.

Requirements:
    pip install faiss-cpu numpy transformers torch
"""

import os
import json
import numpy as np

# -----------------------------
# Config
# -----------------------------
EMBEDDINGS_DIR = "embeddings"
VECTOR_DB_DIR = "vector_db"

# ADJUST HERE if you want to switch which model's embeddings power retrieval.
# Must match a pair of files that actually exist in embeddings/.
ACTIVE_MODEL = "bioclinicalbert"   # "bioclinicalbert" or "minilm"

MODEL_FILES = {
    "bioclinicalbert": os.path.join(EMBEDDINGS_DIR, "bioclinicalbert_embeddings.npy"),
    "minilm": os.path.join(EMBEDDINGS_DIR, "minilm_embeddings.npy"),
}
METADATA_PATH = os.path.join(EMBEDDINGS_DIR, "embeddings_metadata.json")

FAISS_INDEX_PATH = os.path.join(VECTOR_DB_DIR, "faiss_index.index")
INDEX_METADATA_PATH = os.path.join(VECTOR_DB_DIR, "index_to_metadata.json")

BIOCLINICALBERT_MODEL_NAME = "emilyalsentzer/Bio_ClinicalBERT"
MINILM_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

os.makedirs(VECTOR_DB_DIR, exist_ok=True)


# -----------------------------
# Phase E: Build and save the FAISS index
# -----------------------------
def build_index():
    """
    Loads the chosen model's embeddings + metadata, normalizes the vectors
    (so inner-product search behaves like cosine similarity -- this matches
    the brief's "Cosine Similarity" spec for Phase F), and saves a FAISS
    index plus a metadata lookup file to vector_db/.
    """
    import faiss

    embeddings_path = MODEL_FILES[ACTIVE_MODEL]
    if not os.path.exists(embeddings_path):
        raise FileNotFoundError(
            f"Could not find {embeddings_path}. Run phase_d_embedding.py first, "
            f"or check ACTIVE_MODEL matches a file that exists in embeddings/."
        )
    if not os.path.exists(METADATA_PATH):
        raise FileNotFoundError(f"Could not find {METADATA_PATH}. Run phase_d_embedding.py first.")

    print(f"Loading '{ACTIVE_MODEL}' embeddings from {embeddings_path} ...")
    embeddings = np.load(embeddings_path).astype("float32")

    with open(METADATA_PATH, "r") as f:
        metadata = json.load(f)

    if embeddings.shape[0] != len(metadata):
        raise ValueError(
            f"Mismatch: {embeddings.shape[0]} embedding rows but {len(metadata)} "
            f"metadata entries. These must line up 1:1 -- re-run phase_d_embedding.py."
        )

    dim = embeddings.shape[1]
    print(f"Loaded {embeddings.shape[0]} vectors of dimension {dim}.")

    # Normalize so FAISS's inner-product search == cosine similarity
    faiss.normalize_L2(embeddings)

    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    print(f"Built FAISS index with {index.ntotal} vectors.")

    faiss.write_index(index, FAISS_INDEX_PATH)
    with open(INDEX_METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"Saved index      -> {FAISS_INDEX_PATH}")
    print(f"Saved index-meta -> {INDEX_METADATA_PATH}")

    return index, metadata


def load_index():
    """Load a previously built index instead of rebuilding it every run."""
    import faiss

    if not os.path.exists(FAISS_INDEX_PATH) or not os.path.exists(INDEX_METADATA_PATH):
        print("No saved index found -- building it now.")
        return build_index()

    index = faiss.read_index(FAISS_INDEX_PATH)
    with open(INDEX_METADATA_PATH, "r") as f:
        metadata = json.load(f)
    return index, metadata


# -----------------------------
# Query embedding (must match phase_d_embedding.py exactly)
# -----------------------------
_query_model_cache = {}


def embed_query(query_text):
    """
    Embeds a single query string using the SAME model + pooling method as
    Phase D used for the chunks. If these two don't match, similarity
    scores become meaningless -- the query and the chunks must live in
    the same vector space.
    """
    import torch

    if ACTIVE_MODEL == "bioclinicalbert":
        if "bioclinicalbert" not in _query_model_cache:
            from transformers import AutoTokenizer, AutoModel
            print(f"Loading {BIOCLINICALBERT_MODEL_NAME} for query embedding...")
            tokenizer = AutoTokenizer.from_pretrained(BIOCLINICALBERT_MODEL_NAME)
            model = AutoModel.from_pretrained(BIOCLINICALBERT_MODEL_NAME)
            model.eval()
            _query_model_cache["bioclinicalbert"] = (tokenizer, model)
        tokenizer, model = _query_model_cache["bioclinicalbert"]

        with torch.no_grad():
            inputs = tokenizer(query_text, return_tensors="pt", truncation=True, max_length=512, padding=True)
            outputs = model(**inputs)
            token_embeddings = outputs.last_hidden_state
            attention_mask = inputs["attention_mask"].unsqueeze(-1)
            summed = (token_embeddings * attention_mask).sum(dim=1)
            counts = attention_mask.sum(dim=1)
            mean_pooled = (summed / counts).squeeze(0).numpy()
        return mean_pooled.astype("float32")

    elif ACTIVE_MODEL == "minilm":
        if "minilm" not in _query_model_cache:
            from sentence_transformers import SentenceTransformer
            print(f"Loading {MINILM_MODEL_NAME} for query embedding...")
            model = SentenceTransformer(MINILM_MODEL_NAME)
            model.max_seq_length = 512
            _query_model_cache["minilm"] = model
        model = _query_model_cache["minilm"]
        embedding = model.encode(query_text, convert_to_numpy=True)
        return embedding.astype("float32")

    else:
        raise ValueError(f"Unknown ACTIVE_MODEL: {ACTIVE_MODEL}")


# -----------------------------
# Phase F: Retrieval
# -----------------------------
def retrieve_top_k(query_text, k=5, index=None, metadata=None, patient_filter=None):
    """
    The brief's Phase F, in one function call:
        query text -> embedding -> cosine similarity search -> top-k chunks

    patient_filter (optional):
        Pass a Patient_ID string (e.g. "P032") to restrict the search to
        ONLY that patient's chunks. Without this, similarity search has
        no concept of "this question is about one specific person" --
        it just matches on text, and strong repeated words like "HbA1c"
        or "Diabetic" can easily outweigh a patient ID mentioned in the
        query. Use this whenever the question is clearly about one named
        patient (e.g. trend questions) -- leave it as None for general
        cross-patient questions.

    Returns a list of dicts, each with the chunk's original text, its
    similarity score, and its patient/month metadata -- ready to be
    dropped straight into your Phase G prompt to the LLM.
    """
    import faiss

    if index is None or metadata is None:
        index, metadata = load_index()

    query_vec = embed_query(query_text).reshape(1, -1)
    faiss.normalize_L2(query_vec)

    # If filtering to one patient, search for more candidates than k so
    # that after filtering out every other patient, we likely still have
    # k results left. FAISS has no built-in "only search these rows"
    # option for a flat index, so we over-fetch then filter in Python.
    search_k = k if patient_filter is None else len(metadata)  # search all 150, then filter

    scores, indices = index.search(query_vec, search_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue  # FAISS pads with -1 if fewer than k vectors exist
        entry = metadata[idx]

        if patient_filter is not None and entry.get("Patient_ID") != patient_filter:
            continue  # skip chunks belonging to other patients

        chunk_text = ""
        chunk_path = entry.get("chunk_file", "")
        if chunk_path and os.path.exists(chunk_path):
            with open(chunk_path, "r") as f:
                chunk_text = f.read()

        results.append({
            "similarity_score": round(float(score), 4),
            "Patient_ID": entry.get("Patient_ID"),
            "Month": entry.get("Month"),
            "Overall_Status": entry.get("Overall_Status"),
            "text": chunk_text,
        })

        if len(results) >= k:
            break  # got enough matching results, no need to keep scanning

    return results


# -----------------------------
# Main
# -----------------------------
def main():
    print(f"Active retrieval model: {ACTIVE_MODEL}\n")

    index, metadata = load_index()

    # ADJUST HERE -- swap these for real queries once you wire up Phase G

    # General query (no patient filter) -- can and often will pull from
    # multiple patients, since plain similarity search has no concept of
    # "one specific person" unless you tell it to.
    general_query = "Is HbA1c improving over the last 3 months?"
    print(f"\nGeneral query: \"{general_query}\"")
    print("Top-5 retrieved chunks (any patient):\n")
    results = retrieve_top_k(general_query, k=5, index=index, metadata=metadata)
    for i, r in enumerate(results, start=1):
        print(f"{i}. {r['Patient_ID']} / {r['Month']}  (score={r['similarity_score']}, status={r['Overall_Status']})")
        preview = r["text"][:120].replace("\n", " ")
        print(f"   {preview}...\n")

    # Patient-filtered query -- restricts search to one patient's own
    # chunks, so questions about a specific person's history actually
    # retrieve THAT person's months, not whoever has similar wording.
    patient_query = "How has HbA1c changed across visits?"
    target_patient = "P032"
    print(f"\nPatient-filtered query: \"{patient_query}\" (patient_filter=\"{target_patient}\")")
    print(f"Top chunks for {target_patient} only:\n")
    filtered_results = retrieve_top_k(
        patient_query, k=5, index=index, metadata=metadata, patient_filter=target_patient
    )
    if not filtered_results:
        print(f"   No chunks found for {target_patient} -- check the Patient_ID matches your data exactly.\n")
    for i, r in enumerate(filtered_results, start=1):
        print(f"{i}. {r['Patient_ID']} / {r['Month']}  (score={r['similarity_score']}, status={r['Overall_Status']})")
        preview = r["text"][:120].replace("\n", " ")
        print(f"   {preview}...\n")

    print("Phase E/F complete. Output is ready for Phase G (LLM Generation).")


if __name__ == "__main__":
    main()