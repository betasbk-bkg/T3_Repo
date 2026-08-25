# Heldout3 Execution Packet

## Frozen Primary Model
Use v3 Option A as the primary model:

```text
gap_hat_A = gap_hat_E_locked + beta_R * z_RCOAI + beta_C * z_CTPI
```

where:

- beta_R = 0.00285835630443
- beta_C = 0
- z_RCOAI = (RCOAI - 0.28601648253) / 0.447059676322
- z_CTPI = (CTPI - 1.3183877427) / 2.02998325816

DBPI remains exploratory only and is not part of the primary heldout3 decision rule.

## Frozen Standardization Statistics
Standardization was computed only from original_96 + heldout1_56 + heldout2_80:

```json
{
  "features": {
    "CTPI": {
      "column": "corner_turn_phase_index_mean",
      "mean": 1.318387742696156,
      "std": 2.0299832581624586
    },
    "RCOAI": {
      "column": "relief_consistency_overshoot_availability_index_mean",
      "mean": 0.28601648253028955,
      "std": 0.4470596763218
    }
  },
  "source": "v3 development set only"
}
```

## Heldout3 Grid
Use the heldout3 grid from `theory_outputs_v3_spec/heldout3_held-out evaluation_plan.md`:

- trajectories: circle, square, lemniscate, zigzag
- tr values: 0.225, 0.325, 0.425
- delays: 1, 5, 9, 16, 24, 36, 52, 66
- MC: 50
- total cells: 4 trajectories * 3 tr values * 8 delays = 96 cells

## Success Criteria
For v3 heldout3 support, the frozen primary model must satisfy:

```text
balanced accuracy >= 0.85
false benefit <= 3
false harm <= 3
no single trajectory sign accuracy < 0.80
expected coefficient signs preserved
```

No post-hoc gates, threshold tuning, coefficient changes, trajectory corrections, or heldout3-driven feature changes are allowed.
