"""
phase_l_8_rescore_rules_v2.py

Re-runs the rule validator on the SAVED v2 answers (no API calls) with two
scoring fixes, then rewrites the rule fields in the results file:

  FIX A  The model forecast (trajectory prediction) that was GIVEN to Claude
         in the prompt is now treated as context. Quoting it is not fabrication.
  FIX B  A value that equals a published threshold for that biomarker
         (e.g. "6.5% or higher is diabetic") and does not appear in the
         patient's data is labelled "reference_threshold", not fabrication.
         It is reported separately so readers can see how many there were.

A backup of the original file is kept as ..._before_rescore.json.
Prints Table V before and after, plus the remaining flagged values so you
can check by eye whether they are real errors.

Usage:  python phase_l_8_rescore_rules_v2.py            (run 1)
        python phase_l_8_rescore_rules_v2.py --run-id 2
"""
import argparse
import json
import os
import shutil
from collections import defaultdict

from phase_h_validation import load_severity_rules, validate_entry
from results_logger import save_result

V2_DIR = os.path.join("evaluation", "v2")
CONFIGS = ["plain_llm", "standard_rag", "full_system", "full_system_corrective"]


def forecast_chunk(traj):
    """The forecast block Claude saw, as a pseudo-chunk the validator can match against."""
    if not traj:
        return []
    text = (f"Predicted next HbA1c: {traj.get('predicted_HbA1c')}% "
            f"Predicted next FBS: {traj.get('predicted_FBS')} mg/dL "
            f"Predicted next PPBS: {traj.get('predicted_PPBS')} mg/dL")
    return [{"text": text}]


def thresholds_by_biomarker(rules):
    out = defaultdict(set)
    for r in rules:
        for v in (r["min"], r["max"]):
            if v not in (float("inf"), float("-inf")):
                out[r["biomarker"].lower()].add(round(float(v), 2))
    return out


def table_v(results):
    t = {}
    for c in CONFIGS:
        rows = [r["configs"][c] for r in results.values() if c in r["configs"]]
        with_vals = [e for e in rows if e["rule_checked"] > 0]
        checked = sum(e["rule_checked"] for e in with_vals)
        types = defaultdict(int)
        for e in with_vals:
            for x in e["rule_issue_types"]:
                types[x] += 1
        real = types["misclassification"] + types["possible_fabrication"]
        t[c] = {"coverage": round(len(with_vals) / len(rows), 3) if rows else None,
                "values_checked": checked, "issues_by_type": dict(types),
                "real_issue_rate": round(real / checked, 3) if checked else None}
    return t


def show(title, t):
    print(f"\n{title}")
    for c, v in t.items():
        print(f"  {c:<24} coverage {v['coverage']}  values {v['values_checked']}  "
              f"issue rate {v['real_issue_rate']}  {v['issues_by_type']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", type=int, default=1)
    a = ap.parse_args()
    path = os.path.join(V2_DIR, f"benchmark_v2_results_run{a.run_id}.json")
    backup = path.replace(".json", "_before_rescore.json")
    if not os.path.exists(backup):
        shutil.copy2(path, backup)
        print(f"Backup saved -> {backup}")
    with open(backup) as f:          # always rescore from the untouched original
        results = json.load(f)

    before = table_v(results)
    show("TABLE V  BEFORE", before)

    rules = load_severity_rules()
    thresholds = thresholds_by_biomarker(rules)
    from phase_ef_vectorDB import retrieve_top_k, load_index
    index, metadata = load_index()

    flagged = []
    for qid, rec in results.items():
        pid = rec.get("patient_id")
        chunks = retrieve_top_k(rec["query_text"], k=5, index=index, metadata=metadata,
                                patient_filter=pid) if pid else []
        for c in CONFIGS:
            e = rec["configs"].get(c)
            if e is None:
                continue
            ctx = [] if c == "plain_llm" else chunks + forecast_chunk(e.get("trajectory"))
            val = validate_entry({"answer": e["answer"], "retrieved_chunks": ctx}, rules)
            types = []
            for issue in val["issues"]:
                t = issue["type"]
                if (t == "possible_fabrication"
                        and round(issue["value"], 2) in thresholds[issue["biomarker"].lower()]):
                    t = "reference_threshold"
                types.append(t)
                if t in ("possible_fabrication", "misclassification"):
                    flagged.append((qid, c, t, issue["biomarker"], issue["value"],
                                    issue["claimed_label"], issue["context_snippet"][:70]))
            e["rule_checked"] = val["checked_mentions"]
            e["rule_issues"] = sum(t in ("possible_fabrication", "misclassification") for t in types)
            e["rule_issue_types"] = types

    after = table_v(results)
    show("TABLE V  AFTER (forecast counted as context; reference thresholds separated)", after)

    with open(path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nUpdated -> {path}")

    print(f"\nRemaining flagged values ({len(flagged)}) -- check whether these are real errors:")
    for row in flagged[:40]:
        print("  ", " | ".join(str(x) for x in row))
    if len(flagged) > 40:
        print(f"   ... and {len(flagged) - 40} more (all saved in results/)")

    save_result("benchmark_v2", f"table_v_rescored_run{a.run_id}",
                {"before": before, "after": after,
                 "remaining_flags": [dict(zip(["query_id", "config", "type", "biomarker", "value",
                                               "claimed_label", "snippet"], r)) for r in flagged]},
                notes="Table V with forecast as context and reference thresholds separated")


if __name__ == "__main__":
    main()