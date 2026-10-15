# MediRAG

**A trustworthy Retrieval-Augmented Generation framework for explainable lab report interpretation in Type 2 Diabetes.**

MediRAG reads a diabetes patient's lab report and answers questions about it in plain language. Answers are built only from the patient's own report values, checked against ADA 2024 and WHO thresholds by a rule validator, and checked claim-by-claim by a neural faithfulness verifier.

> **Note:** All data in this repository is synthetic. No real patient data is used. This is a research prototype and does not give medical advice.

---

## How it works

1. **Ingest** - lab reports (PDF / image, including deliberately degraded scans) are read with OCR.
2. **Preprocess** - units are normalised, duplicates and invalid records are removed, and each patient-month becomes one labelled text chunk.
3. **Embed and index** - chunks are embedded and stored in a FAISS vector index.
4. **Retrieve** - the question is embedded and the top 5 chunks for that patient are retrieved.
5. **Generate** - Claude (Anthropic API) writes the answer from the retrieved chunks, following an 8-rule grounding prompt, plus a labelled forecast from the trajectory model.
6. **Rule validation** - every biomarker value and label in the answer is checked against the ADA/WHO severity rules (R001-R019).
7. **Neural verification** - a fine-tuned BioClinicalBERT classifier checks each single-month claim against the matching report chunk and labels it faithful or hallucinated.
8. **Trajectory forecasting** - a small GRU predicts the next visit's HbA1c, FBS, PPBS and risk category from 1-2 months of history.
9. **Explainability** - Integrated Gradients for the GRU forecasts; [CLS] attention for the verifier.
10. **Benchmark** - patient queries and hallucination-trap queries are run through four configurations (below) and scored.

---

## Datasets

All datasets in `data/` are synthetic, with values generated to fall within ADA 2024 and WHO ranges.

| Dataset | Contents | Size |
| --- | --- | --- |
| I - Synthetic lab reports | HbA1c, FBS, PPBS, LDL, HDL, triglycerides, status and flag | 50 patients x 3 months = 150 reports |
| II - Reference ranges | Diagnostic thresholds, lipid ranges, treatment targets, 19 severity rules | 4 tables |
| III - Evaluation queries | 15 patient queries, 12 doctor queries, 10 trap queries | 37 queries |

The 10 trap queries are expanded to 50 (10 trap types x 5) by `phase_l_1_trap_expansion.py`.

| Biomarker | Normal | Prediabetes | Diabetes | Source |
| --- | --- | --- | --- | --- |
| HbA1c (%) | < 5.7 | 5.7-6.4 | >= 6.5 | ADA 2024 |
| FBS (mg/dL) | 70-99 | 100-125 | >= 126 | ADA 2024 |
| PPBS (mg/dL) | < 140 | 140-199 | >= 200 | WHO |

---

## Repository structure

```
MediRAG/
├── pipeline/          Main pipeline scripts, run in order (see below)
├── scripts/           Sanity checks and scripts that draw the paper's figures
├── data/              The three datasets
├── reports_pdf/       Generated report PDFs
├── reports_images/    Clean and degraded report images (OCR input)
├── json_reports/      Structured report records
├── preprocessed/      Cleaned records and per-patient-month chunks
├── verifier_data/     Verifier training pairs, trajectory sequences, expanded trap queries
├── evaluation/        Benchmark answers and scores
├── explainability/    Attribution and attention figures
├── results/           Saved metrics (JSON) used in the paper's tables
├── figures/           Figures used in the paper
├── backend/           FastAPI server
├── frontend/          React web app
└── archive/           Older script versions kept for reference
```

Not included (too large; recreated by running the pipeline): `vector_db/`, `embeddings/`, `models/` (the trained verifier and GRU).

---

## Setup

Requires Python <!-- TODO: version, e.g. 3.10 -->.

```bash
git clone https://github.com/NamGaik/MediRAG.git
cd MediRAG
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
```

Create a `.env` file in the project root with your Anthropic API key:

```
ANTHROPIC_API_KEY=your-key-here
```

The Claude model used is set by `CLAUDE_MODEL` in `pipeline/phase_g_generation.py`.

---

## Running the pipeline

Always run from the project root, e.g. `python pipeline/phase_c_preprocessing.py`.

| Step | Script | What it does |
| --- | --- | --- |
| A | `generate_reports.py` | Generates the synthetic lab reports |
| A | `convert_and_degrade.py` | <!-- TODO: one line --> |
| B | `ocr_extract_and_evaluate.py` | OCR on report images/PDFs and extraction accuracy |
| C | `phase_c_preprocessing.py` | Cleans records, normalises units, writes one chunk per patient-month |
| D | `phase_d_1_embedding.py` | Embeds the chunks |
| D | `phase_d_2_label_check.py` | Checks embeddings group chunks by clinical status even with all label text removed (MiniLM vs Bio_ClinicalBERT, same-patient and cross-patient nearest neighbour) |
| E-F | `phase_ef_vectorDB.py` | Builds the FAISS index; top-k retrieval with a patient filter |
| G | `phase_g_generation.py` | Generates answers with Claude using the grounding prompt |
| H | `phase_h_validation.py` | Rule-based validation against ADA/WHO severity rules |
| I | `phase_i_neural_verifier.py` | Builds synthetic faithful/hallucinated pairs and fine-tunes Bio_ClinicalBERT as a verifier (slow on CPU) |
| I | `phase_i_2_verifier_audit.py` | <!-- TODO: one line --> |
| J | `phase_j_1_trajectory_model.py` | Trains the next-visit GRU; 5-fold patient-grouped CV against a persistence baseline |
| J | `phase_j_2_baselines.py` | <!-- TODO: one line --> |
| K | `phase_k_explainability.py` | Integrated Gradients for the GRU (one patient and whole cohort); verifier attention |
| L | `phase_l_1_trap_expansion.py` | Expands the trap queries to 50 (10 types x 5) |
| L | `phase_l_6_benchmark_v2.py` | Main benchmark (see Evaluation). **Makes paid API calls - run with `--dry-run` first** |
| L | other `phase_l_*` scripts | <!-- TODO: say which are current and which are superseded --> |

Start the web app:

```bash
# TODO: backend start command, e.g. uvicorn backend.main:app --reload
# TODO: frontend start command, e.g. cd frontend && npm install && npm start
```

---

## Evaluation

The benchmark (`phase_l_6_benchmark_v2.py`) runs the 15 patient queries and 50 trap queries through four configurations, all using the same Claude model:

| Configuration | Description |
| --- | --- |
| `plain_llm` | Question only, no report context |
| `standard_rag` | Top-5 retrieved chunks plus a minimal "answer from the context" instruction |
| `full_system` | MediRAG grounding prompt + chunks + trajectory forecast |
| `full_system_corrective` | As `full_system`, but regenerated once if the rule validator finds a misclassification or possible fabrication |

The rule validator and neural verifier are then applied to every saved answer as detectors. Trap safety is scored automatically by keywords (secondary measure) and by human labelling (primary measure), with Wilson 95% confidence intervals. Results are saved to `evaluation/v2/`; repeat runs use `--run-id`.

Other evaluations: OCR extraction accuracy (phase B), label-stripped embedding check (D2), verifier validation metrics (I), and GRU vs persistence MAE and risk accuracy (J).

<!-- TODO: add final results tables once numbers are confirmed -->

---

## Team

Namrata Gaikwad, Nehal Kongwad, Sakshi Nikam
Department of Computer Engineering, Pimpri Chinchwad College of Engineering, Pune

Guide: Mrs. B. Mahalakshmi
