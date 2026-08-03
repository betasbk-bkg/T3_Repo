# Supplement S3. Replay Audit Variables and Provenance

## Scope

This table records existing replay/audit values used for observability and scale checks. These values are not validation results, not fitted theorem constants, and not a substitute for a complete global RMSE proof. Row counts are source indicators only.

This repository archive includes the replay source files under `data/theory_audit/replay_source_files/`, including `t3pub_frame_theorem_log.csv`, `paired_honest_t3_divergence_log.csv`, `boundary_switch_frame_log.csv`, `Btail_replay_audit.md`, and `Bswitch_replay_audit.md`.

## Tail-value reconciliation

The locked `B_tail_sum` definition follows the folder 14 tail-to-error bridge:

`TailFrameBound(t) = 2 |eta_anchor(t)| tail_pos_bound_h(t) + tail_pos_bound_h(t)^2.`

`B_tail_sum = sum_t TailFrameBound(t).`

Recomputing this expression from the 3900-row replay log gives:

| Quantity | Recomputed value |
|---|---:|
| `sum tail_pos_bound_h` | 0.894454661023498 |
| `sum tail_vel_bound_h` | 10.733455932281980 |
| `B_tail_sum` | 1.295747349145897 |
| `B_tail_sup` | 0.002278886002926 |

A previously propagated larger tail-scale diagnostic is not the `B_tail_sum` defined by the squared-error tail bridge. It is removed from the locked audit table rather than reused under the same name. The locked value below is tied to the displayed row-wise `TailFrameBound(t)` expression and the 3900-row replay-log basis.

| Code variable | Existing value | Interpretation | Source or provenance | Row/event basis | Manuscript status |
|---|---:|---|---|---|---|
| `sum_L_frame` | 49.051803583841895 | strict same-side local-relief audit sum | `data/theory_audit/replay_source_files/t3pub_frame_theorem_log.csv`; recomputed strict `A_ov` definitions from folder 13 | 3900 T3pub frame rows; 2046 strict `A_ov` rows reported by the included switch-audit source files | replay diagnostic only; overlapping horizons prevent use as global relief |
| `B_tail_sum` | 1.295747349145897 | candidate local projection-tube squared-error tail bridge | `data/theory_audit/replay_source_files/Btail_replay_audit.md`; recomputed from `tail_pos_bound_h` and `eta_anchor` in `t3pub_frame_theorem_log.csv` | 3900 T3pub frame rows | locally instantiable candidate; global use remains conditional on divergence/coupling |
| `B_tail_sup` | 0.002278886002926 | supremum of candidate per-frame tail bridge | `data/theory_audit/replay_source_files/Btail_replay_audit.md`; recomputed from `tail_pos_bound_h` and `eta_anchor` | 3900 T3pub frame rows | local audit scale only |
| `B_switch_universal` | 41.15438706760024 | universal switch-frame jump bound | `data/theory_audit/replay_source_files/Bswitch_replay_audit.md` | 193 state-induced switch frames from 217 vote frames | conservative audit bound; not used as a theorem constant |
| `B_switch_agg(gamma=1)` | 7.949795797231901 | aggregate-jump switch bound at assumed `gamma_min=1` | `data/theory_audit/replay_source_files/Bswitch_replay_audit.md` | 217 vote-frame aggregate jumps | conditional replay audit under assumed denominator |
| `B_switch_agg(gamma=cos(pi/8))` | 8.639694182510958 | aggregate-jump switch bound under explicit future `gamma_min` assumption | `data/theory_audit/replay_source_files/Bswitch_replay_audit.md` | 217 vote-frame aggregate jumps | conditional replay audit; `gamma_min` not derived from replay minima |
| `B_switch_m(gamma=cos(pi/8))` | 23.456873983056102 | per-vote `m_t` switch bound under explicit future `gamma_min` assumption | `data/theory_audit/replay_source_files/Bswitch_replay_audit.md` | 5092 state-induced agent switches across 217 vote frames | conservative replay audit; not a theorem constant |
| `state_divergence_norm` | mean 3.0626044587578165 | paired honest/T3 divergence diagnostic | `data/theory_audit/replay_source_files/paired_honest_t3_divergence_log.csv` | 3900 paired rows | logged pair only; no coupling bound |
| `B_div_smooth` | not instantiated | smooth divergence remainder | not closed in existing theorem packets | not applicable | missing term |
| `B_stoch` | not instantiated | stochastic coupling cost | not closed in existing theorem packets | not applicable | missing term |
| `m_neutral` | not instantiated | neutral-margin exclusion cost | not closed in existing theorem packets | not applicable | missing term |
| theorem-level `gamma_min` | not derived | denominator lower bound for switch bridge | folder 21 gives examples only | not applicable | assumption needed before theorem use |

## Replay packet anchors

The proof-oriented replay packet reports:

- `t3pub_frame_theorem_log.csv`: 3900 frame rows;
- `paired_honest_t3_divergence_log.csv`: 3900 paired rows;
- smooth circle scope valid for all logged replay frames;
- local relief and switch quantities audited without threshold tuning, gate addition, model refit, or validation claim.

The switch-bound packet reports:

- 217 vote frames;
- 193 state-induced switch frames;
- 5092 state-induced agent switches;
- all switch values are replay audits, not theorem-wide constants.

## Boundary

The local relief sum aggregates overlapping finite-horizon quantities around replay states. It is useful for checking observability and scale, but it cannot be inserted directly as a global relief term in a finite-horizon RMSE proof. `B_tail_sum` is locally in squared-error units but remains globally conditional on a divergence/coupling bound. A complete global theorem would still need independently defined and bounded `B_div_smooth`, `B_stoch`, `m_neutral`, and theorem-level `gamma_min`.
