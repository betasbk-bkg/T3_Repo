# V3 Model Form Freeze

## Scope
This file freezes the candidate v3 model forms. It does not estimate coefficients, change the locked E model, add gates, tune thresholds, run heldout3, or evaluate predictive accuracy.

## Shared Baseline
Both options use the locked baseline relief-cost-topology E model as the starting point:

```text
gap_hat_E_locked
```

The target for future held-out evaluation remains:

```text
gap = RMSE_honest - RMSE_T3
```

## Option A: E + RCOAI + CTPI

### Model Form
```text
gap_hat_A =
    gap_hat_E_locked
  + beta_R * RCOAI
  + beta_C * CTPI
```

### Theoretical Justification
RCOAI captures whether projected relief is temporally consistent with overshoot correction availability. CTPI captures delayed tangent mismatch during corner or turn exposure. Together they target the two best-supported missing continuous states from the residual audit: relief-overcall and corner/turn phase cost.

### Expected Signs
```text
beta_R > 0
beta_C < 0
```

### Primary Or Exploratory?
Option A is the primary v3 model form.

### Overfitting Risk
Moderate. The variables were defined after residual inspection, but they are continuous physical quantities computed for all cells and not residual labels. Risk is controlled by freezing formulas before heldout3 and requiring all coefficients to be frozen before heldout3 outcome inspection.

## Option B: E + RCOAI + CTPI + Refined Dynamic Branch Phase

### Model Form
```text
gap_hat_B =
    gap_hat_E_locked
  + beta_R * RCOAI
  + beta_C * CTPI
  + beta_B * DBPI
```

### Theoretical Justification
DBPI tests whether branch/topology residuals arise when delayed controller phase is dynamically aligned with a competing branch and the command perturbation points toward that branch. This is more specific than the prior static BAI approximation and is directly tied to branch phase, not a trajectory label.

### Expected Signs
```text
beta_R > 0
beta_C < 0
beta_B < 0
```

### Primary Or Exploratory?
Option B is exploratory for v3 by default. It can be promoted to primary only if that promotion is explicitly frozen before heldout3 is generated or inspected.

### Overfitting Risk
Moderate to high. The branch/topology residual class is small, and DBPI was refined in response to weak BAI behavior. The main protection is that DBPI is a continuous frame-level geometry-command variable that can be computed for all trajectories from frozen logs without using outcomes.

## Frozen Held-Out Evaluation Rule
Before heldout3 is run, one of the following must be declared:

1. Primary test: Option A only.
2. Primary test: Option A, with Option B reported as exploratory branch analysis.
3. Primary test: Option B, only if this choice is explicitly preregistered before heldout3 simulation and before any heldout3 outcome inspection.

No post-hoc gate, coefficient sign change, threshold, trajectory-specific correction, or heldout3-driven variable alteration is allowed.
