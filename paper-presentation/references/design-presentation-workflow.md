# Design Presentation Patterns

Use this reference while discussing the story or building the structured
outline for a Design section, and later when a reviewer or reviser checks the
rendered prose. It is a pattern catalog, not a separate Design workflow or
pipeline stage. Design follows the same interaction protocol as every other
section:

```text
story discussion → author story alignment → structured outline synthesis
→ author outline alignment → independent review → revision → verification
```

The patterns below help the author and agent choose a reader-facing order for
the outline. They do not prescribe one architecture, one component hierarchy,
or one storage/layout sequence. The selected pattern and its rationale belong
in the aligned outline; the reviewer and reviser must follow that outline
rather than choose a new pattern while writing.

## 1. Record Design relations before choosing prose order

During story and outline discussion, record the supported relations that the
Design must expose. This is a dependency inventory, not a mandatory prose
sequence:

```text
requirement or opportunity; design challenge or constraint; design decision;
component responsibility or contract; mechanism or representation;
operation/state transition; consequence, tradeoff, or downstream dependency
```

The outline may use only a subset of these relations, and may order them
differently when the paper's dependency graph supports it. Do not turn this
inventory into a fixed `requirement → component → layout → update` template.

The **design challenge** is the implementation-independent constraint that the
design must satisfy after Motivation has established the opportunity. It is not
a repetition of Motivation and it is not the name of the final component. For
example, an opportunity to amortize storage overhead can create a challenge to
organize units so they share storage work while preserving the access and
update properties the system needs. The proposed component is introduced only
after this challenge is clear.

Do not infer a challenge, mechanism, or reason that the supplied paper does
not support. Mark a missing edge `Needs context` rather than filling it with a
generic claim such as “for performance.”

## 2. Choose a Design presentation pattern in the outline

Select the smallest pattern that makes the supported dependency graph easy to
follow. Common choices include:

| Pattern | Reader-facing order | Use when |
| --- | --- | --- |
| decision–consequence–mechanism | design decision → new tension or invariant → mechanism → consequence | a choice creates the problem that the next mechanism resolves |
| component contract | component responsibility → contract → realization → boundary or cost | the reader first needs to know what a component promises |
| workflow or dataflow | input/state → operation stages → ownership or invariant → result and cost | the design is best understood as a path through states or data |
| invariant first | required invariant → representation or algorithm → operations that preserve it → limits | correctness or safety is the organizing idea |
| interface then implementations | logical responsibility → selected operations → implementation families → per-family realization | several implementations serve one logical interface |
| lifecycle or state transition | initial state → event/transition → observable state → recovery or update behavior | behavior over time is the main dependency |
| failure to mechanism | failure or constraint → required property → mechanism → residual cost | a concrete failure explains why the mechanism exists |
| architecture overview | system responsibility → component roles and relations → critical data/control flow → details | the reader first needs the system map |

These are alternatives, not steps to execute in sequence. If two patterns are
plausible, expose the alternatives during story/outline discussion and record
the author's choice. Do not select a pattern merely because the source draft
uses it or because a storage paper often uses it.

## 3. Decide the design-unit granularity

Make a component an independent Design unit when it has a distinct:

- problem or design challenge;
- responsibility or contract;
- design decision that is not merely a parameter of another component;
- downstream mechanism or operation that depends on it; or
- evaluation claim or cost that the paper must later attribute to it.

Keep a detail inside its parent component when it only implements that
component's contract and has no independent reader question. A storage unit,
layout, aggregation policy, or update procedure may therefore be a component,
a paragraph, or an inline detail depending on the dependency graph. Do not
promote every data structure or field into a named design unit.

Record the choice in the outline. If two granularities are both supported,
present the alternatives for author alignment instead of silently choosing the
one that resembles the source draft.

## 4. Use an overview only when the outline needs one

When the selected outline begins with an overall Design overview, it commonly
answers how the proposed system satisfies the requirements and how its major
components fit together:

```text
requirement or design challenge → overall design principle → major components
and their relationships → locations of the detailed contracts
```

This is a useful overview pattern, not a required prelude. A workflow,
invariant-first, failure-to-mechanism, or interface-first outline may start
elsewhere if that is the supported reader dependency.

The overview should not explain a physical layout, update algorithm, or every
aggregation step. Name a representation in the overview only when it is the
central design decision and the reader needs that name to understand the
component map. Otherwise defer it to the component subsection.

