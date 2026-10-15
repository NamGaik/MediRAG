"""
backend/main.py

Phase M for Medi-RAG: FastAPI Backend (v2 -- proper signup/login)

Wraps your existing pipeline as REST endpoints, with a real (though
still demo-grade) auth flow:
    - Existing patients (P001-P050): log in with their ID + a shared
      demo password.
    - New patients: sign up (name, age, gender, password) and receive
      a new ID (U-001, U-002, ...), kept in a SEPARATE store from your
      original 50 -- so your original dataset is never mutated, and the
      doctor's patient list clearly shows "Original Cohort" vs "Newly
      Registered" as two distinct groups.
    - Uploading a report always applies to whoever is CURRENTLY LOGGED
      IN -- there's no "upload on behalf of a random other patient"
      flow, since that never made sense. A new patient's first upload
      becomes their Month 1 record; an existing patient's upload
      becomes a genuine new month, permanently appended to their real
      history (not just held in temporary chat memory like the
      previous version).

IMPORTANT -- STUDENT PROJECT AUTH, NOT PRODUCTION SECURITY:
    Passwords are stored in plain text, in memory, and reset every time
    the backend restarts. The "shared demo password" for original
    patients exists only because the dataset never had real per-patient
    passwords to begin with. State this plainly if ever asked whether
    this is deployment-ready -- it is not, by design, for a demo/thesis
    project.

Run with:
    uvicorn backend.main:app --reload

Requirements:
    pip install fastapi uvicorn python-dotenv pdfplumber pytesseract pillow
"""

import os
import sys
import re
from typing import Optional

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# -----------------------------
# .env loading
# -----------------------------
try:
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    load_dotenv(env_path)
    print(f"[STARTUP] .env file exists: {os.path.exists(env_path)}")
except ImportError:
    print("Note: python-dotenv not installed -- run: pip install python-dotenv")

if os.environ.get("ANTHROPIC_API_KEY"):
    print("[STARTUP] ANTHROPIC_API_KEY is SET.")
else:
    print("[STARTUP] *** ANTHROPIC_API_KEY IS NOT SET *** -- /query will fail.")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from phase_ef_vectorDB import load_index, retrieve_top_k
from phase_g_generation import generate_explanation
from phase_j_trajectory_model import load_patient_sequences, predict_next_visit
from phase_i_neural_verifier import verify_answer_by_matched_chunks

# -----------------------------
# App setup
# -----------------------------
app = FastAPI(title="MediRAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEMO_PATIENT_PASSWORD = "diabetes123"   # shared demo password for P001-P050 -- see module docstring
DEMO_DOCTOR_PASSWORD = "doctor123"

# -----------------------------
# Persistence -- saves the full patient state to disk after every change,
# so uploads and signups SURVIVE backend restarts. Without this, every
# restart reloaded fresh from the original Excel file and silently
# discarded anything uploaded during the previous session.
# -----------------------------
import json

SNAPSHOT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "live_patient_snapshot.json")


def save_snapshot():
    os.makedirs(os.path.dirname(SNAPSHOT_PATH), exist_ok=True)
    with open(SNAPSHOT_PATH, "w") as f:
        json.dump({
            "patient_sequences": _patient_sequences,
            "new_patients": _new_patients,
            "next_new_patient_number": _next_new_patient_number,
        }, f, indent=2)


def load_snapshot():
    if not os.path.exists(SNAPSHOT_PATH):
        return None
    with open(SNAPSHOT_PATH, "r") as f:
        return json.load(f)


print("Loading vector index...")
_index, _metadata = load_index()

_snapshot = load_snapshot()
if _snapshot:
    print(f"[STARTUP] Found saved snapshot at {SNAPSHOT_PATH} -- loading it "
          f"(includes any previous uploads/signups) instead of the original Excel file.")
    _patient_sequences = _snapshot["patient_sequences"]
    _new_patients = _snapshot["new_patients"]
    _next_new_patient_number = _snapshot["next_new_patient_number"]
else:
    print("[STARTUP] No saved snapshot found -- loading original patient sequences from Excel "
          "(this is expected on the very first run).")
    _patient_sequences = load_patient_sequences()
    _new_patients = {}
    _next_new_patient_number = 1

print("Backend ready.")


