# Coarse-to-Fine Presentation Refinement Pipeline

Use this pipeline for both automatic iteration and manual review/revise work.
It improves one layer at a time. A later layer may polish an earlier decision,
but it may not silently reopen or replace an earlier structure. If a later pass
finds a regression in an earlier layer, return to that layer, repair it, and
rerun the affected downstream passes.

The fixed high-level story, when present, lives at
`<project-root>/scripts/paper/assets/outlines/story.md`. The section files in
the same fixed outline root contain the paragraph- and sentence-level
contracts. The story and the detailed outline are different views of the same
argument, but they are checked separately:

- the story answers what the paper must establish and why each next claim is
  needed;
- the outline answers where the reader encounters each claim and how each
  sentence renders it; and
- the prose is a rendering of the aligned outline, not a place to invent a
  missing story or structure.

Use the [argument-node outline workflow](argument-node-outline-workflow.md)
after story alignment and before prose rendering. First use the [semantic
object and logic graph workflow](semantic-object-graph-workflow.md) to build
typed objects, claims, evidence, purposes, and relations. The argument-node
execution view and sentence/logic-level human sync view are projections of
that graph and the same canonical outline. Before writing, also use the
[sentence-level realization contract](sentence-realization-contract.md): the
writer needs concrete propositions and relations, not topic-level node labels.

## Stage protocol

Use discussion and author alignment for the story, section architecture, and
structured outline. After those gates pass, use a narrow
`review → align → revise → verify` loop for prose and presentation changes.
Record the stage, fixed manuscript version, outline revision, scope, findings,
gate result, and next stage. Do not make every pass redo every other pass.

### Stage -1: reference-material intake (source-only rewrites)

When a poor subsection is supplied as raw material, freeze it as an immutable
source version before running the ordinary stages. Build a material ledger with
source locators, evidence, scope, terminology status, and a disposition for
each unit. Mark the old wording, paragraph order, transitions, and sentence
roles as non-authoritative unless the author explicitly protects them. Do not
derive the target outline from the source paragraph boundaries.

Recover the subsection story independently from its section responsibility,
adjacent context, evidence, and material ledger. In a manual run, present this
story and the open alternatives to the author and stop at story alignment. In
an authorized automatic run, record the selected story and rationale. Only
after that alignment should the pipeline enter Stage 0 or Stage 1 and
synthesize a new reader-facing outline.

Gate: the workflow has a source disposition map, a supported story, and no
unresolved choice about whether the old organization is being preserved. A
writer must receive the aligned contracts and material ledger rather than the
old prose as a drafting template.

### Stage 0: Motivation recovery, section contracts, and story spine

When Motivation is in scope, run the [Motivation Recovery Workflow](motivation-recovery-workflow.md)
before using Design to explain or repair it. Read the applicable [section
presentation playbook](section-presentation-playbook.md) and select a supported
pattern for each section under review.

The sealed Motivation output records the setting, observations, pressure,
opportunity, design-independent insight candidates, requirements, and a
unit-level leakage map. It also records the allowed Motivation abstraction
level and the first-use order for concepts. Classify naive solutions and
proposed mechanisms separately from the high-level opportunity. If multiple
insight candidates are supported, keep them as alternatives for author
alignment rather than choosing one from later Design details.

Check only the paper-level logic:

```text
question → problem → observation → pressure → opportunity
→ insight/requirements → design promises → evaluation claims
```

Record the supported nodes and edges, the paper's central claim, selected
section patterns, section responsibilities, and the handoff between sections.
The Motivation recovery pass should be completed before the Design
traceability pass. This stage should not polish sentences or import
implementation details to strengthen the problem. Apply an abstraction
firewall: a proposed representation, encoding, identifier, data structure,
algorithm, or component cannot enter Motivation merely because it has been
defined locally. If the opportunity can only be stated with that detail, mark
the boundary as unresolved or move the detail to Design.

Before leaving this stage, create a concept-layer map for the Motivation scope.
For each concept, record its first use, prerequisite, layer, allowed location,
and deferred location. For each central object, record the purpose or operation
that must be stated before its representation. This map is an input to the
sentence and subsection passes, rather than an informal reminder that can be
lost during prose generation.

