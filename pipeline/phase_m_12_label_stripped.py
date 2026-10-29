"""
phase_m_12_label_stripped.py  --  does MediRAG interpret values, or only copy labels?
(cohort 2; about 49 API calls per model, a few cents; then label 49 answers)

In the main benchmark, every report already states each value's classification
("HbA1c: 8.8% (Classification: Diabetic)") and the overall status. A correct answer
can therefore be produced by copying. This experiment removes every classification
and the overall-status line from the reports, and instead gives the laboratory's
reference ranges (the same ADA/WHO rules used to label the reports). The model must
now classify each value itself.

Everything else is identical to the full system in run 2: the same 49 patient
questions, the same retrieved chunks (top-k = 8, i.e. all visits), the same system
prompt and trajectory forecast. Only the output limit is 2,000 tokens (the fix
tested in phase_m_11).

Steps (MediRAG_cohort2 folder, with the 4 cohort-2 settings set in the window):
    $env:MEDIRAG_MODEL = "claude-haiku-5-5"
    python pipeline/phase_m_12_label_stripped.py run --dry-run   # shows one prompt, no API calls
    python pipeline/phase_m_12_label_stripped.py run             # 49 answers + label sheet
    # label evaluation/cohort2/labels/label_stripped_<model>.xlsx (same rules as label_patient.xlsx)
    python pipeline/phase_m_12_label_stripped.py score
Outputs:
    evaluation/cohort2/label_stripped_<model>.json
    evaluation/cohort2/labels/label_stripped_<model>.xlsx
    results/cohort2/label_stripped_<model>_scores.json
"""
import argparse
import glob
import json
import math
import os
import re
import sys

os.environ["MEDIRAG_MAX_TOKENS"] = "2000"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import phase_l_6_benchmark_v2 as bench  # noqa: E402
import phase_g_generation as phase_g  # noqa: E402

CHUNK_DIR = os.path.join("preprocessed", "chunks")
MODEL_TAG = bench.CLAUDE_MODEL.replace("claude-", "").replace(".", "-")
OUT_JSON = os.path.join("evaluation", "cohort2", f"label_stripped_{MODEL_TAG}.json")
SHEET = os.path.join("evaluation", "cohort2", "labels", f"label_stripped_{MODEL_TAG}.xlsx")
SCORES = os.path.join("results", "cohort2", f"label_stripped_{MODEL_TAG}_scores.json")

# The rules that produced the labels in the reports (phase_c_preprocessing.py).
REFERENCE_RANGES = """REFERENCE RANGES used by this laboratory (classifications are not printed on the reports):
- HbA1c: below 5.7% Normal; 5.7-6.4% Prediabetic; 6.5% or higher Diabetic.
- Fasting Blood Sugar (FBS): below 100 mg/dL Normal; 100-125 mg/dL Prediabetic; 126 mg/dL or higher Diabetic.
- Post-Prandial Blood Sugar (PPBS): below 140 mg/dL Normal; 140-199 mg/dL Prediabetic; 200 mg/dL or higher Diabetic.
- LDL Cholesterol: below 100 mg/dL Optimal; 100-129 mg/dL Borderline; 130 mg/dL or higher High Risk.
- HDL Cholesterol: Low if below 40 mg/dL (men) or below 50 mg/dL (women); otherwise Normal.
- Triglycerides: below 150 mg/dL Normal; 150-199 mg/dL Borderline; 200 mg/dL or higher High.
- Overall Glycemic Status: Diabetic if HbA1c or FBS is Diabetic; otherwise Prediabetic if HbA1c or FBS is Prediabetic; otherwise Normal."""

LABEL_RE = re.compile(r"\s*\(Classification:[^)]*\)")
STATUS_RE = re.compile(r"\n*\s*Overall Glycemic Status:[^\n]*", re.I)


def strip_labels(text):
    return STATUS_RE.sub("", LABEL_RE.sub("", text)).rstrip() + "\n"


def stripped_message(q, chunks):
    stripped = [dict(c, text=strip_labels(c["text"])) for c in chunks]
    for c in stripped:
        assert "Classification" not in c["text"] and "Overall Glycemic" not in c["text"], c["text"]
    trajectory = phase_g.get_trajectory_prediction(q["patient_id"])
    # Same layout as phase_g.build_context_block, minus its "(Status: ...)" header
    blocks = []
    for i, c in enumerate(stripped, start=1):
        sim = f" (similarity: {c['similarity_score']})" if c.get("similarity_score") is not None else ""
        blocks.append(f"[Chunk {i}] Patient {c['Patient_ID']}, {c['Month']}{sim}:\n{c['text']}\n")
    context = "\n".join(blocks) + "\n" + REFERENCE_RANGES
    for word in ("Status:", "Classification"):
        assert word not in "\n".join(blocks), word
    msg = phase_g.build_user_message(q["query_text"], context, phase_g.build_trajectory_block(trajectory))
    return msg, trajectory, stripped


