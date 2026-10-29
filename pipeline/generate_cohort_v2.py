"""
generate_cohort_v2.py  --  synthetic cohort 2 (no API calls)

Writes a new synthetic dataset in EXACTLY the same format as
data/Synthetic_diabetes_dataset1.xlsx (sheets Dataset_Overview, Patient_Master,
Laboratory_Reports, same column names), so the whole pipeline can run on it
unchanged.

Cohort 2: 100 patients x 8 monthly visits, built from seven trajectory types:

  normal_stable           HbA1c 4.8-5.5%, small noise
  prediabetic_stable      HbA1c 5.8-6.3%, small noise
  prediabetic_progressing starts prediabetic, drifts upward; some cross 6.5%
  diabetic_improving      newly treated: HbA1c falls, then levels off
  diabetic_worsening      uncontrolled: HbA1c drifts upward
  diabetic_fluctuating    inconsistent adherence: slow up/down HbA1c cycle, noisier glucose
  diabetic_dyslipidemia   diabetic with persistently high lipids

Values are linked the way real labs are linked: mean glucose follows HbA1c via
the ADAG relation (eAG mg/dL = 28.7 x HbA1c - 46.7); fasting glucose is a bit
below and post-prandial glucose above the mean, each with visit-level noise.
Lipids have a patient baseline, slow drift and noise; HDL depends on sex.
Classifications use the same ADA/WHO rules as phase_c_preprocessing.py.

Usage (from the MediRAG root):
    python pipeline/generate_cohort_v2.py                 # 100 x 8, seed 2027
    python pipeline/generate_cohort_v2.py --patients 70 --visits 6
Output:
    data/Synthetic_diabetes_dataset2.xlsx
    data/cohort2_summary.json   (trajectory type per patient + checks)
"""
import argparse
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from phase_c_preprocessing import (classify_hba1c, classify_fbs, classify_ppbs, classify_ldl,
                                   classify_hdl, classify_triglycerides, overall_status)

OUT_XLSX = os.path.join("data", "Synthetic_diabetes_dataset2.xlsx")
OUT_JSON = os.path.join("data", "cohort2_summary.json")

# share of the cohort per trajectory type (sums to 1)
MIX = {"normal_stable": 0.18, "prediabetic_stable": 0.14, "prediabetic_progressing": 0.16,
       "diabetic_improving": 0.16, "diabetic_worsening": 0.14, "diabetic_fluctuating": 0.12,
       "diabetic_dyslipidemia": 0.10}
DESCRIPTIONS = {
    "normal_stable": "Non-diabetic individuals with stable values in normal clinical ranges",
    "prediabetic_stable": "Prediabetic glycemic values that remain stable over time",
    "prediabetic_progressing": "Prediabetic patients drifting upward; some cross the diabetic threshold",
    "diabetic_improving": "Newly treated diabetic patients whose glycemic control improves, then levels off",
    "diabetic_worsening": "Uncontrolled diabetic patients with gradually worsening glucose levels",
    "diabetic_fluctuating": "Diabetic patients whose control cycles up and down (inconsistent adherence)",
    "diabetic_dyslipidemia": "Diabetic patients with persistently high LDL/triglycerides and low HDL",
}