Gate: a reader can state the problem, why it matters, what opportunity follows,
and what the paper should establish without reading the detailed Design
outline. Motivation should remain valid when the proposed implementation is
replaced, and every major Design choice should map to a prior requirement or
an explicitly recorded scope decision.

### Stage 1: section and subsection architecture

Check section order, subsection order, local questions, responsibility,
subsection autonomy, and cross-section handoffs. Each subsection must have a
recoverable purpose and must not require the reader to reconstruct its purpose
from a later subsection.

Gate: the section order answers the paper's questions in a forward path, and
each subsection receives a concrete object, claim, result, or pressure and
passes a concrete one to the next subsection.

When Design is in scope, consult the [Design Presentation
Patterns](design-presentation-workflow.md) during story discussion and outline
synthesis. Select a pattern only when the supported dependency graph calls for
one, and record its reader-facing node order, responsibilities, and relevant
contracts in the outline. This is part of the same story-and-outline gate; it
is not a separate reconstruction stage. The reviewer and reviser use the
aligned pattern after the outline is fixed.

### Stage 1.5: Evaluation reconstruction when triggered

When Evaluation is in scope, run the [Evaluation Presentation and Rebuild
Workflow](evaluation-presentation-workflow.md) and [Evaluation Patterns from
Systems Papers](evaluation-reference-patterns.md) before the paragraph outline.
Recover the Evaluation-level progression when the complete section is
available, select the local subsection archetype, and distinguish source,
Design, evidence, and narrative order. For source-only material, audit claims,
metrics, conditions, evidence, interpretations, costs, and limits separately
from the old paragraph groups.

Build the claim–evidence matrix and bind each result group to the question it
answers. For a design breakdown, retain the Design component order and record
the improved metric, introduced cost, and workload/configuration-dependent net
effect for every component. For other archetypes, choose the narrative order
from the question and dependency graph. If the target order happens to match
the source order, record the supported reason rather than inheriting it
silently.

For a design-centered performance breakdown, additionally freeze the proposed
design as the focal subject, the headline result before attribution, the reason
the breakdown is needed, the baseline role and compression, and the relevance
decision for each operation or implementation detail. The default baseline
role is a concise comparison anchor. Keep a baseline as a co-equal subject
only when the evaluation question requires that comparison.

Gate: the active Evaluation profile, macro progression or local archetype,
narrative order, claim–evidence matrix, paragraph responsibilities, and
source-unit dispositions are fixed or explicitly awaiting author alignment.
For a design-centered performance breakdown, the headline-result-before-
breakdown gate and the focal-design, baseline, and relevance fields are also
fixed.
The writer does not receive an old Evaluation subsection as a drafting
template.

### Stage 1.6: hierarchical outline research

When the author supplies only a rough story or paragraph-level plan, research
the outline in three passes before prose:

1. state the L0 subsection question, claim, scope, incoming pressure, and
   outgoing handoff;
2. derive L1 paragraph claims, order, responsibilities, and incoming/outgoing
   interfaces; and
3. expand each paragraph into L2 sentence propositions, relations, evidence,
   scope, and canonical terms.

Use the [hierarchical outline research workflow](hierarchical-outline-research-workflow.md).
Run an independent outline review after expansion. Show the author all three
levels and any alternatives or unresolved decisions. In a manual run, wait
for author alignment. In an authorized automatic run, select only a supported
completion and record the choice. A coarse outline never goes directly to a
prose writer.

Gate: the L1 paragraph claims and interfaces recover the L0 argument, the L2
slots recover each L1 claim, and every paragraph has a concrete incoming and
outgoing endpoint. Only then freeze the paragraph contracts for sequential
writing.

### Stage 1.75: semantic object and logic graph

Before grouping paragraphs or deriving sentence slots, build the semantic
object graph from the aligned story, evidence, terminology ledger, and section
contracts. Record the objects under discussion, claims, evidence, purposes,
mechanisms, results, costs, conditions, and handoffs. Give every Design
mechanism or operation a supported requirement/purpose edge, and every
Evaluation metric, result, or breakdown a supported question/purpose edge.

