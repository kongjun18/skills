---
name: systems-paper-plotting
description: Create publication-quality plots for systems research papers from an evaluation_plan.yaml and local experiment data. Use when Codex needs to render end-to-end comparisons, normalized speedups, performance breakdowns, load-latency curves, CDF/CCDF tail plots, scalability, ablation, sensitivity, resource time-series, tradeoff scatter, or heatmap figures; generate standalone plots, paper combined figures, complete overview figures, captions, processed data, and audit files; or validate that systems-paper figures avoid misleading normalization, statistics, axis, and layout choices; or iteratively refine rendered paper figures through a reviewer-subagent review → verify → refine loop ("refine figures", "review and fix figures", "polish figure X").
---

# Systems Paper Plotting

## Goal

Convert an executable `evaluation_plan.yaml` plus local experiment data into paper-ready systems figures, processed data, caption drafts, and audit files.

This skill is opinionated: every plotted number must be traceable to input data, and every visual choice must preserve the evidence semantics planned by `systems-evaluation-planner`.

## Input Contract

Use this skill after the planner has produced an executable plan, or when the user already provides equivalent figure specs.

Required inputs:

- `evaluation_plan.yaml` (or an equivalent figure spec) describing each figure's research question, columns, metric, baseline, and output scope;
- raw data root directory;
- metric units, directions, baselines, repetitions, and failure semantics;
- target outputs: main paper, appendix, presentation, or all of them.

Read [Data Contract](references/data-contract.md) when mapping input tables and output fields.

This is a guidance skill: it does not ship a renderer. You write the plotting code yourself, applying the rules below and in the reference files. When a plan is not yet executable, resolve the blocking semantics (or hand back to `systems-evaluation-planner`) before plotting.

## Non-Negotiable Rules

1. **No invented values.** Never fill missing data with zeros unless zero is the measured value.
2. **Absolute before normalized.** Keep absolute figures separate from normalized speedup/slowdown figures.
3. **Baseline must be explicit.** Normalized plots require a named baseline and a 1.0× reference line.
4. **Statistical unit matters.** Independent runs are the default unit; request samples do not become runs.
5. **Failures stay visible.** Timeouts, OOMs, crashes, and overload must appear as gaps, markers, warnings, or separate failure evidence.
6. **Breakdowns must add up.** Use stacked bars only for mutually exclusive additive components.
7. **Multi-facet figures need three outputs.** Generate standalone plots, paper combined figures, and complete overview figures.
8. **Readable at final size.** Check paper figures at their physical paper size, not only as enlarged screenshots; no text below 7 pt at print size.
9. **Captions must be reproducible.** Any quantitative caption claim must be recomputable from processed data.
10. **Avoid misleading decoration.** No 3D, gradients, dual y-axes, arbitrary truncated bars, bars on log axes, or decorative backgrounds.

Read [Anti-Patterns](references/anti-patterns.md) before choosing an unusual chart form or axis treatment.

## Workflow

1. **Validate the plan.** Ensure status is executable, blocking questions are empty, inputs exist, and each figure has data, columns, metric, baseline, and output requirements.
2. **Inspect data semantics.** Confirm units, directions, repetition columns, failure columns, and whether raw samples are available.
3. **Render each figure family.** Choose forms according to evidence semantics; do not force every result into bars.
4. **Render standalone and combined outputs.** For each multi-facet figure, produce per-facet standalone plots, paper combined plots, and complete overview plots.
5. **Write processed data and audits.** Save the transformed data, normalization formulas, warnings, errors, and output file list.
6. **Draft captions.** State the research question, data scope, metric direction, baseline, uncertainty, repetitions, and reproducible quantitative result.
7. **Review final-size readability.** Check labels, legends, panel count, and whether the layout still supports the intended claim. For iterative polishing, run the refinement loop below.

## Visual Style Principles

- Emit PDF for papers and a 300 DPI PNG for quick review; add SVG only when a non-LaTeX consumer needs it.
- Embed TrueType (Type 42) fonts, never Type 3: set `pdf.fonttype = 42` and `ps.fonttype = 42` (Matplotlib defaults to Type 3, which ACM and USENIX PDF checks flag).
- Use sans-serif fonts; size text so it is 7–9 pt at print size (set size × print width / figsize width).
- Label every quantitative axis with its unit, e.g. `Latency (ms)`; scale values into readable units (`Mops/s`, `GB`) instead of Matplotlib offset text such as `1e6`.
- Remove top and right spines.
- Keep only light grid lines that help value reading.
- Use borderless legends.
- Let captions carry long titles; keep in-figure titles short.
- Use neutral gray for baselines, a single primary accent for the proposed system, and restrained auxiliary colors for others.
- Encode important distinctions with markers, line styles, or hatches in addition to color.
- Keep method order and visual mappings consistent across all standalone and combined figures.
- Size the canvas to the placed width so LaTeX scales it by 1.00, and do not save with `bbox_inches="tight"`, which changes the canvas width.
- Place axes in inches (`fig.add_axes`) with fixed margins, panel gaps, and one band for a shared legend, so rearranging panels keeps them equal in size and text unscaled.
- Check annotations and guide-line labels against the curves at print size, and render a grayscale copy to confirm every series stays distinguishable.