# -----------------------------
# Unified patient record access -- treats original and newly-registered
# patients the same way everywhere else in the API, so every other
# endpoint doesn't need to know which store a given ID lives in.
# -----------------------------
def patient_exists(patient_id):
    return patient_id in _patient_sequences or patient_id in _new_patients


def get_history(patient_id):
    if patient_id in _patient_sequences:
        return _patient_sequences[patient_id]
    if patient_id in _new_patients:
        return _new_patients[patient_id]["history"]
    return None


def append_visit(patient_id, visit_record):
    """Permanently adds a new visit (month) to a patient's real history."""
    if patient_id in _patient_sequences:
        _patient_sequences[patient_id].append(visit_record)
    elif patient_id in _new_patients:
        _new_patients[patient_id]["history"].append(visit_record)


# -----------------------------
# Request models
# -----------------------------
class LoginRequest(BaseModel):
    role: str                          # "doctor" or "patient"
    patient_id: Optional[str] = None
    password: Optional[str] = None


class SignupRequest(BaseModel):
    name: str
    age: int
    gender: str
    password: str


class QueryRequest(BaseModel):
    patient_id: str
    query_text: str
    language: str = "English"


# -----------------------------
# Auth
# -----------------------------
@app.post("/auth/login")
def login(req: LoginRequest):
    if req.role == "doctor":
        if req.password != DEMO_DOCTOR_PASSWORD:
            raise HTTPException(status_code=401, detail="Incorrect doctor password.")
        return {"role": "doctor"}

    if req.role == "patient":
        if not req.patient_id:
            raise HTTPException(status_code=400, detail="Patient ID is required.")

        if req.patient_id in _patient_sequences:
            if req.password != DEMO_PATIENT_PASSWORD:
                raise HTTPException(status_code=401, detail="Incorrect password.")
            return {"role": "patient", "patient_id": req.patient_id, "is_new_patient": False}

        if req.patient_id in _new_patients:
            if req.password != _new_patients[req.patient_id]["password"]:
                raise HTTPException(status_code=401, detail="Incorrect password.")
            return {"role": "patient", "patient_id": req.patient_id, "is_new_patient": True}

        raise HTTPException(
            status_code=404,
            detail=f"No account found for {req.patient_id}. If you're a new patient, use Sign Up instead."
        )

    raise HTTPException(status_code=400, detail="role must be 'doctor' or 'patient'")


@app.post("/auth/signup")
def signup(req: SignupRequest):
    """
    Registers a brand-new patient (not one of the original P001-P050)
    and assigns them a new ID. They start with NO history -- their
    first uploaded report becomes their Month 1 record.
    """
    global _next_new_patient_number

    new_id = f"U-{_next_new_patient_number:03d}"
    _next_new_patient_number += 1

    _new_patients[new_id] = {
        "name": req.name,
        "age": req.age,
        "gender": req.gender,
        "password": req.password,
        "history": [],
    }
    save_snapshot()

    return {"role": "patient", "patient_id": new_id, "is_new_patient": True}


# -----------------------------
# Doctor endpoints
# -----------------------------
@app.get("/patients")
def list_patients():
    """
    Doctor dashboard: returns TWO separate groups so the ledger can
    clearly distinguish the original synthetic cohort from patients
    who signed up and were onboarded via report upload.
    """
    original = []
    for patient_id, months in _patient_sequences.items():
        if not months:
            continue
        latest = months[-1]
        original.append({
            "patient_id": patient_id,
            "latest_hba1c": latest["HbA1c(%)"],
            "latest_status": latest["status"],
            "months_on_record": len(months),
        })

    newly_registered = []
    for patient_id, record in _new_patients.items():
        months = record["history"]
        entry = {
            "patient_id": patient_id,
            "name": record["name"],
            "months_on_record": len(months),
        }
        if months:
            entry["latest_hba1c"] = months[-1]["HbA1c(%)"]
            entry["latest_status"] = months[-1]["status"]
        else:
            entry["latest_hba1c"] = None
            entry["latest_status"] = "No reports yet"
        newly_registered.append(entry)

    return {"original_patients": original, "newly_registered_patients": newly_registered}


# -----------------------------
# Patient data endpoints
# -----------------------------
@app.get("/patients/{patient_id}/history")
def get_patient_history(patient_id: str):
    if not patient_exists(patient_id):
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")
    return {"patient_id": patient_id, "history": get_history(patient_id)}


