# Bswitch Replay Audit

Status: existing-log computation from 20 boundary logs and 12/13 theorem-variable logs only.

This is not validation.

## Inputs

Switch log:

```text
data/theory_audit/replay_source_files/boundary_switch_frame_log.csv
```

Eta/error source:

```text
data/theory_audit/replay_source_files/t3pub_frame_theorem_log.csv
```

Local relief comparison source:

```text
data/theory_audit/replay_source_files/
```

The strict `A_ov` local relief sum was recomputed from the 12 log using the folder 13 definitions.

## Constants

```text
MSPD = 5.0
alpha = 0.2
rho = 0.8
DT = 1/60
tau_frames = 18
kernel_pos = 1 - rho^18 = 0.981985601490518
```

Universal impulse displacement:

```text
b_universal = 0.16366426691508631.
```

## Switch Counts

```text
vote frames: 217
state-induced switch frames: 193
state-induced agent switches: 5092
```

## Vote-Frame Eta Stats

Using `|eta_anchor|` at vote frames:

```text
count:  217
min:    0.0
max:    1.8608640509792451
mean:   0.5604828478270193
median: 0.4976306245544322
sum:    121.62477797846319
```

## Logged Aggregate Jump Stats

`aggregate_jump_state_norm`:

```text
count:  217
min:    0.0
max:    1.400083681275891
mean:   0.3704097759417321
median: 0.22961005941905394
sum:    80.37892137935586
```

## Per-Vote m_t Stats

`m_t_state_induced`:

```text
count:  217
min:    0.0
max:    50.0
mean:   23.465437788018434
median: 16.0
sum:    5092.0
```

## B_switch Universal Bound

Using:

```text
||Delta U_switch|| <= 2*MSPD
```

on state-induced switch frames only:

```text
B_switch_universal_switch_frames = 41.15438706760024.
```

If charged on every vote frame:

```text
B_switch_universal_all_vote_frames = 45.62382057458364.
```

## B_switch Aggregate-Jump Bound

Using:

```text
||Delta U_switch(t)||
  <= MSPD * aggregate_jump_state_norm(t) / gamma_min,
```

the replay-derived symbolic coefficients are:

```text
B_switch_agg(gamma_min)
  =
  7.558486607376688 / gamma_min
  +
  0.39130918985521335 / gamma_min^2.
```

If `gamma_min = 1`:

```text
B_switch_agg = 7.949795797231901.
```

If a future theorem explicitly assumes or derives:

```text
gamma_min = cos(pi/8),
```

then the conditional value is:

```text
B_switch_agg = 8.639694182510958.
```

This `gamma_min` example is not fitted from observed denominator minima.

## B_switch Per-Vote m_t Bound

Using:

```text
||Delta A_switch(t)|| <= 2 m_t / N
```

and:

```text
||Delta U_switch(t)|| <= MSPD * (2 m_t/N) / gamma_min,
```

the symbolic coefficients are:

```text
B_switch_m(gamma_min)
  =
  19.063792704614247 / gamma_min
  +
  2.409046429125597 / gamma_min^2.
```

If `gamma_min = 1`:

```text
B_switch_m = 21.472839133739843.
```

If a future theorem explicitly assumes or derives:

```text
gamma_min = cos(pi/8),
```

then the conditional value is:

```text
B_switch_m = 23.456873983056102.
```

## Comparison With Local Relief

Strict `A_ov` local relief from folder 13, recomputed from 12:

```text
strict_Aov_count: 2046
sum_L_frame:      49.051803583841895
```

Ratios to `sum_L_frame`:

```text
universal switch-frame B_switch: 0.8389984477789286
aggregate gamma=1:              0.16206938820595446
aggregate gamma=cos(pi/8):      0.17613407767450473
m_t gamma=1:                    0.43775840162609614
m_t gamma=cos(pi/8):            0.47820614675181905
```

## Interpretation

The universal command bound is large but not instantly fatal in this replay.

The logged aggregate-jump bound is much tighter and appears usable as a replay audit.

The per-vote `m_t` bound is conservative but still materially tighter than universal switch-frame charging.

None of these values is a validation claim or a theorem-wide constant.
