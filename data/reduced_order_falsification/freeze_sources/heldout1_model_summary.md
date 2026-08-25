# Held-Out Model Summary

## Locked Model
- E feature formula trained once on the existing 96-cell full-grid outputs.
- Held-out outcomes were not used for fitting or threshold selection.
- Locked gate used exactly the three specified non-benefit regimes.

## Standardized Linear E Coefficients
- intercept: 0.218146099
- frame_energy_relief: 0.0445620688 (standardized feature space)
- frame_abs_relief: -0.123086824 (standardized feature space)
- osc_change_pct: -0.187594501 (standardized feature space)
- edot_change_pct: 0.00182912438 (standardized feature space)
- tail_delta: -0.0663546114 (standardized feature space)
- corner_or_piecewise: 0.00435889769 (standardized feature space)
- branch_ambiguity: 0.0541717905 (standardized feature space)

## Metrics
- n cells: 56
- benefit / non-benefit count: 48 / 8
- sign accuracy: 0.928571
- balanced accuracy: 0.802083
- false benefit: 3
- false harm: 1
- R2: 0.593473
- MAE: 0.117796
- per-trajectory accuracy: `{"circle": 0.9285714285714286, "lemniscate": 1.0, "square": 1.0, "zigzag": 0.7857142857142857}`
- per-delay accuracy: `{"12": 0.875, "22": 1.0, "30": 1.0, "4": 0.875, "40": 1.0, "50": 1.0, "62": 0.75}`
- per-tr accuracy: `{"0.25": 0.8928571428571429, "0.35": 0.9642857142857143}`
