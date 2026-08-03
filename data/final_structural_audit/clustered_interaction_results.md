# Clustered Interaction Results

Status: completed simulation-cluster bootstrap interaction model.

## Model

Outcome:

```text
counterfactual_event_cost_sscrn = Delta e2_T3 - Delta e2_honest
```

Model:

```text
cost ~ q_coarseness + vote_event + path_event
     + q_coarseness:vote_event
     + q_coarseness:path_event
     + vote_event:path_event
```

Uncertainty:

```text
simulation-cluster bootstrap over paired_id
bootstrap draws = 1000
```

## Coefficients

| Term | Estimate | 95% CI low | 95% CI high | Status |
|---|---:|---:|---:|---|
| intercept | 0.187527 | 0.004197 | 0.376612 | positive baseline |
| q coarseness | 1.792453 | 0.820156 | 2.734079 | positive |
| vote event | 0.021881 | -0.183633 | 0.213407 | uncertain |
| path event | 0.227193 | -0.176576 | 0.667602 | uncertain |
| q x vote | -4.251898 | -5.479751 | -2.958591 | strong interaction |
| q x path | 0.887578 | -0.461003 | 2.427325 | uncertain |
| vote x path | -0.489441 | -0.855593 | -0.118938 | strong interaction |

## Interpretation

The interaction model supports:

```text
vote/path obstruction channels are non-additive.
```

The strongest terms are interaction terms, not simple event main effects. This is exactly why the manuscript should avoid a monotone additive switching-cost story.

## Sparse-Class Boundary

Event-class means remain descriptive because some cells are sparse. Examples:

```text
zigzag q16 path-only rows: 3
lemniscate q16 path-only rows: 14
square q8 path-only rows: 11
```

Therefore:

- use event-class tables to show diagnostic structure;
- use the clustered interaction model for the non-additivity claim;
- do not claim per-class causal effects from sparse class means.

## Verdict

```text
NON_ADDITIVE_INTERACTION_SURVIVES_STREAM_SEPARATED_CRN
```

