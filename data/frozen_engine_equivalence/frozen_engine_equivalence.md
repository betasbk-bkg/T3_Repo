# Frozen-Engine Equivalence

Status: passed for q=8 selected conditions.

## Purpose

The quantizer structural pilot used instrumentation beyond the original public engine. Before using the result in an manuscript, q=8 must be checked against the frozen original implementation.

## Method

The final-gate script builds a frozen-compatible instrumented engine using:

- original `adversary_ladder` trajectory classes;
- original q=8 direction vectors `AL.DIRS`;
- original q=8 angle bins `AL.DA`;
- original `_honest_block` for q=8;
- the same T3 public-history rule used in `t3_confirmatory.sim_u`;
- identical seed, trajectory, delay, minority fraction, and frame count.

The check compares RMSE values against `t3_confirmatory.sim_u` for:

```text
trajectories = circle, square, zigzag, lemniscate
tr = {0.25, 0.35}
delay = {12, 34}
rep = {0, 1, 2, 3}
modes = {T3, honest}
```

Total comparisons:

```text
128
```

## Result

Maximum absolute RMSE difference:

```text
4.440892098500626e-16
```

By trajectory and mode:

| Trajectory | Mode | Count | Mean abs diff | Max abs diff |
|---|---|---:|---:|---:|
| circle | T3 | 16 | 3.469447e-18 | 5.551115e-17 |
| circle | honest | 16 | 0 | 0 |
| lemniscate | T3 | 16 | 1.387779e-17 | 2.220446e-16 |
| lemniscate | honest | 16 | 6.938894e-17 | 4.440892e-16 |
| square | T3 | 16 | 1.734723e-17 | 2.220446e-16 |
| square | honest | 16 | 0 | 0 |
| zigzag | T3 | 16 | 0 | 0 |
| zigzag | honest | 16 | 5.551115e-17 | 2.220446e-16 |

## Boundary

This equivalence applies to the final-gate frozen-compatible instrumented engine in this folder. It does not retroactively convert older replay logs into per-agent vote-switch logs.

This file records a frozen-compatible final-gate rerun used for engine-equivalence context. The final manuscript statistics are documented in the structural-audit and base-condition reanalysis tables.

## Verdict

```text
FROZEN_ENGINE_EQUIVALENCE_PASSED
```

