# MediRAG results summary
Generated: 2026-10-03T12:02:15
Files found: 733


## data

### live_patient_snapshot.json
Original: `data\live_patient_snapshot.json`  |  Last modified: 2026-09-26 12:57

| key | value |
|---|---|
| new_patients.U-001.name | Priya Sharma |
| new_patients.U-001.age | 44 |
| new_patients.U-001.gender | Female |
| new_patients.U-001.password | 12344 |
| next_new_patient_number | 2 |

### uploaded_files_registry.json
Original: `data\uploaded_files_registry.json`  |  Last modified: 2026-09-26 12:57

JSON with 0 values (too large to show)

## embeddings

### embeddings_metadata.json
Original: `embeddings\embeddings_metadata.json`  |  Last modified: 2026-07-20 21:09

JSON list with 150 items

### model_comparison_report.json
Original: `embeddings\model_comparison_report.json`  |  Last modified: 2026-07-20 21:09

| key | value |
|---|---|
| MiniLM_a_same_patient_inclusive.check | same_patient_inclusive |
| MiniLM_a_same_patient_inclusive.model | MiniLM (all-MiniLM-L6-v2) |
| MiniLM_a_same_patient_inclusive.agreement_rate_percent | 98.67 |
| MiniLM_a_same_patient_inclusive.agreements | 148 |
| MiniLM_a_same_patient_inclusive.total | 150 |
| BioClinicalBERT_a_same_patient_inclusive.check | same_patient_inclusive |
| BioClinicalBERT_a_same_patient_inclusive.model | BioClinicalBERT |
| BioClinicalBERT_a_same_patient_inclusive.agreement_rate_percent | 100.0 |
| BioClinicalBERT_a_same_patient_inclusive.agreements | 150 |
| BioClinicalBERT_a_same_patient_inclusive.total | 150 |
| MiniLM_b_cross_patient.check | cross_patient |
| MiniLM_b_cross_patient.model | MiniLM (all-MiniLM-L6-v2) |
| MiniLM_b_cross_patient.agreement_rate_percent | 99.33 |
| MiniLM_b_cross_patient.agreements | 149 |
| MiniLM_b_cross_patient.total | 150 |
| BioClinicalBERT_b_cross_patient.check | cross_patient |
| BioClinicalBERT_b_cross_patient.model | BioClinicalBERT |
| BioClinicalBERT_b_cross_patient.agreement_rate_percent | 100.0 |
| BioClinicalBERT_b_cross_patient.agreements | 150 |
| BioClinicalBERT_b_cross_patient.total | 150 |
| MiniLM_c_label_stripped.check | same_patient_inclusive |
| MiniLM_c_label_stripped.model | MiniLM (label-stripped) |
| MiniLM_c_label_stripped.agreement_rate_percent | 98.67 |
| MiniLM_c_label_stripped.agreements | 148 |
| MiniLM_c_label_stripped.total | 150 |
| BioClinicalBERT_c_label_stripped.check | same_patient_inclusive |
| BioClinicalBERT_c_label_stripped.model | BioClinicalBERT (label-stripped) |
| BioClinicalBERT_c_label_stripped.agreement_rate_percent | 100.0 |
| BioClinicalBERT_c_label_stripped.agreements | 150 |
| BioClinicalBERT_c_label_stripped.total | 150 |

## evaluation

### benchmark_results.json
Original: `evaluation\benchmark_results.json`  |  Last modified: 2026-09-06 18:21

JSON with 0 values (too large to show)

### benchmark_results_final.json
Original: `evaluation\benchmark_results_final.json`  |  Last modified: 2026-09-09 13:14

JSON with 0 values (too large to show)

### benchmark_results_rescored.json
Original: `evaluation\benchmark_results_rescored.json`  |  Last modified: 2026-09-09 11:58

JSON with 0 values (too large to show)

### benchmark_summary.json
Original: `evaluation\benchmark_summary.json`  |  Last modified: 2026-09-06 18:21

| key | value |
|---|---|
| plain_llm.rule_flag_rate | None |
| plain_llm.trap_safety_rate | 0.35 |
| plain_llm.verifier_faithful_rate | None |
| standard_rag.rule_flag_rate | None |
| standard_rag.trap_safety_rate | 0.4 |
| standard_rag.verifier_faithful_rate | None |
| rag_with_rules.rule_flag_rate | 0.44 |
| rag_with_rules.trap_safety_rate | 0.45 |
| rag_with_rules.verifier_faithful_rate | None |
| full_system.rule_flag_rate | 0.4 |
| full_system.trap_safety_rate | 0.5 |
| full_system.verifier_faithful_rate | 0.0 |

### benchmark_summary_final.json
Original: `evaluation\benchmark_summary_final.json`  |  Last modified: 2026-09-09 13:14

| key | value |
|---|---|
| plain_llm.rule_flag_rate | 0.24 |
| plain_llm.trap_safety_rate | 0.35 |
| plain_llm.verifier_faithful_rate | None |
| standard_rag.rule_flag_rate | 0.28 |
| standard_rag.trap_safety_rate | 0.4 |
| standard_rag.verifier_faithful_rate | None |
| rag_with_rules.rule_flag_rate | 0.44 |
| rag_with_rules.trap_safety_rate | 0.45 |
| rag_with_rules.verifier_faithful_rate | None |
| full_system.rule_flag_rate | 0.4 |
| full_system.trap_safety_rate | 0.5 |
| full_system.verifier_faithful_rate | 0.857 |

### benchmark_summary_normalized.json
Original: `evaluation\benchmark_summary_normalized.json`  |  Last modified: 2026-09-09 13:21

| key | value |
|---|---|
| plain_llm.avg_issue_rate | 1.0 |
| plain_llm.coverage | 0.24 |
| plain_llm.n_answers_with_claims | 6 |
| plain_llm.n_total_answers | 25 |
| standard_rag.avg_issue_rate | 0.31 |
| standard_rag.coverage | 0.52 |
| standard_rag.n_answers_with_claims | 13 |
| standard_rag.n_total_answers | 25 |
| rag_with_rules.avg_issue_rate | 0.615 |
| rag_with_rules.coverage | 0.52 |
| rag_with_rules.n_answers_with_claims | 13 |
| rag_with_rules.n_total_answers | 25 |
| full_system.avg_issue_rate | 0.501 |
| full_system.coverage | 0.48 |
| full_system.n_answers_with_claims | 12 |
| full_system.n_total_answers | 25 |

### benchmark_summary_rescored.json
Original: `evaluation\benchmark_summary_rescored.json`  |  Last modified: 2026-09-09 11:58

| key | value |
|---|---|
| verifier_faithful_count | 6 |
| verifier_hallucinated_count | 1 |
| verifier_not_verifiable_count | 18 |
| verifier_faithful_rate | 0.857 |

### chart_trajectory_example.png
Original: `evaluation\chart_trajectory_example.png`  |  Last modified: 2026-10-03 12:00

Image / figure

### chart_trap_safety_ladder.png
Original: `evaluation\chart_trap_safety_ladder.png`  |  Last modified: 2026-09-11 09:44

Image / figure

### chart_verifier_comparison.png
Original: `evaluation\chart_verifier_comparison.png`  |  Last modified: 2026-09-11 09:48

Image / figure

### generation_samples.json
Original: `evaluation\generation_samples.json`  |  Last modified: 2026-09-05 11:03

JSON list with 3 items

### validation_report.json
Original: `evaluation\validation_report.json`  |  Last modified: 2026-09-03 15:01

JSON list with 2 items

## explainability

### trajectory_attribution_P032.png
Original: `explainability\trajectory_attribution_P032.png`  |  Last modified: 2026-10-03 11:45

Image / figure

### verifier_attention_faithful.png
Original: `explainability\verifier_attention_faithful.png`  |  Last modified: 2026-10-03 11:46

Image / figure

### verifier_attention_hallucinated.png
Original: `explainability\verifier_attention_hallucinated.png`  |  Last modified: 2026-10-03 11:46

Image / figure

## frontend

### package-lock.json
Original: `frontend\package-lock.json`  |  Last modified: 2026-09-09 14:50

JSON with 741 values (too large to show)

### package.json
Original: `frontend\package.json`  |  Last modified: 2026-09-09 14:45

| key | value |
|---|---|
| name | medirag-frontend |
| private | True |
| version | 0.1.0 |
| type | module |
| scripts.dev | vite |
| scripts.build | vite build |
| scripts.preview | vite preview |
| dependencies.react | ^18.3.1 |
| dependencies.react-dom | ^18.3.1 |
| devDependencies.@vitejs/plugin-react | ^4.3.1 |
| devDependencies.vite | ^5.4.0 |

## json_reports

### P001_Month_1_Clean.json
Original: `json_reports\P001_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:23

| key | value |
|---|---|
| Patient_ID | P001 |
| Month | Month_1 |
| HbA1c | 5.2 |
| FBS | 72 |
| PPBS | 107. |
| LDL | 77 |
| HDL | 57.0 |
| Triglycerides | 99.0 |

### P001_Month_2_Clean.json
Original: `json_reports\P001_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:23

| key | value |
|---|---|
| Patient_ID | P001 |
| Month | Month_2 |
| HbA1c | 5.4 |
| FBS | 74 |
| PPBS | 128 |
| LDL | 81 |
| HDL | 55.0 |
| Triglycerides | 107.0 |

### P001_Month_3_Clean.json
Original: `json_reports\P001_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:23

| key | value |
|---|---|
| Patient_ID | P001 |
| Month | Month_3 |
| HbA1c | 5.1 |
| FBS | 90 |
| PPBS | 94 |
| LDL | 82 |
| HDL | 59.0 |
| Triglycerides | 99.0 |

### P002_Month_1_Clean.json
Original: `json_reports\P002_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:23

| key | value |
|---|---|
| Patient_ID | P002 |
| Month | Month_1 |
| HbA1c | 5.3 |
| FBS | 93 |
| PPBS | 124 |
| LDL | 67 |
| HDL | 68.0 |
| Triglycerides | 136.0 |

### P002_Month_1_Degraded.json
Original: `json_reports\P002_Month_1_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P002 |
| Month | Month_1 |
| HbA1c | None |
| FBS | None |
| PPBS | None |
| LDL | None |
| HDL | None |
| Triglycerides | None |

### P002_Month_2_Clean.json
Original: `json_reports\P002_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:23

| key | value |
|---|---|
| Patient_ID | P002 |
| Month | Month_2 |
| HbA1c | 4.8 |
| FBS | 84 |
| PPBS | 98 |
| LDL | 62 |
| HDL | 68.0 |
| Triglycerides | 145.0 |

### P002_Month_2_Degraded.json
Original: `json_reports\P002_Month_2_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P002 |
| Month | Month_2 |
| HbA1c | None |
| FBS | None |
| PPBS | None |
| LDL | None |
| HDL | 68.0 |
| Triglycerides | 145.0 |

### P002_Month_3_Clean.json
Original: `json_reports\P002_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:23

| key | value |
|---|---|
| Patient_ID | P002 |
| Month | Month_3 |
| HbA1c | 5.5 |
| FBS | 75 |
| PPBS | 92 |
| LDL | 63 |
| HDL | 66.0 |
| Triglycerides | 137.0 |

### P002_Month_3_Degraded.json
Original: `json_reports\P002_Month_3_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P002 |
| Month | Month_3 |
| HbA1c | 5.5 |
| FBS | 75 |
| PPBS | 92 |
| LDL | 63 |
| HDL | 66.0 |
| Triglycerides | 137.0 |

### P003_Month_1_Clean.json
Original: `json_reports\P003_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:23

| key | value |
|---|---|
| Patient_ID | P003 |
| Month | Month_1 |
| HbA1c | 4.6 |
| FBS | 74 |
| PPBS | 103. |
| LDL | 76 |
| HDL | 66.0 |
| Triglycerides | 85.0 |

### P003_Month_2_Clean.json
Original: `json_reports\P003_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P003 |
| Month | Month_2 |
| HbA1c | 4.9 |
| FBS | 84 |
| PPBS | 124 |
| LDL | 81 |
| HDL | 63.0 |
| Triglycerides | 79.0 |

### P003_Month_3_Clean.json
Original: `json_reports\P003_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P003 |
| Month | Month_3 |
| HbA1c | 4.8 |
| FBS | 73 |
| PPBS | 124 |
| LDL | 76 |
| HDL | 64.0 |
| Triglycerides | 96.0 |

### P004_Month_1_Clean.json
Original: `json_reports\P004_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P004 |
| Month | Month_1 |
| HbA1c | 5.1 |
| FBS | 94 |
| PPBS | 131. |
| LDL | 96 |
| HDL | 63.0 |
| Triglycerides | 110.0 |

### P004_Month_2_Clean.json
Original: `json_reports\P004_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P004 |
| Month | Month_2 |
| HbA1c | 5.2 |
| FBS | 80 |
| PPBS | 122. |
| LDL | 101. |
| HDL | 63.0 |
| Triglycerides | 108.0 |

### P004_Month_3_Clean.json
Original: `json_reports\P004_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P004 |
| Month | Month_3 |
| HbA1c | 4.6 |
| FBS | 80 |
| PPBS | 95 |
| LDL | 99 |
| HDL | 60.0 |
| Triglycerides | 103.0 |

### P005_Month_1_Clean.json
Original: `json_reports\P005_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P005 |
| Month | Month_1 |
| HbA1c | 5 |
| FBS | 80 |
| PPBS | 90 |
| LDL | 72 |
| HDL | 63.0 |
| Triglycerides | 125.0 |

### P005_Month_2_Clean.json
Original: `json_reports\P005_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P005 |
| Month | Month_2 |
| HbA1c | 4.7 |
| FBS | 93 |
| PPBS | 99 |
| LDL | 73 |
| HDL | 61.0 |
| Triglycerides | 116.0 |

### P005_Month_3_Clean.json
Original: `json_reports\P005_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P005 |
| Month | Month_3 |
| HbA1c | 4.9 |
| FBS | 95 |
| PPBS | 92 |
| LDL | 72 |
| HDL | 66.0 |
| Triglycerides | 132.0 |

### P006_Month_1_Clean.json
Original: `json_reports\P006_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P006 |
| Month | Month_1 |
| HbA1c | 4.9 |
| FBS | 78 |
| PPBS | 111. |
| LDL | 68 |
| HDL | 52.0 |
| Triglycerides | 130.0 |

### P006_Month_2_Clean.json
Original: `json_reports\P006_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P006 |
| Month | Month_2 |
| HbA1c | 5.4 |
| FBS | 84 |
| PPBS | 129 |
| LDL | 69 |
| HDL | 49.0 |
| Triglycerides | 125.0 |

### P006_Month_3_Clean.json
Original: `json_reports\P006_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P006 |
| Month | Month_3 |
| HbA1c | 5.3 |
| FBS | 80 |
| PPBS | 116 |
| LDL | 69 |
| HDL | 55.0 |
| Triglycerides | 121.0 |

### P007_Month_1_Clean.json
Original: `json_reports\P007_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P007 |
| Month | Month_1 |
| HbA1c | 4.7 |
| FBS | 83 |
| PPBS | 128 |
| LDL | 78 |
| HDL | 51.0 |
| Triglycerides | 140.0 |

### P007_Month_2_Clean.json
Original: `json_reports\P007_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P007 |
| Month | Month_2 |
| HbA1c | 5.4 |
| FBS | 78 |
| PPBS | 102. |
| LDL | 76 |
| HDL | 48.0 |
| Triglycerides | 151.0 |

### P007_Month_2_Degraded.json
Original: `json_reports\P007_Month_2_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P007 |
| Month | Month_2 |
| HbA1c | None |
| FBS | None |
| PPBS | None |
| LDL | None |
| HDL | None |
| Triglycerides | None |

### P007_Month_3_Clean.json
Original: `json_reports\P007_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P007 |
| Month | Month_3 |
| HbA1c | 4.8 |
| FBS | 80 |
| PPBS | 103. |
| LDL | 79 |
| HDL | 53.0 |
| Triglycerides | 147.0 |

### P007_Month_3_Degraded.json
Original: `json_reports\P007_Month_3_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P007 |
| Month | Month_3 |
| HbA1c | 4.8 |
| FBS | 80 |
| PPBS | 103. |
| LDL | 79 |
| HDL | 53.0 |
| Triglycerides | 147.0 |

### P008_Month_1_Clean.json
Original: `json_reports\P008_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P008 |
| Month | Month_1 |
| HbA1c | 5.1 |
| FBS | 84 |
| PPBS | 95 |
| LDL | 97 |
| HDL | 59.0 |
| Triglycerides | 128.0 |

### P008_Month_2_Clean.json
Original: `json_reports\P008_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P008 |
| Month | Month_2 |
| HbA1c | 4.9 |
| FBS | 72 |
| PPBS | 97 |
| LDL | 93 |
| HDL | 60.0 |
| Triglycerides | 131.0 |

### P008_Month_3_Clean.json
Original: `json_reports\P008_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P008 |
| Month | Month_3 |
| HbA1c | 4.9 |
| FBS | 96 |
| PPBS | 106 |
| LDL | 95 |
| HDL | 58.0 |
| Triglycerides | 119.0 |

### P008_Month_3_Degraded.json
Original: `json_reports\P008_Month_3_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P008 |
| Month | Month_3 |
| HbA1c | None |
| FBS | None |
| PPBS | None |
| LDL | None |
| HDL | None |
| Triglycerides | None |

### P009_Month_1_Clean.json
Original: `json_reports\P009_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P009 |
| Month | Month_1 |
| HbA1c | 5.1 |
| FBS | 94 |
| PPBS | 94 |
| LDL | 64 |
| HDL | 57.0 |
| Triglycerides | 119.0 |

### P009_Month_2_Clean.json
Original: `json_reports\P009_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P009 |
| Month | Month_2 |
| HbA1c | 5.2 |
| FBS | 70 |
| PPBS | 123. |
| LDL | 60 |
| HDL | 59.0 |
| Triglycerides | 119.0 |

