"""
phase_j_3_trajectory_v2.py  --  fairer GRU evaluation (cohort 2; no API calls)

phase_j_1 (used for the paper's Table II) trains the GRU full-batch for a fixed
60 epochs -- only 60 gradient steps, which can leave the model close to
"predict no change" (= persistence). This script keeps the same GRU, data and
patient-grouped 5-fold CV, and fixes the evaluation:

  1. Early stopping on an INNER validation split (15% of the training fold's
     patients), up to MAX_EPOCHS. The test fold is never used for tuning.
  2. Two extra baselines on the same folds:
       linear trend   last value + mean change over the last 3 visits
       ridge          linear regression on the last 3 visits (predicts change)
  3. Persistence for the risk category uses the RECORDED status of the last
     visit (phase_j_1 re-derived it with a slightly different rule).
  4. Per-trajectory-type MAE (uses data/cohort2_summary.json if present), so
     you can see WHERE a learned model helps (trending vs stable patients).

phase_j_1 is left unchanged, so cohort-1 results stay reproducible.

Usage (from the MediRAG_cohort2 root, with MEDIRAG_MAX_SEQ_LEN=7 set):
    python pipeline/phase_j_3_trajectory_v2.py
Output:
    results/trajectory/cv_results_v2.json
    models/trajectory/trajectory_gru.pt (+ scaler.pkl), retrained with the chosen epochs
"""
import json
import os
import pickle
import sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import phase_j_1_trajectory_model as j1
from results_logger import save_result

MAX_EPOCHS = 600
PATIENCE = 60
INNER_VAL_SHARE = 0.15
LAGS = 3
SUMMARY_PATH = os.path.join("data", "cohort2_summary.json")


def train_early_stopping(X_tr, L_tr, y_tr, c_tr, X_iv, L_iv, y_iv, c_iv):
    import torch
    import torch.nn as nn
    model = j1.build_model()
    opt = torch.optim.Adam(model.parameters(), lr=j1.LEARNING_RATE)
    mse, ce = nn.MSELoss(), nn.CrossEntropyLoss()
    T = lambda a: torch.tensor(a)
    Xt, Lt, yt, ct = T(X_tr), T(L_tr), T(y_tr), T(c_tr)
    Xv, Lv, yv, cv = T(X_iv), T(L_iv), T(y_iv), T(c_iv)
    best, best_ep, best_state, wait = float("inf"), 0, None, 0
    for ep in range(1, MAX_EPOCHS + 1):
        model.train(); opt.zero_grad()
        r, c = model(Xt, Lt)
        (mse(r, yt) + ce(c, ct)).backward(); opt.step()
        model.eval()
        with torch.no_grad():
            r, c = model(Xv, Lv)
            v = float(mse(r, yv) + ce(c, cv))
        if v < best - 1e-5:
            best, best_ep, wait = v, ep, 0
            best_state = {k: x.clone() for k, x in model.state_dict().items()}
        else:
            wait += 1
            if wait >= PATIENCE:
                break
    model.load_state_dict(best_state)
    return model, best_ep


def lag_features(X_raw, lengths):
    """Last LAGS visits (earliest padded by repetition), flattened."""
    out = np.zeros((len(X_raw), LAGS * X_raw.shape[2]), dtype=np.float32)
    for i in range(len(X_raw)):
        h = X_raw[i, :lengths[i], :]
        h = np.vstack([np.repeat(h[:1], max(0, LAGS - len(h)), axis=0), h])[-LAGS:]
        out[i] = h.ravel()
    return out


def linear_trend(X_raw, lengths):
    pred = np.zeros((len(X_raw), X_raw.shape[2]), dtype=np.float32)
    for i in range(len(X_raw)):
        h = X_raw[i, :lengths[i], :][-LAGS:]
        pred[i] = h[-1] + (np.mean(np.diff(h, axis=0), axis=0) if len(h) > 1 else 0)
    return pred


