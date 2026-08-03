# Counterfactual Event-Cost Audit

Status: completed paired T3-minus-honest event-cost audit.

## Definition

For each T3 vote-update row, the final-gate script computes:

```text
Delta e2_T3 - Delta e2_honest
```

where the honest value comes from the paired honest counterfactual with the same quantizer, trajectory, delay, minority fraction, replicate, and vote round.

This is a paired trajectory counterfactual audit. It is not a same-state perturbation theorem and not validation.

## Overall Quantizer Result

Mean counterfactual event cost:

| q dirs | Mean counterfactual cost | Positive counterfactual cost |
|---:|---:|---:|
| 4 | -0.000407 | 0.851883 |
| 8 | 0.008754 | 0.619156 |
| 16 | 0.003930 | 0.541966 |

The mean counterfactual cost does not support a simple coarse-quantizer monotone law.

The positive tail of counterfactual cost is larger under q=4 than q=16:

```text
q4 - q16 = 0.309917
95% CI = [0.248223, 0.367957]
```

## Event-Class Interaction

| Event class | q4 cost | q8 cost | q16 cost | q4 - q16 |
|---|---:|---:|---:|---:|
| path-only | 1.310969 | 0.362049 | -0.018041 | 1.329010 |
| quiet | 0.609623 | 0.407878 | 0.362845 | 0.246777 |
| vote-only | -0.424595 | -0.028971 | -0.000893 | -0.423702 |
| vote/path coincident | -0.502233 | -0.155587 | -0.077877 | -0.424356 |

This is the strongest evidence for non-additivity:

```text
Path-only rows show a large positive coarse-fine counterfactual cost, while vote-only and vote/path coincident rows reverse direction.
```

## Interpretation

The obstruction channels are separable but not additive.

Vote events, path events, and coincident events do not combine into one monotone switching-cost law. This supports the revised systems principle:

```text
local relief cannot be closed by a single monotone switching-cost law.
```

## Safe Claim

Safe:

```text
The paired counterfactual audit shows event-class-specific cost regimes and rejects a single additive obstruction-cost interpretation.
```

Unsafe:

```text
The counterfactual audit proves that every coincident event causes global T3 harm.
```

## Verdict

```text
COUNTERFACTUAL_AUDIT_SUPPORTS_NON_ADDITIVE_OBSTRUCTION
```