def hba1c_path(kind, n, rng):
    t = np.arange(n)
    if kind == "normal_stable":
        base = rng.uniform(4.8, 5.4); return base + rng.normal(0, 0.12, n)
    if kind == "prediabetic_stable":
        base = rng.uniform(5.8, 6.2); return base + rng.normal(0, 0.10, n)
    if kind == "prediabetic_progressing":
        base, slope = rng.uniform(5.75, 6.1), rng.uniform(0.06, 0.16)
        return base + slope * t + rng.normal(0, 0.08, n)
    if kind == "diabetic_improving":
        start, floor = rng.uniform(7.8, 10.2), rng.uniform(6.3, 7.1)
        rate = rng.uniform(0.25, 0.45)
        return floor + (start - floor) * np.exp(-rate * t) + rng.normal(0, 0.12, n)
    if kind == "diabetic_worsening":
        base, slope = rng.uniform(7.0, 8.5), rng.uniform(0.10, 0.28)
        return base + slope * t + rng.normal(0, 0.12, n)
    if kind == "diabetic_fluctuating":
        # HbA1c reflects ~3 months of glucose, so it cannot swing every month:
        # a slow cycle (period 4-6 months) from on/off adherence; daily glucose
        # (FBS/PPBS) gets extra visit-level variability below.
        base, amp = rng.uniform(7.2, 8.8), rng.uniform(0.4, 0.8)
        period, phase = rng.uniform(4, 6), rng.uniform(0, 2 * np.pi)
        return base + amp * np.sin(2 * np.pi * t / period + phase) + rng.normal(0, 0.1, n)
    if kind == "diabetic_dyslipidemia":
        base, slope = rng.uniform(7.6, 9.6), rng.uniform(-0.05, 0.10)
        return base + slope * t + rng.normal(0, 0.15, n)
    raise ValueError(kind)


def lipid_path(kind, n, gender, rng):
    t = np.arange(n)
    if kind == "diabetic_dyslipidemia":
        ldl0, tg0, hdl0 = rng.uniform(150, 195), rng.uniform(220, 330), rng.uniform(28, 38)
    elif kind.startswith("diabetic"):
        ldl0, tg0, hdl0 = rng.uniform(95, 150), rng.uniform(150, 240), rng.uniform(34, 48)
    elif kind.startswith("prediabetic"):
        ldl0, tg0, hdl0 = rng.uniform(95, 130), rng.uniform(140, 200), rng.uniform(38, 52)
    else:
        ldl0, tg0, hdl0 = rng.uniform(65, 100), rng.uniform(85, 150), rng.uniform(48, 66)
    if gender == "Female":
        hdl0 += 6
    ldl = ldl0 + rng.uniform(-2, 2) * t + rng.normal(0, 4, n)
    tg = tg0 + rng.uniform(-4, 4) * t + rng.normal(0, 8, n)
    hdl = hdl0 + rng.uniform(-0.4, 0.4) * t + rng.normal(0, 1.5, n)
    return ldl, hdl, tg


def build(patients, visits, seed):
    rng = np.random.default_rng(seed)
    kinds = []
    for k, share in MIX.items():
        kinds += [k] * int(round(share * patients))
    kinds = (kinds + ["normal_stable"] * patients)[:patients]
    rng.shuffle(kinds)

    master, labs, summary = [], [], {}
    for i, kind in enumerate(kinds, start=1):
        pid = f"P{i:03d}"
        gender = rng.choice(["Male", "Female"])
        age = int(rng.integers(25, 45) if kind == "normal_stable" else rng.integers(35, 72))
        master.append({"Patient_ID": pid, "Patient_Name": f"Patient_{i:03d}",
                       "Category": kind, "Age": age, "Gender": gender})
        a1c = np.clip(hba1c_path(kind, visits, rng), 4.3, 13.5)
        eag = 28.7 * a1c - 46.7
        extra = 2.0 if kind == "diabetic_fluctuating" else 1.0
        fbs = np.clip(eag * rng.uniform(0.82, 0.95) + rng.normal(0, 7 * extra, visits), 65, 400)
        ppbs = np.clip(eag * rng.uniform(1.15, 1.32) + rng.normal(0, 12 * extra, visits), 80, 450)
        ldl, hdl, tg = lipid_path(kind, visits, gender, rng)
        ldl, hdl, tg = np.clip(ldl, 50, 260), np.clip(hdl, 22, 90), np.clip(tg, 60, 500)
        for v in range(visits):
            rec = {"Patient_ID": pid, "Month": f"Month_{v + 1}",
                   "HbA1c(%)": round(float(a1c[v]), 1), "FBS (mg/dL)": int(round(fbs[v])),
                   "PPBS (mg/dL)": int(round(ppbs[v])), "LDL": int(round(ldl[v])),
                   "HDL": float(round(hdl[v])), "Triglycerides": float(round(tg[v]))}
            st = overall_status(classify_hba1c(rec["HbA1c(%)"]), classify_fbs(rec["FBS (mg/dL)"]))
            abnormal = (st != "Normal"
                        or classify_ppbs(rec["PPBS (mg/dL)"]) != "Normal"
                        or classify_ldl(rec["LDL"]) != "Optimal"
                        or classify_hdl(rec["HDL"], gender) != "Normal"
                        or classify_triglycerides(rec["Triglycerides"]) != "Normal")
            rec["Overall_Status"] = st
            rec["Flag "] = "Abnormal" if abnormal else "Normal"   # trailing space, as in dataset 1
            labs.append(rec)
        summary[pid] = kind
    return pd.DataFrame(master), pd.DataFrame(labs), summary


