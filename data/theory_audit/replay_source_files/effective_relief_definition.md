# Effective Relief Definition

Status: error-unit effective relief definition for the local-to-RMSE bridge.

## Purpose

The global theorem needs a left-hand-side quantity in error units, not only command units.

Raw projected command relief:

```text
r_proj = -sign(eta_anchor) * DeltaU_n
```

is therefore replaced by a finite-horizon signed-error relief lower bound.

## Definitions

Let:

```text
sigma = sign(eta_anchor)
q_h = -sigma * delta_eta_lin_h
B_h = R_curv_bound_h.
```

Define the safe error-unit relief:

```text
q_safe = max(0, q_h - B_h).
```

Under strict overshoot availability:

```text
A_ov = 1
```

only when:

```text
q_h > B_h
and
q_h + B_h < |eta_anchor|.
```

Then define:

```text
r_eff_h = A_ov * q_safe.
```

This is in signed-error units.

## Squared-Error Lower-Bound Contribution

Inside the smooth projection tube:

```text
err = |eta|.
```

If the same-side condition holds, an error reduction of at least `q_safe` gives a squared-error decrease lower bound:

```text
L_frame
  = A_ov * max(0, 2*|eta_anchor|*q_safe - q_safe^2).
```

This comes from:

```text
eta^2 - (eta - sigma*q_safe)^2
  = 2*|eta|*q_safe - q_safe^2.
```

## When This Supports The Local-To-RMSE Bridge

`L_frame` supports the local-to-RMSE bridge when:

- projection tube is valid;
- closest-path error equals `|eta|`;
- `A_ov = 1` under the strict definition;
- `B_h >= |R_curv(h)|`;
- no sign crossing is guaranteed by `q_h + B_h < |eta_anchor|`;
- the frame contribution is aggregated by a predeclared interval convention.

## Interval EffectiveLocalRelief

A future theorem may define:

```text
EffectiveLocalRelief(I) = sum_{t in I} L_frame(t)
```

or a normalized version:

```text
EffectiveLocalReliefMean(I) = mean_{t in I} L_frame(t).
```

The aggregation convention must be fixed before use and must not be tuned to outcomes.

## Non-Claims

This definition does not close `B_tail`, `B_div`, `B_stoch`, or global RMSE benefit.

It only makes the left-hand local relief term expressible in error units.