The first sentence should expose the overall design decision or responsibility
early. The following sentences should explain how the component introduced
there satisfies the challenge and what later Design subsections will establish.
Avoid a component list with no relationship, a Motivation restatement, or an
Evaluation preview.

## 5. Apply the selected local pattern

When the selected pattern introduces a component through its contract, the
first paragraph should make four things recoverable:

```text
incoming requirement or challenge
→ component responsibility
→ how the overall design uses the component
→ contract or property that the following details realize
```

Prefer a purpose-bearing active sentence such as “The component organizes ...
so that ...” over “We introduce ...” or a bare noun phrase. State what the
component consumes, produces, stores, or exposes only to the extent needed for
the next mechanism. Do not start with a field layout or identifier before the
reader knows why the component exists.

For the storage/layout-oriented component pattern, use the following dependency
only when the outline and evidence support it:

```text
logical responsibility
→ aggregation or placement policy
→ physical representation or layout
→ read/write/update behavior
→ invariant, cost, or boundary
```

Other selected patterns use their own order from the table above. Each edge
must answer a reader question created by the preceding edge. If a layout does
not need its own paragraph, keep it in the sentence that explains the contract
it realizes. If updates introduce a new invariant or cost, give them a
separate paragraph or node rather than hiding them in a long sentence.

## 6. Keep logical and physical levels separate when both are in scope

Explain what the component means before how it is encoded. A logical store,
index, or aggregation unit is not interchangeable with its layout, identifier,
or backing file. Introduce the representation only after the component's
responsibility and stored association are clear, then state the supported reason
for the representation in the same argument unit.

Use direct transitions:

```text
The component groups ... .
This grouping requires ... .
The layout stores ... so that ... .
When ... changes, the update path ... while preserving ... .
```

Do not use a representation name as a substitute for the logical design idea,
and do not describe an update procedure before stating what state it updates
and why that state matters.

## 7. Build the Design argument-node outline

Before prose rendering, create argument nodes for the Design chain. Typical
roles are `requirement`, `challenge`, `decision`, `component`, `contract`,
`aggregation`, `representation`, `operation`, `update`, `invariant`, `cost`,
`tradeoff`, and `handoff`. For every node record its `from`, relation to the
previous node, supported reason, required terminology, and downstream claim.

The first-sentence-only summary should recover the hierarchy selected in the
outline. For example, a component/layout pattern may read:

```text
overall decision → component responsibility → mechanism or layout
→ operation/update consequence → next component or implication
```

An invariant-first or lifecycle pattern should instead expose its invariant or
state transition in the first sentence sequence. Do not force every Design
section into the example above.

A component paragraph should not begin with a lower-level layout if the
previous paragraph established only the component's purpose. A later paragraph
should not reopen the Motivation opportunity; carry the requirement forward in
the smallest useful form and state the new Design responsibility.

## 8. Keep the first unit concise

When the first Design unit establishes a new component, workflow, invariant, or
organizational unit, the opening can be a short contract paragraph or the
corresponding opening for the selected pattern:

```text
challenge → component responsibility → role in the overall design
→ deferred details
```

Do not put the component's purpose, all of its mechanisms, its update path,
and the entire system architecture into one paragraph. Conversely, do not
create a separate bridge paragraph that only repeats the component's name.
Use the next paragraph's opening to carry the component forward into
aggregation, layout, or updates.

## 9. Review and revision gates

The reviewer checks the Design story and outline selected with the author. It
records the applicable requirement, Design challenge, decision, boundaries,
pattern, paragraph order, argument-node relations, and reasons for
representations or operations. It flags:

- a component introduced without a prior challenge or requirement;
- a representation or lower-level mechanism presented before the concept it
  implements when the selected pattern requires the separation;
- relations such as aggregation, layout, and updates mixed without a
  recoverable reason;
- a component list that does not state how the overall design uses each unit;
- a Motivation restatement or Evaluation result inside Design; and
- a named component whose responsibility is not distinct from its parent.

The reviser receives these frozen contracts and rewrites from them rather than
preserving the source paragraph boundaries. The verifier reconstructs the
Design chain and argument-node graph from the final prose and checks it against
the aligned outline.

## 10. Compactness and evidence

Keep one main logical relation per sentence. A Design sentence should explain a
choice, its contract, its supported reason, or its consequence. Remove a
detail when it does none of these. Preserve invariants, conditions, costs, and
interfaces that later Design or Evaluation depends on. Do not add a detail only
to make the paragraph sound complete.
