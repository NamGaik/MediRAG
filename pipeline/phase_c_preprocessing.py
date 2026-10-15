"""
phase_c_preprocessing.py

Phase C for Medi-RAG: Preprocessing

Takes the structured JSON reports produced by Phase B (OCR extraction)
and prepares them for embedding (Phase D). Per the project brief, this
involves four tasks:

1. Noise removal       -- drop/flag incomplete or invalid records
2. Unit normalization   -- ensure consistent units (mg/dL, %), with
                            conversion support for alternate units
                            (e.g. mmol/L glucose, mmol/mol HbA1c)
3. Clinical formatting  -- attach clinical classification (Normal /
                            Prediabetic / Diabetic) to each value using
                            the same ADA/WHO thresholds as Dataset 2
4. Semantic chunking    -- convert each patient-month record into a
                            natural-language paragraph, ready to be
                            embedded in Phase D

Input:  json_reports/*.json   (from Phase B)
        data/Synthetic_diabetes_dataset1.xlsx (Patient_Master sheet, for
        age/gender context in the generated chunk text)
Output: preprocessed/clean_records.json       (cleaned structured records)
        preprocessed/rejected_records.json    (records that failed noise removal)
        preprocessed/chunks/<id>_<month>.txt   (one semantic chunk per record)
        preprocessed/chunks_manifest.json     (index of all chunks, for Phase D)

Run this from your MediRAG root folder (same level as json_reports/, data/).
"""

import os
import re
import json
import glob
import pandas as pd

# -----------------------------
# Config
# -----------------------------
JSON_REPORTS_DIR = "json_reports"
EXCEL_PATH = os.path.join("data", "Synthetic_diabetes_dataset1.xlsx")
PATIENT_MASTER_SHEET = "Patient_Master"

OUT_DIR = "preprocessed"
CHUNKS_DIR = os.path.join(OUT_DIR, "chunks")
CLEAN_RECORDS_PATH = os.path.join(OUT_DIR, "clean_records.json")
REJECTED_RECORDS_PATH = os.path.join(OUT_DIR, "rejected_records.json")
DROPPED_DUPLICATES_PATH = os.path.join(OUT_DIR, "dropped_duplicates.json")
MANIFEST_PATH = os.path.join(OUT_DIR, "chunks_manifest.json")

os.makedirs(CHUNKS_DIR, exist_ok=True)

REQUIRED_FIELDS = ["Patient_ID", "Month", "HbA1c", "FBS", "PPBS", "LDL", "HDL", "Triglycerides"]
NUMERIC_FIELDS = ["HbA1c", "FBS", "PPBS", "LDL", "HDL", "Triglycerides"]


# =====================================================================
# STEP 1: Noise Removal
# =====================================================================
def is_valid_record(record):
    """
    A record passes noise removal only if:
    - Patient_ID and Month are present
    - At least 4 of the 6 numeric fields are present and parseable as numbers
      (allows for 1-2 OCR misses without throwing away the whole record,
      but rejects records that are mostly empty/garbled)
    """
    if not record.get("Patient_ID") or not record.get("Month"):
        return False, "Missing Patient_ID or Month"

    valid_numeric_count = 0
    for field in NUMERIC_FIELDS:
        val = record.get(field)
        if val is not None:
            try:
                float(val)
                valid_numeric_count += 1
            except (ValueError, TypeError):
                pass

    if valid_numeric_count < 4:
        return False, f"Only {valid_numeric_count}/6 numeric fields valid"

    return True, None


def clean_record(record):
    """Convert numeric string fields to actual floats, leave missing ones as None."""
    cleaned = {
        "Patient_ID": record.get("Patient_ID"),
        "Month": record.get("Month"),
        "Source_Quality": record.get("Source_Quality", "Unknown"),
    }
    for field in NUMERIC_FIELDS:
        val = record.get(field)
        try:
            cleaned[field] = float(val) if val is not None else None
        except (ValueError, TypeError):
            cleaned[field] = None
    return cleaned


def run_noise_removal(raw_records):
    """Split records into accepted (clean) and rejected, with reasons logged."""
    accepted = []
    rejected = []

    for record in raw_records:
        valid, reason = is_valid_record(record)
        if valid:
            accepted.append(clean_record(record))
        else:
            rejected.append({**record, "_rejection_reason": reason})

    return accepted, rejected


