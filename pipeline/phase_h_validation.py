"""
phase_h_validation.py   (revised)

Phase H for Medi-RAG: Rule-Based Clinical Validation Layer

Checks every biomarker value mentioned in a generated answer:
  1. MISCLASSIFICATION: does the label stated next to the value agree with
     the ADA/WHO rules in Medical_Reference_Range_Dataset2.xlsx (Table 4)?
  2. FABRICATION: does the value actually appear in the context given to
     the LLM?

FIXES vs the previous version (same function names and outputs, so every
other script keeps working):
  FIX 1  Labels are matched as WHOLE WORDS. Before, "Prediabetic" was read
         as "Diabetic", "lower" as "Low", "higher" as "High".
  FIX 2  The label is only searched in the same sentence as the value.
  FIX 3  Month/visit numbers are skipped. Before, in "HbA1c in Month 2 was
         6.7%" the value read was 2, not 6.7.
  FIX 4  One value is counted once. Before, "Fasting Blood Sugar (FBS):
         139" was counted twice (once per name).
  FIX 5  Numbers are compared as numbers, not text. Before, "139" in an
         answer did not match "139.0" in the context and was flagged as
         fabricated (and "7.3" matched inside "17.3").
  FIX 6  Values between two rule ranges (e.g. HbA1c 6.45) are classified
         instead of silently skipped.
  FIX 7  validate_entry() reports whether any context was available, so
         "no context" can be separated from genuine fabrication.
"""

import os
import re
import json

import pandas as pd

REFERENCE_RANGE_PATH = os.path.join("data", "Medical_Reference_Range_Dataset2.xlsx")
REFERENCE_SHEET = "Reference_Ranges"
INPUT_PATH = os.path.join("evaluation", "generation_samples.json")
OUTPUT_PATH = os.path.join("evaluation", "validation_report.json")

# Longest names first, so "fasting blood sugar" wins over "sugar"-like overlaps
BIOMARKER_ALIASES = {
    "post-prandial blood sugar": "PPBS",
    "postprandial blood sugar": "PPBS",
    "post-meal blood sugar": "PPBS",
    "fasting blood sugar": "FBS",
    "triglycerides": "TG",
    "hba1c": "HbA1c",
    "ppbs": "PPBS",
    "fbs": "FBS",
    "ldl": "LDL",
    "hdl": "HDL",
}
ALIAS_PATTERN = re.compile(
    r"\b(" + "|".join(re.escape(a) for a in BIOMARKER_ALIASES) + r")\b", re.IGNORECASE)

KNOWN_LABELS = ["Diabetic-Severe", "Diabetic-Moderate", "Diabetic-Mild", "Prediabetic",
                "Diabetic", "Borderline", "High Risk", "Optimal", "Normal", "Low", "High"]
LABEL_PATTERN = re.compile(
    r"\b(" + "|".join(re.escape(l) for l in KNOWN_LABELS) + r")\b", re.IGNORECASE)  # FIX 1

NUMBER_PATTERN = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)")
MONTH_BEFORE = re.compile(r"(month|visit|months|visits|month_)\s*$", re.IGNORECASE)
LOOKAHEAD_CHARS = 60  # how far after the biomarker name to look for its value


def broad_category(label):
    label_lower = label.lower()
    if "prediabetic" in label_lower or "borderline" in label_lower or "impaired" in label_lower:
        return "prediabetic"
    if "normal" in label_lower or "optimal" in label_lower:
        return "normal"
    if "diabetic" in label_lower or "high" in label_lower:
        return "diabetic_or_high"
    if "low" in label_lower:
        return "low"
    return label_lower


# -----------------------------
# Rules (Table 4)
# -----------------------------
def parse_condition(condition_str, biomarker):
    condition_str = condition_str.strip()
    if "(M)" in condition_str or "(F)" in condition_str:
        return None  # sex-specific HDL rules: sex is not available here
    m = re.match(r"^([\d.]+)\s*-\s*([\d.]+)$", condition_str)
    if m:
        return (float(m.group(1)), float(m.group(2)))
    m = re.match(r"^<\s*([\d.]+)$", condition_str)
    if m:
        return (float("-inf"), float(m.group(1)))
    m = re.match(r"^>=\s*([\d.]+)$", condition_str)
    if m:
        return (float(m.group(1)), float("inf"))
    return None


def load_severity_rules():
    df = pd.read_excel(REFERENCE_RANGE_PATH, sheet_name=REFERENCE_SHEET, header=None)
    header_row_idx = next((i for i, row in df.iterrows() if str(row[0]).strip() == "Rule_ID"), None)
    if header_row_idx is None:
        raise ValueError("Could not find 'Rule_ID' header row in the reference ranges sheet.")
    rules_df = df.iloc[header_row_idx + 1:].copy()
    rules_df.columns = [str(c).strip() for c in df.iloc[header_row_idx]]
    rules_df = rules_df.dropna(subset=["Rule_ID"])
    label_col = "Severity_Label" if "Severity_Label" in rules_df.columns else "Security_Label"

    rules = []
    for _, row in rules_df.iterrows():
        bounds = parse_condition(str(row["Condition"]), str(row["Biomarker"]))
        if bounds is None:
            continue
        rules.append({"biomarker": str(row["Biomarker"]).strip(),
                      "min": bounds[0], "max": bounds[1],
                      "label": str(row[label_col]).strip()})
    return rules