Extract technical nouns, noun phrases, adjectives, adverbs, verbs, and relation
words used by the outline into the lexical audit. Each item must have a
canonical concept, provenance, abstraction layer, scope, and semantic contract.
Treat technical modifiers as claims; remove or flag a modifier whose property,
comparison axis, scope, or support is missing. Do not introduce a lexical item
that is absent from the terminology ledger, supplied material, or author
decisions.

Gate: every active node has a supported relation and a recoverable object;
every claim has evidence or an explicit reasoning basis; every mechanism,
operation, metric, and result has a purpose/question edge; every cost and
condition qualifies the correct claim; and no node depends on an unresolved
term. Do not repair a failed graph by drafting smoother prose.

### Stage 2: paragraph and argument-node outline

Check paragraph grouping and order. For every paragraph record:

- its local question and role;
- the object, claim, result, or pressure inherited from the preceding
  paragraph;
- the claim it establishes;
- evidence and scope conditions;
- the claims it provides to later paragraphs; and
- the outgoing handoff needed by the next paragraph.

Store these fields as the paragraph-opening matrix from the [paragraph opening
workflow](paragraph-opening-workflow.md). Treat the opening claim as a
structural contract that must survive prose rendering and later polishing.

Within each paragraph, project the already aligned semantic object graph into
argument nodes before writing sentence
contracts. Give each node one main responsibility, a role, a relation to the
preceding node, its evidence or reasoning basis, its scope, and the claims it
provides to later nodes or paragraphs. Then render the sentence/logic-level
human sync view with one row per planned sentence slot or logical node, using
role-tagged summaries such as `[Claim]`, `[Evidence]`, `[Explanation]`,
`[Condition]`, and `[Handoff]`. Each node maps to one planned sentence by
default. The writer may combine adjacent nodes only during prose rendering
when their relation is simple and both node mappings remain visible.

Now compile the sentence-level realization contract. Replace each short row
with one concrete proposition, reader question, incoming relation, evidence,
scope, canonical terms, and provided claim. The default Round 1 mapping is one
slot to one sentence. Require a sentence-to-slot trace from the writer and
reject an outline that still says only “report,” “explain,” or “discuss.”

The first sentence of every paragraph except the first must connect to the
preceding paragraph. The last sentence may complete the current claim or make
the next need visible, but it must not be a detached handoff sentence whose
connection is left for the next paragraph to invent. The next paragraph's first
sentence must carry the transition and state its own responsibility.

Gate: reading only the first sentence of each paragraph and the
sentence/logic-level node rows gives a compact,
understandable account of what the subsection does and how it progresses. The
first sentence of each noninitial paragraph names the smallest needed incoming
endpoint and states the paragraph's own responsibility. Apply this test
especially strictly to Introduction, Motivation, and other sections before
Design, then rerun it after semantic rendering and final English polish.

### Stage 2.5: presentation organization

When the story spine is sound but the current prose or outline is difficult to
follow, run the [presentation organization gate](presentation-organization-workflow.md)
before sentence rendering. Reconstruct the presentation graph independently
from the prose. Do not assume that a correct story makes the current paragraph
grouping or sentence order correct.

For each defect, consider merge, split, reorder, relocate, delete, and rewrite
moves. Make the paragraph's central subject or operation appear early in its
opening; carrying the previous endpoint does not justify burying that subject
in the final clause. Treat unresolved sentence relations, list-like sibling
paragraphs, bridge-only units, repeated handoffs, and overloaded openings as
presentation findings that require organization repair.

If the story, claim strength, evidence, terminology, and section responsibility
remain unchanged, apply a presentation-only organization change within the
authorized scope and update the outline change log. If any of those substantive
interfaces change, stop for author alignment. Do not patch a presentation graph
failure with extra connectives or defer it to Round 3 language polishing.

Gate: the target paragraph and sentence organization is explicit, each opening
states its responsibility with the central concept early, and a blind reader
can recover the intended path without the writer's explanation.

### Stage 3: sentence realization contract and concept flow

