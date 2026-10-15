"""
What this does:
1. Loads every image in reports_images/clean/ and reports_images/degraded/
2. Removes table grid lines (preprocessing fix)
3. Runs Tesseract OCR on the cleaned image
4. Parses the raw OCR text using regex to pull out structured fields:
   Patient_ID, Month, HbA1c, FBS, PPBS, LDL, HDL, Triglycerides
5. Saves each parsed report as a JSON file in json_reports/
6. Compares extracted values against the ground truth in
   data/Synthetic_diabetes_dataset1.xlsx (Laboratory_Reports sheet)
7. Calculates OCR Accuracy and Character Error Rate, separately for
   clean vs degraded images
8. Saves a full results report to evaluation/ocr_evaluation_report.xlsx
"""

import os
import re
import json
import pandas as pd
import numpy as np
import cv2
import pytesseract
from PIL import Image

# -----------------------------
# Config -- EDIT THESE IF NEEDED
# -----------------------------

# If Tesseract isn't auto-detected on Windows, uncomment and set this:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

CLEAN_DIR = os.path.join("reports_images", "clean")
DEGRADED_DIR = os.path.join("reports_images", "degraded")
JSON_OUT_DIR = "json_reports"
EVAL_OUT_DIR = "evaluation"

EXCEL_PATH = os.path.join("data", "Synthetic_diabetes_dataset1.xlsx")
LAB_SHEET_NAME = "Laboratory_Reports"

# Set to True to also save the preprocessed (degridded) images for inspection
SAVE_PREPROCESSED_DEBUG = True
DEBUG_DIR = os.path.join("reports_images", "_debug_preprocessed")

os.makedirs(JSON_OUT_DIR, exist_ok=True)
os.makedirs(EVAL_OUT_DIR, exist_ok=True)
if SAVE_PREPROCESSED_DEBUG:
    os.makedirs(DEBUG_DIR, exist_ok=True)

NUMERIC_FIELDS = ["HbA1c", "FBS", "PPBS", "LDL", "HDL", "Triglycerides"]

HEADER_PATTERNS = {
    "Patient_ID": r"Patient\s*ID\s*[:\-]?\s*([A-Za-z]?\s?[\dOo]{2,4})",
    "Month":      r"Month\s*[:\-]?\s*(Month[_\s]?\d+)",
}


# -----------------------------
# Preprocessing: remove table grid lines
# -----------------------------
def remove_grid_lines(gray_img):
    """
    Detects and removes thin horizontal/vertical grid lines from a grayscale
    image (typical of ReportLab table borders) that otherwise confuse
    Tesseract's text-region detection and cause whole table cells to be
    skipped during OCR.
    """
    thresh = cv2.adaptiveThreshold(
        ~gray_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2
    )

    horizontal = thresh.copy()
    vertical = thresh.copy()

    cols = horizontal.shape[1]
    horizontal_size = max(cols // 30, 1)
    horizontal_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))
    horizontal = cv2.erode(horizontal, horizontal_structure)
    horizontal = cv2.dilate(horizontal, horizontal_structure)

    rows = vertical.shape[0]
    vertical_size = max(rows // 30, 1)
    vertical_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, vertical_size))
    vertical = cv2.erode(vertical, vertical_structure)
    vertical = cv2.dilate(vertical, vertical_structure)

    grid = cv2.add(horizontal, vertical)
    grid_inv = cv2.bitwise_not(grid)
    result = cv2.bitwise_or(gray_img, cv2.bitwise_not(grid_inv))
    return result


def preprocess_image(image_path):
    """Load an image, convert to grayscale, strip grid lines, return a PIL Image."""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cleaned = remove_grid_lines(gray)
    return Image.fromarray(cleaned)


# -----------------------------
# OCR
# -----------------------------
def run_ocr_on_image(preprocessed_pil_img):
    """
    Run Tesseract OCR.
    --psm 6 (uniform block of text) works reliably ONCE the grid lines
    are removed -- the grid removal is what fixes the row-dropping issue,
    not the PSM mode itself.
    """
    config = "--psm 6"
    return pytesseract.image_to_string(preprocessed_pil_img, config=config)


# -----------------------------
# Parsing
# -----------------------------
def parse_header_fields(raw_text):
    result = {}
    for field, pattern in HEADER_PATTERNS.items():
        match = re.search(pattern, raw_text, re.IGNORECASE)
        result[field] = match.group(1).strip() if match else None
    return result


def clean_table_line(line):
    """Strip pipe/bracket noise left over from faint grid-line remnants."""
    return re.sub(r"[|\[\]_]+", " ", line)


