"""
phase_l_rescore_rules.py

Completes the rule-validation comparison ladder WITHOUT any new Claude
API calls. Your first benchmark run only computed rule_flagged for
rag_with_rules and full_system -- plain_llm and standard_rag were left
with no rule-validation data at all, showing as "None" in the summary.

This script fixes that for free:
    - plain_llm: uses an empty retrieved_chunks list (it never had any
      grounding context), so any specific biomarker value it states
      gets correctly flagged as unverifiable -- exactly the signal an
      ungrounded baseline SHOULD produce.
    - standard_rag: re-retrieves the same chunks it would have used
      (free, local, deterministic) and validates its ALREADY-SAVED
      answer against them.

Builds on top of benchmark_results_rescored.json (which already has
the corrected verifier data from phase_l_rescore_verifier.py) so this
produces ONE final, complete results file with everything corrected.

Run this from your MediRAG root folder, AFTER phase_l_rescore_verifier.py
has already produced evaluation/benchmark_results_rescored.json.

Requirements: same as before. NO Anthropic API key needed.
"""

import os
import json

from phase_ef_vectorDB import retrieve_top_k, load_index
from phase_h_validation import load_severity_rules, validate_entry

INPUT_PATH = os.path.join("evaluation", "benchmark_results_rescored.json")
FINAL_RESULTS_PATH = os.path.join("evaluation", "benchmark_results_final.json")
FINAL_SUMMARY_PATH = os.path.join("evaluation", "benchmark_summary_final.json")


def rescore_rules_for_entry(entry, rules, index, metadata):
    """Adds rule_flagged/issues_found to plain_llm and standard_rag for one query."""
    query_text = entry["query_text"]
    patient_id = entry["patient_id"]

    # plain_llm -- no retrieval ever happened, so context is empty
    plain_validation = validate_entry(
        {"query": query_text, "answer": entry["plain_llm"]["answer"], "retrieved_chunks": []},
        rules
    )
    entry["plain_llm"]["rule_flagged"] = plain_validation["status"] == "FLAGGED"
    entry["plain_llm"]["issues_found"] = plain_validation["issues_found"]

    # standard_rag -- re-retrieve the same chunks it would have used (free, local)
    retrieved_chunks = retrieve_top_k(
        query_text, k=5, index=index, metadata=metadata, patient_filter=patient_id
    )
    rag_validation = validate_entry(
        {"query": query_text, "answer": entry["standard_rag"]["answer"], "retrieved_chunks": retrieved_chunks},
        rules
    )
    entry["standard_rag"]["rule_flagged"] = rag_validation["status"] == "FLAGGED"
    entry["standard_rag"]["issues_found"] = rag_validation["issues_found"]

    return entry


def build_final_summary(all_results):
    """Recomputes the complete comparison table across all 4 variants, all metrics."""
    variants = ["plain_llm", "standard_rag", "rag_with_rules", "full_system"]
    summary = {}

    for variant in variants:
        flagged_count = 0
        total_checked = 0
        trap_safe_count = 0
        total_traps = 0
        verifier_faithful = 0
        verifier_hallucinated = 0

        for query_set in ["category_a", "category_c"]:
            for entry in all_results[query_set]:
                v = entry[variant]
                if "rule_flagged" in v:
                    total_checked += 1
                    if v["rule_flagged"]:
                        flagged_count += 1
                if query_set == "category_c" and v.get("trap_safe") is not None:
                    total_traps += 1
                    if v["trap_safe"]:
                        trap_safe_count += 1
                if v.get("verifier_label") == "faithful":
                    verifier_faithful += 1
                elif v.get("verifier_label") == "hallucinated":
                    verifier_hallucinated += 1

        total_verified = verifier_faithful + verifier_hallucinated
        summary[variant] = {
            "rule_flag_rate": round(flagged_count / total_checked, 3) if total_checked else None,
            "trap_safety_rate": round(trap_safe_count / total_traps, 3) if total_traps else None,
            "verifier_faithful_rate": round(verifier_faithful / total_verified, 3) if total_verified else None,
        }

    print("\n=== FINAL COMPLETE BENCHMARK SUMMARY ===\n")
    print(f"{'Variant':<18} {'Rule Flag Rate':<18} {'Trap Safety Rate':<18} {'Verifier Faithful Rate'}")
    for variant in variants:
        s = summary[variant]
        print(f"{variant:<18} {str(s['rule_flag_rate']):<18} {str(s['trap_safety_rate']):<18} {str(s['verifier_faithful_rate'])}")

    print("\nLOWER rule_flag_rate is better. HIGHER trap_safety_rate and verifier_faithful_rate are better.")
    print("verifier_faithful_rate only applies to full_system (the only variant scored by the neural verifier).")

    return summary


def main():
    if not os.path.exists(INPUT_PATH):
        print(f"Could not find {INPUT_PATH} -- run phase_l_rescore_verifier.py first.")
        return

    with open(INPUT_PATH, "r") as f:
        all_results = json.load(f)

    print("Loading rules and vector index (local, no API cost)...")
    rules = load_severity_rules()
    index, metadata = load_index()

    print("\nCompleting rule validation for plain_llm and standard_rag...\n")
    for query_set_name in ["category_a", "category_c"]:
        for entry in all_results[query_set_name]:
            all_results[query_set_name][all_results[query_set_name].index(entry)] = \
                rescore_rules_for_entry(entry, rules, index, metadata)
            print(f"[{query_set_name}] {entry['query_id']}: "
                  f"plain_llm flagged={entry['plain_llm']['rule_flagged']}, "
                  f"standard_rag flagged={entry['standard_rag']['rule_flagged']}")

    with open(FINAL_RESULTS_PATH, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nSaved final complete results -> {FINAL_RESULTS_PATH}")

    summary = build_final_summary(all_results)
    with open(FINAL_SUMMARY_PATH, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved final summary -> {FINAL_SUMMARY_PATH}")

    print("\nDone -- zero new Claude API calls were made. This is your complete,")
    print("final benchmark table, ready for your paper's Results section.")


if __name__ == "__main__":
    main()