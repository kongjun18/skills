# Data Contract

The shared contract between `systems-evaluation-planner` (which writes figure specs into `evaluation_plan.yaml`) and this skill (which renders them). This file is its single owner; the planner links here instead of restating it.

## Input tables

Read experiment data from CSV, TSV, JSON, JSONL/NDJSON, or Parquet. Never modify raw data; write every transform to `processed/`.

## Figure spec fields

Each figure in the plan needs:

| Field | Meaning |
| --- | --- |
| `id` | stable figure id, used in output file names |
| `research_question` | the one question the figure answers |
| `figure_type` | evidence family, e.g. `end_to_end_comparison`, `normalized_speedup`, `breakdown`, `load_latency`, `cdf`, `scalability`, `ablation`, `sensitivity`, `timeseries`, `tradeoff_scatter`, `heatmap` |
| `data_file` | path relative to the plan's `data.root_dir` |
| `columns` | column roles (below) |
| `metric` | metric fields (below) |
| `baseline` | named baseline, required for normalized and ablation figures |
| `output` | output scope (below) |
| `placement` | `main_core`, `main_explanation`, `appendix_completeness`, or `presentation` |

## Column roles

- `x`: categorical or ordered x-axis.
- `series`: method, system, or configuration.
- `facet`: dataset, workload, hardware, or another panel split.
- `value`: primary measured value.
- `repeat`: independent run id, when available.
- `status`: success or failure status; rows whose status is not the plan's `success_status_value` are failures and stay visible.
- `stack`: additive component for breakdowns; `total`: optional total for validating component sums.
- `x_value`, `y_value`: the two values of a tradeoff scatter.

## Metric fields

- `label`: axis and caption label.
- `unit`: unit string.
- `direction`: `higher_is_better`, `lower_is_better`, or `no_direction`.
- `center`: `mean` or `median`.
- `error`: `95% confidence interval`, `standard deviation`, `standard error`, `quantiles`, or `none`.

## Output scope

A figure with more than one facet value produces three outputs; a single-facet figure produces only the standalone one.

```yaml
output:
  standalone: true        # one figure per facet value
  combined_paper: true    # paper-ready small multiples, split into parts when panels exceed the limit
  combined_overview: true # every panel on one large vector canvas (or multipage PDF), for audit
  profiles: [paper-double]   # any of paper-single, paper-double, presentation
```

Plan-wide defaults go under `global.output` with the same keys (`generate_standalone`, `generate_combined_paper`, `generate_combined_overview`, `profiles`); a figure's `output` overrides them.

Profiles:

- `paper-single`: one column wide (about 3.33 in in common two-column templates);
- `paper-double`: full text width (about 7.0 in);
- `presentation`: 16:9, larger text, fewer secondary annotations. A presentation variant never changes data filtering, normalization, baseline, method order, statistical policy, or conclusions.

Use the actual `\columnwidth` or `\textwidth` of the user's template when it is known.

## Output layout

```
figures/standalone/
figures/combined-paper/
figures/combined-overview/
processed/      transformed tables used to draw each figure
captions/       caption drafts
audits/         one audit per figure
```

Each figure is emitted as PDF (TrueType fonts) plus a 300 DPI PNG; SVG only when requested.