### P009_Month_2_Degraded.json
Original: `json_reports\P009_Month_2_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | None |
| Month | Month_2 |
| HbA1c | None |
| FBS | None |
| PPBS | None |
| LDL | None |
| HDL | None |
| Triglycerides | 119.0 |

### P009_Month_3_Clean.json
Original: `json_reports\P009_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P009 |
| Month | Month_3 |
| HbA1c | 5.2 |
| FBS | 91 |
| PPBS | 94 |
| LDL | 64 |
| HDL | 57.0 |
| Triglycerides | 131.0 |

### P010_Month_1_Clean.json
Original: `json_reports\P010_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P010 |
| Month | Month_1 |
| HbA1c | 5.5 |
| FBS | 79 |
| PPBS | 96 |
| LDL | 86 |
| HDL | 58.0 |
| Triglycerides | 140.0 |

### P010_Month_2_Clean.json
Original: `json_reports\P010_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P010 |
| Month | Month_2 |
| HbA1c | 4.9 |
| FBS | 74 |
| PPBS | 102. |
| LDL | 87 |
| HDL | 59.0 |
| Triglycerides | 130.0 |

### P010_Month_3_Clean.json
Original: `json_reports\P010_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P010 |
| Month | Month_3 |
| HbA1c | 4.9 |
| FBS | 77 |
| PPBS | 116 |
| LDL | 89 |
| HDL | 58.0 |
| Triglycerides | 155.0 |

### P011_Month_1_Clean.json
Original: `json_reports\P011_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P011 |
| Month | Month_1 |
| HbA1c | 6.1 |
| FBS | 112. |
| PPBS | 151 |
| LDL | 112. |
| HDL | 51.0 |
| Triglycerides | 165.0 |

### P011_Month_2_Clean.json
Original: `json_reports\P011_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P011 |
| Month | Month_2 |
| HbA1c | 6.3 |
| FBS | 126 |
| PPBS | 151 |
| LDL | 108 |
| HDL | 54.0 |
| Triglycerides | 179.0 |

### P011_Month_3_Clean.json
Original: `json_reports\P011_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P011 |
| Month | Month_3 |
| HbA1c | 5.8 |
| FBS | 105 |
| PPBS | 155 |
| LDL | 110 |
| HDL | 51.0 |
| Triglycerides | 174.0 |

### P011_Month_3_Degraded.json
Original: `json_reports\P011_Month_3_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P011 |
| Month | Month_3 |
| HbA1c | None |
| FBS | None |
| PPBS | None |
| LDL | None |
| HDL | None |
| Triglycerides | None |

### P012_Month_1_Clean.json
Original: `json_reports\P012_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P012 |
| Month | Month_1 |
| HbA1c | 6.1 |
| FBS | 123. |
| PPBS | 184 |
| LDL | 121. |
| HDL | 42.0 |
| Triglycerides | 190.0 |

### P012_Month_2_Clean.json
Original: `json_reports\P012_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P012 |
| Month | Month_2 |
| HbA1c | 6.3 |
| FBS | 107. |
| PPBS | 170 |
| LDL | 122. |
| HDL | 40.0 |
| Triglycerides | 184.0 |

### P012_Month_3_Clean.json
Original: `json_reports\P012_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P012 |
| Month | Month_3 |
| HbA1c | 6.1 |
| FBS | 99 |
| PPBS | 189 |
| LDL | 124 |
| HDL | 42.0 |
| Triglycerides | 181.0 |

### P013_Month_1_Clean.json
Original: `json_reports\P013_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P013 |
| Month | Month_1 |
| HbA1c | 6.1 |
| FBS | 118 |
| PPBS | 187 |
| LDL | 108 |
| HDL | 45.0 |
| Triglycerides | 181.0 |

### P013_Month_1_Degraded.json
Original: `json_reports\P013_Month_1_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P013 |
| Month | Month_1 |
| HbA1c | 61 |
| FBS | None |
| PPBS | None |
| LDL | None |
| HDL | None |
| Triglycerides | 181.0 |

### P013_Month_2_Clean.json
Original: `json_reports\P013_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P013 |
| Month | Month_2 |
| HbA1c | 6.1 |
| FBS | 109 |
| PPBS | 170 |
| LDL | 112. |
| HDL | 44.0 |
| Triglycerides | 195.0 |

### P013_Month_2_Degraded.json
Original: `json_reports\P013_Month_2_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P013 |
| Month | Month_2 |
| HbA1c | None |
| FBS | 109 |
| PPBS | None |
| LDL | 112 |
| HDL | 44.0 |
| Triglycerides | 195.0 |

### P013_Month_3_Clean.json
Original: `json_reports\P013_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P013 |
| Month | Month_3 |
| HbA1c | 6.2 |
| FBS | 122. |
| PPBS | 193. |
| LDL | 110 |
| HDL | 45.0 |
| Triglycerides | 179.0 |

### P014_Month_1_Clean.json
Original: `json_reports\P014_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P014 |
| Month | Month_1 |
| HbA1c | 5.9 |
| FBS | 121. |
| PPBS | 185 |
| LDL | 118 |
| HDL | 47.0 |
| Triglycerides | 195.0 |

### P014_Month_2_Clean.json
Original: `json_reports\P014_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P014 |
| Month | Month_2 |
| HbA1c | 6.2 |
| FBS | 125 |
| PPBS | 158 |
| LDL | 114. |
| HDL | 49.0 |
| Triglycerides | 194.0 |

### P014_Month_3_Clean.json
Original: `json_reports\P014_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P014 |
| Month | Month_3 |
| HbA1c | 5.8 |
| FBS | 108 |
| PPBS | 161. |
| LDL | 119 |
| HDL | 49.0 |
| Triglycerides | 189.0 |

### P015_Month_1_Clean.json
Original: `json_reports\P015_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P015 |
| Month | Month_1 |
| HbA1c | 5.9 |
| FBS | 102. |
| PPBS | 155 |
| LDL | 127 |
| HDL | 41.0 |
| Triglycerides | 172.0 |

### P015_Month_2_Clean.json
Original: `json_reports\P015_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P015 |
| Month | Month_2 |
| HbA1c | 6.1 |
| FBS | 100 |
| PPBS | 167 |
| LDL | 125 |
| HDL | 44.0 |
| Triglycerides | 175.0 |

### P015_Month_3_Clean.json
Original: `json_reports\P015_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P015 |
| Month | Month_3 |
| HbA1c | 5.9 |
| FBS | 114. |
| PPBS | 185 |
| LDL | 126 |
| HDL | 44.0 |
| Triglycerides | 174.0 |

### P016_Month_1_Clean.json
Original: `json_reports\P016_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P016 |
| Month | Month_1 |
| HbA1c | 5.9 |
| FBS | 103. |
| PPBS | 154 |
| LDL | 119 |
| HDL | 50.0 |
| Triglycerides | 165.0 |

### P016_Month_2_Clean.json
Original: `json_reports\P016_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P016 |
| Month | Month_2 |
| HbA1c | 6.2 |
| FBS | 117. |
| PPBS | 175 |
| LDL | 121. |
| HDL | 47.0 |
| Triglycerides | 167.0 |

### P016_Month_3_Clean.json
Original: `json_reports\P016_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P016 |
| Month | Month_3 |
| HbA1c | 5.9 |
| FBS | 119 |
| PPBS | 192. |
| LDL | 122. |
| HDL | 47.0 |
| Triglycerides | 167.0 |

### P016_Month_3_Degraded.json
Original: `json_reports\P016_Month_3_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P016 |
| Month | Month_3 |
| HbA1c | 5.9 |
| FBS | 119 |
| PPBS | 192. |
| LDL | 122. |
| HDL | 47.0 |
| Triglycerides | 167.0 |

### P017_Month_1_Clean.json
Original: `json_reports\P017_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P017 |
| Month | Month_1 |
| HbA1c | 6.1 |
| FBS | 113. |
| PPBS | 182. |
| LDL | 115 |
| HDL | 44.0 |
| Triglycerides | 168.0 |

### P017_Month_2_Clean.json
Original: `json_reports\P017_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P017 |
| Month | Month_2 |
| HbA1c | 6.3 |
| FBS | 121. |
| PPBS | 142 |
| LDL | 110 |
| HDL | 43.0 |
| Triglycerides | 170.0 |

### P017_Month_3_Clean.json
Original: `json_reports\P017_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P017 |
| Month | Month_3 |
| HbA1c | 5.9 |
| FBS | 116 |
| PPBS | 161. |
| LDL | 111. |
| HDL | 44.0 |
| Triglycerides | 158.0 |

### P018_Month_1_Clean.json
Original: `json_reports\P018_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P018 |
| Month | Month_1 |
| HbA1c | 5.8 |
| FBS | 124 |
| PPBS | 176 |
| LDL | 118 |
| HDL | 48.0 |
| Triglycerides | 189.0 |

### P018_Month_2_Clean.json
Original: `json_reports\P018_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P018 |
| Month | Month_2 |
| HbA1c | 6 |
| FBS | 99 |
| PPBS | 163 |
| LDL | 116 |
| HDL | 46.0 |
| Triglycerides | 179.0 |

### P018_Month_2_Degraded.json
Original: `json_reports\P018_Month_2_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P018 |
| Month | Month_2 |
| HbA1c | None |
| FBS | None |
| PPBS | None |
| LDL | None |
| HDL | None |
| Triglycerides | 179.0 |

### P018_Month_3_Clean.json
Original: `json_reports\P018_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P018 |
| Month | Month_3 |
| HbA1c | 6.1 |
| FBS | 106 |
| PPBS | 149 |
| LDL | 117. |
| HDL | 51.0 |
| Triglycerides | 190.0 |

### P018_Month_3_Degraded.json
Original: `json_reports\P018_Month_3_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P018 |
| Month | Month_3 |
| HbA1c | 61 |
| FBS | 106 |
| PPBS | 149 |
| LDL | 117. |
| HDL | 51.0 |
| Triglycerides | None |

### P019_Month_1_Clean.json
Original: `json_reports\P019_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P019 |
| Month | Month_1 |
| HbA1c | 6 |
| FBS | 119 |
| PPBS | 166 |
| LDL | 112. |
| HDL | 47.0 |
| Triglycerides | 160.0 |

### P019_Month_1_Degraded.json
Original: `json_reports\P019_Month_1_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | None |
| Month | None |
| HbA1c | None |
| FBS | 119 |
| PPBS | None |
| LDL | None |
| HDL | None |
| Triglycerides | None |

### P019_Month_2_Clean.json
Original: `json_reports\P019_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P019 |
| Month | Month_2 |
| HbA1c | 6 |
| FBS | 118 |
| PPBS | 188 |
| LDL | 116 |
| HDL | 44.0 |
| Triglycerides | 159.0 |

### P019_Month_3_Clean.json
Original: `json_reports\P019_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P019 |
| Month | Month_3 |
| HbA1c | 6 |
| FBS | 111. |
| PPBS | 166 |
| LDL | 111. |
| HDL | 50.0 |
| Triglycerides | 171.0 |

### P019_Month_3_Degraded.json
Original: `json_reports\P019_Month_3_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | None |
| Month | Month_3 |
| HbA1c | None |
| FBS | None |
| PPBS | None |
| LDL | None |
| HDL | None |
| Triglycerides | 177.0 |

### P020_Month_1_Clean.json
Original: `json_reports\P020_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P020 |
| Month | Month_1 |
| HbA1c | 6 |
| FBS | 103. |
| PPBS | 189 |
| LDL | 102. |
| HDL | 43.0 |
| Triglycerides | 161.0 |

### P020_Month_2_Clean.json
Original: `json_reports\P020_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P020 |
| Month | Month_2 |
| HbA1c | 6.2 |
| FBS | 106 |
| PPBS | 191. |
| LDL | 98 |
| HDL | 44.0 |
| Triglycerides | 171.0 |

### P020_Month_3_Clean.json
Original: `json_reports\P020_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P020 |
| Month | Month_3 |
| HbA1c | 5.9 |
| FBS | 114. |
| PPBS | 193. |
| LDL | 104. |
| HDL | 45.0 |
| Triglycerides | 155.0 |

### P020_Month_3_Degraded.json
Original: `json_reports\P020_Month_3_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P020 |
| Month | Month_3 |
| HbA1c | 5.9 |
| FBS | 114 |
| PPBS | 193 |
| LDL | None |
| HDL | 45.0 |
| Triglycerides | 155.0 |

### P021_Month_1_Clean.json
Original: `json_reports\P021_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P021 |
| Month | Month_1 |
| HbA1c | 6.1 |
| FBS | 122. |
| PPBS | 168 |
| LDL | 120 |
| HDL | 42.0 |
| Triglycerides | 176.0 |

### P021_Month_2_Clean.json
Original: `json_reports\P021_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P021 |
| Month | Month_2 |
| HbA1c | 6.1 |
| FBS | 129 |
| PPBS | 174. |
| LDL | 122. |
| HDL | 42.0 |
| Triglycerides | 179.0 |

### P021_Month_3_Clean.json
Original: `json_reports\P021_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P021 |
| Month | Month_3 |
| HbA1c | 6.2 |
| FBS | 118 |
| PPBS | 158 |
| LDL | 118 |
| HDL | 45.0 |
| Triglycerides | 180.0 |

### P022_Month_1_Clean.json
Original: `json_reports\P022_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P022 |
| Month | Month_1 |
| HbA1c | 5.9 |
| FBS | 115 |
| PPBS | 174. |
| LDL | 109 |
| HDL | 40.0 |
| Triglycerides | 195.0 |

### P022_Month_2_Clean.json
Original: `json_reports\P022_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P022 |
| Month | Month_2 |
| HbA1c | 6.2 |
| FBS | 121. |
| PPBS | 165 |
| LDL | 111. |
| HDL | 38.0 |
| Triglycerides | 196.0 |

### P022_Month_3_Clean.json
Original: `json_reports\P022_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P022 |
| Month | Month_3 |
| HbA1c | 6.2 |
| FBS | 106 |
| PPBS | 158 |
| LDL | 107. |
| HDL | 37.0 |
| Triglycerides | 192.0 |

### P023_Month_1_Clean.json
Original: `json_reports\P023_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P023 |
| Month | Month_1 |
| HbA1c | 7.1 |
| FBS | 143. |
| PPBS | 196 |
| LDL | 89 |
| HDL | 50.0 |
| Triglycerides | 193.0 |

### P023_Month_2_Clean.json
Original: `json_reports\P023_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P023 |
| Month | Month_2 |
| HbA1c | 7 |
| FBS | 132 |
| PPBS | 188 |
| LDL | 84 |
| HDL | 47.0 |
| Triglycerides | 192.0 |

### P023_Month_2_Degraded.json
Original: `json_reports\P023_Month_2_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | None |
| Month | Month_2 |
| HbA1c | None |
| FBS | None |
| PPBS | None |
| LDL | None |
| HDL | None |
| Triglycerides | 192.0 |

### P023_Month_3_Clean.json
Original: `json_reports\P023_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P023 |
| Month | Month_3 |
| HbA1c | 6.7 |
| FBS | 139 |
| PPBS | 171. |
| LDL | 89 |
| HDL | 50.0 |
| Triglycerides | 206.0 |

### P023_Month_3_Degraded.json
Original: `json_reports\P023_Month_3_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P023 |
| Month | Month_3 |
| HbA1c | 6.7 |
| FBS | 139 |
| PPBS | 171. |
| LDL | 89 |
| HDL | 50.0 |
| Triglycerides | 206.0 |

### P024_Month_1_Clean.json
Original: `json_reports\P024_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P024 |
| Month | Month_1 |
| HbA1c | 6.8 |
| FBS | 131. |
| PPBS | 189 |
| LDL | 82 |
| HDL | 45.0 |
| Triglycerides | 152.0 |

### P024_Month_2_Clean.json
Original: `json_reports\P024_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P024 |
| Month | Month_2 |
| HbA1c | 6.9 |
| FBS | 126 |
| PPBS | 186 |
| LDL | 82 |
| HDL | 42.0 |
| Triglycerides | 165.0 |

### P024_Month_3_Clean.json
Original: `json_reports\P024_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P024 |
| Month | Month_3 |
| HbA1c | 6.9 |
| FBS | 138 |
| PPBS | 167 |
| LDL | 85 |
| HDL | 46.0 |
| Triglycerides | 151.0 |

### P025_Month_1_Clean.json
Original: `json_reports\P025_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P025 |
| Month | Month_1 |
| HbA1c | 7.3 |
| FBS | 130 |
| PPBS | 194 |
| LDL | 83 |
| HDL | 46.0 |
| Triglycerides | 158.0 |

### P025_Month_2_Clean.json
Original: `json_reports\P025_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P025 |
| Month | Month_2 |
| HbA1c | 7.2 |
| FBS | 121. |
| PPBS | 170 |
| LDL | 80 |
| HDL | 45.0 |
| Triglycerides | 149.0 |

### P025_Month_3_Clean.json
Original: `json_reports\P025_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P025 |
| Month | Month_3 |
| HbA1c | 7.3 |
| FBS | 138 |
| PPBS | 174. |
| LDL | 82 |
| HDL | 46.0 |
| Triglycerides | 163.0 |

### P026_Month_1_Clean.json
Original: `json_reports\P026_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P026 |
| Month | Month_1 |
| HbA1c | 7.2 |
| FBS | 131. |
| PPBS | 194 |
| LDL | 84 |
| HDL | 40.0 |
| Triglycerides | 175.0 |

### P026_Month_2_Clean.json
Original: `json_reports\P026_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P026 |
| Month | Month_2 |
| HbA1c | 6.7 |
| FBS | 122. |
| PPBS | 156 |
| LDL | 80 |
| HDL | 41.0 |
| Triglycerides | 185.0 |

### P026_Month_3_Clean.json
Original: `json_reports\P026_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P026 |
| Month | Month_3 |
| HbA1c | 6.9 |
| FBS | 125 |
| PPBS | 165 |
| LDL | 85 |
| HDL | 41.0 |
| Triglycerides | 184.0 |

