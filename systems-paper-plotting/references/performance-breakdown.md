# Performance Breakdown

## Additivity Requirement

Stacked bars require mutually exclusive components that sum to a meaningful total. Examples include exclusive runtime phases or byte categories.

If components overlap in time, use intervals, time series, or concurrency views.

## Absolute Before Percent

Plot absolute time, bytes, CPU, memory, I/O, energy, or cost. Percent breakdowns may supplement but should not be the only evidence.

## Component Order

Keep component order fixed across systems, workloads, and facets. Do not reorder stacks per panel.

## Total Validation

When total columns exist, compare component sums with totals. Significant mismatch is an audit error unless the plan defines a known excluded category.

## Many Systems Or Workloads

Use grouped stacked bars with stable structure. Do not let each panel choose a different component set unless missing components are explicitly zero or not applicable.