# State Variable Definitions

## Scope
These variables are preregistered continuous state variables for the remaining structured T3 residuals. They are not gates, do not change the deployed E model, and do not introduce fitted thresholds. Any future use should compute them before inspecting new held-out outcomes.

## Shared Notation
- Frame index: `f`.
- Current path arclength and position: `s_f`, `x_f`.
- Delayed path arclength used by the controller: `s_{f-d}`.
- Path tangent and normal at arclength `s`: `t(s)`, `n(s)`.
- Tangent heading: `theta(s) = atan2(t_y(s), t_x(s))`.
- Curvature proxy: `kappa(s)`.
- Signed cross-track error: `eta_f`.
- Cross-track velocity: `edot_f = v_f dot n(s_f)`.
- T3-vs-counterfactual command difference: `Delta u_f = u_T3,f - u_CF,f`.
- Normal command difference: `Delta u_{n,f} = Delta u_f dot n(s_f)`.
- Tangential command difference: `Delta u_{t,f} = Delta u_f dot t(s_f)`.
- Normal relief signal: `r_f = -sign(eta_f) * Delta u_{n,f}`. Positive `r_f` means the T3 command pushes toward the reference path in the local normal direction.
- Command weight: `W_f = ||Delta u_f|| + 1e-12`.
- Curvature weight: `K_f = |kappa(s_f)| / (mean_path |kappa| + 1e-12)`.
- `wrap_pi(a)` is the angular difference wrapped to `[-pi, pi]`.

All path-level means and normalizers are geometric or within-cell quantities. They are not chosen to improve prediction accuracy.

## 1. Corner/Turn Phase Index

### Mathematical Definition
For each frame, define delayed tangent phase mismatch:

```text
P_f = |wrap_pi(theta(s_f) - theta(s_{f-d}))| / pi
```

Then define the cell-level corner/turn phase index:

```text
CTPI = sum_f W_f * K_f * P_f / sum_f W_f
```

Interpretation: `CTPI` is high when the T3 command acts at high-curvature or corner-like parts of the path while the delayed geometry belongs to a different tangent phase. It is low when the delayed and current path phases match, even if the trajectory has static corner topology.

### Required Frame-Level Quantities
- `s_f`
- `s_{f-d}` or enough per-frame history to recover it
- `theta(s_f)` and `theta(s_{f-d})`, computable from path geometry
- `kappa(s_f)`
- `Delta u_f` or enough command information to recover `W_f`

### Computable From Existing Outputs?
Not exactly.

Existing full-grid sampled frames include `s`, `kappa`, `delta_cmd_tangent`, and `delta_cmd_normal` for original_96, but they are sampled every 120 frames and do not include `s_{f-d}`. Heldout1 and heldout2 currently have only cell-level summaries. Exact computation requires full frame-level logs or an instrumented replay that records current and delayed arclengths per frame.

### Targeted Residual Classes
- zigzag corner-phase
- low-delay corner-onset
- high-delay corner/tail

### Expected Sign / Direction
Higher `CTPI` is expected to reduce T3 benefit or increase harm risk. In an additive relief-cost model, its coefficient should be negative with respect to observed RMSE gap `RMSE_honest - RMSE_T3`.

### Risk Of Overfitting
Moderate. The concept is principled and geometric, but it targets a small number of residual classes. Risk is controlled by defining it from path geometry and delay before any refit, using no outcome-tuned cutoffs, and testing on a new held-out grid.

## 2. Branch Ambiguity Index

### Mathematical Definition
For each frame, find the nearest and second-nearest path projections:

```text
(s1_f, d1_f, t1_f) = nearest branch projection
(s2_f, d2_f, t2_f) = second-nearest branch projection
d1_f <= d2_f
```

Define geometric branch ambiguity:

```text
A_f = max(0, 1 - (d2_f - d1_f) / (d2_f + d1_f + 1e-12)) * (1 - |t1_f dot t2_f|)
```

Define command direction:

```text
q_f = Delta u_f / (||Delta u_f|| + 1e-12)
```