### P027_Month_1_Clean.json
Original: `json_reports\P027_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P027 |
| Month | Month_1 |
| HbA1c | 7.1 |
| FBS | 139 |
| PPBS | 195 |
| LDL | 72 |
| HDL | 47.0 |
| Triglycerides | 172.0 |

### P027_Month_2_Clean.json
Original: `json_reports\P027_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P027 |
| Month | Month_2 |
| HbA1c | 7 |
| FBS | 123. |
| PPBS | 187 |
| LDL | 71 |
| HDL | 48.0 |
| Triglycerides | 181.0 |

### P027_Month_3_Clean.json
Original: `json_reports\P027_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P027 |
| Month | Month_3 |
| HbA1c | 6.5 |
| FBS | 123. |
| PPBS | 172. |
| LDL | 75 |
| HDL | 44.0 |
| Triglycerides | 167.0 |

### P028_Month_1_Clean.json
Original: `json_reports\P028_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P028 |
| Month | Month_1 |
| HbA1c | 6.9 |
| FBS | 125 |
| PPBS | 185 |
| LDL | 91 |
| HDL | 41.0 |
| Triglycerides | 155.0 |

### P028_Month_2_Clean.json
Original: `json_reports\P028_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P028 |
| Month | Month_2 |
| HbA1c | 6.4 |
| FBS | 132 |
| PPBS | 183. |
| LDL | 87 |
| HDL | 43.0 |
| Triglycerides | 152.0 |

### P028_Month_3_Clean.json
Original: `json_reports\P028_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P028 |
| Month | Month_3 |
| HbA1c | 7.2 |
| FBS | 140 |
| PPBS | 170 |
| LDL | 88 |
| HDL | 38.0 |
| Triglycerides | 146.0 |

### P029_Month_1_Clean.json
Original: `json_reports\P029_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P029 |
| Month | Month_1 |
| HbA1c | 6.7 |
| FBS | 140 |
| PPBS | 167 |
| LDL | 77 |
| HDL | 49.0 |
| Triglycerides | 183.0 |

### P029_Month_1_Degraded.json
Original: `json_reports\P029_Month_1_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | None |
| Month | None |
| HbA1c | None |
| FBS | None |
| PPBS | None |
| LDL | None |
| HDL | None |
| Triglycerides | None |

### P029_Month_2_Clean.json
Original: `json_reports\P029_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P029 |
| Month | Month_2 |
| HbA1c | 6.5 |
| FBS | 127 |
| PPBS | 190 |
| LDL | 76 |
| HDL | 50.0 |
| Triglycerides | 190.0 |

### P029_Month_3_Clean.json
Original: `json_reports\P029_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P029 |
| Month | Month_3 |
| HbA1c | 6.8 |
| FBS | 123. |
| PPBS | 162 |
| LDL | 75 |
| HDL | 51.0 |
| Triglycerides | 191.0 |

### P030_Month_1_Clean.json
Original: `json_reports\P030_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P030 |
| Month | Month_1 |
| HbA1c | 7.2 |
| FBS | 139 |
| PPBS | 170 |
| LDL | 80 |
| HDL | 48.0 |
| Triglycerides | 182.0 |

### P030_Month_2_Clean.json
Original: `json_reports\P030_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P030 |
| Month | Month_2 |
| HbA1c | 6.8 |
| FBS | 117. |
| PPBS | 169 |
| LDL | 85 |
| HDL | 48.0 |
| Triglycerides | 180.0 |

### P030_Month_3_Clean.json
Original: `json_reports\P030_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P030 |
| Month | Month_3 |
| HbA1c | 6.6 |
| FBS | 137. |
| PPBS | 185 |
| LDL | 85 |
| HDL | 45.0 |
| Triglycerides | 177.0 |

### P031_Month_1_Clean.json
Original: `json_reports\P031_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P031 |
| Month | Month_1 |
| HbA1c | 7.3 |
| FBS | 127 |
| PPBS | 178 |
| LDL | 105 |
| HDL | 47.0 |
| Triglycerides | 179.0 |

### P031_Month_2_Clean.json
Original: `json_reports\P031_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P031 |
| Month | Month_2 |
| HbA1c | 6.6 |
| FBS | 138 |
| PPBS | 191. |
| LDL | 107. |
| HDL | 44.0 |
| Triglycerides | 179.0 |

### P031_Month_3_Clean.json
Original: `json_reports\P031_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P031 |
| Month | Month_3 |
| HbA1c | 6.6 |
| FBS | 121. |
| PPBS | 182. |
| LDL | 100 |
| HDL | 45.0 |
| Triglycerides | 185.0 |

### P032_Month_1_Clean.json
Original: `json_reports\P032_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:24

| key | value |
|---|---|
| Patient_ID | P032 |
| Month | Month_1 |
| HbA1c | 7.3 |
| FBS | 139 |
| PPBS | 174. |
| LDL | 91 |
| HDL | 44.0 |
| Triglycerides | 194.0 |

### P032_Month_2_Clean.json
Original: `json_reports\P032_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P032 |
| Month | Month_2 |
| HbA1c | 6.7 |
| FBS | 133. |
| PPBS | 181. |
| LDL | 93 |
| HDL | 41.0 |
| Triglycerides | 184.0 |

### P032_Month_3_Clean.json
Original: `json_reports\P032_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P032 |
| Month | Month_3 |
| HbA1c | 7.3 |
| FBS | 137. |
| PPBS | 175 |
| LDL | 89 |
| HDL | 47.0 |
| Triglycerides | 187.0 |

### P033_Month_1_Clean.json
Original: `json_reports\P033_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P033 |
| Month | Month_1 |
| HbA1c | 7 |
| FBS | 136 |
| PPBS | 195 |
| LDL | 100 |
| HDL | 39.0 |
| Triglycerides | 167.0 |

### P033_Month_2_Clean.json
Original: `json_reports\P033_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P033 |
| Month | Month_2 |
| HbA1c | 6.8 |
| FBS | 121. |
| PPBS | 163 |
| LDL | 102. |
| HDL | 39.0 |
| Triglycerides | 164.0 |

### P033_Month_3_Clean.json
Original: `json_reports\P033_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P033 |
| Month | Month_3 |
| HbA1c | 6.8 |
| FBS | 124 |
| PPBS | 178 |
| LDL | 96 |
| HDL | 38.0 |
| Triglycerides | 181.0 |

### P034_Month_1_Clean.json
Original: `json_reports\P034_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P034 |
| Month | Month_1 |
| HbA1c | 6.7 |
| FBS | 132 |
| PPBS | 163 |
| LDL | 109 |
| HDL | 46.0 |
| Triglycerides | 166.0 |

### P034_Month_2_Clean.json
Original: `json_reports\P034_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P034 |
| Month | Month_2 |
| HbA1c | 7 |
| FBS | 131. |
| PPBS | 174. |
| LDL | 106 |
| HDL | 46.0 |
| Triglycerides | 173.0 |

### P034_Month_3_Clean.json
Original: `json_reports\P034_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P034 |
| Month | Month_3 |
| HbA1c | 6.8 |
| FBS | 130 |
| PPBS | 190 |
| LDL | 107. |
| HDL | 47.0 |
| Triglycerides | 168.0 |

### P035_Month_1_Clean.json
Original: `json_reports\P035_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P035 |
| Month | Month_1 |
| HbA1c | 7 |
| FBS | 122. |
| PPBS | 166 |
| LDL | 75 |
| HDL | 41.0 |
| Triglycerides | 156.0 |

### P035_Month_2_Clean.json
Original: `json_reports\P035_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P035 |
| Month | Month_2 |
| HbA1c | 6.6 |
| FBS | 127 |
| PPBS | 156 |
| LDL | 76 |
| HDL | 43.0 |
| Triglycerides | 171.0 |

### P035_Month_3_Clean.json
Original: `json_reports\P035_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P035 |
| Month | Month_3 |
| HbA1c | 7.1 |
| FBS | 123. |
| PPBS | 185 |
| LDL | 71 |
| HDL | 44.0 |
| Triglycerides | 160.0 |

### P035_Month_3_Degraded.json
Original: `json_reports\P035_Month_3_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P035 |
| Month | Month_3 |
| HbA1c | None |
| FBS | 123 |
| PPBS | 185 |
| LDL | None |
| HDL | 44.0 |
| Triglycerides | None |

### P036_Month_1_Clean.json
Original: `json_reports\P036_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P036 |
| Month | Month_1 |
| HbA1c | 7.2 |
| FBS | 132 |
| PPBS | 166 |
| LDL | 104. |
| HDL | 41.0 |
| Triglycerides | 169.0 |

### P036_Month_1_Degraded.json
Original: `json_reports\P036_Month_1_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P036 |
| Month | Month_1 |
| HbA1c | None |
| FBS | None |
| PPBS | None |
| LDL | None |
| HDL | None |
| Triglycerides | 169.0 |

### P036_Month_2_Clean.json
Original: `json_reports\P036_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P036 |
| Month | Month_2 |
| HbA1c | 6.4 |
| FBS | 134 |
| PPBS | 153. |
| LDL | 103. |
| HDL | 40.0 |
| Triglycerides | 178.0 |

### P036_Month_3_Clean.json
Original: `json_reports\P036_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P036 |
| Month | Month_3 |
| HbA1c | 7.1 |
| FBS | 139 |
| PPBS | 160 |
| LDL | 106 |
| HDL | 44.0 |
| Triglycerides | 176.0 |

### P037_Month_1_Clean.json
Original: `json_reports\P037_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P037 |
| Month | Month_1 |
| HbA1c | 7 |
| FBS | 128 |
| PPBS | 196 |
| LDL | 80 |
| HDL | 49.0 |
| Triglycerides | 188.0 |

### P037_Month_2_Clean.json
Original: `json_reports\P037_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P037 |
| Month | Month_2 |
| HbA1c | 6.5 |
| FBS | 122. |
| PPBS | 174. |
| LDL | 82 |
| HDL | 47.0 |
| Triglycerides | 200.0 |

### P037_Month_3_Clean.json
Original: `json_reports\P037_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P037 |
| Month | Month_3 |
| HbA1c | 6.7 |
| FBS | 119 |
| PPBS | 159 |
| LDL | 77 |
| HDL | 47.0 |
| Triglycerides | 194.0 |

### P038_Month_1_Clean.json
Original: `json_reports\P038_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P038 |
| Month | Month_1 |
| HbA1c | 7 |
| FBS | 129 |
| PPBS | 192. |
| LDL | 98 |
| HDL | 41.0 |
| Triglycerides | 158.0 |

### P038_Month_1_Degraded.json
Original: `json_reports\P038_Month_1_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P038 |
| Month | Month_1 |
| HbA1c | None |
| FBS | 429 |
| PPBS | None |
| LDL | None |
| HDL | 41.0 |
| Triglycerides | 158.0 |

### P038_Month_2_Clean.json
Original: `json_reports\P038_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P038 |
| Month | Month_2 |
| HbA1c | 6.7 |
| FBS | 138 |
| PPBS | 168 |
| LDL | 100 |
| HDL | 42.0 |
| Triglycerides | 152.0 |

### P038_Month_3_Clean.json
Original: `json_reports\P038_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P038 |
| Month | Month_3 |
| HbA1c | 6.7 |
| FBS | 138 |
| PPBS | 174. |
| LDL | 103. |
| HDL | 42.0 |
| Triglycerides | 153.0 |

### P039_Month_1_Clean.json
Original: `json_reports\P039_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P039 |
| Month | Month_1 |
| HbA1c | 7.9 |
| FBS | 207. |
| PPBS | 247 |
| LDL | 159 |
| HDL | 36.0 |
| Triglycerides | 321.0 |

### P039_Month_2_Clean.json
Original: `json_reports\P039_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P039 |
| Month | Month_2 |
| HbA1c | 8 |
| FBS | 205 |
| PPBS | 281 |
| LDL | 157 |
| HDL | 36.0 |
| Triglycerides | 326.0 |

### P039_Month_3_Clean.json
Original: `json_reports\P039_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P039 |
| Month | Month_3 |
| HbA1c | 8.1 |
| FBS | 204 |
| PPBS | 275 |
| LDL | 164. |
| HDL | 36.0 |
| Triglycerides | 319.0 |

### P040_Month_1_Clean.json
Original: `json_reports\P040_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P040 |
| Month | Month_1 |
| HbA1c | 10.1 |
| FBS | 158 |
| PPBS | 288 |
| LDL | 173. |
| HDL | 40.0 |
| Triglycerides | 227.0 |

### P040_Month_2_Clean.json
Original: `json_reports\P040_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P040 |
| Month | Month_2 |
| HbA1c | 7.7 |
| FBS | 243. |
| PPBS | 316 |
| LDL | 171. |
| HDL | 41.0 |
| Triglycerides | 242.0 |

### P040_Month_3_Clean.json
Original: `json_reports\P040_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P040 |
| Month | Month_3 |
| HbA1c | 8.8 |
| FBS | 243. |
| PPBS | 230 |
| LDL | 178 |
| HDL | 37.0 |
| Triglycerides | 237.0 |

### P040_Month_3_Degraded.json
Original: `json_reports\P040_Month_3_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P040 |
| Month | Month_3 |
| HbA1c | None |
| FBS | None |
| PPBS | None |
| LDL | None |
| HDL | None |
| Triglycerides | None |

### P041_Month_1_Clean.json
Original: `json_reports\P041_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P041 |
| Month | Month_1 |
| HbA1c | 7.8 |
| FBS | 245 |
| PPBS | 245 |
| LDL | 183. |
| HDL | 31.0 |
| Triglycerides | 265.0 |

### P041_Month_2_Clean.json
Original: `json_reports\P041_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P041 |
| Month | Month_2 |
| HbA1c | 9.7 |
| FBS | 188 |
| PPBS | 262 |
| LDL | 183. |
| HDL | 33.0 |
| Triglycerides | 268.0 |

### P041_Month_3_Clean.json
Original: `json_reports\P041_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P041 |
| Month | Month_3 |
| HbA1c | 8.2 |
| FBS | 172. |
| PPBS | 276 |
| LDL | 182. |
| HDL | 34.0 |
| Triglycerides | 270.0 |

### P042_Month_1_Clean.json
Original: `json_reports\P042_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P042 |
| Month | Month_1 |
| HbA1c | 8.2 |
| FBS | 220 |
| PPBS | 259 |
| LDL | 140 |
| HDL | 36.0 |
| Triglycerides | 248.0 |

### P042_Month_2_Clean.json
Original: `json_reports\P042_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P042 |
| Month | Month_2 |
| HbA1c | 10.5 |
| FBS | 186 |
| PPBS | 296 |
| LDL | 138 |
| HDL | 39.0 |
| Triglycerides | 259.0 |

### P042_Month_3_Clean.json
Original: `json_reports\P042_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P042 |
| Month | Month_3 |
| HbA1c | 9.7 |
| FBS | 210 |
| PPBS | 276 |
| LDL | 142 |
| HDL | 35.0 |
| Triglycerides | 259.0 |

### P043_Month_1_Clean.json
Original: `json_reports\P043_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P043 |
| Month | Month_1 |
| HbA1c | 8.4 |
| FBS | 183. |
| PPBS | 211. |
| LDL | 160 |
| HDL | 38.0 |
| Triglycerides | 227.0 |

### P043_Month_1_Degraded.json
Original: `json_reports\P043_Month_1_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P043 |
| Month | Month_14 |
| HbA1c | None |
| FBS | None |
| PPBS | None |
| LDL | None |
| HDL | None |
| Triglycerides | None |

### P043_Month_2_Clean.json
Original: `json_reports\P043_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P043 |
| Month | Month_2 |
| HbA1c | 9.7 |
| FBS | 187 |
| PPBS | 286 |
| LDL | 155 |
| HDL | 39.0 |
| Triglycerides | 234.0 |

### P043_Month_3_Clean.json
Original: `json_reports\P043_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P043 |
| Month | Month_3 |
| HbA1c | 8.8 |
| FBS | 234 |
| PPBS | 243. |
| LDL | 156 |
| HDL | 36.0 |
| Triglycerides | 218.0 |

### P044_Month_1_Clean.json
Original: `json_reports\P044_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P044 |
| Month | Month_1 |
| HbA1c | 7.7 |
| FBS | 221 |
| PPBS | 203 |
| LDL | 137. |
| HDL | 33.0 |
| Triglycerides | 244.0 |

### P044_Month_2_Clean.json
Original: `json_reports\P044_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P044 |
| Month | Month_2 |
| HbA1c | 10.6 |
| FBS | 189 |
| PPBS | 272 |
| LDL | 139 |
| HDL | 32.0 |
| Triglycerides | 255.0 |

### P044_Month_3_Clean.json
Original: `json_reports\P044_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P044 |
| Month | Month_3 |
| HbA1c | 10.5 |
| FBS | 247 |
| PPBS | 274 |
| LDL | 139 |
| HDL | 34.0 |
| Triglycerides | 247.0 |

### P044_Month_3_Degraded.json
Original: `json_reports\P044_Month_3_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P044 |
| Month | Month_3 |
| HbA1c | None |
| FBS | 247 |
| PPBS | None |
| LDL | None |
| HDL | None |
| Triglycerides | None |

### P045_Month_1_Clean.json
Original: `json_reports\P045_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P045 |
| Month | Month_1 |
| HbA1c | 8.8 |
| FBS | 213 |
| PPBS | 229 |
| LDL | 187 |
| HDL | 36.0 |
| Triglycerides | 217.0 |

### P045_Month_2_Clean.json
Original: `json_reports\P045_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P045 |
| Month | Month_2 |
| HbA1c | 10.4 |
| FBS | 189 |
| PPBS | 212 |
| LDL | 183. |
| HDL | 38.0 |
| Triglycerides | 218.0 |

### P045_Month_3_Clean.json
Original: `json_reports\P045_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P045 |
| Month | Month_3 |
| HbA1c | 9.2 |
| FBS | 235 |
| PPBS | 261 |
| LDL | 183. |
| HDL | 38.0 |
| Triglycerides | 213.0 |

