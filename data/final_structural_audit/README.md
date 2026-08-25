# Stream-Separated Common-Random-Number Structural Audit

Status: completed stream-separated structural audit.

This folder contains the q/vote/path audit outputs used in the manuscript. The design separates:

- honest-agent random stream;
- honest-counterfactual troll stream;
- shared q4/q8/q16 base-condition schedule.

## Main Result

The audit supports a frequency-burden trade-off rather than a simple monotone harm law:

```text
q4 - q16 mean vote-jump chord-squared burden = 0.220008
95% CI = [0.136443, 0.309936]
```

The positive counterfactual cost tail remains larger under coarse quantization:

```text
q4 - q16 positive counterfactual tail = 0.316234
95% CI = [0.256936, 0.374913]
```

Mean counterfactual event cost is not a robust positive coarse effect:

```text
q4 - q16 mean counterfactual cost = -0.005123
95% CI = [-0.013042, 0.002533]
```

The clustered interaction model keeps two interaction terms whose confidence intervals exclude zero: `q_x_vote` and `vote_x_path`. This supports non-additive vote/path event-cost associations in the fixed implementation.

## Boundary

The folder records a structural audit, not a validation study, predictive closure, or a proof that coarse quantization is uniformly worse.
