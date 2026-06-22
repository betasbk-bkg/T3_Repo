# T3 closure probe: second-pass diagnostic analysis

Input: `t3_closure_probe_summary.json`  
Cells: 96 = 4 trajectories × 3 minority fractions × 8 delays  
MC per cell: 50

## 1. Mechanism classes

| mechanism_class          |   n |
|:-------------------------|----:|
| benefit                  |  78 |
| harm_cost_dominance      |  15 |
| harm_or_neutral_unclear  |   2 |
| harm_with_local_reversal |   1 |

## 2. Trajectory-level benefit/harm counts

| traj       |   n |   benefit |   harm |   mean_gap |   mean_osc_change |   mean_tail_delta |
|:-----------|----:|----------:|-------:|-----------:|------------------:|------------------:|
| circle     |  24 |        17 |      7 |      0.186 |            -5.759 |            -0.009 |
| lemniscate |  24 |        16 |      8 |      0.188 |             8.411 |             0.096 |
| square     |  24 |        23 |      1 |      0.311 |           -18.951 |            -0.029 |
| zigzag     |  24 |        22 |      2 |      0.188 |            -8.848 |            -0.015 |

## 3. Delay-level benefit/harm counts

|   delay |      n |   benefit |   harm |   mean_gap |   mean_osc_change |   mean_tail_delta |
|--------:|-------:|----------:|-------:|-----------:|------------------:|------------------:|
|   0.000 | 12.000 |     5.000 |  7.000 |      0.031 |            20.520 |             0.052 |
|   8.000 | 12.000 |     8.000 |  4.000 |     -0.080 |            16.494 |             0.125 |
|  18.000 | 12.000 |    10.000 |  2.000 |      0.083 |            -8.442 |             0.045 |
|  26.000 | 12.000 |    12.000 |  0.000 |      0.252 |           -20.229 |            -0.037 |
|  34.000 | 12.000 |    12.000 |  0.000 |      0.344 |           -24.284 |            -0.033 |
|  44.000 | 12.000 |    10.000 |  2.000 |      0.263 |            -7.679 |            -0.005 |
|  56.000 | 12.000 |    11.000 |  1.000 |      0.372 |           -11.179 |            -0.028 |
|  68.000 | 12.000 |    10.000 |  2.000 |      0.479 |           -15.495 |            -0.031 |

## 4. Diagnostic regression: explaining the RMSE gap

Target: `gap_h_minus_t3`, where positive means T3 improves over honest.

| model                                 |   r2_in_sample |   r2_loocv |   mae_loocv |
|:--------------------------------------|---------------:|-----------:|------------:|
| local_relief_only                     |          0.103 |      0.052 |       0.225 |
| cost_terms_only                       |          0.584 |      0.535 |       0.150 |
| relief_plus_cost                      |          0.648 |      0.587 |       0.140 |
| relief_abs_plus_cost                  |          0.656 |      0.603 |       0.139 |
| relief_cost_with_projection_magnitude |          0.681 |      0.620 |       0.137 |

Mixed model:

| model                            |   r2_in_sample |   r2_loocv |   mae_loocv |
|:---------------------------------|---------------:|-----------:|------------:|
| relief_plus_cost_plus_delay_traj |          0.808 |      0.727 |       0.104 |

## 5. Benefit/harm classification

Positive class = T3 benefit.

| model                      |   auc_loocv |   accuracy_loocv |   balanced_accuracy_loocv | confusion_matrix   |
|:---------------------------|------------:|-----------------:|--------------------------:|:-------------------|
| local_relief_only          |       0.115 |            0.812 |                     0.500 | [[0, 18], [0, 78]] |
| cost_terms_only            |       0.991 |            0.927 |                     0.827 | [[12, 6], [1, 77]] |
| relief_plus_cost           |       0.991 |            0.917 |                     0.799 | [[11, 7], [1, 77]] |
| relief_plus_cost_plus_traj |       0.985 |            0.927 |                     0.827 | [[12, 6], [1, 77]] |

## 6. Key boundary cells

