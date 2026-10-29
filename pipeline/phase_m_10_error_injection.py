"""
phase_m_10_error_injection.py   (Upgrade U7b -- no API calls, no labelling)

Problem: the benchmark has only 5 erroneous patient answers (3 among grounded
answers), too few to measure how well the checkers detect errors.

Solution: CONTROLLED ERROR INJECTION. Take every grounded patient answer that
the authors labelled CORRECT, and create copies with exactly one known error:

  E1 value_perturbed   a patient value changed slightly (e.g. HbA1c 6.1 -> 6.5)
                       -> the new value is NOT in the record
  E2 value_swapped     a value replaced by the same biomarker's value from
                       another visit -> the new value IS in the record (wrong month)
  E3 label_flipped     a classification changed (e.g. Prediabetic -> Normal)
  E4 trend_reversed    a trend word reversed (e.g. "increased" -> "decreased")
  E5 claim_added       an unsupported patient-specific sentence appended
                       (a kidney-function claim; no such data exists)

The originals are the negatives (correct), the injected copies the positives,
so every detector gets hundreds of labelled cases with known ground truth.
The injection rules were fixed before any detector was scored on them.

Detectors:
  rule_v1   rule validator as used in the paper (phase_h)          [always]
  rule_v3   revised validator, F1-F3 (phase_m_3)                   [always]
  verifier  fine-tuned Bio_ClinicalBERT, claim level  [--with-verifier, needs models/]
  nli       zero-shot NLI cross-encoder, sentence level   [--with-nli, downloads model]
  *_routed  the learned checker, with rule-confirmed claims/sentences skipped

Usage (from the MediRAG root):
    python pipeline/phase_m_10_error_injection.py
    python pipeline/phase_m_10_error_injection.py --with-verifier --with-nli
Output:
    verifier_data/injected_answers.json
    results/benchmark_v2/error_injection_run1.json
"""
import argparse
import glob
import json
import os
import random
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from phase_h_validation import load_severity_rules, validate_entry, NUMBER_PATTERN, LABEL_PATTERN
from phase_l_7_labels_v2 import read_labels, load_results, LABEL_DIR, NA
from phase_l_8_rescore_rules_v2 import forecast_chunk, thresholds_by_biomarker
from phase_m_3_routed_verification import (validate_v3, validate_v4, claim_confirmed_by_rules,
                                           detector, patient_chunks)
from results_logger import save_result

SEED = 42
CHUNK_DIR = os.path.join("preprocessed", "chunks")
GROUNDED = ("standard_rag", "full_system", "full_system_corrective")
ERROR_TYPES = ("value_perturbed", "value_swapped", "label_flipped", "trend_reversed", "claim_added")
LINE = re.compile(r"^(HbA1c|Fasting Blood Sugar \(FBS\)|Post-Prandial Blood Sugar \(PPBS\)|"
                  r"LDL Cholesterol|HDL Cholesterol|Triglycerides):\s*([\d.]+)", re.M)
NAME = {"HbA1c": "HbA1c", "Fasting Blood Sugar (FBS)": "FBS", "Post-Prandial Blood Sugar (PPBS)": "PPBS",
        "LDL Cholesterol": "LDL", "HDL Cholesterol": "HDL", "Triglycerides": "TG"}
STEP = {"HbA1c": 0.4, "FBS": 12, "PPBS": 18, "LDL": 15, "HDL": 8, "TG": 25}
FLIP = {"normal": "Prediabetic", "prediabetic": "Normal", "diabetic": "Prediabetic",
        "optimal": "High", "borderline": "Optimal", "high": "Optimal"}
TREND = [("increased", "decreased"), ("decreased", "increased"), ("rose", "fell"), ("fell", "rose"),
         ("rising", "falling"), ("falling", "rising"), ("higher", "lower"), ("lower", "higher"),
         ("improved", "worsened"), ("worsened", "improved"), ("improving", "worsening"),
         ("worsening", "improving"), ("upward", "downward"), ("downward", "upward")]
ADDED = " Your kidney function results also declined across these visits, which is worth monitoring."


def retrieved_chunks(pid):
    """Same shape as retrieve_top_k() output, so the verifier can match months."""
    out = []
    months = sorted(int(re.search(r"_Month_(\d+)\.txt$", p).group(1))
                    for p in glob.glob(os.path.join(CHUNK_DIR, f"{pid}_Month_*.txt")))
    for m in months:
        p = os.path.join(CHUNK_DIR, f"{pid}_Month_{m}.txt")
        if os.path.exists(p):
            with open(p) as f:
                t = f.read()
            status = re.search(r"Overall Glycemic Status:\s*(\w+)", t)
            out.append({"Patient_ID": pid, "Month": f"Month_{m}", "month": m, "text": t,
                        "Overall_Status": status.group(1) if status else None,
                        "similarity_score": None})
    return out


