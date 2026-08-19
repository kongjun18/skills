# End-To-End And Normalization

## Absolute Figures

Absolute figures answer deployability questions: what latency, throughput, cost, or resource usage should a reader expect?

### Grouped Bars

Use only when categories and methods are few. Bars start at zero.

### Dot Plots

Use horizontal dot plots when categories are many, labels are long, or differences are small. Dot plots can focus on the relevant range without exaggerating truncated bars.

### Lines

Use lines only when x has natural order, such as load, scale, time, or parameter value.

## Normalized Figures

For higher-is-better metrics:

```
normalized = system / baseline
```

For lower-is-better metrics:

```
speedup = baseline / system
```

Values above 1 mean the proposed system is better. Do not call the same number both a percentage reduction and a speedup factor.

## Paired Ratios

If baseline and system rows share the same run id, compute a ratio for each pair and then summarize ratios.

If runs are not paired, compute the ratio of estimates and warn in the audit.

## Geometric Mean

Use geometric means only when all ratios are positive and benchmark weighting is meaningful. Keep per-benchmark figures.

## Reference Line

Draw a 1.0× reference line. The baseline may appear as a 1.0 series or be omitted, but the caption must name it.