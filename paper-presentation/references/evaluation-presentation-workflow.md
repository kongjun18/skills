# Evaluation Presentation and Rebuild Workflow

Load this profile when the requested scope contains Evaluation prose, an
evaluation subsection, or a source-only rewrite of evaluation material. It
adds an evaluation-specific structure pass to the shared presentation
workflow. It does not judge whether the experiments are scientifically
adequate and does not request new experiments.

For pattern selection, also read [Evaluation Patterns from Systems Papers](evaluation-reference-patterns.md).
Use the O3-LSM and Remzi-paper observations there as transferable reasoning
patterns; do not copy their visible section order or terminology.

Evaluation prose is an argument about supported results. Treat the old
paragraph order, figure order, and one-paragraph-per-experiment grouping as
source material rather than as the target presentation. Preserve the supplied
facts, measurements, conditions, and claim strength while rebuilding the
reader path from evaluation questions and evidence.

## 0. Evidence-bounded argument-first evaluation gate

Evaluation is organized around supported claims, not narrated as a data log.
This is a presentation rule, not a request to strengthen the scientific claim
or to add experiments. Treat every number, figure, table, configuration, and
baseline as evidence that serves a reader-facing argument. Before drafting,
write the claim spine:

```text
evaluation question
→ subsection claim
→ supporting claim
→ evidence
→ supported interpretation
→ cost, condition, or limitation
→ scoped implication, evidence boundary, or next question
```

Every paragraph has one primary supported claim or evidence boundary. Every
sentence has one role in that claim, such as purpose, claim, evidence,
interpretation, comparison, condition, cost, net effect, limitation, or
handoff. A sentence that only describes a figure, repeats a number, lists a
configuration, or names a baseline is not accepted as a paragraph's argument
unless it makes the supported claim or its scope clearer. It can remain as an
evidence sentence when it has an explicit source and a trace to the claim.

Use this test for every sentence and paragraph:

```text
What claim does this establish, support, explain, qualify, compare, or limit?
Which next claim becomes possible because this sentence is present?
```

If the answer is only “it reports the data,” attach the data to the supported
claim or mark the sentence as an evidence-boundary sentence. If a paragraph
cannot be summarized as a supported claim, its evidence, or its evidence
boundary, rebuild its paragraph responsibility before prose. Do not turn an
unmeasured relationship into a stronger claim merely to make the argument
look complete.

The normal sentence order is:

```text
supported claim or evaluation purpose
→ metric orientation when needed
→ explicit evidence source
→ interpretation or comparison
→ cost/condition/net effect
→ next claim, evidence boundary, or scoped implication
```

This order does not require a fixed number of sentences. It keeps evidence
subordinate to the supported argument without asking the prose to exceed the
measurement. “Figure X shows ...” is an evidence sentence; it must be tied to
the claim or boundary it supports, rather than becoming the paragraph's entire
point. A metric definition is useful only when it orients the claim being
tested. If the experiment does not isolate a net effect, say so as the
evaluation boundary instead of proposing a new experiment inside the paper.

## 1. Recover the Evaluation-level progression

When the complete Evaluation section is in scope, first recover its supported
macro progression. Use the reference patterns to generate candidates, then
select the one supported by the target paper:

```text
evaluation questions → shared experimental setup
→ headline end-to-end results → mechanism or design breakdown
→ application/generalization or robustness → scalability and limits
```

This is a common systems-paper progression, not a requirement to include every
part. A paper may omit an unsupported part, combine two parts, or place a
specialized analysis earlier when the question requires it. The central result
normally appears before detailed attribution, so the reader knows whether the
system meets the paper's main claim before reading why. Setup belongs before
the result it conditions, but repeated setup does not belong in every result
paragraph. If only one subsection is in scope, use the available surrounding
outline to identify its place in this progression and keep its local question
independent.

## 2. Select the subsection archetype

Identify the question the subsection answers and select the narrowest supported
archetype before drafting or reorganizing:

| Archetype | Reader path |
| --- | --- |
| End-to-end comparison | question → baseline/configuration → result → explanation → scope |
| Design-centered performance breakdown | headline result for the proposed design → purpose of the breakdown → Design components in Design order → benefit metric → introduced cost → net effect under the evaluated workload/configuration → compact baseline contrast |
| Other design breakdown | Design components in Design order → benefit metric → introduced cost → net effect under the evaluated workload/configuration |
| Ablation | isolated claim → removed component or policy → measured change → attribution and interaction with the full system |
| Sensitivity | varied parameter or resource → expected effect → trend across the range → operating region or boundary |
| Scalability | varied system size, load, or concurrency → scaling metric and baseline → trend → bottleneck or limit |
| Microbenchmark | isolated mechanism or path → metric purpose → controlled comparison → supported explanation |
| Robustness or generality | varied workload, failure, or environment → result across conditions → scope and limitation |

