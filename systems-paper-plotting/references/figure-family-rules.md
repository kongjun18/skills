# Figure Family Rules

Read the section for each figure family you render, plus Statistics and Anti-Patterns for every figure. Visual styling is in [visual-style-principles.md](visual-style-principles.md); input and output fields are in [data-contract.md](data-contract.md).

## Contents

1. [End-to-end comparison](#1-end-to-end-comparison)
2. [Normalization](#2-normalization)
3. [Performance breakdown](#3-performance-breakdown)
4. [Load, throughput, and latency](#4-load-throughput-and-latency)
5. [Distributions: CDF and CCDF](#5-distributions-cdf-and-ccdf)
6. [Scalability, ablation, and sensitivity](#6-scalability-ablation-and-sensitivity)
7. [Resource time series](#7-resource-time-series)
8. [Tradeoff scatter](#8-tradeoff-scatter)
9. [Heatmap](#9-heatmap)
10. [Combined figures](#10-combined-figures)
11. [Statistics and error](#11-statistics-and-error)
12. [Anti-patterns](#12-anti-patterns)

## 1. End-to-end comparison

Absolute figures answer deployability questions: what latency, throughput, cost, or resource use should a reader expect?

- **Grouped bars** only when categories and methods are few. Bars start at zero.
- **Horizontal dot plots** when categories are many, labels are long, or differences are small. A dot plot can focus on the relevant range with confidence intervals; never truncate bars to do it.
- **Lines** only when x has a natural order (load, scale, time, parameter value). Never connect unordered categories.

## 2. Normalization

- Keep normalized figures separate from absolute ones; normalized values supplement, they do not replace.
- Higher is better: `normalized = system / baseline`. Lower is better: `speedup = baseline / system`. Values above 1 mean the proposed system is better. Do not call the same number both a percentage reduction and a speedup factor.
- Name the baseline and draw a 1.0× reference line. The baseline may appear as a 1.0 series or be omitted, but the caption names it.
- **Paired runs:** if baseline and system rows share a run id, compute a ratio per pair, then summarize. Unpaired: use the ratio of estimates and warn in the audit.
- **Geometric mean** across benchmarks only when every ratio is positive and the weighting is meaningful; it summarizes and never replaces per-benchmark results. Do not take arithmetic means of ratios.
- **Ratio axis:** when ratios fall on both sides of 1.0 or span more than about 10×, use a log₂ axis with ticks at 0.25×, 0.5×, 1×, 2×, 4×, so equal-factor wins and losses sit equally far from 1.0, and draw ratios as dots. Bars on a linear ratio axis only when every ratio is at least 1.0, still starting at zero.

## 3. Performance breakdown

- Plot absolute time, cycles, bytes, CPU, memory, I/O, energy, or cost. Percent breakdowns are supplementary only.
- **Stacked bars only for mutually exclusive, additive components** that sum to a meaningful total. Components that overlap in time need intervals, time series, or concurrency views.
- Keep component order fixed across every system, workload, facet, and figure.
- When totals exist, compare component sums with them; a significant mismatch is an audit error unless the plan names an excluded category.
- For many systems and workloads, use grouped stacked bars with one stable component set; a missing component is explicitly zero or marked not applicable.

## 4. Load, throughput, and latency

- State whether x is offered load, achieved throughput, clients, or concurrency; offered load and achieved throughput are not interchangeable.
- With p50/p95/p99 together, encode system by color and quantile by line style; keep the curve count per panel small.
- With an SLO, draw it as a reference line and report the maximum stable load that meets it. Define saturation by an explicit criterion (latency threshold, error rate, throughput plateau), not by eye.
- Never connect failed, timed-out, or OOM points as zero; use gaps, explicit markers, or a separate failure-rate plot.
- With achieved throughput on x, the curve can fold back past saturation: connect points in offered-load order (never sorted by x) and mark post-saturation points.
- Use a log latency axis when tails grow by orders of magnitude near saturation.
- A tail-latency claim needs quantile or distribution evidence at comparable load; one average-latency curve cannot support it.

## 5. Distributions: CDF and CCDF

- Compute only from raw samples or explicit weighted histograms. Never draw a CDF from p50/p95/p99 alone.
- Use a CDF for the body and a CCDF (log y, positive values only) for the tail.
- Report the sample count and the sampling unit (requests, operations, windows, runs, users); sample count is not repetition count.
- Facet overcrowded curves by workload or dataset, and still produce the complete overview.

## 6. Scalability, ablation, and sensitivity

- **Scalability:** plot actual values against a named scaling axis (threads, cores, nodes, clients, data size). Add speedup, efficiency, or an ideal line only with a stated reference point.
- **Ablation:** the full system is the baseline; change one component or mechanism at a time. Multi-factor changes are a configuration comparison, not an ablation.
- **Sensitivity:** lines for ordered parameters (cache size, threshold, skew), dots or bars for unordered configurations; mark the default setting when it matters for interpretation.

## 7. Resource time series

- Put time on x with its unit and origin (for example, seconds since load start). State the sampling interval; if you smooth, state the window and keep raw points in the processed data.
- Mark or exclude warm-up explicitly; do not silently crop it.
- Annotate injected events (failures, compaction, GC, reconfiguration, load changes) with vertical lines at their logged timestamps.
- Plot different resources in stacked panels that share the time axis, not on dual y-axes.

## 8. Tradeoff scatter

- Label both axes with metric, unit, and direction; mark the "better" corner or add a direction arrow.
- Draw a Pareto frontier only through measured points, never interpolated ones.
- Label points directly when there are few; use a legend otherwise. Keep method colors and markers identical to the other figures.

## 9. Heatmap

- Use a perceptually uniform sequential colormap (for example `viridis`) for magnitudes, or a diverging colormap centered at 1.0 (log-normalized) for ratios. No `jet` or rainbow maps.
- Always include a colorbar with metric and unit.
- Annotate cell values when the grid is readable at print size; choose text color by cell luminance.
- Show missing or failed cells with a pattern or color outside the colormap, never as the minimum value.

## 10. Combined figures

Which outputs to produce is set by the output scope in [data-contract.md](data-contract.md#output-scope). Layout rules:

- A combined figure is small multiples with shared encoding, not a cross-dataset average. Add an aggregate panel only when the plan requests it and units and statistical meaning are compatible.
- Default to at most six panels per paper figure part; split into parts rather than shrinking panels. The complete overview is for audit: enlarge the vector canvas or use multipage PDF instead.
- Keep method order, colors, markers, hatches, line styles, component order, and normalization policy identical across standalone and combined outputs.
- Share y-axes only when scales are similar and most panels stay readable; never force different units, metric directions, or breakdown definitions onto one axis.
- Prefer one shared legend and short panel labels and facet titles.

## 11. Statistics and error

- Independent runs are the default statistical unit. Requests, time windows, and operations are not independent runs unless the experiment design says so; never shrink intervals by treating them as runs.
- Roughly symmetric repeated-run results: mean with a 95% confidence interval (Student-t for small samples).
- Skewed latency: median, quantiles, CDF, or CCDF.
- Too few runs: plot the individual runs instead of an interval that pretends to be precise.
- Captions state what error bars mean (standard deviation, standard error, confidence interval, quantile range) and the repetition count. Do not mix standard-deviation and confidence-interval language.

## 12. Anti-patterns

Do not produce these unless the user asks for a diagnostic sketch that will not be used as evidence:

- normalized-only results with no absolute values, or percent-only breakdowns with no absolute total;
- truncated bar axes, bars on a log axis, or speedups on a linear axis where 0.5× looks half as far from 1.0 as 2×;
- dual y-axes, 3D effects, gradients, or decorative backgrounds;
- missing or failed runs drawn as zero;
- a CDF from summary quantiles;
- request-level error bars presented as run-level uncertainty;
- methods or components reordered between panels, or lines connecting unordered categories;
- a combined figure that averages incompatible datasets;
- axis labels without units, Matplotlib offset text (`1e6`) standing in for a unit, or Type 3 fonts in the PDF.
