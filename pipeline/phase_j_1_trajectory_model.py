"""
phase_j_trajectory_model.py   (revised)

Phase J for Medi-RAG: Longitudinal Trajectory Forecasting Model

Trains a small GRU to predict a patient's NEXT visit (HbA1c, FBS, PPBS and
risk category) from their history, using one-step-ahead pairs:
    [Month 1]          -> Month 2
    [Month 1, Month 2] -> Month 3
giving 100 pairs (50 patients x 2).

CHANGES FROM THE PREVIOUS VERSION (see comments marked FIX):
  FIX 1  Padding bug: histories are now POST-padded. pack_padded_sequence
         reads the FIRST `length` timesteps, so the old pre-padding made the
         GRU see only the zero-padding row for every 1-month history
         (half of all samples).
  FIX 2  Folds are split by patient (GroupKFold). With plain KFold, one
         patient's two pairs could sit in train and validation at once.
  FIX 3  The scaler is fitted on the training fold only, not on all data.
  FIX 4  Per-biomarker MAE (mean and std over folds) is now saved, so every
         Table II value comes from this file. The combined MAE was removed:
         averaging % and mg/dL is not meaningful.
  FIX 5  A persistence baseline ("next = last value") is computed on the
         SAME folds and saved next to the GRU results for direct comparison.
  FIX 6  Optional PREDICT_CHANGE flag: the GRU predicts the change from the
         last visit instead of the raw value. Try both and report honestly.
  FIX 7  results_logger import moved to the top; indentation error fixed.

Run from the MediRAG root folder (same level as data/).
Requirements: pip install pandas openpyxl torch scikit-learn
"""

import os
import json
import pickle

import numpy as np
import pandas as pd

from results_logger import save_result  # FIX 7

# -----------------------------
# Config
# -----------------------------
DATA_PATH = os.path.join("data", "Synthetic_diabetes_dataset1.xlsx")
SHEET_NAME = "Laboratory_Reports"

MODEL_OUTPUT_DIR = os.path.join("models", "trajectory")
SEQUENCE_DATA_PATH = os.path.join("verifier_data", "trajectory_sequences.json")

FEATURE_COLUMNS = ["HbA1c(%)", "FBS (mg/dL)", "PPBS (mg/dL)"]
STATUS_COLUMN = "Overall_Status"
STATUS_CLASSES = ["Normal", "Prediabetic", "Diabetic"]

MAX_SEQ_LEN = 2
HIDDEN_SIZE = 16
NUM_EPOCHS = 60
LEARNING_RATE = 0.005
K_FOLDS = 5
RANDOM_SEED = 42
PREDICT_CHANGE = True # FIX 6: set True to predict (next - last) instead of next

os.makedirs(MODEL_OUTPUT_DIR, exist_ok=True)
os.makedirs("verifier_data", exist_ok=True)


# -----------------------------
# Step 1: Per-patient sequences and one-step-ahead pairs
# -----------------------------
def load_patient_sequences():
    df = pd.read_excel(DATA_PATH, sheet_name=SHEET_NAME)
    df = df.dropna(subset=["Patient_ID"])

    df["month_num"] = df["Month"].astype(str).str.strip().str.extract(r"Month[_\s]*(\d+)")[0]
    unparseable = df[df["month_num"].isna()]
    if len(unparseable) > 0:
        print(f"Warning: dropping {len(unparseable)} row(s) with an unrecognized Month format:")
        print(unparseable[["Patient_ID", "Month"]].to_string())
    df = df.dropna(subset=["month_num"])
    df["month_num"] = df["month_num"].astype(int)
    df = df.sort_values(["Patient_ID", "month_num"])

    sequences = {}
    for patient_id, group in df.groupby("Patient_ID"):
        sequences[patient_id] = [{
            "HbA1c(%)": float(row["HbA1c(%)"]),
            "FBS (mg/dL)": float(row["FBS (mg/dL)"]),
            "PPBS (mg/dL)": float(row["PPBS (mg/dL)"]),
            "status": str(row[STATUS_COLUMN]),
        } for _, row in group.iterrows()]
    return sequences


def build_one_step_ahead_pairs(sequences):
    pairs = []
    for patient_id, months in sequences.items():
        for t in range(1, len(months)):
            pairs.append({
                "patient_id": patient_id,
                "history": months[:t],
                "target_features": [months[t][col] for col in FEATURE_COLUMNS],
                "target_status": months[t]["status"],
            })
    return pairs


