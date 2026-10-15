"""
debug_verifier.py

Diagnostic script to understand why phase_l_benchmark.py reported a
0.0 verifier faithful rate on the full_system variant, despite those
being genuinely correct, well-grounded answers (like the real P032
HbA1c answer we confirmed by hand earlier).

HYPOTHESIS being tested: the verifier was trained ONLY on short,
templated single-sentence examples (e.g. "Your HbA1c is 7.3%,
classified as Diabetic.") but real Claude answers are long,
multi-paragraph, conversational text with bullet points and hedging
language -- a distribution shift the verifier never saw during
training. This script checks that directly, plus a token-length /
truncation check as a second possible cause.

Run this from your MediRAG root folder, after phase_i_neural_verifier.py
has already trained and saved a model.
"""

import os
import json

from phase_i_neural_verifier import predict_faithfulness, MAX_LENGTH, wrap_realistic
import re


def decompose_answer_into_claims(answer_text):
    """
    Splits a real, long, multi-fact Claude answer into individual
    candidate factual claims -- e.g. turns:
        "- Month 1: 7.3% (Diabetic range)
         - Month 2: 6.7% (Diabetic range)"
    into two separate claim strings, each checkable on its own. This
    lets us reuse the EXISTING trained verifier (which only ever saw
    single-fact examples) without needing to retrain it on multi-fact
    input -- we just stop asking it to judge multiple facts at once.

    Keeps only lines/sentences containing a digit (likely to be an
    actual factual claim, not just narrative filler).
    """
    candidates = []

    # Bullet-point lines first (most real Claude answers use these for facts)
    for line in answer_text.split("\n"):
        stripped = line.strip("-* ").strip()
        if stripped and any(ch.isdigit() for ch in stripped) and len(stripped) < 200:
            candidates.append(stripped)

    # Also split any remaining prose into sentences, in case facts appear
    # outside of bullet points (e.g. "Your latest FBS was 137.0 mg/dL...")
    prose = re.sub(r"^[-*]\s.*$", "", answer_text, flags=re.MULTILINE)  # remove bullet lines already captured
    for sentence in re.split(r"(?<=[.!?])\s+", prose):
        sentence = sentence.strip()
        if sentence and any(ch.isdigit() for ch in sentence) and len(sentence) < 200:
            candidates.append(sentence)

    # De-duplicate while preserving order
    seen = set()
    unique_candidates = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            unique_candidates.append(c)

    return unique_candidates


def verify_answer_by_decomposition(context, answer_text):
    """
    The actual no-retraining fix: instead of checking the whole answer
    at once, decompose it into individual claims, wrap each in the same
    style the verifier was trained on, and check them one at a time.
    The answer is flagged hallucinated overall if ANY individual claim
    is flagged -- otherwise it's faithful.
    """
    claims = decompose_answer_into_claims(answer_text)
    claim_results = []

    for claim in claims:
        wrapped_claim = wrap_realistic(claim)
        result = predict_faithfulness(context, wrapped_claim)
        claim_results.append({"claim": claim, **result})

    overall_label = "hallucinated" if any(
        r["predicted_label"] == "hallucinated" for r in claim_results
    ) else "faithful"

    return {"overall_label": overall_label, "claim_results": claim_results}


def match_claim_to_chunk(claim_text, retrieved_chunks):
    """
    Finds the SINGLE chunk that actually corresponds to a claim's
    referenced month (e.g. a claim mentioning "Month 2" gets matched to
    ONLY that month's chunk, not the full multi-month context). This
    matches the training format exactly -- every training example paired
    one claim with exactly one chunk's worth of context, never a
    concatenation of several months at once.

    Returns None if no clear month reference is found (e.g. a narrative
    summary sentence, or a future-prediction claim not tied to any
    existing chunk) -- such claims are outside what a single chunk can
    verify and are skipped rather than checked against the wrong context.
    """
    match = re.search(r"month[\s_]*(\d+)", claim_text, re.IGNORECASE)
    if not match:
        return None
    month_num = match.group(1)

    for chunk in retrieved_chunks:
        chunk_month = str(chunk.get("Month", ""))
        if re.search(rf"month[\s_]*{month_num}\b", chunk_month, re.IGNORECASE):
            return chunk["text"]
    return None