def classify_value(biomarker, value, rules):
    """FIX 6: pick the rule with the highest lower bound <= value (no gaps between ranges)."""
    candidates = [r for r in rules if r["biomarker"].lower() == biomarker.lower()]
    if not candidates:
        return None
    lowest_min = min(r["min"] for r in candidates)
    lowest_rules = [r for r in candidates if r["min"] == lowest_min]
    if lowest_min != float("-inf") and value < lowest_min:
        return None  # below every rule (e.g. FBS < 70): not covered by Table 4
    best = max((r for r in candidates if r["min"] <= value), key=lambda r: r["min"],
               default=lowest_rules[0])
    return best["label"]


# -----------------------------
# Extraction
# -----------------------------
def _sentence_end(text, start):
    m = re.search(r"(?<!\d)[.!?](?!\d)|\n", text[start:])
    return start + m.start() if m else len(text)


def extract_mentions(text):
    """
    Returns [{"biomarker", "value", "context"}] with one entry per stated value.
    FIX 3: skips numbers that follow "Month"/"visit".
    FIX 4: a name right after another name (e.g. "Fasting Blood Sugar (FBS)")
           is treated as the same mention.
    """
    mentions = []
    alias_hits = list(ALIAS_PATTERN.finditer(text))
    last_alias_end = -100
    for i, hit in enumerate(alias_hits):
        if hit.start() - last_alias_end <= 3:     # e.g. "... Sugar (FBS)"
            last_alias_end = hit.end()
            continue
        last_alias_end = hit.end()
        canonical = BIOMARKER_ALIASES[hit.group(1).lower()]

        # value must come before the next biomarker name and within the lookahead
        stop = alias_hits[i + 1].start() if i + 1 < len(alias_hits) else len(text)
        stop = min(stop, hit.end() + LOOKAHEAD_CHARS)
        # extend past an immediately following alias, e.g. "(FBS)"
        j = i + 1
        while j < len(alias_hits) and alias_hits[j].start() - hit.end() <= 3:
            stop = min(alias_hits[j + 1].start() if j + 1 < len(alias_hits) else len(text),
                       alias_hits[j].end() + LOOKAHEAD_CHARS)
            j += 1
        window_start = hit.end()

        value, value_end = None, None
        for num in NUMBER_PATTERN.finditer(text, window_start, stop):
            if MONTH_BEFORE.search(text[max(0, num.start() - 8):num.start()]):
                continue
            value, value_end = float(num.group(1)), num.end()
            break
        if value is None:
            continue

        sentence_stop = _sentence_end(text, value_end)          # FIX 2
        mentions.append({"biomarker": canonical, "value": value,
                         "context": text[value_end:sentence_stop]})
    return mentions


def extract_claimed_label(context_text):
    m = LABEL_PATTERN.search(context_text)
    if not m:
        return None
    found = m.group(1).lower()
    return next(l for l in KNOWN_LABELS if l.lower() == found)


def _numbers_in(text):
    return {float(n) for n in NUMBER_PATTERN.findall(text)}


def value_appears_in_context(biomarker, value, retrieved_chunks):
    """FIX 5: numeric comparison, so 139 == 139.0 and 7.3 != 17.3."""
    for chunk in retrieved_chunks:
        if any(abs(value - n) < 1e-6 for n in _numbers_in(chunk.get("text", ""))):
            return True
    return False


# -----------------------------
# Validation
# -----------------------------
def validate_entry(entry, rules):
    answer_text = entry.get("answer", "")
    retrieved_chunks = entry.get("retrieved_chunks", [])
    has_context = any(c.get("text") for c in retrieved_chunks)

    issues, checked = [], 0
    for m in extract_mentions(answer_text):
        true_label = classify_value(m["biomarker"], m["value"], rules)
        if true_label is None:
            continue
        checked += 1
        claimed = extract_claimed_label(m["context"])
        problem = None
        if not value_appears_in_context(m["biomarker"], m["value"], retrieved_chunks):
            problem = "possible_fabrication" if has_context else "unverifiable_no_context"
        elif claimed is not None and broad_category(claimed) != broad_category(true_label):
            problem = "misclassification"
        if problem:
            issues.append({"type": problem, "biomarker": m["biomarker"], "value": m["value"],
                           "claimed_label": claimed, "true_label": true_label,
                           "context_snippet": m["context"][:100]})
    return {
        "query": entry.get("query"),
        "has_context": has_context,                                # FIX 7
        "checked_mentions": checked,
        "issues_found": len(issues),
        "issues": issues,
        "status": "FLAGGED" if issues else "PASSED",
    }


def main():
    rules = load_severity_rules()
    print(f"Loaded {len(rules)} parseable rules.\n")
    if not os.path.exists(INPUT_PATH):
        print(f"Could not find {INPUT_PATH} -- run phase_g_generation.py first.")
        return
    with open(INPUT_PATH) as f:
        generation_results = json.load(f)
    reports = [validate_entry(e, rules) for e in generation_results]
    for r in reports:
        print(f"[{r['status']}] \"{r['query']}\" -- {r['checked_mentions']} checked, {r['issues_found']} issue(s)")
        for i in r["issues"]:
            print(f"    - {i['type']}: {i['biomarker']} = {i['value']} "
                  f"(claimed: {i['claimed_label']}, true: {i['true_label']})")
    os.makedirs("evaluation", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(reports, f, indent=2)
    print(f"\nSaved -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()