# Data Contract

## Supported Tables

Read experiment data from common tabular formats: CSV, TSV, JSON, JSONL/NDJSON, and Parquet.

## Required Figure Fields

Each figure needs:

- `id`;
- `research_question`;
- `figure_type`;
- `data_file`;
- `columns`;
- `metric`;
- `output`.

## Common Column Roles

- `x`: categorical or ordered x-axis.
- `series`: method, system, or configuration.
- `facet`: dataset, workload, hardware, or another panel split.
- `value`: primary measured value.
- `repeat`: independent run id when available.
- `status`: success/failure status.
- `stack`: additive component for breakdowns.
- `total`: optional total for breakdown validation.
- `x_value` and `y_value`: values for tradeoff scatter.

## Metric Fields

- `label`: axis/caption label.
- `unit`: unit string.
- `direction`: `higher_is_better`, `lower_is_better`, or `no_direction`.
- `center`: `mean` or `median`.
- `error`: `95% confidence interval`, `standard deviation`, `standard error`, or `none`.

## Output Fields

For faceted plots, set:

```yaml
output:
  standalone: true
  combined_paper: true
  combined_overview: true
```