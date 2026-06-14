# Contrarian rate-damping in latency-affected crowd-sourced continuous control

Simulation code, deterministic seeds, results and figures for the study of a
**coordinated contrarian minority** that *stabilizes* latency- and curvature-induced
overshoot in crowd-sourced continuous control — outperforming an honest crowd in
overshoot-limited regimes.

**Author:** BongKeun Song · ORCID [0009-0008-3120-8126](https://orcid.org/0009-0008-3120-8126) · `bongkeun.song@fau.de`
**License:** MIT · **Target venue:** Journal of Computational Science

---

## What this shows (one paragraph)

In a fixed-velocity, 8-direction, vector-mean crowd-control simulator with control
latency and velocity smoothing, a coherent **anti-aggregate minority** lowers tracking
RMSE below the *honest counterfactual* (the same agents voting honestly) whenever the
controller is overshoot-limited (delay **or** trajectory curvature). Frame-level
regression shows the minority injects a **velocity-opposing (rate-damping) command term**
that is absent in the honest crowd. The effect is specific to continuous vector-mean
aggregation, vanishes under majority voting, and is robust to quantization, smoothing and
look-ahead. A reduced-order model with fixed-speed saturation reproduces the honest
latency trend and the damping channel but **does not predict the benefit/harm boundary** —
a clearly identified scope limit of the scalar approximation.

## Repository layout

```
code/
  adversary_ladder.py     # simulation engine (trajectories, honest block, aggregation, T0/T3 adversaries)
  t3_confirmatory.py      # MAIN confirmatory grid: MC=50, 4 trajectories x 3 fractions x 8 latencies
  t3_quant_ablation.py    # quantization ablation (8/16/32 dirs) -> rules out dead-zone mechanism
  t3_strengthen.py        # frame-level rate-damping evidence + controller generality (alpha, look-ahead)
  t3_theorem.py           # small-signal characteristic equation + numerical critical-delay d* (companion matrix)
  t3_zeta.py              # effective damping-ratio estimate (supporting, log-decrement)
results/
  t3_confirmatory_results.json   # output of the MC=50 grid (figures/tables derive from this)
figures/
  t3_E1_delay_compensation.png   # main effect vs delay (delay-curvature dissociation)
  t3_generality.png              # robustness across quantization / smoothing / look-ahead
  t3_stability_margin.png        # small-signal d* extension (diagnostic)
  t3_fig4_decomposition.png      # lumped vs decomposed regression (minority-specific damping)
  t3_fig5_saturation.png         # saturated reduced model reproduces honest latency curve
  t3_fig6_scope_boundary.png     # reduced model does NOT predict the gap (scope boundary)
docs/                            # (manuscript / supplementary, added separately)
CITATION.cff  LICENSE  requirements.txt
```

## Reproduce

Requires Python 3.10+ with `numpy` and `matplotlib`.

```bash
pip install -r requirements.txt
cd code

# Main confirmatory grid (deterministic seeds; quick ~3-4 min, full ~80 min)
python3 t3_confirmatory.py quick      # smoke check
python3 t3_confirmatory.py full       # paper-grade -> writes results/t3_confirmatory_results.json

# Mechanism / robustness / theory (each self-contained, run from code/)
python3 t3_quant_ablation.py          # dead-zone shrinks 4x but effect persists -> not a dead-zone effect
python3 t3_strengthen.py              # cos(minority, velocity) ~ -0.98; advantage robust across controllers
python3 t3_theorem.py                 # characteristic equation + numerical d* (honest vs minority)
python3 t3_zeta.py                    # effective damping ratio (supporting)
```

All randomness uses fixed integer seeds, so a given configuration is bit-reproducible
across runs and machines. `t3_confirmatory.py` at `ctrl_delay_f=26, t3_obs_delay=1`
is bit-compatible with the base engine `adversary_ladder.py`.

## Key numbers (from the MC=50 grid)

- Minority beats the honest counterfactual in **74/96** conditions (77%); **12/12** at the design latency.
- Mechanism: minority contribution is anti-parallel to velocity (**cos ≈ −0.98**); damping coefficient is
  **minority-specific** (frame-level regression: minority k ≈ 0.28, R² ≈ 0.82; honest k ≈ 0).
- Quantization ablation (8→16→32 directions): effect **persists/grows** while the dead-zone shrinks 4× → rules out a dead-zone mechanism.
- Robust across smoothing α (0.1/0.2/0.4) and look-ahead (1/2/3); specific to continuous aggregation (majority voting ≈ no effect).
- Reduced model reproduces the honest latency curve (r ≈ 0.92, one-point calibration) but **fails to predict the honest–minority gap sign** at high delay (d44–d56 mistiming band): scalar approximation scope boundary.

## Minting a Zenodo DOI (do before manuscript submission)

1. Push this folder to a public GitHub repository.
2. Log in to https://zenodo.org with GitHub, enable the repository under **Settings → GitHub**.
3. On GitHub, create a **release** (e.g. `v1.0.0`). Zenodo automatically archives it and issues a DOI.
4. Copy the DOI badge into this README and update the `Data availability` statement and `CITATION.cff` in the manuscript.

> `CITATION.cff` is pre-filled (author, ORCID, license, keywords). Update `version` / `date-released`
> to match the GitHub release tag.
