"""
generate_chart_verifier_comparison.py

Generates the "before/after" verifier comparison chart by RECOMPUTING
both scoring methods live, directly on your real saved generated
answers -- this is necessary because the intermediate "before" result
was overwritten when the claim-decomposition fix was applied earlier,
so there is no single saved file containing both numbers. This script
reconstructs both from your actual saved answers + your actual trained
verifier model, so both numbers are genuinely real and reproducible,
not remembered from earlier conversation.

Run this from your MediRAG root folder.

Requirements: pip install matplotlib
"""

import json
import matplotlib.pyplot as plt

from phase_ef_vectorDB import retrieve_top_k, load_index
from phase_i_neural_verifier import predict_faithfulness, verify_answer_by_matched_chunks

RESULTS_PATH = "evaluation/benchmark_results_final.json"  # ADJUST if your final results file has a different name
OUTPUT_PATH = "evaluation/chart_verifier_comparison.png"


def score_whole_answer_method(entry, index, metadata):
    """The ORIGINAL method: check the whole multi-visit answer against the full combined context at once."""
    chunks = retrieve_top_k(
        entry["query_text"], k=5, index=index, metadata=metadata, patient_filter=entry["patient_id"]
    )
    if not chunks:
        return None
    combined_context = " ".join(c["text"] for c in chunks)
    result = predict_faithfulness(combined_context, entry["full_system"]["answer"])
    return result["predicted_label"]


def score_decomposition_method(entry, index, metadata):
    """The FIXED method: decompose into claims, match each to its own chunk."""
    chunks = retrieve_top_k(
        entry["query_text"], k=5, index=index, metadata=metadata, patient_filter=entry["patient_id"]
    )
    if not chunks:
        return None
    result = verify_answer_by_matched_chunks(entry["full_system"]["answer"], chunks)
    return result["overall_label"]


with open(RESULTS_PATH, "r") as f:
    all_results = json.load(f)

index, metadata = load_index()

whole_answer_faithful = 0
whole_answer_total = 0
decomposition_faithful = 0
decomposition_total = 0

for query_set in ["category_a", "category_c"]:
    for entry in all_results[query_set]:
        label_a = score_whole_answer_method(entry, index, metadata)
        if label_a in ("faithful", "hallucinated"):
            whole_answer_total += 1
            if label_a == "faithful":
                whole_answer_faithful += 1

        label_b = score_decomposition_method(entry, index, metadata)
        if label_b in ("faithful", "hallucinated"):
            decomposition_total += 1
            if label_b == "faithful":
                decomposition_faithful += 1

rate_before = whole_answer_faithful / whole_answer_total if whole_answer_total else 0
rate_after = decomposition_faithful / decomposition_total if decomposition_total else 0
total_answers = sum(len(all_results[q]) for q in ["category_a", "category_c"])

print(f"Answers in benchmark: {total_answers} | with retrievable context: {whole_answer_total}")
print(f"Whole-answer method:        {whole_answer_faithful}/{whole_answer_total} = {rate_before:.1%}")
print(f"Claim-decomposition method: {decomposition_faithful}/{decomposition_total} = {rate_after:.1%}")

fig, ax = plt.subplots(figsize=(6, 4.5))
methods = [f"Whole-answer scoring\n(n = {whole_answer_total} answers)",
           f"Claim-decomposition scoring\n(n = {decomposition_total} answers)"]
rates = [rate_before, rate_after]
counts = [f"{whole_answer_faithful}/{whole_answer_total}", f"{decomposition_faithful}/{decomposition_total}"]
bars = ax.bar(methods, rates, color=["#A2453B", "#3D6B66"], width=0.5)
ax.set_ylabel("Share of answers labelled faithful")
ax.set_ylim(0, 1.05)
ax.set_title("Verifier faithful rate: whole-answer vs claim-level scoring")
for bar, val, c in zip(bars, rates, counts):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 0.02, f"{val:.1%}\n({c})",
            ha="center", fontweight="bold")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=300)
print(f"Saved -> {OUTPUT_PATH}")

from results_logger import save_result
save_result("verifier", "fig6_whole_vs_decomposition", {
    "total_answers": total_answers,
    "answers_with_context": whole_answer_total,
    "whole_answer": {"faithful": whole_answer_faithful, "n": whole_answer_total, "rate": rate_before},
    "decomposition": {"faithful": decomposition_faithful, "n": decomposition_total, "rate": rate_after},
}, notes="Fig. 6, final verifier, recomputed on saved full_system answers")