def extract_verifiable_claims(answer_text):
    """
    Stricter than decompose_answer_into_claims() -- keeps only lines
    that look like a direct, attributable factual statement (mentions a
    specific month AND a number), dropping narrative/summary sentences
    that describe a TREND rather than stating a single lookup-able fact.

    Trend/summary sentences (e.g. "your HbA1c dipped then rose across
    Month 2 and Month 3") reference MULTIPLE months and inherently
    cannot be verified against any single chunk -- this is a genuine
    scope boundary of claim-level verification, not a bug. Such
    sentences are detected (multiple month mentions, or trend language
    like "changed"/"dipped"/"across") and excluded from single-chunk
    checking rather than incorrectly matched to just one month's chunk.
    """
    TREND_WORDS = ["dipped", "changed", "trend", "across", "consistently",
                   "throughout", "overall", "over the", "compared to"]

    claims = []
    for line in answer_text.split("\n"):
        stripped = line.strip("-* ").strip()
        if not (re.search(r"month[\s_]*\d+", stripped, re.IGNORECASE) and any(ch.isdigit() for ch in stripped)):
            continue

        month_mentions = len(re.findall(r"month[\s_]*\d+", stripped, re.IGNORECASE))
        has_trend_language = any(word in stripped.lower() for word in TREND_WORDS)

        if month_mentions > 1 or has_trend_language:
            continue  # trend/summary claim -- out of scope for single-chunk verification

        claims.append(stripped)
    return claims


def verify_answer_by_matched_chunks(answer_text, retrieved_chunks):
    """
    The refined no-retraining fix: for each verifiable claim, use ONLY
    its own matching single-month chunk as context (not the combined
    multi-month blob), exactly mirroring the training data's shape.
    Claims with no clear month match (e.g. future predictions) are
    reported separately as "not verifiable against retrieved chunks"
    rather than being incorrectly checked against mismatched context.
    """
    claims = extract_verifiable_claims(answer_text)
    results = []
    skipped = []

    for claim in claims:
        matched_context = match_claim_to_chunk(claim, retrieved_chunks)
        if matched_context is None:
            skipped.append(claim)
            continue
        wrapped_claim = wrap_realistic(claim)
        result = predict_faithfulness(matched_context, wrapped_claim)
        results.append({"claim": claim, **result})

    overall_label = "hallucinated" if any(
        r["predicted_label"] == "hallucinated" for r in results
    ) else "faithful"

    return {"overall_label": overall_label, "claim_results": results, "skipped_claims": skipped}


def condense_chunks_for_verification(retrieved_chunks):
    """
    Builds a compact context string for the verifier, keeping only the
    actual biomarker facts per month rather than the full chunk text
    (which repeats "Laboratory Report Summary for Patient X (Female,
    age 53)..." boilerplate once per month, wasting a large share of
    the 512-token budget on repeated demographic text rather than the
    facts that actually matter for a faithfulness check).
    """
    import re

    lines = []
    for chunk in retrieved_chunks:
        text = chunk.get("text", "")
        month = chunk.get("Month", "")
        # Extract just the "Marker: value (Classification: label)" statements
        matches = re.findall(
            r"([A-Z][A-Za-z0-9 \-\(\)]*?):\s*([\d]+\.?[\d]*)\s*(%|mg/dL)?\s*\(Classification:\s*([A-Za-z\- ]+?)\)",
            text
        )
        fact_strs = [f"{m[0].strip()}={m[1]}{m[2] or ''} ({m[3].strip()})" for m in matches]
        lines.append(f"{month}: " + ", ".join(fact_strs))

    return " | ".join(lines)

GENERATION_SAMPLES_PATH = os.path.join("evaluation", "generation_samples.json")


