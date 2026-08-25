# Supplementary Information S2. Zigzag Smoothing Tail Bound

## Scope

This supplement records the local smoothing-memory tail calculation used for zigzag endpoint obstruction. It is a conditional implementation bound. It excludes endpoint wrap discontinuities, overlapping event windows, and any global RMSE conclusion.

## Velocity-bound basis

Assume each stream starts inside the velocity ball, `||vel_0|| <= MSPD`, uses direction commands with `||u_n|| <= 1`, and follows the implemented convex smoothing update:

`vel_{n+1} = (1-alpha) vel_n + alpha MSPD u_n.`

For `0 < alpha <= 1`, convexity gives:

`||vel_{n+1}|| <= (1-alpha)||vel_n|| + alpha MSPD ||u_n|| <= MSPD.`

Hence the velocity ball of radius `MSPD` is invariant. For two streams satisfying this invariant:

`||Delta vel_{g_i}|| <= ||vel_{g_i}^{(1)}|| + ||vel_{g_i}^{(2)}|| <= 2 MSPD.`

This is the basis for the factor `2 MSPD` in the tail bound. If an implementation uses a different velocity update or command normalization, this invariant must be rechecked.

## Definitions

Let `rho = 1 - alpha`. For the logarithmic cutoff formula below, assume `0 < rho < 1`; the `rho = 0` case is handled separately. Let `g_i` be the frame index of a zigzag endpoint or corner event. After the local event window ends, suppose no additional command perturbation is injected into the compared streams, so the remaining difference follows:

`Delta vel_{n+1} = rho Delta vel_n.`

For a cutoff horizon `H`, define the residual positive-position tail magnitude by:

`TailPos(g_i,H) = ||DT sum_{m=H}^{infty} Delta vel_{g_i+m}||.`

This is a norm envelope for remaining smoothing memory after `H` frames, not an RMSE theorem term.

## Geometric-series derivation

For `0 < rho < 1`, since `||Delta vel_{g_i+m}|| <= rho^m ||Delta vel_{g_i}||`, define the scalar geometric tail `S_tail(H) = rho^H / (1-rho)`. The residual position tail satisfies:

`TailPos(g_i,H) <= DT S_tail(H) ||Delta vel_{g_i}||`

`TailPos(g_i,H) <= 2 DT MSPD S_tail(H)`

`TailPos(g_i,H) <= 2 DT MSPD rho^H / (1-rho).`

For a tolerance `epsilon_tail`, choose:

`H_epsilon = ceil(log(epsilon_tail) / log(rho)).`

Then `rho^{H_epsilon} <= epsilon_tail`, and:

`TailPos(g_i,H_epsilon) <= 2 DT MSPD epsilon_tail / (1-rho).`

If `rho = 0`, the smoothing-memory discrepancy vanishes after one update, so the logarithmic cutoff formula is not used.

## Implementation note

With `alpha = 0.2`, `rho = 0.8`, and `epsilon_tail = 0.01`, this gives `H_epsilon = 21` frames. Since `VOTE_INT = 18` frames in the fixed implementation, the cutoff exceeds one vote interval. This quantitatively supports the memory-overlap obstruction for repeated nearby events. It does not prove additive corner costs, global benefit, or a zigzag RMSE sign prediction.