### P046_Month_1_Clean.json
Original: `json_reports\P046_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P046 |
| Month | Month_1 |
| HbA1c | 8.1 |
| FBS | 152 |
| PPBS | 251 |
| LDL | 148 |
| HDL | 37.0 |
| Triglycerides | 275.0 |

### P046_Month_2_Clean.json
Original: `json_reports\P046_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P046 |
| Month | Month_2 |
| HbA1c | 9.8 |
| FBS | 241. |
| PPBS | 205 |
| LDL | 144 |
| HDL | 40.0 |
| Triglycerides | 289.0 |

### P046_Month_2_Degraded.json
Original: `json_reports\P046_Month_2_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | None |
| Month | None |
| HbA1c | None |
| FBS | None |
| PPBS | None |
| LDL | None |
| HDL | None |
| Triglycerides | None |

### P046_Month_3_Clean.json
Original: `json_reports\P046_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P046 |
| Month | Month_3 |
| HbA1c | 9.4 |
| FBS | 236 |
| PPBS | 229 |
| LDL | 147. |
| HDL | 40.0 |
| Triglycerides | 269.0 |

### P047_Month_1_Clean.json
Original: `json_reports\P047_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P047 |
| Month | Month_1 |
| HbA1c | 8.8 |
| FBS | 245 |
| PPBS | 273 |
| LDL | 174 |
| HDL | 37.0 |
| Triglycerides | 241.0 |

### P047_Month_2_Clean.json
Original: `json_reports\P047_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P047 |
| Month | Month_2 |
| HbA1c | 10.7 |
| FBS | 216 |
| PPBS | 233 |
| LDL | 169 |
| HDL | 36.0 |
| Triglycerides | 256.0 |

### P047_Month_2_Degraded.json
Original: `json_reports\P047_Month_2_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | None |
| Month | None |
| HbA1c | None |
| FBS | None |
| PPBS | None |
| LDL | None |
| HDL | None |
| Triglycerides | None |

### P047_Month_3_Clean.json
Original: `json_reports\P047_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P047 |
| Month | Month_3 |
| HbA1c | 9.9 |
| FBS | 233 |
| PPBS | 246 |
| LDL | 170 |
| HDL | 37.0 |
| Triglycerides | 245.0 |

### P048_Month_1_Clean.json
Original: `json_reports\P048_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P048 |
| Month | Month_1 |
| HbA1c | 8.2 |
| FBS | 179 |
| PPBS | 209 |
| LDL | 169 |
| HDL | 38.0 |
| Triglycerides | 217.0 |

### P048_Month_2_Clean.json
Original: `json_reports\P048_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P048 |
| Month | Month_2 |
| HbA1c | 9.9 |
| FBS | 231 |
| PPBS | 273 |
| LDL | 174 |
| HDL | 39.0 |
| Triglycerides | 216.0 |

### P048_Month_3_Clean.json
Original: `json_reports\P048_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P048 |
| Month | Month_3 |
| HbA1c | 9 |
| FBS | 162 |
| PPBS | 223 |
| LDL | 165 |
| HDL | 35.0 |
| Triglycerides | 217.0 |

### P048_Month_3_Degraded.json
Original: `json_reports\P048_Month_3_Degraded.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P048 |
| Month | Month_3 |
| HbA1c | 9 |
| FBS | 162 |
| PPBS | 223 |
| LDL | 165 |
| HDL | 35.0 |
| Triglycerides | 217.0 |

### P049_Month_1_Clean.json
Original: `json_reports\P049_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P049 |
| Month | Month_1 |
| HbA1c | 9.8 |
| FBS | 159 |
| PPBS | 208 |
| LDL | 169 |
| HDL | 37.0 |
| Triglycerides | 330.0 |

### P049_Month_2_Clean.json
Original: `json_reports\P049_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P049 |
| Month | Month_2 |
| HbA1c | 9.5 |
| FBS | 165 |
| PPBS | 225 |
| LDL | 173. |
| HDL | 38.0 |
| Triglycerides | 329.0 |

### P049_Month_3_Clean.json
Original: `json_reports\P049_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P049 |
| Month | Month_3 |
| HbA1c | 9 |
| FBS | 237 |
| PPBS | 263 |
| LDL | 170 |
| HDL | 37.0 |
| Triglycerides | 327.0 |

### P050_Month_1_Clean.json
Original: `json_reports\P050_Month_1_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P050 |
| Month | Month_1 |
| HbA1c | 10.3 |
| FBS | 219 |
| PPBS | 222 |
| LDL | 135 |
| HDL | 38.0 |
| Triglycerides | 222.0 |

### P050_Month_2_Clean.json
Original: `json_reports\P050_Month_2_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P050 |
| Month | Month_2 |
| HbA1c | 8.9 |
| FBS | 213 |
| PPBS | 259 |
| LDL | 132 |
| HDL | 40.0 |
| Triglycerides | 227.0 |

### P050_Month_3_Clean.json
Original: `json_reports\P050_Month_3_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P050 |
| Month | Month_3 |
| HbA1c | 7.9 |
| FBS | 164 |
| PPBS | 214 |
| LDL | 139 |
| HDL | 39.0 |
| Triglycerides | 229.0 |

### Poorly-Controlled_P039-P050_Clean.json
Original: `json_reports\Poorly-Controlled_P039-P050_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | P000 |
| Month | None |
| HbA1c | 7.6 |
| FBS | 152 |
| PPBS | 202 |
| LDL | None |
| HDL | None |
| Triglycerides | None |

### Prediabetic_P011-P022_Clean.json
Original: `json_reports\Prediabetic_P011-P022_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | None |
| Month | None |
| HbA1c | 5.7 |
| FBS | 101 |
| PPBS | 141 |
| LDL | None |
| HDL | None |
| Triglycerides | None |

### Prediabetic_P011-P022_Degraded.json
Original: `json_reports\Prediabetic_P011-P022_Degraded.json`  |  Last modified: 2026-06-20 18:26

| key | value |
|---|---|
| Patient_ID | None |
| Month | None |
| HbA1c | None |
| FBS | 101 |
| PPBS | None |
| LDL | None |
| HDL | None |
| Triglycerides | None |

### Well-Controlled_P023-P038_Clean.json
Original: `json_reports\Well-Controlled_P023-P038_Clean.json`  |  Last modified: 2026-06-20 18:25

| key | value |
|---|---|
| Patient_ID | None |
| Month | None |
| HbA1c | 6.5 |
| FBS | 122 |
| PPBS | 162 |
| LDL | None |
| HDL | None |
| Triglycerides | None |

## models\trajectory

### cv_results.json
Original: `models\trajectory\cv_results.json`  |  Last modified: 2026-10-03 11:34

| key | value |
|---|---|
| setup.num_samples | 100 |
| setup.num_patients | 50 |
| setup.num_folds | 5 |
| setup.split | GroupKFold by Patient_ID |
| setup.predict_change | True |
| setup.epochs | 60 |
| setup.hidden_size | 16 |
| setup.learning_rate | 0.005 |
| gru.HbA1c(%)_MAE.mean | 0.4764 |
| gru.HbA1c(%)_MAE.std | 0.1104 |
| gru.FBS (mg/dL)_MAE.mean | 13.935 |
| gru.FBS (mg/dL)_MAE.std | 3.2681 |
| gru.PPBS (mg/dL)_MAE.mean | 19.7936 |
| gru.PPBS (mg/dL)_MAE.std | 2.9343 |
| gru.risk_accuracy.mean | 0.94 |
| gru.risk_accuracy.std | 0.0583 |
| gru.risk_macro_f1.mean | 0.9327 |
| gru.risk_macro_f1.std | 0.0668 |
| persistence_baseline.HbA1c(%)_MAE.mean | 0.5 |
| persistence_baseline.HbA1c(%)_MAE.std | 0.1152 |
| persistence_baseline.FBS (mg/dL)_MAE.mean | 15.08 |
| persistence_baseline.FBS (mg/dL)_MAE.std | 2.172 |
| persistence_baseline.PPBS (mg/dL)_MAE.mean | 19.88 |
| persistence_baseline.PPBS (mg/dL)_MAE.std | 2.2121 |
| persistence_baseline.risk_accuracy.mean | 0.96 |
| persistence_baseline.risk_accuracy.std | 0.08 |
| persistence_baseline.risk_macro_f1.mean | 0.9556 |
| persistence_baseline.risk_macro_f1.std | 0.0889 |

### model_config.json
Original: `models\trajectory\model_config.json`  |  Last modified: 2026-10-03 11:34

| key | value |
|---|---|
| predict_change | True |
| padding | post |

## models\verifier

### eval_results.json
Original: `models\verifier\eval_results.json`  |  Last modified: 2026-09-09 03:40

| key | value |
|---|---|
| eval_loss | 0.0872 |
| eval_accuracy | 0.9792 |
| eval_precision | 0.9365 |
| eval_recall | 0.9833 |
| eval_f1 | 0.9593 |
| eval_runtime | 578.3315 |
| eval_samples_per_second | 1.245 |
| eval_steps_per_second | 0.156 |
| epoch | 3.0 |

## preprocessed\chunks

### P001_Month_1.txt
Original: `preprocessed\chunks\P001_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P001 (Male, age 28) -- Month 1.

HbA1c: 5.2% (Classification: Normal).
Fasting Blood Sugar (FBS): 72.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 107.0 mg/dL (Classification: Normal).
LDL Cholesterol: 77.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 57.0 mg/dL (Classification: Normal).
Triglycerides: 99.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P001_Month_2.txt
Original: `preprocessed\chunks\P001_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P001 (Male, age 28) -- Month 2.

HbA1c: 5.4% (Classification: Normal).
Fasting Blood Sugar (FBS): 74.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 128.0 mg/dL (Classification: Normal).
LDL Cholesterol: 81.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 55.0 mg/dL (Classification: Normal).
Triglycerides: 107.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P001_Month_3.txt
Original: `preprocessed\chunks\P001_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P001 (Male, age 28) -- Month 3.

HbA1c: 5.1% (Classification: Normal).
Fasting Blood Sugar (FBS): 90.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 94.0 mg/dL (Classification: Normal).
LDL Cholesterol: 82.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 59.0 mg/dL (Classification: Normal).
Triglycerides: 99.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P002_Month_1.txt
Original: `preprocessed\chunks\P002_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P002 (Female, age 34) -- Month 1.

HbA1c: 5.3% (Classification: Normal).
Fasting Blood Sugar (FBS): 93.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 124.0 mg/dL (Classification: Normal).
LDL Cholesterol: 67.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 68.0 mg/dL (Classification: Normal).
Triglycerides: 136.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P002_Month_2.txt
Original: `preprocessed\chunks\P002_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P002 (Female, age 34) -- Month 2.

HbA1c: 4.8% (Classification: Normal).
Fasting Blood Sugar (FBS): 84.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 98.0 mg/dL (Classification: Normal).
LDL Cholesterol: 62.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 68.0 mg/dL (Classification: Normal).
Triglycerides: 145.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P002_Month_3.txt
Original: `preprocessed\chunks\P002_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P002 (Female, age 34) -- Month 3.

HbA1c: 5.5% (Classification: Normal).
Fasting Blood Sugar (FBS): 75.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 92.0 mg/dL (Classification: Normal).
LDL Cholesterol: 63.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 66.0 mg/dL (Classification: Normal).
Triglycerides: 137.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P003_Month_1.txt
Original: `preprocessed\chunks\P003_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P003 (Male, age 41) -- Month 1.

HbA1c: 4.6% (Classification: Normal).
Fasting Blood Sugar (FBS): 74.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 103.0 mg/dL (Classification: Normal).
LDL Cholesterol: 76.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 66.0 mg/dL (Classification: Normal).
Triglycerides: 85.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P003_Month_2.txt
Original: `preprocessed\chunks\P003_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P003 (Male, age 41) -- Month 2.

HbA1c: 4.9% (Classification: Normal).
Fasting Blood Sugar (FBS): 84.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 124.0 mg/dL (Classification: Normal).
LDL Cholesterol: 81.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 63.0 mg/dL (Classification: Normal).
Triglycerides: 79.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P003_Month_3.txt
Original: `preprocessed\chunks\P003_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P003 (Male, age 41) -- Month 3.

HbA1c: 4.8% (Classification: Normal).
Fasting Blood Sugar (FBS): 73.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 124.0 mg/dL (Classification: Normal).
LDL Cholesterol: 76.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 64.0 mg/dL (Classification: Normal).
Triglycerides: 96.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P004_Month_1.txt
Original: `preprocessed\chunks\P004_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P004 (Female, age 37) -- Month 1.

HbA1c: 5.1% (Classification: Normal).
Fasting Blood Sugar (FBS): 94.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 131.0 mg/dL (Classification: Normal).
LDL Cholesterol: 96.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 63.0 mg/dL (Classification: Normal).
Triglycerides: 110.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P004_Month_2.txt
Original: `preprocessed\chunks\P004_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P004 (Female, age 37) -- Month 2.

HbA1c: 5.2% (Classification: Normal).
Fasting Blood Sugar (FBS): 80.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 122.0 mg/dL (Classification: Normal).
LDL Cholesterol: 101.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 63.0 mg/dL (Classification: Normal).
Triglycerides: 108.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P004_Month_3.txt
Original: `preprocessed\chunks\P004_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P004 (Female, age 37) -- Month 3.

HbA1c: 4.6% (Classification: Normal).
Fasting Blood Sugar (FBS): 80.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 95.0 mg/dL (Classification: Normal).
LDL Cholesterol: 99.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 60.0 mg/dL (Classification: Normal).
Triglycerides: 103.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P005_Month_1.txt
Original: `preprocessed\chunks\P005_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P005 (Male, age 45) -- Month 1.

HbA1c: 5.0% (Classification: Normal).
Fasting Blood Sugar (FBS): 80.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 90.0 mg/dL (Classification: Normal).
LDL Cholesterol: 72.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 63.0 mg/dL (Classification: Normal).
Triglycerides: 125.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P005_Month_2.txt
Original: `preprocessed\chunks\P005_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P005 (Male, age 45) -- Month 2.

HbA1c: 4.7% (Classification: Normal).
Fasting Blood Sugar (FBS): 93.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 99.0 mg/dL (Classification: Normal).
LDL Cholesterol: 73.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 61.0 mg/dL (Classification: Normal).
Triglycerides: 116.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P005_Month_3.txt
Original: `preprocessed\chunks\P005_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P005 (Male, age 45) -- Month 3.

HbA1c: 4.9% (Classification: Normal).
Fasting Blood Sugar (FBS): 95.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 92.0 mg/dL (Classification: Normal).
LDL Cholesterol: 72.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 66.0 mg/dL (Classification: Normal).
Triglycerides: 132.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P006_Month_1.txt
Original: `preprocessed\chunks\P006_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P006 (Female, age 31) -- Month 1.

HbA1c: 4.9% (Classification: Normal).
Fasting Blood Sugar (FBS): 78.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 111.0 mg/dL (Classification: Normal).
LDL Cholesterol: 68.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 52.0 mg/dL (Classification: Normal).
Triglycerides: 130.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P006_Month_2.txt
Original: `preprocessed\chunks\P006_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P006 (Female, age 31) -- Month 2.

HbA1c: 5.4% (Classification: Normal).
Fasting Blood Sugar (FBS): 84.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 129.0 mg/dL (Classification: Normal).
LDL Cholesterol: 69.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 49.0 mg/dL (Classification: Low).
Triglycerides: 125.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P006_Month_3.txt
Original: `preprocessed\chunks\P006_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P006 (Female, age 31) -- Month 3.

HbA1c: 5.3% (Classification: Normal).
Fasting Blood Sugar (FBS): 80.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 116.0 mg/dL (Classification: Normal).
LDL Cholesterol: 69.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 55.0 mg/dL (Classification: Normal).
Triglycerides: 121.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P007_Month_1.txt
Original: `preprocessed\chunks\P007_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P007 (Male, age 39) -- Month 1.

HbA1c: 4.7% (Classification: Normal).
Fasting Blood Sugar (FBS): 83.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 128.0 mg/dL (Classification: Normal).
LDL Cholesterol: 78.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 51.0 mg/dL (Classification: Normal).
Triglycerides: 140.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P007_Month_2.txt
Original: `preprocessed\chunks\P007_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P007 (Male, age 39) -- Month 2.

HbA1c: 5.4% (Classification: Normal).
Fasting Blood Sugar (FBS): 78.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 102.0 mg/dL (Classification: Normal).
LDL Cholesterol: 76.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 48.0 mg/dL (Classification: Normal).
Triglycerides: 151.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Normal.
```

### P007_Month_3.txt
Original: `preprocessed\chunks\P007_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P007 (Male, age 39) -- Month 3.

HbA1c: 4.8% (Classification: Normal).
Fasting Blood Sugar (FBS): 80.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 103.0 mg/dL (Classification: Normal).
LDL Cholesterol: 79.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 53.0 mg/dL (Classification: Normal).
Triglycerides: 147.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P008_Month_1.txt
Original: `preprocessed\chunks\P008_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P008 (Female, age 48) -- Month 1.

HbA1c: 5.1% (Classification: Normal).
Fasting Blood Sugar (FBS): 84.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 95.0 mg/dL (Classification: Normal).
LDL Cholesterol: 97.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 59.0 mg/dL (Classification: Normal).
Triglycerides: 128.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P008_Month_2.txt
Original: `preprocessed\chunks\P008_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P008 (Female, age 48) -- Month 2.

HbA1c: 4.9% (Classification: Normal).
Fasting Blood Sugar (FBS): 72.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 97.0 mg/dL (Classification: Normal).
LDL Cholesterol: 93.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 60.0 mg/dL (Classification: Normal).
Triglycerides: 131.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P008_Month_3.txt
Original: `preprocessed\chunks\P008_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P008 (Female, age 48) -- Month 3.

HbA1c: 4.9% (Classification: Normal).
Fasting Blood Sugar (FBS): 96.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 106.0 mg/dL (Classification: Normal).
LDL Cholesterol: 95.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 58.0 mg/dL (Classification: Normal).
Triglycerides: 119.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P009_Month_1.txt
Original: `preprocessed\chunks\P009_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P009 (Male, age 42) -- Month 1.

