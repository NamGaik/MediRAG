"""
phase_m_7_nli_baseline.py   (Upgrade U7 -- no API calls, no training; downloads a
                             pretrained NLI model from Hugging Face once)

A zero-shot baseline for the fine-tuned Bio_ClinicalBERT verifier: an
off-the-shelf natural-language-inference (NLI) cross-encoder, applied
sentence by sentence (SummaC-style) to the SAVED v2 benchmark answers.

  premise    = the patient's visit records (+ the labelled forecast for
               full-system answers), exactly the context the LLM saw
  hypothesis = one sentence of the answer
  A sentence is flagged if P(contradiction) >= threshold. "Neutral" is NOT
  flagged, because the prompt allows clearly-marked general background.
  An answer is flagged if any sentence is flagged.
Routed variant: sentences whose numbers and labels the rule layer confirms
against the records are not sent to the NLI model (as in U3).

Compared with the author labels on the same patient answers as Table VII.

Usage (from the MediRAG root):
    python pipeline/phase_m_7_nli_baseline.py [--model cross-encoder/nli-deberta-v3-base]
Output:
    results/benchmark_v2/nli_baseline_run1.json
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from phase_h_validation import NUMBER_PATTERN, LABEL_PATTERN
from phase_l_7_labels_v2 import read_labels, load_results, LABEL_DIR, NA
from phase_l_8_rescore_rules_v2 import forecast_chunk
from phase_m_3_routed_verification import patient_chunks, detector
from results_logger import save_result

THRESHOLDS = (0.5, 0.7, 0.9)
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")
MD = re.compile(r"[*#_`>|]+")


def sentences(answer):
    out = []
    for s in SENT_SPLIT.split(answer or ""):
        s = MD.sub(" ", s).strip(" -•\t")
        s = re.sub(r"\s+", " ", s)
        if (len(s) >= 12 and NUMBER_PATTERN.search(s)) or len(s) >= 25:
            out.append(s)
    return out


def rule_confirmed(sentence, context_text):
    """True if every number and label in the sentence appears in the context."""
    nums = [float(n) for n in NUMBER_PATTERN.findall(sentence)]
    if not nums:
        return False
    ctx_nums = {float(n) for n in NUMBER_PATTERN.findall(context_text)}
    if not all(any(abs(n - c) < 1e-6 for c in ctx_nums) for n in nums):
        return False
    ctx_labels = {l.lower() for l in LABEL_PATTERN.findall(context_text)}
    return all(l.lower() in ctx_labels for l in LABEL_PATTERN.findall(sentence))


class NLI:
    def __init__(self, name):
        from sentence_transformers import CrossEncoder
        self.model = CrossEncoder(name, max_length=512)
        id2label = self.model.model.config.id2label
        self.contra = next(i for i, l in id2label.items() if "contra" in l.lower())
        print(f"Loaded {name}; labels {id2label}")

    def contradiction_probs(self, premise, hyps):
        if not hyps:
            return []
        import numpy as np
        logits = np.asarray(self.model.predict([(premise, h) for h in hyps]))
        e = np.exp(logits - logits.max(axis=1, keepdims=True))
        return list((e / e.sum(axis=1, keepdims=True))[:, self.contra])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", type=int, default=1)
    ap.add_argument("--model", default="cross-encoder/nli-deberta-v3-base")
    a = ap.parse_args()

    results = load_results(a.run_id)
    with open(os.path.join(LABEL_DIR, "KEY_do_not_open.json")) as f:
        key = json.load(f)["key"]
    pl, _ = read_labels("patient", ["all_values_correct (yes/no)", "unsupported_claim (yes/no)"])
    nli = NLI(a.model)

    rows = []
    for lid, v in pl.items():
        if lid not in key:
            continue
        vals, unsup = v["all_values_correct (yes/no)"], v["unsupported_claim (yes/no)"]
        if vals is None or unsup is None or unsup == NA:
            continue
        q, c = key[lid]["query_id"], key[lid]["config"]
        if c == "plain_llm":
            continue                      # no context to check against
        rec = results[q]
        e = rec["configs"][c]
        ctx = patient_chunks(rec["patient_id"]) + forecast_chunk(e.get("trajectory"))
        premise = "\n".join(x["text"] for x in ctx)
        sents = sentences(e["answer"])
        probs = nli.contradiction_probs(premise, sents)
        routed = [p for s, p in zip(sents, probs) if not rule_confirmed(s, premise)]
        rows.append({"label_id": lid, "query_id": q, "config": c,
                     "error": vals is False or unsup is True,
                     "n_sentences": len(sents), "max_contra": max(probs, default=0.0),
                     "max_contra_routed": max(routed, default=0.0),
                     "sentences_confirmed_by_rules": len(sents) - len(routed)})

    print(f"\nNLI baseline vs author labels (grounded patient answers, run {a.run_id})")
    out = {"run_id": a.run_id, "model": a.model, "by_threshold": {}}
    for t in THRESHOLDS:
        out["by_threshold"][str(t)] = {
            "nli": detector(f"NLI, contradiction >= {t}", [(r["max_contra"] >= t, r["error"]) for r in rows]),
            "nli_routed": detector(f"NLI + rule routing, >= {t}",
                                   [(r["max_contra_routed"] >= t, r["error"]) for r in rows]),
        }
    print("\nFor comparison, the fine-tuned verifier (paper): precision 0.20, recall 1.00 "
          "on the answers it could assess; rule override (U3): precision 0.50, recall 0.50.")
    print(f"Sentences checked: {sum(r['n_sentences'] for r in rows)}; "
          f"confirmed by rules and skipped in routed mode: "
          f"{sum(r['sentences_confirmed_by_rules'] for r in rows)}")
    print("Note: the NLI model assesses EVERY grounded answer (no 'not verifiable' cases).")
    out["rows"] = rows
    save_result("benchmark_v2", f"nli_baseline_run{a.run_id}", out,
                notes="U7: zero-shot NLI cross-encoder baseline vs author labels")


if __name__ == "__main__":
    main()