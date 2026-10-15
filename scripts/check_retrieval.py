import json
from phase_ef_vectorDB import retrieve_top_k, load_index

index, metadata = load_index()
results = json.load(open("evaluation/benchmark_results_final.json"))
for cat in ["category_a", "category_c"]:
    for e in results[cat]:
        chunks = retrieve_top_k(e["query_text"], k=5, index=index,
                                metadata=metadata, patient_filter=e["patient_id"])
        print(f"{e['query_id']:<6} {e['patient_id']:<6} chunks={len(chunks)}  {e['query_text'][:55]}")