def run_deduplication(accepted_records):
    """
    If both a Clean and Degraded version of the same Patient_ID + Month
    exist (this happens because Phase B runs OCR on both image sets),
    keep only the Clean version -- it is strictly more reliable and using
    both would mean two competing chunks for the same real-world fact in
    the vector database, which would quietly hurt retrieval accuracy in
    later phases. Degraded duplicates are dropped here, logged, and kept
    out of the embedding pipeline entirely (they already served their
    purpose in the Phase B OCR robustness evaluation).
    """
    best_by_key = {}
    dropped_duplicates = []

    quality_rank = {"Clean": 2, "Unknown": 1, "Degraded": 0}

    for record in accepted_records:
        key = (record["Patient_ID"], record["Month"])
        current_rank = quality_rank.get(record.get("Source_Quality", "Unknown"), 1)

        if key not in best_by_key:
            best_by_key[key] = record
        else:
            existing_rank = quality_rank.get(best_by_key[key].get("Source_Quality", "Unknown"), 1)
            if current_rank > existing_rank:
                dropped_duplicates.append(best_by_key[key])
                best_by_key[key] = record
            else:
                dropped_duplicates.append(record)

    deduplicated = list(best_by_key.values())
    return deduplicated, dropped_duplicates


# =====================================================================
# STEP 2: Unit Normalization
# =====================================================================
def normalize_hba1c(value, unit="%"):
    """
    Convert HbA1c to % (NGSP), the standard your Reference_Ranges use.
    Supports mmol/mol (IFCC), which is the other common reporting unit
    internationally, using the standard NGSP-IFCC master equation:
        NGSP(%) = (IFCC(mmol/mol) / 10.929) + 2.15
    """
    if value is None:
        return None
    if unit.lower() in ("%", "ngsp", "percent"):
        return round(value, 2)
    if unit.lower() in ("mmol/mol", "ifcc"):
        return round((value / 10.929) + 2.15, 2)
    return round(value, 2)  # assume already %


def normalize_glucose(value, unit="mg/dl"):
    """
    Convert glucose-type values (FBS, PPBS) to mg/dL, the standard your
    Reference_Ranges use. Supports mmol/L, the SI unit used in many
    countries outside the US/India.
        mg/dL = mmol/L * 18.0182
    """
    if value is None:
        return None
    if unit.lower() in ("mg/dl", "mg/dL".lower()):
        return round(value, 1)
    if unit.lower() in ("mmol/l", "mmol/L".lower()):
        return round(value * 18.0182, 1)
    return round(value, 1)


def normalize_lipid(value, unit="mg/dl"):
    """Same mg/dL <-> mmol/L logic applies to LDL/HDL/Triglycerides."""
    if value is None:
        return None
    if unit.lower() in ("mg/dl", "mg/dL".lower()):
        return round(value, 1)
    if unit.lower() in ("mmol/l", "mmol/L".lower()):
        return round(value * 38.67, 1)  # cholesterol conversion factor
    return round(value, 1)


def run_unit_normalization(record, units=None):
    """
    Apply unit normalization to a single cleaned record.
    `units` is an optional dict like {"HbA1c": "%", "FBS": "mg/dl", ...} --
    in this project all synthetic data is already generated in mg/dL and %,
    so this is effectively a no-op pass-through, but the conversion logic
    is here and active so the pipeline is ready for real-world reports
    that may use different units.
    """
    units = units or {}
    normalized = dict(record)
    normalized["HbA1c"] = normalize_hba1c(record.get("HbA1c"), units.get("HbA1c", "%"))
    normalized["FBS"] = normalize_glucose(record.get("FBS"), units.get("FBS", "mg/dl"))
    normalized["PPBS"] = normalize_glucose(record.get("PPBS"), units.get("PPBS", "mg/dl"))
    normalized["LDL"] = normalize_lipid(record.get("LDL"), units.get("LDL", "mg/dl"))
    normalized["HDL"] = normalize_lipid(record.get("HDL"), units.get("HDL", "mg/dl"))
    normalized["Triglycerides"] = normalize_lipid(record.get("Triglycerides"), units.get("Triglycerides", "mg/dl"))
    return normalized


# =====================================================================
# STEP 3: Clinical Formatting (classification using ADA/WHO thresholds)
# =====================================================================
def classify_hba1c(value):
    if value is None:
        return "Unknown"
    if value >= 6.5:
        return "Diabetic"
    if value >= 5.7:
        return "Prediabetic"
    return "Normal"


def classify_fbs(value):
    if value is None:
        return "Unknown"
    if value >= 126:
        return "Diabetic"
    if value >= 100:
        return "Prediabetic"
    return "Normal"


