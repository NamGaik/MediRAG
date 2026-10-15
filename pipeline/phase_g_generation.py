"""
phase_g_generation.py

Phase G for Medi-RAG: LLM Generation (grounded on retrieved chunks)

Takes a patient's question, retrieves the most relevant report chunks
using phase_e_vector_db.py, and asks Claude to answer USING ONLY that
retrieved context. This is the "G" in your pipeline -- turning raw lab
values into a plain-language explanation.

Why the strict "only use given context" prompt:
    This is what makes the system "grounded" rather than a generic
    chatbot. Everything the LLM says should be traceable back to a
    specific retrieved chunk -- if it isn't in the context, the model
    is told to say so rather than guess. This also gives you and the
    rule-based validator (next step) something concrete to check against.

Run this from your MediRAG root folder (same level as embeddings/ and
vector_db/), AFTER phase_e_vector_db.py has already built its index.

Requirements:
    pip install anthropic
    Set your API key first:
        export ANTHROPIC_API_KEY="your-key-here"      (Mac/Linux)
        setx ANTHROPIC_API_KEY "your-key-here"          (Windows)
"""

import os
import json

from phase_ef_vectorDB import retrieve_top_k, load_index
from phase_j_1_trajectory_model import load_patient_sequences, predict_next_visit, FEATURE_COLUMNS

# -----------------------------
# Config
# -----------------------------
# ADJUST HERE if Anthropic releases a newer model you want to switch to.
CLAUDE_MODEL = "claude-sonnet-5"

TOP_K = 5
SYSTEM_PROMPT = """You are a medical report explainer helping a patient understand their lab results.

STRICT RULES:
1. Only use facts that appear in the CONTEXT below. Do not use outside medical knowledge to fill gaps.
2. If the context does not contain enough information to answer the question, say so directly instead of guessing.
3. Every specific number or classification you mention (e.g. HbA1c value, "Diabetic", "Normal") must come from the context, not be invented or estimated.
4. Write in plain, patient-friendly language -- avoid unexplained jargon.
5. Do not give treatment advice, dosing instructions, or diagnoses beyond what the context explicitly states. Recommend the patient discuss results with their doctor.
6. Keep the answer focused and concise -- a few short paragraphs, not an exhaustive report.
7. If a "MODEL-PREDICTED TREND" section is provided, you may reference it, but you MUST clearly label it as a prediction (e.g. "our model predicts..." or "based on your trend, the model estimates...") -- never state a predicted value as if it were an actual measured result. Also mention that this is an estimate, not a certainty, and that real lab testing is needed to confirm it.
8. Rule 1 restricts you to the context ONLY for the patient's specific facts and numbers -- it does NOT restrict general medical education. When asked to explain a general medical concept or term (e.g. "what is LDL cholesterol", "why does high blood sugar matter long-term", "what does HbA1c measure"), you MUST provide that general explanation using your own medical knowledge, clearly introduced with a phrase such as "In general," or "For background,". Do not decline to explain a general concept just because the patient's own report doesn't discuss it -- only decline when the patient asks for a SPECIFIC PERSONAL number, measurement, or diagnosis that is genuinely absent from the context. If a question combines both (e.g. "what is my LDL and what does it mean"), answer the general part using your own knowledge and the specific part using only the context, clearly separating the two.
"""


# -----------------------------
# Prompt construction
# -----------------------------
def build_context_block(retrieved_chunks):
    """
    Turns the list of retrieved chunks into a numbered context block, so
    the LLM (and later, your rule-based validator and neural verifier)
    can be pointed back to exactly which chunk backs which claim.
    """
    lines = []
    for i, chunk in enumerate(retrieved_chunks, start=1):
        lines.append(
            f"[Chunk {i}] Patient {chunk['Patient_ID']}, {chunk['Month']} "
            f"(Status: {chunk['Overall_Status']}, similarity: {chunk['similarity_score']}):\n"
            f"{chunk['text']}\n"
        )
    return "\n".join(lines)


