# Distribution Plots

## Valid Inputs

CDF and CCDF plots require raw samples or explicit weighted histograms. Precomputed p50/p95/p99 values are not enough.

## CDF Versus CCDF

- CDF emphasizes the body of the distribution.
- CCDF emphasizes tail probability.
- Log y-axis is useful for tail probability but requires positive values.

## Sampling Unit

State whether samples are requests, operations, windows, runs, or users. Do not confuse sample count with independent repetition count.

## Overplotting

If many curves overlap, facet by workload or dataset and still generate a complete overview.