def classify_ppbs(value):
    if value is None:
        return "Unknown"
    if value >= 200:
        return "Diabetic"
    if value >= 140:
        return "Prediabetic"
    return "Normal"


def classify_ldl(value):
    if value is None:
        return "Unknown"
    if value >= 130:
        return "High Risk"
    if value >= 100:
        return "Borderline"
    return "Optimal"


def classify_hdl(value, gender="Unknown"):
    if value is None:
        return "Unknown"
    threshold = 50 if gender == "Female" else 40
    return "Normal" if value >= threshold else "Low"


def classify_triglycerides(value):
    if value is None:
        return "Unknown"
    if value >= 200:
        return "High"
    if value >= 150:
        return "Borderline"
    return "Normal"


def overall_status(hba1c_class, fbs_class):
    """Mirrors the Overall_Status logic already used in Laboratory_Reports sheet."""
    if "Diabetic" in (hba1c_class, fbs_class):
        return "Diabetic"
    if "Prediabetic" in (hba1c_class, fbs_class):
        return "Prediabetic"
    if "Unknown" in (hba1c_class, fbs_class):
        return "Unknown"
    return "Normal"


def run_clinical_formatting(record, gender="Unknown"):
    """Attach a classification label to every field, plus an overall status."""
    formatted = dict(record)
    formatted["HbA1c_Class"] = classify_hba1c(record.get("HbA1c"))
    formatted["FBS_Class"] = classify_fbs(record.get("FBS"))
    formatted["PPBS_Class"] = classify_ppbs(record.get("PPBS"))
    formatted["LDL_Class"] = classify_ldl(record.get("LDL"))
    formatted["HDL_Class"] = classify_hdl(record.get("HDL"), gender)
    formatted["Triglycerides_Class"] = classify_triglycerides(record.get("Triglycerides"))
    formatted["Overall_Status"] = overall_status(formatted["HbA1c_Class"], formatted["FBS_Class"])
    return formatted


# =====================================================================
# STEP 4: Semantic Chunking
# =====================================================================
def value_or_unknown(value, unit=""):
    return f"{value}{unit}" if value is not None else "not available"


def build_semantic_chunk(record, patient_info=None):
    """
    Convert one formatted patient-month record into a natural-language
    paragraph. This is the actual text that gets embedded in Phase D --
    embedding models work far better on natural sentences than on raw
    JSON key-value pairs, since the embedding captures clinical meaning,
    not just field names.
    """
    patient_info = patient_info or {}
    age = patient_info.get("Age", "unknown age")
    gender = patient_info.get("Gender", "unknown gender")

    pid = record["Patient_ID"]
    month = record["Month"].replace("_", " ")

    chunk = (
        f"Laboratory Report Summary for Patient {pid} ({gender}, age {age}) -- {month}.\n\n"
        f"HbA1c: {value_or_unknown(record.get('HbA1c'), '%')} "
        f"(Classification: {record.get('HbA1c_Class', 'Unknown')}).\n"
        f"Fasting Blood Sugar (FBS): {value_or_unknown(record.get('FBS'), ' mg/dL')} "
        f"(Classification: {record.get('FBS_Class', 'Unknown')}).\n"
        f"Post-Prandial Blood Sugar (PPBS): {value_or_unknown(record.get('PPBS'), ' mg/dL')} "
        f"(Classification: {record.get('PPBS_Class', 'Unknown')}).\n"
        f"LDL Cholesterol: {value_or_unknown(record.get('LDL'), ' mg/dL')} "
        f"(Classification: {record.get('LDL_Class', 'Unknown')}).\n"
        f"HDL Cholesterol: {value_or_unknown(record.get('HDL'), ' mg/dL')} "
        f"(Classification: {record.get('HDL_Class', 'Unknown')}).\n"
        f"Triglycerides: {value_or_unknown(record.get('Triglycerides'), ' mg/dL')} "
        f"(Classification: {record.get('Triglycerides_Class', 'Unknown')}).\n\n"
        f"Overall Glycemic Status: {record.get('Overall_Status', 'Unknown')}."
    )
    return chunk


# =====================================================================
# Main pipeline
# =====================================================================
def load_patient_master():
    """Load age/gender lookup, if the Patient_Master sheet exists."""
    if not os.path.exists(EXCEL_PATH):
        print(f"Note: {EXCEL_PATH} not found -- chunks will omit age/gender context.")
        return {}
    try:
        df = pd.read_excel(EXCEL_PATH, sheet_name=PATIENT_MASTER_SHEET)
        lookup = {}
        for _, row in df.iterrows():
            lookup[str(row["Patient_ID"]).strip()] = {
                "Age": row.get("Age"),
                "Gender": row.get("Gender"),
            }
        return lookup
    except Exception as e:
        print(f"Could not load Patient_Master sheet: {e}")
        return {}