HbA1c: 5.1% (Classification: Normal).
Fasting Blood Sugar (FBS): 94.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 94.0 mg/dL (Classification: Normal).
LDL Cholesterol: 64.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 57.0 mg/dL (Classification: Normal).
Triglycerides: 119.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P009_Month_2.txt
Original: `preprocessed\chunks\P009_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P009 (Male, age 42) -- Month 2.

HbA1c: 5.2% (Classification: Normal).
Fasting Blood Sugar (FBS): 70.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 123.0 mg/dL (Classification: Normal).
LDL Cholesterol: 60.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 59.0 mg/dL (Classification: Normal).
Triglycerides: 119.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P009_Month_3.txt
Original: `preprocessed\chunks\P009_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P009 (Male, age 42) -- Month 3.

HbA1c: 5.2% (Classification: Normal).
Fasting Blood Sugar (FBS): 91.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 94.0 mg/dL (Classification: Normal).
LDL Cholesterol: 64.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 57.0 mg/dL (Classification: Normal).
Triglycerides: 131.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P010_Month_1.txt
Original: `preprocessed\chunks\P010_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P010 (Female, age 51) -- Month 1.

HbA1c: 5.5% (Classification: Normal).
Fasting Blood Sugar (FBS): 79.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 96.0 mg/dL (Classification: Normal).
LDL Cholesterol: 86.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 58.0 mg/dL (Classification: Normal).
Triglycerides: 140.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P010_Month_2.txt
Original: `preprocessed\chunks\P010_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P010 (Female, age 51) -- Month 2.

HbA1c: 4.9% (Classification: Normal).
Fasting Blood Sugar (FBS): 74.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 102.0 mg/dL (Classification: Normal).
LDL Cholesterol: 87.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 59.0 mg/dL (Classification: Normal).
Triglycerides: 130.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Normal.
```

### P010_Month_3.txt
Original: `preprocessed\chunks\P010_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P010 (Female, age 51) -- Month 3.

HbA1c: 4.9% (Classification: Normal).
Fasting Blood Sugar (FBS): 77.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 116.0 mg/dL (Classification: Normal).
LDL Cholesterol: 89.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 58.0 mg/dL (Classification: Normal).
Triglycerides: 155.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Normal.
```

### P011_Month_1.txt
Original: `preprocessed\chunks\P011_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P011 (Male, age 46) -- Month 1.

HbA1c: 6.1% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 112.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 151.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 112.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 51.0 mg/dL (Classification: Normal).
Triglycerides: 165.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P011_Month_2.txt
Original: `preprocessed\chunks\P011_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P011 (Male, age 46) -- Month 2.

HbA1c: 6.3% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 126.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 151.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 108.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 54.0 mg/dL (Classification: Normal).
Triglycerides: 179.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P011_Month_3.txt
Original: `preprocessed\chunks\P011_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P011 (Male, age 46) -- Month 3.

HbA1c: 5.8% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 105.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 155.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 110.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 51.0 mg/dL (Classification: Normal).
Triglycerides: 174.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P012_Month_1.txt
Original: `preprocessed\chunks\P012_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P012 (Female, age 56) -- Month 1.

HbA1c: 6.1% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 123.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 184.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 121.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 42.0 mg/dL (Classification: Low).
Triglycerides: 190.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P012_Month_2.txt
Original: `preprocessed\chunks\P012_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P012 (Female, age 56) -- Month 2.

HbA1c: 6.3% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 107.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 170.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 122.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 40.0 mg/dL (Classification: Low).
Triglycerides: 184.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P012_Month_3.txt
Original: `preprocessed\chunks\P012_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P012 (Female, age 56) -- Month 3.

HbA1c: 6.1% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 99.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 189.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 124.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 42.0 mg/dL (Classification: Low).
Triglycerides: 181.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P013_Month_1.txt
Original: `preprocessed\chunks\P013_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P013 (Male, age 49) -- Month 1.

HbA1c: 6.1% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 118.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 187.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 108.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 45.0 mg/dL (Classification: Normal).
Triglycerides: 181.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P013_Month_2.txt
Original: `preprocessed\chunks\P013_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P013 (Male, age 49) -- Month 2.

HbA1c: 6.1% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 109.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 170.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 112.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 44.0 mg/dL (Classification: Normal).
Triglycerides: 195.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P013_Month_3.txt
Original: `preprocessed\chunks\P013_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P013 (Male, age 49) -- Month 3.

HbA1c: 6.2% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 122.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 193.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 110.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 45.0 mg/dL (Classification: Normal).
Triglycerides: 179.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P014_Month_1.txt
Original: `preprocessed\chunks\P014_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P014 (Female, age 58) -- Month 1.

HbA1c: 5.9% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 121.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 185.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 118.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 47.0 mg/dL (Classification: Low).
Triglycerides: 195.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P014_Month_2.txt
Original: `preprocessed\chunks\P014_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P014 (Female, age 58) -- Month 2.

HbA1c: 6.2% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 125.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 158.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 114.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 49.0 mg/dL (Classification: Low).
Triglycerides: 194.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P014_Month_3.txt
Original: `preprocessed\chunks\P014_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P014 (Female, age 58) -- Month 3.

HbA1c: 5.8% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 108.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 161.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 119.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 49.0 mg/dL (Classification: Low).
Triglycerides: 189.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P015_Month_1.txt
Original: `preprocessed\chunks\P015_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P015 (Male, age 44) -- Month 1.

HbA1c: 5.9% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 102.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 155.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 127.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 41.0 mg/dL (Classification: Normal).
Triglycerides: 172.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P015_Month_2.txt
Original: `preprocessed\chunks\P015_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P015 (Male, age 44) -- Month 2.

HbA1c: 6.1% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 100.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 167.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 125.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 44.0 mg/dL (Classification: Normal).
Triglycerides: 175.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P015_Month_3.txt
Original: `preprocessed\chunks\P015_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P015 (Male, age 44) -- Month 3.

HbA1c: 5.9% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 114.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 185.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 126.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 44.0 mg/dL (Classification: Normal).
Triglycerides: 174.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P016_Month_1.txt
Original: `preprocessed\chunks\P016_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P016 (Female, age 53) -- Month 1.

HbA1c: 5.9% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 103.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 154.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 119.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 50.0 mg/dL (Classification: Normal).
Triglycerides: 165.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P016_Month_2.txt
Original: `preprocessed\chunks\P016_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P016 (Female, age 53) -- Month 2.

HbA1c: 6.2% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 117.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 175.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 121.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 47.0 mg/dL (Classification: Low).
Triglycerides: 167.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P016_Month_3.txt
Original: `preprocessed\chunks\P016_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P016 (Female, age 53) -- Month 3.

HbA1c: 5.9% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 119.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 192.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 122.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 47.0 mg/dL (Classification: Low).
Triglycerides: 167.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P017_Month_1.txt
Original: `preprocessed\chunks\P017_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P017 (Male, age 47) -- Month 1.

HbA1c: 6.1% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 113.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 182.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 115.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 44.0 mg/dL (Classification: Normal).
Triglycerides: 168.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P017_Month_2.txt
Original: `preprocessed\chunks\P017_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P017 (Male, age 47) -- Month 2.

HbA1c: 6.3% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 121.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 142.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 110.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 43.0 mg/dL (Classification: Normal).
Triglycerides: 170.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P017_Month_3.txt
Original: `preprocessed\chunks\P017_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P017 (Male, age 47) -- Month 3.

HbA1c: 5.9% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 116.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 161.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 111.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 44.0 mg/dL (Classification: Normal).
Triglycerides: 158.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P018_Month_1.txt
Original: `preprocessed\chunks\P018_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P018 (Female, age 61) -- Month 1.

HbA1c: 5.8% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 124.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 176.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 118.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 48.0 mg/dL (Classification: Low).
Triglycerides: 189.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P018_Month_2.txt
Original: `preprocessed\chunks\P018_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P018 (Female, age 61) -- Month 2.

HbA1c: 6.0% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 99.0 mg/dL (Classification: Normal).
Post-Prandial Blood Sugar (PPBS): 163.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 116.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 46.0 mg/dL (Classification: Low).
Triglycerides: 179.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P018_Month_3.txt
Original: `preprocessed\chunks\P018_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P018 (Female, age 61) -- Month 3.

HbA1c: 6.1% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 106.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 149.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 117.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 51.0 mg/dL (Classification: Normal).
Triglycerides: 190.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P019_Month_1.txt
Original: `preprocessed\chunks\P019_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P019 (Male, age 52) -- Month 1.

HbA1c: 6.0% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 119.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 166.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 112.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 47.0 mg/dL (Classification: Normal).
Triglycerides: 160.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P019_Month_2.txt
Original: `preprocessed\chunks\P019_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P019 (Male, age 52) -- Month 2.

HbA1c: 6.0% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 118.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 188.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 116.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 44.0 mg/dL (Classification: Normal).
Triglycerides: 159.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P019_Month_3.txt
Original: `preprocessed\chunks\P019_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P019 (Male, age 52) -- Month 3.

HbA1c: 6.0% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 111.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 166.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 111.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 50.0 mg/dL (Classification: Normal).
Triglycerides: 171.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P020_Month_1.txt
Original: `preprocessed\chunks\P020_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P020 (Female, age 56) -- Month 1.

HbA1c: 6.0% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 103.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 189.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 102.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 43.0 mg/dL (Classification: Low).
Triglycerides: 161.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P020_Month_2.txt
Original: `preprocessed\chunks\P020_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P020 (Female, age 56) -- Month 2.

HbA1c: 6.2% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 106.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 191.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 98.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 44.0 mg/dL (Classification: Low).
Triglycerides: 171.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P020_Month_3.txt
Original: `preprocessed\chunks\P020_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P020 (Female, age 56) -- Month 3.

HbA1c: 5.9% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 114.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 193.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 104.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 45.0 mg/dL (Classification: Low).
Triglycerides: 155.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P021_Month_1.txt
Original: `preprocessed\chunks\P021_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P021 (Male, age 48) -- Month 1.

HbA1c: 6.1% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 122.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 168.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 120.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 42.0 mg/dL (Classification: Normal).
Triglycerides: 176.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P021_Month_2.txt
Original: `preprocessed\chunks\P021_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P021 (Male, age 48) -- Month 2.

HbA1c: 6.1% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 129.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 174.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 122.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 42.0 mg/dL (Classification: Normal).
Triglycerides: 179.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P021_Month_3.txt
Original: `preprocessed\chunks\P021_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P021 (Male, age 48) -- Month 3.

HbA1c: 6.2% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 118.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 158.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 118.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 45.0 mg/dL (Classification: Normal).
Triglycerides: 180.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P022_Month_1.txt
Original: `preprocessed\chunks\P022_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P022 (Female, age 63) -- Month 1.

HbA1c: 5.9% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 115.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 174.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 109.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 40.0 mg/dL (Classification: Low).
Triglycerides: 195.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P022_Month_2.txt
Original: `preprocessed\chunks\P022_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P022 (Female, age 63) -- Month 2.

HbA1c: 6.2% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 121.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 165.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 111.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 38.0 mg/dL (Classification: Low).
Triglycerides: 196.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P022_Month_3.txt
Original: `preprocessed\chunks\P022_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P022 (Female, age 63) -- Month 3.

HbA1c: 6.2% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 106.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 158.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 107.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 37.0 mg/dL (Classification: Low).
Triglycerides: 192.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Prediabetic.
```

### P023_Month_1.txt
Original: `preprocessed\chunks\P023_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P023 (Male, age 54) -- Month 1.

HbA1c: 7.1% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 143.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 196.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 89.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 50.0 mg/dL (Classification: Normal).
Triglycerides: 193.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P023_Month_2.txt
Original: `preprocessed\chunks\P023_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P023 (Male, age 54) -- Month 2.

HbA1c: 7.0% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 132.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 188.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 84.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 47.0 mg/dL (Classification: Normal).
Triglycerides: 192.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P023_Month_3.txt
Original: `preprocessed\chunks\P023_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P023 (Male, age 54) -- Month 3.

HbA1c: 6.7% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 139.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 171.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 89.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 50.0 mg/dL (Classification: Normal).
Triglycerides: 206.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P024_Month_1.txt
Original: `preprocessed\chunks\P024_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P024 (Female, age 59) -- Month 1.

HbA1c: 6.8% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 131.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 189.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 82.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 45.0 mg/dL (Classification: Low).
Triglycerides: 152.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P024_Month_2.txt
Original: `preprocessed\chunks\P024_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P024 (Female, age 59) -- Month 2.

HbA1c: 6.9% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 126.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 186.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 82.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 42.0 mg/dL (Classification: Low).
Triglycerides: 165.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P024_Month_3.txt
Original: `preprocessed\chunks\P024_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P024 (Female, age 59) -- Month 3.

HbA1c: 6.9% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 138.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 167.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 85.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 46.0 mg/dL (Classification: Low).
Triglycerides: 151.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P025_Month_1.txt
Original: `preprocessed\chunks\P025_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P025 (Male, age 50) -- Month 1.

HbA1c: 7.3% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 130.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 194.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 83.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 46.0 mg/dL (Classification: Normal).
Triglycerides: 158.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P025_Month_2.txt
Original: `preprocessed\chunks\P025_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P025 (Male, age 50) -- Month 2.

HbA1c: 7.2% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 121.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 170.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 80.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 45.0 mg/dL (Classification: Normal).
Triglycerides: 149.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Diabetic.
```

### P025_Month_3.txt
Original: `preprocessed\chunks\P025_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P025 (Male, age 50) -- Month 3.

HbA1c: 7.3% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 138.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 174.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 82.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 46.0 mg/dL (Classification: Normal).
Triglycerides: 163.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P026_Month_1.txt
Original: `preprocessed\chunks\P026_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P026 (Female, age 57) -- Month 1.

HbA1c: 7.2% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 131.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 194.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 84.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 40.0 mg/dL (Classification: Low).
Triglycerides: 175.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P026_Month_2.txt
Original: `preprocessed\chunks\P026_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P026 (Female, age 57) -- Month 2.

HbA1c: 6.7% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 122.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 156.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 80.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 41.0 mg/dL (Classification: Low).
Triglycerides: 185.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P026_Month_3.txt
Original: `preprocessed\chunks\P026_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P026 (Female, age 57) -- Month 3.

HbA1c: 6.9% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 125.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 165.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 85.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 41.0 mg/dL (Classification: Low).
Triglycerides: 184.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P027_Month_1.txt
Original: `preprocessed\chunks\P027_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P027 (Male, age 62) -- Month 1.

HbA1c: 7.1% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 139.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 195.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 72.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 47.0 mg/dL (Classification: Normal).
Triglycerides: 172.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P027_Month_2.txt
Original: `preprocessed\chunks\P027_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P027 (Male, age 62) -- Month 2.

HbA1c: 7.0% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 123.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 187.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 71.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 48.0 mg/dL (Classification: Normal).
Triglycerides: 181.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P027_Month_3.txt
Original: `preprocessed\chunks\P027_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P027 (Male, age 62) -- Month 3.

HbA1c: 6.5% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 123.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 172.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 75.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 44.0 mg/dL (Classification: Normal).
Triglycerides: 167.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P028_Month_1.txt
Original: `preprocessed\chunks\P028_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P028 (Female, age 46) -- Month 1.

HbA1c: 6.9% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 125.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 185.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 91.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 41.0 mg/dL (Classification: Low).
Triglycerides: 155.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P028_Month_2.txt
Original: `preprocessed\chunks\P028_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P028 (Female, age 46) -- Month 2.

HbA1c: 6.4% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 132.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 183.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 87.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 43.0 mg/dL (Classification: Low).
Triglycerides: 152.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P028_Month_3.txt
Original: `preprocessed\chunks\P028_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P028 (Female, age 46) -- Month 3.

HbA1c: 7.2% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 140.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 170.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 88.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 38.0 mg/dL (Classification: Low).
Triglycerides: 146.0 mg/dL (Classification: Normal).

Overall Glycemic Status: Diabetic.
```

### P029_Month_1.txt
Original: `preprocessed\chunks\P029_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P029 (Male, age 68) -- Month 1.

HbA1c: 6.7% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 140.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 167.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 77.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 49.0 mg/dL (Classification: Normal).
Triglycerides: 183.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P029_Month_2.txt
Original: `preprocessed\chunks\P029_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P029 (Male, age 68) -- Month 2.

HbA1c: 6.5% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 127.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 190.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 76.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 50.0 mg/dL (Classification: Normal).
Triglycerides: 190.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P029_Month_3.txt
Original: `preprocessed\chunks\P029_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P029 (Male, age 68) -- Month 3.

HbA1c: 6.8% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 123.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 162.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 75.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 51.0 mg/dL (Classification: Normal).
Triglycerides: 191.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P030_Month_1.txt
Original: `preprocessed\chunks\P030_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P030 (Female, age 55) -- Month 1.

HbA1c: 7.2% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 139.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 170.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 80.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 48.0 mg/dL (Classification: Low).
Triglycerides: 182.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P030_Month_2.txt
Original: `preprocessed\chunks\P030_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P030 (Female, age 55) -- Month 2.

HbA1c: 6.8% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 117.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 169.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 85.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 48.0 mg/dL (Classification: Low).
Triglycerides: 180.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P030_Month_3.txt
Original: `preprocessed\chunks\P030_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P030 (Female, age 55) -- Month 3.

HbA1c: 6.6% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 137.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 185.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 85.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 45.0 mg/dL (Classification: Low).
Triglycerides: 177.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P031_Month_1.txt
Original: `preprocessed\chunks\P031_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P031 (Male, age 60) -- Month 1.

HbA1c: 7.3% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 127.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 178.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 105.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 47.0 mg/dL (Classification: Normal).
Triglycerides: 179.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P031_Month_2.txt
Original: `preprocessed\chunks\P031_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P031 (Male, age 60) -- Month 2.

