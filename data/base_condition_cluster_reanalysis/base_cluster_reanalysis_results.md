# Base-Condition Cluster Reanalysis Results

Status: completed statistical repair.

## What Was Corrected

Folder 47 used stream-separated common-random-number schedules, but clustered the interaction bootstrap by:

```text
paired_id = base condition + q_dirs
```

The true shared-noise unit is:

```text
base_condition_id = trajectory x minority fraction x delay x replicate
```

This folder reuses the folder 47 event table and recomputes interaction confidence intervals using `base_condition_id` as the cluster.

No new simulations were run.

## Corrected Interaction Model

Adjusted model:

```text
cost ~ q_coarseness + vote_event + path_event
     + q_coarseness:vote_event
     + q_coarseness:path_event
     + vote_event:path_event
     + trajectory fixed effects
     + delay fixed effect
     + minority-fraction fixed effect
```

Cluster:

```text
base_condition_id
```

Bootstrap draws:

```text
2000
```

## Adjusted Base-Cluster Results

| Term | Estimate | 95% CI low | 95% CI high | Excludes zero |
|---|---:|---:|---:|---|
| intercept | 0.197936 | 0.035170 | 0.378098 | yes |
| q coarseness | 1.789337 | 1.020660 | 2.582424 | yes |
| vote event | 0.002244 | -0.202844 | 0.202911 | no |
| path event | 0.142235 | -0.351617 | 0.657303 | no |
| q x vote | -4.336568 | -5.492429 | -3.263838 | yes |
| q x path | 0.962349 | -0.691075 | 2.733094 | no |
| vote x path | -0.443359 | -0.813922 | -0.089269 | yes |

## Interpretation

The two important interaction terms survive the corrected clustering:

```text
q_x_vote excludes zero.
vote_x_path excludes zero.
```

The path-event main effect and q-by-path interaction remain uncertain. Therefore the correct claim is:

```text
The final audit supports q-by-vote and vote-by-path non-additive interactions, not a complete event-cost model.
```

## Comparison With Previous Cluster Level

The correction did not overturn the interaction conclusion. Under all checked variants, `q_x_vote` and `vote_x_path` exclude zero:

- paired-id cluster, base model;
- paired-id cluster, covariate-adjusted model;
- base-condition cluster, base model;
- base-condition cluster, covariate-adjusted model.

## Verdict

```text
BASE_CONDITION_CLUSTER_REPAIR_SURVIVES
```