| traj       |    tr |   delay |   gap_h_minus_t3 |   energy_relief |   abs_relief |   osc_change_pct |   edot_change_pct |   tail_delta | mechanism_class          |
|:-----------|------:|--------:|-----------------:|----------------:|-------------:|-----------------:|------------------:|-------------:|:-------------------------|
| circle     | 0.200 |       0 |           -0.060 |           0.556 |        0.345 |            1.497 |            19.835 |        0.081 | harm_cost_dominance      |
| circle     | 0.200 |      34 |            0.223 |           0.975 |        0.895 |          -24.088 |           -11.906 |       -0.036 | benefit                  |
| circle     | 0.200 |      44 |           -0.239 |           0.981 |        0.925 |           40.684 |            46.609 |        0.095 | harm_cost_dominance      |
| circle     | 0.200 |      56 |            0.277 |           0.969 |        0.878 |          -20.478 |           -11.448 |       -0.047 | benefit                  |
| circle     | 0.300 |       0 |           -0.030 |           0.418 |        0.290 |           14.899 |            92.239 |        0.051 | harm_cost_dominance      |
| circle     | 0.300 |      34 |            0.329 |           0.585 |        0.420 |          -31.199 |            -8.697 |       -0.047 | benefit                  |
| circle     | 0.300 |      44 |           -0.193 |           0.657 |        0.550 |           37.114 |            50.888 |        0.080 | harm_cost_dominance      |
| circle     | 0.300 |      56 |           -0.007 |           0.610 |        0.496 |           19.268 |            26.301 |        0.028 | harm_cost_dominance      |
| circle     | 0.400 |       0 |           -0.003 |           0.567 |        0.408 |           14.111 |           196.055 |        0.003 | harm_cost_dominance      |
| circle     | 0.400 |       8 |           -0.005 |           0.522 |        0.366 |            6.887 |           112.806 |        0.011 | harm_cost_dominance      |
| circle     | 0.400 |      34 |            0.679 |           0.270 |        0.127 |          -67.371 |            21.375 |       -0.050 | benefit                  |
| circle     | 0.400 |      44 |            0.256 |           0.278 |        0.175 |          -12.952 |            39.088 |       -0.033 | benefit                  |
| circle     | 0.400 |      56 |            0.200 |           0.239 |        0.170 |            9.428 |            37.161 |       -0.023 | benefit                  |
| lemniscate | 0.200 |       0 |           -0.092 |           0.018 |       -0.016 |           42.888 |            47.649 |        0.160 | harm_cost_dominance      |
| lemniscate | 0.200 |       8 |           -0.484 |           0.987 |        0.928 |          105.145 |           781.899 |        0.464 | harm_cost_dominance      |
| lemniscate | 0.300 |       0 |           -0.130 |          -0.188 |       -0.096 |           55.592 |            51.790 |        0.222 | harm_with_local_reversal |
| lemniscate | 0.300 |       8 |           -0.658 |           0.789 |        0.549 |          139.037 |           742.595 |        0.654 | harm_cost_dominance      |
| lemniscate | 0.300 |      18 |           -0.256 |           0.881 |        0.789 |           27.319 |           711.148 |        0.351 | harm_cost_dominance      |
| lemniscate | 0.400 |       0 |           -0.121 |           0.442 |        0.316 |           54.599 |            70.501 |        0.193 | harm_cost_dominance      |
| lemniscate | 0.400 |       8 |           -0.557 |           0.660 |        0.533 |          118.052 |           751.462 |        0.560 | harm_cost_dominance      |
| lemniscate | 0.400 |      18 |           -0.243 |           0.654 |        0.396 |           23.455 |           749.754 |        0.382 | harm_cost_dominance      |
| square     | 0.400 |       0 |           -0.021 |           0.511 |        0.372 |           73.710 |           221.055 |        0.048 | harm_cost_dominance      |
| zigzag     | 0.200 |      68 |           -0.007 |           0.761 |        0.632 |            2.433 |            -8.996 |        0.006 | harm_or_neutral_unclear  |
| zigzag     | 0.300 |      68 |           -0.163 |           0.697 |        0.578 |            6.902 |            -6.309 |        0.026 | harm_or_neutral_unclear  |

## Suggested manuscript claim

Frame-level diagnostics do not show that the harm bands are primarily caused by a reversal of the local relief channel. Instead, most harm cells retain positive local relief but exhibit increased oscillation, error-derivative variation, and/or high-error tail rate. The appropriate mechanism statement is therefore:

> T3 provides a projected local error-relief channel. Global RMSE benefit occurs when this relief exceeds mistiming-induced oscillation, jitter, tail, and topology costs. Harm bands are mainly cost-dominance boundaries, not phase-reversal boundaries.
