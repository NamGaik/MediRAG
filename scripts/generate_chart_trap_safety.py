"""
generate_chart_trap_safety.py

Generates the trap safety rate chart DIRECTLY from your real saved
benchmark results -- not from remembered numbers. Reads
evaluation/benchmark_summary_final.json (or benchmark_summary_normalized.json
if you prefer the coverage-normalized version).

Run this from your MediRAG root folder.

Requirements: pip install matplotlib
"""

import json
import matplotlib.pyplot as plt

SUMMARY_PATH = "evaluation/benchmark_summary_final.json"  # ADJUST if using the normalized version instead
OUTPUT_PATH = "evaluation/chart_trap_safety_ladder.png"

with open(SUMMARY_PATH, "r") as f:
    summary = json.load(f)

variants = ["plain_llm", "standard_rag", "rag_with_rules", "full_system"]
labels = ["Plain LLM", "Standard RAG", "RAG + Rules", "Full System"]
trap_safety = [summary[v]["trap_safety_rate"] for v in variants]

fig, ax = plt.subplots(figsize=(7, 4.5))
colors = ["#A2453B", "#B98B4E", "#6B8F71", "#3D6B66"]
bars = ax.bar(labels, trap_safety, color=colors)
ax.set_ylabel("Trap Safety Rate")
ax.set_ylim(0, max(trap_safety) + 0.15)
ax.set_title("Trap Safety Rate Across System Configurations\n(from real benchmark data)")
for bar, val in zip(bars, trap_safety):
    ax.text(bar.get_x() + bar.get_width() / 2, val + 0.015, f"{val:.2f}", ha="center", fontweight="bold")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=200)
print(f"Saved -> {OUTPUT_PATH}")
print(f"Values used (from your real data): {dict(zip(labels, trap_safety))}")