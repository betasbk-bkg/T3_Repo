# Revised Systems Principle

Status: Systems-facing central principle after the final gate.

## Rejected Simple Principle

Do not center the paper on:

```text
Coarser quantization is worse.
```

The final-gate results do not support that as a universal monotone law.

## Stronger Principle

Use:

```text
Quantizer refinement produces a frequency-magnitude trade-off, while path and vote events form separable but non-additive hybrid obstruction channels; consequently, smooth local relief cannot be closed by a single monotone switching-cost law.
```

## Why This Is Stronger

This principle explains both positive and negative results:

- smooth local relief remains valid under its assumptions;
- square corners supply a true path-transition charge;
- zigzag retains interior/event topology obstructions;
- lemniscate requires branch-state or exclusion;
- quantizer refinement increases switching frequency but reduces per-switch magnitude burden;
- q by event-class interaction rejects additive event-cost closure;
- counterfactual mean cost does not obey a simple monotone law.

## Result-To-Principle Mapping

| Result | Principle Component |
|---|---|
| q=8 frozen equivalence passed | Instrumentation is tied to the frozen implementation |
| q4 > q16 vote-switch chord2 burden | Magnitude side of frequency-magnitude trade-off |
| q16 > q4 vote-switch rate | Frequency side of frequency-magnitude trade-off |
| aggregate jump burden peaks at q=8 | No single monotone aggregate law |
| path-only counterfactual q4 - q16 positive | Path event cost can dominate in some regimes |
| vote-only and coincident q4 - q16 negative | Event channels are non-additive |
| square reverses some contrasts | Regime dependence is real |

## Manuscript Wording

Recommended:

```text
The final structural audit does not yield a universal monotone quantization law. Instead, it exposes a systems trade-off: refinement increases switching opportunities while reducing jump magnitudes, and the resulting event costs depend on trajectory and event class.
```

Avoid:

```text
The quantizer pilot validates the obstruction theorem.
```

Avoid:

```text
The event costs add linearly to predict global RMSE.
```

## Theorem Boundary

This principle should be written as a systems proposition or interpretive theorem boundary, not as a complete global RMSE theorem.

Allowed form:

```text
Under a delayed quantized collective-control implementation, smooth-mode local relief does not determine global closure unless the path-transition, vote-switching, memory, and projection-ambiguity channels are separately controlled. The final-gate audit shows these channels are separable and non-additive in the frozen implementation.
```

Not allowed:

```text
The final-gate audit proves global closure failure for all delayed quantized collective-control systems.
```

## Verdict

```text
REVISED_SYSTEMS_PRINCIPLE_LOCKED
```

