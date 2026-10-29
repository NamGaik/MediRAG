"""
phase_m_9_scoped_fastpath.py   (Upgrade U9 -- no API calls; needs vector_db/ and
                                the Bio_ClinicalBERT download, same as phase_ef)

For patient-scoped queries, compares:
  ranked     the current path: embed the query with Bio_ClinicalBERT, rank all
             150 chunks with FAISS, keep the patient's chunks
  fast path  skip embedding and FAISS; return the patient's chunks directly
             (retrieve_top_k(..., scoped_fast_path=True))

Checks that both return exactly the same SET of chunks for every query, and
reports latency. The order differs: the fast path is chronological (Month 1, 2, 3),
the ranked path is by similarity.

Usage (from the MediRAG root):
    python pipeline/phase_m_9_scoped_fastpath.py
Output:
    results/retrieval/scoped_fastpath.json
"""
import json
import os
import statistics as st
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from phase_ef_vectorDB import load_index, retrieve_top_k
from results_logger import save_result

RESULTS_PATH = os.path.join("evaluation", "v2", "benchmark_v2_results_run1.json")
K = 5
REPEATS = 3   # time each query several times and keep the median


def timed(fn):
    times, out = [], None
    for _ in range(REPEATS):
        t0 = time.perf_counter()
        out = fn()
        times.append((time.perf_counter() - t0) * 1000)
    return out, st.median(times)


def main():
    with open(RESULTS_PATH) as f:
        queries = [(r["query_text"], r["patient_id"]) for r in json.load(f).values()
                   if r.get("patient_id")]
    index, metadata = load_index()
    retrieve_top_k("warm-up", k=1, index=index, metadata=metadata)   # load the model once

    same_set, same_order, ranked_ms, fast_ms = 0, 0, [], []
    for q, pid in queries:
        ranked, t_r = timed(lambda: retrieve_top_k(q, k=K, index=index, metadata=metadata,
                                                   patient_filter=pid))
        fast, t_f = timed(lambda: retrieve_top_k(q, k=K, index=index, metadata=metadata,
                                                 patient_filter=pid, scoped_fast_path=True))
        ranked_ms.append(t_r); fast_ms.append(t_f)
        key = lambda rs: [(r["Patient_ID"], r["Month"]) for r in rs]
        same_set += set(key(ranked)) == set(key(fast))
        same_order += key(ranked) == key(fast)

    n = len(queries)
    out = {"queries": n,
           "identical_chunk_sets": same_set, "identical_order": same_order,
           "ranked_ms_p50": round(st.median(ranked_ms), 2),
           "ranked_ms_p95": round(sorted(ranked_ms)[int(0.95 * (n - 1))], 2),
           "fast_ms_p50": round(st.median(fast_ms), 3),
           "fast_ms_p95": round(sorted(fast_ms)[int(0.95 * (n - 1))], 3)}
    out["speedup_p50"] = round(out["ranked_ms_p50"] / max(out["fast_ms_p50"], 1e-6), 1)

    print(f"\nPatient-scoped queries: {n}")
    print(f"  identical chunk sets      {same_set}/{n}")
    print(f"  identical order           {same_order}/{n}  (fast path is chronological by design)")
    print(f"  ranked path   p50 {out['ranked_ms_p50']} ms   p95 {out['ranked_ms_p95']} ms")
    print(f"  fast path     p50 {out['fast_ms_p50']} ms   p95 {out['fast_ms_p95']} ms")
    print(f"  speed-up (p50)  {out['speedup_p50']}x")
    save_result("retrieval", "scoped_fastpath", out,
                notes="U9: skip query embedding for patient-scoped retrieval")


if __name__ == "__main__":
    main()
