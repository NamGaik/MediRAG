"""
phase_l_rescore_verifier.py

Rescores your ALREADY-SAVED benchmark_results.json (from your first
phase_l_benchmark.py run) using the FIXED claim-level, chunk-matched
verifier -- without making any new Claude API calls.

Why this is free:
    The saved results already contain every generated answer -- we
    don't need to regenerate them. The only new work is:
    1. Re-running RETRIEVAL for the full_system answers (free -- this
       is local FAISS + BioClinicalBERT, no API call, since it's the
       same deterministic index as before).
    2. Re-scoring with the fixed verify_answer_by_matched_chunks()
       (free -- this runs your already-trained verifier locally).

    Only rule_flag_rate and trap_safety_rate stay as originally
    computed (those were never broken -- only the neural verifier's
    whole-answer scoring was). This script only corrects the
    verifier_faithful_rate numbers.

Run this from your MediRAG root folder, AFTER phase_l_benchmark.py has
already produced evaluation/benchmark_results.json.

Requirements: same as phase_l_benchmark.py, but NO Anthropic API key needed.
"""

import os
import json

from phase_ef_vectorDB import retrieve_top_k, load_index
from phase_i_neural_verifier import verify_answer_by_matched_chunks

RESULTS_PATH = os.path.join("evaluation", "benchmark_results.json")
RESCORED_RESULTS_PATH = os.path.join("evaluation", "benchmark_results_rescored.json")
RESCORED_SUMMARY_PATH = os.path.join("evaluation", "benchmark_summary_rescored.json")


def rescore_full_system_entry(entry, index, metadata):
    """
    Re-retrieves the same chunks that would have been used originally
    (deterministic given the same query + patient_filter), then
    re-scores the already-generated full_system answer with the fixed
    verifier. Returns the new verifier result.
    """
    query_text = entry["query_text"]
    patient_id = entry["patient_id"]
    answer_text = entry["full_system"]["answer"]

    retrieved_chunks = retrieve_top_k(
        query_text, k=5, index=index, metadata=metadata, patient_filter=patient_id
    )

    if not retrieved_chunks:
        return {"overall_label": "not_verifiable", "claim_results": [], "skipped_claims": [], "correction_claims": []}

    return verify_answer_by_matched_chunks(answer_text, retrieved_chunks)


def rescore_all(all_results, index, metadata):
    for query_set_name in ["category_a", "category_c"]:
        for entry in all_results[query_set_name]:
            new_verifier_result = rescore_full_system_entry(entry, index, metadata)

            entry["full_system"]["verifier_label"] = new_verifier_result["overall_label"]
            entry["full_system"]["verifier_claims_checked"] = len(new_verifier_result["claim_results"])
            entry["full_system"]["verifier_claims_skipped"] = len(new_verifier_result["skipped_claims"])
            entry["full_system"]["verifier_corrections_excluded"] = len(new_verifier_result["correction_claims"])
            entry["full_system"]["verifier_claim_details"] = new_verifier_result["claim_results"]

            print(f"[{query_set_name}] {entry['query_id']}: "
                  f"verifier -> {new_verifier_result['overall_label']} "
                  f"({len(new_verifier_result['claim_results'])} checked, "
                  f"{len(new_verifier_result['skipped_claims'])} skipped, "
                  f"{len(new_verifier_result['correction_claims'])} corrections excluded)")

    return all_results


def summarize_verifier_only(all_results):
    """Recomputes just the verifier faithful rate for the full_system variant with corrected data."""
    faithful_count = 0
    hallucinated_count = 0
    not_verifiable_count = 0

    for query_set_name in ["category_a", "category_c"]:
        for entry in all_results[query_set_name]:
            label = entry["full_system"].get("verifier_label")
            if label == "faithful":
                faithful_count += 1
            elif label == "hallucinated":
                hallucinated_count += 1
            elif label == "not_verifiable":
                not_verifiable_count += 1

    total_scored = faithful_count + hallucinated_count
    faithful_rate = round(faithful_count / total_scored, 3) if total_scored else None

    summary = {
        "verifier_faithful_count": faithful_count,
        "verifier_hallucinated_count": hallucinated_count,
        "verifier_not_verifiable_count": not_verifiable_count,
        "verifier_faithful_rate": faithful_rate,
    }

    print("\n=== CORRECTED VERIFIER SUMMARY (full_system variant) ===")
    print(f"Faithful:       {faithful_count}")
    print(f"Hallucinated:   {hallucinated_count}")
    print(f"Not verifiable: {not_verifiable_count} (answers with no single-chunk-checkable claims)")
    print(f"Faithful rate:  {faithful_rate}")

    return summary


def main():
    if not os.path.exists(RESULTS_PATH):
        print(f"Could not find {RESULTS_PATH} -- run phase_l_benchmark.py first.")
        return

    with open(RESULTS_PATH, "r") as f:
        all_results = json.load(f)

    print("Loading vector index (local, no API cost)...")
    index, metadata = load_index()

    print("\nRescoring all full_system answers with the fixed verifier...\n")
    all_results = rescore_all(all_results, index, metadata)

    with open(RESCORED_RESULTS_PATH, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nSaved rescored results -> {RESCORED_RESULTS_PATH}")

    summary = summarize_verifier_only(all_results)
    with open(RESCORED_SUMMARY_PATH, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved corrected verifier summary -> {RESCORED_SUMMARY_PATH}")

    print("\nRescoring complete -- zero new Claude API calls were made.")
    print("Your rule_flag_rate and trap_safety_rate numbers from the original run are still valid;")
    print("only the verifier_faithful_rate needed correcting.")


if __name__ == "__main__":
    main()