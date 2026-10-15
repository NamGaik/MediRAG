"""
phase_k_explainability.py

Phase K for Medi-RAG: Explainability Layer

Adds genuine model interpretability on top of the two trained models
from Phases I and J -- this is the piece that actually earns the
"explainable AI" claim in your paper, as distinct from grounding (which
only shows WHERE a fact came from, not WHY a model decided what it did).

Two different techniques are used, because the two models have
different architectures:

1. TRAJECTORY MODEL (GRU) -> Integrated Gradients
   A gradient-based attribution method (Sundararajan et al., 2017) that
   answers: "which past month and which biomarker most influenced this
   specific prediction?" Works by comparing gradients along a path from
   a zero baseline to the real input, and is a standard, citable
   technique for models without built-in attention.

2. NEURAL VERIFIER (BioClinicalBERT classifier) -> Attention extraction
   Since this model IS a transformer, it already computes attention
   weights internally. We extract the final layer's attention FROM the
   [CLS] token (which drives the classification decision) TO every
   other token, revealing which specific words in the report/explanation
   pair most influenced the faithful/hallucinated decision.

Honesty note for your paper: both of these are widely-used but
approximate interpretability techniques -- attention weights are a
heuristic proxy for "importance," not a rigorous causal explanation,
and this is worth stating explicitly in your limitations section rather
than overselling either method as ground truth.

Outputs:
    explainability/trajectory_attribution_<patient_id>.png
    explainability/verifier_attention_<label>.png

Run this from your MediRAG root folder, AFTER phase_j_trajectory_model.py
and phase_i_neural_verifier.py have both been run and saved their models.

Requirements:
    pip install torch transformers matplotlib numpy
"""

import os

import numpy as np
import torch
import matplotlib.pyplot as plt

