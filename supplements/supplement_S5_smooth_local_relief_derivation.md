# Supplementary Information S5. Smooth Local Relief Derivation

This appendix gives the formal version of the local smooth result used
in the manuscript. It is local, same-state, and conditional on a smooth
projection tube. Global RMSE theorem status is outside this appendix.

## A.1 Reference path and projection tube

Let r(s) be a planar reference curve parameterised by arclength on an
interval J. Assume r is $C^{2}$, has unit tangent T(s), unit normal
N(s), and scalar curvature kappa(s) satisfying
$\left| \kappa(s) \right| \leq K$. Let:

$$\Phi(s,\eta) = r(s) + \eta N(s)$$

Assume a projection tube:

$$|\eta| \leq \rho_{tube}K\rho_{tube} < 1$$

on which Phi is one-to-one. For any state p in this tube there are
unique coordinates $\left( s(p),\eta(p) \right)$ such that:

$$p = r\left( s(p) \right) + \eta(p)N\left( s(p) \right)$$

The closest-path Euclidean distance is:

$$dist(p,path) = \left| \eta(p) \right|$$

## A.2 Curvature remainder

In a planar tubular neighborhood, the signed-distance coordinate
$\eta(p)$ is differentiable with gradient:

$$grad\eta(p) = N\left( s(p) \right)$$

Its Hessian has curvature-controlled tangent component:

$$\left\| D^{2}\eta(p) \right\| \leq L_{\eta}L_{\eta} = \frac{K}{\left( 1 - K\rho_{tube} \right)}$$

Therefore, for an anchor state p_t and a displacement $\delta p$ whose
full interpolation segment $p_{t} + \lambda\delta p$,
$0 \leq \lambda \leq 1$, remains in the tube,

$$\eta\left( p_{t} + \delta p \right) = \eta\left( p_{t} \right) + N_{t} \cdot \delta p + R_{curv}(\delta p)$$

where $N_{t} = N\left( s\left( p_{t} \right) \right)$ and:

$$\left| R_{curv}(\delta p) \right| \leq R_{curv,bound}(\delta p) = \left( \frac{1}{2} \right)L_{\eta}\left\| \delta p \right\|^{2}$$

This defines the manuscript\'s curvature/projection remainder:

$$R_{curv}(h) = \eta\left( p_{t} + \delta p_{t + h} \right) - \eta\left( p_{t} \right) - N_{t} \cdot \delta p_{t + h}$$

$$R_{curv,bound,h} = \left( \frac{1}{2} \right)\left\lbrack \frac{K}{\left( 1 - K\rho_{tube} \right)} \right\rbrack\left\| \delta p_{t + h} \right\|^{2}$$

If the reference segment is straight, $K = 0$ and this bound gives zero
curvature remainder inside the tube.

## A.3 Finite-memory displacement response

The implemented smoothing update is:

$${vel}_{n + 1} = (1 - \alpha){vel}_{n} + \alpha MSPDu_{n}$$

$${pos}_{n + 1} = {pos}_{n} + DT{vel}_{n + 1}$$

Consider two command streams from the same state and velocity at time t,
and define:

