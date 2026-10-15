"""
check_forecasts.py

Checks that every forecast number Claude quoted in a full-system answer is the
number the trajectory model actually produced (saved by the v2 benchmark).
No API calls; runs instantly.

Run from the MediRAG root:   python check_forecasts.py
"""
import json
import re

RESULTS = "evaluation/v2/benchmark_v2_results_run1.json"
CONFIGS = ["full_system", "full_system_corrective"]
FORECAST_WORDS = ("predict", "forecast", "estimate", "projection")
FIELDS = {"predicted_HbA1c": "HbA1c", "predicted_FBS": "FBS", "predicted_PPBS": "PPBS"}

with open(RESULTS) as f:
    results = json.load(f)

checked = matched = 0
problems = []
for qid, rec in results.items():
    for c in CONFIGS:
        e = rec["configs"].get(c)
        if not e or not e.get("trajectory"):
            continue
        answer = e["answer"]
        if not any(w in answer.lower() for w in FORECAST_WORDS):
            continue  # answer did not mention a forecast at all
        numbers = {float(n) for n in re.findall(r"\d+(?:\.\d+)?", answer)}
        for key, name in FIELDS.items():
            value = e["trajectory"].get(key)
            if value is None:
                continue
            # only check values the answer appears to talk about
            if name.lower() not in answer.lower() and name != "HbA1c":
                continue
            checked += 1
            if any(abs(value - n) < 0.051 for n in numbers):
                matched += 1
            else:
                problems.append(f"{qid} {c}: model {name} = {value}, not found in answer")

print(f"Forecast values checked: {checked}")
print(f"Quoted correctly:        {matched}")
if problems:
    print("\nCheck these by reading the answer (the answer may simply not quote that value):")
    for p in problems:
        print("  ", p)
else:
    print("\nAll forecast values quoted in full-system answers matched the model output.")