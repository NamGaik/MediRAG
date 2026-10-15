"""
generate_chart_v2_results.py

Fig. 7 for the revised paper, drawn directly from the final scored results
(no numbers typed in):
  (a) Patient queries: correct / error / no patient data, per configuration
  (b) Trap queries: share answered safely, with 95% confidence intervals

Run from the MediRAG root, AFTER:  python phase_l_9_final_scores.py score
Output: figures/fig7_v2_results.png (300 dpi)
"""
import json
import os

import matplotlib.pyplot as plt
import numpy as np

RESULTS_PATH = os.path.join("results", "benchmark_v2", "final_tables_run1.json")
OUT_PATH = os.path.join("figures", "fig7_v2_results.png")
CONFIGS = ["plain_llm", "standard_rag", "full_system", "full_system_corrective"]
NAMES = ["Plain LLM", "Standard RAG", "Full system", "Full +\ncorrective"]

with open(RESULTS_PATH) as f:
    data = json.load(f)["results"]
pa, t4 = data["patient_answers"], data["table_iv"]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4), gridspec_kw={"width_ratios": [1.15, 1]})
x = np.arange(len(CONFIGS))

# (a) patient answers, as shares of n with counts printed
parts = [("correct", "Correct", "#3D6B66"), ("error", "Error", "#A2453B"),
         ("no_patient_data", "No patient data", "#C9C9C9")]
bottom = np.zeros(len(CONFIGS))
for key, label, colour in parts:
    share = np.array([pa[c][key] / pa[c]["n"] for c in CONFIGS])
    ax1.bar(x, share, 0.6, bottom=bottom, color=colour, label=label, edgecolor="white")
    for i, c in enumerate(CONFIGS):
        if pa[c][key]:
            ax1.text(x[i], bottom[i] + share[i] / 2, f"{pa[c][key]}/{pa[c]['n']}",
                     ha="center", va="center", fontsize=8.5,
                     color="white" if key != "no_patient_data" else "black")
    bottom += share
ax1.set_xticks(x)
ax1.set_xticklabels(NAMES, fontsize=9)
ax1.set_ylim(0, 1)
ax1.set_ylabel("Share of patient-query answers")
ax1.set_title("(a) Patient queries", fontsize=11)
ax1.legend(fontsize=8.5, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=3)

# (b) trap safety with Wilson 95% CI
rate = np.array([t4[c]["rate"] for c in CONFIGS])
lo = np.array([t4[c]["ci95"][0] for c in CONFIGS])
hi = np.array([t4[c]["ci95"][1] for c in CONFIGS])
ax2.bar(x, rate, 0.6, color="#3D6B66")
ax2.errorbar(x, rate, yerr=[rate - lo, hi - rate], fmt="none", ecolor="black", capsize=4, lw=1)
for i, c in enumerate(CONFIGS):
    ax2.text(x[i], 0.06, f"{t4[c]['safe']}/{t4[c]['n']}", ha="center", color="white", fontsize=9)
ax2.set_xticks(x)
ax2.set_xticklabels(NAMES, fontsize=9)
ax2.set_ylim(0, 1.05)
ax2.set_ylabel("Share of trap queries answered safely")
ax2.set_title("(b) Hallucination-trap queries (95% CI)", fontsize=11)

for ax in (ax1, ax2):
    ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
os.makedirs("figures", exist_ok=True)
plt.savefig(OUT_PATH, dpi=300, bbox_inches="tight")
print(f"Saved -> {OUT_PATH}")