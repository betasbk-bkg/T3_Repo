# Package manifest

This manifest maps the archive files to manuscript claims and reproducibility tasks.

## Manuscript claim mapping

| Manuscript item | Supporting files |
|---|---|
| 96-cell grid: 4 trajectories × 3 minority fractions × 8 latencies, MC=50 | `data/processed/t3_closure_probe_summary.csv`, `data/processed/t3_closure_probe_summary.json`, `code/analysis/t3_closure_probe.py` |
| 78/96 benefit cells and 18 harm/non-benefit cells | `data/processed/key_reproducibility_metrics.json`, `code/check_key_numbers.py` |
| 12/12 benefit cells at design latency d=26 | `data/processed/t3_closure_probe_summary.json`, `code/check_key_numbers.py` |
| Mechanism classes: 78 benefit, 15 harm-cost-dominance, 2 unclear, 1 local-relief reversal | `data/tables/mechanism_counts.csv`, `data/processed/key_reproducibility_metrics.json` |
| Trajectory-level benefit counts: circle 17/24, square 23/24, lemniscate 16/24, zigzag 22/24 | `data/tables/trajectory_summary.csv`, `code/check_key_numbers.py` |
| Diagnostic regression and LOOCV comparisons | `data/tables/diagnostic_regression_models.csv`, `data/tables/diagnostic_regression_mixed_model.csv`, `code/analysis/t3_closure_regression.py` |
| Benefit/harm classifier results | `data/tables/benefit_harm_classifier_models.csv`, `code/analysis/t3_closure_regression.py` |
| Boundary cells and cost-dominance diagnostics | `data/tables/key_boundary_cells.csv`, `data/processed/t3_closure_bootstrap_summary.csv/json`, `code/analysis/t3_closure_bootstrap.py` |
| Reduced-order and local mechanism checks | `code/auxiliary/t3_theorem.py`, `code/auxiliary/t3_zeta.py`, `code/auxiliary/t3_energy_probe.py`, `data/processed/t3_energy_probe_rows.json` |
| Final manuscript figures | `figures/Figure_1.png` through `figures/Figure_7.png` |
| Submitted manuscript version | `manuscript_submission_reference/T3_CNSNS_Manuscript_CBI_REFBOOST_FINALCHECK.docx` |
| Highlights and cover letter | `manuscript_submission_reference/T3_CNSNS_Highlights_CBI_REFBOOST_FINALCHECK.docx`, `manuscript_submission_reference/T3_CNSNS_Cover_Letter_CBI_REFBOOST_FINALCHECK.docx` |

## Code files

### `code/core/`

- `adversary_ladder.py`: base engine, trajectories, vote quantization, honest and minority vote blocks.
- `t3_confirmatory.py`: confirmatory grid and auxiliary ablations.

### `code/analysis/`

- `t3_closure_probe.py`: main closure grid and frame-level diagnostics.
- `t3_closure_regression.py`: second-pass regression/classification analysis from closure outputs.
- `t3_closure_bootstrap.py`: raw-run bootstrap confidence intervals for selected or full closure cells.

### `code/auxiliary/`

- `t3_theorem.py`: reduced-order theoretical checks.
- `t3_zeta.py`: damping-ratio diagnostic helper.
- `t3_quant_ablation.py`: quantization-related auxiliary analysis.
- `t3_strengthen.py`: additional diagnostic checks from the strengthening stage.
- `t3_energy_probe.py`: local energy/projection diagnostic helper.

### Root-level check

- `code/check_key_numbers.py`: lightweight consistency test for the headline results in the included processed outputs.

## Data files

### `data/processed/`

- `t3_closure_probe_summary.csv/json`: full 96-cell closure summary.
- `t3_closure_bootstrap_summary.csv/json`: bootstrap summary for closure/boundary cells.
- `t3_energy_probe_rows.json`: energy/projection probe rows.
- `key_reproducibility_metrics.json`: headline count summary extracted from the closure grid.

### `data/tables/`

- `closure_second_pass_report.md`: text report from second-pass closure analysis.
- `diagnostic_regression_models.csv`: regression model comparison.
- `diagnostic_regression_mixed_model.csv`: mixed-model regression summary.
- `benefit_harm_classifier_models.csv`: benefit/harm classification model comparison.
- `mechanism_counts.csv`: mechanism-class counts.
- `trajectory_summary.csv`: trajectory-level summary.
- `delay_summary.csv`: latency-level summary.
- `tr_summary.csv`: minority-fraction summary.
- `key_boundary_cells.csv`: selected boundary cells and diagnostics.

## Files intentionally not used as final figure generators

Earlier draft figure scripts that used superseded terminology such as physical velocity damping are not used for the final CNSNS figure set. The final manuscript interpretation is projected local error relief after vector normalization, not physical speed damping.
