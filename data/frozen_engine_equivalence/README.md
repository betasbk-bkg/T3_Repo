# Fixed-Engine Equivalence and Structural Final Gate

Status: completed fixed-engine equivalence and structural audit.

This folder records the check that the selected q=8 instrumented path remains compatible with the fixed engine, followed by the structural q/vote/path audit used by the manuscript.

## Design Summary

```text
frozen q=8 equivalence comparisons: 128
structural paired condition rows: 384
underlying simulations: 768
T3 vote-event rows with paired honest counterfactual: 38,400
```

Fixed axes:

```text
q_dirs = {4, 8, 16}
trajectories = {circle, square, zigzag, lemniscate}
delays = {12, 34}
minority fractions = {0.25, 0.35}
MC = 8
frames = 1800
```

## Interpretation

The outputs support a frequency-burden trade-off and non-additive vote/path event-cost associations in the fixed implementation. They do not provide a closed monotone switching-cost law, independent plant transfer, or a global RMSE theorem.

## Key Files

- `frozen_engine_equivalence.csv`
- `final_gate_q_summary.csv`
- `final_gate_directional_tests.csv`
- `final_gate_cluster_bootstrap_ci.csv`
- `final_gate_coarse_fine_contrast_ci.csv`
- `final_gate_condition_consistency.csv`
- `final_gate_q_event_interaction.csv`
- `counterfactual_event_cost_audit.md`
- `revised_systems_principle.md`
