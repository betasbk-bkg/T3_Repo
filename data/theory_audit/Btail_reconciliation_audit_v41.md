# Btail Reconciliation Audit

## Locked Value

`B_tail_sum = 1.295747349145897`

## Definition

The locked local squared-error tail bridge is

`TailFrameBound(t) = 2 |eta_anchor(t)| tail_pos_bound_h(t) + tail_pos_bound_h(t)^2`.

The reported value is

`B_tail_sum = sum_t TailFrameBound(t)`

over the 3900-row replay-log basis described in Supplement S3.

## Boundary

This value is a locally instantiable replay/audit quantity in projection-tube squared-error units. It is not a validation result, not a fitted theorem constant, and not a complete global RMSE tail bound. A complete global closure theorem would still require independent divergence/coupling and stochastic terms.