@app.get("/patients/{patient_id}/trend")
def get_patient_trend(patient_id: str):
    if not patient_exists(patient_id):
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")

    history = get_history(patient_id)
    if len(history) < 1:
        raise HTTPException(
            status_code=400,
            detail="No reports on record yet -- upload a report first to see a trend."
        )
    if len(history) < 2:
        raise HTTPException(
            status_code=400,
            detail="Need at least 2 recorded visits to forecast a trend -- upload another report."
        )

    recent_history = history[-2:]
    prediction = predict_next_visit(recent_history)
    return {"patient_id": patient_id, "history": history, "prediction": prediction}


# -----------------------------
# Report upload -- OCR extraction + PERMANENT history update
# -----------------------------


def normalize_marker_key(marker_text):
    """
    Robust marker matching using substring checks rather than an exact
    dictionary lookup -- exact matching was fragile and silently failed
    on real-world text variations (extra spacing, different wording,
    plain .txt formatting differing slightly from the PDF template),
    which is why a .txt upload could show "extracted the data" in the
    raw text/structured-values preview while History still showed
    blank values: the marker string just didn't match any dict key
    EXACTLY, even though it clearly meant the same biomarker.
    """
    m = marker_text.strip().lower()
    if "hba1c" in m:
        return "HbA1c(%)"
    if "fasting" in m or m == "fbs" or "(fbs)" in m:
        return "FBS (mg/dL)"
    if "post-prandial" in m or "postprandial" in m or "(ppbs)" in m or m == "ppbs":
        return "PPBS (mg/dL)"
    return None