def load_raw_json_reports():
    """
    Load every JSON file from json_reports/.
    Filenames follow the pattern <PatientID>_<Month>_<Clean|Degraded>.json
    (produced by Phase B). We extract that quality tag here so it can be
    tracked through the rest of the pipeline and reported on later
    (e.g. comparing groundedness of Clean- vs Degraded-sourced chunks
    in Phase I evaluation).
    """
    records = []
    for path in glob.glob(os.path.join(JSON_REPORTS_DIR, "*.json")):
        with open(path, "r") as f:
            try:
                record = json.load(f)
            except json.JSONDecodeError:
                print(f"  Skipping malformed JSON: {path}")
                continue

        filename = os.path.basename(path)
        if "_Degraded" in filename:
            record["Source_Quality"] = "Degraded"
        elif "_Clean" in filename:
            record["Source_Quality"] = "Clean"
        else:
            record["Source_Quality"] = "Unknown"

        records.append(record)
    return records


def main():
    print("Loading raw JSON reports from Phase B...")
    raw_records = load_raw_json_reports()
    print(f"Loaded {len(raw_records)} raw records.")

    patient_lookup = load_patient_master()

    print("\n--- Step 1: Noise Removal ---")
    accepted, rejected = run_noise_removal(raw_records)
    print(f"Accepted: {len(accepted)}  |  Rejected: {len(rejected)}")
    if rejected:
        for r in rejected[:5]:
            print(f"  Rejected {r.get('Patient_ID')}_{r.get('Month')}: {r.get('_rejection_reason')}")

    print("\n--- Step 1b: Deduplication (Clean preferred over Degraded) ---")
    deduplicated, dropped_duplicates = run_deduplication(accepted)
    print(f"Unique patient-month records: {len(deduplicated)}  |  Duplicates dropped: {len(dropped_duplicates)}")
    if dropped_duplicates:
        for d in dropped_duplicates[:5]:
            print(f"  Dropped duplicate {d['Patient_ID']}_{d['Month']} (Source_Quality: {d.get('Source_Quality')})")

    print("\n--- Step 2: Unit Normalization ---")
    normalized = [run_unit_normalization(r) for r in deduplicated]
    print(f"Normalized {len(normalized)} records (pass-through; all source data already mg/dL and %).")

    print("\n--- Step 3: Clinical Formatting ---")
    formatted = []
    for r in normalized:
        gender = patient_lookup.get(r["Patient_ID"], {}).get("Gender", "Unknown")
        formatted.append(run_clinical_formatting(r, gender))
    print(f"Classified {len(formatted)} records using ADA/WHO thresholds.")

    print("\n--- Step 4: Semantic Chunking ---")
    manifest = []
    for r in formatted:
        patient_info = patient_lookup.get(r["Patient_ID"], {})
        chunk_text = build_semantic_chunk(r, patient_info)

        chunk_filename = f"{r['Patient_ID']}_{r['Month']}.txt"
        chunk_path = os.path.join(CHUNKS_DIR, chunk_filename)
        with open(chunk_path, "w") as f:
            f.write(chunk_text)

        manifest.append({
            "Patient_ID": r["Patient_ID"],
            "Month": r["Month"],
            "Overall_Status": r["Overall_Status"],
            "Source_Quality": r.get("Source_Quality", "Unknown"),
            "chunk_file": chunk_path,
        })
    print(f"Created {len(manifest)} semantic chunks in '{CHUNKS_DIR}/'.")

    # Save outputs
    with open(CLEAN_RECORDS_PATH, "w") as f:
        json.dump(formatted, f, indent=2)
    with open(REJECTED_RECORDS_PATH, "w") as f:
        json.dump(rejected, f, indent=2)
    with open(DROPPED_DUPLICATES_PATH, "w") as f:
        json.dump(dropped_duplicates, f, indent=2)
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nSaved cleaned records to: {CLEAN_RECORDS_PATH}")
    print(f"Saved rejected records to: {REJECTED_RECORDS_PATH}")
    print(f"Saved dropped duplicates to: {DROPPED_DUPLICATES_PATH}")
    print(f"Saved chunk manifest to: {MANIFEST_PATH}")
    print("\nPhase C complete. Output is ready for Phase D (Embedding Generation).")


if __name__ == "__main__":
    main()