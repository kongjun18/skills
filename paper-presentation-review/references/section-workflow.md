# Section Responsibility Workflow

Use this workflow when reviewing or revising multiple sections, especially the
relationship between Motivation and Design. The sections form a dependency
chain, but each section must answer its own reader question at the level of
detail appropriate to its role.

Use the [section presentation playbook](../../paper-presentation/references/section-presentation-playbook.md)
to select a section-specific argument pattern. When Motivation may have been
written backward from Design, run the [Motivation Recovery Workflow](../../paper-presentation/references/motivation-recovery-workflow.md)
before this section traceability review.

## Section contracts

### Background

Background establishes concepts, terminology, operating assumptions, and
existing-system behavior needed by later sections. It can describe a baseline
mechanism when readers need it to understand an observation. It does not need
to preview the proposed implementation or argue that the proposed component is
necessary.

### Motivation

Motivation answers: **What problem or opportunity follows from the workload,
existing behavior, constraints, and observations?** Its normal chain is:

`high-level setting → observation → limitation or pressure → opportunity or requirement`.

Motivation is design-blind. Before reading Design, a reader should be able to
state the problem, why it matters, what capability is missing, and what
requirements a solution would need to satisfy. Motivation may use domain
objects and established operations, such as requests, records, objects, storage tiers, or matching operations,
when those objects are needed to describe the observation. It should not
introduce or reverse-engineer the proposed component, data structure, encoding,
algorithm step, routing policy, or implementation-specific mechanism.

Do not write Motivation backward from Design. Phrases such as "we add a coordinator," "we divide records into three
levels," or "we use a packed store" answer how the paper will solve the
problem. Replace them with a requirement that follows independently from the
observation, such as the need to locate reusable objects across distributed
resources with bounded coordination and retrieval cost. The exact mechanism belongs in Design.

The test is counterfactual: hide Design and ask whether the Motivation still
supports the same problem and opportunity. If deleting a design-specific noun
or algorithm step breaks the argument, the text is likely reverse-engineered
from Design. Move the mechanism to Design or rewrite it as a high-level
requirement. Do not use later design details, evaluation wins, or the proposed
architecture as evidence for the Motivation's problem statement.

### Design

Design answers: **How does the proposed system satisfy the requirements that
Motivation established?** Each major component or mechanism should map to one
or more prior requirements and state its supported reason. Design may introduce
new implementation concepts, but it should make their contract, operation, and
tradeoff clear. A component without a Motivation mapping needs justification or
is likely misplaced. A Motivation requirement without a Design mapping is an
open requirement, an explicit scope boundary, or an author decision.

### Evaluation

Evaluation answers: **What question is being tested, under which workload and
configuration, and what does the evidence show?** State the metric's purpose
before results, introduce figures and tables explicitly, and interpret benefits,
costs, and net effects under their measured conditions. Breakdowns follow the
Design order. Evaluation can explain an observed result using Design mechanisms,
but it must distinguish measured effects from intended reasons.

### Introduction and Related Work

The Introduction can preview the problem, insight, design at a high level, and
results to orient the reader. That preview does not authorize putting
implementation detail into Motivation. Related Work explains relationships and
distinctions among supplied prior systems. It should not become a second
Motivation or introduce unsupported claims about the proposed design.

## Design-blind review and traceability review

For a multi-section review, use two passes:

1. **Sealed Motivation pass.** Read Background and Motivation without using
   Design details. Produce the Motivation Recovery contract, including the
   setting, observations, pressure, opportunity, design-independent insight
   candidates, requirements, and unit-level leakage map. Mark any phrase that
   depends on later Design knowledge or belongs to a naive-solution chain.
2. **Traceability pass.** Read Design and map each major choice back to the
   Motivation contract. Check that the mapping is explanatory rather than
   circular. Do not revise Motivation merely to make an existing Design look
   necessary. If the Design is not motivated, report the missing requirement or
   author decision.

Apply the same two-pass rule after revision. A final presentation passes only
when Motivation remains understandable without Design and Design clearly maps
back to Motivation.
