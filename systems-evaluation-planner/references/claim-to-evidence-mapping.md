# Claim To Evidence Mapping

## Claim Keywords And Required Evidence

| Claim Keyword | Meaning To Verify | Minimum Evidence |
| --- | --- | --- |
| Faster | Lower latency or completion time under the same workload and fairness conditions | Absolute end-to-end values, strongest baseline, repetitions |
| Higher throughput | More completed work per time at comparable latency/error constraints | Throughput plus latency or success-rate context |
| Lower tail latency | Lower p95/p99 or better tail distribution | Raw samples or valid quantiles; load context |
| Scalable | Performance improves or degrades gracefully as a named resource/scale increases | Scaling curve, ideal line or efficiency, bottleneck notes |
| Robust | Conclusions hold under skew, bursts, faults, hardware, parameters, or data scale | Robustness sweeps, boundary cases, failure points |
| Lower overhead | Added time, CPU, memory, I/O, network, or energy cost is small | Absolute overhead, additive breakdown, or resource plot |
| Lower cost | Cost, cost/request, or performance per dollar improves at equal quality or SLO | Cost model, measured usage, Pareto plot |

## Unsupported Wording Patterns

- One workload: cannot support “generally faster.”
- Only normalized speedups: cannot support absolute deployability or cost.
- No failure records: cannot support robustness under overload.
- Request samples only: cannot claim uncertainty across independent runs.
- Few datasets: cannot generalize to all workloads.
- Microbenchmarks only: cannot replace end-to-end evidence for a system claim.

## Figure Evidence Responsibility

For each figure record:

```yaml
id: fig-end-to-end
research_question: Does System-X improve throughput across datasets at stable load?
expected_claim: System-X improves throughput on most stable-load points across three datasets.
evidence_family: end_to_end_comparison
supported_wording: System-X improves mean throughput by X–Y% on these datasets under the stated load.
unsupported_wording: System-X is universally faster.
```