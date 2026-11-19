# Evaluation Writing

Read this when outlining, writing, refining, or reviewing evaluation text. An
evaluation is an argument about supported results, not a data log. This guide
governs presentation and interpretation of existing evidence. It never asks
for new experiments: to plan experiments or the figure set, use
`systems-evaluation-planner`; to render plots, use `systems-paper-plotting`.

## 1. Argument first

Every paragraph establishes one supported claim or one **evidence boundary**
(what the measurement does not establish). Every sentence has one role in it:
purpose, claim, metric orientation, evidence, interpretation, comparison,
condition, cost, net effect, limitation, or handoff. Test each sentence:

```text
What claim does this establish, support, explain, qualify, compare, or limit?
```

If the answer is only "it reports the data", attach the data to its claim or
cut it. A paragraph summarized only as "Figure X shows Y", or several data
sentences with no interpretation, is a data inventory. Write the paragraph's
claim in the outline before its numbers. A metric, figure, configuration, or
baseline is evidence inside a claim, never the claim itself; a sequence of
"metric, number, more numbers" with no interpretation fails. An explicit evidence boundary is a
valid result; never strengthen an unmeasured relationship to make the argument
look complete.

Usual sentence order: claim or purpose → metric orientation (when new) →
evidence with a source clause → interpretation or comparison → cost, condition,
or net effect → next question or scoped implication.

## 2. Section progression: results before diagnosis

Open with the questions the available experiments answer. Common order (omit,
merge, or reorder parts by the paper's claims; do not add parts to fill it):

| Part | Reader's question |
| --- | --- |
| Setup | Is the comparison interpretable and fair? Baselines, resource budgets, workloads, metrics, procedure, repetitions. State it once. |
| Headline results | Does the system improve the target outcome, and how broadly? |
| Attribution | Which mechanisms explain the result, at what cost? (breakdowns, ablations, controlled comparisons) |
| Costs and secondary paths | What did the central decision change elsewhere? |
| Sensitivity, generality, robustness | When does the benefit grow, shrink, or reverse? |
| Application | Does the benefit survive integration? |
| Scalability and limits | What happens as resources or demand grow; what remains a bottleneck? |

The central result normally precedes its attribution, so the reader knows
whether the claim holds before reading why.

## 3. Subsection archetypes

Select the narrowest archetype that matches the subsection's question; if
several fit, show the alternatives for outline alignment.

| Archetype | Reader path |
| --- | --- |
| End-to-end comparison | question → baselines and configuration → overall ranking and magnitude → conditions that change the gap → explanation → scope |
| Design breakdown | components in Design order → per component: improved metric → introduced cost → net effect under the workload |
| Design-centered performance breakdown | see §4 |
| Ablation | the exact change → incremental effect → affected cost → interaction with other components |
| Cost breakdown | total cost → dominant components → added overhead and saved work → net result |
| Sensitivity / parameter sweep | varied parameter → trend → saturation or crossover → competing effects → operating region |
| Scalability | what grows and what stays fixed → aggregate throughput and scaling efficiency → bottleneck |
| Microbenchmark | isolated path → metric purpose → controlled comparison → explanation |
| Robustness / generality | varied workload, failure, or environment → result across conditions → limitation |
| Stability | dips, bursts, or dispersion → frequency or severity → link to measured events |
| Application | integration and workload → application-visible gain → whether engine-level gains survive other costs |

## 4. Breakdowns that explain the proposed system

**Rule (stated once):** when a breakdown exists to explain the proposed
system's measured performance:

1. State the proposed system's headline result first.
2. Say why attribution is needed ("To explain this gap, we break down ...").
3. Walk the proposed design's components in Design order, not by measured
   magnitude or figure order. For each: the metric it improves and the
   direction, the cost it introduces, and the net effect under the evaluated
   workload and configuration, as one connected account.
4. Keep baselines as comparison anchors: at most one sentence each for the
   outcome or causal distinction that explains the focal result. Break a
   baseline down only when the evaluation question is about that baseline.
5. Keep a Design operation or implementation detail only if it explains the
   focal metric, an introduced cost, a measured boundary, or a direct
   comparison. Existing in Design does not make it evaluation material.
6. Use the measured effect's vocabulary (latency, throughput, retrievals,
   traffic), not a mechanism's internal vocabulary, unless the question is
   about that mechanism.

