# Argument-Node Outline and Human Sync View

Use this workflow after story alignment and before prose rendering whenever the
author is discussing presentation structure, requesting a structured outline,
or asking for guided generation. It gives the coordinator a precise execution
contract and gives the author a sentence/logic-level artifact for
synchronization. It does not create a second canonical outline.

Before prose, also apply the [sentence-level realization contract](sentence-realization-contract.md).
Argument nodes describe the logic, but the realization contract is the writer's
closed-world input. A node whose payload is only “report,” “explain,” or
“discuss” is not ready for rendering.

When the author supplies a coarse outline, also use the [hierarchical outline
research workflow](hierarchical-outline-research-workflow.md). Keep the L0
subsection claim, L1 paragraph claims/interfaces, and L2 sentence propositions
as parent and child records. Do not expand L2 independently of its L1
paragraph claim.

First apply the [semantic object and logic graph workflow](semantic-object-graph-workflow.md).
Argument nodes and sentence slots are projections of that graph; they are not
places to invent new objects, claims, terms, or causal relations.

## 1. Use three levels of representation

Keep these levels distinct but linked:

1. **Story map:** the paper-level chain of supported questions, observations,
   pressure, opportunity, insight, requirements, design choices, evidence,
   results, and implications.
2. **Argument-node outline:** the reader-facing hierarchy and the logical units
   that a paragraph must render. Each node carries one main claim, evidence,
   condition, explanation, contrast, or handoff relation.
3. **Prose:** the English rendering of the aligned outline.

Call a unit an `argument node` because it names the logical responsibility of a
sentence slot. A node normally maps to one planned sentence. Adjacent nodes may
share a sentence only when their relation is simple and the resulting sentence
remains easy to parse; otherwise split them. A sentence with several
independent claims must map to several nodes and should normally be split
before prose rendering. The author-facing outline must therefore expose every
sentence slot or logical node, even when the final prose later combines two
closely related slots.

## 2. Keep one canonical outline and derive two views

The fixed outline remains the only canonical presentation specification. Store
argument-node IDs and relations in its paragraph and sentence contracts; do not
create a second story, presentation, or synchronization file.

Derive two views from that outline:

- **Execution view:** full IDs, `from`, `needs`, evidence locators, scope,
  terminology, dependencies, figure bindings, and handoffs for agents.
- **Human sync view:** a two-layer author-facing projection. First show the
  section/subsection/paragraph navigation; then show every paragraph's
  sentence slots or logical nodes with role, claim, `from`, `needs`,
  `link`/transition, evidence, and `provided_to`. Emit it in the discussion
  response and, when the fixed outline schema permits, store it as a generated
  projection inside the same outline revision. It is never an independent
  source of truth. A paragraph-only summary is not sufficient for outline
  alignment.

If the author edits the human sync view, the coordinator maps the change to
stable outline IDs, records an outline delta, and regenerates the execution
view. Do not let a writer infer structure from an unaligned human edit.

## 3. Argument-node schema

For each node, record the semantic graph fields first, then the presentation
fields:

```text
node_id
sentence_slot
role
object
semantic_payload
from
relation_to_previous
supports_or_answers
needs
evidence
scope
canonical_terms
provided_to
status
```

Useful roles include `question`, `setting`, `observation`, `pressure`,
`opportunity`, `claim`, `evidence`, `explanation`, `mechanism`, `contrast`,
`cost`, `condition`, `net_effect`, `implication`, and `handoff`. Select the
role from the actual argument; do not add labels that do not change the
reader's reasoning.

`relation_to_previous` should name the supported edge, such as `supports`,
`explains`, `qualifies`, `contrasts`, `motivates`, `causes`, or
`transitions-to`. A node with no recoverable relation is incomplete even if its
local wording sounds plausible. `evidence` identifies the figure, table,
measurement, citation, or supplied reasoning that supports the node; it does
not merely repeat the node's semantic payload.

For a claim followed by evidence, make the direction explicit:

```text
[Claim] Prefix reuse can reduce serving cost.
[Evidence] The measured reuse rate is X% under workload W.
  relation: supports → Claim
[Condition] The benefit depends on the cached blocks remaining available.
  relation: qualifies → Claim
```

For Evaluation, use the relevant metric purpose, result, explanation, cost,
and workload/configuration as separate nodes when they carry separate
relations. For Motivation, keep the nodes design-independent and do not
introduce a later representation merely to make the chain concrete.

## 4. Synthesize the outline after story alignment

The coordinator should not ask the author to approve prose before this pass.
Synthesize, in order:

1. section and subsection hierarchy, local questions, and responsibilities;
2. paragraph roles, incoming endpoints, central claims, provided claims, and
   outgoing handoffs;
3. argument nodes in reader-facing order, with their relations and evidence;
4. sentence-level realization contracts that map each eventual sentence to one
   concrete proposition and one or more nodes, preserving `from`, `needs`,
   `link`/`transition`, and scope; and
5. figure, table, terminology, and evaluation-specific bindings.

The argument-node order is the proposed reader path. It may differ from source
paragraph order, figure order, or the order in which the author discovered the
idea. For a Design breakdown, preserve Design order; for other sections, use
the selected question and dependency graph.

