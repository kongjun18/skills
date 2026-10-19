# Fixed Outline and Presentation Structure

The structured outline is the paper's single presentation specification. It is
not an input that must be discovered and it is not a second artifact beside a
generic presentation-structure record.

## Fixed location

Use exactly this project-relative location:

```text
<project-root>/scripts/paper/assets/outlines/
```

The fixed root contains `README.md`, which is the index and schema, and the
section files named by that index. Read the index first, then open the exact
file mapped to the requested section or subsection. Do not search the
workspace, `build/`, worktrees, backups, agent caches, or alternate outline
directories. If the fixed root or its index is absent, report `Needs context`
and stop; do not infer a replacement location.

The index is the only file map. A section that has no mapped file is not
outlined. Do not silently use a historical or build copy to fill that gap.

For `rebuild-from-material`, this missing-subsection rule has one controlled
exception: after the source material has been audited and the author has
aligned the recovered story, synthesize the new subsection in this fixed root
as a `proposal` and update the index. The exception never permits searching an
alternate outline directory or deriving the proposal from the old paragraph
order. The fixed root and its index must already exist.

## One artifact at different levels

The outline and presentation structure are the same artifact viewed at
different levels:

- section and subsection nodes define hierarchy, reader questions, local
  responsibilities, selected section pattern, abstraction level, and handoffs;
- paragraph nodes define the order and purpose of the argument units; and
- semantic object nodes define the concepts, claims, evidence, purposes,
  mechanisms, results, costs, conditions, metrics, and handoffs that the
  argument uses; and
- argument nodes define the logical units within a paragraph, such as a claim,
  evidence item, explanation, condition, contrast, or handoff; and
- sentence contracts map those nodes to prose while defining the local logical
  chain, evidence, definitions, transitions, and protected scope.

Call the section/subsection/paragraph projection the **presentation-structure
view**. Call the full tree, including argument nodes, sentence contracts, and
figure contracts, the **structured outline**. Generate both the execution view
and the sentence/logic-level **human sync view** from the outline when needed;
never create
or persist a parallel `presentation_structure`, `argument_graph`, or
`.paper-presentation/structure-alignment.yaml` sidecar.

The human sync view is an author-facing sentence/logic-level projection, not a
second structure record. It must expose every sentence slot or logical node,
not only paragraph summaries. If it is persisted for convenience, it must be
generated inside the same outline revision and remain subordinate to the stable
IDs and contracts of that outline. Read [the semantic object and logic graph
workflow](semantic-object-graph-workflow.md) and [the argument-node outline
workflow](argument-node-outline-workflow.md) for their schema and handoff
rules.

The outline's status, revision, manuscript version, and change log are the
alignment state. Use the existing project statuses (`current`, `proposal`, or
`agreed`) and preserve stable IDs. A change in hierarchy, order, role, claim,
source mapping, or sentence relation is an outline change and receives a new
outline version or change-log entry. A wording edit that preserves all of
those fields does not change the outline.

## Required contract fields

Preserve the outline's hierarchy and IDs. Each paragraph and sentence should
carry the fields already defined by the fixed `README.md` schema:

- paragraph ID, role, and the reviewer question it answers;
- semantic object or node IDs rendered by the sentence, including each
  object's type, short semantic payload, purpose/question edge, and status;
- sentence ID and role;
- argument-node IDs rendered by the sentence, with each node's role and
  relation to the preceding node;
- what the sentence must say, without drafting its wording;
- `from`: the source claim, observation, section, or evidence it condenses;
- `needs`: the definition, number, citation, figure, table, or source required;
- `link` or `transition`: the relation to the preceding unit when it is not
  plain continuation;
- the concept or claim introduced, supported, limited, or handed off;
- protected qualifiers, workload, configuration, and scope; and
- figure/table contracts, including takeaway, what it shows, why it is
  needed, citing sentence IDs, and source inputs.

For Motivation sections, preserve the recovered setting, observations,
pressure, opportunity, design-independent insight candidates, requirements,
and leakage decisions. These are the high-level contract that later Design
traceability uses; they do not authorize implementation detail in Motivation.

For Design sections, preserve the incoming Motivation requirement or
opportunity, the Design challenge, the pattern selected during story/outline
discussion, each component or unit's responsibility and contract, and the
reader-facing node order. Record representation, operation, invariant, cost,
or update relations only when the selected pattern and evidence require them.
The outline should make clear how the overall Design uses each unit without
imposing one storage, layout, or update sequence on every paper.

For comparison, tension, and core-claim units, also record the claim-rendering
fields when they are relevant:

- the shared comparison question and aligned outcome/path axes;
- the reader-visible effect and the mechanism that explains it;
- the causal source of each benefit, cost, or observed net effect; and
- the canonical terms and the first figure sentence that anchors the claim,
  when a figure is involved.

Do not flatten these fields into prose such as “discuss the index design.”
They are the executable contract that lets a writer produce a paragraph
without guessing what an undefined concept, claim, or transition means.

## Status and alignment

Use the exact file in the fixed root as follows:

- `agreed`: preserve its hierarchy, IDs, roles, order, handoffs, and evidence
  mappings unless the author approves an outline change;
- `current`: compare it with the manuscript version named in the file and
  report drift before revision; and
- `proposal`: discuss and align it before dispatching writers.

If the author changes a proposal, edit the fixed outline and record the
decision there. If the author has aligned only the story or claims, keep the
run at `Awaiting outline alignment`; the outline's grouping, order, and
handoffs are still undecided. Once aligned, compile subsection contracts
directly from the selected outline subtree.

## Synchronization and verification

At the start of every `discuss`, `review`, `revise`, or `auto` run, read the
fixed index and the exact outline files for the requested scope. Compare their
manuscript version with the input artifact. Report role drift, missing
`needs`/`from` mappings, broken `link`/`transition` relations, and figure
contract drift before drafting.

After revision, reconstruct the section, subsection, paragraph, and sentence
structure from the prose without consulting the outline. Compare that reverse
outline with the fixed outline and report any missing, duplicated, reordered,
or newly invented unit. An edit is structurally verified only when the prose
and the fixed outline agree.

## Parallel revision

Freeze a content version and derive each worker's subsection contract from a
disjoint subtree of the fixed outline. The contract includes the incoming
handoff, local claim, claims supplied to later units, outgoing handoff,
protected evidence and terminology, and allowed local changes. Workers may
edit their owned prose but may not alter another subtree or silently change a
shared edge. A proposed boundary change is first an outline delta; after the
coordinator updates the fixed outline, rerun the affected dependency cone.
