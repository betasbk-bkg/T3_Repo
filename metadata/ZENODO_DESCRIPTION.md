# Zenodo description text

This archive provides the reproducibility package for the manuscript **“Projected anti-aggregate stabilization and mistiming-cost boundaries in latency-affected quantized collective control.”**

The study investigates a latency-affected quantized collective-control model in which many agents steer a fixed-speed point agent by vector-mean aggregation of directional votes. The main tested minority policy, T3, votes opposite to the previous public aggregate and is compared with a same-size honest counterfactual. The package contains the simulation engine, confirmatory and closure-analysis scripts, diagnostic regression/classification outputs, bootstrap boundary checks, final manuscript figures, and submission-reference files.

The main closure grid covers 4 trajectories, 3 minority fractions, and 8 control-latency values, giving 96 cells with MC=50 repetitions per cell. The included outputs reproduce the headline results reported in the manuscript: T3 improves the honest counterfactual in 78/96 cells, improves all 12 cells at the design latency d=26 frames, and the 18 harm/non-benefit cells are mostly explained by cost-dominance rather than reversal of the local relief channel. Specifically, the second-pass mechanism classification gives 78 benefit cells, 15 harm-cost-dominance cells, 2 harm/neutral unclear cells, and 1 harm cell with local-relief reversal.

The package is organized as follows: `code/` contains the simulation and analysis scripts; `data/processed/` contains closure and bootstrap summaries; `data/tables/` contains diagnostic-regression, classification, and summary tables; `figures/` contains final manuscript figures; `manuscript_submission_reference/` contains the corresponding manuscript, highlights, and cover-letter files; and `metadata/` contains citation, release, license, and Zenodo-description templates.

A quick consistency check can be run with:

```bash
python code/check_key_numbers.py
```

This archive is intended for manuscript review and exact reproducibility of the submitted numerical results. After Zenodo assigns a DOI, the DOI should be inserted into the manuscript Data Availability statement.

## Suggested keywords

nonlinear simulation; collective control; feedback latency; quantized voting; vector aggregation; anti-aggregate minority; reduced-order model; mechanism validation; bootstrap; reproducibility
