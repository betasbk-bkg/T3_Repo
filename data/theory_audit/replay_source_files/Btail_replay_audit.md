# B_tail Replay Audit

Status: existing-log audit only. No new simulations were run.

## Source Logs

Existing replay log:

```text
data/theory_audit/replay_source_files/t3pub_frame_theorem_log.csv
```

Existing effective-relief definition:

```text
data/theory_audit/replay_source_files/effective_relief_definition.md
```

## Candidate TailFrameBound

Using:

```text
TailFrameBound
  = 2*|eta_anchor|*tail_pos_bound_h + tail_pos_bound_h^2.
```

## tail_pos_bound_h Stats

```text
count:  3900
min:    0.0
max:    0.0007229891360506495
mean:   0.0002293473489803842
median: 0.00003248669454988074
sum:    0.8944546610234984
sup:    0.0007229891360506495
```

## tail_vel_bound_h Stats

```text
count:  3900
min:    0.0
max:    0.008675869632607795
mean:   0.0027521681877646104
median: 0.00038984033459856887
sum:    10.73345593228198
sup:    0.008675869632607795
```

## Candidate TailFrameBound Stats

```text
count:  3900
min:    0.0
max:    0.002278886002925662
mean:   0.0003322429100374095
median: 0.000039514624081859854
sum:    1.295747349145897
sup:    0.002278886002925662
```

Thus:

```text
B_tail_sum candidate = 1.295747349145897
B_tail_sup candidate = 0.002278886002925662
```

## Descriptive Comparison With L_frame

From the 13 `A_ov/r_eff` definition applied to the same existing log:

```text
sum L_frame = 49.05180358384206
```

Descriptive ratio:

```text
B_tail_sum candidate / sum L_frame = 0.02641589614398447
```

This is only a theorem-variable audit comparison. It is not validation and does not prove global closure.

## Interpretation

The local projection-tube tail-to-squared-error conversion is numerically instantiable for this replay.

But `B_tail_sum` is only a candidate local tail bound unless a theorem shows that `tail_pos_bound_h` captures the relevant closed-loop tail cost over the interval.

