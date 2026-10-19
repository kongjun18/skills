# Section Presentation Playbook

Use this playbook after the paper-level story is recovered and before drafting
or restructuring a section. It provides reusable section contracts and common
argument patterns. It is a menu of supported patterns, not a fixed paper
template. Select a pattern from the section's question, dependency graph, and
available evidence, then record that choice in the outline.

The general rule is that a section answers its own question at the right
abstraction level. A section may use a neighboring section's result as an
incoming handoff, but it should not make the reader reconstruct its purpose
from a later section.

## Section contracts and common patterns

### Abstract

Answer what problem the paper addresses, the central insight or approach at a
high level, and the main supported result or implication. Use only enough
method detail to identify the contribution. Avoid new terminology, evidence
qualification, or a miniature related-work discussion.

Common order:

```text
problem → opportunity or insight → approach → main result → implication
```

### Introduction

Orient the reader to the problem, why it matters, the high-level opportunity,
the paper's approach, and the evidence that supports the claim. The
Introduction may preview Design and Evaluation, but it should not replace
their explanations or import low-level mechanisms into Motivation.

Common order:

```text
setting → decision-relevant problem → evidence or pressure
→ high-level insight → approach preview → contributions or questions
```

### Background

Provide concepts, operating assumptions, existing behavior, and baseline
mechanisms that later reasoning needs. Introduce only context that enables a
later observation, design contract, or evaluation interpretation. Background
can explain how an existing system works, but it should not present the
proposed mechanism as if it were established context.

Common order:

```text
concept or interface → relevant operation → existing behavior or constraint
→ implication needed by the next section
```

### Motivation

Derive a high-level problem, opportunity, insight, or requirement from
workload properties, existing behavior, constraints, failures, or measured
observations. Keep the argument valid when the proposed implementation is
replaced. A baseline or naive approach may appear briefly when it is evidence
for the pressure, but the core chain should remain design-independent.

Common order:

```text
setting → observation → limitation or pressure
→ opportunity or missing capability → insight or requirements
```

If the reasoning instead follows `requirement → obvious approach → failure →
final mechanism`, classify it as a Design pattern and move it there. See the
[Motivation Recovery Workflow](motivation-recovery-workflow.md).

Keep Motivation at the capability and requirement level. State what the system
needs to locate, associate, retain, or improve before naming a proposed
representation, encoding, identifier, data structure, or component. If a
concrete representation is itself an existing-system observation, identify it
as such and preserve the scope that makes it relevant. A locally explained
implementation term is still a leak when the reader needs Design to understand
why that term was chosen.

### Design

For Design discussion and outline synthesis, consult the [Design Presentation
Patterns](design-presentation-workflow.md). It helps the author and agent
separate the requirement or opportunity from the Design challenge, choose the
right unit of explanation, and select a reader-facing dependency order. It is
a menu of patterns, not a fixed Design workflow or a required
responsibility-to-layout-to-update sequence.

Explain how the proposed choices satisfy the requirements and what each choice
costs or enables. Introduce a component through its contract and purpose
before its implementation details. When a naive solution is useful, make the
reasoning explicit rather than hiding it inside Motivation:

```text
requirement → naive solution → limitation or new tension
→ design principle → proposed mechanism → contract and tradeoff
```

Alternative Design patterns include component-by-component explanation,
workflow or dataflow explanation, invariant-first explanation, and
failure-case-to-mechanism explanation. Select the pattern that best matches
the dependency graph instead of forcing every design into one sequence.

In the semantic object graph, every mechanism, operation, layout, or update
must have a supported requirement, challenge, or purpose edge. A Design unit
that only describes what the system does, without recording what requirement
the choice serves, is incomplete even when the mechanism is technically
correct.

When a Motivation opportunity creates a Design challenge, make that challenge
the incoming edge of the selected first Design unit. The outline may then use
a component contract, workflow, invariant-first, failure-to-mechanism,
interface-first, or another supported pattern. State a component's role before
its lower-level representation only when the selected pattern requires that
separation. Give aggregation, representation, layout, or update behavior a
separate paragraph or argument node only when it answers an independent reader
question or establishes an invariant or cost. Do not put the whole
architecture and every mechanism into the first Design paragraph.

