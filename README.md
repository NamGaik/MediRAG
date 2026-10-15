# MediRAG

**A trustworthy Retrieval-Augmented Generation framework for explainable lab report interpretation in Type 2 Diabetes.**

MediRAG reads a diabetes patient's lab report and answers questions about it in plain language. Answers are built only from the patient's own report values, then checked against ADA 2024 and WHO clinical thresholds before they are shown.

> **Note:** All data in this repository is synthetic. No real patient data is used. This is a research prototype and does not give medical advice.

---

## How it works

1. **Ingest** — a lab report (PDF, scan or image) is read with OCR and its results table is extracted.
2. **Preprocess** — units are normalised, noise is removed, and the text is split into labelled chunks.
3. **Embed and store** — each chunk is converted to a vector and stored in a vector database.
4. **Retrieve** — a user's question is embedded and the top 5 most similar chunks are retrieved (cosine similarity).
5. **Generate** — an LLM writes the answer using only the retrieved chunks.
6. **Validate** — a rule-based checker compares every value and label against ADA/WHO thresholds and flags mismatches.
7. **Verify, explain, evaluate** — <!-- TODO: one line on the neural verifier, trajectory model and explainability -->

---

## Datasets

All three datasets are in `data/` and are synthetic, with values generated to fall within ADA 2024 and WHO ranges.

| Dataset | Contents | Size |
| --- | --- | --- |
| I – Synthetic lab reports | HbA1c, FBS, PPBS, LDL, HDL, triglycerides, status and flag | 50 patients × 3 months = 150 reports |
| II – Reference ranges | Diagnostic thresholds, lipid ranges, treatment targets, 19 severity rules | 4 tables |
| III – Evaluation queries | Patient queries, doctor queries, hallucination-trap queries | 37 queries |

Thresholds used by the rule checker:

| Biomarker | Normal | Prediabetes | Diabetes | Source |
| --- | --- | --- | --- | --- |
| HbA1c (%) | < 5.7 | 5.7–6.4 | ≥ 6.5 | ADA 2024 |
| FBS (mg/dL) | 70–99 | 100–125 | ≥ 126 | ADA 2024 |
| PPBS (mg/dL) | < 140 | 140–199 | ≥ 200 | WHO |

---

## Repository structure

```
MediRAG/
├── pipeline/      Main pipeline scripts, run in order (see below)
├── scripts/       Sanity checks and scripts that generate the paper's figures
├── data/          Datasets and sample report PDFs/images
├── backend/       FastAPI server
├── frontend/      React web app
├── results/       Evaluation outputs
├── figures/       Figures used in the paper
├── docs/          Project overview and paper draft
└── archive/       Older versions kept for reference
```

---

## Setup

Requires Python <!-- TODO: version, e.g. 3.10 -->.

```bash
git clone <repo-url>
cd MediRAG
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
```

Create a `.env` file in the project root (see `.env.example`):

```
# TODO: list the variable names your code reads, e.g. the LLM API key name
```

---

## Running the pipeline

Run from the project root, in this order:

| Step | Script | What it does |
| --- | --- | --- |
| A | `pipeline/generate_reports.py` | Generates the synthetic lab reports |
| A | `pipeline/convert_and_degrade.py` | <!-- TODO: e.g. converts reports to PDF/image and adds scan noise --> |
| B | `pipeline/ocr_extract_and_evaluate.py` | Runs OCR on reports and measures extraction accuracy |
| C | `pipeline/phase_c_preprocessing.py` | Cleans, normalises units and chunks the text |
| D | `pipeline/phase_d_1_embedding.py` | Creates embeddings for each chunk |
| D | `pipeline/phase_d_2_label_check.py` | <!-- TODO --> |
| E–F | `pipeline/phase_ef_vectorDB.py` | Builds the vector database and retrieval |
| G | `pipeline/phase_g_generation.py` | Generates answers with the LLM |
| H | `pipeline/phase_h_validation.py` | Rule-based validation against ADA/WHO thresholds |
| I | `pipeline/phase_i_neural_verifier.py` | <!-- TODO --> |
| I | `pipeline/phase_i_2_verifier_audit.py` | <!-- TODO --> |
| J | `pipeline/phase_j_1_trajectory_model.py` | <!-- TODO --> |
| J | `pipeline/phase_j_2_baselines.py` | <!-- TODO --> |
| K | `pipeline/phase_k_explainability.py` | <!-- TODO --> |
| L | `pipeline/phase_l_*.py` | <!-- TODO: trap expansion, benchmark, rescoring; list the order --> |

Start the web app:

```bash
# TODO: backend start command, e.g. uvicorn backend.main:app --reload
# TODO: frontend start command, e.g. cd frontend && npm install && npm start
```

---

## Evaluation

| Level | Metrics |
| --- | --- |
| Retrieval | Precision@5, Recall@5 |
| Generation | Groundedness score, hallucination rate, response relevance |
| Clinical | Rule consistency, medical correctness |

<!-- TODO: add a results table once final numbers are confirmed -->

---

## Team

Namrata Gaikwad, Nehal Kongwad, Sakshi Nikam
Department of Computer Engineering, Pimpri Chinchwad College of Engineering, Pune

Guide: Mrs. B. Mahalakshmi
