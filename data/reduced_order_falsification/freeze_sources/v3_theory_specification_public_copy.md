# V3 Theory Specification

## Scope
This document preregisters the v3 form of the T3 relief-cost-topology boundary theory. It is a specification only: no E-model coefficients are refit here, no new gates are added, no thresholds are tuned, no heldout3 simulations are run, and no predictive accuracy is evaluated.

## Starting Point
The v3 theory starts from the locked baseline relief-cost-topology E model used in the prior confirmatory analyses. The baseline E model remains the reference cell-level predictor of the RMSE gap:

```text
gap = RMSE_honest - RMSE_T3
```

Positive gap means T3 benefit; negative gap means T3 harm or non-benefit.

The residual audit found that the remaining hard residuals are structured rather than randomly dispersed. The missing structure is not another binary gate; it is a set of continuous state variables describing when local projected relief is dynamically available, when corner/turn phase makes delayed commands costly, and when branch phase makes the active path ambiguous.

## V3 Theory
The preregistered v3 theory is:

```text
baseline relief-cost-topology E model
+ RCOAI: relief consistency / overshoot availability state
+ CTPI: corner/turn phase cost state
+ optional DBPI: refined dynamic branch-phase state
```

No fitted coefficients are assigned in this specification. Any future coefficient estimation must be performed and frozen before heldout3 outcomes are inspected.

## Primary Variables

### Relief Consistency / Overshoot Availability Index
RCOAI measures whether projected normal relief persists across the actuator response horizon when the trajectory is actually in an overshoot-correctable state.

Expected direction:

```text
higher RCOAI -> larger T3 benefit -> positive contribution to gap
```

RCOAI is the best-supported v3 variable from the state-variable audit. It targets low-delay no-overshoot and relief-overcalled residuals, where aggregate relief exists but is not temporally consistent with the correction opportunity.

### Corner/Turn Phase Index
CTPI measures delayed tangent phase mismatch weighted by curvature or corner-like exposure and command magnitude.

Expected direction:

```text
higher CTPI -> lower T3 benefit or greater harm risk -> negative contribution to gap
```

CTPI is a primary v3 variable because it captures a principled missing cost state for square, zigzag, and high-delay turn/corner regimes. The audit shows it is partial rather than complete, so it should be interpreted as a cost-state term, not as a closure by itself.

## Exploratory Branch Variable

### Dynamic Branch Phase Index
The current BAI approximation is not strong enough to be treated as a primary v3 closure variable. It is replaced by a refined dynamic branch-phase index, DBPI, defined separately in `dynamic_branch_phase_definition.md`.

Expected direction:

```text
higher DBPI -> lower T3 benefit or greater harm risk -> negative contribution to gap
```

DBPI is optional and exploratory unless a future held-out evaluation packet explicitly promotes Option B before heldout3 outcomes are generated or inspected.

## V3 Model Form
The generic additive form for a future frozen held-out evaluation is:

```text
gap_hat_v3 =
    gap_hat_E_locked
  + beta_R * RCOAI
  + beta_C * CTPI
  + beta_B * DBPI
```

with expected signs:

```text
beta_R > 0
beta_C < 0
beta_B < 0
```

Option A excludes DBPI and is the primary low-risk v3 test. Option B includes DBPI and is branch/topology exploratory unless explicitly preregistered as primary before any heldout3 outcome inspection.

## Claim Status
Before heldout3, this theory supports only a preregistered mechanistic hypothesis:

```text
Residual T3 boundary errors are expected to be reduced by continuous state variables for relief consistency, corner/turn phase, and possibly dynamic branch phase.
```

It does not support any claim of improved predictive accuracy, empirical closure, universal theorem, or complete 2D Frenet theory closure.
