# Guided Paragraph Generation Workflow

Use this workflow when the author supplies paragraph roles and logical
relations but wants publication-ready prose. Read the fixed outline workflow
first. The author's map is a proposed edit to the relevant outline subtree;
the generated paragraph is only correct when it can be round-tripped to that
subtree.

Also read the [argument-node outline workflow](argument-node-outline-workflow.md).
Also read the [semantic object and logic graph workflow](semantic-object-graph-workflow.md).
Treat the semantic object graph and argument-node execution view as the logical
contract and return a node-to-prose trace together with the generated
paragraph. The human sync view is for author alignment; it does not replace
the full object and node metadata.
Also read the [claim-flow materialization workflow](claim-flow-materialization-workflow.md).
Also read the [sentence-level realization contract](sentence-realization-contract.md).
Freeze the complete ordered claim flow before rendering any paragraph; prose is
its materialization, not a place to discover missing claims or transitions.

Select the relevant section pattern from [the section presentation playbook](section-presentation-playbook.md).
Also compile the [subsection flow and abstraction workflow](subsection-flow-workflow.md)
before rendering prose. A paragraph map is not complete until its subsection
opening purpose, abstraction level, and boundary ownership are explicit.
When the supplied paragraphs include Motivation, run [Motivation Recovery](motivation-recovery-workflow.md)
before rendering them so that a design-independent opportunity is not
silently replaced by a design justification.

For comparisons, design tradeoffs, core claims, paragraph openings, or figure
introductions, also use [the claim rendering and tension workflow](claim-rendering-workflow.md)
after the paragraph contract has been validated.

## 1. Compile the paragraph contract from the outline

Represent each paragraph using the stable IDs in the fixed outline. Include:

- section/subsection and local role and question;
- subsection opening purpose, abstraction level, and transition mode;
- incoming handoff and its relation to the preceding unit;
- outgoing handoff and the concrete node the next unit needs;
- central claim or takeaway;
- the concept layer allowed in this paragraph and any future-layer concepts
  that must remain deferred;
- whether an operation list is representative or exhaustive;
- concepts and operations that must be introduced before use;
- evidence, figures, tables, or citations allowed to support it;
- workload, configuration, baseline, and other scope conditions;
- protected facts and phrases; and
- mechanisms, claims, or terminology that must not be introduced here.

Within the paragraph, list the semantic objects and argument nodes in
reader-facing order. For each node, record its type, object, semantic payload,
role, relation to the previous node, purpose/question edge, evidence or
reasoning basis, scope, lexical terms, and the sentence contract(s) that will
render it. Keep
the node order independent from the source sentence order. A node may share a
sentence with an adjacent node only when their relation remains explicit.

For each needed concept, also record whether it is an independent node that
will be used later or only an inline description. Do not introduce a named
representation, encoding, or intermediate form without a later distinction or
operation that depends on it.

Compile the sentence-level realization contract from these nodes before calling
the writer. Every slot must state a concrete proposition, reader question,
incoming relation, evidence, scope, canonical terms, and provided claim. A row
such as “explain the result” is incomplete and must be expanded. Round 1 uses
one slot per sentence by default and returns a sentence-to-slot trace.

For a comparison or tension, also record the shared question, aligned
outcome/path axes, reader-visible effects, causal sources, and net-effect
conditions. For a core design claim, record the canonical term and any figure
that should be first cited beside it.

For an interface paragraph, record the responsibility, selected operations,
each operation's input, purpose, output or effect, and the implementation
families that follow. Use scope-calibrated wording when the paragraph focuses
on representative operations. Do not call a selected subset the complete
interface unless the source establishes that scope.

If an endpoint, evidence mapping, or claim scope is missing, mark the outline
`Needs context` before drafting. Do not fill the gap with a plausible system
fact.

## 2. Validate the outline subtree

Load the exact outline file named by the fixed index and compare the supplied
map with it. If the map changes hierarchy, grouping, order, boundaries, roles,
or handoffs, return an outline delta and stop for alignment. Do not treat a
graph whose edges are all supported as sufficient evidence that its
presentation order is good.

Check that:

1. every incoming edge has a named source in the preceding scope;
2. every paragraph claim has evidence or an explicitly stated reasoning basis;
3. every concept is introduced before its first dependent use;
4. every outgoing edge is a supported handoff rather than a new unexplained
   topic; and
5. section contracts remain valid, especially design-blind Motivation and
   Design-to-requirement traceability.
6. each subsection opening states its purpose and owned object without
   repeating the preceding subsection's explanation;
7. each paragraph stays at its declared abstraction level, and no bridge-only
   sentence duplicates the next opening; and
8. every named concept and clause has a current or downstream reader-facing
   job; and
9. no concept is locally defined but premature for the paragraph's abstraction
   layer, especially a representation, encoding, identifier, data structure,
   or proposed component in Motivation.
10. every argument node has a sentence mapping or an authorized merge, split,
    relocation, or drop, and every node relation is rendered or explicitly
    marked unresolved.

