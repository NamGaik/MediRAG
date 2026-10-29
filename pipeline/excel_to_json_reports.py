"""
excel_to_json_reports.py  --  write json_reports/ directly from the Excel file

Phase C reads json_reports/*.json, which normally come from the OCR step
(generate_reports -> convert_and_degrade -> ocr_extract_and_evaluate).
For cohort 2 the experiment is about generation and answer checking, not OCR
(OCR is evaluated separately on cohort 1), so this script writes the same JSON
records straight from the Laboratory_Reports sheet, with exact values.

To test OCR on cohort 2 as well, run the normal OCR scripts instead.

Usage (from the MediRAG root of the cohort-2 working folder):
    python pipeline/excel_to_json_reports.py [path/to/dataset.xlsx]
Default input: data/Synthetic_diabetes_dataset1.xlsx (in the cohort-2 folder this
file holds the cohort-2 data -- see the cohort-2 instructions).
"""
import json
import os
import sys

import pandas as pd

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join("data", "Synthetic_diabetes_dataset1.xlsx")
OUT = "json_reports"
COLS = {"HbA1c(%)": "HbA1c", "FBS (mg/dL)": "FBS", "PPBS (mg/dL)": "PPBS",
        "LDL": "LDL", "HDL": "HDL", "Triglycerides": "Triglycerides"}


def main():
    df = pd.read_excel(SRC, sheet_name="Laboratory_Reports").dropna(subset=["Patient_ID", "Month"])
    df = df[df["Patient_ID"].astype(str).str.match(r"^P\d+$")]
    os.makedirs(OUT, exist_ok=True)
    old = [f for f in os.listdir(OUT) if f.endswith(".json")]
    for f in old:
        os.remove(os.path.join(OUT, f))
    for _, r in df.iterrows():
        rec = {"Patient_ID": r["Patient_ID"], "Month": r["Month"]}
        rec.update({k: str(r[c]) for c, k in COLS.items()})
        with open(os.path.join(OUT, f"{r['Patient_ID']}_{r['Month']}_Clean.json"), "w") as f:
            json.dump(rec, f)
    print(f"Removed {len(old)} old files; wrote {len(df)} records to {OUT}/ from {SRC}")


if __name__ == "__main__":
    main()
