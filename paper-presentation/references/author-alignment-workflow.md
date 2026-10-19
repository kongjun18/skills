# Story–Outline Alignment–Review–Revision Workflow

Use this as the default interaction protocol for presentation work. The
orchestrator first aligns the story and exposes the proposed reader-facing
structure in the fixed structured outline. It lets the author align both
artifacts before dispatching the independent reviewer and reviser. An
explicit review request may diagnose an existing artifact first, but a rewrite
still returns to story and outline alignment when those artifacts are not
fixed. Apply the [coarse-to-fine refinement pipeline](refinement-pipeline.md):
each alignment is for the current stage, and a later prose pass must not
silently resolve an earlier story or structure decision.

For the outline's logical units and the author-facing projection, use the
[semantic object and logic graph workflow](semantic-object-graph-workflow.md)
and the [argument-node outline workflow](argument-node-outline-workflow.md).
Apply the [structured outline refinement workflow](outline-refinement-workflow.md)
before presenting an outline for author alignment.
The semantic object graph, argument-node execution view, and sentence/logic-
level human sync view are generated from the same fixed outline.

When the author replies to a review or discussion, also apply the
[review-to-outline continuation routing workflow](continuation-routing-workflow.md).
Treat the reply as a state transition: record its decisions, synthesize the
next structured artifact when it is missing, and state the next stage instead
of waiting for the author to issue a second workflow command.

## Default author-driven route

For an ordinary discussion, rewrite, or improvement request, begin with the
author's story and reader-facing structure:

```text
story discussion → author story alignment → structured outline synthesis
→ sentence/logic-level human sync view → author outline alignment
→ independent review → revision → independent verification
```

This route is the same for Motivation, Design, Background, and Evaluation.
Section-specific pattern catalogs help choose the story and outline, but they
do not add a separate workflow stage. Do not dispatch a prose reviewer or
writer before the author has aligned the story and structured outline. Once
that alignment is complete, the reviewer and reviser remain separate roles and
the reviser may run the named prose-refinement rounds automatically.

If the author supplies only a section direction, use the [section content
planning workflow](section-content-planning-workflow.md) inside the discussion
step. Expand the direction into a section purpose, content dimensions,
argument nodes, evidence, and handoffs, return the structured outline and
sentence/logic-level human sync view, and wait for outline alignment. This does
not start prose review or revision.

An explicit `review` request may start with the read-only Review stage below so
the author can diagnose an existing artifact. If that review does not already
provide an aligned story and outline, route any rewrite through the default
story-and-outline sequence before revision.

## Stages

### 0. Reference-material intake (source-only rewrites)

When the author supplies a poor subsection as material rather than as a target,
freeze that source version and run the [reference-material rebuild workflow](reference-material-rebuild-workflow.md).
Extract supported facts, claims, conditions, evidence, and terminology
candidates into a material ledger. Mark the source wording, paragraph order,
transitions, and sentence roles as non-authoritative unless the author
explicitly protects them. Recover the story independently and stop at
`Awaiting story alignment` in a manual run. Do not let a source-only rewrite
enter the ordinary Revision stage from the old prose alone.

### 1. Review

In the default route, run this stage after story and structured-outline
alignment. Read one fixed manuscript version and the exact outline subtree for
the requested scope. Return located findings, acceptance conditions, outline
changes, affected terminology and figures, and unresolved context. Keep the
manuscript read-only. Freeze this review artifact before any writer is
dispatched. The reviewer and writer are separate roles, calls, or sub-agents;
if delegation is unavailable, use a clean sequential handoff. A writer's
self-check cannot replace this review.

### 2. Author alignment

Convert the author's response into an explicit decision in the fixed outline.
For a source-only rewrite, record the source disposition map separately before
recording the new target outline:

- accepted findings and required fixes;
- rejected or deferred findings and the reason;
- selected hierarchy, grouping, and paragraph order;
- protected claims, evidence, scope, and terminology;
- the recovered Motivation contract, leakage decisions, and selected
  design-independent insight when Motivation is in scope;
- the selected section pattern for each section and the reason it fits;
- the semantic object types and relations, argument-node order, node roles,
  evidence relations, conditions, and
  paragraph-to-node grouping shown in the human sync view;
- for Evaluation, the selected question or archetype, macro progression or
  narrative order, claim–evidence bindings, and source/design/figure-order
  decisions;
- approved changes to subsection boundaries or figures; and
- decisions that remain `Needs context`.

Freeze the active terminology ledger and semantic operation/state contracts
before revision. A writer may use only active canonical terms and their allowed
forms. A new technical term, synonym, or state-changing verb is a review
finding or an author decision, not a local wording choice. Record each
accepted term decision as a proposed glossary edit.

Do not interpret “keep the important content” as “keep every source sentence.”
The material ledger decides what is retained, relocated, merged, split,
deferred, or dropped; the author only needs to resolve the substantive alternatives and
protected decisions.

Natural-language responses such as “按这个改，但保留原来的 subsection 顺序”
must be normalized into the outline's stable IDs, roles, order, handoffs, and
change log. If the response is ambiguous about a claim, structure, or section
responsibility, ask one focused question rather than silently choosing.

If the response accepts the findings or aligns the story but does not provide a
complete reader-facing structure, automatically continue to outline synthesis:
produce the section/subsection hierarchy, paragraph roles and order,
argument-node summaries and relations, sentence mappings, handoffs, and
evidence mappings, then render the sentence/logic-level human sync view and
set `Awaiting outline alignment`. Do not treat “按这个方向改” as permission to skip the
structured outline. Continue directly to interface compilation only when the
author has supplied or selected a complete, validated outline and has
authorized editing.