def main():
    import torch
    from sklearn.linear_model import Ridge
    from sklearn.metrics import accuracy_score, f1_score
    from sklearn.model_selection import GroupKFold, GroupShuffleSplit

    torch.manual_seed(j1.RANDOM_SEED)
    seqs = j1.load_patient_sequences()
    pairs = j1.build_one_step_ahead_pairs(seqs)
    X_raw, L, y_raw, y_cls, groups = j1.build_raw_arrays(pairs)
    last_status = np.array([j1.STATUS_CLASSES.index(p["history"][-1]["status"]) for p in pairs])
    types = None
    if os.path.exists(SUMMARY_PATH):
        with open(SUMMARY_PATH) as f:
            tmap = json.load(f)["trajectory_by_patient"]
        types = np.array([tmap.get(g, "unknown") for g in groups])
    print(f"{len(seqs)} patients, {len(pairs)} pairs, max history {j1.MAX_SEQ_LEN}")

    names = ["gru", "persistence", "linear_trend", "ridge"]
    mae = {n: [] for n in names}
    err_by_type = {n: defaultdict(list) for n in names}
    acc, f1, epochs = {"gru": [], "persistence": []}, {"gru": [], "persistence": []}, []

    for fold, (tr, te) in enumerate(GroupKFold(n_splits=j1.K_FOLDS).split(X_raw, y_raw, groups), 1):
        inner = GroupShuffleSplit(n_splits=1, test_size=INNER_VAL_SHARE, random_state=fold)
        fit_i, val_i = next(inner.split(tr, groups=groups[tr]))
        fit, iv = tr[fit_i], tr[val_i]
        sc = j1.fit_scaler(X_raw[fit], L[fit])
        prep = lambda idx: (j1.scale_inputs(X_raw[idx], L[idx], sc), L[idx],
                            j1.make_targets(y_raw[idx], X_raw[idx], L[idx], sc), y_cls[idx])
        model, ep = train_early_stopping(*prep(fit), *prep(iv))
        epochs.append(ep)
        model.eval()
        with torch.no_grad():
            r, c = model(torch.tensor(j1.scale_inputs(X_raw[te], L[te], sc)), torch.tensor(L[te]))
        preds = {"gru": j1.to_real_units(r.numpy(), X_raw[te], L[te], sc),
                 "persistence": j1.last_visit(X_raw[te], L[te]),
                 "linear_trend": linear_trend(X_raw[te], L[te])}
        ridge = Ridge(alpha=1.0).fit(lag_features(X_raw[tr], L[tr]),
                                     y_raw[tr] - j1.last_visit(X_raw[tr], L[tr]))
        preds["ridge"] = j1.last_visit(X_raw[te], L[te]) + ridge.predict(lag_features(X_raw[te], L[te]))
        for n, p in preds.items():
            e = np.abs(y_raw[te] - p)
            mae[n].append(e.mean(axis=0))
            if types is not None:
                for t, row in zip(types[te], e):
                    err_by_type[n][t].append(row[0])          # HbA1c error
        pc = c.argmax(dim=1).numpy()
        acc["gru"].append(accuracy_score(y_cls[te], pc)); f1["gru"].append(f1_score(y_cls[te], pc, average="macro"))
        acc["persistence"].append(accuracy_score(y_cls[te], last_status[te]))
        f1["persistence"].append(f1_score(y_cls[te], last_status[te], average="macro"))
        print(f"Fold {fold}: GRU stopped at epoch {ep}; HbA1c MAE GRU {mae['gru'][-1][0]:.3f} "
              f"vs persistence {mae['persistence'][-1][0]:.3f}")

    res = {"setup": {"pairs": len(pairs), "patients": len(seqs), "max_history": j1.MAX_SEQ_LEN,
                     "max_epochs": MAX_EPOCHS, "patience": PATIENCE, "chosen_epochs": epochs}}
    print(f"\n{'Model':<14}" + "".join(f"{c:>22}" for c in j1.FEATURE_COLUMNS))
    for n in names:
        m = np.array(mae[n])
        res[n] = {f"{c}_MAE": {"mean": float(m[:, j].mean()), "std": float(m[:, j].std())}
                  for j, c in enumerate(j1.FEATURE_COLUMNS)}
        print(f"{n:<14}" + "".join(f"{m[:, j].mean():>14.3f} ± {m[:, j].std():<5.3f}"
                                   for j in range(len(j1.FEATURE_COLUMNS))))
    for n in ("gru", "persistence"):
        res[n]["risk_accuracy"] = {"mean": float(np.mean(acc[n])), "std": float(np.std(acc[n]))}
        res[n]["risk_macro_f1"] = {"mean": float(np.mean(f1[n])), "std": float(np.std(f1[n]))}
    print(f"\nRisk category accuracy: GRU {np.mean(acc['gru']):.3f}, "
          f"persistence (recorded last status) {np.mean(acc['persistence']):.3f}")
    if types is not None:
        res["hba1c_mae_by_trajectory"] = {}
        print(f"\nHbA1c MAE by trajectory type\n{'type':<26}" + "".join(f"{n:>14}" for n in names))
        for t in sorted(set(types)):
            row = {n: float(np.mean(err_by_type[n][t])) for n in names}
            res["hba1c_mae_by_trajectory"][t] = row
            print(f"{t:<26}" + "".join(f"{row[n]:>14.3f}" for n in names))

    # final model for deployment: all data, epochs = median chosen epoch
    final_ep = int(np.median(epochs))
    sc = j1.fit_scaler(X_raw, L)
    X = j1.scale_inputs(X_raw, L, sc)
    yr = j1.make_targets(y_raw, X_raw, L, sc)
    saved = j1.NUM_EPOCHS
    j1.NUM_EPOCHS = final_ep
    torch.manual_seed(j1.RANDOM_SEED)
    model = j1.train_model(X, L, yr, y_cls)
    j1.NUM_EPOCHS = saved
    os.makedirs(j1.MODEL_OUTPUT_DIR, exist_ok=True)
    torch.save(model.state_dict(), os.path.join(j1.MODEL_OUTPUT_DIR, "trajectory_gru.pt"))
    with open(os.path.join(j1.MODEL_OUTPUT_DIR, "scaler.pkl"), "wb") as f:
        pickle.dump(sc, f)
    res["setup"]["final_model_epochs"] = final_ep
    print(f"\nSaved final model ({final_ep} epochs) -> {j1.MODEL_OUTPUT_DIR}")
    save_result("trajectory", "cv_results_v2", res,
                notes="GRU with inner-split early stopping vs persistence, linear trend, ridge")


if __name__ == "__main__":
    main()