These are candidate patterns, not a fixed Evaluation template. Combine them
only when the evidence and the reader's question require the combination. If a
subsection has several plausible patterns, return the alternatives and their
tradeoffs for outline alignment rather than silently choosing one from the old
text.

## 2a. Center a performance breakdown on the proposed design

Use `Design-centered performance breakdown` when a breakdown exists to explain
the proposed system's measured performance. It is an explanation of a
headline result, not another inventory of numbers or a tour of baseline
implementations. The default reader path is:

```text
headline result for the proposed design
→ why the breakdown is needed
→ proposed design component in Design order
→ measured effect on the focal metric
→ introduced cost or overhead
→ net effect under the workload and configuration
→ concise baseline contrast when it explains that effect
```

Report the focal result before attributing it. If the result and breakdown are
in one subsection, state the purpose explicitly, for example: “To explain this
performance difference, we break down the costs introduced by the proposed
design.” Do not begin by reporting a baseline breakdown or by listing figures;
that reverses the reader's dependency. A later breakdown must answer why the
headline result has the observed shape.

Make the proposed design the narrative subject. A baseline is normally a
comparison anchor: give each baseline at most the one sentence needed to state
the relevant outcome or causal distinction. Do not spend the subsection on a
baseline's internal implementation, and do not discuss differences that do not
explain the focal result. Break down a baseline in detail only when the
evaluation question explicitly compares that baseline mechanism.

Include an operation, intermediate state, or implementation detail only when
it explains the reported metric, an introduced cost, a measured boundary, or a
supported causal distinction. An operation's purpose from the Design section
does not by itself make it evaluation material. Likewise, use terms such as
“access path” only when the evaluation question is actually about access-path
behavior; otherwise name the measured effect directly (for example,
retrieval overhead, latency, throughput, or storage traffic).

Use the following relevance test before retaining a sentence:

```text
Does it answer the evaluation question, orient the focal metric, explain the
proposed design's measured effect, identify its cost, or bound its scope?
```

If the answer is no, relocate the material to the appropriate Design or
Implementation contract, or drop it. This test prevents a performance
breakdown from becoming a data-and-analysis pile.

### Component-level breakdown with bounded attribution

When the evaluation isolates design components one at a time, use this
presentation pattern:

```text
P0: overall component-level measured tradeoff and isolation condition
P1: component A benefit → component A cost → scoped interpretation → boundary
P2: component B benefit → component B cost → scoped interpretation → boundary
P3: component C benefit → component C cost → scoped interpretation → boundary
```

The P0 opening states what the component measurements establish and names the
isolation protocol only as the condition for interpreting them. It does not
claim an end-to-end improvement unless the experiment measures that outcome.
Each component opening states its measured benefit and cost before describing
the implementation. The final sentence may state the component-level tradeoff
and the evidence boundary, such as the fact that the ablation does not isolate
request-level latency, throughput, or hit-rate effects.

For a filtering component, describe the stages only to establish what is
removed, what `Actual Retrieved` means, and where early stopping occurs. Then
state the filtering cost and whether the available comparison isolates its
net effect. For a pruning component, state routing-state reduction, the
measured increase in segment retrievals, the resulting component-level
tradeoff, and the boundary on request-level conclusions. These are reusable
argument roles; use the paper's actual component names and evidence.

Do not convert an unisolated comparison into a missing-claim problem. If the
data cannot establish the net effect, write the supported component result and
its limitation. Do not request, design, or imply a new experiment in an
Evaluation presentation pass. Experiment design belongs to
`systems-evaluation-planner` and is activated only by an explicit request for
evaluation planning.

## 3. Separate the four orders

Record these orders separately in the evaluation structure artifact:

- `source_order`: the order in the supplied draft, used only as a locator;
- `design_order`: the order of components established by the Design section;
- `evidence_order`: the order in which figures, tables, or measurements are
  available or introduced; and
- `narrative_order`: the order that lets a reader answer the subsection's
  questions with the least backtracking.

