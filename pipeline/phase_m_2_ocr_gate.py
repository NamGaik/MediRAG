"""
phase_m_2_ocr_gate.py   (Upgrade U2 -- no API calls, no GPU)

An OCR quality gate that sits between OCR extraction and preprocessing.
Every extracted value gets one status:
    ok                    passes all checks
    missing               nothing extracted        -> ask the user to re-upload / type it
    repaired_confirm      fixed by a known OCR pattern (e.g. "61" -> 6.1 for HbA1c)
                          -> shown to the user for confirmation, never used silently
    quarantined_range     outside wide sanity bounds
    quarantined_jump      implausible jump vs. the same patient's other visits
Only "ok" values reach the LLM. Everything else is shown to the user.

Evaluated on the saved OCR results (evaluation/ocr_evaluation_report.xlsx):
the key metric is the SILENT ERROR RATE -- wrong values that would reach
the LLM without any warning.

Usage (from the MediRAG root):
    python pipeline/phase_m_2_ocr_gate.py
Output:
    results/ocr/ocr_gate.json
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from results_logger import save_result

OCR_REPORT = os.path.join("evaluation", "ocr_evaluation_report.xlsx")
CLEAN_RECORDS = os.path.join("preprocessed", "clean_records.json")
FIELDS = ["HbA1c", "FBS", "PPBS", "LDL", "HDL", "Triglycerides"]

# Wide sanity bounds -- engineering limits, NOT clinical thresholds.
BOUNDS = {"HbA1c": (3.0, 20.0), "FBS": (20, 800), "PPBS": (20, 900),
          "LDL": (10, 500), "HDL": (5, 200), "Triglycerides": (20, 3000)}
# Largest believable change between consecutive monthly visits (configurable).
MAX_JUMP = {"HbA1c": 1.5, "FBS": 80, "PPBS": 100, "LDL": 60, "HDL": 25, "Triglycerides": 150}
CONFUSIONS = str.maketrans({"l": "1", "I": "1", "|": "1", "O": "0", "o": "0",
                            "S": "5", "B": "8", ",": "."})
NUM = re.compile(r"^\d+(\.\d+)?$")


def load_history():
    """Other-visit values per patient, used for the jump check."""
    hist = defaultdict(dict)
    with open(CLEAN_RECORDS) as f:
        for r in json.load(f):
            hist[r["Patient_ID"]][r["Month"]] = r
    return hist


def neighbours(hist, pid, month, field):
    """Values from the patient's OTHER months (never the month being checked)."""
    return [rec[field] for m, rec in hist.get(pid, {}).items()
            if m != month and isinstance(rec.get(field), (int, float))]


def gate(field, raw, pid, month, hist):
    s = str(raw).strip()
    if s == "":
        return "missing", None
    s = s.translate(CONFUSIONS).rstrip(".")
    repaired = s != str(raw).strip().rstrip(".")
    if not NUM.match(s):
        return "quarantined_range", None
    v = float(s)
    lo, hi = BOUNDS[field]
    if not lo <= v <= hi:
        # Known pattern: decimal point lost in HbA1c ("61" -> 6.1)
        if field == "HbA1c" and v.is_integer() and 30 <= v <= 200:
            return "repaired_confirm", v / 10
        return "quarantined_range", v
    others = neighbours(hist, pid, month, field)
    if others and min(abs(v - o) for o in others) > MAX_JUMP[field]:
        return "quarantined_jump", v
    return ("repaired_confirm" if repaired else "ok"), v


def main():
    df = pd.read_excel(OCR_REPORT, sheet_name="Detailed_Comparison", dtype=str, keep_default_na=False)
    df = df[df["Field"].isin(FIELDS)]
    hist = load_history()
    out = {}
    for img_type, g in df.groupby("Image_Type"):
        counts = Counter()
        examples = []
        for _, r in g.iterrows():
            truth = float(r["Ground_Truth_Value"])
            raw = r["OCR_Extracted_Value"]
            correct = r["Correct"].strip().lower() == "yes"
            status, val = gate(r["Field"], raw, r["Patient_ID"], r["Month"], hist)
            if correct:
                counts["correct_passed" if status == "ok" else "correct_flagged"] += 1
            elif str(raw).strip() == "":
                counts["missing_flagged"] += 1
            else:
                counts["wrong_silent" if status == "ok" else "wrong_caught"] += 1
                if status == "repaired_confirm" and val is not None and abs(val - truth) < 1e-6:
                    counts["wrong_repaired_exactly"] += 1
                examples.append({"file": r["File"], "field": r["Field"], "truth": truth,
                                 "ocr": raw, "gate": status, "gate_value": val})
        n = len(g)
        wrong_nonempty = counts["wrong_silent"] + counts["wrong_caught"]
        silent_before = wrong_nonempty            # without a gate every wrong value passes
        res = {"fields": n, **counts,
               "silent_error_rate_before": round(silent_before / n, 4),
               "silent_error_rate_after": round(counts["wrong_silent"] / n, 4),
               "false_flag_rate_on_correct": round(
                   counts["correct_flagged"] / max(1, counts["correct_passed"] + counts["correct_flagged"]), 4),
               "wrong_value_examples": examples}
        out[img_type] = res
        print(f"\n{img_type} images ({n} numeric fields)")
        print(f"  correct values passed           {counts['correct_passed']}")
        print(f"  correct values wrongly flagged  {counts['correct_flagged']}  "
              f"(false-flag rate {res['false_flag_rate_on_correct']})")
        print(f"  missing values flagged          {counts['missing_flagged']}")
        print(f"  wrong values caught             {counts['wrong_caught']}  "
              f"(repaired to the exact true value: {counts['wrong_repaired_exactly']})")
        print(f"  wrong values passed silently    {counts['wrong_silent']}")
        print(f"  SILENT ERROR RATE  before gate {res['silent_error_rate_before']}  "
              f"-> after gate {res['silent_error_rate_after']}")
        for e in examples:
            print(f"    {e['file']} {e['field']}: truth {e['truth']}, OCR '{e['ocr']}' -> {e['gate']} {e['gate_value']}")
    save_result("ocr", "ocr_gate", out, notes="U2: OCR quality gate on saved OCR evaluation")


if __name__ == "__main__":
    main()