See [Visual Style Principles](references/visual-style-principles.md).

## Figure Family Rules

### End-To-End Comparison

- Few workloads and methods: grouped bars are acceptable.
- Many categories or long labels: use horizontal dot plots.
- Naturally ordered x-axis: use lines.
- Do not connect unordered categories with lines.
- Bars must start at zero; if small differences need focus, use dot plots and confidence intervals instead of truncating bars.

### Normalization

- Separate absolute and normalized figures.
- Higher is better: `system / baseline`.
- Lower is better: `baseline / system`.
- Draw a 1.0× reference line.
- Name the baseline.
- When ratios fall on both sides of 1.0 or span more than about 10×, use a log₂ y-axis so 0.5× and 2× sit equally far from 1.0, and show ratios as dots, not bars.
- With paired repetitions, compute ratios per run before summarizing; without pairing, use ratio of estimates and warn in the audit.
- Geometric means across benchmarks may summarize but must not replace per-benchmark results.

See [End-To-End And Normalization](references/end-to-end-and-normalization.md).

### Performance Breakdown

- Prefer absolute time, resource, cycles, bytes, or energy.
- Use stacked bars only when components are mutually exclusive and additive.
- Percent breakdowns are supplementary only.
- Keep component order fixed across every figure.
- Use time-series, interval, or concurrency plots for overlapping components.
- Validate component sums; total mismatches must enter the audit.
- For many systems and workloads, use grouped stacked bars rather than changing structure per panel.

See [Performance Breakdown](references/performance-breakdown.md).

### Load, Throughput, And Latency

- State whether x is offered load, achieved throughput, clients, or concurrency.
- When p50/p95/p99 share a plot, encode system by color and quantile by line style.
- Draw SLO reference lines when applicable and report the maximum stable load satisfying the SLO.
- Mark saturation using an explicit criterion, not visual intuition.
- Do not connect failed, OOM, or timed-out points as zero; use gaps or explicit symbols.
- With achieved throughput on x, connect points in offered-load order and mark post-saturation points, since the curve can fold back.
- Use a log latency axis when tails grow by orders of magnitude near saturation.

See [Load Latency And Tail Latency](references/load-latency-and-tail-latency.md).

### CDF And CCDF

- Compute only from raw samples or explicit weighted histograms.
- Do not draw a CDF from only p50/p95/p99.
- Use CDF for the body; use CCDF or log scale for the tail.
- Report sample count and sampling unit.
- Split overcrowded curves into facets and still generate a complete overview.

See [Distribution Plots](references/distribution-plots.md).

### Scalability, Ablation, And Sensitivity

- Scalability plots show actual values; add ideal lines, speedup, or efficiency only when useful.
- State the ideal-line reference point.
- Ablations change one clear factor at a time and use the full system as baseline.
- Sensitivity with natural order uses lines; unordered configurations use points or bars.
- Do not call multi-factor configuration changes ablations.

See [Scalability Ablation Sensitivity](references/scalability-ablation-sensitivity.md).

### Resource Time-Series, Tradeoff Scatter, And Heatmap

- Time-series: state the sampling interval and any smoothing window; mark or exclude warm-up; annotate injected events (failures, compaction, reconfiguration) at their timestamps.
- Tradeoff scatter: mark the "better" corner or arrow on the axes; draw the Pareto frontier only over measured points.
- Heatmap: use a perceptually uniform sequential colormap, or a diverging one centered at 1.0 for ratios; always include a colorbar with units; annotate cell values when the grid is small.

See [Time-Series Scatter Heatmap](references/timeseries-scatter-heatmap.md).

## Standalone And Combined Figures

When facets have multiple values, generate by default:

1. per-facet standalone figures;
2. `combined-paper`: paper-ready small multiples, split into parts when panel count is high;
3. `combined-overview`: a large-canvas vector overview with every panel for one-pass inspection;
4. presentation variants when the plan requests presentation output.

A combined figure is not a cross-dataset average. Add aggregation only when the plan explicitly requests it and units/statistical meaning are compatible.