When a Design subsection presents a logical interface and multiple structures,
separate the interface contract from its implementations. A useful order is
responsibility and stored association, selected operations with their inputs
and results, implementation families, and per-family representation or
procedure. Say that the subsection focuses on selected operations unless the
source establishes an exhaustive interface. Do not move directly from an
operation name to a data structure before stating what the operation consumes
and returns.

### Implementation

Connect implementation details to Design contracts. Explain the data layout,
control flow, state transitions, exceptions, and engineering choices that a
reader needs to reproduce or assess the system. Do not reopen the Motivation
or restate the entire Design. Keep correctness invariants and performance
costs near the implementation they constrain.

Common order:

```text
design contract → implementation choice → operation or state transition
→ invariant or exception → resource and performance consequence
```

### Evaluation

Evaluation answers a question with evidence under a stated workload and
configuration. It is not a list of numbers. Start each metric-specific unit
with the metric's purpose or meaning, then state the setup or scope before
reporting the result. Introduce figures and tables with an explicit source
clause.

For a complete Evaluation section or a source-only rewrite, also load the
[Evaluation Presentation and Rebuild Workflow](evaluation-presentation-workflow.md).
It separates the Evaluation-level progression from the local subsection
pattern and distinguishes Design, evidence, source, and narrative order.

The default result pattern is:

```text
evaluation question → metric purpose → workload/configuration
→ result → supported explanation → cost, limitation, or scope
```

Select a more specific pattern when appropriate:

- **End-to-end comparison:** question → baseline and configuration → result
  across workloads → explanation of the main difference → scope.
- **Design-centered performance breakdown:** proposed-system headline result
  → why attribution is needed → design components in Design order →
  per-component improved metric → introduced cost → net effect under the
  evaluated workload/configuration → concise baseline contrast.
- **Other design breakdown:** design components in Design order → per-component
  improved metric → introduced cost → net effect under the evaluated
  workload/configuration.
- **Ablation:** component or policy removed → isolated question → measured
  change → interpretation and interaction with the full system.
- **Sensitivity:** parameter or resource varied → expected effect → result
  across the range → operating region or boundary.
- **Scalability:** system size, load, or concurrency varied → scaling metric
  and baseline → trend → bottleneck or limit.
- **Microbenchmark:** one mechanism or path isolated → metric purpose →
  controlled comparison → explanation of the measured difference.
- **Robustness or generality:** workload, failure, or environment varied →
  scope of the claim → result across conditions → limitation.

These patterns can be combined when the evidence supports the combination.
Do not add a breakdown, ablation, or causal explanation that the supplied
measurements cannot establish.

The semantic object graph must preserve the evaluation question, metric
purpose, workload/configuration, result, interpretation, and any cost or
condition as separate typed objects when they carry different relations. A
metric or result without a question/purpose edge is not ready for prose
rendering.

### Related Work

Organize prior work by the distinction relevant to the paper's question, not
by an unstructured bibliography. State the shared problem or interface, group
systems by the meaningful design dimension, and explain the supplied
difference. Keep unsupported novelty or superiority claims out of the
section.

Common order:

```text
shared problem or interface → comparison dimension → prior-work groups
→ relationship and remaining distinction
```

### Discussion or Limitations

State what the evidence supports, where the design applies, what tradeoffs it
accepts, and which conditions remain open. Connect each limitation to the
claim or mechanism it bounds. Do not introduce a new central contribution.

### Conclusion

Return to the problem, central insight, and supported result or implication.
Use the conclusion to close the story, not to introduce new evidence,
mechanisms, or unprepared claims.

## Pattern selection and verification

For each section, record:

- the local reader question;
- the selected pattern and why its dependency structure fits;
- the incoming and outgoing handoffs;
- the abstraction level and concepts allowed at this point;
- the evidence and scope conditions; and
- the common failure mode being checked.

Review the section against its selected pattern, then run the general
concept-flow, terminology, transition, evidence, and first-sentence checks.
If a section follows a different but supported pattern, record that choice
instead of treating deviation from the defaults as an error.