Before any writer call, use the [sentence-level realization contract](sentence-realization-contract.md)
as a dry run with no manuscript prose. For every slot, write one concrete
proposition, reader question, incoming relation, evidence, scope, canonical
terms, provided claim, and allowed merge. Identify the argument-node IDs it
renders, its source (`from`), required evidence (`needs`), and its relation to
the preceding sentence (`link` or `transition`). For every adjacent pair,
name the concrete endpoint carried forward and the supported relation. If the
endpoint is not recoverable, or a row says only “report,” “explain,” or
“discuss,” repair the outline before writing. A sentence cannot silently
introduce an argument node absent from the aligned outline.

For every concept, operation, input, or output that later reasoning depends on,
check its first substantive use, prerequisite, and abstraction layer. The
surrounding prose must make its role, input or source, purpose, and effect
recoverable before the dependent claim. A concept can be locally explained and
still be premature when its meaning comes from a later representation layer.
Use the canonical terminology ledger and preserve intentional distinctions.

Record a sentence-load check for each contract. A sentence should normally
carry one main relation and only the concepts needed to express that relation.
Split a sentence when it combines an observation, a caveat, and a new
requirement, or when the reader must retain several independent causal steps.
Do not hide a missing relation by packing more clauses into the sentence.

Gate: the complete ordered slot list alone recovers the subsection's argument;
each paragraph has a declared incoming and outgoing endpoint; every slot has a
concrete proposition and supported relation; the terminology ledger covers all
required lexical items; no dependent concept is premature; no proposed
lower-level term appears before the operation or requirement it serves; no
claim has a dangling or ambiguous edge; every sentence pair has a recoverable
logical relation; and no sentence carries more conceptual load than its
contract requires. Only this passing contract can enter claim-flow
materialization. Rerun it whenever outline structure or claims change.

### Stage 4: subsection flow and abstraction

Run the [subsection flow and abstraction workflow](subsection-flow-workflow.md)
before rendering claims into prose. Compile each subsection's local question,
opening purpose, incoming endpoint, owned concepts, abstraction level, outgoing
endpoint, and transition mode. Check that a subsection opening states its
responsibility instead of repeating the preceding handoff. Check that a
representation alias is not promoted to a named concept without a later
distinction or use, and that every clause has a current or downstream
reader-facing job.

For a central object, check that the opening states its purpose or operation
before describing what the system stores, keeps, or records. Select an active
relation from the applicable domain profile when the text describes what one
object does to another. The index profile may require tracking or mapping;
other profiles may require a different relation. Do not turn an example verb
into a generic vocabulary rule.

Select the supported information hierarchy for the subsection. A common Design
sequence is responsibility or contract, supported operation, structure or
policy, implementation detail, and consequence or tradeoff. Keep alternative
structures after the operation or requirement they serve. Remove bridge-only
sentences when the next opening already carries the purpose. When two
paragraphs are sibling alternatives, mark their common parent and use a
parallel-alternative or contrast relation in the second opening. Keep
supporting mechanisms, caveats, and examples on their declared side branches.

Gate: the first sentence of each subsection identifies its object and purpose,
the paragraph openings recover the local progression, abstraction levels do not
jump without a supported relation, and no unnecessary term or clause remains.

### Stage 5: claim rendering and tension

Run the focused [claim rendering workflow](claim-rendering-workflow.md) before
semantic prose rendering and final English polishing. Apply it to comparisons, design tradeoffs, core
claims, paragraph openings, and first figure mentions rather than mechanically
to every sentence.

For a comparison, record the shared question and align the alternatives on the
same outcome and path axes. The prose should expose the tension at that level,
such as one option keeping matching queries fast while recovering slowly
and another recovering quickly while slowing matching queries, when the supplied
evidence supports that contrast. An operation or mechanism can explain the
effect, but should not replace the effect the reader needs to understand; use
an access-path description only when the comparison question is about that
path.

For a tradeoff, trace both benefit and cost to the design choice or mechanism
that produces them. Record the workload or configuration that conditions the
net effect. Avoid making a benefit such as fast recovery the grammatical cause
of a separate query-path cost, and avoid describing a cost as shifted unless
the evidence supports a transfer.

