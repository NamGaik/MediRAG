"""
phase_d_2_label_check.py

Re-runs the LABEL-STRIPPED nearest-neighbour check (Table I, check c) correctly.

The original strip_labels() removed "(Classification: ...)" but left the line
"Overall Glycemic Status: <label>." in every chunk - the very label the check
compares. This script removes BOTH, embeds the remaining raw values with each
model, and reports agreement two ways:
  * same-patient-inclusive (excludes only the chunk itself), as in the original
  * cross-patient (excludes all chunks of the same patient), the stricter version

It does NOT overwrite any existing embeddings, index or metadata files.
No API calls. Takes a few minutes on CPU (Bio_ClinicalBERT is the slow part).

Run from the MediRAG root:   python phase_d_2_label_check.py
"""
import json
import os
import re

import numpy as np

from results_logger import save_result

MANIFEST_PATH = os.path.join("preprocessed", "chunks_manifest.json")
MINILM = "sentence-transformers/all-MiniLM-L6-v2"
BCB = "emilyalsentzer/Bio_ClinicalBERT"


def strip_all_labels(text):
    text = re.sub(r"\(Classification:[^)]*\)", "", text)
    text = re.sub(r"Overall\s+Glycemic\s+Status:[^\n.]*\.?", "", text, flags=re.IGNORECASE)
    return text.strip()


def load():
    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)
    texts, meta = [], []
    for e in manifest:
        p = e["chunk_file"].replace("\\", "/")
        if not os.path.exists(p):
            continue
        with open(p) as f:
            texts.append(strip_all_labels(f.read()))
        meta.append({"pid": e["Patient_ID"], "status": e.get("Overall_Status", "Unknown")})
    return texts, meta


def embed_minilm(texts):
    from sentence_transformers import SentenceTransformer
    m = SentenceTransformer(MINILM)
    m.max_seq_length = 512
    return m.encode(texts, convert_to_numpy=True, show_progress_bar=True)


def embed_bcb(texts):
    import torch
    from transformers import AutoTokenizer, AutoModel
    tok, model = AutoTokenizer.from_pretrained(BCB), AutoModel.from_pretrained(BCB)
    model.eval()
    out = []
    with torch.no_grad():
        for i, t in enumerate(texts, 1):
            enc = tok(t, return_tensors="pt", truncation=True, max_length=512)
            h = model(**enc).last_hidden_state
            mask = enc["attention_mask"].unsqueeze(-1)
            out.append(((h * mask).sum(1) / mask.sum(1)).squeeze(0).numpy())
            if i % 25 == 0 or i == len(texts):
                print(f"  Bio_ClinicalBERT {i}/{len(texts)}")
    return np.array(out)


def agreement(emb, meta, cross_patient):
    from sklearn.metrics.pairwise import cosine_similarity
    sim = cosine_similarity(emb)
    agree = 0
    for i in range(len(meta)):
        s = sim[i].copy()
        s[i] = -np.inf
        if cross_patient:
            for j in range(len(meta)):
                if meta[j]["pid"] == meta[i]["pid"]:
                    s[j] = -np.inf
        agree += meta[int(np.argmax(s))]["status"] == meta[i]["status"]
    return agree, len(meta)


def main():
    texts, meta = load()
    leftover = sum(bool(re.search(r"\b(Normal|Prediabetic|Diabetic)\b", t)) for t in texts)
    print(f"Loaded {len(texts)} chunks. Example after stripping:\n---\n{texts[0]}\n---")
    print(f"Chunks still containing a status word after stripping: {leftover} (should be 0)\n")

    results = {}
    for name, fn in (("MiniLM", embed_minilm), ("Bio_ClinicalBERT", embed_bcb)):
        emb = fn(texts)
        for label, cross in (("same_patient_inclusive", False), ("cross_patient", True)):
            a, n = agreement(emb, meta, cross)
            results[f"{name}_{label}"] = {"agree": int(a), "n": n, "rate": round(a / n, 4)}
            print(f"{name:<17} label-stripped, {label:<23} {a}/{n} = {a / n:.2%}")

    save_result("embedding", "label_stripped_corrected", results,
                notes="Table I check (c) with classification AND overall-status text removed")


if __name__ == "__main__":
    main()