# -----------------------------
# Trajectory prediction integration
# -----------------------------
_patient_sequences_cache = None


def get_trajectory_prediction(patient_filter, history_override=None):
    """
    Looks up the given patient's real history and runs it through the
    trained trajectory model to predict their likely next-visit values.
    Returns None if no patient_filter was given, the patient isn't
    found, or they have no recorded months -- in any of those cases,
    generation proceeds without a trend prediction rather than failing.

    Uses the LAST up to 2 months of history as input, matching how the
    model was trained (see phase_j_trajectory_model.py's one-step-ahead
    pairs) -- this generalizes naturally to patients with exactly 2 or
    3+ months on record.

    history_override (optional):
        Pass a patient's CURRENT list of visit dicts directly, bypassing
        the internal cache below entirely. Use this when the caller
        maintains its own live, always-current history (e.g. a backend
        that just accepted a new report upload) -- without this, the
        internal cache is loaded once and never refreshed, so it would
        silently miss any newly uploaded visits.
    """
    global _patient_sequences_cache

    if not patient_filter:
        return None

    if history_override is not None:
        patient_history = history_override
    else:
        if _patient_sequences_cache is None:
            _patient_sequences_cache = load_patient_sequences()
        patient_history = _patient_sequences_cache.get(patient_filter)

    if not patient_history:
        return None

    # Filter out INCOMPLETE visits (missing one or more biomarker values --
    # e.g. from a partial/failed OCR extraction) before picking the last 2.
    # Feeding a visit with a missing value into the model can produce a
    # NaN ("Not a Number") prediction, which then crashes the API response
    # when trying to convert it to JSON. Skipping incomplete visits here
    # means trend prediction always uses genuinely complete data, while
    # the incomplete visit still correctly remains visible in History.
    required_fields = ["HbA1c(%)", "FBS (mg/dL)", "PPBS (mg/dL)"]
    complete_history = [
        v for v in patient_history
        if all(v.get(f) is not None for f in required_fields)
    ]

    if len(complete_history) < 1:
        return None  # no complete visits available to predict from

    recent_history = complete_history[-2:]  # last up to 2 COMPLETE months, matching training

    try:
        prediction = predict_next_visit(recent_history)
    except FileNotFoundError:
        # Trajectory model hasn't been trained yet -- proceed without it
        # rather than crashing generation.
        return None

    # Safety net: NaN ("Not a Number") cannot be converted to JSON and
    # will crash the entire API response if it ever slips through. This
    # check guarantees that never happens again, regardless of cause.
    for key, value in prediction.items():
        if isinstance(value, float) and value != value:  # NaN is the only value where x != x
            print(f"[WARNING] Trajectory prediction produced NaN for '{key}' -- suppressing trend prediction for this request.")
            return None

    return prediction


def build_trajectory_block(prediction):
    """
    Formats a trajectory prediction as a clearly-labeled section for the
    prompt, so it's visually and textually distinct from the real
    retrieved report chunks above it.
    """
    if prediction is None:
        return ""

    return f"""

MODEL-PREDICTED TREND (this is an ESTIMATE from a trained forecasting model, NOT a measured lab result):
- Predicted next HbA1c: {prediction['predicted_HbA1c']}%
- Predicted next Fasting Blood Sugar: {prediction['predicted_FBS']} mg/dL
- Predicted next Post-Prandial Blood Sugar: {prediction['predicted_PPBS']} mg/dL
- Predicted next risk category: {prediction['predicted_status']}
"""


def build_user_message(query, context_block, trajectory_block=""):
    return f"""CONTEXT:
{context_block}
{trajectory_block}
PATIENT QUESTION:
{query}

Answer the patient's question using only the CONTEXT above. If a MODEL-PREDICTED TREND section is present and relevant to the question, you may reference it, clearly labeled as a prediction."""