def extract_text_from_upload(filename, content_bytes):
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""

    if ext == "txt":
        return content_bytes.decode("utf-8", errors="ignore")

    if ext == "pdf":
        import io
        import pdfplumber
        text_parts = []
        with pdfplumber.open(io.BytesIO(content_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        extracted = "\n".join(text_parts).strip()
        if not extracted:
            raise HTTPException(
                status_code=422,
                detail="No text could be extracted -- this may be a scanned image-only PDF. Try JPG/PNG instead."
            )
        return extracted

    if ext in ("jpg", "jpeg", "png"):
        import io
        import pytesseract
        from PIL import Image, ImageOps

        default_windows_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        if os.name == "nt" and os.path.exists(default_windows_path):
            pytesseract.pytesseract.tesseract_cmd = default_windows_path

        try:
            original_image = Image.open(io.BytesIO(content_bytes)).convert("L")  # grayscale baseline

            # Build several candidate versions of the image -- aggressive
            # preprocessing (upscaling + hard black/white thresholding)
            # helps genuinely degraded/blurry scans, but can actually HURT
            # an already-clean, high-quality image by destroying fine
            # table gridlines and thin text. Rather than guess which
            # applies, try multiple levels and keep whichever combination
            # (image version + PSM mode) finds the most real biomarkers.
            candidate_images = {"raw_grayscale": original_image}

            light = ImageOps.autocontrast(original_image)
            candidate_images["light_contrast_only"] = light

            aggressive = light
            if aggressive.width < 1500:
                scale = 1500 / aggressive.width
                aggressive = aggressive.resize(
                    (int(aggressive.width * scale), int(aggressive.height * scale)), Image.LANCZOS
                )
            aggressive = aggressive.point(lambda p: 255 if p > 150 else 0)
            candidate_images["aggressive_binarized"] = aggressive

            candidate_modes = ["--psm 6", "--psm 4", "--psm 11"]

            best_text = ""
            best_match_count = -1
            best_combo = None

            for image_label, candidate_image in candidate_images.items():
                for mode in candidate_modes:
                    candidate_text = pytesseract.image_to_string(candidate_image, config=mode).strip()
                    match_count = sum(
                        1 for name_pattern in KNOWN_BIOMARKERS.values()
                        if re.search(
                            rf"{name_pattern}\s*[:\|]\s*\|?\s*[\d]+\.?\d*", candidate_text, re.IGNORECASE
                        )
                    )
                    if match_count > best_match_count:
                        best_match_count = match_count
                        best_text = candidate_text
                        best_combo = (image_label, mode)

            print(f"[OCR] Best result from {best_combo}, found {best_match_count} biomarkers")
            extracted = best_text
        except pytesseract.TesseractNotFoundError:
            raise HTTPException(
                status_code=500,
                detail=(
                    "Tesseract OCR engine is not installed or not found on this computer. "
                    "Download and install it from: "
                    "https://github.com/UB-Mannheim/tesseract/wiki (Windows installer), "
                    "then restart the backend."
                )
            )

        if not extracted:
            raise HTTPException(status_code=422, detail="No readable text found in this image.")
        return extracted

    raise HTTPException(status_code=400, detail=f"Unsupported file type: .{ext}. Use PDF, JPG, PNG, or TXT.")


KNOWN_BIOMARKERS = {
    "HbA1c": r"HbA1c",
    "FBS": r"(?:Fasting Blood Sugar\s*\(FBS\)|Fasting Blood Sugar|FBS)",
    "PPBS": r"(?:Post-Prandial Blood Sugar\s*\(PPBS\)|Post-Prandial Blood Sugar|PPBS)",
    "LDL": r"LDL(?:\s*Cholesterol)?",
    "HDL": r"HDL(?:\s*Cholesterol)?",
    "Triglycerides": r"Triglycerides",
}


def extract_structured_values(text):
    """
    Extracts known biomarker values from OCR'd/pasted text, supporting
    TWO different real-world formats seen across your reports:

        Colon format (used by the synthetic demo PDF reports):
            "HbA1c: 7.4% (Classification: Diabetic)"

        Pipe/table format (used by your original real report images):
            "Triglycerides | 187.0 | mg/dL"

    Restricted to a whitelist of KNOWN_BIOMARKERS rather than a generic
    "any label: number" pattern -- the generic version was accidentally
    matching unrelated fields like "Age: 53.0" as if it were a lab value.
    """
    results = []

    for canonical_name, name_pattern in KNOWN_BIOMARKERS.items():
        # Colon format: "Marker: 7.4% (Classification: Label)"
        colon_match = re.search(
            rf"{name_pattern}\s*:\s*([\d]+\.?\d*)\s*(%|mg/dL)?\s*(?:\(Classification:\s*([A-Za-z\- ]+?)\))?",
            text, re.IGNORECASE
        )
        if colon_match:
            results.append({
                "marker": canonical_name,
                "value": colon_match.group(1),
                "unit": colon_match.group(2) or "",
                "label": colon_match.group(3).strip() if colon_match.group(3) else None,
            })
            continue

        # Pipe/table format: "Marker | 187.0 | mg/dL"
        pipe_match = re.search(
            rf"{name_pattern}\s*\|\s*([\d]+\.?\d*)\s*\|?\s*(%|mg/dL)?",
            text, re.IGNORECASE
        )
        if pipe_match:
            results.append({
                "marker": canonical_name,
                "value": pipe_match.group(1),
                "unit": pipe_match.group(2) or "",
                "label": None,
            })

    return results


def build_visit_record(structured_values, text):
    """
    Converts extracted values into the same shape as the rest of the
    system's history records, so a new upload is indistinguishable
    from an originally-recorded visit everywhere else in the app
    (History, Trends, chat retrieval all just see a normal visit).
    Fields not found default to None rather than a fabricated number.
    """
    record = {"HbA1c(%)": None, "FBS (mg/dL)": None, "PPBS (mg/dL)": None, "status": "Unknown"}

    for v in structured_values:
        key = normalize_marker_key(v["marker"])
        if key:
            try:
                record[key] = float(v["value"])
            except ValueError:
                pass

    status_match = re.search(r"Overall Glycemic Status:\s*([A-Za-z\- ]+)", text, re.IGNORECASE)
    if status_match:
        record["status"] = status_match.group(1).strip()
    elif record["HbA1c(%)"] is not None:
        h = record["HbA1c(%)"]
        record["status"] = "Diabetic" if h >= 6.5 else ("Prediabetic" if h >= 5.7 else "Normal")

    return record


# -----------------------------
# Uploaded Reports storage -- keeps the ORIGINAL uploaded file (not just
# extracted text), so a doctor can open and independently verify what
# was actually submitted, rather than only trusting the extraction.
# -----------------------------
UPLOADED_FILES_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "uploaded_reports")
os.makedirs(UPLOADED_FILES_DIR, exist_ok=True)

# Registry of uploaded files per patient, persisted alongside the patient snapshot.
_uploaded_files_registry = {}  # patient_id -> [{"filename":, "stored_path":, "month":, "uploaded_at":}]


def save_uploaded_file(patient_id, filename, content_bytes, month_number):
    """
    Saves the raw uploaded file to disk under a patient-specific folder,
    and records it in the registry so it can be listed and served later.
    Text pasted directly (not a real file) is NOT saved here -- there is
    no original document to preserve in that case.
    """
    import datetime
    patient_dir = os.path.join(UPLOADED_FILES_DIR, patient_id)
    os.makedirs(patient_dir, exist_ok=True)

    safe_filename = f"month{month_number}_{filename}".replace(" ", "_")
    stored_path = os.path.join(patient_dir, safe_filename)
    with open(stored_path, "wb") as f:
        f.write(content_bytes)

    entry = {
        "filename": filename,
        "stored_filename": safe_filename,
        "month": month_number,
        "uploaded_at": datetime.datetime.now().isoformat(),
    }
    _uploaded_files_registry.setdefault(patient_id, []).append(entry)
    save_uploaded_files_registry()


UPLOADED_FILES_REGISTRY_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "uploaded_files_registry.json")