# -----------------------------
# Step 2: Raw (unscaled) arrays. Scaling now happens inside each fold.
# -----------------------------
def build_raw_arrays(pairs):
    """
    Returns unscaled arrays:
        X_raw   (n, MAX_SEQ_LEN, f)  history, POST-padded (real months first)
        lengths (n,)                 true history length
        y_raw   (n, f)               next-visit values
        y_cls   (n,)                 next-visit status index
        groups  (n,)                 patient ID, for GroupKFold
    """
    n, f = len(pairs), len(FEATURE_COLUMNS)
    X_raw = np.zeros((n, MAX_SEQ_LEN, f), dtype=np.float32)
    lengths = np.zeros(n, dtype=np.int64)
    y_raw = np.zeros((n, f), dtype=np.float32)
    y_cls = np.zeros(n, dtype=np.int64)
    groups = np.array([p["patient_id"] for p in pairs])

    for i, pair in enumerate(pairs):
        hist = [[m[col] for col in FEATURE_COLUMNS] for m in pair["history"]]
        lengths[i] = len(hist)
        X_raw[i, :len(hist), :] = hist          # FIX 1: post-padding
        y_raw[i] = pair["target_features"]
        y_cls[i] = STATUS_CLASSES.index(pair["target_status"])
    return X_raw, lengths, y_raw, y_cls, groups


def last_visit(X_raw, lengths):
    """Most recent real visit for each sample (works with post-padding)."""
    return X_raw[np.arange(len(X_raw)), lengths - 1, :]


def fit_scaler(X_raw, lengths):
    """Fit a StandardScaler on the real (non-padded) history values only."""
    from sklearn.preprocessing import StandardScaler
    rows = np.concatenate([X_raw[i, :lengths[i], :] for i in range(len(X_raw))])
    return StandardScaler().fit(rows)


def scale_inputs(X_raw, lengths, scaler):
    """Scale real timesteps; padding stays exactly zero."""
    X = np.zeros_like(X_raw)
    for i in range(len(X_raw)):
        X[i, :lengths[i], :] = scaler.transform(X_raw[i, :lengths[i], :])
    return X


def make_targets(y_raw, X_raw, lengths, scaler):
    """Regression target in scaled space: next value, or change from last (FIX 6)."""
    y_scaled = scaler.transform(y_raw)
    if PREDICT_CHANGE:
        return (y_scaled - scaler.transform(last_visit(X_raw, lengths))).astype(np.float32)
    return y_scaled.astype(np.float32)


def to_real_units(reg_out, X_raw, lengths, scaler):
    """Convert model output back to real clinical units."""
    if PREDICT_CHANGE:
        reg_out = reg_out + scaler.transform(last_visit(X_raw, lengths))
    return scaler.inverse_transform(reg_out)


# -----------------------------
# Step 3: The GRU model
# -----------------------------
def build_model():
    import torch.nn as nn

    class TrajectoryGRU(nn.Module):
        def __init__(self, input_size, hidden_size, num_classes):
            super().__init__()
            self.gru = nn.GRU(input_size, hidden_size, batch_first=True)
            self.regression_head = nn.Linear(hidden_size, input_size)
            self.classification_head = nn.Linear(hidden_size, num_classes)

        def forward(self, x, lengths):
            packed = nn.utils.rnn.pack_padded_sequence(
                x, lengths.cpu(), batch_first=True, enforce_sorted=False
            )
            _, hidden = self.gru(packed)
            hidden = hidden.squeeze(0)
            return self.regression_head(hidden), self.classification_head(hidden)

    return TrajectoryGRU(len(FEATURE_COLUMNS), HIDDEN_SIZE, len(STATUS_CLASSES))


def train_model(X, lengths, y_reg, y_cls):
    import torch
    import torch.nn as nn

    model = build_model()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    mse, ce = nn.MSELoss(), nn.CrossEntropyLoss()
    X_t, L_t = torch.tensor(X), torch.tensor(lengths)
    yr_t, yc_t = torch.tensor(y_reg), torch.tensor(y_cls)

    model.train()
    for _ in range(NUM_EPOCHS):
        optimizer.zero_grad()
        reg_pred, cls_pred = model(X_t, L_t)
        loss = mse(reg_pred, yr_t) + ce(cls_pred, yc_t)
        loss.backward()
        optimizer.step()
    return model