HbA1c: 6.6% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 138.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 191.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 107.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 44.0 mg/dL (Classification: Normal).
Triglycerides: 179.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P031_Month_3.txt
Original: `preprocessed\chunks\P031_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P031 (Male, age 60) -- Month 3.

HbA1c: 6.6% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 121.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 182.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 100.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 45.0 mg/dL (Classification: Normal).
Triglycerides: 185.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P032_Month_1.txt
Original: `preprocessed\chunks\P032_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P032 (Female, age 53) -- Month 1.

HbA1c: 7.3% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 139.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 174.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 91.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 44.0 mg/dL (Classification: Low).
Triglycerides: 194.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P032_Month_2.txt
Original: `preprocessed\chunks\P032_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P032 (Female, age 53) -- Month 2.

HbA1c: 6.7% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 133.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 181.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 93.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 41.0 mg/dL (Classification: Low).
Triglycerides: 184.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P032_Month_3.txt
Original: `preprocessed\chunks\P032_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P032 (Female, age 53) -- Month 3.

HbA1c: 7.3% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 137.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 175.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 89.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 47.0 mg/dL (Classification: Low).
Triglycerides: 187.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P033_Month_1.txt
Original: `preprocessed\chunks\P033_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P033 (Male, age 65) -- Month 1.

HbA1c: 7.0% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 136.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 195.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 100.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 39.0 mg/dL (Classification: Low).
Triglycerides: 167.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P033_Month_2.txt
Original: `preprocessed\chunks\P033_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P033 (Male, age 65) -- Month 2.

HbA1c: 6.8% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 121.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 163.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 102.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 39.0 mg/dL (Classification: Low).
Triglycerides: 164.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P033_Month_3.txt
Original: `preprocessed\chunks\P033_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P033 (Male, age 65) -- Month 3.

HbA1c: 6.8% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 124.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 178.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 96.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 38.0 mg/dL (Classification: Low).
Triglycerides: 181.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P034_Month_1.txt
Original: `preprocessed\chunks\P034_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P034 (Female, age 58) -- Month 1.

HbA1c: 6.7% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 132.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 163.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 109.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 46.0 mg/dL (Classification: Low).
Triglycerides: 166.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P034_Month_2.txt
Original: `preprocessed\chunks\P034_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P034 (Female, age 58) -- Month 2.

HbA1c: 7.0% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 131.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 174.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 106.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 46.0 mg/dL (Classification: Low).
Triglycerides: 173.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P034_Month_3.txt
Original: `preprocessed\chunks\P034_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P034 (Female, age 58) -- Month 3.

HbA1c: 6.8% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 130.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 190.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 107.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 47.0 mg/dL (Classification: Low).
Triglycerides: 168.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P035_Month_1.txt
Original: `preprocessed\chunks\P035_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P035 (Male, age 51) -- Month 1.

HbA1c: 7.0% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 122.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 166.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 75.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 41.0 mg/dL (Classification: Normal).
Triglycerides: 156.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P035_Month_2.txt
Original: `preprocessed\chunks\P035_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P035 (Male, age 51) -- Month 2.

HbA1c: 6.6% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 127.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 156.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 76.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 43.0 mg/dL (Classification: Normal).
Triglycerides: 171.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P035_Month_3.txt
Original: `preprocessed\chunks\P035_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P035 (Male, age 51) -- Month 3.

HbA1c: 7.1% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 123.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 185.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 71.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 44.0 mg/dL (Classification: Normal).
Triglycerides: 160.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P036_Month_1.txt
Original: `preprocessed\chunks\P036_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P036 (Female, age 67) -- Month 1.

HbA1c: 7.2% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 132.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 166.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 104.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 41.0 mg/dL (Classification: Low).
Triglycerides: 169.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P036_Month_2.txt
Original: `preprocessed\chunks\P036_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P036 (Female, age 67) -- Month 2.

HbA1c: 6.4% (Classification: Prediabetic).
Fasting Blood Sugar (FBS): 134.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 153.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 103.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 40.0 mg/dL (Classification: Low).
Triglycerides: 178.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P036_Month_3.txt
Original: `preprocessed\chunks\P036_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P036 (Female, age 67) -- Month 3.

HbA1c: 7.1% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 139.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 160.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 106.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 44.0 mg/dL (Classification: Low).
Triglycerides: 176.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P037_Month_1.txt
Original: `preprocessed\chunks\P037_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P037 (Male, age 59) -- Month 1.

HbA1c: 7.0% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 128.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 196.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 80.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 49.0 mg/dL (Classification: Normal).
Triglycerides: 188.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P037_Month_2.txt
Original: `preprocessed\chunks\P037_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P037 (Male, age 59) -- Month 2.

HbA1c: 6.5% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 122.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 174.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 82.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 47.0 mg/dL (Classification: Normal).
Triglycerides: 200.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P037_Month_3.txt
Original: `preprocessed\chunks\P037_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P037 (Male, age 59) -- Month 3.

HbA1c: 6.7% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 119.0 mg/dL (Classification: Prediabetic).
Post-Prandial Blood Sugar (PPBS): 159.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 77.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 47.0 mg/dL (Classification: Normal).
Triglycerides: 194.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P038_Month_1.txt
Original: `preprocessed\chunks\P038_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P038 (Female, age 72) -- Month 1.

HbA1c: 7.0% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 129.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 192.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 98.0 mg/dL (Classification: Optimal).
HDL Cholesterol: 41.0 mg/dL (Classification: Low).
Triglycerides: 158.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P038_Month_2.txt
Original: `preprocessed\chunks\P038_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P038 (Female, age 72) -- Month 2.

HbA1c: 6.7% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 138.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 168.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 100.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 42.0 mg/dL (Classification: Low).
Triglycerides: 152.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P038_Month_3.txt
Original: `preprocessed\chunks\P038_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P038 (Female, age 72) -- Month 3.

HbA1c: 6.7% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 138.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 174.0 mg/dL (Classification: Prediabetic).
LDL Cholesterol: 103.0 mg/dL (Classification: Borderline).
HDL Cholesterol: 42.0 mg/dL (Classification: Low).
Triglycerides: 153.0 mg/dL (Classification: Borderline).

Overall Glycemic Status: Diabetic.
```

### P039_Month_1.txt
Original: `preprocessed\chunks\P039_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P039 (Male, age 55) -- Month 1.

HbA1c: 7.9% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 207.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 247.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 159.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 36.0 mg/dL (Classification: Low).
Triglycerides: 321.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P039_Month_2.txt
Original: `preprocessed\chunks\P039_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P039 (Male, age 55) -- Month 2.

HbA1c: 8.0% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 205.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 281.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 157.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 36.0 mg/dL (Classification: Low).
Triglycerides: 326.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P039_Month_3.txt
Original: `preprocessed\chunks\P039_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P039 (Male, age 55) -- Month 3.

HbA1c: 8.1% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 204.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 275.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 164.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 36.0 mg/dL (Classification: Low).
Triglycerides: 319.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P040_Month_1.txt
Original: `preprocessed\chunks\P040_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P040 (Female, age 63) -- Month 1.

HbA1c: 10.1% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 158.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 288.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 173.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 40.0 mg/dL (Classification: Low).
Triglycerides: 227.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P040_Month_2.txt
Original: `preprocessed\chunks\P040_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P040 (Female, age 63) -- Month 2.

HbA1c: 7.7% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 243.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 316.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 171.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 41.0 mg/dL (Classification: Low).
Triglycerides: 242.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P040_Month_3.txt
Original: `preprocessed\chunks\P040_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P040 (Female, age 63) -- Month 3.

HbA1c: 8.8% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 243.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 230.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 178.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 37.0 mg/dL (Classification: Low).
Triglycerides: 237.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P041_Month_1.txt
Original: `preprocessed\chunks\P041_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P041 (Male, age 61) -- Month 1.

HbA1c: 7.8% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 245.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 245.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 183.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 31.0 mg/dL (Classification: Low).
Triglycerides: 265.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P041_Month_2.txt
Original: `preprocessed\chunks\P041_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P041 (Male, age 61) -- Month 2.

HbA1c: 9.7% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 188.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 262.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 183.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 33.0 mg/dL (Classification: Low).
Triglycerides: 268.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P041_Month_3.txt
Original: `preprocessed\chunks\P041_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P041 (Male, age 61) -- Month 3.

HbA1c: 8.2% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 172.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 276.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 182.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 34.0 mg/dL (Classification: Low).
Triglycerides: 270.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P042_Month_1.txt
Original: `preprocessed\chunks\P042_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P042 (Female, age 57) -- Month 1.

HbA1c: 8.2% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 220.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 259.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 140.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 36.0 mg/dL (Classification: Low).
Triglycerides: 248.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P042_Month_2.txt
Original: `preprocessed\chunks\P042_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P042 (Female, age 57) -- Month 2.

HbA1c: 10.5% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 186.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 296.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 138.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 39.0 mg/dL (Classification: Low).
Triglycerides: 259.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P042_Month_3.txt
Original: `preprocessed\chunks\P042_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P042 (Female, age 57) -- Month 3.

HbA1c: 9.7% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 210.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 276.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 142.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 35.0 mg/dL (Classification: Low).
Triglycerides: 259.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P043_Month_1.txt
Original: `preprocessed\chunks\P043_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P043 (Male, age 69) -- Month 1.

HbA1c: 8.4% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 183.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 211.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 160.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 38.0 mg/dL (Classification: Low).
Triglycerides: 227.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P043_Month_2.txt
Original: `preprocessed\chunks\P043_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P043 (Male, age 69) -- Month 2.

HbA1c: 9.7% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 187.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 286.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 155.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 39.0 mg/dL (Classification: Low).
Triglycerides: 234.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P043_Month_3.txt
Original: `preprocessed\chunks\P043_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P043 (Male, age 69) -- Month 3.

HbA1c: 8.8% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 234.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 243.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 156.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 36.0 mg/dL (Classification: Low).
Triglycerides: 218.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P044_Month_1.txt
Original: `preprocessed\chunks\P044_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P044 (Female, age 64) -- Month 1.

HbA1c: 7.7% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 221.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 203.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 137.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 33.0 mg/dL (Classification: Low).
Triglycerides: 244.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P044_Month_2.txt
Original: `preprocessed\chunks\P044_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P044 (Female, age 64) -- Month 2.

HbA1c: 10.6% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 189.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 272.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 139.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 32.0 mg/dL (Classification: Low).
Triglycerides: 255.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P044_Month_3.txt
Original: `preprocessed\chunks\P044_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P044 (Female, age 64) -- Month 3.

HbA1c: 10.5% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 247.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 274.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 139.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 34.0 mg/dL (Classification: Low).
Triglycerides: 247.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P045_Month_1.txt
Original: `preprocessed\chunks\P045_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P045 (Male, age 60) -- Month 1.

HbA1c: 8.8% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 213.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 229.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 187.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 36.0 mg/dL (Classification: Low).
Triglycerides: 217.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P045_Month_2.txt
Original: `preprocessed\chunks\P045_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P045 (Male, age 60) -- Month 2.

HbA1c: 10.4% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 189.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 212.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 183.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 38.0 mg/dL (Classification: Low).
Triglycerides: 218.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P045_Month_3.txt
Original: `preprocessed\chunks\P045_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P045 (Male, age 60) -- Month 3.

HbA1c: 9.2% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 235.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 261.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 183.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 38.0 mg/dL (Classification: Low).
Triglycerides: 213.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P046_Month_1.txt
Original: `preprocessed\chunks\P046_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P046 (Female, age 71) -- Month 1.

HbA1c: 8.1% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 152.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 251.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 148.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 37.0 mg/dL (Classification: Low).
Triglycerides: 275.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P046_Month_2.txt
Original: `preprocessed\chunks\P046_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P046 (Female, age 71) -- Month 2.

HbA1c: 9.8% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 241.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 205.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 144.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 40.0 mg/dL (Classification: Low).
Triglycerides: 289.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P046_Month_3.txt
Original: `preprocessed\chunks\P046_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P046 (Female, age 71) -- Month 3.

HbA1c: 9.4% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 236.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 229.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 147.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 40.0 mg/dL (Classification: Low).
Triglycerides: 269.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P047_Month_1.txt
Original: `preprocessed\chunks\P047_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P047 (Male, age 65) -- Month 1.

HbA1c: 8.8% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 245.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 273.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 174.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 37.0 mg/dL (Classification: Low).
Triglycerides: 241.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P047_Month_2.txt
Original: `preprocessed\chunks\P047_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P047 (Male, age 65) -- Month 2.

HbA1c: 10.7% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 216.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 233.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 169.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 36.0 mg/dL (Classification: Low).
Triglycerides: 256.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P047_Month_3.txt
Original: `preprocessed\chunks\P047_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P047 (Male, age 65) -- Month 3.

HbA1c: 9.9% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 233.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 246.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 170.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 37.0 mg/dL (Classification: Low).
Triglycerides: 245.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P048_Month_1.txt
Original: `preprocessed\chunks\P048_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P048 (Female, age 68) -- Month 1.

HbA1c: 8.2% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 179.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 209.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 169.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 38.0 mg/dL (Classification: Low).
Triglycerides: 217.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P048_Month_2.txt
Original: `preprocessed\chunks\P048_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P048 (Female, age 68) -- Month 2.

HbA1c: 9.9% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 231.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 273.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 174.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 39.0 mg/dL (Classification: Low).
Triglycerides: 216.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P048_Month_3.txt
Original: `preprocessed\chunks\P048_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P048 (Female, age 68) -- Month 3.

HbA1c: 9.0% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 162.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 223.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 165.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 35.0 mg/dL (Classification: Low).
Triglycerides: 217.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P049_Month_1.txt
Original: `preprocessed\chunks\P049_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P049 (Male, age 73) -- Month 1.

HbA1c: 9.8% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 159.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 208.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 169.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 37.0 mg/dL (Classification: Low).
Triglycerides: 330.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P049_Month_2.txt
Original: `preprocessed\chunks\P049_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P049 (Male, age 73) -- Month 2.

HbA1c: 9.5% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 165.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 225.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 173.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 38.0 mg/dL (Classification: Low).
Triglycerides: 329.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P049_Month_3.txt
Original: `preprocessed\chunks\P049_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P049 (Male, age 73) -- Month 3.

HbA1c: 9.0% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 237.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 263.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 170.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 37.0 mg/dL (Classification: Low).
Triglycerides: 327.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P050_Month_1.txt
Original: `preprocessed\chunks\P050_Month_1.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P050 (Female, age 66) -- Month 1.

HbA1c: 10.3% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 219.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 222.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 135.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 38.0 mg/dL (Classification: Low).
Triglycerides: 222.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P050_Month_2.txt
Original: `preprocessed\chunks\P050_Month_2.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P050 (Female, age 66) -- Month 2.

HbA1c: 8.9% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 213.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 259.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 132.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 40.0 mg/dL (Classification: Low).
Triglycerides: 227.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

### P050_Month_3.txt
Original: `preprocessed\chunks\P050_Month_3.txt`  |  Last modified: 2026-06-20 18:47

```
Laboratory Report Summary for Patient P050 (Female, age 66) -- Month 3.

HbA1c: 7.9% (Classification: Diabetic).
Fasting Blood Sugar (FBS): 164.0 mg/dL (Classification: Diabetic).
Post-Prandial Blood Sugar (PPBS): 214.0 mg/dL (Classification: Diabetic).
LDL Cholesterol: 139.0 mg/dL (Classification: High Risk).
HDL Cholesterol: 39.0 mg/dL (Classification: Low).
Triglycerides: 229.0 mg/dL (Classification: High).

Overall Glycemic Status: Diabetic.
```

## preprocessed

### chunks_manifest.json
Original: `preprocessed\chunks_manifest.json`  |  Last modified: 2026-06-20 18:47

JSON list with 150 items

### clean_records.json
Original: `preprocessed\clean_records.json`  |  Last modified: 2026-06-20 18:47

JSON list with 150 items

### dropped_duplicates.json
Original: `preprocessed\dropped_duplicates.json`  |  Last modified: 2026-06-20 18:47

JSON list with 8 items

### rejected_records.json
Original: `preprocessed\rejected_records.json`  |  Last modified: 2026-06-20 18:47

JSON list with 24 items

## reports_images\_debug_preprocessed

### P001_Month_1.png
Original: `reports_images\_debug_preprocessed\P001_Month_1.png`  |  Last modified: 2026-06-20 18:23

Image / figure

### P001_Month_2.png
Original: `reports_images\_debug_preprocessed\P001_Month_2.png`  |  Last modified: 2026-06-20 18:23

Image / figure

### P001_Month_3.png
Original: `reports_images\_debug_preprocessed\P001_Month_3.png`  |  Last modified: 2026-06-20 18:23

Image / figure

### P002_Month_1.png
Original: `reports_images\_debug_preprocessed\P002_Month_1.png`  |  Last modified: 2026-06-20 18:23

Image / figure

### P002_Month_1_degraded.png
Original: `reports_images\_debug_preprocessed\P002_Month_1_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P002_Month_2.png
Original: `reports_images\_debug_preprocessed\P002_Month_2.png`  |  Last modified: 2026-06-20 18:23

Image / figure

### P002_Month_2_degraded.png
Original: `reports_images\_debug_preprocessed\P002_Month_2_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P002_Month_3.png
Original: `reports_images\_debug_preprocessed\P002_Month_3.png`  |  Last modified: 2026-06-20 18:23

Image / figure