from phase_j_trajectory_model import (
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


# =============================================================
# PART 1: Trajectory model explainability (Integrated Gradients)
# =============================================================
def load_trajectory_model_and_scaler():
    import pickle

    model = build_trajectory_model()
    model.load_state_dict(torch.load(os.path.join(TRAJECTORY_MODEL_DIR, "trajectory_gru.pt")))
    model.eval()
    with open(os.path.join(TRAJECTORY_MODEL_DIR, "scaler.pkl"), "rb") as f:
        scaler = pickle.load(f)
    return model, scaler


def integrated_gradients(model, input_tensor, length_tensor, target_output_idx=0, steps=50):
    """
    Computes Integrated Gradients attribution for the trajectory model's
    regression output at target_output_idx (0=HbA1c, 1=FBS, 2=PPBS).

    Method: interpolate `steps` points along a straight line from an
    all-zero baseline to the real input, compute the gradient of the
    target output with respect to the input at each point, average
    those gradients, then multiply by (input - baseline). This
    approximates each input feature's contribution to the final
    prediction (Sundararajan et al., 2017, "Axiomatic Attribution for
    Deep Networks").

    The all-zero baseline is a natural choice here since it matches the
    padding value already used for shorter sequences in this model.
    """
    baseline = torch.zeros_like(input_tensor)
    alphas = torch.linspace(0, 1, steps + 1)

    gradients = []
    for alpha in alphas[1:]:  # skip alpha=0 (baseline itself has undefined/zero gradient signal)
        interpolated = baseline + alpha * (input_tensor - baseline)
        interpolated = interpolated.clone().detach().requires_grad_(True)

        reg_out, _ = model(interpolated, length_tensor)
        target = reg_out[0, target_output_idx]

        model.zero_grad()
        target.backward()
        gradients.append(interpolated.grad.detach().clone())

    avg_gradients = torch.stack(gradients).mean(dim=0)
    attributions = (input_tensor - baseline) * avg_gradients
    return attributions.squeeze(0).numpy()  # shape: (MAX_SEQ_LEN, num_features)


def explain_trajectory_prediction(patient_id, target_feature="HbA1c"):
    """
    Runs Integrated Gradients for a real patient's trajectory prediction
    and saves a bar chart showing which (month, biomarker) combination
    most influenced the predicted value.
    """
    target_idx = FEATURE_COLUMNS.index(
        [c for c in FEATURE_COLUMNS if target_feature.lower() in c.lower()][0]
    )

    model, scaler = load_trajectory_model_and_scaler()
    sequences = load_patient_sequences()
    patient_history = sequences.get(patient_id)

    if not patient_history or len(patient_history) < 2:
        print(f"Not enough history for {patient_id} to explain a prediction.")
        return None

    recent_history = patient_history[-2:]
    history_values = [[month[col] for col in FEATURE_COLUMNS] for month in recent_history]
    history_scaled = scaler.transform(history_values)

    X = np.zeros((1, MAX_SEQ_LEN, len(FEATURE_COLUMNS)), dtype=np.float32)
    X[0, MAX_SEQ_LEN - len(recent_history):, :] = history_scaled
    input_tensor = torch.tensor(X)
    length_tensor = torch.tensor([len(recent_history)])

    attributions = integrated_gradients(model, input_tensor, length_tensor, target_output_idx=target_idx)

    # Only the real (non-padded) months have meaningful attribution
    real_months = attributions[MAX_SEQ_LEN - len(recent_history):, :]
    month_labels = [f"Month t-{len(recent_history) - i}" for i in range(len(recent_history))]

    fig, ax = plt.subplots(figsize=(7, 4))
    x = np.arange(len(FEATURE_COLUMNS))
    width = 0.8 / len(real_months)

    for i, month_attr in enumerate(real_months):
        ax.bar(x + i * width, month_attr, width, label=month_labels[i])

    ax.set_xticks(x + width * (len(real_months) - 1) / 2)
    ax.set_xticklabels(FEATURE_COLUMNS)
    ax.set_ylabel("Attribution (Integrated Gradients)")
    ax.set_title(f"What drove the predicted {target_feature} for {patient_id}?")
    ax.axhline(0, color="black", linewidth=0.5)
    ax.legend()
    plt.tight_layout()

    out_path = os.path.join(OUTPUT_DIR, f"trajectory_attribution_{patient_id}.png")
    plt.savefig(out_path, dpi=150)
    plt.close()

    print(f"Saved trajectory attribution chart -> {out_path}")
    print("Attribution values (higher magnitude = more influence on the prediction):")
    for i, month_attr in enumerate(real_months):
        for j, feature in enumerate(FEATURE_COLUMNS):
            print(f"  {month_labels[i]} / {feature}: {month_attr[j]:+.4f}")

    return real_months


# =============================================================
# PART 2: Neural verifier explainability (attention extraction)
# =============================================================
def load_verifier_with_attentions():
    from transformers import AutoTokenizer, AutoModelForSequenceClassification

    tokenizer = AutoTokenizer.from_pretrained(VERIFIER_MODEL_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(
        VERIFIER_MODEL_DIR, output_attentions=True
    )
    model.eval()
    return tokenizer, model


def explain_verifier_decision(context, explanation, top_k=10):
    """
    Runs the trained verifier on a (context, explanation) pair and
    extracts which tokens received the most attention FROM the [CLS]
    token in the final transformer layer -- the [CLS] token's
    representation is what the classification head actually uses to
    make its faithful/hallucinated decision, so its attention pattern
    is a reasonable (though approximate) proxy for "what the model
    focused on."
    """
    tokenizer, model = load_verifier_with_attentions()

    inputs = tokenizer(
        context, explanation,
        truncation=True, max_length=VERIFIER_MAX_LENGTH, padding=True,
        return_tensors="pt",
    )

    with torch.no_grad():
        outputs = model(**inputs, output_attentions=True)

    probs = torch.softmax(outputs.logits, dim=-1).squeeze()
    predicted_label = "faithful" if probs[1] > probs[0] else "hallucinated"
    confidence = float(max(probs))

    last_layer_attention = outputs.attentions[-1][0]      # (num_heads, seq_len, seq_len)
    avg_attention = last_layer_attention.mean(dim=0)       # (seq_len, seq_len)
    cls_attention = avg_attention[0]                       # CLS token's attention to all tokens

    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

    # Exclude special tokens from the ranking -- their high attention
    # scores are a structural BERT artifact, not meaningful content signal
    special_tokens = {tokenizer.cls_token, tokenizer.sep_token, tokenizer.pad_token}
    scored_tokens = [
        (tok, float(score)) for tok, score in zip(tokens, cls_attention)
        if tok not in special_tokens
    ]
    scored_tokens.sort(key=lambda x: x[1], reverse=True)
    top_tokens = scored_tokens[:top_k]

    fig, ax = plt.subplots(figsize=(7, 4))
    labels = [tok for tok, _ in top_tokens][::-1]
    values = [score for _, score in top_tokens][::-1]
    ax.barh(labels, values, color="steelblue")
    ax.set_xlabel("Attention weight from [CLS]")
    ax.set_title(f"Top tokens driving verifier decision: {predicted_label} ({confidence:.1%} confidence)")
    plt.tight_layout()

    out_path = os.path.join(OUTPUT_DIR, f"verifier_attention_{predicted_label}.png")
    plt.savefig(out_path, dpi=150)
    plt.close()

    print(f"Saved verifier attention chart -> {out_path}")
    print(f"Predicted: {predicted_label} ({confidence:.1%} confidence)")
    print(f"Top {top_k} tokens by attention:")
    for tok, score in top_tokens:
        print(f"  {tok}: {score:.4f}")

    return {"predicted_label": predicted_label, "confidence": confidence, "top_tokens": top_tokens}


# -----------------------------
# Main
# -----------------------------
def main():
    print("=== Part 1: Explaining a trajectory prediction (P032) ===\n")
    explain_trajectory_prediction("P032", target_feature="HbA1c")

    print("\n=== Part 2: Explaining verifier decisions ===\n")

    print("-- Faithful example --")
    faithful_context = (
        "Laboratory Report Summary for Patient P032 (Female, age 53) -- "
        "Month 1. HbA1c: 7.3% (Classification: Diabetic)."
    )
    faithful_explanation = "Your HbA1c is 7.3%, classified as Diabetic."
    explain_verifier_decision(faithful_context, faithful_explanation)

    print("\n-- Hallucinated example --")
    hallucinated_explanation = "Your HbA1c is 5.2%, classified as Normal."
    explain_verifier_decision(faithful_context, hallucinated_explanation)

    print("\nPhase K complete. Explainability charts saved to explainability/.")
    print("These figures are ready to drop into your paper's Methodology/Results sections.")


if __name__ == "__main__":
    main()