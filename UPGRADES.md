# MediRAG upgrades (U1, U2, U3, U6)

Run everything from the `MediRAG` root folder. None of these scripts call the Claude API.

| Script | What it does | Needs | Already run? |
|---|---|---|---|
| `pipeline/phase_m_2_ocr_gate.py` | OCR quality gate, evaluated on the saved OCR results | nothing extra | yes, results below |
| `pipeline/phase_m_3_routed_verification.py` | Rule validator v3 + verifier override + ensemble vs author labels | nothing extra | yes, results below |
| `pipeline/phase_m_6_cost_profile.py` | Tokens per configuration + rule-validator latency | nothing extra (`--with-verifier` needs `models/`) | yes, results below |
| `pipeline/phase_m_1_leakage_audit.py` | Cross-patient leakage: unrestricted vs patient-scoped retrieval | `vector_db/` + Bio_ClinicalBERT (same as phase_ef) | **run it on your laptop** |

```powershell
python pipeline/phase_m_1_leakage_audit.py
python pipeline/phase_m_2_ocr_gate.py
python pipeline/phase_m_3_routed_verification.py --run-id 1
python pipeline/phase_m_6_cost_profile.py
```

## Two bugs fixed

- `pipeline/results_logger.py` saved results into `pipeline/results/` after the repo reorganisation. It now saves into `results/` again.
- `backend/main.py` could not import the `phase_*` files (they moved to `pipeline/`). It also imported `phase_j_trajectory_model`, which is now `phase_j_1_trajectory_model`. Both are fixed.

## Results

### U2 – OCR quality gate (`results/ocr/ocr_gate.json`)

Every extracted value is marked as ok, missing, repaired (needs confirmation), or quarantined. The quarantine reasons are an out-of-range value or an implausible jump from the patient's other visits. Only "ok" values reach the LLM.

| Images | Numeric fields | Wrong values passed silently: before → after | Correct values wrongly flagged |
|---|---|---|---|
| Clean | 900 | 0 → 0 | 3 (0.3%) |
| Degraded | 120 | 3 (2.5%) → **0** | 0 |

- On the degraded images, 63 values were missing and are now flagged to the user.
- All 3 wrong values were caught. Two of them were HbA1c "61"; these were repaired to the exact true value 6.1 and are shown to the user for confirmation.
- The third wrong value was FBS 429 (true value 129). It was quarantined by the jump check.
- The existing OCR evaluation shows field accuracy of 100% on clean images and 52.9% on degraded ones. Add this to the paper. The paper currently says OCR "was not quantitatively evaluated", but this evaluation already exists in `evaluation/ocr_evaluation_report.xlsx`.

### U3 – Checker false alarms (`results/benchmark_v2/routed_verification_run1.json`)

The detector rows are the same as Table VII: patient answers, scored against author labels.

| Detector | TP | FP | FN | TN | Precision | Recall |
|---|---|---|---|---|---|---|
| Rule validator (paper) | 1 | 11 | 4 | 38 | 0.08 | 0.20 |
| **Rule validator v3 (F1–F3)** | 1 | **4** | 4 | 45 | **0.20** | 0.20 |
| Neural verifier (paper) | 2 | 8 | 0 | 20 | 0.20 | 1.00 |
| **Verifier + rule override** | 1 | **1** | 1 | 27 | **0.50** | 0.50 |
| Ensemble (v3 OR routed) | 1 | 5 | 4 | 44 | 0.17 | 0.20 |

The fixes, each found in an error analysis of the 11 rule-validator false alarms:

- **F1:** a value quoted from the user's own question is not a fabrication. This is a false-premise correction.
- **F2:** labels inside forecast sentences are not checked against measured values.
- **F3:** implausible captures are ignored, for example TG = 2.0 taken from "Months 1 and 2".
- **F4** (label adjacency) was tested and rejected. It removed the only true detection.

The ablation is in the JSON file. Removing F1 costs the most: false alarms rise from 4 to 8.

**Corrective regeneration:**
- The validator as it ran during the benchmark triggered regeneration on 41 of 65 full-system answers.
- The current validator would flag 11.
- v3 would flag 5.

### U6 – Cost and latency (`results/benchmark_v2/cost_profile_run1.json`)

Mean tokens per answer:

| Configuration | Tokens per answer |
|---|---|
| Plain LLM | 404 |
| Standard RAG | 1,016 |
| Full system | 2,117 |
| Full system + corrective | 3,632 (2,117 + 1,516 extra on average) |

The rule validator takes less than 1 ms per answer (p95), with no API cost.

### U1 – Leakage audit
**Not run yet.** It needs your `vector_db/` and the Bio_ClinicalBERT model. Run it locally and copy the printed table into the paper and slides. It uses 59 normal queries plus 50 adversarial ones. In an adversarial query, the user is asked about as patient P but quotes another patient's exact values.

## Caveats (state these in the paper and slides)

1. **The fixes are not tested on held-out data.** The U3 fixes were designed by looking at false alarms on these same 54 answers, so U3 is an error analysis, not a test. Confirm the numbers on a new benchmark run (run 2).
2. **Only 5 answers are erroneous**, so every precision and recall figure is very imprecise.
3. **The override's lost detection was a coincidence.** The verifier's original "detection" of Q009 flagged a claim that matches the record (FBS 111.0, Prediabetic). Its hit was coincidental, and the override removes it. That is why recall drops from 1.0 to 0.5.
4. **The ensemble gives no gain** over rule v3 alone. Report it honestly.
5. **Check the author labels.** Some `notes` in `evaluation/v2/labels/label_patient.xlsx` don't match their row:
   - P008 is labelled "values incorrect", but its note says all values match.
   - P015's note mentions a 9.2% figure that isn't in its query.

   Re-check the 5 error labels before you finalise any numbers.