Run the first-sentence-only check on the paragraph openings and the
node-only check on each paragraph. Reading only the node summaries should
recover the paragraph's role and progression. If it does not, reorganize,
merge, split, relocate, or drop nodes before rendering prose.

## 5. Render the sentence/logic-level human sync view

The sync view should be compact enough for the author to approve or edit, but
must preserve the complete local logic chain. Use this shape:

```text
Subsection: <local question>

Paragraph 1 — <role>
  S1 [Claim] <what this sentence establishes>
     from: <incoming endpoint or prior paragraph>
     needs: <definition, context, or evidence>
     provides: <claim used by a later node>
  S2 [Evidence] <what the evidence shows>
     from: S1
     link: supports S1
     needs: <figure, table, citation, or measurement>
  S3 [Interpretation] <what S2 means for the argument>
     from: S2
     link: explains S2
     provides: <next claim>
  S4 [Transition/Handoff] <why the next paragraph follows>
     from: S3
     link: motivates → Paragraph 2

Paragraph 2 — <role>
  S5 [Claim] ...
     from: S4
     needs: ...
     link: ...
```

For a performance paragraph, do not collapse the logic into “report the
metric, cite the figure, and compare baselines.” Expand it into the units the
writer must render, for example:

```text
P1 — overall request throughput
  S1 [Purpose] State what request throughput measures and why this metric is
     reported.
  S2 [Result] Report the proposed system's throughput across the evaluated
     workloads.  from: S1  needs: Figure <id>
  S3 [Comparison] State the supported range relative to the relevant
     baselines.  from: S2  link: compares
  S4 [Interpretation] State what the result establishes for the section's
     claim.  from: S3  link: supports
  S5 [Transition] Explain why the next breakdown or metric follows.  from: S4
     link: motivates → P2
```

The labels are planning contracts, not prose to copy into the manuscript. The
author can move, merge, split, or delete these slots before writing.

For the writer, replace each row's short payload with the full realization
fields: proposition, reader question, relation, evidence, scope, canonical
terms, and provided claim. Keep the short human view for synchronization, but
do not use it as the sole writer input.

Show the smallest useful evidence locator and scope condition, but omit
internal confidence fields and raw source-unit lists unless the author asks
for them. Keep stable sentence-slot labels such as `S1`, `S2`, and `S3`; they
are the handles the author uses to move, merge, split, or rewrite a logical
unit. The view must let the author decide whether each claim is supported,
whether each concept is introduced before use, whether a paragraph is in the
right place, and whether every transition has a concrete endpoint without
reading the prose.

Do not replace the sentence/logic rows with a paragraph summary such as “report
the result, then explain the breakdown.” That is a navigation note, not an
aligned outline. If the agent can provide only that summary, keep the state at
`Awaiting outline alignment` and ask it to expand the paragraph into logical
nodes.

The coordinator should present the sync view together with only the open
choices that require author judgment. Agreement with the story does not imply
agreement with this grouping or node order. Keep the state at
`Awaiting outline alignment` until the author aligns the view or explicitly
authorizes an automatic choice.

## 6. Independent review, revision, and verification

Use separate calls or sub-agents with explicit input boundaries:

- **Structural reviewer:** receives the frozen manuscript version, canonical
  outline revision, argument-node execution view, sentence/logic-level human sync view, evidence,
  and writing rules. It is read-only and returns findings, missing or broken
  edges, required organization moves, and acceptance conditions. It does not
  receive a reviser's rationale or draft.
- **Reviser:** receives the same frozen manuscript and aligned outline, plus
  the frozen review artifact and accepted author decisions. It writes only
  inside the authorized scope and records any outline delta. It does not
  rewrite the review decision or silently redesign the node graph.
- **Verifier:** receives the integrated revised manuscript, the frozen
  acceptance conditions, and the outline revision in a fresh context. It does
  not rely on the reviser's self-check or process explanation. It reconstructs
  the argument-node graph from the final prose and compares it with the
  canonical outline.

The coordinator is the only role that updates the canonical outline, merges
patches, resolves shared edges, or changes the author-aligned story. If the
reviewer and reviser are implemented by the same model, they still require
separate calls, separate role prompts, and a frozen artifact boundary; a
self-review inside a revision call is not independent.

## 7. Acceptance checks

Before prose rendering, verify:

- the semantic object graph has no unsupported object, claim, purpose, result,
  cost, condition, or lexical item;
- every mechanism, operation, metric, and result has a supported purpose or
  question edge;
- every paragraph has a local question, role, incoming endpoint, and outgoing
  handoff;
- every sentence slot or argument node has one main responsibility and a
  supported relation;
- every claim has nearby evidence or an explicit reasoning basis;
- evidence nodes identify what they support rather than merely repeating a
  number;
- conditions and scope remain attached to the claims they qualify;
- technical lexical items have provenance, canonical forms, semantic
  contracts, and scope; unsupported modifiers are removed or unresolved;
- concepts appear at the correct abstraction layer before dependent nodes;
- the human sync view is a faithful projection of the canonical outline;
- the human sync view exposes every sentence slot or logical node rather than
  only paragraph-level summaries; and
- the first-sentence-only and node-only summaries recover the intended path.

After revision, reconstruct the node graph from prose without consulting the
writer's explanation. Missing, invented, reversed, or overstrong nodes are
outline or prose findings, not matters for final English polish.