Define competing-branch command preference:

```text
B_f = max(0, q_f dot t2_f - q_f dot t1_f)
```

Then define the cell-level branch ambiguity index:

```text
BAI = sum_f W_f * A_f * B_f / sum_f W_f
```

For trajectories with no meaningful second branch, `BAI = 0` by definition.

Interpretation: `BAI` is high when the agent is near an ambiguous multi-branch region and the T3 command points more toward the competing branch than the active nearest branch.

### Required Frame-Level Quantities
- `x_f`
- nearest and second-nearest path projections
- active and competing branch tangents `t1_f`, `t2_f`
- `Delta u_f` in global coordinates, or enough command headings to reconstruct it

### Computable From Existing Outputs?
Not exactly.

Existing cell outputs contain only a static `branch_ambiguity` flag. Original_96 sampled frame logs include `x`, `y`, `psi_t3`, and `psi_cf`, which are enough to approximate command direction for sampled original frames if the path projection routine is reused. However, exact full-grid computation requires dense frame logs for original_96, heldout1, and heldout2 plus a path routine that returns nearest and second-nearest projections.

### Targeted Residual Classes
- lemniscate branch/topology

### Expected Sign / Direction
Higher `BAI` is expected to reduce T3 benefit or increase harm risk. In an additive model, its coefficient should be negative with respect to observed RMSE gap.

### Risk Of Overfitting
Low to moderate. The variable is mechanistically specific to branch ambiguity, but it is motivated by only a few hard lemniscate residuals. Risk is controlled by defining it as a continuous geometry-command alignment term rather than a lemniscate-specific binary correction.

## 3. Relief Consistency / Overshoot Availability Index

### Mathematical Definition
Define overshoot availability:

```text
O_f = max(0, eta_f * edot_f) / (mean_f |eta_f * edot_f| + 1e-12)
```

`O_f` is high when the trajectory is moving farther away from the path in the direction of the current cross-track error. It is low when the agent is already moving back toward the path or has little cross-track motion.

Let `H` be a fixed actuator response horizon derived from the simulation dynamics:

```text
H = ceil(1 / SMOOTH)
```

where `SMOOTH` is the engine's velocity smoothing parameter. This is not outcome-tuned.

Define horizon-averaged relief:

```text
Rbar_f = (1 / H) * sum_{h=0}^{H-1} r_{f+h}
```

Then define the cell-level relief consistency / overshoot availability index:

```text
RCOAI = mean_f O_f * Rbar_f / (mean_f |r_f| + 1e-12)
```

Interpretation: `RCOAI` is high when projected relief persists across the response horizon precisely when overshoot correction is available. It is low or negative when apparent local relief is temporally inconsistent, arrives after the correction opportunity, or points the wrong way over the response horizon.

### Required Frame-Level Quantities
- `eta_f`
- `edot_f`
- `Delta u_{n,f}`
- frame-to-frame sequence order with no coarse subsampling
- engine `SMOOTH` value

### Computable From Existing Outputs?
Not exactly.

Cell summaries include `frame_abs_relief`, `projected_relief_positive_rate`, `rms_eta`, `osc_change_pct`, `edot_change_pct`, and tail terms. These are proxies, not the temporal consistency variable. Original_96 sampled frames include `eta`, `edot`, `delta_cmd_normal`, and `local_abs_power`, but the 120-frame stride is too sparse for the fixed response horizon. Exact computation requires dense frame-level logs.

### Targeted Residual Classes
- low-delay no-overshoot
- relief-overcalled false benefits
- corner/branch cases where local relief is present but phase-inconsistent

### Expected Sign / Direction
Higher `RCOAI` is expected to increase T3 benefit. Low or negative `RCOAI` is expected to identify cases where aggregate projected relief overstates actual RMSE improvement.

### Risk Of Overfitting
Moderate. It is broad enough to explain several residual classes, which makes it useful but also easier to overfit if tuned. Risk is controlled by fixing the response horizon from engine dynamics and avoiding any residual-derived threshold.