### 3. Outline synthesis and alignment

Keep story/claim alignment as a diagnostic pass, but store the reader-facing
answer in the fixed outline. When Motivation is in scope, align the recovered
opportunity and requirements before aligning the Design chain. The outline
should specify section and subsection hierarchy, ordered paragraphs, local
responsibility, incoming and outgoing handoffs, argument nodes and their
relations, evidence mappings, and sentence-level `from`, `needs`, and
`link`/`transition` fields. Return the sentence/logic-level human sync view in
the same turn so the author can align the full chain without reading internal
metadata. A paragraph-only summary is not sufficient.

If the author has not selected or adjusted grouping, order, or handoffs, set
the stage to `Awaiting outline alignment` and do not dispatch writers. Update
the exact outline file and its change log once aligned. Later discussion and
review load that file and its revision; they do not reconstruct a separate
outline revision.

After story alignment and before interface compilation, run the [presentation
organization gate](presentation-organization-workflow.md) whenever the prose
or current outline is hard to follow. Story agreement does not make the
existing paragraph grouping, sentence order, or openings authoritative. The
gate must explicitly consider merge, split, reorder, relocate, delete, and
rewrite moves. If the story and substantive interfaces remain unchanged,
presentation-only organization may be applied within the authorized scope; if
grouping or sentence roles change in the fixed outline, expose the target
delta and obtain outline alignment rather than silently preserving the old
layout.

When the author explicitly requested review, the continuation after a review
response is:

```text
review → record author decisions → outline synthesis → present outline
→ outline alignment → presentation organization → interface compilation
→ revision
```

For the ordinary author-driven route, the continuation is instead:

```text
story discussion → story alignment → outline synthesis and sentence/logic-level human sync view
→ outline alignment → independent review → presentation organization
→ interface compilation → revision → verification
```

For a source-only rewrite, use:

```text
material audit → independent story recovery → author story alignment
→ outline synthesis → outline alignment → independent review
→ presentation organization → interface compilation → revision → verification
```

Return the synthesized outline in the same turn that the route is selected
when the current interaction supports it. If a substantive choice remains
ambiguous, return the alternatives and the smallest author decision needed,
rather than silently choosing a paragraph order.

### 4. Presentation organization and interface compilation

Before dispatching writers, turn the aligned outline subtrees into subsection
contracts. Each contract records local responsibility, incoming handoff,
central claim, claims provided to later subsections, outgoing handoff,
protected evidence and terminology, allowed local changes, and the owner of
each shared edge. Freeze these interfaces for the revision round. A writer may
propose an outline delta, but may not silently apply a change to a shared edge
or substantive claim. It may still make an authorized presentation-only merge,
split, reorder, relocate, or deletion inside its owned subtree and must record
the change.

### 5. Revision

Give each writer the fixed manuscript version, fixed outline revision, issue
IDs, acceptance conditions, frozen review artifact, scope manifest, and frozen subsection contract. The
writer may reorder or rewrite within its outline subtree, but must preserve
protected content and report any conflict. Independent subsection writers may
run in parallel from the same fixed version and must return isolated patches.
The coordinator updates the outline before accepting a boundary or claim
change, then reruns the affected dependency cone.

When the story and outline are aligned but the prose needs more than a local
rewrite, instantiate the [iterative prose refinement workflow](iterative-prose-refinement.md).
Run semantic rendering, presentation/logic repair, and concise English polish
as separate rounds with a fixed version and gate for each. A writer may not
collapse these rounds into one undifferentiated rewrite.

### 6. Independent verification

Give the exact revised artifact and exact outline revision to the reviewer.
Reapply the relevant criteria to the full scope, check every accepted finding,
and verify that the revision did not change rejected or protected items. A
writer's own agreement or self-check is not independent verification.
For a multi-round prose revision, verify the final Round 3 artifact and retain
the round history; if verification finds a Round 1 or Round 2 regression,
return to that round rather than applying another language-only pass.

## Default routing

Use this staged workflow when the user asks to improve, revise, polish, or
discuss a manuscript without explicitly requesting autonomous end-to-end
editing. The default status after Review is `Awaiting alignment`; after claim
alignment, use `Awaiting outline alignment` until the fixed outline's reader-
facing structure is selected.

After the author aligns the reader-facing outline and authorizes prose edits,
the orchestrator automatically runs the three named prose rounds, even though
the story and outline decisions were handled manually. Manual mode controls
substantive decisions; it does not require the user to trigger each wording
round. Pause only when a round exposes a new story, claim, hierarchy,
terminology, evidence, or scope decision. Use `draft-only` only when the author
explicitly requests the first semantic-rendered draft.

Use `auto` when the user explicitly authorizes the orchestrator to make
presentation decisions that would otherwise require alignment, such as choosing
among competing stories or outline structures. The three prose rounds do not
require `auto` once their outline and edit authorization are aligned. Stop with
`Needs context` for missing evidence or a substantive author decision.

Direct `revise` or `guided` requests may skip a new review only when the user
has supplied an independent review artifact bound to the exact input version,
with issue IDs and acceptance conditions, or explicitly requests a wording-only
change whose scope is fully fixed. An aligned outline alone does not replace
review. Otherwise review the fixed input before changing it.