def save_uploaded_files_registry():
    with open(UPLOADED_FILES_REGISTRY_PATH, "w") as f:
        json.dump(_uploaded_files_registry, f, indent=2)


def load_uploaded_files_registry():
    if os.path.exists(UPLOADED_FILES_REGISTRY_PATH):
        with open(UPLOADED_FILES_REGISTRY_PATH, "r") as f:
            return json.load(f)
    return {}


_uploaded_files_registry = load_uploaded_files_registry()


@app.post("/patients/{patient_id}/upload")
async def upload_report(patient_id: str, file: UploadFile = File(...)):
    """
    Extracts a report's values and PERMANENTLY appends them as a new
    visit to the logged-in patient's own history. This always applies
    to whoever is currently logged in -- there is no "choose a
    different patient" option, since uploading on behalf of a random
    other patient never made sense.

    Also saves the ORIGINAL uploaded file to disk (Uploaded Reports
    feature), so a doctor can open and independently verify the source
    document -- not just trust the automatically extracted values.
    """
    if not patient_exists(patient_id):
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")

    content_bytes = await file.read()
    extracted_text = extract_text_from_upload(file.filename, content_bytes)
    structured_values = extract_structured_values(extracted_text)
    visit_record = build_visit_record(structured_values, extracted_text)

    append_visit(patient_id, visit_record)
    new_month_number = len(get_history(patient_id))

    save_uploaded_file(patient_id, file.filename, content_bytes, new_month_number)
    save_snapshot()

    return {
        "patient_id": patient_id,
        "filename": file.filename,
        "extracted_text": extracted_text,
        "structured_values": structured_values,
        "saved_as_month": new_month_number,
        "message": f"Saved as Month {new_month_number} in your history.",
    }


class TextUploadRequest(BaseModel):
    text: str


@app.post("/patients/{patient_id}/upload-text")
def upload_report_text(patient_id: str, req: TextUploadRequest):
    """
    Same as /upload, but for text pasted directly into a text box instead
    of a file -- useful when a report is already in text form, or for
    quick testing without needing to create a file first.
    """
    if not patient_exists(patient_id):
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Pasted text is empty.")

    structured_values = extract_structured_values(req.text)
    visit_record = build_visit_record(structured_values, req.text)

    append_visit(patient_id, visit_record)
    save_snapshot()
    new_month_number = len(get_history(patient_id))

    return {
        "patient_id": patient_id,
        "filename": "Pasted text",
        "extracted_text": req.text,
        "structured_values": structured_values,
        "saved_as_month": new_month_number,
        "message": f"Saved as Month {new_month_number} in your history.",
    }


@app.get("/patients/{patient_id}/reports")
def list_uploaded_reports(patient_id: str):
    """
    Lists every ORIGINAL file uploaded for this patient (PDF/image),
    for the Uploaded Reports view -- lets a doctor independently open
    and verify the source document, not just trust extracted values.
    Pasted-text submissions have no original file and are not listed
    here (there is nothing to view -- the extracted text itself is
    already fully visible in History).
    """
    if not patient_exists(patient_id):
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")
    return {"patient_id": patient_id, "reports": _uploaded_files_registry.get(patient_id, [])}