def checks(labs, summary, visits):
    """Sanity checks printed and saved with the data."""
    out = {}
    out["status_counts"] = labs["Overall_Status"].value_counts().to_dict()
    trans = 0
    for pid, g in labs.groupby("Patient_ID"):
        s = g["Overall_Status"].tolist()
        trans += sum(a != b for a, b in zip(s, s[1:]))
    out["status_transitions"] = int(trans)
    # learnability: next-visit HbA1c MAE of persistence vs a 2-point linear trend
    pers, lin = [], []
    for pid, g in labs.groupby("Patient_ID"):
        y = g["HbA1c(%)"].to_numpy()
        for t in range(2, visits):
            pers.append(abs(y[t] - y[t - 1]))
            lin.append(abs(y[t] - (y[t - 1] + (y[t - 1] - y[t - 2]))))
    out["hba1c_mae_persistence"] = round(float(np.mean(pers)), 3)
    out["hba1c_mae_linear_trend"] = round(float(np.mean(lin)), 3)
    out["trajectory_types"] = pd.Series(summary).value_counts().to_dict()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--patients", type=int, default=100)
    ap.add_argument("--visits", type=int, default=8)
    ap.add_argument("--seed", type=int, default=2027)
    a = ap.parse_args()
    master, labs, summary = build(a.patients, a.visits, a.seed)
    overview = pd.DataFrame([{"Category": k, "Patients": int((master["Category"] == k).sum()),
                              "Descriptions": DESCRIPTIONS[k]} for k in MIX])
    overview.loc[len(overview)] = {"Category": None, "Patients": f"Total Patients = {a.patients}",
                                   "Descriptions": None}
    os.makedirs("data", exist_ok=True)
    with pd.ExcelWriter(OUT_XLSX) as w:
        overview.to_excel(w, sheet_name="Dataset_Overview", index=False)
        master.to_excel(w, sheet_name="Patient_Master", index=False)
        labs.to_excel(w, sheet_name="Laboratory_Reports", index=False)
    info = {"patients": a.patients, "visits": a.visits, "seed": a.seed, "checks": checks(labs, summary, a.visits),
            "trajectory_by_patient": summary}
    with open(OUT_JSON, "w") as f:
        json.dump(info, f, indent=1)
    c = info["checks"]
    print(f"Wrote {OUT_XLSX}: {a.patients} patients x {a.visits} visits = {len(labs)} reports")
    print(f"Trajectory types: {c['trajectory_types']}")
    print(f"Overall status counts: {c['status_counts']}; status changes between visits: {c['status_transitions']}")
    print(f"Next-visit HbA1c MAE: persistence {c['hba1c_mae_persistence']}, "
          f"2-point linear trend {c['hba1c_mae_linear_trend']}")


if __name__ == "__main__":
    main()
