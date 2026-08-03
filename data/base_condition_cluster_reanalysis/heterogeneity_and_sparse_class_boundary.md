# Heterogeneity And Sparse-Class Boundary

Status: final boundary note for event-class interpretation.

## Sparse Classes

Some event classes remain too sparse for standalone class-effect claims.

Smallest cells:

| q dirs | Trajectory | Event class | Rows | Base conditions |
|---:|---|---|---:|---:|
| 16 | zigzag | path-only | 3 | 3 |
| 8 | square | path-only | 11 | 8 |
| 16 | lemniscate | path-only | 14 | 10 |
| 8 | zigzag | path-only | 18 | 15 |
| 8 | lemniscate | path-only | 31 | 16 |

Therefore event-class means should be used as diagnostic summaries only.

## Allowed Use

Allowed:

```text
Event-class summaries show where the interaction model is drawing structure from.
```

Allowed:

```text
Sparse path-only cells are reported but not interpreted as independent effect estimates.
```

## Not Allowed

Not allowed:

```text
The q16 zigzag path-only mean estimates a reliable path-only effect.
```

Not allowed:

```text
Every event class has enough support for standalone inference.
```

## Heterogeneity Boundary

The interaction result survives trajectory, delay, and minority-fraction adjustment, but the paper should still report heterogeneity rather than hiding it.

Safe:

```text
The non-additive interaction is detected after adjustment for trajectory, delay, and minority fraction, while some individual event classes remain sparse.
```

Unsafe:

```text
The same event law holds uniformly across all trajectories.
```

## Verdict

```text
SPARSE_CLASS_BOUNDARY_FINALIZED
```

