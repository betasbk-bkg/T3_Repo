# Supplementary Information S1. Reduced-Order Closure Falsification Details

## Role of this supplement

The reduced-order route is included to document a frozen closure attempt that failed on heldout3. It is not a primary contribution, not a validation result, and not a theorem. It explains why the manuscript moves from predictive reduced-order closure to a hybrid obstruction framework.

## Sign convention

The reduced-order route uses one sign convention throughout:

`gap = RMSE_honest - RMSE_intervention.`

Therefore:

- `gap > 0`: intervention benefit;
- `gap <= 0`: harm or non-benefit.

A predicted benefit means `gap_hat > 0`. An observed benefit means the measured gap is positive under the same convention.

## Data lineage and freeze status

| Dataset or file | Purpose | Fitted? | Used for heldout3 outcome inspection before freeze? | Status |
|---|---|---:|---:|---|
| `original_96` | original grid and locked E-model source | yes, before v3 residual correction | no | development |
| `heldout1_56`, `heldout2_80` | development extension for v3 residual correction | yes | no | development |
| `heldout3` | frozen held-out evaluation of the v3 correction | no | no | held out until coefficients were frozen |
| `frozen_v3_coefficients.json` | frozen residual-correction coefficients and standardization constants | no, stored result only | no | frozen before heldout3 |
| `development_v3_calibration_table.csv` | calibration table used to freeze v3 coefficients | yes | no | 232 development rows |

The coefficient packet reports `n_training_cells = 232` over `original_96, heldout1_56, heldout2_80`. No threshold tuning, refit, gate addition, or trajectory-specific adjustment was performed on heldout3.

This repository archive includes the reduced-order freeze sources under `data/reduced_order_falsification/freeze_sources/`, including `frozen_v3_coefficients.json` and `development_v3_calibration_table.csv`.

## Feature equations

The two v3 diagnostic features were specified before heldout3 evaluation as reduced-order physical summaries. The small denominator constant is fixed at `epsilon = 1e-12`, and the response horizon is fixed from engine dynamics:

`H = ceil(1 / SMOOTH).`

With the engine value `SMOOTH = alpha = 0.2`, the reduced-order response horizon is `H = 5` frames. This horizon is not outcome-tuned and is distinct from the proof-oriented replay horizon `tau_frames = 18`.

`RCOAI = mean_f O_f Rbar_f / (mean_f |r_f| + 1e-12).`

`CTPI = sum_f ||Delta u_f|| K_f P_f / sum_f ||Delta u_f||.`

Here `O_f` denotes the overshoot-availability or correctability state at frame `f`, `Rbar_f` is the response-horizon average of projected relief, `r_f` is the correction-scale or projected-residual denominator used by the reduced-order route, `Delta u_f` is the command perturbation, `K_f` is curvature or corner exposure, and `P_f` is the delayed phase or topology exposure. These are diagnostic reduced-order variables, not theorem terms.

## Standardization constants

The standardized features used in the frozen residual correction were:

`z_RCOAI = (RCOAI - 0.28601648253028955) / 0.4470596763218.`

`z_CTPI = (CTPI - 1.318387742696156) / 2.0299832581624586.`

Source columns:

| Feature | Source column | Mean | Standard deviation |
|---|---|---:|---:|
| `RCOAI` | `relief_consistency_overshoot_availability_index_mean` | 0.28601648253028955 | 0.4470596763218 |
| `CTPI` | `corner_turn_phase_index_mean` | 1.318387742696156 | 2.0299832581624586 |

## Frozen residual correction

The compact frozen correction was:

`gap_hat_A = gap_hat_E_locked + beta_R z_RCOAI + beta_C z_CTPI.`

with:

| Coefficient | Frozen value | Expected sign |
|---|---:|---|
| `beta_R` | 0.0028583563044266803 | `>= 0` |
| `beta_C` | 0.0 | `<= 0` |

The active-set solution retained `RCOAI` and constrained `CTPI` to zero. The target residual was `observed_gap - gap_hat_E_locked`.

## Classification rules

Sign classification used the frozen predicted gap:

- predicted benefit if `gap_hat_A > 0`;
- predicted harm or non-benefit if `gap_hat_A <= 0`;
- observed benefit if `gap > 0`;
- observed harm or non-benefit if `gap <= 0`.

A false benefit is a cell with predicted benefit but observed harm or non-benefit. A false harm is a cell with predicted harm or non-benefit but observed benefit. Balanced accuracy is the mean of benefit-class recall and harm/non-benefit-class recall under this binary split.

## Source references inside the project

| Source | What it supports |
|---|---|
| `reduceorder1st/theory_outputs_state_variables/state_variable_definitions.md` | `1e-12` denominator constant and `H = ceil(1 / SMOOTH)` response horizon |
| `reduceorder1st/theory_outputs_state_features/state_feature_computability_report.md` | dense frame computation and response horizon of 5 frames |
| `data/reduced_order_falsification/freeze_sources/v3_theory_specification_public_copy.md` | feature equations and model-form specification |
| `reduceorder1st/theory_outputs_v3_spec/v3_theory_specification.md` | sign convention, feature intent, preregistered v3 option |
| `reduceorder1st/theory_outputs_v3_spec/v3_model_form_freeze.md` | frozen model form and no-threshold/no-gate discipline |
| `reduceorder1st/theory_outputs_v3_coefficient_freeze/frozen_v3_coefficients.json` | frozen coefficients and standardization constants |
| `reduceorder1st/theory_outputs_v3_coefficient_freeze/development_v3_calibration_table.csv` | 232 development rows used for coefficient freeze |
| `reduceorder1st/theory_outputs_heldout3/` | heldout3 outcome packet after freeze |


## Main-text Table 2 lock

The main text reports the original fitted model row from `C_relief_cost_balance` in `theory_model_comparison.csv`:

- sign accuracy: `0.90625`;
- balanced accuracy: `0.75`;
- `R^2`: `0.6078980949512564`;
- `MAE`: `0.13873221826559223`.

The topology-aware model `E_topology_aware_hybrid` is retained in the provenance package but is not used for the main-text row because its metric tuple differs: sign accuracy `0.8958333333333334`, balanced accuracy `0.7435897435897436`, `R^2 = 0.6251354345473948`, and `MAE = 0.12116669701059068`.

## Interpretation

The frozen correction did not deliver held-out predictive closure. This negative result is used only as motivation for the hybrid obstruction formulation. It is not evidence that the intervention is generally ineffective, and it is not validation of the final manuscript framework.
