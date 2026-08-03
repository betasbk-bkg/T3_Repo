# Heldout3 Model Summary

## Frozen Model Discipline
- This is the single heldout3 run for frozen v3 Option A.
- No coefficients were changed.
- No gates were added.
- No thresholds were tuned.
- DBPI was not used for the primary decision.

## Frozen Option A Formula
```text
gap_hat_A = gap_hat_E_locked + beta_R * z_RCOAI + beta_C * z_CTPI
```

- beta_R: 0.00285835630443
- beta_C: 0
- RCOAI mean/std: 0.28601648253 / 0.447059676322
- CTPI mean/std: 1.3183877427 / 2.02998325816

## Primary V3 Metrics
- n cells: 96
- benefit / non-benefit count: 77 / 19
- sign accuracy: 0.854167
- balanced accuracy: 0.691046
- false benefit: 11
- false harm: 3
- R2: 0.611735
- MAE: 0.147803
- per-trajectory accuracy: `{"circle": 0.7083333333333334, "lemniscate": 0.875, "square": 0.9166666666666666, "zigzag": 0.9166666666666666}`
- per-delay accuracy: `{"1": 0.5, "16": 0.9166666666666666, "24": 1.0, "36": 1.0, "5": 0.75, "52": 0.8333333333333334, "66": 0.8333333333333334, "9": 1.0}`
- per-tr accuracy: `{"0.225": 0.8125, "0.325": 0.8125, "0.425": 0.9375}`

## Locked E Baseline Reference
- sign accuracy: 0.854167
- balanced accuracy: 0.691046
- false benefit: 11
- false harm: 3
- R2: 0.613093
- MAE: 0.147674

## Error Count
- primary v3 sign errors: 14
- verdict: HELDOUT3_FAILS_CURRENT_THEORY