For each noninitial paragraph, render the incoming endpoint, the relation to
that endpoint, and the paragraph's own responsibility in its opening sentence.
For a problem-to-design boundary, state the pressure and purpose that motivate
the design. Reuse the canonical term during this pass, and keep a figure's
first source clause next to the core claim it explains.

Gate: comparisons use a recoverable common frame, core effects are visible,
causal sources are accurate, paragraph openings carry their purpose, and no
new technical term or detached figure reference was introduced.

### Stage 5.5: claim-flow materialization plan

Read the complete ordered semantic graph before writing any paragraph. The
graph, rather than the source prose or a locally plausible sentence, is the
writing target. Apply the [claim-flow materialization workflow](claim-flow-materialization-workflow.md)
to compile one paragraph contract per paragraph. Each contract records its
responsibility, incoming endpoint and relation, ordered node IDs, evidence and
scope, canonical terms, outgoing endpoint, and the next paragraph's required
input.

Materialize paragraphs in outline order. For each paragraph, provide the writer
with its contract, the last passing endpoint from the preceding paragraph, and
the next paragraph's required input. Verify the paragraph independently before
starting the next one. A paragraph may split or combine sentences for clarity,
but it may not add a claim, object, evidence item, causal edge, technical term,
or implementation detail. If the contract cannot be rendered naturally, return
to the graph or outline instead of inventing a transition.

After all paragraphs pass locally, read only their openings and endpoints to
verify the subsection-level migration. Repair a boundary sentence only when
the graph is unchanged. Any changed node order, paragraph responsibility,
abstraction layer, or edge is an outline delta and returns to alignment.

Gate: every paragraph materializes its assigned nodes in order, preserves its
incoming and outgoing interfaces, and passes the local contract check; the
complete subsection passes the opening/endpoint migration check; and the
prose graph remains equivalent to the frozen claim graph.

### Stage 6: semantic prose rendering

Only after the preceding gates pass, render the contracts into simple, direct
prose one paragraph at a time in outline order. A sentence may contain an
essential subordinate clause, but it should
normally carry one main logical relation. Split a sentence when it combines
multiple new concepts, several causal steps, or nested qualifications that a
reader must hold at once. Remove stacked nouns, unnecessary subordinate
clauses, and abstract filler. This is semantic rendering, not the final
English copyedit: preserve the aligned claims, transitions, and terminology
while making their relations readable. Do not optimize a readability score at
the cost of a missing condition or weakened claim.

Do not repair a missing concept with a defensive sentence such as:

```text
We define X as X.
X is <a restatement that gives no role or purpose>.
```

Introduce ordinary concepts through the sentence that uses them: state what
the operation does, what it acts on, or why it is needed. A standalone
definition is justified only when the paper introduces a central named
abstraction, formal notation, invariant, or boundary that the rest of the
paper repeatedly depends on. Even then, give the concept's purpose and role,
not only a tautological category.

Prefer a purpose-bearing subject and a concrete relation over an outline slot
rendered as a generic noun phrase. When the active profile is `logical-interface`
and the supported relation is indexing, say that the index tracks or maps the
relevant objects before describing their representation. Avoid passive or
nominal phrases such as “recorded sequences” when they hide the relation.
Avoid wrappers such as “generally implement these operations with”
when the claim can directly state which already introduced structures existing
systems use. Do not add a representation or a structure just to make an
abstract sentence sound concrete; return to the concept-layer stage if that
detail is needed.

Gate: a reader can follow every sentence on one pass, no sentence carries
unnecessary conceptual load, each opening states the relevant purpose before
the central object, and every new term is introduced naturally at the correct
abstraction layer. The logical structure and semantic relations are stable
enough for a later language-only pass.

### Stage 7: evidence, terminology, and figures

Bind claims to their evidence after the prose structure is stable. Check that
figure and table observations use sentence-initial source clauses, metric
paragraphs state what the metric means or why it is reported before giving
numbers, and the active Evaluation structure and claim–evidence matrix remain
visible. Evaluation breakdowns follow Design order while stating benefit, cost,
and workload/configuration-dependent net effect. For a design-centered
performance breakdown, also verify that the proposed-system result precedes
attribution, the breakdown purpose is explicit, baselines remain concise
comparison anchors, and unrelated operations or implementation details were
not retained. Check the terminology ledger
across prose, headings, captions, labels, tables, and figures.

