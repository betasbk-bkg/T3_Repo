# Held-Out 2 Model Summary

## Locked Model And Gate
- E coefficients are the held-out 1 locked standardized coefficients; no E-model fitting is performed here.
- Standardization statistics are from the existing 96-cell full-grid training data.
- Held-out 2 outcomes are not used for fitting or threshold selection.
- Gate = original locked gate + exactly one pre-specified zigzag geometric-cost gate.

## Locked E Coefficients
- intercept: 0.218146099
- frame_energy_relief: 0.0445620688 (locked standardized coefficient)
- frame_abs_relief: -0.123086824 (locked standardized coefficient)
- osc_change_pct: -0.187594501 (locked standardized coefficient)
- edot_change_pct: 0.00182912438 (locked standardized coefficient)
- tail_delta: -0.0663546114 (locked standardized coefficient)
- corner_or_piecewise: 0.00435889769 (locked standardized coefficient)
- branch_ambiguity: 0.0541717905 (locked standardized coefficient)

## Metrics
- n cells: 80
- benefit / non-benefit count: 65 / 15
- sign accuracy: 0.875000
- balanced accuracy: 0.794872
- false benefit: 5
- false harm: 5
- R2: 0.572526
- MAE: 0.150206
- min trajectory accuracy: 0.800000
- per-trajectory accuracy: `{"circle": 0.85, "lemniscate": 0.9, "square": 0.95, "zigzag": 0.8}`
- per-delay accuracy: `{"10": 0.875, "14": 0.625, "2": 0.625, "20": 1.0, "28": 1.0, "38": 1.0, "46": 1.0, "58": 1.0, "6": 0.75, "64": 0.875}`
- per-tr accuracy: `{"0.275": 0.9, "0.375": 0.85}`