@app.get("/patients/{patient_id}/reports/{stored_filename}")
def get_uploaded_report_file(patient_id: str, stored_filename: str):
    """Serves the actual original uploaded file for viewing/download."""
    from fastapi.responses import FileResponse

    if not patient_exists(patient_id):
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")

    file_path = os.path.join(UPLOADED_FILES_DIR, patient_id, stored_filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)


# -----------------------------
# Chat / Ask Questions
# -----------------------------
def classify_marker(marker, value):
    """
    Simple ADA-threshold classification for building live chunk text.
    Standard thresholds, consistent with what's used project-wide:
        HbA1c:  <5.7 Normal | 5.7-6.4 Prediabetic | >=6.5 Diabetic
        FBS:    <100 Normal | 100-125 Prediabetic | >=126 Diabetic
        PPBS:   <140 Normal | 140-199 Prediabetic | >=200 Diabetic
    """
    if value is None:
        return "Unknown"
    thresholds = {"HbA1c": (5.7, 6.5), "FBS": (100, 126), "PPBS": (140, 200)}
    lo, hi = thresholds.get(marker, (0, 0))
    if value >= hi:
        return "Diabetic"
    if value >= lo:
        return "Prediabetic"
    return "Normal"


def build_chunks_from_history(patient_id, history):
    """
    Builds retrieval-equivalent chunks directly from a patient's CURRENT
    live history, rather than relying on the FAISS index -- which was
    built once at startup and never updated. This guarantees any newly
    uploaded visit is immediately usable in chat, without needing to
    re-embed/re-index anything. Text format matches the original chunk
    style so the rule validator and verifier's parsing logic (which look
    for "Marker: value (Classification: label)") work identically.
    """
    chunks = []
    for i, visit in enumerate(history):
        month_label = f"Month_{i + 1}"
        hba1c = visit.get("HbA1c(%)")
        fbs = visit.get("FBS (mg/dL)")
        ppbs = visit.get("PPBS (mg/dL)")

        lines = [f"Laboratory Report Summary for Patient {patient_id} -- {month_label}."]
        if hba1c is not None:
            lines.append(f"HbA1c: {hba1c}% (Classification: {classify_marker('HbA1c', hba1c)}).")
        if fbs is not None:
            lines.append(f"Fasting Blood Sugar (FBS): {fbs} mg/dL (Classification: {classify_marker('FBS', fbs)}).")
        if ppbs is not None:
            lines.append(f"Post-Prandial Blood Sugar (PPBS): {ppbs} mg/dL (Classification: {classify_marker('PPBS', ppbs)}).")

        chunks.append({
            "Patient_ID": patient_id,
            "Month": month_label,
            "Overall_Status": visit.get("status", "Unknown"),
            "text": " ".join(lines),
            "similarity_score": 1.0,  # authoritative record, not a semantic search result
        })
    return chunks


@app.post("/query")
def query(req: QueryRequest):
    if not patient_exists(req.patient_id):
        raise HTTPException(status_code=404, detail=f"Patient {req.patient_id} not found")

    # Always build chunks from the patient's LIVE, current history --
    # this works identically for original and newly-registered patients,
    # and immediately reflects any report uploaded this session (unlike
    # FAISS retrieval, which only knows about the original pre-built index).
    history = get_history(req.patient_id)
    live_chunks = build_chunks_from_history(req.patient_id, history)

    # Multilingual support: instruct the model to respond in the chosen
    # language. This is appended to the query text (not the system prompt)
    # for simplicity -- safe here because retrieval is fully bypassed via
    # override_chunks, so this has no effect on finding the right chunks.
    query_text = req.query_text
    if req.language and req.language.lower() != "english":
        query_text = f"{req.query_text}\n\n(Please respond in {req.language}.)"

    result = generate_explanation(
        query_text,
        override_chunks=live_chunks,
        patient_filter=req.patient_id,
        history_override=history,
    )

    verifier_summary = None
    if result["retrieved_chunks"]:
        verifier_result = verify_answer_by_matched_chunks(result["answer"], result["retrieved_chunks"])
        verifier_summary = {
            "label": verifier_result["overall_label"],
            "claims_checked": len(verifier_result["claim_results"]),
            "claims_skipped": len(verifier_result["skipped_claims"]),
        }

    return {
        "query": req.query_text,
        "answer": result["answer"],
        "grounded_in": [
            {"patient_id": c["Patient_ID"], "month": c["Month"], "score": c["similarity_score"]}
            for c in result["retrieved_chunks"]
        ],
        "trajectory_prediction": result.get("trajectory_prediction"),
        "verifier": verifier_summary,
    }


