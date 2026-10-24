"""
phase_m_3_routed_verification.py   (Upgrade U3 -- no API calls, no GPU)

Re-scores the SAVED v2 benchmark answers with:
  1. Rule validator v3 -- four fixes for the false-alarm patterns found in
     the error analysis of Table VII:
       F1 quoted_from_question : a value the USER put in the question (e.g. a
                                 false-premise "9.2%") is not a fabrication
       F2 forecast_label       : labels inside a forecast sentence ("predicted
                                 risk category of Diabetic") are not checked
                                 against the measured value
       F3 parse_artifact       : implausible captures (e.g. TG = 2.0 taken from
                                 "Months 1 and 2") are ignored
       F4 label adjacency      : a label only counts for a value if it appears
                                 before the NEXT number in the sentence
                                 (fixes trend sentences "123 -> 107 -> 99, Normal")
  2. Routed verifier -- a verifier "hallucinated" flag on a claim is overridden
     when every number and label in that claim is confirmed by the rule layer
     against the claim's own month chunk.
  3. Ensemble -- answer flagged if rule v3 flags it OR the routed verifier does.

Compares all detectors against the author labels (same rows as Table VII).

Usage (from the MediRAG root):
    python pipeline/phase_m_3_routed_verification.py --run-id 1
Output:
    results/benchmark_v2/routed_verification_run1.json
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from phase_h_validation import (load_severity_rules, classify_value, extract_mentions,
                                extract_claimed_label, value_appears_in_context, broad_category,
                                NUMBER_PATTERN, LABEL_PATTERN)
from phase_l_7_labels_v2 import read_labels, load_results, LABEL_DIR, NA
from phase_l_8_rescore_rules_v2 import forecast_chunk, thresholds_by_biomarker
from results_logger import save_result

CHUNK_DIR = os.path.join("preprocessed", "chunks")

# Wide sanity bounds (NOT clinical thresholds): values outside these are parse artefacts.
PLAUSIBLE = {"HbA1c": (3.0, 20.0), "FBS": (20, 800), "PPBS": (20, 900),
             "LDL": (10, 500), "HDL": (5, 200), "TG": (20, 3000)}
FORECAST_WORDS = re.compile(r"predict|forecast|estimate|projected|risk category", re.I)
MONTH_IN_CLAIM = re.compile(r"month\s*(\d)", re.I)
# F4 was tested and is OFF by default: in the ablation it removed the only true
# detection (a trend sentence that wrongly implied earlier values were diabetic-range).
DEFAULT_FIXES = ("F1", "F2", "F3")


def patient_chunks(pid):
    out = []
    for m in (1, 2, 3):
        p = os.path.join(CHUNK_DIR, f"{pid}_Month_{m}.txt")
        if os.path.exists(p):
            with open(p) as f:
                out.append({"month": m, "text": f.read()})
    return out


def label_before_next_number(context):
    """F4: only accept a label that occurs before the next number."""
    nxt = NUMBER_PATTERN.search(context)
    return extract_claimed_label(context[:nxt.start()] if nxt else context)


def validate_v3(answer, query_text, ctx, rules, thresholds, fixes=DEFAULT_FIXES):
    has_ctx = any(c.get("text") for c in ctx)
    q_numbers = {float(n) for n in NUMBER_PATTERN.findall(query_text or "")}
    issues, ignored, checked = [], [], 0
    for m in extract_mentions(answer):
        b, v = m["biomarker"], m["value"]
        lo, hi = PLAUSIBLE.get(b, (float("-inf"), float("inf")))
        if "F3" in fixes and not lo <= v <= hi:
            ignored.append(("parse_artifact", b, v)); continue                    # F3
        true_label = classify_value(b, v, rules)
        if true_label is None:
            continue
        checked += 1
        if not value_appears_in_context(b, v, ctx):
            if not has_ctx:
                ignored.append(("unverifiable_no_context", b, v)); continue
            if round(v, 2) in thresholds[b.lower()]:
                ignored.append(("reference_threshold", b, v)); continue
            if "F1" in fixes and any(abs(v - n) < 1e-6 for n in q_numbers):
                ignored.append(("quoted_from_question", b, v)); continue           # F1
            issues.append(("possible_fabrication", b, v)); continue
        if "F2" in fixes and FORECAST_WORDS.search(m["context"]):
            ignored.append(("forecast_label", b, v)); continue                      # F2
        claimed = (label_before_next_number(m["context"]) if "F4" in fixes      # F4
                   else extract_claimed_label(m["context"]))
        if claimed is not None and broad_category(claimed) != broad_category(true_label):
            issues.append(("misclassification", b, v))
    return {"checked": checked, "issues": issues, "ignored": ignored}


def claim_confirmed_by_rules(claim, chunks):
    """True if every number and label in the claim appears in its own month chunk."""
    mm = MONTH_IN_CLAIM.search(claim)
    if not mm:
        return False
    chunk = next((c["text"] for c in chunks if c["month"] == int(mm.group(1))), None)
    if chunk is None:
        return False
    text = MONTH_IN_CLAIM.sub(" ", claim)
    nums = [float(n) for n in NUMBER_PATTERN.findall(text)]
    if not nums:
        return False
    chunk_nums = {float(n) for n in NUMBER_PATTERN.findall(chunk)}
    if not all(any(abs(n - c) < 1e-6 for c in chunk_nums) for n in nums):
        return False
    chunk_labels = {l.lower() for l in LABEL_PATTERN.findall(chunk)}
    return all(l.lower() in chunk_labels for l in LABEL_PATTERN.findall(text))


def routed_verifier_label(entry, chunks):
    claims = entry.get("verifier_claims") or []
    if not claims:
        return "not_verifiable", 0
    overridden, flagged = 0, False
    for c in claims:
        if c["label"] == "hallucinated":
            if claim_confirmed_by_rules(c["claim"], chunks):
                overridden += 1
            else:
                flagged = True
    return ("hallucinated" if flagged else "faithful"), overridden


def detector(name, flags):
    tp = sum(f and e for f, e in flags); fp = sum(f and not e for f, e in flags)
    fn = sum((not f) and e for f, e in flags); tn = sum((not f) and (not e) for f, e in flags)
    prec = round(tp / (tp + fp), 3) if tp + fp else None
    rec = round(tp / (tp + fn), 3) if tp + fn else None
    print(f"  {name:<30} TP {tp:>2}  FP {fp:>2}  FN {fn:>2}  TN {tn:>2}  "
          f"precision {prec}  recall {rec}  (n={len(flags)})")
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn, "precision": prec, "recall": rec, "n": len(flags)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", type=int, default=1)
    a = ap.parse_args()

    results = load_results(a.run_id)
    with open(os.path.join(LABEL_DIR, "KEY_do_not_open.json")) as f:
        key = json.load(f)["key"]
    pl, _ = read_labels("patient", ["all_values_correct (yes/no)", "unsupported_claim (yes/no)"])
    rules = load_severity_rules()
    thresholds = thresholds_by_biomarker(rules)

    rows, overrides, ignored_counts = [], 0, {}
    for lid, v in pl.items():
        if lid not in key:
            continue
        vals, unsup = v["all_values_correct (yes/no)"], v["unsupported_claim (yes/no)"]
        if vals is None or unsup is None or unsup == NA:
            continue
        q, c = key[lid]["query_id"], key[lid]["config"]
        rec = results[q]
        e = rec["configs"][c]
        err = vals is False or unsup is True
        chunks = patient_chunks(rec["patient_id"])
        ctx = [] if c == "plain_llm" else chunks + forecast_chunk(e.get("trajectory"))

        rule_v1 = any(t in ("misclassification", "possible_fabrication") for t in e["rule_issue_types"])
        v3 = validate_v3(e["answer"], rec["query_text"], ctx, rules, thresholds)
        for t, _, _ in v3["ignored"]:
            ignored_counts[t] = ignored_counts.get(t, 0) + 1
        rule_v3 = bool(v3["issues"])
        ver_v1 = e.get("verifier_label")
        ver_v2, n_over = routed_verifier_label(e, chunks) if c != "plain_llm" else ("not_verifiable", 0)
        overrides += n_over
        ensemble = rule_v3 or ver_v2 == "hallucinated"
        rows.append({"label_id": lid, "query_id": q, "config": c, "error": err,
                     "rule_v1": rule_v1, "rule_v3": rule_v3, "rule_v3_issues": v3["issues"],
                     "verifier_v1": ver_v1, "verifier_routed": ver_v2, "ensemble": ensemble})

    print(f"\nDetectors vs author label 'answer has an error' (patient answers, run {a.run_id})")
    out = {"run_id": a.run_id}
    out["rule_v1"] = detector("Rule validator (paper)", [(r["rule_v1"], r["error"]) for r in rows])
    out["rule_v3"] = detector("Rule validator v3 (F1-F3)", [(r["rule_v3"], r["error"]) for r in rows])
    vr = [r for r in rows if r["verifier_v1"] in ("faithful", "hallucinated")]
    out["verifier_v1"] = detector("Neural verifier (paper)",
                                  [(r["verifier_v1"] == "hallucinated", r["error"]) for r in vr])
    out["verifier_routed"] = detector("Verifier + rule override",
                                      [(r["verifier_routed"] == "hallucinated", r["error"]) for r in vr])
    out["ensemble"] = detector("Ensemble (rule v3 OR routed)", [(r["ensemble"], r["error"]) for r in rows])
    print("\nAblation: effect of each fix (F1-F3 removed one at a time; F4 added)")
    out["ablation"] = {}
    variants = {"without_F1": ("F2", "F3"), "without_F2": ("F1", "F3"),
                "without_F3": ("F1", "F2"), "with_F4": ("F1", "F2", "F3", "F4")}
    for drop, keep in variants.items():
        flags = []
        for r in rows:
            rec = results[r["query_id"]]; e = rec["configs"][r["config"]]
            ctx = ([] if r["config"] == "plain_llm" else
                   patient_chunks(rec["patient_id"]) + forecast_chunk(e.get("trajectory")))
            flags.append((bool(validate_v3(e["answer"], rec["query_text"], ctx, rules,
                                           thresholds, keep)["issues"]), r["error"]))
        out["ablation"][drop] = detector(f"Rule v3 {drop}", flags)
    out["verifier_claim_flags_overridden"] = overrides
    out["rule_v3_ignored_by_type"] = ignored_counts

    print(f"\nVerifier claim flags overridden by the rule layer: {overrides}")
    print(f"Rule v3 ignored mentions by reason: {ignored_counts}")
    print("\nRemaining rule-v3 flags (check each by eye):")
    for r in rows:
        if r["rule_v3"]:
            tag = "TRUE ERROR " if r["error"] else "false alarm"
            print(f"  [{tag}] {r['query_id']} {r['config']}: {r['rule_v3_issues']}")
    out["rows"] = rows
    save_result("benchmark_v2", f"routed_verification_run{a.run_id}", out,
                notes="U3: rule validator v3 + verifier override + ensemble vs author labels")


if __name__ == "__main__":
    main()