# -----------------------------
# Generation
# -----------------------------
def generate_explanation(query, k=TOP_K, index=None, metadata=None, patient_filter=None, extra_context=None, override_chunks=None, history_override=None):
    """
    Full Phase F -> G flow in one call:
        query -> retrieve top-k chunks -> build grounded prompt -> Claude -> answer

    patient_filter (optional):
        Pass a Patient_ID string (e.g. "P032") when the question is about
        one specific patient.

    extra_context (optional):
        Additional grounding text not already in the vector index.

    override_chunks (optional):
        Pass a pre-built list of chunk dicts (same shape retrieve_top_k
        returns) to use INSTEAD of FAISS retrieval entirely. This is for
        callers that maintain their own authoritative, always-current
        record of a patient's history (e.g. after a live report upload
        that hasn't been re-embedded into the index yet) -- using
        override_chunks guarantees the answer reflects the real current
        data rather than a stale, pre-built index.

    Returns a dict with the answer text AND the retrieved chunks, so the
    next step (rule-based validation / neural verifier) can check the
    answer against the exact same context that produced it.
    """
    import anthropic

    if override_chunks is not None:
        retrieved_chunks = override_chunks
    else:
        if index is None or metadata is None:
            index, metadata = load_index()
        retrieved_chunks = retrieve_top_k(
            query, k=k, index=index, metadata=metadata, patient_filter=patient_filter
        )

    if not retrieved_chunks and not extra_context:
        return {
            "query": query,
            "answer": "I couldn't find any relevant report information to answer this question.",
            "retrieved_chunks": [],
        }

    context_block = build_context_block(retrieved_chunks) if retrieved_chunks else ""
    if extra_context:
        context_block += f"\n\n[Newly uploaded report, not yet in patient history]:\n{extra_context}"

    trajectory_prediction = get_trajectory_prediction(patient_filter, history_override=history_override)
    trajectory_block = build_trajectory_block(trajectory_prediction)

    user_message = build_user_message(query, context_block, trajectory_block)

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from environment

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=800,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": user_message}
        ],
    )

    answer_text = "".join(
        block.text for block in response.content if block.type == "text"
    )

    return {
        "query": query,
        "answer": answer_text,
        "retrieved_chunks": retrieved_chunks,
        "trajectory_prediction": trajectory_prediction,
    }


# -----------------------------
# Main
# -----------------------------
def main():
    index, metadata = load_index()

    # ADJUST HERE -- swap these for real queries once evaluation starts,
    # e.g. loop over Evaluation_Query_Dataset3.xlsx
    # Each entry is (query_text, patient_filter). Use None for patient_filter
    # on general questions not tied to one person.
    test_queries = [
        ("How has my HbA1c changed across visits?", "P032"),
        ("What does my latest fasting blood sugar result mean?", "P032"),
        ("What is my HbA1c likely to be at my next visit?", "P032"),
    ]

    results = []
    for q, patient_filter in test_queries:
        print(f"\nQuery: {q}  (patient_filter={patient_filter})")
        result = generate_explanation(q, index=index, metadata=metadata, patient_filter=patient_filter)
        print(f"Answer:\n{result['answer']}\n")
        print(f"Grounded in {len(result['retrieved_chunks'])} chunks:")
        for c in result["retrieved_chunks"]:
            print(f"  - {c['Patient_ID']} / {c['Month']} (score={c['similarity_score']})")
        if result["trajectory_prediction"]:
            print(f"Trajectory prediction used: {result['trajectory_prediction']}")
        results.append(result)

    # Save so the rule-based validator (next step) can run against these
    # without re-calling the API every time
    os.makedirs("evaluation", exist_ok=True)
    out_path = os.path.join("evaluation", "generation_samples.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved generation samples -> {out_path}")

    print("\nPhase G complete. Output is ready for the rule-based validation layer.")


if __name__ == "__main__":
    main()