"""
check_forecasts_v2.py

Question answered: when a full-system answer STATES a forecast number, is it the
number the trajectory model produced?

For every sentence that talks about a forecast ("predict", "forecast",
"estimate", "projection", "next visit"...), each number in that sentence must be
one of:
  * a value the trajectory model produced for this patient (within 0.05), or
  * one of the patient's recorded values (answers often compare with them), or
  * a reference threshold (e.g. 5.7, 6.5, 100, 126, 140, 200) or a small
    count/month number (<= 12).
Anything else is printed for you to read. Runs instantly, no API calls.

Run from the MediRAG root:   python check_forecasts_v2.py
"""
import json
import re

import pandas as pd

RESULTS = "evaluation/v2/benchmark_v2_results_run1.json"
DATA = "data/Synthetic_diabetes_dataset1.xlsx"
CONFIGS = ["full_system", "full_system_corrective"]
FORECAST_WORDS = ("predict", "forecast", "estimate", "projection", "next visit",
                  "next reading", "next month", "next lab")
THRESHOLDS = {5.7, 6.4, 6.5, 7.0, 8.0, 9.0, 70, 99, 100, 125, 126, 139, 140, 150, 160,
              190, 199, 200, 40, 50, 60, 130}
COLS = ["HbA1c(%)", "FBS (mg/dL)", "PPBS (mg/dL)", "LDL", "HDL", "Triglycerides"]

df = pd.read_excel(DATA, sheet_name="Laboratory_Reports")
df.columns = [c.strip() for c in df.columns]
df = df[df["Patient_ID"].astype(str).str.match(r"^P\d+$")]
recorded = {pid: {float(v) for c in COLS for v in g[c] if pd.notna(v)}
            for pid, g in df.groupby("Patient_ID")}

with open(RESULTS) as f:
    results = json.load(f)

answers = forecast_answers = 0
flags = []
for qid, rec in results.items():
    for c in CONFIGS:
        e = rec["configs"].get(c)
        if not e or not e.get("trajectory"):
            continue
        answers += 1
        traj = [float(v) for k, v in e["trajectory"].items() if k.startswith("predicted_")
                and isinstance(v, (int, float))]
        ok = recorded.get(rec.get("patient_id"), set())
        sentences = re.split(r"(?<=[.!?])\s+|\n+", e["answer"])
        fsent = [s for s in sentences if any(w in s.lower() for w in FORECAST_WORDS)]
        if not fsent:
            continue
        forecast_answers += 1
        for s in fsent:
            for n in re.findall(r"(?<![\w.])\d+(?:\.\d+)?", s):
                v = float(n)
                if (any(abs(v - t) < 0.051 for t in traj) or v in ok or v in THRESHOLDS
                        or v <= 12 and v == int(v)):
                    continue
                flags.append((qid, c, v, s.strip()[:160]))

print(f"Full-system answers with a model forecast available: {answers}")
print(f"Answers that talk about a forecast:                 {forecast_answers}")
if flags:
    print(f"\n{len(flags)} number(s) in forecast sentences that are NOT the model's output,")
    print("a recorded value or a threshold -- read these:")
    for qid, c, v, s in flags:
        print(f"  {qid} {c}: {v}\n      \"{s}\"")
else:
    print("\nEvery number stated in a forecast sentence matched the model's output "
          "(or was a recorded value or reference threshold).")