def main():
    if not os.path.exists(GENERATION_SAMPLES_PATH):
        print(f"Could not find {GENERATION_SAMPLES_PATH} -- run phase_g_generation.py first.")
        return

    with open(GENERATION_SAMPLES_PATH, "r") as f:
        samples = json.load(f)

    if not samples:
        print("No saved generation samples found.")
        return

    entry = samples[0]  # the real P032 HbA1c answer
    real_answer = entry["answer"]
    retrieved_chunks = entry["retrieved_chunks"]
    combined_context = " ".join(c["text"] for c in retrieved_chunks)

    print("=" * 70)
    print("TEST 1: The REAL, full, multi-paragraph Claude answer as-is")
    print("=" * 70)
    print(f"Answer length: {len(real_answer)} characters")
    result_full = predict_faithfulness(combined_context, real_answer)
    print(f"Result: {result_full}\n")

    print("=" * 70)
    print("TEST 2: Just the first factual sentence extracted from the answer")
    print("(mimics the short, templated style the verifier was trained on)")
    print("=" * 70)
    # crude extraction: first line that looks like a bullet with a real value
    first_fact_line = None
    for line in real_answer.split("\n"):
        if "%" in line and any(ch.isdigit() for ch in line):
            first_fact_line = line.strip("- *").strip()
            break
    if first_fact_line:
        print(f"Extracted line: \"{first_fact_line}\"")
        result_short = predict_faithfulness(combined_context, first_fact_line)
        print(f"Result: {result_short}\n")
    else:
        print("Could not extract a short fact line automatically.\n")

    print("=" * 70)
    print("TEST 3: Token length check (is truncation happening?)")
    print("=" * 70)
    from transformers import AutoTokenizer
    from phase_i_neural_verifier import MODEL_OUTPUT_DIR
    tokenizer = AutoTokenizer.from_pretrained(MODEL_OUTPUT_DIR)

    context_tokens = len(tokenizer.encode(combined_context))
    answer_tokens = len(tokenizer.encode(real_answer))
    total_tokens = len(tokenizer.encode(combined_context, real_answer))

    print(f"Context alone:      {context_tokens} tokens")
    print(f"Full answer alone:  {answer_tokens} tokens")
    print(f"Combined pair:      {total_tokens} tokens")
    print(f"MAX_LENGTH setting: {MAX_LENGTH} tokens")
    if total_tokens > MAX_LENGTH:
        print(f"TRUNCATION IS HAPPENING -- {total_tokens - MAX_LENGTH} tokens are being cut off.")
        print("This alone could explain the failure -- the model may never see the")
        print("actual answer content if the context eats up the token budget first.")
    else:
        print("No truncation -- the full pair fits within MAX_LENGTH.")

    print("\n" + "=" * 70)
    print("TEST 4: Real answer + CONDENSED context (the actual fix, no retraining)")
    print("=" * 70)
    condensed_context = condense_chunks_for_verification(retrieved_chunks)
    condensed_tokens = len(tokenizer.encode(condensed_context))
    print(f"Condensed context: \"{condensed_context}\"")
    print(f"Condensed context length: {condensed_tokens} tokens (vs {context_tokens} tokens raw)")

    result_condensed = predict_faithfulness(condensed_context, real_answer)
    print(f"Result: {result_condensed}")

    if result_condensed["predicted_label"] == "faithful":
        print("\nFIX CONFIRMED: condensing the context (removing repeated boilerplate)")
        print("resolves the truncation problem WITHOUT needing to retrain the model.")
    else:
        print("\nStill failing even with condensed context -- truncation wasn't the")
        print("full story; trying claim decomposition next...")

    print("\n" + "=" * 70)
    print("TEST 5: Claim decomposition (check each fact separately, no retraining)")
    print("=" * 70)
    decomposition_result = verify_answer_by_decomposition(combined_context, real_answer)
    print(f"Overall verdict: {decomposition_result['overall_label']}\n")
    print("Per-claim results:")
    for r in decomposition_result["claim_results"]:
        print(f"  [{r['predicted_label']:>12}] (faithful={r['faithful_confidence']:.3f}) \"{r['claim']}\"")

    if decomposition_result["overall_label"] == "faithful":
        print("\nFIX CONFIRMED: checking each claim individually (matching the model's")
        print("training distribution) correctly identifies this real answer as faithful,")
        print("WITHOUT any retraining.")
    else:
        flagged = [r for r in decomposition_result["claim_results"] if r["predicted_label"] == "hallucinated"]
        print(f"\n{len(flagged)}/{len(decomposition_result['claim_results'])} individual claims still flagged.")
        print("Decomposition helped narrow down WHICH specific claims are problematic,")
        print("even if it didn't fully resolve every one.")

    print("\n" + "=" * 70)
    print("TEST 6: Claim decomposition + MATCHED single-chunk context (refined fix)")
    print("=" * 70)
    matched_result = verify_answer_by_matched_chunks(real_answer, retrieved_chunks)
    print(f"Overall verdict: {matched_result['overall_label']}\n")
    print("Per-claim results (each checked against ONLY its own matching month's chunk):")
    for r in matched_result["claim_results"]:
        print(f"  [{r['predicted_label']:>12}] (faithful={r['faithful_confidence']:.3f}) \"{r['claim']}\"")
    if matched_result["skipped_claims"]:
        print("\nSkipped (no matching single chunk found, e.g. future predictions):")
        for c in matched_result["skipped_claims"]:
            print(f"  - \"{c}\"")

    if matched_result["overall_label"] == "faithful":
        print("\nFIX CONFIRMED: matching each claim to its OWN single-month chunk")
        print("(exactly mirroring the training data's shape) correctly identifies")
        print("this real answer as faithful, with NO retraining needed.")
    else:
        print("\nStill failing even with matched single-chunk context.")

    print("\n" + "=" * 70)
    print("INTERPRETATION")
    print("=" * 70)
    if result_full["predicted_label"] == "hallucinated" and first_fact_line:
        if result_short["predicted_label"] == "faithful":
            print("CONFIRMED: the verifier correctly identifies faithful content when it's")
            print("short and templated (matching training data), but fails on the same")
            print("factual content when embedded in a longer, real-style answer.")
            print("This points to a train/test distribution mismatch, not a logic bug.")
        else:
            print("Both the full answer AND the short extracted fact scored as hallucinated --")
            print("see TEST 4 above: this is likely because the raw context was too long")
            print("and got truncated, silently dropping later months' data.")


if __name__ == "__main__":
    main()