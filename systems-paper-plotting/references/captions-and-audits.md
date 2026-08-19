# Captions And Audits

## Caption Structure

A caption should state:

1. what the figure compares;
2. workload, dataset, and scale scope;
3. metric unit and direction;
4. baseline for comparisons or normalization;
5. center estimate, error-bar meaning, and repetition count;
6. the strongest quantitative conclusion supported by processed data;
7. how failures, missing values, or excluded points are handled.

Example:

```
End-to-end throughput across three datasets; higher is better. Points show per-workload means over three independent runs, with 95% confidence intervals. Speedup is normalized to Baseline-A, and failed runs are omitted only when the audit records an explicit timeout.
```

## Audit Contents

Each figure audit should include:

- input file path and checksum;
- required columns;
- row counts before and after filtering;
- missing values and failure rows;
- duplicate keys and unbalanced repetitions;
- normalization formula and baseline;
- component-sum checks for breakdowns;
- processed data path;
- output file paths;
- derived caption numbers;
- warnings and errors.

## Audit Policy

Errors block delivery. Warnings may be delivered only when explained and when they do not invalidate the claim.