For a design breakdown, keep the component sequence in `design_order` unless
the paper explicitly establishes another order. This does not require
`narrative_order` to copy `source_order` or `evidence_order`. For other
archetypes, choose the order from the evaluation questions and dependency
graph. A figure can support a claim without determining a paragraph boundary.

If `design_order` is unavailable or conflicts with the supplied outline, mark
the decision as `Needs context` rather than inferring it from the measured
magnitude or figure order.

## 4. Audit source material without inheriting its structure

For `rebuild-from-material`, freeze the source version and classify each source
unit as one or more of:

- evaluation question or motivation for the measurement;
- metric and its purpose;
- workload, baseline, configuration, or scope condition;
- measured result or evidence source;
- supported interpretation or mechanism;
- cost, limitation, or boundary; and
- unsupported framing, repetition, or source presentation.

Give every unit a source locator, evidence mapping, scope, terminology status,
and disposition (`retain`, `relocate`, `merge`, `split`, `defer`, `drop`, or
`needs context`). A source paragraph is not a required target paragraph. A
source unit can contribute to several contracts when the facts support that
use, and several units can be merged when they answer one reader question.

Do not give the writer the old subsection as the primary drafting template.
Provide the material ledger and evidence-linked excerpts first; retain the raw
source only as a read-only lookup by source-unit ID. If the target structure
is identical to the source structure, record why the dependency graph requires
that choice. “The source already uses this order” is not a reason.

## 5. Build the evaluation claim–evidence matrix

Before prose rendering, record one row for each reader-facing claim or result:

```text
claim_id
evaluation_question
archetype_role
claim_kind: observed_result | supported_interpretation | evidence_boundary |
             purpose | limitation
claim_or_result
paragraph_claim
sentence_roles
metric_and_purpose
baseline/workload/configuration
evidence_source
supported_interpretation
cost_or_limitation
scope_and_claim_strength
incoming_endpoint
provided_claims
outgoing_handoff
source_unit_ids
```

Keep the three layers distinct:

1. **Claim:** what the experiment establishes.
2. **Evidence:** what the figure, table, trace, or measurement reports.
3. **Interpretation:** what the result supports about the mechanism, design
   choice, or workload.

Also record the role of every sentence that renders the row. Do not let
`metric_and_purpose`, `evidence_source`, or `observed_result` become a list of
data sentences without a `claim_or_result` and `supported_interpretation`.
The matrix is incomplete when it contains measurements but no answer to the
evaluation question. An `evidence_boundary` row is a valid answer when the
available measurement does not support a stronger attribution. It records what
the experiment does not establish; it does not create a request for another
experiment.

Do not turn an intended benefit into an observed result, or an observed
correlation into a causal explanation. If a cost or interpretation is not
supported by the supplied evidence, mark it unresolved instead of filling the
row with a generic explanation.

For a design breakdown, each component row also records:

```text
design_component
improved_metric_and_direction
introduced_cost
net_effect_under_workload_and_configuration
```

For a design-centered performance breakdown, also record:

```text
focal_design_or_subject
headline_result_before_breakdown
breakdown_purpose
baseline_role_and_compression
relevant_operation_or_detail
```

`baseline_role_and_compression` should normally be `comparison anchor` and
`one-sentence contrast`, unless the question explicitly makes a baseline a
co-equal subject. `relevant_operation_or_detail` is a filter, not a request to
describe every operation used by the design.

The net effect explains the measured result at the supported scope. It does
not claim that the component is universally beneficial.

## 6. Choose paragraph responsibilities before writing

The first paragraph normally states the subsection claim or evaluation question
and why the reported metric or comparison can answer it. Introduce a metric's
purpose before its values when the metric is new, and state the shared setup
only once unless a later paragraph changes it. Lead evidence with an explicit
source clause such as “Figure X shows ...” or “Table Y reports ...”, then
state what claim the evidence supports. Do not let the metric definition or
shared setup become the paragraph's takeaway.

Use the selected archetype to assign paragraph roles. For example, a design
breakdown normally has:

```text
evaluation question and shared setup
→ component A: benefit, cost, net effect
→ component B: benefit, cost, net effect
→ ... in Design order
→ synthesis or scope of the breakdown
```

For a design-centered performance breakdown, use this more specific sequence:

```text
metric purpose and headline result
→ explicit reason to break down the result
→ focal design component A: measured effect, cost, net effect
→ focal design component B: measured effect, cost, net effect
→ concise baseline contrasts where they clarify A or B
→ synthesis and scope
```

