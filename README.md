# T3 CNSNS reproducibility package

This archive contains code, processed outputs, manuscript figures, and submission-reference files for the manuscript:

**Projected anti-aggregate stabilization and mistiming-cost boundaries in latency-affected quantized collective control**

Author: **Bong-Keun Song**  
Affiliation used in the manuscript: **CBI, Friedrich-Alexander-Universität Erlangen-Nürnberg, Erlangen, Germany**

## Purpose

This package supports the numerical simulation and mechanism-closure claims in the manuscript. The study analyzes a latency-affected quantized collective-control model in which a coherent anti-aggregate minority policy, T3, is compared with a same-size honest counterfactual.

The package is intended to let reviewers and readers inspect and reproduce the main grid, closure diagnostics, diagnostic regressions, bootstrap boundary checks, and final manuscript figures.

## Key manuscript-level outputs

The included processed outputs reproduce the following headline results:

- Main closure grid: **96 cells** = 4 trajectories × 3 minority fractions × 8 control latencies.
- Monte Carlo repetitions: **MC = 50** per cell.
- T3 improves the honest counterfactual in **78/96 cells**.
- T3 improves **12/12 cells** at the design latency, `d = 26` frames.
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
    t3_strengthen.py              # earlier strengthening diagnostics
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
    delay_summary.csv
    tr_summary.csv
    key_boundary_cells.csv

figures/
  Figure_1.png ... Figure_7.png   # final CNSNS submission figures

manuscript_submission_reference/
  T3_CNSNS_Manuscript_CBI_REFBOOST_FINALCHECK.docx
  T3_CNSNS_Highlights_CBI_REFBOOST_FINALCHECK.docx
  T3_CNSNS_Cover_Letter_CBI_REFBOOST_FINALCHECK.docx

metadata/
  ZENODO_DESCRIPTION.md
  zenodo_metadata_template.json
  CITATION.cff
  RELEASE_NOTES.md
  LICENSE_RECOMMENDATION.md

checksums/
  SHA256SUMS.txt
```

## Environment

The scripts are pure Python and were prepared for Python 3.10+.

Install the recommended dependencies with:

```bash
python -m pip install -r requirements.txt
```

The most important dependencies are `numpy`, `pandas`, `scipy`, `matplotlib`, `scikit-learn`, and `statsmodels`.

## Reproduction workflow

The included processed outputs are the exact outputs used for the current CNSNS submission package. To verify them, run:

```bash
python code/check_key_numbers.py
```

To regenerate the full closure grid from the simulation engine, run from the package root:

```bash
cd code/analysis
python t3_closure_probe.py full
```

This writes new outputs to a `results/` directory relative to the script location. Runtime depends on hardware.

To regenerate the second-pass closure analysis from the included summary file, either copy the included summary file into the expected `results/` path or pass it explicitly:

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

The `figures/` directory contains the final publication figures used in the CNSNS submission package. Some auxiliary scripts in this project were produced during earlier theory-development stages and are retained for computational provenance. The final manuscript interpretation is not physical speed damping; it is projected local error relief under normalized vector-mean aggregation, with global benefit/harm determined by cost-dominance boundaries.

## DOI update instruction

Before journal submission, update the manuscript's Data Availability statement with the final **version-specific Zenodo DOI** generated after upload. If the Zenodo record also gives a concept DOI, prefer the version DOI for exact reproducibility in the manuscript.

## Suggested citation

After the Zenodo upload, replace `TBD` fields in `metadata/CITATION.cff` and the manuscript Data Availability statement with the final DOI.