def parse_table_fields(raw_text):
    """
    Extract the 6 lab values from the table section.
    Tesseract (after grid removal) typically outputs each row as one line,
    e.g. "HbA1c 5.2 %" or "Triglycerides 130 mg/dL", sometimes with stray
    pipe/bracket characters left over from faint border remnants -- those
    are stripped first.
    """
    # Tolerant prefix patterns for each field, allowing for common Tesseract
    # misreads (e.g. "1" read as "t"/"l"/"I", "c" sometimes dropped/added)
    FIELD_PREFIX_PATTERNS = {
        "HbA1c":         r"Hb\s*A\s*[1lItT]\s*c",
        "FBS":           r"FBS",
        "PPBS":          r"PPBS",
        "LDL":           r"LDL",
        "HDL":           r"HDL",
        "Triglycerides": r"Triglycerides",
    }

    lines = [clean_table_line(l).strip() for l in raw_text.split("\n") if l.strip()]
    result = {field: None for field in NUMERIC_FIELDS}

    for line in lines:
        for field in NUMERIC_FIELDS:
            prefix_pattern = FIELD_PREFIX_PATTERNS[field]
            match = re.match(rf"\s*{prefix_pattern}", line, re.IGNORECASE)
            if match:
                rest = line[match.end():]
                num_match = re.search(r"([\d]+[.,]?[\d]*)", rest)
                if num_match:
                    result[field] = num_match.group(1).replace(",", ".")

    return result


def normalize_month(month_str):
    if not month_str:
        return None
    digits = re.search(r"(\d+)", month_str)
    return f"Month_{digits.group(1)}" if digits else month_str


def normalize_patient_id(pid_str):
    if not pid_str:
        return None
    # Fix common OCR confusion: letter O misread instead of digit 0
    pid_str = pid_str.replace("O", "0").replace("o", "0")
    digits = re.search(r"(\d+)", pid_str)
    return f"P{int(digits.group(1)):03d}" if digits else pid_str.upper()


# -----------------------------
# Ground truth loading
# -----------------------------
def load_ground_truth():
    df = pd.read_excel(EXCEL_PATH, sheet_name=LAB_SHEET_NAME)

    def find_col(possible_names):
        for name in possible_names:
            if name in df.columns:
                return name
        return None

    col_map = {
        "HbA1c": find_col(["HbA1c(%)", "HbA1c (%)", "HbA1c"]),
        "FBS": find_col(["FBS (mg/dL)", "FBS (mg/dl)", "FBS(mg/dl)", "FBS"]),
        "PPBS": find_col(["PPBS (mg/dL)", "PPBS  (mg/dl)", "PPBS(mg/dl)", "PPBS"]),
        "LDL": find_col(["LDL", "LDL (mg/dL)"]),
        "HDL": find_col(["HDL", "HDL (mg/dL)"]),
        "Triglycerides": find_col(["Triglycerides", "Triglycerides (mg/dL)"]),
    }

    gt_lookup = {}
    for _, row in df.iterrows():
        key = (str(row["Patient_ID"]).strip(), str(row["Month"]).strip())
        gt_lookup[key] = {field: row.get(col) for field, col in col_map.items() if col}
    return gt_lookup


# -----------------------------
# Comparison
# -----------------------------
def values_match(extracted, truth, tolerance=0.01):
    if extracted is None or truth is None:
        return False
    try:
        return abs(float(extracted) - float(truth)) <= tolerance
    except (ValueError, TypeError):
        return str(extracted).strip().lower() == str(truth).strip().lower()


def char_error_rate(extracted, truth):
    a = "" if extracted is None else str(extracted)
    b = str(truth)
    if len(b) == 0:
        return 0.0 if len(a) == 0 else 1.0

    prev_row = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        curr_row = [i] + [0] * len(b)
        for j, cb in enumerate(b, start=1):
            cost = 0 if ca == cb else 1
            curr_row[j] = min(
                prev_row[j] + 1,
                curr_row[j - 1] + 1,
                prev_row[j - 1] + cost
            )
        prev_row = curr_row
    return prev_row[-1] / len(b)


def find_best_ground_truth_match(parsed_id, parsed_month, ground_truth):
    """
    Try an exact (Patient_ID, Month) match first. If that fails (common on
    degraded images where a digit gets misread, e.g. P099 -> P399), fall
    back to matching on Month plus the closest Patient_ID by edit distance.
    This ensures degraded images still contribute field-level accuracy data
    instead of being skipped entirely just because the ID had one bad digit.
    Returns (truth_dict_or_None, key_used, was_exact_match).
    """
    key = (parsed_id, parsed_month)
    if key in ground_truth:
        return ground_truth[key], key, True

    if not parsed_id or not parsed_month:
        return None, key, False

    candidates = [k for k in ground_truth.keys() if k[1] == parsed_month]
    if not candidates:
        return None, key, False

    def id_distance(a, b):
        if len(a) != len(b):
            return max(len(a), len(b))
        return sum(1 for x, y in zip(a, b) if x != y)

    best_key = min(candidates, key=lambda k: id_distance(k[0], parsed_id))
    if id_distance(best_key[0], parsed_id) <= 1:
        return ground_truth[best_key], best_key, False

    return None, key, False


