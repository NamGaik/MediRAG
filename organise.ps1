# organise.ps1 - reorganises the MediRAG folder for GitHub.
# RUN THIS ON A COPY of the MediRAG folder, not the original.
# Usage (from inside the copied MediRAG folder):
#   powershell -ExecutionPolicy Bypass -File organise.ps1

$ErrorActionPreference = "Stop"

function Move-Files($files, $dest) {
    if (-not (Test-Path $dest)) { New-Item -ItemType Directory -Path $dest | Out-Null }
    foreach ($f in $files) {
        if (Test-Path $f) {
            Move-Item -Path $f -Destination $dest
            Write-Host "moved  $f  ->  $dest/"
        } else {
            Write-Host "skip   $f  (not found)" -ForegroundColor Yellow
        }
    }
}

# 1. Main pipeline, in run order
$pipeline = @(
    "generate_reports.py",
    "convert_and_degrade.py",
    "ocr_extract_and_evaluate.py",
    "phase_c_preprocessing.py",
    "phase_d_1_embedding.py",
    "phase_d_2_label_check.py",
    "phase_ef_vectorDB.py",
    "phase_g_generation.py",
    "phase_h_validation.py",
    "phase_i_neural_verifier.py",
    "phase_i_2_verifier_audit.py",
    "phase_j_1_trajectory_model.py",
    "phase_j_2_baselines.py",
    "phase_k_explainability.py",
    "phase_l_1_trap_expansion.py",
    "phase_l_2_benchmark.py",
    "phase_l_4_audit_benchmark.py",
    "phase_l_6_benchmark_v2.py",
    "phase_l_7_labels_v2.py",
    "phase_l_8_rescore_rules_v2.py",
    "phase_l_normalise_rule_metrix.py",
    "phase_l_rescore_rules.py",
    "phase_l_rescore_verifier.py",
    "results_logger.py"
)
Move-Files $pipeline "pipeline"

# 2. Helper scripts: checks and paper figures
$scripts = @(
    "check.py",
    "check_forecasts.py",
    "check_forecasts_v2.py",
    "check_retrieval.py",
    "collect_results.py",
    "count_changes.py",
    "generate_chart_fig6_v2.py",
    "generate_chart_trajectoryEg.py",
    "generate_chart_trap_safety.py",
    "generate_chart_v2_results.py",
    "generate_chart_verifier_comparison.py"
)
Move-Files $scripts "scripts"

# 3. Old / debug / empty files - kept in archive/ so nothing is lost
$archive = @(
    "phase_k_explainability_OLD.py",
    "phase_l_2_benchmark_ORIGINAL.py",
    "phase_l_3_debug_verifier.py"
)
Move-Files $archive "archive"

# 4. Clear compiled caches (they are regenerated automatically)
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force

Write-Host ""
Write-Host "Done. Any .py files still in the root were not in the lists above:" -ForegroundColor Green
Get-ChildItem -File -Filter "*.py" | ForEach-Object { Write-Host "  $($_.Name)" }
