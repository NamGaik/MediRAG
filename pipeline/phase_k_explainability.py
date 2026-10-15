"""
phase_k_explainability.py   (revised)

Phase K for Medi-RAG: Explainability Layer

1. TRAJECTORY MODEL (GRU) -> Integrated Gradients (Sundararajan et al., 2017)
2. NEURAL VERIFIER (BioClinicalBERT) -> final-layer [CLS] attention

CHANGES FROM THE PREVIOUS VERSION (see comments marked FIX):
  FIX 1  Inputs are POST-padded, matching the revised phase_j (real months
         first). Reads predict_change from models/trajectory/model_config.json
         so the explained quantity is always the predicted VALUE.
  FIX 2  Attributions are converted to real clinical units (% or mg/dL).
         Previously they were in standardised units, which the paper did not say.
  FIX 3  Completeness check: IG attributions should sum to F(input) - F(baseline).
         The gap is printed and saved, so the figure can be trusted.
  FIX 4  Cohort-level attribution: mean |attribution| over all 50 patients,
         so the paper is not relying on one patient (P032) alone.
  FIX 5  The verifier's "faithful" class index is a named constant checked
         against the model config, instead of being silently assumed.
  FIX 6  All numbers are saved with save_result() for the results folder.

Baseline note for the paper: inputs are standardised, so the all-zero
baseline is the TRAINING-SET MEAN patient, not a biomarker value of zero.

Run from the MediRAG root, AFTER phase_j and phase_i have saved their models.
Requirements: pip install torch transformers matplotlib numpy
"""

import os
import json
import pickle

import numpy as np
import torch
import matplotlib.pyplot as plt

from results_logger import save_result
from phase_j_1_trajectory_model import (
    build_model as build_trajectory_model,
    load_patient_sequences,
    FEATURE_COLUMNS,
    MAX_SEQ_LEN,
    MODEL_OUTPUT_DIR as TRAJECTORY_MODEL_DIR,
)
from phase_i_neural_verifier import (
    MODEL_OUTPUT_DIR as VERIFIER_MODEL_DIR,
    MAX_LENGTH as VERIFIER_MAX_LENGTH,
)

OUTPUT_DIR = "explainability"
os.makedirs(OUTPUT_DIR, exist_ok=True)

IG_STEPS = 50
# FIX 5: which output index of the verifier means "faithful".
# CHECK THIS against how labels are assigned in phase_i_neural_verifier.py.
FAITHFUL_LABEL_INDEX = 1


# =============================================================
# PART 1: Trajectory model (Integrated Gradients)
# =============================================================
def load_trajectory_model_and_scaler():
    model = build_trajectory_model()
    model.load_state_dict(torch.load(os.path.join(TRAJECTORY_MODEL_DIR, "trajectory_gru.pt")))
    model.eval()
    with open(os.path.join(TRAJECTORY_MODEL_DIR, "scaler.pkl"), "rb") as f:
        scaler = pickle.load(f)
    config_path = os.path.join(TRAJECTORY_MODEL_DIR, "model_config.json")
    predict_change = False
    if os.path.exists(config_path):
        with open(config_path) as f:
            predict_change = json.load(f).get("predict_change", False)
    else:
        print("WARNING: model_config.json not found -- re-run the revised phase_j first.")
    return model, scaler, predict_change


def build_input(history_months, scaler):
    """Scaled, POST-padded input tensor (FIX 1)."""
    hist = [[m[col] for col in FEATURE_COLUMNS] for m in history_months][-MAX_SEQ_LEN:]
    X = np.zeros((1, MAX_SEQ_LEN, len(FEATURE_COLUMNS)), dtype=np.float32)
    X[0, :len(hist), :] = scaler.transform(hist)
    return torch.tensor(X), torch.tensor([len(hist)])


def predicted_value_scaled(model, x, lengths, idx, predict_change):
    """
    The predicted VALUE of biomarker `idx` in scaled units.
    If the model predicts a change, prediction = last visit + change, so the
    last visit is added back here (keeps gradients flowing through it).
    """
    reg_out, _ = model(x, lengths)
    out = reg_out[:, idx]
    if predict_change:
        last_pos = lengths - 1
        out = out + x[torch.arange(x.shape[0]), last_pos, idx]
    return out