# -----------------------------
# Main pipeline
# -----------------------------
def process_folder(folder_path, image_type_label, ground_truth):
    if not os.path.isdir(folder_path):
        print(f"Folder not found, skipping: {folder_path}")
        return []

    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    print(f"\nProcessing {len(image_files)} images in '{folder_path}' ({image_type_label})...")

    records = []
    unmatched = []
    ocr_errors = 0

    for img_file in image_files:
        img_path = os.path.join(folder_path, img_file)
        base_name = os.path.splitext(img_file)[0].replace("_degraded", "")

        try:
            preprocessed = preprocess_image(img_path)
            if SAVE_PREPROCESSED_DEBUG:
                preprocessed.save(os.path.join(DEBUG_DIR, img_file))
            raw_text = run_ocr_on_image(preprocessed)
        except Exception as e:
            print(f"  OCR failed on {img_file}: {e}")
            ocr_errors += 1
            continue

        header = parse_header_fields(raw_text)
        table_vals = parse_table_fields(raw_text)

        parsed = {
            "Patient_ID": normalize_patient_id(header.get("Patient_ID")),
            "Month": normalize_month(header.get("Month")),
            **table_vals,
        }

        json_path = os.path.join(JSON_OUT_DIR, f"{base_name}_{image_type_label}.json")
        with open(json_path, "w") as f:
            json.dump(parsed, f, indent=2)

        truth, matched_key, was_exact = find_best_ground_truth_match(
            parsed.get("Patient_ID"), parsed.get("Month"), ground_truth
        )

        if truth is None:
            unmatched.append((base_name, (parsed.get("Patient_ID"), parsed.get("Month"))))
            continue

        # record whether the Patient_ID itself was read correctly
        records.append({
            "Image_Type": image_type_label,
            "File": img_file,
            "Patient_ID": parsed.get("Patient_ID"),
            "Month": parsed.get("Month"),
            "Field": "Patient_ID",
            "Ground_Truth_Value": matched_key[0],
            "OCR_Extracted_Value": parsed.get("Patient_ID"),
            "Correct": "Yes" if was_exact else "No",
            "Char_Error_Rate": round(char_error_rate(parsed.get("Patient_ID"), matched_key[0]), 4),
        })

        for field in NUMERIC_FIELDS:
            extracted_val = parsed.get(field)
            truth_val = truth.get(field)
            is_correct = values_match(extracted_val, truth_val)
            cer = char_error_rate(extracted_val, truth_val)

            records.append({
                "Image_Type": image_type_label,
                "File": img_file,
                "Patient_ID": parsed.get("Patient_ID"),
                "Month": parsed.get("Month"),
                "Field": field,
                "Ground_Truth_Value": truth_val,
                "OCR_Extracted_Value": extracted_val,
                "Correct": "Yes" if is_correct else "No",
                "Char_Error_Rate": round(cer, 4),
            })

    if ocr_errors:
        print(f"  {ocr_errors} image(s) failed OCR entirely.")
    if unmatched:
        print(f"  {len(unmatched)} file(s) had no matching ground truth (parsed ID/Month didn't match Excel):")
        for name, key in unmatched[:5]:
            print(f"    - {name} -> parsed as {key}")
        if len(unmatched) > 5:
            print(f"    ... and {len(unmatched) - 5} more")

    return records


def build_summary(records_df):
    summary_rows = []
    for image_type in records_df["Image_Type"].unique():
        subset = records_df[records_df["Image_Type"] == image_type]
        total = len(subset)
        correct = (subset["Correct"] == "Yes").sum()
        accuracy = round((correct / total) * 100, 2) if total > 0 else 0.0
        avg_cer = round(subset["Char_Error_Rate"].mean(), 4) if total > 0 else 0.0

        summary_rows.append({
            "Image_Type": image_type,
            "Total_Fields_Checked": total,
            "Correct": correct,
            "Incorrect": total - correct,
            "Accuracy_%": accuracy,
            "Avg_Char_Error_Rate": avg_cer,
        })

    return pd.DataFrame(summary_rows)


def main():
    print("Loading ground truth from Excel...")
    ground_truth = load_ground_truth()
    print(f"Loaded {len(ground_truth)} ground-truth records.")

    all_records = []
    all_records += process_folder(CLEAN_DIR, "Clean", ground_truth)
    all_records += process_folder(DEGRADED_DIR, "Degraded", ground_truth)

    if not all_records:
        print("\nNo records were generated -- check folder paths and ground truth matching.")
        return

    records_df = pd.DataFrame(all_records)
    summary_df = build_summary(records_df)

    print("\n=== SUMMARY ===")
    print(summary_df.to_string(index=False))

    eval_path = os.path.join(EVAL_OUT_DIR, "ocr_evaluation_report.xlsx")
    with pd.ExcelWriter(eval_path, engine="openpyxl") as writer:
        summary_df.to_excel(writer, sheet_name="Summary", index=False)
        records_df.to_excel(writer, sheet_name="Detailed_Comparison", index=False)

    print(f"\nFull results saved to: {eval_path}")
    print(f"Structured JSON reports saved to: {JSON_OUT_DIR}/")


if __name__ == "__main__":
    main()