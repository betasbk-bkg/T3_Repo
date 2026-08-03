# Base-Condition Cluster Interaction Repair Protocol

Status: pre-run statistical reanalysis.

## Problem

Folder 47 correctly used stream-separated common-random-number schedules, but the interaction-model bootstrap clustered by `paired_id`.

Because `paired_id` includes `q_dirs`, q4, q8, and q16 simulations from the same base condition were treated as independent clusters. The true shared-noise unit is:

```text
base_condition_id = trajectory x minority fraction x delay x replicate
```

This may make interaction confidence intervals too optimistic.

## Repair

This folder performs no new simulations. It reuses:

```text
data/final_structural_audit/sscrn_vote_events_with_counterfactual.csv
```

and recomputes the interaction model with bootstrap clusters at:

```text
base_condition_id
```

## Models

### Base Interaction Model

```text
cost ~ q_coarseness + vote_event + path_event
     + q_coarseness:vote_event
     + q_coarseness:path_event
     + vote_event:path_event
```

### Covariate-Adjusted Interaction Model

```text
cost ~ q_coarseness + vote_event + path_event
     + q_coarseness:vote_event
     + q_coarseness:path_event
     + vote_event:path_event
     + trajectory fixed effects
     + delay fixed effect
     + minority-fraction fixed effect
```

## Decision Rule

If `q_x_vote` and `vote_x_path` still exclude zero under base-condition clustered bootstrap, then the non-additive obstruction result survives the final statistical repair.

If one or both intervals cross zero, the paper should downgrade the non-additivity claim to suggestive interaction evidence.