### P002_Month_3_degraded.png
Original: `reports_images\_debug_preprocessed\P002_Month_3_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P003_Month_1.png
Original: `reports_images\_debug_preprocessed\P003_Month_1.png`  |  Last modified: 2026-06-20 18:23

Image / figure

### P003_Month_2.png
Original: `reports_images\_debug_preprocessed\P003_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P003_Month_3.png
Original: `reports_images\_debug_preprocessed\P003_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P004_Month_1.png
Original: `reports_images\_debug_preprocessed\P004_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P004_Month_2.png
Original: `reports_images\_debug_preprocessed\P004_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P004_Month_3.png
Original: `reports_images\_debug_preprocessed\P004_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P005_Month_1.png
Original: `reports_images\_debug_preprocessed\P005_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P005_Month_2.png
Original: `reports_images\_debug_preprocessed\P005_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P005_Month_3.png
Original: `reports_images\_debug_preprocessed\P005_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P006_Month_1.png
Original: `reports_images\_debug_preprocessed\P006_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P006_Month_2.png
Original: `reports_images\_debug_preprocessed\P006_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P006_Month_3.png
Original: `reports_images\_debug_preprocessed\P006_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P007_Month_1.png
Original: `reports_images\_debug_preprocessed\P007_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P007_Month_2.png
Original: `reports_images\_debug_preprocessed\P007_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P007_Month_2_degraded.png
Original: `reports_images\_debug_preprocessed\P007_Month_2_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P007_Month_3.png
Original: `reports_images\_debug_preprocessed\P007_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P007_Month_3_degraded.png
Original: `reports_images\_debug_preprocessed\P007_Month_3_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P008_Month_1.png
Original: `reports_images\_debug_preprocessed\P008_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P008_Month_2.png
Original: `reports_images\_debug_preprocessed\P008_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P008_Month_3.png
Original: `reports_images\_debug_preprocessed\P008_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P008_Month_3_degraded.png
Original: `reports_images\_debug_preprocessed\P008_Month_3_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P009_Month_1.png
Original: `reports_images\_debug_preprocessed\P009_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P009_Month_2.png
Original: `reports_images\_debug_preprocessed\P009_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P009_Month_2_degraded.png
Original: `reports_images\_debug_preprocessed\P009_Month_2_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P009_Month_3.png
Original: `reports_images\_debug_preprocessed\P009_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P010_Month_1.png
Original: `reports_images\_debug_preprocessed\P010_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P010_Month_2.png
Original: `reports_images\_debug_preprocessed\P010_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P010_Month_3.png
Original: `reports_images\_debug_preprocessed\P010_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P011_Month_1.png
Original: `reports_images\_debug_preprocessed\P011_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P011_Month_2.png
Original: `reports_images\_debug_preprocessed\P011_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P011_Month_3.png
Original: `reports_images\_debug_preprocessed\P011_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P011_Month_3_degraded.png
Original: `reports_images\_debug_preprocessed\P011_Month_3_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P012_Month_1.png
Original: `reports_images\_debug_preprocessed\P012_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P012_Month_2.png
Original: `reports_images\_debug_preprocessed\P012_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P012_Month_3.png
Original: `reports_images\_debug_preprocessed\P012_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P013_Month_1.png
Original: `reports_images\_debug_preprocessed\P013_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P013_Month_1_degraded.png
Original: `reports_images\_debug_preprocessed\P013_Month_1_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P013_Month_2.png
Original: `reports_images\_debug_preprocessed\P013_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P013_Month_2_degraded.png
Original: `reports_images\_debug_preprocessed\P013_Month_2_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P013_Month_3.png
Original: `reports_images\_debug_preprocessed\P013_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P014_Month_1.png
Original: `reports_images\_debug_preprocessed\P014_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P014_Month_2.png
Original: `reports_images\_debug_preprocessed\P014_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P014_Month_3.png
Original: `reports_images\_debug_preprocessed\P014_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P015_Month_1.png
Original: `reports_images\_debug_preprocessed\P015_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P015_Month_2.png
Original: `reports_images\_debug_preprocessed\P015_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P015_Month_3.png
Original: `reports_images\_debug_preprocessed\P015_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P016_Month_1.png
Original: `reports_images\_debug_preprocessed\P016_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P016_Month_2.png
Original: `reports_images\_debug_preprocessed\P016_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P016_Month_3.png
Original: `reports_images\_debug_preprocessed\P016_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P016_Month_3_degraded.png
Original: `reports_images\_debug_preprocessed\P016_Month_3_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P017_Month_1.png
Original: `reports_images\_debug_preprocessed\P017_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P017_Month_2.png
Original: `reports_images\_debug_preprocessed\P017_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P017_Month_3.png
Original: `reports_images\_debug_preprocessed\P017_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P018_Month_1.png
Original: `reports_images\_debug_preprocessed\P018_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P018_Month_2.png
Original: `reports_images\_debug_preprocessed\P018_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P018_Month_2_degraded.png
Original: `reports_images\_debug_preprocessed\P018_Month_2_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P018_Month_3.png
Original: `reports_images\_debug_preprocessed\P018_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P018_Month_3_degraded.png
Original: `reports_images\_debug_preprocessed\P018_Month_3_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P019_Month_1.png
Original: `reports_images\_debug_preprocessed\P019_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P019_Month_1_degraded.png
Original: `reports_images\_debug_preprocessed\P019_Month_1_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P019_Month_2.png
Original: `reports_images\_debug_preprocessed\P019_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P019_Month_3.png
Original: `reports_images\_debug_preprocessed\P019_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P019_Month_3_degraded.png
Original: `reports_images\_debug_preprocessed\P019_Month_3_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P020_Month_1.png
Original: `reports_images\_debug_preprocessed\P020_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P020_Month_2.png
Original: `reports_images\_debug_preprocessed\P020_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P020_Month_3.png
Original: `reports_images\_debug_preprocessed\P020_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P020_Month_3_degraded.png
Original: `reports_images\_debug_preprocessed\P020_Month_3_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P021_Month_1.png
Original: `reports_images\_debug_preprocessed\P021_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P021_Month_2.png
Original: `reports_images\_debug_preprocessed\P021_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P021_Month_3.png
Original: `reports_images\_debug_preprocessed\P021_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P022_Month_1.png
Original: `reports_images\_debug_preprocessed\P022_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P022_Month_2.png
Original: `reports_images\_debug_preprocessed\P022_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P022_Month_3.png
Original: `reports_images\_debug_preprocessed\P022_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P023_Month_1.png
Original: `reports_images\_debug_preprocessed\P023_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P023_Month_2.png
Original: `reports_images\_debug_preprocessed\P023_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P023_Month_2_degraded.png
Original: `reports_images\_debug_preprocessed\P023_Month_2_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P023_Month_3.png
Original: `reports_images\_debug_preprocessed\P023_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P023_Month_3_degraded.png
Original: `reports_images\_debug_preprocessed\P023_Month_3_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P024_Month_1.png
Original: `reports_images\_debug_preprocessed\P024_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P024_Month_2.png
Original: `reports_images\_debug_preprocessed\P024_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P024_Month_3.png
Original: `reports_images\_debug_preprocessed\P024_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P025_Month_1.png
Original: `reports_images\_debug_preprocessed\P025_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P025_Month_2.png
Original: `reports_images\_debug_preprocessed\P025_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P025_Month_3.png
Original: `reports_images\_debug_preprocessed\P025_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P026_Month_1.png
Original: `reports_images\_debug_preprocessed\P026_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P026_Month_2.png
Original: `reports_images\_debug_preprocessed\P026_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P026_Month_3.png
Original: `reports_images\_debug_preprocessed\P026_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P027_Month_1.png
Original: `reports_images\_debug_preprocessed\P027_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P027_Month_2.png
Original: `reports_images\_debug_preprocessed\P027_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P027_Month_3.png
Original: `reports_images\_debug_preprocessed\P027_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P028_Month_1.png
Original: `reports_images\_debug_preprocessed\P028_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P028_Month_2.png
Original: `reports_images\_debug_preprocessed\P028_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P028_Month_3.png
Original: `reports_images\_debug_preprocessed\P028_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P029_Month_1.png
Original: `reports_images\_debug_preprocessed\P029_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P029_Month_1_degraded.png
Original: `reports_images\_debug_preprocessed\P029_Month_1_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P029_Month_2.png
Original: `reports_images\_debug_preprocessed\P029_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P029_Month_3.png
Original: `reports_images\_debug_preprocessed\P029_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P030_Month_1.png
Original: `reports_images\_debug_preprocessed\P030_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P030_Month_2.png
Original: `reports_images\_debug_preprocessed\P030_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P030_Month_3.png
Original: `reports_images\_debug_preprocessed\P030_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P031_Month_1.png
Original: `reports_images\_debug_preprocessed\P031_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P031_Month_2.png
Original: `reports_images\_debug_preprocessed\P031_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P031_Month_3.png
Original: `reports_images\_debug_preprocessed\P031_Month_3.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P032_Month_1.png
Original: `reports_images\_debug_preprocessed\P032_Month_1.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P032_Month_2.png
Original: `reports_images\_debug_preprocessed\P032_Month_2.png`  |  Last modified: 2026-06-20 18:24

Image / figure

### P032_Month_3.png
Original: `reports_images\_debug_preprocessed\P032_Month_3.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P033_Month_1.png
Original: `reports_images\_debug_preprocessed\P033_Month_1.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P033_Month_2.png
Original: `reports_images\_debug_preprocessed\P033_Month_2.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P033_Month_3.png
Original: `reports_images\_debug_preprocessed\P033_Month_3.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P034_Month_1.png
Original: `reports_images\_debug_preprocessed\P034_Month_1.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P034_Month_2.png
Original: `reports_images\_debug_preprocessed\P034_Month_2.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P034_Month_3.png
Original: `reports_images\_debug_preprocessed\P034_Month_3.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P035_Month_1.png
Original: `reports_images\_debug_preprocessed\P035_Month_1.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P035_Month_2.png
Original: `reports_images\_debug_preprocessed\P035_Month_2.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P035_Month_3.png
Original: `reports_images\_debug_preprocessed\P035_Month_3.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P035_Month_3_degraded.png
Original: `reports_images\_debug_preprocessed\P035_Month_3_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P036_Month_1.png
Original: `reports_images\_debug_preprocessed\P036_Month_1.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P036_Month_1_degraded.png
Original: `reports_images\_debug_preprocessed\P036_Month_1_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P036_Month_2.png
Original: `reports_images\_debug_preprocessed\P036_Month_2.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P036_Month_3.png
Original: `reports_images\_debug_preprocessed\P036_Month_3.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P037_Month_1.png
Original: `reports_images\_debug_preprocessed\P037_Month_1.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P037_Month_2.png
Original: `reports_images\_debug_preprocessed\P037_Month_2.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P037_Month_3.png
Original: `reports_images\_debug_preprocessed\P037_Month_3.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P038_Month_1.png
Original: `reports_images\_debug_preprocessed\P038_Month_1.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P038_Month_1_degraded.png
Original: `reports_images\_debug_preprocessed\P038_Month_1_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P038_Month_2.png
Original: `reports_images\_debug_preprocessed\P038_Month_2.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P038_Month_3.png
Original: `reports_images\_debug_preprocessed\P038_Month_3.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P039_Month_1.png
Original: `reports_images\_debug_preprocessed\P039_Month_1.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P039_Month_2.png
Original: `reports_images\_debug_preprocessed\P039_Month_2.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P039_Month_3.png
Original: `reports_images\_debug_preprocessed\P039_Month_3.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P040_Month_1.png
Original: `reports_images\_debug_preprocessed\P040_Month_1.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P040_Month_2.png
Original: `reports_images\_debug_preprocessed\P040_Month_2.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P040_Month_3.png
Original: `reports_images\_debug_preprocessed\P040_Month_3.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P040_Month_3_degraded.png
Original: `reports_images\_debug_preprocessed\P040_Month_3_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P041_Month_1.png
Original: `reports_images\_debug_preprocessed\P041_Month_1.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P041_Month_2.png
Original: `reports_images\_debug_preprocessed\P041_Month_2.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P041_Month_3.png
Original: `reports_images\_debug_preprocessed\P041_Month_3.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P042_Month_1.png
Original: `reports_images\_debug_preprocessed\P042_Month_1.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P042_Month_2.png
Original: `reports_images\_debug_preprocessed\P042_Month_2.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P042_Month_3.png
Original: `reports_images\_debug_preprocessed\P042_Month_3.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P043_Month_1.png
Original: `reports_images\_debug_preprocessed\P043_Month_1.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P043_Month_1_degraded.png
Original: `reports_images\_debug_preprocessed\P043_Month_1_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P043_Month_2.png
Original: `reports_images\_debug_preprocessed\P043_Month_2.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P043_Month_3.png
Original: `reports_images\_debug_preprocessed\P043_Month_3.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P044_Month_1.png
Original: `reports_images\_debug_preprocessed\P044_Month_1.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P044_Month_2.png
Original: `reports_images\_debug_preprocessed\P044_Month_2.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P044_Month_3.png
Original: `reports_images\_debug_preprocessed\P044_Month_3.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P044_Month_3_degraded.png
Original: `reports_images\_debug_preprocessed\P044_Month_3_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P045_Month_1.png
Original: `reports_images\_debug_preprocessed\P045_Month_1.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P045_Month_2.png
Original: `reports_images\_debug_preprocessed\P045_Month_2.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P045_Month_3.png
Original: `reports_images\_debug_preprocessed\P045_Month_3.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P046_Month_1.png
Original: `reports_images\_debug_preprocessed\P046_Month_1.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P046_Month_2.png
Original: `reports_images\_debug_preprocessed\P046_Month_2.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P046_Month_2_degraded.png
Original: `reports_images\_debug_preprocessed\P046_Month_2_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P046_Month_3.png
Original: `reports_images\_debug_preprocessed\P046_Month_3.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P047_Month_1.png
Original: `reports_images\_debug_preprocessed\P047_Month_1.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P047_Month_2.png
Original: `reports_images\_debug_preprocessed\P047_Month_2.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P047_Month_2_degraded.png
Original: `reports_images\_debug_preprocessed\P047_Month_2_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P047_Month_3.png
Original: `reports_images\_debug_preprocessed\P047_Month_3.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P048_Month_1.png
Original: `reports_images\_debug_preprocessed\P048_Month_1.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P048_Month_2.png
Original: `reports_images\_debug_preprocessed\P048_Month_2.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P048_Month_3.png
Original: `reports_images\_debug_preprocessed\P048_Month_3.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P048_Month_3_degraded.png
Original: `reports_images\_debug_preprocessed\P048_Month_3_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P049_Month_1.png
Original: `reports_images\_debug_preprocessed\P049_Month_1.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P049_Month_2.png
Original: `reports_images\_debug_preprocessed\P049_Month_2.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P049_Month_3.png
Original: `reports_images\_debug_preprocessed\P049_Month_3.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P050_Month_1.png
Original: `reports_images\_debug_preprocessed\P050_Month_1.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P050_Month_2.png
Original: `reports_images\_debug_preprocessed\P050_Month_2.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### P050_Month_3.png
Original: `reports_images\_debug_preprocessed\P050_Month_3.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### Poorly-Controlled_P039-P050.png
Original: `reports_images\_debug_preprocessed\Poorly-Controlled_P039-P050.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### Prediabetic_P011-P022.png
Original: `reports_images\_debug_preprocessed\Prediabetic_P011-P022.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### Prediabetic_P011-P022_degraded.png
Original: `reports_images\_debug_preprocessed\Prediabetic_P011-P022_degraded.png`  |  Last modified: 2026-06-20 18:25

Image / figure

### Well-Controlled_P023-P038.png
Original: `reports_images\_debug_preprocessed\Well-Controlled_P023-P038.png`  |  Last modified: 2026-06-20 18:25

Image / figure

## reports_images\clean

