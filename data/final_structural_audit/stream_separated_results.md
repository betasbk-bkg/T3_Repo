# Stream-Separated CRN Results

Status: completed.

## Quantizer Means

| q dirs | Vote-switch rate | Vote-switch chord2 | Agg jump chord2 | Path/vote co-occurrence | Positive T3 err2 increment | Mean counterfactual cost | Positive counterfactual tail |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.270811 | 0.654825 | 0.680313 | 0.095156 | 0.612278 | 0.002260 | 0.844643 |
| 8 | 0.441616 | 0.674607 | 1.056459 | 0.108594 | 0.412354 | 0.005007 | 0.621094 |
| 16 | 0.602145 | 0.434817 | 0.607436 | 0.095313 | 0.360253 | 0.007383 | 0.528409 |

## Coarse-Fine Contrasts

Contrast:

```text
q4 - q16
```

| Metric | Mean | 95% CI low | 95% CI high | Fraction positive | Strength |
|---|---:|---:|---:|---:|---|
| vote-switch chord2 | 0.220008 | 0.136443 | 0.309936 | 0.710938 | strong |
| aggregate jump chord2 | 0.072876 | -0.039394 | 0.180475 | 0.585938 | weak |
| path/vote co-occurrence | -0.000156 | -0.013908 | 0.014146 | 0.234375 | failed/none |
| positive T3 err2 increment | 0.252024 | 0.204352 | 0.299889 | 0.750000 | strong |
| mean counterfactual cost | -0.005123 | -0.013042 | 0.002533 | 0.531250 | not positive |
| positive counterfactual tail | 0.316234 | 0.256936 | 0.374913 | 0.781250 | strong |

## Directional Summary

Directional tests:

```text
4 / 6 passed
```

But this should not be used as a headline. The accurate breakdown is:

- strong: vote-switch magnitude burden;
- strong: positive T3 squared-error increment;
- strong: positive counterfactual cost tail;
- weak: aggregate jump burden;
- failed/none: path/vote co-occurrence;
- failed/none: mean counterfactual event cost.

## Frequency-Magnitude Trade-Off

Vote-switch rate increases with refinement:

```text
q4:  0.270811
q8:  0.441616
q16: 0.602145
```

Vote-switch magnitude burden is larger in coarse q4 than fine q16:

```text
q4:  0.654825
q16: 0.434817
q4 - q16 = 0.220008
```

This supports the frequency-magnitude trade-off, not a simple "coarser is always worse" law.

## Verdict

```text
FREQUENCY_MAGNITUDE_TRADEOFF_SURVIVES_STREAM_SEPARATION
```

