"""
phase_l_normalize_rule_metric.py

Fixes the rule-flag-rate distortion identified in the benchmark: a
binary "was anything flagged" metric unfairly rewards answers that say
LITTLE (like plain_llm's frequent refusals, which have nothing to
check and trivially "pass") over answers that make many real,
checkable claims and get flagged on a small fraction of them.

This computes a COVERAGE-NORMALIZED issue rate instead:
    issue_rate = issues_found / checked_mentions

...averaged only over answers that actually made at least one
checkable claim. Answers with zero checkable claims (refusals, or
answers that never state a specific biomarker value) are excluded
from the issue-rate average entirely, but their COVERAGE (fraction of
answers with at least one checkable claim) is reported separately --
since a system that mostly refuses to answer is a different problem
than a system that answers but gets facts wrong, and conflating them
was exactly the original metric's flaw.

Requires re-running validate_entry() locally to reconstruct
checked_mentions, which wasn't saved in the original results -- this
is free (local computation, no API calls), same pattern as the
previous two rescoring scripts.

Run this from your MediRAG root folder, AFTER phase_l_rescore_rules.py
has already produced evaluation/benchmark_results_final.json.

Requirements: same as before. NO Anthropic API key needed.
"""

import os
import json

from phase_ef_vectorDB import retrieve_top_k, load_index
from phase_h_validation import load_severity_rules, validate_entry

INPUT_PATH = os.path.join("evaluation", "benchmark_results_final.json")
OUTPUT_SUMMARY_PATH = os.path.join("evaluation", "benchmark_summary_normalized.json")


def get_chunks_for_variant(variant_name, query_text, patient_id, index, metadata):
    """
    Reconstructs the retrieved_chunks each variant would have used, so
    validate_entry can be re-run consistently. plain_llm always used
    none; the other three all used the same patient-scoped retrieval.
    """
    if variant_name == "plain_llm":
        return []
    return retrieve_top_k(query_text, k=5, index=index, metadata=metadata, patient_filter=patient_id)


def compute_normalized_metrics(all_results, rules, index, metadata):
    variants = ["plain_llm", "standard_rag", "rag_with_rules", "full_system"]
    per_variant_rates = {v: [] for v in variants}
    per_variant_coverage = {v: {"with_claims": 0, "total": 0} for v in variants}

    for query_set_name in ["category_a", "category_c"]:
        for entry in all_results[query_set_name]:
            query_text = entry["query_text"]
            patient_id = entry["patient_id"]

            for variant in variants:
                answer_text = entry[variant]["answer"]
                chunks = get_chunks_for_variant(variant, query_text, patient_id, index, metadata)

                validation = validate_entry(
                    {"query": query_text, "answer": answer_text, "retrieved_chunks": chunks},
                    rules
                )
                checked = validation["checked_mentions"]
                issues = validation["issues_found"]

                per_variant_coverage[variant]["total"] += 1
                if checked > 0:
                    per_variant_coverage[variant]["with_claims"] += 1
                    per_variant_rates[variant].append(issues / checked)
                # answers with checked == 0 are excluded from the rate
                # average entirely -- nothing to measure, not a "pass"

    print("\n=== NORMALIZED RULE METRIC (coverage-aware) ===\n")
    print(f"{'Variant':<18} {'Avg Issue Rate':<18} {'Coverage (has claims)'}")

    summary = {}
    for variant in variants:
        rates = per_variant_rates[variant]
        avg_rate = round(sum(rates) / len(rates), 3) if rates else None
        coverage = round(
            per_variant_coverage[variant]["with_claims"] / per_variant_coverage[variant]["total"], 3
        )
        summary[variant] = {
            "avg_issue_rate": avg_rate,
            "coverage": coverage,
            "n_answers_with_claims": per_variant_coverage[variant]["with_claims"],
            "n_total_answers": per_variant_coverage[variant]["total"],
        }
        print(f"{variant:<18} {str(avg_rate):<18} {coverage} "
              f"({per_variant_coverage[variant]['with_claims']}/{per_variant_coverage[variant]['total']} answers)")

    print("\navg_issue_rate = issues_found / checkable_claims, averaged ONLY over answers")
    print("that made at least one checkable claim. LOWER is better.")
    print("coverage = fraction of answers that made at least one checkable claim --")
    print("this is reported separately since a low-coverage system (frequent refusals)")
    print("is a different problem than a system that answers but states wrong facts.")

    return summary


def main():
    if not os.path.exists(INPUT_PATH):
        print(f"Could not find {INPUT_PATH} -- run phase_l_rescore_rules.py first.")
        return

    with open(INPUT_PATH, "r") as f:
        all_results = json.load(f)

    print("Loading rules and vector index (local, no API cost)...")
    rules = load_severity_rules()
    index, metadata = load_index()

    summary = compute_normalized_metrics(all_results, rules, index, metadata)

    with open(OUTPUT_SUMMARY_PATH, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved -> {OUTPUT_SUMMARY_PATH}")
    print("\nDone -- zero new Claude API calls were made.")


if __name__ == "__main__":
    main()