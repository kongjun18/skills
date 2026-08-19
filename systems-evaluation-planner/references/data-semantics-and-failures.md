# Data Semantics And Failure Handling

## Metric Semantics

For every metric, record:

- unit;
- whether higher or lower is better;
- whether values are raw samples, per-run summaries, or already aggregated;
- whether the metric is bounded or can be zero/negative;
- whether the metric is comparable across workloads or only within a workload.

## Repetition Semantics

Do not treat all rows as independent repetitions. Identify whether a row represents:

- an independent run;
- a random seed;
- a client;
- a request;
- a time-window sample;
- an aggregate produced by another tool.

Confidence intervals over independent runs are not the same as intervals over requests.

## Failure Semantics

Explicitly classify:

- timeout;
- out of memory;
- crash;
- aborted run;
- overload or saturation;
- missing measurement;
- value outside the measurement range.

Never convert these to zero unless zero is the true measured value. Prefer gaps, explicit failure markers, or separate failure-rate figures.

## Load Semantics

Record whether the x-axis is:

- offered load;
- achieved throughput;
- number of clients;
- concurrency;
- data size;
- elapsed time.

Offered load and achieved throughput answer different questions and must not be silently swapped.