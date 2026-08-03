# Stream-Separated CRN Final Gate Protocol

Status: pre-run correction of the CRN repair.

## Purpose

This folder repeats the common-random-number final gate with explicit RNG-stream separation:

- honest-agent noise is pre-generated and shared by T3 and honest;
- honest-counterfactual troll noise is generated from a separate stream;
- q4, q8, and q16 share the same base condition noise schedules;
- event-class interaction is tested at the simulation-cluster level;
- sparse event classes are treated as descriptive only.

## Relation To Folder 46

Folder 46 repaired the main pairing problem. This folder makes the repair stricter by using separate child streams for honest-agent noise and troll-counterfactual noise.

The frozen q=8 engine equivalence result remains in folder 45. This stream-separated CRN analysis is a sensitivity/audit design, not a bitwise reproduction of the frozen stochastic engine.

## Fixed Axes

```text
q_dirs = {4, 8, 16}
trajectories = {circle, square, zigzag, lemniscate}
delays = {12, 34}
minority fractions = {0.25, 0.35}
MC = 8
frames = 1800
```

## Claim Boundary

This folder may strengthen:

- frequency-magnitude trade-off;
- separable vote/path obstruction channels;
- non-additive event interaction.

It must not claim:

- validation;
- global RMSE closure;
- universal monotone quantizer law;
- theorem constants from observed simulation values.