# -----------------------------
# Step 4: Patient-grouped cross-validation with a persistence baseline
# -----------------------------
def summarise(values):
    return {"mean": float(np.mean(values)), "std": float(np.std(values))}


def train_with_cross_validation(X_raw, lengths, y_raw, y_cls, groups):
    import torch
    from sklearn.model_selection import GroupKFold
    from sklearn.metrics import accuracy_score, f1_score

    torch.manual_seed(RANDOM_SEED)
    gkf = GroupKFold(n_splits=K_FOLDS)  # FIX 2

    gru_mae, base_mae = [], []
    gru_acc, gru_f1, base_acc, base_f1 = [], [], [], []

    for fold, (tr, va) in enumerate(gkf.split(X_raw, y_raw, groups), start=1):
        assert not set(groups[tr]) & set(groups[va]), "patient leaked across folds"

        scaler = fit_scaler(X_raw[tr], lengths[tr])  # FIX 3
        X_tr = scale_inputs(X_raw[tr], lengths[tr], scaler)
        X_va = scale_inputs(X_raw[va], lengths[va], scaler)
        y_tr = make_targets(y_raw[tr], X_raw[tr], lengths[tr], scaler)

        model = train_model(X_tr, lengths[tr], y_tr, y_cls[tr])
        model.eval()
        with torch.no_grad():
            reg_va, cls_va = model(torch.tensor(X_va), torch.tensor(lengths[va]))

        pred_real = to_real_units(reg_va.numpy(), X_raw[va], lengths[va], scaler)
        gru_mae.append(np.mean(np.abs(y_raw[va] - pred_real), axis=0))
        pred_cls = cls_va.argmax(dim=1).numpy()
        gru_acc.append(accuracy_score(y_cls[va], pred_cls))
        gru_f1.append(f1_score(y_cls[va], pred_cls, average="macro", zero_division=0))

        # FIX 5: persistence baseline on the identical validation fold
        last = last_visit(X_raw[va], lengths[va])
        base_mae.append(np.mean(np.abs(y_raw[va] - last), axis=0))
        last_status = np.array([STATUS_CLASSES.index(classify_status(v)) for v in last])
        base_acc.append(accuracy_score(y_cls[va], last_status))
        base_f1.append(f1_score(y_cls[va], last_status, average="macro", zero_division=0))

        m = gru_mae[-1]
        print(f"Fold {fold}/{K_FOLDS} | GRU MAE HbA1c {m[0]:.2f}  FBS {m[1]:.1f}  PPBS {m[2]:.1f} "
              f"| acc {gru_acc[-1]:.3f}  F1 {gru_f1[-1]:.3f}")

    gru_mae, base_mae = np.array(gru_mae), np.array(base_mae)
    results = {"setup": {"num_samples": int(len(X_raw)),
                         "num_patients": int(len(set(groups))),
                         "num_folds": K_FOLDS,
                         "split": "GroupKFold by Patient_ID",
                         "predict_change": PREDICT_CHANGE,
                         "epochs": NUM_EPOCHS, "hidden_size": HIDDEN_SIZE,
                         "learning_rate": LEARNING_RATE}}
    for name, mae, acc, f1 in (("gru", gru_mae, gru_acc, gru_f1),
                               ("persistence_baseline", base_mae, base_acc, base_f1)):
        results[name] = {f"{col}_MAE": summarise(mae[:, j]) for j, col in enumerate(FEATURE_COLUMNS)}
        results[name]["risk_accuracy"] = summarise(acc)
        results[name]["risk_macro_f1"] = summarise(f1)

    print("\nTable II comparison (mean ± std over folds)")
    print(f"{'Metric':<22}{'GRU':>18}{'Persistence':>18}")
    keys = [f"{c}_MAE" for c in FEATURE_COLUMNS] + ["risk_accuracy", "risk_macro_f1"]
    for k in keys:
        g, b = results["gru"][k], results["persistence_baseline"][k]
        print(f"{k:<22}{g['mean']:>10.3f} ± {g['std']:<5.3f}{b['mean']:>10.3f} ± {b['std']:<5.3f}")
    return results


def classify_status(values):
    """ADA thresholds used to label the dataset (HbA1c, FBS, PPBS)."""
    hba1c, fbs, ppbs = values
    if hba1c >= 6.5 or fbs >= 126 or ppbs >= 200:
        return "Diabetic"
    if hba1c >= 5.7 or fbs >= 100 or ppbs >= 140:
        return "Prediabetic"
    return "Normal"