@app.get("/")
def root():
    return {"status": "MediRAG API is running", "docs": "/docs"}


# -----------------------------
# Treatment approaches -- general educational information
# -----------------------------
# NOTE: This content is STATIC and curated, not AI-generated -- deliberately,
# since freeform AI-generated treatment advice carries real risk of being
# wrong or unsafe. Every entry is general educational information only,
# not personalized advice, and explicitly says so.
TREATMENT_APPROACHES = {
    "lifestyle": {
        "title": "Lifestyle & Dietary Management",
        "summary": "The most evidence-backed foundation for T2DM management, recommended by ADA/WHO guidelines alongside any other treatment.",
        "points": [
            "Regular physical activity (150+ minutes/week of moderate exercise is a common general guideline)",
            "Consistent meal timing and portion control to manage blood glucose spikes",
            "Reducing refined carbohydrates and added sugars",
            "Weight management, where relevant, in consultation with a doctor",
            "Regular sleep schedule -- poor sleep is linked to worse glycemic control",
        ],
    },
    "ayurvedic": {
        "title": "Ayurvedic Approaches",
        "summary": "A traditional Indian system of medicine that includes dietary guidelines, herbs, and lifestyle practices for metabolic health.",
        "points": [
            "Commonly discussed herbs include bitter gourd (karela), fenugreek (methi), and gudmar",
            "Emphasizes dietary routine (dinacharya) and individualized constitution (dosha) assessment",
            "Scientific evidence varies by specific herb/practice -- quality and rigor of studies differ widely",
            "Should be discussed with both an Ayurvedic practitioner AND your treating physician, since some herbs can interact with diabetes medication",
        ],
    },
    "homeopathy": {
        "title": "Homeopathy",
        "summary": "A system of alternative medicine based on highly diluted substances; used by some patients alongside conventional care.",
        "points": [
            "Practitioners may recommend remedies based on individual symptom patterns, not standardized by lab values",
            "Scientific evidence for homeopathy's effectiveness in diabetes management is limited and contested in mainstream medical literature",
            "Should never replace insulin or prescribed medication without explicit medical guidance",
            "Discuss any homeopathic treatment with your treating physician before starting",
        ],
    },
    "herbal_supplements": {
        "title": "Herbal & Dietary Supplements",
        "summary": "Various plant-based and nutritional supplements are marketed for blood sugar support.",
        "points": [
            "Commonly discussed options include cinnamon, chromium, alpha-lipoic acid, and berberine",
            "Evidence quality varies significantly between supplements -- some have modest supporting research, others very little",
            "Supplements are not regulated as strictly as medications -- purity and dosing can vary between products",
            "Can interact with prescribed diabetes medication (e.g., increasing hypoglycemia risk) -- always inform your doctor before starting any supplement",
        ],
    },
    "mind_body": {
        "title": "Mind-Body Alternative Therapies",
        "summary": "Practices addressing the connection between mental/emotional state and physical health, often used to support stress management.",
        "points": [
            "Includes yoga, meditation, tai chi, and structured breathing practices",
            "Chronic stress can affect blood glucose levels via cortisol -- stress management is a reasonable complementary practice",
            "Generally low-risk and can be combined safely with conventional treatment",
            "Best used as a complement to, not a replacement for, medical management",
        ],
    },
}


@app.get("/treatments")
def list_treatment_categories():
    """Returns all treatment categories with their summary, for a selector UI."""
    return {
        "categories": [
            {"key": key, "title": v["title"], "summary": v["summary"]}
            for key, v in TREATMENT_APPROACHES.items()
        ]
    }


@app.get("/treatments/{category_key}")
def get_treatment_detail(category_key: str):
    """Returns full detail for one treatment category."""
    if category_key not in TREATMENT_APPROACHES:
        raise HTTPException(status_code=404, detail=f"Unknown category: {category_key}")
    return TREATMENT_APPROACHES[category_key]