def true_record(pid):
    """The patient's original labelled reports, compressed, for the labeller."""
    lines = []
    files = sorted(glob.glob(os.path.join(CHUNK_DIR, f"{pid}_Month_*.txt")),
                   key=lambda p: int(re.search(r"Month_(\d+)", p).group(1)))
    for p in files:
        t = open(p).read()
        m = re.search(r"Month_(\d+)", p).group(1)
        vals = re.findall(r"^(HbA1c|Fasting Blood Sugar|Post-Prandial Blood Sugar|LDL Cholesterol|HDL Cholesterol|"
                          r"Triglycerides)[^:]*:\s*([\d.]+)[^(]*\(Classification:\s*([^)]+)\)", t, re.M)
        short = {"HbA1c": "HbA1c", "Fasting Blood Sugar": "FBS", "Post-Prandial Blood Sugar": "PPBS",
                 "LDL Cholesterol": "LDL", "HDL Cholesterol": "HDL", "Triglycerides": "TG"}
        st = re.search(r"Overall Glycemic Status:\s*(\w+)", t)
        lines.append(f"M{m}: " + "; ".join(f"{short[n]} {v} ({c})" for n, v, c in vals)
                     + f"; Overall {st.group(1) if st else '?'}")
    return "\n".join(lines)


def run(dry):
    from phase_ef_vectorDB import load_index, retrieve_top_k
    if bench.TOP_K != 8:
        sys.exit(f'MEDIRAG_TOP_K is {bench.TOP_K}; cohort 2 needs 8. Run:  $env:MEDIRAG_TOP_K = "8"')
    qpath = os.environ.get("MEDIRAG_PATIENT_QUERIES")
    if not qpath or "cohort2" not in qpath:
        sys.exit('Set $env:MEDIRAG_PATIENT_QUERIES = "verifier_data/cohort2_patient_queries.json"')
    queries = json.load(open(qpath))
    index, metadata = load_index()
    out = json.load(open(OUT_JSON)) if os.path.exists(OUT_JSON) else {}
    for i, q in enumerate(queries, 1):
        if q["query_id"] in out:
            continue
        chunks = retrieve_top_k(q["query_text"], k=bench.TOP_K, index=index, metadata=metadata,
                                patient_filter=q["patient_id"])
        msg, trajectory, stripped = stripped_message(q, chunks)
        if dry:
            print("=" * 70, f"\nModel {bench.CLAUDE_MODEL}, max_tokens {bench.MAX_TOKENS}\n", msg)
            print("\nDry run: no API calls made.")
            return
        text, usage, model_id = bench.claude([{"role": "user", "content": msg}], system=phase_g.SYSTEM_PROMPT)
        out[q["query_id"]] = {**q, "answer": text, "usage": usage, "model_id": model_id,
                              "trajectory": trajectory, "true_record": true_record(q["patient_id"])}
        print(f"[{i}/{len(queries)}] {q['query_id']} tokens={usage['output_tokens']}")
        os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
        json.dump(out, open(OUT_JSON, "w"), indent=1)    # saved after every answer (safe to restart)
    make_sheet(out)


def make_sheet(out):
    import pandas as pd
    rows = [{"query_id": k, "patient_id": v["patient_id"], "question": v["query_text"],
             "reference_facts": v.get("reference", ""), "true_record (with correct classes)": v["true_record"],
             "answer": v["answer"], "all_values_correct": "", "unsupported_claim": "", "notes": ""}
            for k, v in sorted(out.items())]
    os.makedirs(os.path.dirname(SHEET), exist_ok=True)
    if os.path.exists(SHEET):
        sys.exit(f"{SHEET} already exists; not overwritten (it may contain your labels).")
    pd.DataFrame(rows).to_excel(SHEET, index=False)
    print(f"\nLabel sheet -> {SHEET}\nLabel all_values_correct (yes/no) and unsupported_claim (yes/no) with the SAME "
          "rules as label_patient.xlsx.\nA class the model assigned is wrong if it differs from the class in "
          "true_record. Leave empty answers blank and note 'empty'.")


def wilson(k, n, z=1.96):
    if n == 0:
        return (math.nan, math.nan)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(c - h, 3), round(c + h, 3))


def score():
    import pandas as pd
    df = pd.read_excel(SHEET).fillna("")
    norm = lambda s: str(s).strip().lower()
    lab = df[df["all_values_correct"].map(norm).isin(["yes", "no"])]
    missing = df[~df["all_values_correct"].map(norm).isin(["yes", "no"])]
    ok = ((lab["all_values_correct"].map(norm) == "yes") & (lab["unsupported_claim"].map(norm) != "yes")).sum()
    n = len(lab)
    errs = lab[~((lab["all_values_correct"].map(norm) == "yes") & (lab["unsupported_claim"].map(norm) != "yes"))]
    res = {"model": bench.CLAUDE_MODEL, "labelled": n, "unlabelled_or_empty": len(missing),
           "correct": int(ok), "errors": int(n - ok), "ci95": wilson(ok, n),
           "error_queries": errs[["query_id", "notes"]].to_dict("records")}
    os.makedirs(os.path.dirname(SCORES), exist_ok=True)
    json.dump(res, open(SCORES, "w"), indent=1)
    print(f"Label-stripped ({bench.CLAUDE_MODEL}): correct {ok}/{n}  95% CI {res['ci95']}  "
          f"(unlabelled/empty: {len(missing)})")
    for e in res["error_queries"]:
        print(f"   error: {e['query_id']}  {e['notes']}")
    print(f"Saved -> {SCORES}\nCompare with run 2 (labels in the reports): Haiku full system 47/49, Sonnet 48/49.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("step", choices=["run", "score"])
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    run(a.dry_run) if a.step == "run" else score()