def record_values(chunks):
    """{biomarker: {month: value}} parsed from the patient's chunks."""
    vals = defaultdict(dict)
    for c in chunks:
        for name, v in LINE.findall(c["text"]):
            vals[NAME[name]][c["month"]] = float(v)
    return vals


def fmt_like(old_str, new_val):
    decimals = len(old_str.split(".")[1]) if "." in old_str else 0
    return f"{new_val:.{decimals}f}"


def value_spans(answer, vals):
    """Number spans in the answer that equal exactly one biomarker's recorded value."""
    lookup = defaultdict(set)
    for b, months in vals.items():
        for v in months.values():
            lookup[round(v, 2)].add(b)
    spans = []
    for m in NUMBER_PATTERN.finditer(answer):
        if re.search(r"(month|visit)s?\s*$", answer[max(0, m.start() - 8):m.start()], re.I):
            continue
        hits = lookup.get(round(float(m.group(1)), 2), set())
        if len(hits) == 1:
            spans.append((m.start(), m.end(), next(iter(hits)), float(m.group(1)), m.group(1)))
    return spans


def inject(answer, vals, kind, rng):
    spans = value_spans(answer, vals)
    if kind in ("value_perturbed", "value_swapped", "label_flipped") and not spans:
        return None
    if kind == "value_perturbed":
        s, e, b, v, raw = rng.choice(spans)
        recorded = {round(x, 2) for x in vals[b].values()}
        for sign in rng.sample([1, -1], 2):
            nv = round(v + sign * STEP[b], 2)
            if nv > 0 and nv not in recorded:
                return answer[:s] + fmt_like(raw, nv) + answer[e:]
        return None
    if kind == "value_swapped":
        rng.shuffle(spans)
        for s, e, b, v, raw in spans:
            others = [x for x in vals[b].values() if abs(x - v) > 1e-6]
            if others:
                return answer[:s] + fmt_like(raw, rng.choice(others)) + answer[e:]
        return None
    if kind == "label_flipped":
        rng.shuffle(spans)
        for s, e, b, v, raw in spans:
            nxt = NUMBER_PATTERN.search(answer, e)
            stop = min(nxt.start() if nxt else len(answer), e + 60)
            lab = LABEL_PATTERN.search(answer, e, stop)
            if lab and lab.group(1).lower() in FLIP:
                new = FLIP[lab.group(1).lower()]
                if lab.group(1)[0].islower():
                    new = new.lower()
                return answer[:lab.start()] + new + answer[lab.end():]
        return None
    if kind == "trend_reversed":
        for a, b in TREND:
            m = re.search(rf"\b{a}\b", answer, re.I)
            if m:
                rep = b.capitalize() if m.group(0)[0].isupper() else b
                return answer[:m.start()] + rep + answer[m.end():]
        return None
    if kind == "claim_added":
        return answer.rstrip() + ADDED
    raise ValueError(kind)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", type=int, default=1)
    ap.add_argument("--with-verifier", action="store_true")
    ap.add_argument("--with-nli", action="store_true")
    ap.add_argument("--nli-model", default="cross-encoder/nli-deberta-v3-base")
    ap.add_argument("--nli-threshold", type=float, default=0.7)
    a = ap.parse_args()
    rng = random.Random(SEED)

    results = load_results(a.run_id)
    with open(os.path.join(LABEL_DIR, "KEY_do_not_open.json")) as f:
        key = json.load(f)["key"]
    pl, _ = read_labels("patient", ["all_values_correct (yes/no)", "unsupported_claim (yes/no)"])
    rules = load_severity_rules()
    thresholds = thresholds_by_biomarker(rules)

    # ---- build the injected set from answers the authors labelled CORRECT ----
    cases = []
    for lid, v in sorted(pl.items()):
        if lid not in key or key[lid]["config"] not in GROUNDED:
            continue
        vals_ok, unsup = v["all_values_correct (yes/no)"], v["unsupported_claim (yes/no)"]
        if vals_ok is not True or unsup is not False:
            continue
        q, c = key[lid]["query_id"], key[lid]["config"]
        rec = results[q]
        e = rec["configs"][c]
        chunks = retrieved_chunks(rec["patient_id"])
        base = {"query_id": q, "config": c, "patient_id": rec["patient_id"],
                "query_text": rec["query_text"], "trajectory": e.get("trajectory")}
        cases.append({**base, "kind": "original", "error": False, "answer": e["answer"]})
        vals = record_values(chunks)
        for kind in ERROR_TYPES:
            new = inject(e["answer"], vals, kind, rng)
            if new and new != e["answer"]:
                cases.append({**base, "kind": kind, "error": True, "answer": new})
    os.makedirs("verifier_data", exist_ok=True)
    with open(os.path.join("verifier_data", "injected_answers.json"), "w") as f:
        json.dump(cases, f, indent=1)
    counts = defaultdict(int)
    for x in cases:
        counts[x["kind"]] += 1
    print("Cases:", dict(counts))

    # ---- optional learned checkers ----
    verify = nli = None
    if a.with_verifier:
        from phase_i_neural_verifier import verify_answer_by_matched_chunks as verify
    if a.with_nli:
        from phase_m_7_nli_baseline import NLI, sentences, rule_confirmed
        nli = NLI(a.nli_model)

    # ---- score every case ----
    for x in cases:
        chunks = retrieved_chunks(x["patient_id"])
        ctx = chunks + forecast_chunk(x["trajectory"])
        v1 = validate_entry({"answer": x["answer"], "retrieved_chunks": ctx}, rules)
        x["rule_v1"] = any(i["type"] in ("misclassification", "possible_fabrication")
                           and not (i["type"] == "possible_fabrication"
                                    and round(i["value"], 2) in thresholds[i["biomarker"].lower()])
                           for i in v1["issues"])
        x["rule_v3"] = bool(validate_v3(x["answer"], x["query_text"], ctx, rules, thresholds)["issues"])
        x["rule_v4"] = bool(validate_v4(x["answer"], x["query_text"], ctx, rules, thresholds)["issues"])
        if verify:
            res = verify(x["answer"], chunks)
            claims = res.get("claim_results", [])
            x["verifier"] = any(cl["predicted_label"] == "hallucinated" for cl in claims)
            x["verifier_routed"] = any(cl["predicted_label"] == "hallucinated"
                                       and not claim_confirmed_by_rules(cl["claim"], chunks)
                                       for cl in claims)
            x["verifier_assessed"] = bool(claims)
        if nli:
            premise = "\n".join(c["text"] for c in ctx)
            sents = sentences(x["answer"])
            probs = nli.contradiction_probs(premise, sents)
            x["nli"] = max(probs, default=0.0) >= a.nli_threshold
            x["nli_routed"] = max([p for s, p in zip(sents, probs) if not rule_confirmed(s, premise)],
                                  default=0.0) >= a.nli_threshold

    detectors = ["rule_v1", "rule_v3", "rule_v4"] + (["verifier", "verifier_routed"] if verify else []) \
        + (["nli", "nli_routed"] if nli else [])
    out = {"run_id": a.run_id, "seed": SEED, "cases": dict(counts), "detectors": {}}
    originals = [x for x in cases if not x["error"]]
    print(f"\n{'detector':<17}{'false alarms':>15}" + "".join(f"{t[:14]:>16}" for t in ERROR_TYPES)
          + f"{'all errors':>13}")
    for d in detectors:
        fa = sum(x[d] for x in originals) / len(originals)
        row = {"false_alarm_rate": round(fa, 3), "detection_rate": {}}
        for t in ERROR_TYPES:
            pos = [x for x in cases if x["kind"] == t]
            row["detection_rate"][t] = round(sum(x[d] for x in pos) / len(pos), 3) if pos else None
        allpos = [x for x in cases if x["error"]]
        row["detection_rate"]["all"] = round(sum(x[d] for x in allpos) / len(allpos), 3)
        out["detectors"][d] = row
        print(f"{d:<17}{fa:>15.2f}" + "".join(
            f"{row['detection_rate'][t]:>16.2f}" if row["detection_rate"][t] is not None else f"{'-':>16}"
            for t in ERROR_TYPES) + f"{row['detection_rate']['all']:>13.2f}")
    if verify:
        out["verifier_assessed_share"] = round(sum(x["verifier_assessed"] for x in cases) / len(cases), 3)
        print(f"\nVerifier could assess {out['verifier_assessed_share']:.0%} of cases "
              "(the rest have no single-visit claim and count as 'not flagged').")
    print("\nRows: share of ORIGINAL (correct) answers flagged = false alarms;"
          " share of INJECTED answers flagged per error type = detection rate.")
    # ---- v4 on the REAL author-labelled answers (same rows as Table VII) ----
    real = []
    for lid, v in pl.items():
        if lid not in key:
            continue
        vals_ok, unsup = v["all_values_correct (yes/no)"], v["unsupported_claim (yes/no)"]
        if vals_ok is None or unsup is None or unsup == NA:
            continue
        q, c = key[lid]["query_id"], key[lid]["config"]
        rec = results[q]; e = rec["configs"][c]
        ctx = [] if c == "plain_llm" else patient_chunks(rec["patient_id"]) + forecast_chunk(e.get("trajectory"))
        real.append((bool(validate_v4(e["answer"], rec["query_text"], ctx, rules, thresholds)["issues"]),
                     vals_ok is False or unsup is True))
    print("\nRule validator v4 on the real author-labelled answers:")
    out["rule_v4_real_answers"] = detector("Rule validator v4", real)
    save_result("benchmark_v2", f"error_injection_run{a.run_id}", out,
                notes="U7b: controlled error injection into correct grounded answers")


if __name__ == "__main__":
    main()
