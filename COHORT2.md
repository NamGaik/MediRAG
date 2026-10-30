# Cohort 2: setup (steps 1–2 of the improvement plan)

Cohort 2 has 100 patients × 8 monthly visits (800 reports) with seven trajectory types: normal stable, prediabetic stable, prediabetic progressing, diabetic improving, diabetic worsening, diabetic fluctuating, and diabetic with dyslipidemia.

**No API calls are needed for these steps.**

## Why a separate folder

The pipeline writes its outputs into fixed folders: `preprocessed/`, `vector_db/`, `models/`, `evaluation/`. Running cohort 2 inside your main `MediRAG` folder would overwrite cohort 1, and your paper's run 1 would no longer be reproducible.

So cohort 2 runs in its own **copy** of the project. Your main folder stays untouched.

## One-time setup (PowerShell)

```powershell
cd <folder that contains MediRAG>
# 1. copy the whole project (including the code changes from this zip)
Copy-Item -Recurse MediRAG MediRAG_cohort2
cd MediRAG_cohort2
..\.venv-1\Scripts\Activate.ps1

# 2. generate cohort 2
python pipeline/generate_cohort_v2.py

# 3. put cohort 2 where the pipeline expects the data (only in this copy!)
Copy-Item data\Synthetic_diabetes_dataset2.xlsx data\Synthetic_diabetes_dataset1.xlsx -Force
```

## Settings for 8 visits

Set these in **every** PowerShell window you use for the cohort-2 folder:

```powershell
$env:MEDIRAG_TOP_K = "8"          # give the LLM all 8 visits, not 5
$env:MEDIRAG_MAX_SEQ_LEN = "7"    # GRU uses up to 7 past visits, not 2
```

Without them, the code behaves exactly as it does for cohort 1 (top-k 5, 2-visit history).

## Build the pipeline for cohort 2

```powershell
python pipeline/excel_to_json_reports.py      # writes json_reports/ from the Excel file (no OCR)
python pipeline/phase_c_preprocessing.py      # expect: 800 chunks
python pipeline/phase_d_1_embedding.py
Remove-Item -Recurse -Force vector_db         # the copy still holds cohort 1's index -- delete it
python pipeline/phase_ef_vectorDB.py          # rebuilds the index: expect 'Built FAISS index with 800 vectors'
python pipeline/phase_j_1_trajectory_model.py # original GRU evaluation (as in the paper)
python pipeline/phase_j_3_trajectory_v2.py     # fairer evaluation: early stopping + extra baselines + per-type breakdown
```

`excel_to_json_reports.py` skips OCR. This is deliberate: OCR was evaluated on cohort 1, and cohort 2 tests generation and answer checking. If you want OCR on cohort 2 too, run `generate_reports.py`, then `convert_and_degrade.py`, then `ocr_extract_and_evaluate.py` instead.

If you run the backend in this folder, first delete `data\live_patient_snapshot.json` (it holds cohort 1's patients).

## What changed in the code (cohort-1 results unchanged)

| File | Change | Default (cohort 1) |
|---|---|---|
| `phase_g_generation.py`, `phase_l_6_benchmark_v2.py` | `TOP_K` read from `MEDIRAG_TOP_K` | 5 |
| `phase_j_1_trajectory_model.py` | `MAX_SEQ_LEN` read from `MEDIRAG_MAX_SEQ_LEN` | 2 |
| `phase_g_generation.py`, `backend/main.py` | forecast history uses `MAX_SEQ_LEN` instead of a fixed 2 | 2 |
| `phase_m_3_routed_verification.py`, `phase_m_10_error_injection.py` | read all of a patient's visits instead of exactly 3 | same result for 3 visits |
| new: `generate_cohort_v2.py`, `excel_to_json_reports.py` | cohort-2 data | — |

I re-ran `phase_m_3` and `phase_m_10` on cohort 1 after these changes, and every number was identical.

## Step 3: questions and traps (built)

```powershell
python pipeline/phase_l_9_cohort2_queries.py
```

This writes `verifier_data/cohort2_patient_queries.json` (49 questions, 7 per trajectory type) and `verifier_data/cohort2_trap_queries.json` (70 traps: the 10 original types and 4 new ones, 5 each). Every patient question stores **reference facts** computed from the record, to help with labelling.

To make the benchmark use them, set these two settings (together with the two above):

```powershell
$env:MEDIRAG_PATIENT_QUERIES = "verifier_data/cohort2_patient_queries.json"
$env:MEDIRAG_TRAP_QUERIES = "verifier_data/cohort2_trap_queries.json"
```

`phase_l_6_benchmark_v2.py` now also has `--pilot N`: it runs only N queries, spread across question and trap types, saves them to `evaluation/v2/pilot_<model>.json`, and prints the tokens used per query. **Do not run it yet.** The Haiku configuration comes first.

## Step 5: two models (built)

The benchmark now reads these settings:

| Setting | Meaning | Default (cohort 1) |
|---|---|---|
| `MEDIRAG_MODEL` | Claude model for the whole run | `claude-sonnet-5` |
| `MEDIRAG_CONFIGS` | which configurations, comma-separated | `plain_llm,standard_rag,full_system` |
| `MEDIRAG_CORRECTIVE` | `1` adds full system + corrective, `0` skips it | `1` |

Plan for cohort 2 (keeps the cost low):

- **Haiku 5.5:** all 4 configurations, all 119 queries. It is cheap, and a weaker model makes more natural errors.
- **Sonnet 5:** full system only, all 119 queries. This is the main model.

## Step 6: pilot (10 queries) -- check the cost before the full run

Use one PowerShell window in `MediRAG_cohort2`, and set all four cohort-2 settings first:

```powershell
$env:MEDIRAG_TOP_K = "8"
$env:MEDIRAG_MAX_SEQ_LEN = "7"
$env:MEDIRAG_PATIENT_QUERIES = "verifier_data/cohort2_patient_queries.json"
$env:MEDIRAG_TRAP_QUERIES = "verifier_data/cohort2_trap_queries.json"
```

**Pilot A, Haiku with all configurations (40 API calls):**

```powershell
$env:MEDIRAG_MODEL = "claude-haiku-5-5"
$env:MEDIRAG_CONFIGS = "plain_llm,standard_rag,full_system"
$env:MEDIRAG_CORRECTIVE = "1"
python pipeline/phase_l_6_benchmark_v2.py --pilot 10
```

**Pilot B, Sonnet with the full system only (10 API calls):**

```powershell
$env:MEDIRAG_MODEL = "claude-sonnet-5"
$env:MEDIRAG_CONFIGS = "full_system"
$env:MEDIRAG_CORRECTIVE = "0"
python pipeline/phase_l_6_benchmark_v2.py --pilot 10
```

After each pilot, note the printed "Per query" token counts, and check the **Cost** tab in the Anthropic console. Then scale by 119/10 to estimate the full run. Send both outputs before starting the full runs.

## Next steps (not yet built)

- The full runs (run 2 = Haiku, run 3 = Sonnet), then the label sheets for cohort 2.
