"""
phase_l_4_audit_benchmark.py

Audits the SAVED benchmark results. No API calls, no model loading, runs in seconds.

Reads:
    evaluation/benchmark_results.json        (original run: whole-answer verifier labels)
    evaluation/benchmark_results_final.json  (after rescore_verifier + rescore_rules)
    data/Synthetic_diabetes_dataset1.xlsx    (true values, to help human labelling)

Reports (printed + saved to results/benchmark/benchmark_audit.json):
    1. How many queries were actually evaluated, per category
    2. Trap safety per configuration as k/n with a 95% confidence interval
    3. Rule flag rate per configuration as k/n
    4. Fig. 6 counts: whole-answer vs claim-decomposition verifier labels,
       how many answers were "not verifiable", and claim-level counts

Writes two labelling sheets (open in Excel, fill the human_label column):
    evaluation/label_verifier_claims.csv  every claim the verifier scored,
                                          with the patient's true values
    evaluation/label_trap_answers.csv     every trap answer, with the
                                          automatic trap_safe verdict

Run from the MediRAG root:   python phase_l_4_audit_benchmark.py
"""
import csv
import json
import math
import os
import re

import pandas as pd

from results_logger import save_result

ORIGINAL_PATH = os.path.join("evaluation", "benchmark_results.json")
FINAL_PATH = os.path.join("evaluation", "benchmark_results_final.json")
DATA_PATH = os.path.join("data", "Synthetic_diabetes_dataset1.xlsx")
CLAIM_SHEET = os.path.join("evaluation", "label_verifier_claims.csv")
TRAP_SHEET = os.path.join("evaluation", "label_trap_answers.csv")

VARIANTS = ["plain_llm", "standard_rag", "rag_with_rules", "full_system"]
CATEGORIES = ["category_a", "category_c"]
VALUE_COLS = ["HbA1c(%)", "FBS (mg/dL)", "PPBS (mg/dL)", "LDL", "HDL", "Triglycerides"]


def wilson(k, n, z=1.96):
    """95% Wilson confidence interval for a proportion k/n."""
    if n == 0:
        return None, None
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return round(max(0.0, centre - half), 3), round(min(1.0, centre + half), 3)


def fmt(k, n):
    lo, hi = wilson(k, n)
    rate = f"{k / n:.3f}" if n else "n/a"
    return f"{k}/{n} = {rate}  (95% CI {lo}-{hi})" if n else "0/0"


def load_true_values():
    """{(patient_id, month_number): {biomarker: value}} from the dataset."""
    if not os.path.exists(DATA_PATH):
        return {}
    df = pd.read_excel(DATA_PATH, sheet_name="Laboratory_Reports")
    df.columns = [c.strip() for c in df.columns]
    df = df[df["Patient_ID"].astype(str).str.match(r"^P\d+$")]
    out = {}
    for _, row in df.iterrows():
        m = re.search(r"(\d+)", str(row["Month"]))
        if m:
            out[(row["Patient_ID"], int(m.group(1)))] = {c: row.get(c) for c in VALUE_COLS if c in df.columns}
    return out


def entries(results):
    for cat in CATEGORIES:
        for e in results.get(cat, []):
            yield cat, e