Report contradictions, missing evidence, and ambiguous endpoints before prose
generation. Once the story and substantive interfaces are aligned, still run
the [presentation organization gate](presentation-organization-workflow.md)
when the current paragraph grouping, sentence order, or openings are weak.
Preserve the aligned story and claims, but do not preserve a poor presentation
organization merely because the outline was previously written. Record any
presentation-only merge, split, reorder, relocate, or deletion in the outline
change log before rendering.

## 3. Render one paragraph contract at a time

Use the smallest context that makes the edges recoverable: the preceding
paragraph's final handoff, the current outline contract, the terminology
ledger, allowed evidence, and the next paragraph's incoming edge. Do not write
the next paragraph early or use later Design details to strengthen Motivation.
Write paragraphs in outline order. Independently verify each paragraph's node
sequence and endpoints before starting the next one; after all paragraphs pass,
run the subsection-level opening/endpoint migration check.

Pass the complete ordered sentence slots for the current paragraph to the
writer. Require the returned prose and a sentence-to-slot trace. Do not accept
an untraceable paragraph, a topic-level outline, or a paragraph that fills a
missing slot with an invented term or relation.

Choose a reasoning pattern from the relation in the contract, for example:

- observation → interpretation or pressure → opportunity;
- claim → evidence → interpretation → scope condition;
- design decision → consequence or invariant → mechanism;
- metric purpose → source observation → benefit → cost → net effect; and
- result or limitation → applicability condition → next question.

Within the paragraph:

- open with the paragraph's local purpose or the concrete endpoint inherited
  from the preceding paragraph;
- for a central object, state its purpose or operation before describing what
  the system stores, keeps, or records;
- introduce each needed concept operationally before using it in a claim;
- state evidence with an explicit source clause when a figure or table is
  involved;
- keep one main graph relation per sentence and preserve qualifiers beside
  the claim they qualify;
- explain why the paragraph's result makes the outgoing edge necessary; and
- end with the current paragraph's completed claim or the smallest concrete
  need that makes the next paragraph necessary; do not append a standalone
  handoff sentence whose connection is left for the next paragraph to invent;
- start the next paragraph by carrying that endpoint forward and stating the
  next paragraph's responsibility.

For Motivation, use the smallest design-blind description that supports the
opportunity. Do not introduce a proposed encoding or data structure merely to
make a high-level object concrete. Prefer an active relation such as tracking,
mapping, or indexing when that is the supported meaning. Avoid wrapper phrases
such as “generally implement these operations with” and nominal phrases such as
“recorded sequences” when a direct actor–operation–object sentence is available.
If the intended relation or abstraction level is unclear, return `Needs context`
instead of choosing a plausible representation.

When an interface paragraph leads into implementations, state the logical
operation contract before naming the structure family. Keep the interface
operation's input and result stable when explaining how different structures
realize it, and use direct mappings to named systems only when the source
supports them.

Use simple, direct English during rendering. An essential subordinate clause
is allowed, but split a sentence when it carries several independent logical
relations, introduces multiple new concepts, or puts a condition far from the
claim it qualifies. Prefer concrete subjects and verbs over long noun chains.

For comparison prose, state the alternatives on one shared outcome/path frame
so the tension is visible. For a design tradeoff, keep the design choice or
mechanism as the source of both benefit and cost, and attach the net effect to
the supplied workload or configuration. State the reader-visible effect before
using an operation or access path to explain it. Reuse the canonical term and
place the first figure source clause beside the core claim it supports.

Do not add a generic transition, a second summary sentence, or a new concept
just to make the paragraph sound connected. Do not repair a missing first-use
orientation with `we define X as X` or an isolated `X is ...` sentence; fold an
ordinary concept's role and purpose into the sentence that uses it. If the edge is unsupported, return
`Needs context` rather than smoothing over the gap.

## 4. Polish without changing the outline

Check sentence order, referents, terminology, evidence placement, claim
strength, and paragraph economy. Keep each subsection locally understandable
when the preceding subsection is not visible, while retaining a short,
forward-oriented handoff. Do not use later implementation details to make
Motivation appear more necessary. Preserve costs, conditions, and exceptions.

## 5. Round-trip verification

Reconstruct the paragraph graph, argument-node graph, and reverse outline from
the generated prose without consulting the outline. Compare them with the
fixed IDs, hierarchy, order, node roles and relations, sentence roles,
`from`, `needs`, and `link`/`transition` relations. Return the node-to-prose
trace and report missing or invented nodes, reversed or overstrong edges,
concepts used before introduction or at the wrong abstraction layer, detached
evidence, lost scope, and a final sentence that fails to hand off the declared
endpoint.
Report missing or invented nodes, reversed or overstrong edges, concepts used
before introduction or at the wrong abstraction layer, detached evidence, lost
scope, and a final sentence that fails to hand off the declared endpoint. If
the prose needs a structural change, update the outline and its change log
before accepting the paragraph.