### P001_Month_1.png
Original: `reports_images\clean\P001_Month_1.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P001_Month_2.png
Original: `reports_images\clean\P001_Month_2.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P001_Month_3.png
Original: `reports_images\clean\P001_Month_3.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P002_Month_1.png
Original: `reports_images\clean\P002_Month_1.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P002_Month_2.png
Original: `reports_images\clean\P002_Month_2.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P002_Month_3.png
Original: `reports_images\clean\P002_Month_3.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P003_Month_1.png
Original: `reports_images\clean\P003_Month_1.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P003_Month_2.png
Original: `reports_images\clean\P003_Month_2.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P003_Month_3.png
Original: `reports_images\clean\P003_Month_3.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P004_Month_1.png
Original: `reports_images\clean\P004_Month_1.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P004_Month_2.png
Original: `reports_images\clean\P004_Month_2.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P004_Month_3.png
Original: `reports_images\clean\P004_Month_3.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P005_Month_1.png
Original: `reports_images\clean\P005_Month_1.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P005_Month_2.png
Original: `reports_images\clean\P005_Month_2.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P005_Month_3.png
Original: `reports_images\clean\P005_Month_3.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P006_Month_1.png
Original: `reports_images\clean\P006_Month_1.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P006_Month_2.png
Original: `reports_images\clean\P006_Month_2.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P006_Month_3.png
Original: `reports_images\clean\P006_Month_3.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P007_Month_1.png
Original: `reports_images\clean\P007_Month_1.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P007_Month_2.png
Original: `reports_images\clean\P007_Month_2.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P007_Month_3.png
Original: `reports_images\clean\P007_Month_3.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P008_Month_1.png
Original: `reports_images\clean\P008_Month_1.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P008_Month_2.png
Original: `reports_images\clean\P008_Month_2.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P008_Month_3.png
Original: `reports_images\clean\P008_Month_3.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P009_Month_1.png
Original: `reports_images\clean\P009_Month_1.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P009_Month_2.png
Original: `reports_images\clean\P009_Month_2.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P009_Month_3.png
Original: `reports_images\clean\P009_Month_3.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P010_Month_1.png
Original: `reports_images\clean\P010_Month_1.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P010_Month_2.png
Original: `reports_images\clean\P010_Month_2.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P010_Month_3.png
Original: `reports_images\clean\P010_Month_3.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P011_Month_1.png
Original: `reports_images\clean\P011_Month_1.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P011_Month_2.png
Original: `reports_images\clean\P011_Month_2.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P011_Month_3.png
Original: `reports_images\clean\P011_Month_3.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P012_Month_1.png
Original: `reports_images\clean\P012_Month_1.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P012_Month_2.png
Original: `reports_images\clean\P012_Month_2.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P012_Month_3.png
Original: `reports_images\clean\P012_Month_3.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P013_Month_1.png
Original: `reports_images\clean\P013_Month_1.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P013_Month_2.png
Original: `reports_images\clean\P013_Month_2.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P013_Month_3.png
Original: `reports_images\clean\P013_Month_3.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P014_Month_1.png
Original: `reports_images\clean\P014_Month_1.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P014_Month_2.png
Original: `reports_images\clean\P014_Month_2.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P014_Month_3.png
Original: `reports_images\clean\P014_Month_3.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P015_Month_1.png
Original: `reports_images\clean\P015_Month_1.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P015_Month_2.png
Original: `reports_images\clean\P015_Month_2.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P015_Month_3.png
Original: `reports_images\clean\P015_Month_3.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P016_Month_1.png
Original: `reports_images\clean\P016_Month_1.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P016_Month_2.png
Original: `reports_images\clean\P016_Month_2.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P016_Month_3.png
Original: `reports_images\clean\P016_Month_3.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P017_Month_1.png
Original: `reports_images\clean\P017_Month_1.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P017_Month_2.png
Original: `reports_images\clean\P017_Month_2.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P017_Month_3.png
Original: `reports_images\clean\P017_Month_3.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P018_Month_1.png
Original: `reports_images\clean\P018_Month_1.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P018_Month_2.png
Original: `reports_images\clean\P018_Month_2.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P018_Month_3.png
Original: `reports_images\clean\P018_Month_3.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P019_Month_1.png
Original: `reports_images\clean\P019_Month_1.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P019_Month_2.png
Original: `reports_images\clean\P019_Month_2.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P019_Month_3.png
Original: `reports_images\clean\P019_Month_3.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P020_Month_1.png
Original: `reports_images\clean\P020_Month_1.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P020_Month_2.png
Original: `reports_images\clean\P020_Month_2.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P020_Month_3.png
Original: `reports_images\clean\P020_Month_3.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P021_Month_1.png
Original: `reports_images\clean\P021_Month_1.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P021_Month_2.png
Original: `reports_images\clean\P021_Month_2.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P021_Month_3.png
Original: `reports_images\clean\P021_Month_3.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P022_Month_1.png
Original: `reports_images\clean\P022_Month_1.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P022_Month_2.png
Original: `reports_images\clean\P022_Month_2.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P022_Month_3.png
Original: `reports_images\clean\P022_Month_3.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P023_Month_1.png
Original: `reports_images\clean\P023_Month_1.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P023_Month_2.png
Original: `reports_images\clean\P023_Month_2.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P023_Month_3.png
Original: `reports_images\clean\P023_Month_3.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P024_Month_1.png
Original: `reports_images\clean\P024_Month_1.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P024_Month_2.png
Original: `reports_images\clean\P024_Month_2.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P024_Month_3.png
Original: `reports_images\clean\P024_Month_3.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P025_Month_1.png
Original: `reports_images\clean\P025_Month_1.png`  |  Last modified: 2026-06-19 15:45

Image / figure

### P025_Month_2.png
Original: `reports_images\clean\P025_Month_2.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P025_Month_3.png
Original: `reports_images\clean\P025_Month_3.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P026_Month_1.png
Original: `reports_images\clean\P026_Month_1.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P026_Month_2.png
Original: `reports_images\clean\P026_Month_2.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P026_Month_3.png
Original: `reports_images\clean\P026_Month_3.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P027_Month_1.png
Original: `reports_images\clean\P027_Month_1.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P027_Month_2.png
Original: `reports_images\clean\P027_Month_2.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P027_Month_3.png
Original: `reports_images\clean\P027_Month_3.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P028_Month_1.png
Original: `reports_images\clean\P028_Month_1.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P028_Month_2.png
Original: `reports_images\clean\P028_Month_2.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P028_Month_3.png
Original: `reports_images\clean\P028_Month_3.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P029_Month_1.png
Original: `reports_images\clean\P029_Month_1.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P029_Month_2.png
Original: `reports_images\clean\P029_Month_2.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P029_Month_3.png
Original: `reports_images\clean\P029_Month_3.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P030_Month_1.png
Original: `reports_images\clean\P030_Month_1.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P030_Month_2.png
Original: `reports_images\clean\P030_Month_2.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P030_Month_3.png
Original: `reports_images\clean\P030_Month_3.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P031_Month_1.png
Original: `reports_images\clean\P031_Month_1.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P031_Month_2.png
Original: `reports_images\clean\P031_Month_2.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P031_Month_3.png
Original: `reports_images\clean\P031_Month_3.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P032_Month_1.png
Original: `reports_images\clean\P032_Month_1.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P032_Month_2.png
Original: `reports_images\clean\P032_Month_2.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P032_Month_3.png
Original: `reports_images\clean\P032_Month_3.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P033_Month_1.png
Original: `reports_images\clean\P033_Month_1.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P033_Month_2.png
Original: `reports_images\clean\P033_Month_2.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P033_Month_3.png
Original: `reports_images\clean\P033_Month_3.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P034_Month_1.png
Original: `reports_images\clean\P034_Month_1.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P034_Month_2.png
Original: `reports_images\clean\P034_Month_2.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P034_Month_3.png
Original: `reports_images\clean\P034_Month_3.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P035_Month_1.png
Original: `reports_images\clean\P035_Month_1.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P035_Month_2.png
Original: `reports_images\clean\P035_Month_2.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P035_Month_3.png
Original: `reports_images\clean\P035_Month_3.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P036_Month_1.png
Original: `reports_images\clean\P036_Month_1.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P036_Month_2.png
Original: `reports_images\clean\P036_Month_2.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P036_Month_3.png
Original: `reports_images\clean\P036_Month_3.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P037_Month_1.png
Original: `reports_images\clean\P037_Month_1.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P037_Month_2.png
Original: `reports_images\clean\P037_Month_2.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P037_Month_3.png
Original: `reports_images\clean\P037_Month_3.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P038_Month_1.png
Original: `reports_images\clean\P038_Month_1.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P038_Month_2.png
Original: `reports_images\clean\P038_Month_2.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P038_Month_3.png
Original: `reports_images\clean\P038_Month_3.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P039_Month_1.png
Original: `reports_images\clean\P039_Month_1.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P039_Month_2.png
Original: `reports_images\clean\P039_Month_2.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P039_Month_3.png
Original: `reports_images\clean\P039_Month_3.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P040_Month_1.png
Original: `reports_images\clean\P040_Month_1.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P040_Month_2.png
Original: `reports_images\clean\P040_Month_2.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P040_Month_3.png
Original: `reports_images\clean\P040_Month_3.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P041_Month_1.png
Original: `reports_images\clean\P041_Month_1.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P041_Month_2.png
Original: `reports_images\clean\P041_Month_2.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P041_Month_3.png
Original: `reports_images\clean\P041_Month_3.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P042_Month_1.png
Original: `reports_images\clean\P042_Month_1.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P042_Month_2.png
Original: `reports_images\clean\P042_Month_2.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P042_Month_3.png
Original: `reports_images\clean\P042_Month_3.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P043_Month_1.png
Original: `reports_images\clean\P043_Month_1.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P043_Month_2.png
Original: `reports_images\clean\P043_Month_2.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P043_Month_3.png
Original: `reports_images\clean\P043_Month_3.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P044_Month_1.png
Original: `reports_images\clean\P044_Month_1.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P044_Month_2.png
Original: `reports_images\clean\P044_Month_2.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P044_Month_3.png
Original: `reports_images\clean\P044_Month_3.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P045_Month_1.png
Original: `reports_images\clean\P045_Month_1.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P045_Month_2.png
Original: `reports_images\clean\P045_Month_2.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P045_Month_3.png
Original: `reports_images\clean\P045_Month_3.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P046_Month_1.png
Original: `reports_images\clean\P046_Month_1.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P046_Month_2.png
Original: `reports_images\clean\P046_Month_2.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P046_Month_3.png
Original: `reports_images\clean\P046_Month_3.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P047_Month_1.png
Original: `reports_images\clean\P047_Month_1.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P047_Month_2.png
Original: `reports_images\clean\P047_Month_2.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P047_Month_3.png
Original: `reports_images\clean\P047_Month_3.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P048_Month_1.png
Original: `reports_images\clean\P048_Month_1.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P048_Month_2.png
Original: `reports_images\clean\P048_Month_2.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P048_Month_3.png
Original: `reports_images\clean\P048_Month_3.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P049_Month_1.png
Original: `reports_images\clean\P049_Month_1.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P049_Month_2.png
Original: `reports_images\clean\P049_Month_2.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P049_Month_3.png
Original: `reports_images\clean\P049_Month_3.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P050_Month_1.png
Original: `reports_images\clean\P050_Month_1.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P050_Month_2.png
Original: `reports_images\clean\P050_Month_2.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P050_Month_3.png
Original: `reports_images\clean\P050_Month_3.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### Poorly-Controlled_P039-P050.png
Original: `reports_images\clean\Poorly-Controlled_P039-P050.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### Prediabetic_P011-P022.png
Original: `reports_images\clean\Prediabetic_P011-P022.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### Well-Controlled_P023-P038.png
Original: `reports_images\clean\Well-Controlled_P023-P038.png`  |  Last modified: 2026-06-19 15:46

Image / figure

## reports_images\degraded

### P002_Month_1_degraded.png
Original: `reports_images\degraded\P002_Month_1_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P002_Month_2_degraded.png
Original: `reports_images\degraded\P002_Month_2_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P002_Month_3_degraded.png
Original: `reports_images\degraded\P002_Month_3_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P007_Month_2_degraded.png
Original: `reports_images\degraded\P007_Month_2_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P007_Month_3_degraded.png
Original: `reports_images\degraded\P007_Month_3_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P008_Month_3_degraded.png
Original: `reports_images\degraded\P008_Month_3_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P009_Month_2_degraded.png
Original: `reports_images\degraded\P009_Month_2_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P011_Month_3_degraded.png
Original: `reports_images\degraded\P011_Month_3_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P013_Month_1_degraded.png
Original: `reports_images\degraded\P013_Month_1_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P013_Month_2_degraded.png
Original: `reports_images\degraded\P013_Month_2_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P016_Month_3_degraded.png
Original: `reports_images\degraded\P016_Month_3_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P018_Month_2_degraded.png
Original: `reports_images\degraded\P018_Month_2_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P018_Month_3_degraded.png
Original: `reports_images\degraded\P018_Month_3_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P019_Month_1_degraded.png
Original: `reports_images\degraded\P019_Month_1_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P019_Month_3_degraded.png
Original: `reports_images\degraded\P019_Month_3_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P020_Month_3_degraded.png
Original: `reports_images\degraded\P020_Month_3_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P023_Month_2_degraded.png
Original: `reports_images\degraded\P023_Month_2_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P023_Month_3_degraded.png
Original: `reports_images\degraded\P023_Month_3_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P029_Month_1_degraded.png
Original: `reports_images\degraded\P029_Month_1_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P035_Month_3_degraded.png
Original: `reports_images\degraded\P035_Month_3_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P036_Month_1_degraded.png
Original: `reports_images\degraded\P036_Month_1_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P038_Month_1_degraded.png
Original: `reports_images\degraded\P038_Month_1_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P040_Month_3_degraded.png
Original: `reports_images\degraded\P040_Month_3_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P043_Month_1_degraded.png
Original: `reports_images\degraded\P043_Month_1_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P044_Month_3_degraded.png
Original: `reports_images\degraded\P044_Month_3_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P046_Month_2_degraded.png
Original: `reports_images\degraded\P046_Month_2_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P047_Month_2_degraded.png
Original: `reports_images\degraded\P047_Month_2_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### P048_Month_3_degraded.png
Original: `reports_images\degraded\P048_Month_3_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

### Prediabetic_P011-P022_degraded.png
Original: `reports_images\degraded\Prediabetic_P011-P022_degraded.png`  |  Last modified: 2026-06-19 15:46

Image / figure

## results\explainability

### trajectory_integrated_gradients.json
Original: `results\explainability\trajectory_integrated_gradients.json`  |  Last modified: 2026-10-03 11:45

| key | value |
|---|---|
| _produced_by | phase_k_explainability.py |
| _saved_at | 2026-10-03T11:45:55 |
| _notes | Fig. 8 and Section 4.6 |
| results.P032.patient_id | P032 |
| results.P032.target | HbA1c(%) |
| results.P032.unit | % |
| results.P032.predicted_value | 7.3933 |
| results.P032.baseline_value | 6.9325 |
| results.P032.completeness_gap | -0.0 |
| results.P032.predict_change | True |
| results.P032.attributions.Month t-2 / HbA1c(%) | 0.0232 |
| results.P032.attributions.Month t-2 / FBS (mg/dL) | 0.0027 |
| results.P032.attributions.Month t-2 / PPBS (mg/dL) | -0.0039 |
| results.P032.attributions.Month t-1 / HbA1c(%) | 0.4132 |
| results.P032.attributions.Month t-1 / FBS (mg/dL) | 0.0151 |
| results.P032.attributions.Month t-1 / PPBS (mg/dL) | 0.0105 |
| results.cohort.num_patients | 50 |
| results.cohort.max_completeness_gap | 0.0002 |
| results.cohort.mean_abs_attribution.Month t-2 / HbA1c(%) | 0.0914 |
| results.cohort.mean_abs_attribution.Month t-2 / FBS (mg/dL) | 0.0213 |
| results.cohort.mean_abs_attribution.Month t-2 / PPBS (mg/dL) | 0.0401 |
| results.cohort.mean_abs_attribution.Month t-1 / HbA1c(%) | 1.1043 |
| results.cohort.mean_abs_attribution.Month t-1 / FBS (mg/dL) | 0.1855 |
| results.cohort.mean_abs_attribution.Month t-1 / PPBS (mg/dL) | 0.0546 |

### verifier_attention.json
Original: `results\explainability\verifier_attention.json`  |  Last modified: 2026-10-03 11:46

| key | value |
|---|---|
| _produced_by | phase_k_explainability.py |
| _saved_at | 2026-10-03T11:46:08 |
| _notes | Fig. 9; illustrative single examples, final verifier model |
| results.faithful_example.case | faithful |
| results.faithful_example.predicted_label | faithful |
| results.faithful_example.confidence | 0.9908 |
| results.faithful_example.top1_attention_share | 0.1585 |
| results.hallucinated_example.case | hallucinated |
| results.hallucinated_example.predicted_label | hallucinated |
| results.hallucinated_example.confidence | 0.9995 |
| results.hallucinated_example.top1_attention_share | 0.1761 |

## results\test

### hello.json
Original: `results\test\hello.json`  |  Last modified: 2026-10-03 11:22

| key | value |
|---|---|
| _produced_by | <string> |
| _saved_at | 2026-10-03T11:22:49 |
| _notes |  |
| results.a | 1 |

## results\trajectory

### cv_results.json
Original: `results\trajectory\cv_results.json`  |  Last modified: 2026-10-03 11:34

| key | value |
|---|---|
| _produced_by | phase_j_1_trajectory_model.py |
| _saved_at | 2026-10-03T11:34:49 |
| _notes | Table II: GRU vs persistence, patient-grouped 5-fold CV |
| results.setup.num_samples | 100 |
| results.setup.num_patients | 50 |
| results.setup.num_folds | 5 |
| results.setup.split | GroupKFold by Patient_ID |
| results.setup.predict_change | True |
| results.setup.epochs | 60 |
| results.setup.hidden_size | 16 |
| results.setup.learning_rate | 0.005 |
| results.gru.HbA1c(%)_MAE.mean | 0.4764 |
| results.gru.HbA1c(%)_MAE.std | 0.1104 |
| results.gru.FBS (mg/dL)_MAE.mean | 13.935 |
| results.gru.FBS (mg/dL)_MAE.std | 3.2681 |
| results.gru.PPBS (mg/dL)_MAE.mean | 19.7936 |
| results.gru.PPBS (mg/dL)_MAE.std | 2.9343 |
| results.gru.risk_accuracy.mean | 0.94 |
| results.gru.risk_accuracy.std | 0.0583 |
| results.gru.risk_macro_f1.mean | 0.9327 |
| results.gru.risk_macro_f1.std | 0.0668 |
| results.persistence_baseline.HbA1c(%)_MAE.mean | 0.5 |
| results.persistence_baseline.HbA1c(%)_MAE.std | 0.1152 |
| results.persistence_baseline.FBS (mg/dL)_MAE.mean | 15.08 |
| results.persistence_baseline.FBS (mg/dL)_MAE.std | 2.172 |
| results.persistence_baseline.PPBS (mg/dL)_MAE.mean | 19.88 |
| results.persistence_baseline.PPBS (mg/dL)_MAE.std | 2.2121 |
| results.persistence_baseline.risk_accuracy.mean | 0.96 |
| results.persistence_baseline.risk_accuracy.std | 0.08 |
| results.persistence_baseline.risk_macro_f1.mean | 0.9556 |
| results.persistence_baseline.risk_macro_f1.std | 0.0889 |

## results\verifier

### verifier_audit.json
Original: `results\verifier\verifier_audit.json`  |  Last modified: 2026-10-03 11:55

JSON with 53 values (too large to show)

## vector_db

### index_to_metadata.json
Original: `vector_db\index_to_metadata.json`  |  Last modified: 2026-08-09 05:17

JSON list with 150 items

## verifier_data

### expanded_trap_queries.json
Original: `verifier_data\expanded_trap_queries.json`  |  Last modified: 2026-09-06 17:58

JSON list with 50 items

### synthetic_pairs.json
Original: `verifier_data\synthetic_pairs.json`  |  Last modified: 2026-09-08 12:47

JSON list with 3600 items

### trajectory_sequences.json
Original: `verifier_data\trajectory_sequences.json`  |  Last modified: 2026-10-03 11:34

JSON list with 100 items
