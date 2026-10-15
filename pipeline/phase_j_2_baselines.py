"""
Baseline check for the MediRAG trajectory model (Table II).

Compares two simple baselines against your GRU using the SAME setup:
100 one-step-ahead pairs (Month1->Month2, Months1-2->Month3), 5-fold CV,
folds split BY PATIENT so no patient appears in both train and test.

  1. Persistence : "next value = last recorded value" (no learning at all)
  2. Ridge       : linear regression on the last visit + last change

Usage:  python phase_j_2_baselines.py path/to/Synthetic_diabetes_dataset1.xlsx
Results are also saved to results/trajectory/baselines.json
"""
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold
from sklearn.linear_model import Ridge
from sklearn.metrics import accuracy_score, f1_score
from results_logger import save_result

path = sys.argv[1] if len(sys.argv) > 1 else "Synthetic_diabetes_dataset1.xlsx"
df = pd.read_excel(path, sheet_name="Laboratory_Reports")
df.columns = [c.strip() for c in df.columns]
df = df[df["Patient_ID"].astype(str).str.match(r"^P\d+$")].copy()
df["t"] = df["Month"].str[-1].astype(int)

FEATS = ["HbA1c(%)", "FBS (mg/dL)", "PPBS (mg/dL)"]
ALL = FEATS + ["LDL", "HDL", "Triglycerides"]
for c in ALL:
    df[c] = pd.to_numeric(df[c], errors="coerce")

# Build the 100 supervised pairs
X, Y, last, s_prev, s_true, groups = [], [], [], [], [], []
for pid, g in df.sort_values("t").groupby("Patient_ID"):
    g = g.set_index("t")
    for tgt in (2, 3):
        prev = g.loc[tgt - 1, ALL].values.astype(float)
        delta = prev - g.loc[tgt - 2, ALL].values.astype(float) if tgt == 3 else np.zeros(len(ALL))
        X.append(np.concatenate([prev, delta]))
        Y.append(g.loc[tgt, FEATS].values.astype(float))
        last.append(g.loc[tgt - 1, FEATS].values.astype(float))
        s_prev.append(g.loc[tgt - 1, "Overall_Status"])
        s_true.append(g.loc[tgt, "Overall_Status"])
        groups.append(pid)
X, Y, last = map(np.array, (X, Y, last))
s_prev, s_true, groups = np.array(s_prev), np.array(s_true), np.array(groups)
print(f"Pairs: {len(Y)}  Patients: {len(set(groups))}")

res = {"persist": [], "ridge": [], "acc": [], "f1": []}
for tr, te in GroupKFold(n_splits=5).split(X, Y, groups):
    res["persist"].append(np.abs(Y[te] - last[te]).mean(axis=0))
    pred = Ridge(alpha=1.0).fit(X[tr], Y[tr]).predict(X[te])
    res["ridge"].append(np.abs(Y[te] - pred).mean(axis=0))
    res["acc"].append(accuracy_score(s_true[te], s_prev[te]))
    res["f1"].append(f1_score(s_true[te], s_prev[te], average="macro"))

print("\nMAE per biomarker, mean ± std over 5 patient-grouped folds")
print(f"{'Biomarker':<14}{'Persistence':>18}{'Ridge':>18}")
for i, f in enumerate(FEATS):
    p = np.array(res["persist"])[:, i]; r = np.array(res["ridge"])[:, i]
    print(f"{f:<14}{p.mean():>10.2f} ± {p.std():<5.2f}{r.mean():>10.2f} ± {r.std():<5.2f}")
print(f"\nRisk category (persistence): accuracy {np.mean(res['acc']):.3f} ± {np.std(res['acc']):.3f}, "
      f"macro-F1 {np.mean(res['f1']):.3f} ± {np.std(res['f1']):.3f}")
print("\nYour GRU (Table II): HbA1c 0.83, FBS 24.30, PPBS 29.34, accuracy 0.780, macro-F1 0.685")

summary = {}
for i, f in enumerate(FEATS):
    p = np.array(res["persist"])[:, i]; r = np.array(res["ridge"])[:, i]
    summary[f] = {"persistence_mae_mean": p.mean(), "persistence_mae_std": p.std(),
                  "ridge_mae_mean": r.mean(), "ridge_mae_std": r.std()}
summary["risk_category_persistence"] = {
    "accuracy_mean": np.mean(res["acc"]), "accuracy_std": np.std(res["acc"]),
    "macro_f1_mean": np.mean(res["f1"]), "macro_f1_std": np.std(res["f1"])}
summary["setup"] = {"pairs": int(len(Y)), "patients": int(len(set(groups))),
                    "folds": 5, "split": "GroupKFold by Patient_ID"}
save_result("trajectory", "baselines", summary,
            notes="Baselines for Table II, same 100 pairs and patient-grouped 5-fold CV")