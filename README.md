# Data and code for projected anti-aggregate stabilization in latency-affected quantized collective control

This repository contains the code, processed data, final figures, and reproducibility checks supporting the manuscript:

**Projected anti-aggregate stabilization and mistiming-cost boundaries in latency-affected quantized collective control**

Author: **Bong-Keun Song**  
Affiliation used in the manuscript: **Friedrich-Alexander-Universität Erlangen-Nürnberg, Erlangen, Germany**

## Purpose

This package supports the numerical simulation and mechanism-closure claims in the manuscript. The study analyzes a latency-affected quantized collective-control model in which a coherent anti-aggregate minority policy, denoted T3 in the code, is compared with a same-size honest counterfactual.

The archive is intended to let reviewers and readers inspect and reproduce the main grid, closure diagnostics, diagnostic regressions, bootstrap boundary checks, and final manuscript figures.

## Key manuscript-level outputs

The included processed outputs reproduce the following headline results:

- Main closure grid: **96 cells** = 4 trajectories × 3 minority fractions × 8 control latencies.
- Monte Carlo repetitions: **MC = 50** per cell.
- The anti-aggregate minority policy improves the honest counterfactual in **78/96 cells**.
- It improves **12/12 cells** at the design latency, `d = 26` frames.
- Harm/non-benefit cells: **18**.
- Harm mechanism classes:
  - `harm_cost_dominance`: **15** cells
  - `harm_with_local_reversal`: **1** cell
  - `harm_or_neutral_unclear`: **2** cells
- Benefit counts by trajectory:
  - circle: **17/24**
  - square: **23/24**
  - lemniscate: **16/24**
  - zigzag: **22/24**

A quick consistency check can be run with:

```bash
python code/check_key_numbers.py
```

## Directory structure

```text
code/
  core/
    adversary_ladder.py           # simulation engine and trajectory definitions
    t3_confirmatory.py            # confirmatory grid and ablation experiments
  analysis/
    t3_closure_probe.py           # frame-level closure diagnostic grid
    t3_closure_regression.py      # second-pass diagnostic regression/classification
    t3_closure_bootstrap.py       # raw-run bootstrap checks for boundary cells
  auxiliary/
    t3_theorem.py                 # reduced-order theoretical checks
    t3_zeta.py                    # damping-ratio diagnostic helper
    t3_quant_ablation.py          # quantization-related auxiliary analysis
    t3_strengthen.py              # strengthening diagnostics
    t3_energy_probe.py            # energy/projection diagnostic helper
  check_key_numbers.py            # verifies headline numbers from included outputs

data/
  processed/
    t3_closure_probe_summary.csv/json
    t3_closure_bootstrap_summary.csv/json
    t3_energy_probe_rows.json
    key_reproducibility_metrics.json
  tables/
    closure_second_pass_report.md
    diagnostic_regression_models.csv
    diagnostic_regression_mixed_model.csv
    benefit_harm_classifier_models.csv
    mechanism_counts.csv
    trajectory_summary.csv
    latency_summary.csv
    tr_summary.csv
    key_boundary_cells.csv

figures/
  Figure_1.png ... Figure_7.png   # final manuscript figures

metadata/
  ZENODO_DESCRIPTION.md
  zenodo_metadata_template.json
  CITATION.cff
  RELEASE_NOTES.md
  LICENSE_RECOMMENDATION.md
```

## Environment

The scripts are pure Python and were prepared for Python 3.10+.

Install the recommended dependencies with:

```bash
python -m pip install -r requirements.txt
```

The most important dependencies are `numpy`, `pandas`, `scipy`, `matplotlib`, `scikit-learn`, and `statsmodels`.

## Reproduction workflow

The included processed outputs are the outputs supporting the current manuscript. To verify them, run:

```bash
python code/check_key_numbers.py
```

To regenerate the full closure grid from the simulation engine, run from the package root:

```bash
cd code/analysis
python t3_closure_probe.py full
```

This writes new outputs to a `results/` directory relative to the script location. Runtime depends on hardware.

To regenerate the second-pass closure analysis from the included summary file:

```bash
cd code/analysis
python t3_closure_regression.py --input ../../data/processed/t3_closure_probe_summary.json --out ../../data/tables_regenerated
```

To regenerate bootstrap checks for selected boundary cells:

```bash
cd code/analysis
python t3_closure_bootstrap.py boundary --mc 50 --boot 1000
```

To run a quick smoke test of the confirmatory simulation script:

```bash
cd code/core
python t3_confirmatory.py quick
```

The full confirmatory grid is more expensive:

```bash
cd code/core
python t3_confirmatory.py full
```

## Notes on final figures

The `figures/` directory contains the final figures associated with the current manuscript version. Some auxiliary scripts were produced during theory-development stages and are retained for computational provenance. The final interpretation is not physical speed damping; it is projected local error relief under normalized vector-mean aggregation, with global benefit/harm determined by cost-dominance boundaries.

## DOI update instruction

After Zenodo archival, cite the final **version-specific Zenodo DOI** in the manuscript Data Availability statement.
