# Captions And Audits

Every figure ships with a caption draft in `captions/` and an audit in `audits/` (layout in [data-contract.md](data-contract.md#output-layout)).

## Caption structure

A caption states:

1. what the figure compares (the research question);
2. workload, dataset, and scale scope;
3. metric, unit, and direction;
4. baseline for comparisons or normalization;
5. center estimate, error-bar meaning, and repetition count;
6. the strongest quantitative conclusion, recomputable from the processed data;
7. how failures, missing values, or excluded points are handled, when relevant.

Do not put mechanism claims in a caption unless the plotted data directly supports them.

Example:

```
End-to-end throughput across three datasets; higher is better. Points show per-workload means over three independent runs, with 95% confidence intervals. Speedup is normalized to Baseline-A; runs that timed out are marked with x and excluded from the means.
```

## Audit contents

Each figure audit records and checks:

- input file paths and checksums; required columns present;
- row counts before and after filtering; missing values and failure rows;
- duplicate keys and unbalanced repetitions;
- units, metric direction, and the baseline; the normalization formula, with the baseline equal to 1 where applicable;
- component-sum checks for breakdowns;
- log axes contain no non-positive values;
- missing values were not filled as zero;
- PDF fonts embedded, none Type 3 (`pdffonts <file>.pdf`);
- every required output exists (standalone, combined paper, combined overview, PDF and PNG, SVG when requested);
- processed-data path, output paths, and the caption numbers recomputed from processed data;
- warnings and errors.

## Audit policy

Errors block delivery. Warnings may be delivered only when explained and when they do not invalidate the claim.
