"""
generate_chart_fig6_v2.py

Fig. 6 for the revised paper, computed on the v2 benchmark's full-system
answers (the same run as Tables IV-V and Fig. 7):
  * whole-answer scoring: each answer checked against its full combined context
  * claim-level scoring: the per-claim, chunk-matched labels already saved
    by the v2 benchmark
No API calls. Loads the trained verifier (a few minutes on CPU).

Run from the MediRAG root:  python generate_chart_fig6_v2.py
Output: figures/fig6_verifier_v2.png (300 dpi) + results/verifier/fig6_v2.json
"""
import json
import os

import matplotlib.pyplot as plt

from phase_ef_vectorDB import retrieve_top_k, load_index
from phase_i_neural_verifier import predict_faithfulness
from results_logger import save_result

RESULTS_PATH = os.path.join("evaluation", "v2", "benchmark_v2_results_run1.json")
OUT_PATH = os.path.join("figures", "fig6_verifier_v2.png")
CONFIG = "full_system"

with open(RESULTS_PATH) as f:
    results = json.load(f)
index, metadata = load_index()

whole = {"faithful": 0, "hallucinated": 0}
claim_answers = {"faithful": 0, "hallucinated": 0, "not_verifiable": 0}
claims = {"faithful": 0, "hallucinated": 0}
no_context = 0

for i, (qid, rec) in enumerate(results.items(), 1):
    e = rec["configs"].get(CONFIG)
    if e is None:
        continue
    pid = rec.get("patient_id")
    chunks = retrieve_top_k(rec["query_text"], k=5, index=index, metadata=metadata,
                            patient_filter=pid) if pid else []
    if not chunks:
        no_context += 1
        continue
    # whole-answer scoring
    label = predict_faithfulness(" ".join(c["text"] for c in chunks), e["answer"])["predicted_label"]
    whole[label] += 1
    # claim-level scoring (saved by the benchmark)
    claim_answers[e.get("verifier_label", "not_verifiable")] = \
        claim_answers.get(e.get("verifier_label", "not_verifiable"), 0) + 1
    for c in e.get("verifier_claims", []):
        claims[c["label"]] += 1
    print(f"[{i}/{len(results)}] {qid}: whole={label}  claim-level={e.get('verifier_label')}")

n_whole = whole["faithful"] + whole["hallucinated"]
n_claim = claim_answers["faithful"] + claim_answers["hallucinated"]
n_claims = claims["faithful"] + claims["hallucinated"]
rate_whole = whole["faithful"] / n_whole if n_whole else 0
rate_claim = claim_answers["faithful"] / n_claim if n_claim else 0

print(f"\nAnswers with context: {n_whole} (no context: {no_context})")
print(f"Whole-answer:  {whole['faithful']}/{n_whole} faithful = {rate_whole:.1%}")
print(f"Claim-level:   {claim_answers['faithful']}/{n_claim} answers faithful = {rate_claim:.1%} "
      f"({claim_answers['not_verifiable']} answers had no single-visit claim)")
print(f"Individual claims: {claims['faithful']}/{n_claims} faithful")

fig, ax = plt.subplots(figsize=(6, 4.5))
labels = [f"Whole-answer scoring\n(n = {n_whole} answers)",
          f"Claim-level scoring\n(n = {n_claim} answers)"]
bars = ax.bar(labels, [rate_whole, rate_claim], color=["#A2453B", "#3D6B66"], width=0.5)
for bar, rate, txt in zip(bars, [rate_whole, rate_claim],
                          [f"{whole['faithful']}/{n_whole}", f"{claim_answers['faithful']}/{n_claim}"]):
    ax.text(bar.get_x() + bar.get_width() / 2, rate + 0.02, f"{rate:.1%}\n({txt})",
            ha="center", fontweight="bold")
ax.set_ylabel("Share of answers labelled faithful")
ax.set_ylim(0, 1.12)
ax.set_title("Verifier on full-system answers: whole-answer vs claim-level")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
os.makedirs("figures", exist_ok=True)
plt.savefig(OUT_PATH, dpi=300)
print(f"Saved -> {OUT_PATH}")

save_result("verifier", "fig6_v2", {
    "config": CONFIG, "answers_with_context": n_whole, "answers_without_context": no_context,
    "whole_answer": whole, "claim_level_answers": claim_answers, "individual_claims": claims,
}, notes="Fig. 6 on the v2 benchmark (same run as Tables IV-V)")