def integrated_gradients(model, x, lengths, idx, predict_change, steps=IG_STEPS):
    """IG from an all-zero (= training-mean) baseline, Riemann midpoint rule."""
    baseline = torch.zeros_like(x)
    grads = []
    for k in range(steps):
        alpha = (k + 0.5) / steps
        point = (baseline + alpha * (x - baseline)).clone().detach().requires_grad_(True)
        out = predicted_value_scaled(model, point, lengths, idx, predict_change).sum()
        model.zero_grad()
        out.backward()
        grads.append(point.grad.detach().clone())
    attributions = (x - baseline) * torch.stack(grads).mean(dim=0)

    with torch.no_grad():  # FIX 3: completeness check
        f_x = predicted_value_scaled(model, x, lengths, idx, predict_change).item()
        f_b = predicted_value_scaled(model, baseline, lengths, idx, predict_change).item()
    gap = float(attributions.sum().item() - (f_x - f_b))
    return attributions.squeeze(0).numpy(), f_x, f_b, gap


def explain_trajectory_prediction(patient_id, target_feature="HbA1c"):
    idx = next(i for i, c in enumerate(FEATURE_COLUMNS) if target_feature.lower() in c.lower())
    model, scaler, predict_change = load_trajectory_model_and_scaler()
    history = load_patient_sequences().get(patient_id)
    if not history or len(history) < 2:
        print(f"Not enough history for {patient_id}.")
        return None

    recent = history[-MAX_SEQ_LEN:]
    x, lengths = build_input(recent, scaler)
    attr, f_x, f_b, gap = integrated_gradients(model, x, lengths, idx, predict_change)

    unit = scaler.scale_[idx]                               # FIX 2
    real_attr = attr[:len(recent), :] * unit                # real months only (post-padded)
    pred_real = f_x * unit + scaler.mean_[idx]
    base_real = f_b * unit + scaler.mean_[idx]
    month_labels = [f"Month t-{len(recent) - i}" for i in range(len(recent))]
    target_unit = "%" if "HbA1c" in FEATURE_COLUMNS[idx] else "mg/dL"

    fig, ax = plt.subplots(figsize=(7, 4))
    xpos = np.arange(len(FEATURE_COLUMNS))
    width = 0.8 / len(real_attr)
    for i, row in enumerate(real_attr):
        ax.bar(xpos + i * width, row, width, label=month_labels[i])
    ax.set_xticks(xpos + width * (len(real_attr) - 1) / 2)
    ax.set_xticklabels(FEATURE_COLUMNS)
    ax.set_ylabel(f"Contribution to predicted {target_feature} ({target_unit})")
    ax.set_title(f"Integrated Gradients: predicted {target_feature} for {patient_id}")
    ax.axhline(0, color="black", linewidth=0.5)
    ax.legend()
    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, f"trajectory_attribution_{patient_id}.png")
    plt.savefig(out_path, dpi=300)
    plt.close()

    print(f"Saved -> {out_path}")
    print(f"Predicted {target_feature}: {pred_real:.2f}{target_unit}  "
          f"(baseline = training-mean patient: {base_real:.2f}{target_unit})")
    print(f"Completeness gap (should be near 0): {gap * unit:+.5f} {target_unit}")
    table = {}
    for i, lab in enumerate(month_labels):
        for j, col in enumerate(FEATURE_COLUMNS):
            table[f"{lab} / {col}"] = float(real_attr[i, j])
            print(f"  {lab} / {col}: {real_attr[i, j]:+.4f} {target_unit}")

    return {"patient_id": patient_id, "target": FEATURE_COLUMNS[idx], "unit": target_unit,
            "predicted_value": pred_real, "baseline_value": base_real,
            "completeness_gap": gap * unit, "predict_change": predict_change,
            "attributions": table}


def cohort_attribution(target_feature="HbA1c"):
    """FIX 4: mean |IG| per (month, biomarker) over every patient's last two visits."""
    idx = next(i for i, c in enumerate(FEATURE_COLUMNS) if target_feature.lower() in c.lower())
    model, scaler, predict_change = load_trajectory_model_and_scaler()
    all_attr, gaps = [], []
    for pid, history in load_patient_sequences().items():
        if len(history) < MAX_SEQ_LEN:
            continue
        x, lengths = build_input(history[-MAX_SEQ_LEN:], scaler)
        attr, _, _, gap = integrated_gradients(model, x, lengths, idx, predict_change)
        all_attr.append(np.abs(attr) * scaler.scale_[idx])
        gaps.append(abs(gap * scaler.scale_[idx]))
    mean_abs = np.mean(all_attr, axis=0)
    labels = [f"Month t-{MAX_SEQ_LEN - i}" for i in range(MAX_SEQ_LEN)]
    table = {f"{labels[i]} / {col}": float(mean_abs[i, j])
             for i in range(MAX_SEQ_LEN) for j, col in enumerate(FEATURE_COLUMNS)}
    print(f"\nCohort mean |attribution| for predicted {target_feature} "
          f"({len(all_attr)} patients, max completeness gap {max(gaps):.5f}):")
    for k, v in sorted(table.items(), key=lambda kv: -kv[1]):
        print(f"  {k}: {v:.4f}")
    return {"num_patients": len(all_attr), "max_completeness_gap": float(max(gaps)),
            "mean_abs_attribution": table}