Keep the first result paragraph and the explanatory breakdown distinct in
purpose even when they share a subsection. Do not introduce a baseline's
implementation before the proposed system's result has been established.

For each paragraph, write its claim above the paragraph contract before writing
any prose. During review, delete or relocate a paragraph that cannot answer
“What does this paragraph establish?” with one supported sentence. A paragraph
that reports several figures but has no interpretation is a data inventory,
not an Evaluation argument.

The component paragraph should name the reader-visible metric or measured
effect before describing an implementation detail. Do not create a separate bridge
paragraph merely to hand off to the next component; the next opening should
carry the component or result it depends on. Do not repeat the setup, metric
definition, or headline result in every component paragraph.

## 7. Independent review gate

The reviewer, before any writer receives the source prose, returns:

- the selected archetype and evaluation question;
- the four orders and the recommended `narrative_order`;
- the claim–evidence matrix;
- paragraph responsibilities, openings, incoming/outgoing handoffs, and
  figure/table bindings;
- source-unit dispositions and any material that must be deferred or dropped;
- required merge, split, reorder, relocate, delete, or rewrite moves; and
- unresolved evidence, scope, or author decisions.

For a design-centered performance breakdown, the review also freezes the focal
design, headline result, reason the breakdown is needed, baseline role and
compression, and the relevance decision for every operation or implementation
detail. A review fails the structure gate when it leads with baseline
implementation or data, omits the reason for the breakdown, or gives the
baseline more narrative weight than the proposed design without an evaluation
question that requires it.

The review also fails the argument gate when a paragraph is organized as
figure, data, or configuration descriptions without a paragraph claim, or when
a sentence reports a value without identifying the claim, comparison,
condition, or interpretation that the value supports. Reorder the evidence
around the claim before asking for wording changes.

Classify inherited source organization as a presentation violation when it
blocks the selected reader path, even when every source paragraph contains a
valid measurement. If the reviewer recommends preserving the old organization,
the review records the dependency or scope reason. A fluent source-like draft
does not pass this gate merely because its local results are correct.

The first-sentence-only test should let a reader recover the evaluation
question and progression. The sequence should not read like repeated figure
introductions or a list of unrelated numbers.

## 8. Writer handoff and refinement

The writer receives the frozen evaluation structure, claim–evidence matrix,
material ledger, terminology ledger, and acceptance conditions. It writes from
those contracts rather than paraphrasing source paragraphs. Structural moves
are made before sentence polishing.

For each paragraph, pass its paragraph claim and ordered sentence roles before
passing its evidence values. For each sentence, require a trace to a claim,
interpretation, condition, comparison, or handoff. A sentence whose only trace
is “reports data” fails the handoff and is rewritten around the claim it
supports. The writer may report several values when they establish one
comparison, but it should not enumerate values whose interpretation is absent
or already established.

Write these paragraphs sequentially. Finish and independently check the
current paragraph before giving its endpoint to the next paragraph. This is
especially important for a component breakdown, where the next component must
inherit the prior component's measured boundary without reopening its claim.

Run the normal three prose rounds after this gate:

1. render claims, evidence, conditions, and handoffs;
2. repair result-to-interpretation transitions, paragraph organization,
   redundancy, and sentence load; and
3. polish concise English without adding claims, evidence, mechanisms, or
   terminology variants.

If a later round discovers that the narrative still follows source order or
that a result lacks its evaluation question, return to this workflow before
continuing prose refinement.

## 9. Independent verification

Verify the final subsection against the frozen evaluation structure, not only
against the source text. Check that:

- the selected question and archetype remain visible;
- `narrative_order` is intentional and does not silently become source or
  figure order;
- every claim has nearby evidence and scope;
- every metric is oriented before its result when needed;
- every figure/table observation has an explicit source clause;
- a breakdown follows Design order and states benefit, cost, and net effect for
  each component;
- a design-centered performance breakdown reports the proposed design's
  headline result before its explanation, states why the breakdown follows,
  keeps baselines as concise comparison anchors, and retains only details that
  explain the focal metric, cost, or scope;
- interpretations do not exceed the evidence; and
- no paragraph is a data inventory: each paragraph has one supported claim,
  and each result sentence advances that claim through evidence,
  interpretation, comparison, condition, cost, or implication; and
- the first-sentence-only summary recovers the evaluation progression.

This verification is about presentation and faithful interpretation. It does
not establish that the experiments are sufficient or that the scientific
claims are correct.