def train_final_model(X_raw, lengths, y_raw, y_cls):
    import torch

    torch.manual_seed(RANDOM_SEED)
    scaler = fit_scaler(X_raw, lengths)
    X = scale_inputs(X_raw, lengths, scaler)
    y = make_targets(y_raw, X_raw, lengths, scaler)
    model = train_model(X, lengths, y, y_cls)

    torch.save(model.state_dict(), os.path.join(MODEL_OUTPUT_DIR, "trajectory_gru.pt"))
    with open(os.path.join(MODEL_OUTPUT_DIR, "scaler.pkl"), "wb") as f:
        pickle.dump(scaler, f)
    with open(os.path.join(MODEL_OUTPUT_DIR, "model_config.json"), "w") as f:
        json.dump({"predict_change": PREDICT_CHANGE, "padding": "post"}, f, indent=2)
    print(f"\nSaved final model -> {MODEL_OUTPUT_DIR}/trajectory_gru.pt")
    return model


# -----------------------------
# Step 5: Inference
# -----------------------------
_trajectory_cache = {}


def predict_next_visit(history_months):
    """Predict the next visit from 1-2 months of history (used by phase_g)."""
    import torch

    if "model" not in _trajectory_cache:
        model = build_model()
        model.load_state_dict(torch.load(os.path.join(MODEL_OUTPUT_DIR, "trajectory_gru.pt")))
        model.eval()
        with open(os.path.join(MODEL_OUTPUT_DIR, "scaler.pkl"), "rb") as f:
            _trajectory_cache["scaler"] = pickle.load(f)
        _trajectory_cache["model"] = model

    model, scaler = _trajectory_cache["model"], _trajectory_cache["scaler"]
    hist = [[m[col] for col in FEATURE_COLUMNS] for m in history_months][-MAX_SEQ_LEN:]
    X_raw = np.zeros((1, MAX_SEQ_LEN, len(FEATURE_COLUMNS)), dtype=np.float32)
    X_raw[0, :len(hist), :] = hist                  # FIX 1: post-padding
    lengths = np.array([len(hist)])
    X = scale_inputs(X_raw, lengths, scaler)

    with torch.no_grad():
        reg, cls = model(torch.tensor(X), torch.tensor(lengths))
    pred = to_real_units(reg.numpy(), X_raw, lengths, scaler)[0]
    return {
        "predicted_HbA1c": round(float(pred[0]), 2),
        "predicted_FBS": round(float(pred[1]), 1),
        "predicted_PPBS": round(float(pred[2]), 1),
        "predicted_status": STATUS_CLASSES[cls.argmax(dim=1).item()],
    }


# -----------------------------
# Main
# -----------------------------
def main():
    print("=== Step 1: Building per-patient sequences ===\n")
    sequences = load_patient_sequences()
    pairs = build_one_step_ahead_pairs(sequences)
    print(f"Loaded {len(sequences)} patients, built {len(pairs)} one-step-ahead pairs.\n")
    with open(SEQUENCE_DATA_PATH, "w") as f:
        json.dump(pairs, f, indent=2)

    X_raw, lengths, y_raw, y_cls, groups = build_raw_arrays(pairs)

    print("=== Step 2: Patient-grouped cross-validation ===\n")
    cv_results = train_with_cross_validation(X_raw, lengths, y_raw, y_cls, groups)

    with open(os.path.join(MODEL_OUTPUT_DIR, "cv_results.json"), "w") as f:
        json.dump(cv_results, f, indent=2)
    save_result("trajectory", "cv_results", cv_results,
                notes="Table II: GRU vs persistence, patient-grouped 5-fold CV")

    print("\n=== Step 3: Training final model on all data ===")
    train_final_model(X_raw, lengths, y_raw, y_cls)

    print("\n=== Step 4: Sanity test on P032 ===\n")
    p032 = sequences.get("P032")
    if p032 and len(p032) >= 3:
        pred = predict_next_visit(p032[:2])
        actual = p032[2]
        print(f"Predicted Month 3: {pred}")
        print(f"Actual Month 3:    HbA1c={actual['HbA1c(%)']}, FBS={actual['FBS (mg/dL)']}, "
              f"PPBS={actual['PPBS (mg/dL)']}, status={actual['status']}")
        print(f"Persistence guess: HbA1c={p032[1]['HbA1c(%)']}")
    print("\nPhase J complete.")


if __name__ == "__main__":
    main()