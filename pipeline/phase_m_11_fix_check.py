"""
phase_m_11_fix_check.py  --  test the two fixes on the affected Haiku answers only
(cohort 2; a few cents of API cost; NO labelling needed)

Run 2 (Haiku 5.5, max_tokens 800) showed two problems:
  1. answers cut off or empty because hidden reasoning used up the output budget
  2. corrective regeneration triggered only by validator false alarms (v1)

This script checks both fixes WITHOUT touching run 2's labelled results:
  Fix 1  re-generates every full-system answer that was cut off or empty, with
         max_tokens 2000, and records whether it now finishes.
  Fix 2  re-decides corrective regeneration with validator v4 (forecast-aware,
         every value checked) instead of v1, and regenerates only those, also
         with max_tokens 2000.
Outcome measured: the answer is complete (non-empty and not stopped by the
token limit). Answer quality is NOT re-labelled.

Usage (MediRAG_cohort2 folder, with the 4 cohort-2 settings set):
    $env:MEDIRAG_MODEL = "claude-haiku-5-5"
    python pipeline/phase_m_11_fix_check.py --dry-run     # lists what would be re-run, no API calls
    python pipeline/phase_m_11_fix_check.py
Output:
    results/cohort2/fix_check.json
"""
import argparse
import json
import os
import re
import sys

os.environ["MEDIRAG_MAX_TOKENS"] = "2000"
os.environ.setdefault("MEDIRAG_MODEL", "claude-haiku-5-5")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import phase_l_6_benchmark_v2 as bench  # noqa: E402
from phase_h_validation import load_severity_rules  # noqa: E402
from phase_ef_vectorDB import load_index, retrieve_top_k  # noqa: E402

RUN2 = os.path.join("evaluation", "v2", "benchmark_v2_results_run2.json")
OUT = os.path.join("results", "cohort2", "fix_check.json")
OLD_LIMIT = 800


def incomplete(answer, output_tokens, limit):
    a = (answer or "").strip()
    return (not a) or (output_tokens >= limit and not re.search(r'[.!?)\]*"”:|]\s*$', a))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    assert bench.MAX_TOKENS == 2000, "MEDIRAG_MAX_TOKENS must be 2000 here"
    if bench.TOP_K != 8:
        sys.exit(f"MEDIRAG_TOP_K is {bench.TOP_K}, but cohort 2 needs 8 (all visits). In this window run:\n"
                 f'    $env:MEDIRAG_TOP_K = "8"\nthen start the script again.')
    res = json.load(open(RUN2))
    rules = load_severity_rules()

    redo_full = [q for q, r in res.items() if "full_system" in r["configs"]
                 and incomplete(r["configs"]["full_system"]["answer"],
                                r["configs"]["full_system"]["usage"]["output_tokens"], OLD_LIMIT)]
    old_corr = [q for q, r in res.items() if (r["configs"].get("full_system_corrective") or {}).get("corrected")]
    old_corr_bad = [q for q in old_corr if incomplete(res[q]["configs"]["full_system_corrective"]["answer"],
                                                     res[q]["configs"]["full_system_corrective"]["usage"]["output_tokens"],
                                                     OLD_LIMIT)]
    print(f"Fix 1: {len(redo_full)} full-system answers were cut off or empty at 800 tokens")
    print(f"Fix 2: v1 regenerated {len(old_corr)} answers ({len(old_corr_bad)} of them ended cut off or empty)")
    index, metadata = load_index()
    if a.dry_run:
        n4 = 0
        for qid, r in res.items():
            if not r["patient_id"] or "full_system" not in r["configs"]:
                continue
            q = {k: r[k] for k in ("query_id", "category", "patient_id", "query_text", "trap_type")}
            chunks = retrieve_top_k(q["query_text"], k=bench.TOP_K, index=index, metadata=metadata,
                                    patient_filter=q["patient_id"])
            fs = r["configs"]["full_system"]
            n4 += bool(bench.corrective_issues_v4(
                q, {"answer": fs["answer"], "chunks": chunks, "trajectory": fs.get("trajectory")}, rules))
        print(f"Fix 2: v4 would regenerate {n4} answers (expected about 7)")
        print("Dry run: no API calls made.")
        return

    out = {"model": bench.CLAUDE_MODEL, "max_tokens": bench.MAX_TOKENS, "fix1": {}, "fix2": {}}
    for i, qid in enumerate(redo_full, 1):
        r = res[qid]
        q = {k: r[k] for k in ("query_id", "category", "patient_id", "query_text", "trap_type")}
        chunks = retrieve_top_k(q["query_text"], k=bench.TOP_K, index=index, metadata=metadata,
                                patient_filter=q["patient_id"] or None) if q["patient_id"] else []
        g = bench.gen_full(q, {"chunks": chunks})
        done = not incomplete(g["answer"], g["usage"]["output_tokens"], bench.MAX_TOKENS)
        out["fix1"][qid] = {"complete": done, "output_tokens": g["usage"]["output_tokens"],
                            "chars": len(g["answer"]), "answer": g["answer"]}
        print(f"[fix 1 {i}/{len(redo_full)}] {qid} complete={done} tokens={g['usage']['output_tokens']}")

    # Fix 2: re-decide with v4 on the ORIGINAL full-system answers (as the corrective step would)
    v4_trigger = []
    for qid, r in res.items():
        if not r["patient_id"] or "full_system" not in r["configs"]:
            continue
        q = {k: r[k] for k in ("query_id", "category", "patient_id", "query_text", "trap_type")}
        chunks = retrieve_top_k(q["query_text"], k=bench.TOP_K, index=index, metadata=metadata,
                                patient_filter=q["patient_id"])
        fs = r["configs"]["full_system"]
        full_result = {"answer": fs["answer"], "chunks": chunks, "trajectory": fs.get("trajectory")}
        if bench.corrective_issues_v4(q, full_result, rules):
            g = bench.gen_corrective(q, {"chunks": chunks}, full_result, rules)
            done = not incomplete(g["answer"], g["usage"]["output_tokens"], bench.MAX_TOKENS)
            v4_trigger.append(qid)
            out["fix2"][qid] = {"problems_sent": g.get("problems_sent"), "complete": done,
                                "output_tokens": g["usage"]["output_tokens"], "answer": g["answer"]}
            print(f"[fix 2] {qid} regenerated, complete={done}")
    f1 = out["fix1"]
    out["summary"] = {
        "fix1_redone": len(f1), "fix1_complete": sum(v["complete"] for v in f1.values()),
        "fix2_v1_regenerations": len(old_corr), "fix2_v1_incomplete_after": len(old_corr_bad),
        "fix2_v4_regenerations": len(v4_trigger),
        "fix2_v4_incomplete_after": sum(not v["complete"] for v in out["fix2"].values()),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    s = out["summary"]
    print(f"\nFix 1: {s['fix1_complete']}/{s['fix1_redone']} previously cut-off/empty answers now complete "
          f"(max_tokens 2000)")
    print(f"Fix 2: regenerations {s['fix2_v1_regenerations']} (v1) -> {s['fix2_v4_regenerations']} (v4); "
          f"incomplete after regeneration {s['fix2_v1_incomplete_after']} -> {s['fix2_v4_incomplete_after']}")
    print(f"Saved -> {OUT}")


if __name__ == "__main__":
    main()