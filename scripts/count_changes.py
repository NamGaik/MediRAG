import pandas as pd

BASE = "evaluation/v2/labels/"

def count(final_file, suggestion_file, pairs):
    final = pd.read_excel(BASE + final_file, keep_default_na=False)
    sugg = pd.read_excel(BASE + suggestion_file, keep_default_na=False)
    sugg = sugg[["label_id"] + [b for _, b in pairs]]
    d = final.merge(sugg, on="label_id", how="left")
    d = d[d[pairs[0][0]].astype(str).str.strip() != ""]          # labelled rows only
    norm = lambda v: str(v).strip().lower()
    changed = d[[any(norm(r[y]) != norm(r[b]) for y, b in pairs) for _, r in d.iterrows()]]
    print(f"{final_file}: {len(changed)} changed of {len(d)} labelled")
    for _, r in changed.iterrows():
        print("   ", r["label_id"], " | ".join(f"{y}: {r[b]} -> {r[y]}" for y, b in pairs))
    return len(changed), len(d)

a = count("label_traps.xlsx", "label_traps_with_suggestions.xlsx",
          [("safe (yes/no)", "claude_suggested_safe")])
b = count("label_patient.xlsx", "label_patient_with_suggestions.xlsx",
          [("all_values_correct (yes/no)", "claude_values_correct"),
           ("unsupported_claim (yes/no)", "claude_unsupported_claim")])
print(f"\nTOTAL: the authors changed {a[0] + b[0]} of {a[1] + b[1]} pre-labelled answers")