# A_ov Replay Audit

Status: audit using existing 12 replay logs only. No new simulations were run.

## Source

Existing log:

```text
data/theory_audit/replay_source_files/t3pub_frame_theorem_log.csv
```

Replay scope:

```text
circle, T3pub, tr = 0.30, delay = 26, N = 50, tau_frames = 18
```

## Definitions Used

```text
sigma = sign(eta_anchor)
q_h = -sigma * delta_eta_lin_h
B_h = R_curv_bound_h
q_safe = max(0, q_h - B_h)
```

Strict binary overshoot availability:

```text
A_ov = 1
```

if:

```text
q_h > B_h
and
q_h + B_h < |eta_anchor|.
```

Squared-error lower-bound contribution:

```text
L_frame = A_ov * max(0, 2*|eta_anchor|*q_safe - q_safe^2).
```

## Audit Counts

```text
total frames: 3900
invalid frames for A_ov calculation: 1
frames with q_h > 0: 2056
frames with q_h > B_h: 2056
strict binary A_ov = 1 frames: 2046
prior same-side count from 12: 2046
```

The strict `A_ov = 1` count matches the prior same-side count from the 12 replay audit.

## q_safe Summary

All-frame `q_safe` summary:

```text
sum:    31.468866721498205
mean:   0.00806894018499954
median: 0.0015994646357504775
```

Nonzero `q_safe` summary:

```text
count:  2046
mean:   0.015380677771993258
median: 0.013368458944534615
max:    0.03706188095777494
```

## L_frame Summary

```text
sum L_frame over all frames:    49.05180358384206
mean L_frame over all frames:   0.012577385534318477
median L_frame over all frames: 0.0003552255379484275
nonzero L_frame count:          2046
max L_frame:                    0.10642849732033607
```

## Interpretation

The 12 replay supports nonempty strict overshoot-available frames.

For this smooth circle replay, `A_ov` can be computed non-empirically from logged local quantities.

This does not validate T3 and does not close the global theorem.

