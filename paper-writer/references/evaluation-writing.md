# Evaluation Writing

Write each evaluation paragraph as a supported argument about one finding:
**question → quantified result → explanation → boundary of the result**.
Use this guide within the parent skill's outline, writing, and simplification
stages; it does not add a review loop or require new experiments.

## Section structure: results before diagnosis

Open with the questions the available experiments answer. A useful default
order is below; adapt it to the paper's claims and existing evidence rather
than adding subsections merely to fill the template.

| Part | Reader's question | Presentation objective |
|---|---|---|
| Setup | Is the comparison interpretable and fair? | Define baselines, resource budgets, workloads, metrics, and measurement procedure. |
| Overall results | Does the system improve the target outcome? | Establish the main result and how broadly it holds. |
| Ablations and breakdowns | Which mechanisms explain the result? | Connect design choices to measured effects and costs. |
| Sensitivity and tradeoffs | When does the benefit grow, shrink, or reverse? | Explain parameter dependence and limitations. |
| Application results | Does the benefit survive integration? | Show application-visible outcomes. |
| Scalability | What happens as resources or demand increase? | Quantify scaling and identify remaining bottlenecks. |

In the outline, map each question to its figure or table, one intended
takeaway, and the evidence supporting any explanation. Assign sentence roles
before drafting prose. Do not turn the section into a figure-by-figure tour
without a chain of questions and answers.

## Result paragraph roles

| Move | What the sentence contributes |
|---|---|
| Orient | Identify the workload, varied parameter, and figure. Include only setup details needed here. |
| State the finding | State which metric changes, against which baseline, under which conditions. |
| Quantify | Give representative values or a range; add a complementary metric when it changes the interpretation. |
| Explain | Connect the performance difference to a bottleneck and the mechanism that changes it, with supporting evidence. |
| Qualify | Discuss a meaningful exception, crossover, regression, diminishing return, or unresolved observation. |
| Interpret | State the scoped design implication, if it is not already clear. |

The finding and evidence are essential. Other moves may span adjacent
paragraphs or be omitted when unnecessary. Put the finding first when the
setup is already clear. Do not force six sentences, invent an anomaly, or
end every paragraph with a generic claim that the design is effective.

### Adaptable prose template

> Under [workload and condition], [system] achieves [result] relative to
> [baseline] (Figure [X]). Across [parameter range], the advantage
> [grows/shrinks/remains stable], with [representative evidence]. [Baseline]
> is limited by [bottleneck], whereas [mechanism] reduces [specific cost];
> [ablation or diagnostic measurement] supports this explanation. However,
> at [boundary condition], [exception], because [supported explanation, or
> explicitly labeled hypothesis]. These results support [scoped conclusion].

Use only the supported parts of this template. Preserve the parent skill's
phase rules and source requirements when results or explanations are missing.

## Explain comparisons through bottlenecks

Build explanations around:

**workload property → bottleneck → design mechanism → measured consequence**

- Group baselines with the same limitation; discuss them separately when
  their mechanisms differ. Avoid repetitive baseline-by-baseline prose.
- Explain changes in the performance gap as well as changes in absolute
  performance. All systems slowing down does not explain why one slows less.
- Distinguish relative disadvantage from failure. Lower throughput alone
  does not establish malfunction or architectural inadequacy.
- Match causal language to evidence: “the breakdown shows” for measured
  effects, “is consistent with” for indirect evidence, and “we hypothesize”
  for an unverified explanation. A throughput plot alone usually establishes
  the outcome, not its cause.
- Use ablations, counters, profiles, or controlled comparisons to support
  causal explanations. If those are unavailable, narrow the wording; do not
  invent measurements or silently turn a plausible mechanism into a fact.

## Adapt the narrative to the experiment

| Experiment | Recommended narrative |
|---|---|
| Baseline comparison | Overall ranking → magnitude → conditions that change the gap → explanation. |
| Ablation | Precisely define the change → incremental effect → affected cost → interactions with other components. |
| Cost breakdown | Total cost → dominant components → added overhead and saved work → net result. |
| Parameter sweep | Trend → saturation or crossover → competing effects → practical implication. |
| Stability | Dips, bursts, or dispersion → frequency or severity → connection to measured system events. |
| Application | Integration and workload → application-visible gain → whether engine-level benefits survive other costs. |
| Scalability | What grows and stays fixed → aggregate throughput and scaling efficiency → saturation or shared bottleneck. |

For incremental ablations, say “adding B on top of A improves throughput
by ….” Do not call this B's independent contribution without an experiment
that isolates it. For scalability, distinguish increasing capacity from
proportional throughput scaling; report per-node behavior when aggregate
throughput could conceal declining efficiency.

## Exceptions define operating conditions

Look for losses or narrowing advantages, opposing effects on throughput and
latency or resource use, saturation, nonmonotonic trends, baseline rank
changes, and discrepancies between expected and observed behavior. State
the condition and its consequence. Explain it when evidence permits;
otherwise identify the cause as unresolved. Do not hide regressions behind
an aggregate gain or invent exceptions to complete the paragraph structure.

## Quantitative reporting and final checks

- Attach each number to a metric, baseline, and condition. Include absolute
  values when ratios alone obscure the practical effect.
- Prefer “2.0× the throughput of B” or “100% higher throughput” over ambiguous
  “2× improvement.” Compute a latency reduction as (baseline − system) /
  baseline; distinguish relative percentages from percentage points.
- Accompany an “up to” result with typical behavior or the range across
  tested conditions. Do not let an extreme stand in for the full result.
- Separate equal-resource comparisons from experiments adding memory,
  cores, or nodes. Identify references with different guarantees, such as
  nonpersistent upper bounds, and keep conclusions within that scope.
- Distinguish less traffic on one link from less total traffic, and
  overlapped work from eliminated work. Account for where costs move.
- Report the repetition and aggregation procedure in setup. Do not infer
  statistical significance or run-to-run stability from means alone.
- Verify that prose, figures, tables, captions, units, and calculated
  percentages agree. Ensure every explanation has evidence or an explicit
  uncertainty qualifier and every conclusion stays within tested conditions.

## Presentation reference and scope

This guide synthesizes patterns observed in §5 of
[O³-LSM: Maximizing Disaggregated LSM Write Performance via Three-Layer Offloading](https://arxiv.org/html/2603.05439v1#S5)
and additional reporting safeguards. It is guidance for presentation, not
an endorsement of every claim or numerical convention in that paper.

Useful structural examples: §5.2 moves from quantified comparisons to
workload-dependent explanations and discusses skew's opposing read/write
effects; §5.3 uses incremental designs, cost breakdowns, and local/remote
memtable tradeoffs. Reuse these argument shapes, not the paper's wording,
numbers, or mechanisms in an unrelated evaluation. The guide is self-contained;
consult the source when verifying these examples, not as a prerequisite for
every writing task.