$$\Delta U_{t + j} = MSPD\left( {u^{'}}_{t + j} - u_{t + j} \right)$$

$$\rho = 1 - \alpha$$

The velocity perturbation satisfies:

$$\Delta{vel}_{t + k + 1} = \alpha\sum_{j = 0}^{k}\rho^{k - j}\Delta U_{t + j}$$

Summing positions over h frames gives:

$$\delta p_{t + h} = DT\sum_{j = 0}^{h - 1}\left\lbrack 1 - \rho^{h - j} \right\rbrack\Delta U_{t + j}$$

Define the linear normal displacement:

$${\delta\eta}_{lin,h} = N_{t} \cdot \delta p_{t + h}$$

The actual signed normal-coordinate change is:

$$\delta\eta_{h} = {\delta\eta}_{lin,h} + R_{curv}(h)$$

with $\left| R_{curv}(h) \right| \leq R_{curv,bound,h}$ under the tube
assumptions above.

## A.4 Strict same-side availability

Let:

$$\eta_{anchor} = \eta\left( p_{t} \right),\sigma = sign\left( \eta_{anchor} \right)$$

and assume $\eta_{anchor} \neq 0$. Define movement toward the path by:

$$q_{h} = - \sigma{\delta\eta}_{lin,h}$$

and define:

$$B_{h} = R_{curv,bound,h}$$

Strict overshoot availability is:

$$A_{ov}(h) = 1$$

if:

$$q_{h} > B_{h}$$

and:

$$q_{h} + B_{h} < \left| \eta_{anchor} \right|$$

Otherwise, $A_{ov}(h) = 0$.

This is a theorem variable rather than a controller gate, and replay
counts play no role in tuning it.

## A.5 Local relief proposition

If $A_{ov}(h) = 1$, then local closest-path absolute error decreases at
horizon h.

Proof. Since $\left| R_{curv}(h) \right| \leq B_{h}$,

$$- \sigma\delta\eta_{h} = - \sigma{\delta\eta}_{lin,h} - \sigma R_{curv}(h) \geq q_{h} - B_{h} > 0$$

Thus the actual displacement has a component toward the path. Also,

$$- \sigma\delta\eta_{h} \leq q_{h} + B_{h} < \left| \eta_{anchor} \right|$$

so the signed normal coordinate preserves its sign while moving toward
the path. Because the motion stays on the same side while moving toward
zero,

$$\left| \eta_{anchor} + \delta\eta_{h} \right| < \left| \eta_{anchor} \right|$$

Inside the projection tube $dist(p,path) = \left| \eta(p) \right|$, so
closest-path absolute error decreases.

## A.6 Squared-error relief term

Define the conservative same-side relief amount:

$$q_{safe} = \max\left( 0,q_{h} - B_{h} \right)$$

When $A_{ov}(h) = 1$, the squared normal-error decrease is bounded below
by:

$${\eta_{anchor}}^{2} - \left( \left| \eta_{anchor} \right| - q_{safe} \right)^{2} = 2\left| \eta_{anchor} \right|q_{safe} - {q_{safe}}^{2}$$

Therefore the local squared-error contribution used in the audit is:

$$L_{frame} = A_{ov}\max\left( 0,2\left| \eta_{anchor} \right|q_{safe} - {q_{safe}}^{2} \right)$$

This is a lower bound for the local smooth same-state perturbation. It
excludes tail, divergence, stochastic, vote-switching, and path-mode
costs.

## A.7 Algebra, Index, and Sign Check

This subsection records the algebra check for the local result. Let
$\rho = 1 - \alpha$ with $0 < \alpha \leq 1$, so $0 \leq \rho < 1$. For
two command streams started from the same state and velocity,
$\Delta{vel}_{t} = 0$ and:

$$\Delta{vel}_{n + 1} = \rho\Delta{vel}_{n} + \alpha\Delta U_{n}$$

Induction gives:

$$\Delta{vel}_{t + k + 1} = \alpha\sum_{j = 0}^{k}\rho^{k - j}\Delta U_{t + j}$$

Therefore:

$$\delta p_{t + h} = DT\sum_{k = 0}^{h - 1}\Delta{vel}_{t + k + 1}$$

$$\delta p_{t + h} = DT\sum_{j = 0}^{h - 1}\alpha\sum_{k = j}^{h - 1}\rho^{k - j}\Delta U_{t + j}$$

$$\delta p_{t + h} = DT\sum_{j = 0}^{h - 1}\left\lbrack 1 - \rho^{h - j} \right\rbrack\Delta U_{t + j}$$

because $\frac{\alpha}{(1 - \rho)} = 1$. This confirms the index
convention in Equation 2.

For the sign convention, $\sigma = sign\left( \eta_{anchor} \right)$ and
$q_{h} = - \sigma{\delta\eta}_{lin,h}$. Thus q_h \> 0 means the linear
displacement points toward the path. With
$\left| R_{curv}(h) \right| \leq B_{h}$:

$$- \sigma\delta\eta_{h} \geq q_{h} - B_{h}$$

and:

$$- \sigma\delta\eta_{h} \leq q_{h} + B_{h}$$

The two strict conditions q_h \> B_h and therefore imply a positive
toward-path displacement that remains smaller than the original signed
distance. The normal sign is preserved.

Let . On the interval , the squared-error decrease is increasing in r_h.
Since , the lower bound in Equation 6 follows. This check verifies the
existing proof\'s indices, the convention, the sign convention, and the
curvature remainder usage in the existing proof.

## A.8 Scope

The result requires:

-   a unique smooth projection chart;

-   $C^{2}$ path geometry on the interval;

-   $K\rho_{tube} < 1$;

-   the full interpolation segment $p_{t} + \lambda\delta p$ remains
    inside the projection tube for every lambda in \[0,1\];

-   finite command perturbations over a finite horizon;

-   strict same-side availability.

It excludes square corners, zigzag endpoint wrap, sampled-lemniscate
nearest-sample discontinuities, lemniscate branch ambiguity, vote-bin
discontinuities, stochastic expectation statements, and coupled global
RMSE claims.