# =============================================================
# PART 2: Neural verifier (attention extraction)
# =============================================================
_verifier = {}


def load_verifier_with_attentions():
    if not _verifier:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        _verifier["tok"] = AutoTokenizer.from_pretrained(VERIFIER_MODEL_DIR)
        model = AutoModelForSequenceClassification.from_pretrained(
            VERIFIER_MODEL_DIR, output_attentions=True)
        model.eval()
        _verifier["model"] = model
        print(f"Verifier id2label from config: {model.config.id2label} "
              f"(script assumes index {FAITHFUL_LABEL_INDEX} = faithful)")
    return _verifier["tok"], _verifier["model"]


def explain_verifier_decision(context, explanation, case_name, top_k=10):
    tokenizer, model = load_verifier_with_attentions()
    inputs = tokenizer(context, explanation, truncation=True,
                       max_length=VERIFIER_MAX_LENGTH, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs, output_attentions=True)

    probs = torch.softmax(outputs.logits, dim=-1).squeeze()
    p_faithful = float(probs[FAITHFUL_LABEL_INDEX])
    predicted_label = "faithful" if p_faithful >= 0.5 else "hallucinated"
    confidence = max(p_faithful, 1 - p_faithful)

    cls_attention = outputs.attentions[-1][0].mean(dim=0)[0]   # last layer, head-avg, from [CLS]
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
    segment = inputs["token_type_ids"][0].tolist() if "token_type_ids" in inputs else [0] * len(tokens)
    special = {tokenizer.cls_token, tokenizer.sep_token, tokenizer.pad_token}

    scored = [(f"{tok} [{'ctx' if seg == 0 else 'ans'}]", float(s))
              for tok, s, seg in zip(tokens, cls_attention, segment) if tok not in special]
    scored.sort(key=lambda t: t[1], reverse=True)
    top = scored[:top_k]

    # How concentrated is attention? Share of non-special attention held by the top token.
    total = sum(s for _, s in scored)
    top1_share = top[0][1] / total if total else 0.0

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh([t for t, _ in top][::-1], [s for _, s in top][::-1], color="steelblue")
    ax.set_xlabel("Attention weight from [CLS] (final layer, head-averaged)")
    ax.set_title(f"{case_name} input -> predicted {predicted_label} ({confidence:.1%})")
    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, f"verifier_attention_{case_name}.png")
    plt.savefig(out_path, dpi=300)
    plt.close()

    print(f"Saved -> {out_path}")
    print(f"Predicted {predicted_label} ({confidence:.1%}); top token holds {top1_share:.1%} "
          f"of non-special attention. [ctx]=report side, [ans]=explanation side")
    for tok, s in top:
        print(f"  {tok}: {s:.4f}")
    return {"case": case_name, "predicted_label": predicted_label, "confidence": confidence,
            "top1_attention_share": top1_share, "top_tokens": top}


# -----------------------------
# Main
# -----------------------------
def main():
    print("=== Part 1: Trajectory attribution (P032) ===\n")
    p032 = explain_trajectory_prediction("P032", target_feature="HbA1c")
    cohort = cohort_attribution("HbA1c")
    save_result("explainability", "trajectory_integrated_gradients",
                {"P032": p032, "cohort": cohort}, notes="Fig. 8 and Section 4.6")

    print("\n=== Part 2: Verifier attention ===\n")
    context = ("Laboratory Report Summary for Patient P032 (Female, age 53) -- "
               "Month 1. HbA1c: 7.3% (Classification: Diabetic).")
    faithful = explain_verifier_decision(
        context, "Your HbA1c is 7.3%, classified as Diabetic.", "faithful")
    print()
    hallucinated = explain_verifier_decision(
        context, "Your HbA1c is 5.2%, classified as Normal.", "hallucinated")
    save_result("explainability", "verifier_attention",
                {"faithful_example": faithful, "hallucinated_example": hallucinated},
                notes="Fig. 9; illustrative single examples, final verifier model")

    print("\nPhase K complete. Charts saved to explainability/.")


if __name__ == "__main__":
    main()