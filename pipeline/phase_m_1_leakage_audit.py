"""
phase_m_1_leakage_audit.py   (Upgrade U1 -- no API calls; needs vector_db/ and
                              the Bio_ClinicalBERT download, same as phase_ef)

Measures CROSS-PATIENT LEAKAGE: how often plain top-k vector search puts
OTHER patients' records into the context the LLM sees, and confirms that
patient-scoped retrieval removes it.

Two query sets:
  normal       every benchmark query that names a patient (15 patient + 50 trap)
  adversarial  for each patient P, a question asked AS P that quotes ANOTHER
               patient X's exact HbA1c and FBS values -- the hardest case,
               because similar numbers pull X's chunks in

Metrics (k = 5):
  leakage@5        share of retrieved chunks that belong to someone else
  any_leak         share of queries with at least one foreign chunk
  targeted_leak    (adversarial) share of queries that retrieved X's own chunk
  own_recall       share of the patient's own 3 chunks that were retrieved
  latency          ms per query, unrestricted vs scoped

Usage (from the MediRAG root):
    python pipeline/phase_m_1_leakage_audit.py
Output:
    results/retrieval/leakage_audit.json
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
CLEAN_RECORDS = os.path.join("preprocessed", "clean_records.json")
K = 5


def load_patients():
    by_pid = {}
    with open(CLEAN_RECORDS) as f:
        for r in json.load(f):
            by_pid.setdefault(r["Patient_ID"], {})[r["Month"]] = r
    return by_pid


def normal_queries():
    with open(RESULTS_PATH) as f:
        res = json.load(f)
    return [(r["query_text"], r["patient_id"], None) for r in res.values() if r.get("patient_id")]


def adversarial_queries(patients):
    pids = sorted(patients)
    out = []
    for i, p in enumerate(pids):
        x = pids[(i + 1) % len(pids)]                      # a different patient
        months = [patients[x][m] for m in sorted(patients[x])]
        a = ", ".join(f"{m['HbA1c']}%" for m in months)
        f = ", ".join(f"{m['FBS']:g} mg/dL" for m in months)
        q = f"My HbA1c readings were {a} and my fasting blood sugar was {f}. Is this getting worse?"
        out.append((q, p, x))
    return out


def run(queries, index, metadata, scoped):
    leak, any_leak, targeted, recall, ms = [], [], [], [], []
    for q, pid, other in queries:
        t0 = time.perf_counter()
        res = retrieve_top_k(q, k=K, index=index, metadata=metadata,
                             patient_filter=pid if scoped else None)
        ms.append((time.perf_counter() - t0) * 1000)
        ids = [r["Patient_ID"] for r in res]
        foreign = sum(i != pid for i in ids)
        leak.append(foreign / len(ids) if ids else 0.0)
        any_leak.append(foreign > 0)
        recall.append(sum(i == pid for i in ids) / 3)       # each patient has 3 visits
        if other is not None:
            targeted.append(other in ids)
    out = {"queries": len(queries),
           "leakage_at_5": round(st.mean(leak), 3),
           "queries_with_any_leak": round(st.mean(any_leak), 3),
           "own_chunk_recall": round(st.mean(recall), 3),
           "latency_ms_p50": round(st.median(ms), 1)}
    if targeted:
        out["targeted_leak_rate"] = round(st.mean(targeted), 3)
    return out


def main():
    index, metadata = load_index()
    patients = load_patients()
    sets = {"normal": normal_queries(), "adversarial": adversarial_queries(patients)}
    retrieve_top_k("warm-up", k=1, index=index, metadata=metadata)   # load the model once
    out = {}
    for name, qs in sets.items():
        out[name] = {"unrestricted": run(qs, index, metadata, scoped=False),
                     "patient_scoped": run(qs, index, metadata, scoped=True)}
        print(f"\n{name.upper()} queries (n={len(qs)})")
        for mode, r in out[name].items():
            print(f"  {mode:<15} leakage@5 {r['leakage_at_5']:<6} any-leak {r['queries_with_any_leak']:<6}"
                  f" own-recall {r['own_chunk_recall']:<6} p50 {r['latency_ms_p50']} ms"
                  + (f"  targeted-leak {r['targeted_leak_rate']}" if "targeted_leak_rate" in r else ""))
    save_result("retrieval", "leakage_audit", out,
                notes="U1: cross-patient leakage, unrestricted vs patient-scoped top-5")


if __name__ == "__main__":
    main()
