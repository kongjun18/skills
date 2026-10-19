# Section Content Planning Workflow

Use this workflow inside `discuss` when the author provides a high-level
direction for a section but not a complete reader-facing outline. It is a
planning stage, not a prose-writing stage. It turns the author's direction
into candidate content and structure, then waits for author alignment before
review or revision.

First apply the [semantic object and logic graph workflow](semantic-object-graph-workflow.md).
The plan must be built from typed objects and supported relations, not from
draft sentences.
Before returning the plan, apply the [structured outline refinement
workflow](outline-refinement-workflow.md) and complete its three gates.

## 1. Recover the section purpose

State the question the section must answer, the role it plays in the paper,
the abstraction level, and the claim it should leave the reader with. Keep
this purpose independent of sentence wording and avoid importing later Design
details merely because they could make the section sound concrete.

For a Related Work section, the purpose is usually to position the paper along
relevant research dimensions and make the closest distinction clear. The
agent must verify the actual purpose from the paper rather than assume this
template applies.

## 2. Generate content dimensions and alternatives

From the supplied direction, manuscript context, evidence, and available
references, propose the smallest useful set of organizing dimensions. A
dimension may be a problem, workload, abstraction, design choice, consistency
property, evaluation goal, or other supported comparison axis. Do not organize
by paper chronology or list papers one by one unless that is the section's
actual question.

For each candidate organization, record:

- the question or distinction it makes visible;
- the categories or subsections it creates;
- the representative works or evidence needed;
- the relation to the paper's own claim; and
- the cost, ambiguity, or missing evidence introduced by the choice.

If several organizations are equally supported, present them as alternatives
for author alignment. In an authorized automatic run, choose only when the
choice does not change the paper's contribution claim or scientific emphasis;
otherwise stop with `Needs context`.

## 3. Expand the selected direction into semantic objects and argument nodes

Before writing prose, create a semantic object graph and then project it into
argument nodes. For every subsection or paragraph record the objects, claims,
evidence, purposes, costs, conditions, and handoffs before recording:

```text
local question or role
→ opening claim
→ concepts and prerequisites
→ representative evidence or citations
→ interpretation or comparison
→ limitation, boundary, or relation to this paper
→ claims provided to the next unit
→ outgoing handoff
```

For a Related Work category, the nodes often follow:

```text
category claim
→ representative prior systems
→ shared approach or comparison axis
→ supported boundary or limitation
→ relation to this paper
→ next category or final positioning
```

This is an example, not a fixed Related Work template. Use the dependency
graph that the section actually needs.

## 4. Return two synchronized outline views

Return both:

1. the execution outline with stable IDs, node roles, relations, evidence,
   terminology, conditions, and sentence-level `from`/`needs`/`link` fields;
2. the sentence/logic-level human sync view that shows the section purpose,
   paragraph navigation, and every sentence slot or logical node with its
   object, type, semantic payload, role, `from`, `needs`, evidence, purpose or
   question edge, transition, and handoff.

Generate both views from the same outline revision. The human view should let
the author confirm the entire local logic chain without reading internal
metadata. A paragraph-only overview is not sufficient.

## 5. Stop before prose when the structure is incomplete

Set the run to `Awaiting outline alignment` when the author has not selected
the organization, category boundaries, paragraph order, or handoffs. Do not
start a draft, imitate the old prose, or let a writer choose among competing
structures. After the author aligns the outline, route to independent review,
then revision and the named prose-refinement rounds.

## 6. Keep planning separate from source authority

When an old section is supplied as material, audit its facts, citations,
scope, and terminology candidates, but do not inherit its grouping or order.
The planning output must show how each retained unit maps to the new outline
or why it is relocated, merged, deferred, or dropped.

## 7. Planning gate

The stage passes when the author can answer:

- What question does this section answer?
- Why are these categories or dimensions grouped together?
- What does each paragraph establish?
- Which evidence or citation supports each claim?
- How does each paragraph connect to the next?
- What final relation to the paper should the reader retain?

If any answer depends on an unstated decision, preserve the alternative and
ask for the smallest author choice needed.