Within one combined figure:

- keep method order, colors, markers, hatches, and component order consistent;
- share y-axes only when scales are similar and most panels remain readable;
- do not force different units, metric directions, or breakdown definitions onto one axis;
- prefer shared legends;
- keep panel labels and facet titles short;
- default to at most six panels per paper figure part; enlarge the overview canvas instead of shrinking panels indefinitely.

See [Combined Figures](references/combined-figures.md).

## Statistics And Error

- Independent runs are the default statistical unit.
- Use mean and 95% confidence intervals for roughly symmetric repeated-run results.
- Use medians, quantiles, CDFs, or CCDFs for skewed latency.
- Use Student-t intervals for small samples.
- Captions must state whether error bars are standard deviation, standard error, confidence interval, or quantiles.
- With too few runs, show individual points rather than pretending uncertainty is precise.
- Do not shrink confidence intervals by treating request-level samples as independent runs.

See [Statistics And Error](references/statistics-and-error.md).

## Paper And Presentation Profiles

Supported profiles:

- `paper-single`: approximately 3.33 inches wide (`\columnwidth` in the USENIX and acmart templates);
- `paper-double`: approximately 7.0 inches wide (`\textwidth`);
- `presentation`: widescreen, larger text, fewer secondary annotations.

Presentation variants must not change data filtering, normalization formula, baseline, method order, statistical policy, or conclusions.

## Producing Figures

Write the plotting code yourself (Matplotlib is the assumed default) for each figure, applying the rules in this file and the reference documents. There is no bundled renderer to hide behind: every transform from raw data to plotted number is code you can inspect.

Hold every figure to the same discipline:

- Read raw data directly; never fabricate, interpolate, or zero-fill missing values.
- Keep the transform auditable: filter to successful rows, compute the center and error explicitly, and save the transformed table used to draw the figure.
- Emit each figure as PDF (Type 42 fonts) for the paper, plus a 300 DPI PNG for quick review.
- Write a processed-data table, a caption draft, and an audit note alongside each figure.
- Print the numbers that the caption and paper text quote, and compare them before handing off.
- After refactoring a plot script, render the old configuration and confirm it matches the old output pixel for pixel before making any visible change.

A convention that keeps outputs organized:

```
figures/standalone/
figures/combined-paper/
figures/combined-overview/
processed/
captions/
audits/
```

Reuse one style module across all figures so method order, colors, markers, hatches, and component order stay globally consistent (see [Visual Style Principles](references/visual-style-principles.md)).

## Figure Refinement Loop

To polish rendered figures, run a review → verify → refine loop: a fresh reviewer subagent critiques each figure against its paper claim at print size, you verify every finding against the image, script, and data, apply only accepted layout fixes, regenerate, re-check the non-negotiable rules, and repeat. Scope is presentation/layout only; data, panel, metric, chart-type, figsize, and shared-naming changes are escalated to the human, not applied.

Read [Refinement Loop](references/refinement-loop.md) for the phases, verdicts, escalation triggers, and ledger format, and fill [Reviewer Brief](references/reviewer-brief.md) as the reviewer's prompt.

## Caption Drafts

Each caption must include:

- research question or comparison;
- workload, dataset, or scale range;
- metric and direction;
- baseline;
- error-bar meaning and repetition count;
- quantitative conclusion recomputable from processed data;
- handling of timeouts, missing data, or anomalies when relevant.

Do not write mechanism claims in captions unless the plotted data directly supports them.

## Audits

Each audit must check at least:

- input files and required columns exist;
- units, metric direction, and baseline;
- duplicate keys and unbalanced repetitions;
- normalized baseline equals 1 where applicable;
- performance-breakdown component sums;
- log axes contain no non-positive values;
- PDF fonts are embedded and none are Type 3 (`pdffonts <file>.pdf`);
- missing values are not filled as zero;
- standalone and combined figures are complete;
- PDF and PNG outputs exist (SVG when requested);
- caption numbers can be recomputed from processed data.

See [Captions And Audits](references/captions-and-audits.md).

## Done Criteria

Deliver only when:

- no blocking data semantics remain unresolved;
- all main figures are readable at final physical size;
- multi-facet figures include standalone, paper combined, and complete overview outputs;
- absolute and normalized views are separate;
- performance breakdown additivity passes or the figure type changes;
- error-bar semantics are explicit;
- PDF, PNG, processed data, captions, and audits are complete;
- visuals contain no 3D effects, gradients, dual y-axes, bars on log axes, misleading truncation, Type 3 fonts, or decorative noise;
- audits have no errors and warnings are explained.
