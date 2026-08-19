# Load Latency And Tail Latency

## X-Axis Semantics

State whether x is offered load, achieved throughput, clients, concurrency, or another scale. Offered load and achieved throughput are not interchangeable.

## Quantiles

When showing p50/p95/p99 together, encode systems by color and quantiles by line style. Avoid too many curves in one panel.

## SLOs And Saturation

If the paper uses an SLO, draw a horizontal reference line and report the maximum stable load satisfying it. Define saturation by a criterion such as latency threshold, error rate, or throughput plateau.

## Failures

Do not connect failed, timed-out, or OOM points to zero. Use gaps, explicit markers, or a separate failure-rate plot.

## Tail Claims

Tail claims require quantile or distribution evidence at comparable load. A single average latency curve cannot support low-tail-latency claims.