"""
phase_m_6_cost_profile.py   (Upgrade U6 -- no API calls)

Profiles the cost of each configuration from the token usage SAVED in the v2
benchmark, and times the rule validator (which runs locally) on every answer.

  * input/output tokens per answer, per configuration
  * extra tokens spent by corrective regeneration
  * rule-validator latency per answer (ms)

Optional: --with-verifier also times the neural verifier (needs models/ locally).

Usage (from the MediRAG root):
    python pipeline/phase_m_6_cost_profile.py [--run-id 1] [--with-verifier]
Output:
    results/benchmark_v2/cost_profile_run1.json
"""
import argparse
import os
import statistics as st
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from phase_h_validation import load_severity_rules, validate_entry
from phase_l_7_labels_v2 import load_results
from phase_l_8_rescore_rules_v2 import forecast_chunk
from phase_m_3_routed_verification import patient_chunks
from results_logger import save_result

CONFIGS = ["plain_llm", "standard_rag", "full_system", "full_system_corrective"]


def pct(xs, p):
    xs = sorted(xs)
    return round(xs[min(len(xs) - 1, int(round(p / 100 * (len(xs) - 1))))], 3) if xs else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", type=int, default=1)
    ap.add_argument("--with-verifier", action="store_true")
    a = ap.parse_args()
    results = load_results(a.run_id)
    rules = load_severity_rules()
    verify = None
    if a.with_verifier:
        from phase_i_neural_verifier import verify_answer_by_matched_chunks as verify

    out = {"run_id": a.run_id, "configs": {}}
    print(f"{'config':<24}{'answers':>8}{'in tok':>9}{'out tok':>9}{'total':>9}"
          f"{'rule ms p50':>13}{'p95':>8}" + (f"{'verif ms p50':>14}" if verify else ""))
    for c in CONFIGS:
        ins, outs, rule_ms, ver_ms, regenerated = [], [], [], [], 0
        for rec in results.values():
            e = rec["configs"].get(c)
            if e is None:
                continue
            u = e.get("usage") or {}
            ins.append(u.get("input_tokens", 0)); outs.append(u.get("output_tokens", 0))
            if e.get("corrected"):
                regenerated += 1
            ctx = ([] if c == "plain_llm" or not rec.get("patient_id")
                   else patient_chunks(rec["patient_id"]) + forecast_chunk(e.get("trajectory")))
            t0 = time.perf_counter()
            validate_entry({"answer": e["answer"], "retrieved_chunks": ctx}, rules)
            rule_ms.append((time.perf_counter() - t0) * 1000)
            if verify and ctx:
                t0 = time.perf_counter()
                verify(e["answer"], ctx)
                ver_ms.append((time.perf_counter() - t0) * 1000)
        row = {"answers": len(ins), "mean_input_tokens": round(st.mean(ins), 1),
               "mean_output_tokens": round(st.mean(outs), 1),
               "mean_total_tokens": round(st.mean(ins) + st.mean(outs), 1),
               "answers_regenerated": regenerated,
               "rule_validator_ms_p50": pct(rule_ms, 50), "rule_validator_ms_p95": pct(rule_ms, 95)}
        if ver_ms:
            row["verifier_ms_p50"], row["verifier_ms_p95"] = pct(ver_ms, 50), pct(ver_ms, 95)
        out["configs"][c] = row
        print(f"{c:<24}{row['answers']:>8}{row['mean_input_tokens']:>9}{row['mean_output_tokens']:>9}"
              f"{row['mean_total_tokens']:>9}{row['rule_validator_ms_p50']:>13}{row['rule_validator_ms_p95']:>8}"
              + (f"{row.get('verifier_ms_p50', ''):>14}" if verify else ""))
    # In phase_l_6, corrective usage = ONLY the regeneration call (0 when not regenerated),
    # so its real cost is the full_system call plus this extra.
    fs, fc = out["configs"]["full_system"], out["configs"]["full_system_corrective"]
    fc["extra_tokens_over_full_system"] = fc["mean_total_tokens"]
    fc["mean_total_tokens_including_first_pass"] = round(fs["mean_total_tokens"] + fc["mean_total_tokens"], 1)
    print(f"\nCorrective regeneration ran on {fc['answers_regenerated']}/{fc['answers']} answers; "
          f"real cost per answer = {fc['mean_total_tokens_including_first_pass']} tokens "
          f"(full system {fs['mean_total_tokens']} + {fc['extra_tokens_over_full_system']} extra on average).")
    save_result("benchmark_v2", f"cost_profile_run{a.run_id}", out,
                notes="U6: token usage per configuration and checker latency")


if __name__ == "__main__":
    main()