If evidence cannot support one of the three per-component points, mark it
unresolved. When components are isolated one at a time, open with what the
component measurements establish and the isolation condition, then give each
component's benefit, cost, scoped interpretation, and boundary; do not claim
an end-to-end effect the experiment did not measure.

## 5. Keep four orders apart

Record `source_order` (the old draft, a locator only), `design_order` (from
the Design section), `evidence_order` (the order figures and tables exist),
and `narrative_order` (the order that answers the questions with the least
backtracking). A breakdown follows `design_order`; other archetypes take their
order from the questions and dependencies. A figure supports a claim without
setting a paragraph boundary. If the target order equals the source order,
record the dependency reason; "the draft already does this" is not one. If
`design_order` is unknown, mark `Needs context`.

## 6. The result-group contract

Before prose, fill one row per result group in the outline:

```text
question | claim tested | metric and purpose | baseline | workload/configuration
evidence source | observed result | supported explanation | cost or limitation
net effect and scope | next question
```

Keep claim (what the experiment establishes), evidence (what the figure
reports), explanation (what mechanism it supports), and condition (when it
holds) distinct. Do not turn an intended benefit into an observed result or a
correlation into a cause.

## 7. Writing result paragraphs

| Move | Contribution |
| --- | --- |
| Orient | workload, varied parameter, and figure; only the setup needed here |
| Finding | which metric changes, against which baseline, under which conditions |
| Quantify | representative values or a range; a complementary metric when it changes the reading |
| Explain | the bottleneck and the mechanism that changes it, with supporting evidence |
| Qualify | a real exception, crossover, regression, or diminishing return |
| Interpret | the scoped design implication, if not already clear |

The finding and its evidence are essential; the other moves may span
paragraphs or be omitted. When a metric is new, the paragraph's first sentence
says what it measures or why it is reported, before any number. Introduce each
figure or table observation with a source clause ("Figure 6 shows ..."); a
parenthetical reference alone is not an introduction.

Explain comparisons as **workload property → bottleneck → mechanism →
measured consequence**:

- Group baselines that share a limitation; avoid baseline-by-baseline prose.
- Explain changes in the gap, not only in absolute performance.
- Lower throughput alone does not mean a baseline malfunctions.
- Match causal wording to evidence: "the breakdown shows" (measured), "is
  consistent with" (indirect), "we hypothesize" (unverified).
- For incremental ablations, write "adding B on top of A improves ...", not
  B's independent contribution, unless an experiment isolates it.

Losses, narrowing advantages, opposing effects on two metrics, saturation,
non-monotonic trends, and rank changes define operating conditions. State the
condition and its consequence; explain it when evidence permits, otherwise
mark the cause unresolved. Never hide a regression behind an aggregate gain or
invent an exception to complete a pattern.

## 8. Quantitative reporting

- Attach every number to its system, metric, unit, comparator or denominator,
  and conditions, in the sentence or explicit adjacent context. Say what a
  range spans (datasets, systems, configurations).
- Distinguish ratios, relative percentage changes, and percentage points.
  Prefer "2.0× the throughput of B" over "2× improvement"; compute a reduction
  as (baseline − system) / baseline.
- Give absolute values when a ratio hides the practical effect, and say who
  pays a cost.
- Pair an "up to" figure with typical behavior or the full range.
- Separate equal-resource comparisons from runs that add memory, cores, or
  nodes, and references with different guarantees (for example a
  non-durable upper bound).
- Distinguish less traffic on one link from less total traffic, and overlapped
  work from eliminated work.
- Report repetitions and aggregation in setup; do not infer significance from
  means.
- Never infer exact values or causes from a vague plot. Prose, figures,
  captions, units, and computed percentages must agree.

## 9. Checks

- [ ] Each subsection's question and archetype are visible; the first-sentence
      summary recovers question → result → explanation or scope.
- [ ] No paragraph is a data inventory; each number serves a claim.
- [ ] Breakdowns follow §4; narrative order is deliberate.
- [ ] Every claim has nearby evidence and scope; interpretations do not exceed
      the evidence.
- [ ] No sentence requests or implies a new experiment.