def main():
    with open(FINAL_PATH) as f:
        final = json.load(f)
    original = None
    if os.path.exists(ORIGINAL_PATH):
        with open(ORIGINAL_PATH) as f:
            original = json.load(f)
    truth = load_true_values()
    report = {}

    # 1. Query counts
    counts = {cat: len(final.get(cat, [])) for cat in CATEGORIES}
    report["queries_evaluated"] = counts
    print("=== 1. Queries evaluated ===")
    print(f"  category_a (patient queries): {counts['category_a']}")
    print(f"  category_c (trap queries):    {counts['category_c']}")

    # 2. Trap safety
    print("\n=== 2. Trap safety (Table IV) ===")
    report["trap_safety"] = {}
    for v in VARIANTS:
        vals = [e[v].get("trap_safe") for _, e in entries(final)
                if _ == "category_c" and v in e and e[v].get("trap_safe") is not None]
        k, n = sum(bool(x) for x in vals), len(vals)
        lo, hi = wilson(k, n)
        report["trap_safety"][v] = {"safe": k, "n": n, "rate": k / n if n else None, "ci95": [lo, hi]}
        print(f"  {v:<16} {fmt(k, n)}")

    # 3. Rule flags (answer level)
    print("\n=== 3. Rule flag rate, answer level (any flag in the answer) ===")
    report["rule_flags"] = {}
    for v in VARIANTS:
        vals = [e[v].get("rule_flagged") for _, e in entries(final)
                if v in e and e[v].get("rule_flagged") is not None]
        k, n = sum(bool(x) for x in vals), len(vals)
        report["rule_flags"][v] = {"flagged": k, "n": n}
        print(f"  {v:<16} {fmt(k, n)}")

    # 4. Verifier (Fig. 6)
    print("\n=== 4. Verifier on full_system answers (Fig. 6) ===")
    def label_counts(results):
        c = {"faithful": 0, "hallucinated": 0, "not_verifiable": 0, "missing": 0}
        for _, e in entries(results):
            lab = e.get("full_system", {}).get("verifier_label")
            c[lab if lab in c else "missing"] += 1
        return c

    new = label_counts(final)
    report["verifier_claim_decomposition_answers"] = new
    if original:
        old = label_counts(original)
        report["verifier_whole_answer_answers"] = old
        print(f"  Whole-answer scoring (original run): {old}")
        print(f"    faithful rate = {fmt(old['faithful'], old['faithful'] + old['hallucinated'])}")
    print(f"  Claim decomposition (rescored):      {new}")
    print(f"    faithful rate = {fmt(new['faithful'], new['faithful'] + new['hallucinated'])}")

    checked = skipped = corrected = claims_faithful = 0
    claim_rows = []
    for cat, e in entries(final):
        fs = e.get("full_system", {})
        checked += fs.get("verifier_claims_checked", 0) or 0
        skipped += fs.get("verifier_claims_skipped", 0) or 0
        corrected += fs.get("verifier_corrections_excluded", 0) or 0
        for c in fs.get("verifier_claim_details", []) or []:
            claims_faithful += c.get("predicted_label") == "faithful"
            m = re.search(r"month[\s_]*(\d+)", c.get("claim", ""), re.IGNORECASE)
            true_vals = truth.get((e.get("patient_id"), int(m.group(1)))) if m else None
            claim_rows.append({
                "query_id": e.get("query_id"), "category": cat, "patient_id": e.get("patient_id"),
                "claim": c.get("claim"), "verifier_label": c.get("predicted_label"),
                "faithful_confidence": c.get("faithful_confidence"),
                "true_values_that_month": json.dumps(true_vals) if true_vals else "",
                "human_label (faithful/hallucinated)": "", "notes": "",
            })
    report["verifier_claims"] = {"checked": checked, "skipped_no_single_chunk": skipped,
                                 "corrections_excluded": corrected,
                                 "checked_and_labelled_faithful": claims_faithful}
    print(f"  Claims checked: {checked} | skipped (no single-month match): {skipped} | "
          f"corrections excluded: {corrected}")
    print(f"  Claim-level faithful rate = {fmt(claims_faithful, checked)}")

    # Labelling sheets
    os.makedirs("evaluation", exist_ok=True)
    if claim_rows:
        with open(CLAIM_SHEET, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(claim_rows[0].keys()))
            w.writeheader()
            w.writerows(claim_rows)
        print(f"\nWrote {len(claim_rows)} claims to label -> {CLAIM_SHEET}")

    trap_rows = []
    for cat, e in entries(final):
        if cat != "category_c":
            continue
        for v in VARIANTS:
            if v in e:
                trap_rows.append({
                    "query_id": e.get("query_id"), "variant": v, "query_text": e.get("query_text"),
                    "trap_type": e.get("trap_type", ""), "expected_behaviour": e.get("expected_behaviour", ""),
                    "answer": e[v].get("answer", ""), "auto_trap_safe": e[v].get("trap_safe"),
                    "human_trap_safe (yes/no)": "", "notes": "",
                })
    if trap_rows:
        with open(TRAP_SHEET, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(trap_rows[0].keys()))
            w.writeheader()
            w.writerows(trap_rows)
        print(f"Wrote {len(trap_rows)} trap answers to label -> {TRAP_SHEET}")

    save_result("benchmark", "benchmark_audit", report,
                notes="Counts and CIs behind Table IV, Table V and Fig. 6")


if __name__ == "__main__":
    main()