Gate: every quantitative or visual claim has a nearby source and scope, every
metric is oriented before its result, and each recurring concept has one
canonical form.

### Stage 8: final English polish

Run this pass only after the structural, concept-flow, claim-rendering,
evidence, terminology, and figure gates pass and the integrated revision has a
fixed version. Improve English expression without reopening the argument:
grammar, articles and prepositions, idiomatic wording, sentence length,
parallelism, pronoun antecedents, and transitions within and between
paragraphs. Reduce repetitive or mechanically stacked connectives such as
`because`, `therefore`, and `however` when the replacement preserves the
supported relation. Do not add or remove a claim, concept, evidence item,
mechanism, qualifier, figure/table source clause, metric purpose, or section
handoff. A shorter sentence or a split sentence is allowed when it preserves
the same contract. Do not introduce stylistic synonyms for a canonical term.

Gate: the English is natural and concise, sentence and paragraph transitions
remain explicit, and a contract diff shows no semantic or structural change.

### Stage 9: independent verification

Read the integrated manuscript without the writer's plan and reconstruct:

1. the paper-level story and its supported edges;
2. the section and subsection hierarchy;
3. the first-sentence-only subsection summary;
4. the subsection abstraction order and boundary ownership;
5. the paragraph and sentence handoffs;
6. the first-use map for concepts and terms; and
7. the claim-rendering checks for comparisons, tradeoffs, openings, and figure
   anchors; and
8. the evidence and figure bindings; and
9. the semantic equivalence of the final English-polish pass.

Compare these reconstructions with `story.md` and the fixed section outlines.
Any mismatch is an outline or story change, not a wording preference. Run a
final simplicity scan only after these structural comparisons.

## Narrow-pass rules

- A story pass must not solve a sentence-style problem by adding Design detail.
- An architecture pass must not rewrite prose merely because a sentence sounds
  awkward; record the structural cause first.
- A sentence-flow pass must not introduce a new claim or change section
  responsibility.
- A subsection-flow pass must not invent a purpose, promote a one-use
  representation into a concept, or use a transition to make an unsupported
  factual claim.
- A claim-rendering pass should sharpen the visible effect or tension without
  changing the comparison frame, causal source, claim strength, or scope.
- A semantic prose pass must not add standalone definitions, generic
  transitions, or new evidence. It may use an essential subordinate clause,
  but should split sentences that carry several independent logical relations.
- The final English-polish pass must not reopen story, structure, claim
  rendering, evidence, terminology, or figure decisions. If its wording
  change would alter one of those, return the issue to the earliest affected
  stage instead.
- A terminology pass must not rename a concept unless the outline and all
  dependent contracts are updated.
- A verification pass must inspect the full requested scope, but it should
  report the earliest failed stage so the next iteration can be narrow.

## Iteration policy

For prose-bearing work, the pipeline has three named rendering rounds after
the outline is aligned. Run the [iterative prose refinement workflow](iterative-prose-refinement.md):

1. **Claim-flow materialization and semantic rendering:** materialize the
   aligned claim graph paragraph by paragraph, then split overloaded sentences
   without changing the argument.
2. **Presentation and logic repair:** independently review transitions,
   paragraph branches, sentence load, redundancy, concept layers, and unknown
   terminology, then revise only supported defects.
3. **Concise English polish:** improve idiomatic English after the presentation
   gate passes, without reopening structure or claim decisions.

Each round has its own input and output version, findings, acceptance
conditions, and gate. Once the outline and edit authorization are aligned,
manual and automatic modes both run the rounds in order. Manual mode pauses
only when a round exposes an author decision; it does not require the author to
trigger each wording round. A `draft-only` request explicitly stops after
Round 1. The final language round is still followed by independent
verification; no language pass proves that the presentation remains aligned.
Stop with `Needs context` when a gate depends on missing evidence or an author
decision; do not smooth over the gap with a new definition, transition, or
stronger claim.
