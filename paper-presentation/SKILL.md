---
name: paper-presentation
description: Orchestrate academic-paper presentation review, guided paragraph generation from an author story map, story discussion, section-responsibility audits, terminology and subsection audits, figure planning, structural revision, final-manuscript visual QA, and independent verification. Use for manual review/revise workflows or automatic iteration of systems-paper presentation while preserving technical meaning and evidence. Delegates detailed checks to paper-presentation-review, paper-presentation-revise, and appropriate figure workflows. Excludes scientific correctness review, new experiments, and acceptance prediction.
---

# Paper Presentation Orchestrator

Coordinate the companion presentation reviewer and writer so the manuscript's
story, argument structure, transitions, and prose are improved in a controlled
loop. This skill owns mode selection, version handoffs, iteration, and stopping
conditions. It does not decide whether the research is correct, novel, or
accepted.

## Required inputs and shared standard

First read the [rule activation workflow](references/rule-activation-workflow.md)
and create its active-context card. Load the small always-on core, then load
only the conditional profiles triggered by the requested section, subsection
archetype, pipeline stage, and mode. Conditional loading keeps the full quality
standard while preventing unrelated domain rules and examples from competing
with the current task. If revision changes the scope or archetype, recompute
the card and load the newly triggered profile before continuing.

Always load [paper-presentation-review](../paper-presentation-review/SKILL.md),
[paper-presentation-revise](../paper-presentation-revise/SKILL.md), the shared
[presentation criteria](../paper-presentation-review/references/criteria.md),
the [fixed outline workflow](references/project-outline-integration.md), and
[the argument-node outline workflow](references/argument-node-outline-workflow.md),
[the semantic object and logic graph workflow](references/semantic-object-graph-workflow.md), and
[the structured outline refinement workflow](references/outline-refinement-workflow.md), and
[the sentence-level realization contract](references/sentence-realization-contract.md), and
[the hierarchical outline research workflow](references/hierarchical-outline-research-workflow.md), and
[the local paragraph review and revision workflow](references/local-paragraph-review-revise-workflow.md), and
the [coarse-to-fine refinement pipeline](references/refinement-pipeline.md).
Load the [paragraph opening workflow](references/paragraph-opening-workflow.md)
for every prose, outline, guided-generation, or structure task. It is a
required gate, not an optional polishing suggestion.

Load the [frozen prose-round contract](references/prose-round-contract-workflow.md)
for every prose-bearing automatic, guided, or multi-round revision. It freezes
the render target and requires an independent round-trip diff before the next
round.
Load the [claim-flow materialization workflow](references/claim-flow-materialization-workflow.md)
after the semantic graph and paragraph contracts are aligned and before prose
rendering. It makes the claim flow primary and writes paragraphs sequentially
from their contracts.

Load the [presentation organization gate](references/presentation-organization-workflow.md)
whenever the story is aligned but the prose, sentence relations, paragraph
grouping, transitions, or paragraph openings are under review. Story alignment
does not seal presentation organization. This gate may require merging,
splitting, reordering, relocating, or deleting units before prose rendering.

Load the [reference-material rebuild workflow](references/reference-material-rebuild-workflow.md)
when the author supplies an existing subsection as raw material for a rewrite,
or when no aligned story and outline are supplied for a structurally poor
subsection. This route treats the supplied prose as evidence candidates and
content material, not as the target presentation.

Load the following only when their trigger is present: the [structural
presentation workflow](../paper-presentation-review/references/structure-workflow.md),
[outline-based presentation structure workflow](references/structure-alignment-workflow.md),
[section responsibility workflow](../paper-presentation-review/references/section-workflow.md),
[section presentation playbook](references/section-presentation-playbook.md),
[Evaluation Presentation and Rebuild Workflow](references/evaluation-presentation-workflow.md),
[Design Presentation Patterns](references/design-presentation-workflow.md),
[Motivation Recovery Workflow](references/motivation-recovery-workflow.md),
[systems-paper presentation patterns](references/research-presentation-patterns.md),
[concept–claim logic flow workflow](references/logic-flow-workflow.md),
[claim rendering and tension workflow](references/claim-rendering-workflow.md),
[subsection flow and abstraction workflow](references/subsection-flow-workflow.md),
[presentation organization gate](references/presentation-organization-workflow.md),
[review-to-outline continuation routing workflow](references/continuation-routing-workflow.md),
[section content planning workflow](references/section-content-planning-workflow.md),
[terminology and subsection workflow](../paper-presentation-review/references/terminology-workflow.md),
[guided paragraph generation workflow](references/guided-paragraph-workflow.md),
[parallel section scope workflow](references/parallel-scope-workflow.md), and
[reasoning effort policy](references/effort-policy.md). Use the [iterative
prose refinement workflow](references/iterative-prose-refinement.md) whenever
the story and aligned outline are stable but the rendered prose needs multiple
passes. Use the [presentation
figure workflow](../paper-presentation-review/references/figure-workflow.md)
only for figure decisions, and the [final manuscript visual QA workflow](references/visual-qa-workflow.md)
only when the author explicitly requests a PDF, page-layout, page-break, or
final visual check.

Do not compile or inspect a PDF during ordinary source-level review, revision,
guided generation, figure planning, or automatic iteration. A conditional
profile adds checks and ordering; it never relaxes the core, the paper's
writing guide, or an accepted author decision. The detailed stage descriptions
below are a dispatcher, not a simultaneous checklist. Apply a domain-specific
clause only when its profile is active, and record that choice in the active
context card.
The default interaction protocol is defined in the [review–alignment–revision
workflow](references/author-alignment-workflow.md).
Read applicable `AGENTS.md` files, linked writing guides, the paper's
[glossary](../paper-presentation-review/references/glossary.md), the fixed outline
files for the requested scope, and the complete available manuscript before
making cross-section claims.

Identify the manuscript revision, requested scope, edit authorization, target
venue or paper type when supplied, available evidence, and any author
constraints. Read enough adjacent sections to resolve terminology and
handoffs. For a source excerpt, restrict conclusions to the excerpt.

The default shared state is defined in
[orchestration-contract.md](references/orchestration-contract.md). Keep one
fixed version for each handoff. Do not let a reviewer and writer modify a
moving draft concurrently.

## Default interaction workflow

Unless the user explicitly requests `auto`, or supplies an already aligned
target and edit authorization, use this sequence:

```text
story discussion → author story alignment → hierarchical outline research
→ L0/L1/L2 outline completion → sentence/logic-level human sync view
→ author outline alignment
→ independent structural review → presentation organization → interface freeze
→ parallel Round 1 rendering → integrate
→ Round 2 presentation/logic repair → Round 3 English polish
→ independent verification
```

The story and reader-facing outline are the author's alignment points. Do not
dispatch a prose reviewer or writer for the ordinary author-driven workflow
before those two artifacts are aligned. An explicit `review` request is an
exception: review the supplied manuscript and return findings, but still
route any subsequent rewrite through story and outline alignment when they are
not already fixed.

Author alignment may be coarse. The author can approve a paragraph-level chain
and its major internal relations while the discussion agent completes the
sentence-level propositions. The completed contract, rather than the coarse
input, is what the prose agents receive.

For a story or `discuss` run, use this route by default:

```text
story discussion → story alignment → hierarchical outline research
→ L0/L1/L2 outline synthesis → sentence/logic-level human sync view
→ author outline alignment → independent structural review
→ revision → independent verification
```

If the author supplies only a paragraph-level story or an internal paragraph
chain, outline synthesis expands it into the sentence-level realization
contract. The author may intervene at the paragraph, slot, relation,
terminology, or scope level; the author does not need to write every slot
manually. Run an independent outline review before freezing the contract. Once
it is frozen, hand it to the separate review/revise agents and keep routine
prose iteration automatic unless a substantive decision reopens the contract.

Return the sentence/logic-level human sync view in the same turn as outline
synthesis. It must be projected from the semantic object graph and show every
sentence slot or argument node, its object, role, incoming relation, `needs`,
evidence, transition, and provided claim; a
paragraph-only synopsis does not satisfy outline alignment. The author should
not need to request a separate outline-generation stage.

Before dispatching a writer, expand those nodes into the
[sentence-level realization contract](references/sentence-realization-contract.md).
Every slot must state one concrete proposition, its relation, evidence, scope,
canonical terms, and provided claim. A row such as “report the result” or
“explain the mechanism” is still a topic summary, not a writing contract. Keep
the run at `Awaiting outline alignment` until the rows pass the proposition and
opening tests. Round 1 receives the ordered slots and returns a
sentence-to-slot trace; prose without that trace is not a valid generated
draft.

When the author's input is paragraph-level, run the [hierarchical outline
research workflow](references/hierarchical-outline-research-workflow.md):
research and freeze L0 subsection claim, L1 paragraph claims/interfaces, and L2
sentence propositions in that order. The author may revise any level after the
agent's research pass. Do not let a writer receive L2 without its L0 and L1
parents.

For a source-only rewrite, insert the following route before story alignment:

```text
material audit → independent story recovery → author story alignment
→ outline synthesis → author outline alignment → presentation organization
→ interface freeze → Round 1 rendering → Round 2 presentation/logic repair
→ Round 3 English polish → independent verification
```

When the story is already aligned but presentation is weak, insert
`presentation organization` before interface freeze and Round 1. The gate
must issue a structural finding and target organization when needed; it must
not reduce the problem to local wording edits.

When the user directly requests review or revision of one paragraph or a small
contiguous paragraph scope, activate the [local paragraph review and revision
workflow](references/local-paragraph-review-revise-workflow.md). Compare the
paragraph with the old outline, but do not block the local review because the
outline is stale. Reconstruct only the local contract when the shared
interfaces remain unchanged; route an incoming or outgoing interface change to
outline alignment.

When Evaluation is in scope, run the [Evaluation Presentation and Rebuild
Workflow](references/evaluation-presentation-workflow.md) and its [Evaluation
Patterns from Systems Papers](references/evaluation-reference-patterns.md) after story and
outline alignment and before interface freeze or prose rendering. It recovers
the Evaluation-level progression, selects the local subsection archetype,
separates source/design/figure/narrative order, and freezes the claim–evidence
matrix. In a source-only rewrite, its material audit runs before target-outline
synthesis. A valid old result or figure sequence does not replace this
reconstruction.

The old subsection is immutable reference material on this route. Its facts,
scope conditions, and evidence candidates are audited; its wording, paragraph
boundaries, order, transitions, and local terminology are not inherited by
default. Do not dispatch a writer from the old prose alone.

Apply this workflow through the staged refinement pipeline: Motivation
recovery, story and claim spine, section/subsection architecture, paragraph and
argument-node outline, sentence and
concept flow, subsection flow and abstraction, claim rendering and tension,
simple clear prose,
evidence/terminology/figures, and final independent verification. Each stage uses a narrow
discussion or `review → align → revise → verify` loop as appropriate. Story,
section architecture, and the structured outline use discussion and author
alignment first; prose review and revision begin only after the story and
outline gates pass. Do not send prose to a later stage until the earlier stage's
gate passes.

In an explicit review request, the first response is read-only: return located
findings, acceptance conditions, target outline delta or paragraph repair map,
and the decisions that need author alignment. In the ordinary author-driven
workflow, the first response is the story discussion and structured-outline
proposal, not a prose review. In both cases, record the author's follow-up in
the fixed outline before dispatching any writer. When the author replies to
those findings or to the proposed story/outline, apply
the [review-to-outline continuation routing workflow](references/continuation-routing-workflow.md):
record the response as explicit decisions, then automatically synthesize and
present the structured outline and sentence/logic-level human sync view if the author has
not supplied a complete one.
Set `Awaiting outline alignment` and do not dispatch a writer until the
reader-facing hierarchy, order, paragraph roles, and handoffs are aligned. Do
not silently turn a review request into an edit, and do not make a structural
or claim-framing decision merely because it would make the prose smoother.

Review is a hard barrier before revision. When delegation is available, run
`paper-presentation-review` in a separate reviewer call or sub-agent and keep
the manuscript read-only. The writer receives the immutable review artifact,
not a moving reviewer draft. If delegation is unavailable, run review and
revision as separate sequential calls with a fixed version and a clean review
state. Never ask the same writer call to review and revise its own text and
count that as independent review.

After revision and patch integration, dispatch a fresh verification call or
sub-agent with the integrated manuscript, canonical outline, argument-node
execution view, and acceptance conditions. Do not pass the reviser's process
explanation or self-check as evidence. The verifier reconstructs the final
argument-node graph and independently checks the reviewer conditions.

Once the author has aligned the story and reader-facing outline and authorized
writing, prose refinement continues through all three named rounds by default,
including in a manual discussion workflow. Pause only when a round exposes a
new story, claim, hierarchy, terminology, evidence, or scope decision. A user
may explicitly request `draft-only` to stop after Round 1, or may request a
different finite round limit.

Round 1 is paragraph-granular within each subsection. Generate, verify, and
commit one paragraph before generating the next. A full subsection is never
passed to a writer as an unconstrained one-shot drafting task. Parallelism is
reserved for independent subsections whose incoming and outgoing interfaces
are already frozen.

One orchestrator session owns this sequence. It may dispatch review agents in
parallel, but it must complete and freeze the review artifact before dispatching
any writer. After story and outline alignment, it freezes subsection interfaces
derived from the exact fixed outline revision, and may dispatch independent
subsection revision agents in parallel from the same manuscript version. It
serializes outline changes, interface changes, patch merging, and final
section-level verification; a worker must not silently redefine a shared edge
or edit a moving canonical draft. Ask the author only when a substantive
decision, missing fact, or unresolved conflict prevents a faithful repair.

## Modes

Select the mode from the user's request. Do not silently switch a manual mode
to automatic editing.

### `review`

Run `paper-presentation-review` on the requested scope. Return located
findings, acceptance conditions, and a target outline delta when structure or
story is defective. Keep the manuscript read-only. This mode is appropriate
for "review the presentation," "find story problems," and verification of an
existing revision. For a single paragraph or small contiguous scope, use the
local paragraph route: review the paragraph even if the fixed outline is stale,
and return its reverse outline, interface findings, and smallest outline delta
instead of stopping at the stale-outline diagnosis.

### `revise`

Run `paper-presentation-revise` on the authorized scope using the supplied
findings, fixed-outline subtree, target map, or user instructions. Load the
fixed outline and its current revision first. If the outline is a proposal,
stale against the manuscript, or structurally contradicted, produce an outline
delta and stop for whole-scope structural edits before making them unless the
user explicitly supplied a complete target and edit authorization. For a direct
paragraph or small contiguous-scope request, use the local paragraph route:
rebuild only the local contract when the shared interfaces remain unchanged and
proceed with the authorized local rewrite. A changed incoming or outgoing
interface still returns to outline alignment before neighboring claims change.
Return the revised artifact, outline revision/status, issue-to-change map,
outline-change map, and unresolved items. This mode may edit files only when
the user has authorized manuscript edits. Once the outline and edit
authorization are aligned, this mode runs the three named prose refinement
rounds by default. Use `draft-only` only when the user explicitly requests the
Round 1 semantic-rendered draft without later presentation repair or English
polish.

This mode requires an independent review artifact bound to the exact input
version, unless the author explicitly supplies a complete current review with
acceptance conditions. If that artifact is absent or stale, run review first;
do not let the writer infer its own review findings while revising.

If the request supplies only a poorly written subsection and describes it as
reference material, route it to `rebuild-from-material` before any prose edit.
The route returns a material ledger and independently recovered story first;
it does not treat the source paragraph order as a target.

If the story is already aligned but presentation is weak, run the presentation
organization gate before the three prose rounds. A writer may make
presentation-only merges, splits, reorders, relocations, and deletions within
the authorized scope. Pause only if the change affects story, claim strength,
evidence scope, terminology, section responsibility, or a shared interface.

### `rebuild-from-material`

Reconstruct a subsection from a poor source draft while preserving supported
meaning and evidence. Read the [reference-material rebuild workflow](references/reference-material-rebuild-workflow.md).
Keep the source immutable, classify its units by authority and disposition,
recover the story independently, and present the story for author alignment.
After story alignment, synthesize and present a new structured outline and its
sentence/logic-level human sync view. Only
after outline alignment and edit authorization should the writer render prose
from the material ledger and the approved contracts. Then run the three named
prose rounds and independent verification. This mode is the default internal
route for “rewrite this subsection; use the old version as reference” and may
be selected explicitly by the author.

The first response in a manual run is read-only and contains the material
ledger, source-order warning, recovered story, candidate alternatives, and
open decisions. It must not be a lightly edited version of the source. A
writer may consult the raw source for evidence lookup, but the Round 1 trace
must be contract-to-material, not sentence-to-sentence.

### `discuss`

Review the story and generate a small set of supported outline options. Load
the fixed outline using the [fixed outline workflow](references/project-outline-integration.md)
before generating options. Treat it as the baseline and return an outline
delta or a proposal rather than an unstructured replacement. Preserve its
paragraph and sentence IDs, roles, `from`, `needs`, and `link`/`transition`
fields.
When an option is mature enough for author synchronization, first build the
semantic object and logic graph, then compile its argument-node execution view
sentence/logic-level human sync view, and sentence-level realization contract.
The
sync view must show every sentence slot or logical node, role, evidence
relations, conditions, `from`, `needs`, `link`/transition, and handoffs without
exposing internal metadata. A paragraph-only summary is a planning note, not
an outline ready for author alignment.
For each slot, the author-facing projection must also state the concrete
proposition, reader question, relation, evidence, scope, canonical terms, and
provided claim. Do not return a slot that says only “report,” “explain,” or
“discuss.” Run the proposition and opening tests before returning the option.
When the supplied outline is coarse, complete the missing slot propositions and
relations in this pass. Do not ask the prose writer to perform that expansion.
Return the L0/L1/L2 hierarchy and the outline-review findings together, so the
author can change the correct level without reading a prose draft.
Before returning any option, run the [structured outline refinement
workflow](references/outline-refinement-workflow.md): semantic graph
construction, independent graph/lexical review, and author-facing projection.
For structure discussion, read the [systems-paper presentation patterns](references/research-presentation-patterns.md).
Extract presentation invariants first; transfer a source-paper reasoning
pattern only when the target manuscript has the same dependency relationship.
Never copy a source paper's visible section order as a template.
For Motivation discussion, run the [Motivation Recovery Workflow](references/motivation-recovery-workflow.md)
and present the recovered design-independent opportunity separately from any
naive-solution or proposed-design chain. For Evaluation and other sections,
use the [section presentation playbook](references/section-presentation-playbook.md)
to compare supported pattern options.
When the author provides only a high-level direction for a section and no
complete reader-facing outline, also load the [section content planning
workflow](references/section-content-planning-workflow.md). First recover the
section purpose, then propose supported content dimensions, categories,
representative evidence or citations, paragraph responsibilities, argument
nodes, and handoffs. For Related Work, organize by the comparison dimensions
that position the paper; do not default to a paper-by-paper list. This is a
planning pass inside `discuss`, not a new user mode and not a prose draft.
For each option, state the section and subsection hierarchy, opening question,
paragraph or section sequence, local responsibility of every unit, argument
nodes and their relations, incoming and outgoing handoffs, causal links,
evidence mappings, what moves, and what information must remain. Persist these
options in the fixed outline's
proposal/change-log area. Story agreement alone is not outline agreement: keep
the run at `Awaiting outline alignment` until the author selects or adjusts the
grouping, order, and handoffs. Do not dispatch prose writers from a proposed
story graph or an unaligned outline.
Explain the tradeoff between the options and identify the decision that only
the author can make. Do not edit the manuscript until the user selects or
adjusts an option. Use this mode for discussion of the story, motivation,
contribution framing, section content, section order, or a major presentation
change. If the author has only provided a direction, stop at `Awaiting outline
alignment` after returning the detailed content plan and synchronized outline
views; do not dispatch review or prose writers yet.

When discussion is split across agents, give every agent a fixed input version,
exclusive analysis scope, adjacent read-only context, and the shared section
contract. Treat all outputs as proposals and merge them through one
coordinator before any revision.

### `sections`

Audit the responsibilities of the requested sections without editing. Read
the section presentation playbook and select a supported pattern for each
section. When Motivation and Design are in scope, run Motivation Recovery first:
record its high-level problem, observations, pressure, opportunity,
design-independent insight candidates, requirements, and leakage map before
mapping Design choices back to that contract. Use this mode when the user is
deciding what Motivation, Design, Evaluation, or adjacent sections should
accomplish.

### `figures`

Audit the requested scope for missing, misplaced, redundant, or unsupported
figures. Decide whether each candidate is `required`, `beneficial`,
`unnecessary`, or `blocked`. For selected figures, return a figure brief with
the reader question, first placement, role, entities, relationships, visual
encoding, caption takeaway, source inputs, and rendering route. Do not edit the
manuscript or draw a final artifact unless figure generation is authorized.

### `visual-qa`

Run the [final manuscript visual QA workflow](references/visual-qa-workflow.md)
only after the author explicitly requests a rendered-artifact or PDF check.
Inspect the bound PDF or rendered pages for page breaks, headings,
paragraph/column continuations, figure and table placement, captions,
equations, and other layout effects that change reader comprehension. Return
located visual findings and source locators when available. Do not silently
compile or open a PDF in another mode. Do not make source or layout edits
unless they are explicitly authorized. A visual QA pass is an additional
post-manuscript gate and does not replace source-level review or verification.

### `terms`

Build or audit the terminology ledger for the requested scope, seeded from the
paper's glossary. Return the canonical term, definition, allowed forms, accidental variants, and nearby
concepts that must remain distinct. Also audit subsection openings and
handoffs for local independence. For each needed concept and operation, check
its first substantive use for a short operational orientation: role, input or
source, purpose, and effect. Flag bare nouns and defensive `we define X as X`
sentences. Do not edit the manuscript in this mode.
Surface author decisions when two forms may represent different concepts.
Return proposed glossary lines for every term decision the author must make.

### `guided`

Turn an author-supplied paragraph map into publication-ready prose. Read the
guided paragraph generation workflow, the outline-based presentation structure
workflow, and the fixed outline workflow. Validate the supplied roles,
paragraph order, incoming and outgoing relations, evidence mapping, and scope
conditions against the exact outline subtree. If the proposal conflicts with
the outline, report an outline delta and stop for alignment rather than
silently choosing one. Only then render one paragraph contract at a time and
run the three named prose refinement rounds by default. Do not silently
redesign the story, invent missing evidence, or use later Design details to
strengthen Motivation. Return the outline path/revision/status, generated
scope, paragraph-contract trace, unresolved context, iteration history, and
the round-trip graph and reverse-outline checks. Use `draft-only` only when the
user explicitly requests the Round 1 semantic-rendered draft. Independent
verification remains part of the default three-round flow.

### `auto`

Run the finite review-revise-verify loop below. Use this mode when the user
asks to automatically improve, iterate, polish, or generate a presentation-ready
systems paper. Automatic mode can make authorized manuscript edits. If edit
authorization is absent, produce a proposed revision or patch and stop before
writing the manuscript files.

If the user gives an iteration limit, honor it. Otherwise use the three named
   rounds in the [iterative prose refinement workflow](references/iterative-prose-refinement.md)
   and the [frozen prose-round contract](references/prose-round-contract-workflow.md)
for prose improvement: semantic rendering, presentation/logic repair, and
concise English polish. These are different gates, not three generic rewrites.
   Report each round and its gate result. Before the first writer call, freeze
   the render-contract revision, protected node/edge/lexical IDs,
   paragraph-opening matrix, and round change budget. A later round may not
   silently reopen an earlier structure decision or use the preceding prose as
   its new outline.
Automatic mode ends with source-level verification. It does not compile, open,
or inspect a PDF. Run `visual-qa` separately when the paper is complete and the
author requests final layout review.

## Automatic loop

For a prose-bearing automatic run, initialize an iteration plan before the
first writer call. The plan records `iteration_id`, the fixed outline revision,
the round limit, the round-specific goal, and the gate that permits the next
round. Run the [iterative prose refinement workflow](references/iterative-prose-refinement.md)
and the [frozen prose-round contract](references/prose-round-contract-workflow.md)
as the round controller. The ordinary stage pipeline remains the source of the
checks within a round; the iteration controller determines which checks are
active and when a later round is allowed.

1. **Select the active rule profile.** Before reading detailed guidance,
   classify the scope, section, subsection archetype, pipeline stage, and mode
   with the [rule activation workflow](references/rule-activation-workflow.md).
   Record the active and inactive profiles and the reason for each selection.
   Keep this card fixed for the round. Recompute it if the selected outline or
   subsection responsibility changes.
2. **Intake and baseline.** Bind the original manuscript, writing guide,
   scope, evidence, and constraints to a version identifier or content hash.
   Record missing inputs and the checks they prevent. Select the effort profile
   from [the reasoning effort policy](references/effort-policy.md); use `high`
   by default, promote structure search and independent verification to
   `xhigh` when the policy triggers, and lower only stable local rewrites.
   When the runtime supports per-call effort, pass the selected value to the
   delegated phase and record it in the round ledger.
   If work is split across agents, freeze the version and create a scope
   manifest with disjoint owned units, read-only boundary context, shared
   edges, and one coordinator before dispatching any worker. Read the fixed
   outline index and exact section files for the requested scope. Compare the
   outline revision and named manuscript version with the input artifact;
   report drift before reusing it. Do not search for alternate outline files.
   If the requested subsection is supplied as a poor source draft without an
   aligned target, activate `material-rebuild`: freeze the source snapshot,
   build the material ledger and disposition map, and recover the story
   independently before binding a target outline. In a manual run, stop at
   `Awaiting story alignment`; in an authorized automatic run, record the
   selected story and rationale. Never use the source paragraph order as the
   default target.
3. **Bind the fixed outline and author blueprint.** Import the exact outline
   subtree with its paragraph, argument-node, and sentence contracts before
   drafting.
   If the user supplies paragraph roles, paragraph order, or a logic map, read
   the guided paragraph generation workflow and the outline-based presentation
   structure workflow. Treat the map as an outline delta until its
   grouping, hierarchy, order, handoffs, sentence roles, `needs`, `from`, and
   evidence mappings are validated against the fixed outline. Do not let a
   correct story graph silently approve a conflicting presentation structure.
   If the fixed outline lacks the requested scope, stop with `Needs context`
   in ordinary revision. In `rebuild-from-material`, the fixed root and index
   remain mandatory, but the missing subsection may be synthesized there as a
   `proposal` after story alignment; do not search another directory or use
   the source prose as its replacement.
   When the author has aligned only a story, paragraph chain, or internal
   paragraph logic, synthesize and independently review the argument-node
   execution view, sentence/logic-level human sync view, and sentence-level
   realization contract before dispatching any reviewer or writer. Keep the
   run at `Awaiting outline alignment` until
   the author aligns the grouping, node order, relations, and handoffs.
   If the author supplied only a high-level section direction, activate
   `section-planning` and the [section content planning
   workflow](references/section-content-planning-workflow.md). Generate the
   section purpose, supported content dimensions or categories, argument
   nodes, evidence and citation needs, paragraph responsibilities, and
   handoffs before prose. In an authorized automatic run, select a target only
   when one supported organization is clearly preferable and record the
   rationale in the outline; otherwise stop at `Awaiting outline alignment`.
   If `auto` is authorized and the story or outline is missing, run the
   [structured outline refinement workflow](references/outline-refinement-workflow.md)
   before any prose review or revision. Automatic selection may resolve only
   presentation choices that do not change the paper's claim or scientific
   emphasis; otherwise preserve the alternatives and stop for author context.
4. **Motivation recovery and section contract pass when triggered.** When the
   active card includes Motivation or a cross-section Motivation–Design
   dependency, read the [Motivation Recovery Workflow](references/motivation-recovery-workflow.md)
   and the [section presentation playbook](references/section-presentation-playbook.md).
   For Motivation, first extract the setting, observations, pressure,
   opportunity, design-independent insight candidates, requirements, and
   leakage map without using Design details. Record the allowed Motivation
   abstraction level and the first-use order for concepts. Apply an abstraction
   firewall: a proposed representation, encoding, identifier, data structure,
   algorithm, or component remains in Design even if it can be explained
   locally. Classify any naive solution or proposed mechanism separately and
   place it in the Design chain. Select a supported presentation pattern for
   each section in scope. Only after the
   Motivation contract is stable, extract the paper's full question, problem,
   insight, design promises, and evaluation claims, then map Design choices
   back to the contract. Stop with `Needs context` or `Awaiting alignment` if
   the story depends on an implementation detail, if multiple motivation ideas
   remain equally supported, or if a major design choice has no prior
   requirement.
   When the active card includes Design, consult the [Design Presentation
   Patterns](references/design-presentation-workflow.md) while discussing the
   story and synthesizing the structured outline. Select a supported
   reader-facing pattern only when the Design dependency graph needs one, and
   record the selected pattern, node order, component responsibilities, and
   relevant consequences in the outline. This is part of story/outline
   alignment, not a separate Design stage. Do not impose a storage, layout, or
   update sequence when the selected Design pattern does not require it.
   When the active card includes Evaluation, also run the [Evaluation
   Presentation and Rebuild Workflow](references/evaluation-presentation-workflow.md).
   Recover the Evaluation-level progression, classify the local subsection
   archetype, separate the four orders, and build the claim–evidence matrix
   before paragraph rendering. For source-only material, keep the old order as
   source locators only. If the proposed target order matches the source order,
   record the evidence or dependency reason in the outline.
5. **Architecture and outline pass.** Run the review skill and consult the
   systems-paper presentation patterns. Validate section/subsection order,
   local questions, responsibilities, and cross-section handoffs against the
   fixed outline. Compare only supported alternatives and write any selected
   change to the fixed outline. In manual runs, stop with `Awaiting outline
   alignment`; in automatic runs, record the selected alternative and its
   rationale in the outline.
   If the story is sound but the current prose or outline is hard to follow,
   run the presentation organization gate before paragraph rendering. A
   correct story does not make the current grouping, sentence order, or
   openings authoritative.
   For Evaluation, the target outline also records the selected macro
   progression or local archetype, narrative order, claim–evidence bindings,
   and source-unit dispositions before a writer is dispatched. When the local
   archetype is a design-centered performance breakdown, it also records the
   proposed design as the focal subject, the headline result before
   attribution, the breakdown purpose, baseline compression, and the relevance
   decision for each operation or implementation detail.
5a. **Semantic object and logic pass.** Before deriving sentence slots, read
   the [semantic object and logic graph workflow](references/semantic-object-graph-workflow.md).
   Type the concepts, claims, evidence, purposes, mechanisms, results, costs,
   conditions, metrics, and handoffs in the aligned outline. Require a
   supported purpose or question edge for every Design mechanism or Evaluation
   metric/result, and require evidence or an explicit reasoning basis for every
   claim. Extract all technical nouns, noun phrases, adjectives, adverbs,
   verbs, and relation words into the lexical audit. A technical modifier must
   have a property, comparison axis, scope, and support; an unproven or
   untracked lexical item is a graph finding or `Needs context`, not a wording
   choice. Keep the run at `semantic_graph` until this gate passes.
6. **Paragraph-flow pass.** Read the [paragraph opening workflow](references/paragraph-opening-workflow.md)
   and compile its paragraph-opening matrix from the aligned outline subtree.
   For each paragraph record its incoming endpoint, supported relation, local
   responsibility, opening claim, provided claims, outgoing endpoint, and
   before-Design or Design boundary. Apply the first-sentence-only test before
   drafting or rewriting: reading only the paragraph openings must recover the
   subsection's high-level framework and progression, especially before
   Design. Require every noninitial opening to carry the smallest concrete
   endpoint and the paragraph's own responsibility. Do not rely on a detached
   handoff sentence at the end of the previous paragraph. If the opening
   summary does not match the fixed outline, return to paragraph structure
   before rendering prose.
7. **Subsection-flow and abstraction pass when triggered.** When the active
   card includes subsection flow or a logical-interface profile, read the [subsection flow and
   abstraction workflow](references/subsection-flow-workflow.md). Otherwise
   retain the core concept-order and paragraph-opening checks without importing
   this profile's domain examples. Compile each
   subsection's local question, opening purpose, incoming endpoint, owned
   concepts, allowed concept layer, abstraction level, outgoing endpoint, and
   transition mode. Check
   that the opening states the subsection's responsibility rather than
   repeating the preceding handoff, that alternative structures follow the
   operation or requirement they serve, and that a representation alias is not
   promoted to a new concept without a later distinction or use. Remove
   bridge-only sentences when the next opening already carries the purpose.
   Reject clauses that have no current or downstream reader-facing job. For a
   central object, require a purpose or operation before the system's stored
   representation, and use the active relation selected by the applicable
   domain profile when that is the supported meaning. When a subsection discusses
   an interface and its implementations, separate the selected logical
   operations from the implementation families and mark whether the operation
   list is representative or exhaustive.
8. **Sentence and concept-flow pass.** Check every sentence contract, adjacent
   sentence edge, first substantive use, prerequisite layer, and canonical term
   for every needed concept. For each sentence pair, identify the concrete
   endpoint carried forward and the supported relation. Repair missing
   endpoints by reordering, combining, or rewriting. Introduce ordinary
   concepts through the sentence that uses them; do not add `we define X as X`
   or an isolated `X is ...` sentence unless X is a central named abstraction,
   formal notation, invariant, or critical boundary. A locally understandable
   term still fails when it belongs to a later implementation layer.
9. **Claim-rendering pass when triggered.** When the active card includes a
   comparison, tradeoff, figure, or paragraph-opening profile, read the [claim rendering and tension workflow](references/claim-rendering-workflow.md).
   For comparison paragraphs, align the alternatives on one shared question
   and the same outcome/path axes, then state the tension at that level. For
   core tradeoffs, trace both benefit and cost to the design choice or
   mechanism, and keep workload/configuration conditions attached to the net
   effect. Make paragraph openings carry their incoming endpoint and purpose.
   Reuse canonical terms and place a figure's first source clause next to the
   core claim it explains. If the comparison frame or causal source is unclear,
   return an outline delta or `Needs context` rather than strengthening the
   prose.
9a. **Presentation organization pass.** When the story spine is aligned but
    the prose graph, paragraph grouping, sentence order, or openings are weak,
    run the [presentation organization gate](references/presentation-organization-workflow.md)
    before rendering. Independently reconstruct the presentation graph from
    the current text. Consider merge, split, reorder, relocate, delete, and
    rewrite moves; do not assume that a correct story makes the existing
    sentence and paragraph boundaries correct. Make the paragraph's central
    subject or operation appear early in its opening instead of burying it in
    the final clause. If the story, claim strength, evidence, terminology,
    scope, and subsection interfaces remain unchanged, apply the organization
    repair within the authorized scope and record it as a presentation-only
    outline change. If any substantive interface changes, stop for alignment.
    This pass produces a target organization and acceptance conditions; it is
    not a wording suggestion.
10. **Sentence-contract compilation and claim-flow materialization (Round 1).**
   Read the complete frozen claim graph, then compile the
   [sentence-level realization contract](references/sentence-realization-contract.md).
   Every slot must contain one concrete proposition, relation, evidence, scope,
   canonical terms, and provided claim. Run the proposition and opening tests
   before writing. Materialize one paragraph at a time in outline order. Pass
   the complete ordered slots, paragraph interface, previous passing endpoint,
   and next paragraph's required input to the writer. Require a
   sentence-to-slot trace and independently verify every slot and endpoint
   before moving to the next paragraph. Do not let the writer discover missing
   claims, purposes, objects, or transitions from neighboring prose.
   Do not send the whole subsection to one unconstrained writer call. If the
   runtime exposes one call only, execute this paragraph loop inside it and
   commit each passing endpoint before starting the next paragraph.
   When Evaluation is active, pass the paragraph claim and sentence role for
   every slot before its evidence values. Reject any paragraph or sentence
   whose only function is to describe data without advancing the evaluation
   claim. Accept an explicit evidence boundary when the measurement does not
   isolate a stronger effect. Do not request or invent a missing experiment in
   a presentation pass.
11. **Semantic prose rendering within each sentence contract (Round 1).**
   For the paragraph selected in Stage 10, render its aligned contracts into
   simple, direct prose with one main logical relation per sentence. Necessary
   subordinate clauses are allowed, but split a sentence when it introduces
   several new concepts, chains multiple causal steps, or places a condition
   far from the claim it qualifies. Prefer concrete subjects and verbs over
   stacked noun phrases. This pass renders the argument and preserves its
   transitions; it is not the final English copyedit. Bind figures, tables,
   metrics, terminology, and scope conditions only when their contracts are
   already supported. Prefer sentence-initial figure/table source clauses,
   metric-purpose openings, and Design-ordered evaluation breakdowns with
   benefit, cost, and net effect under the evaluated workload and
   configuration. When Evaluation is active, render from its frozen structure
   and claim–evidence matrix rather than from source paragraph order. Prefer
   purpose-bearing subjects and direct actor–operation–
   object relations. Avoid nominal phrases such as “recorded sequences” when
   the intended relation is tracking or mapping, and avoid wrappers such as
   “generally implement these operations with” when a direct, scope-calibrated
   statement is supported. For a design-centered performance breakdown,
   render the proposed-system headline result before the attribution, state why
   the breakdown follows, and keep baseline implementation and unrelated
   operations out of the focal explanation. Do not introduce a lower-level
   representation just to make an abstract sentence sound concrete.
12. **Interface freeze and parallel revision when triggered.** When the active
   card includes parallel workers or a shared subsection boundary, convert the aligned outline
   subtree into subsection contracts. Freeze local responsibility, incoming
   handoff, central claim, provided claims, outgoing handoff, protected
   evidence and terminology, allowed local changes, and shared-edge ownership.
   Then run independent subsection revisions in parallel from the same fixed
   version, with disjoint owned units and isolated patches. Return any proposed
   interface change as an outline delta before rerunning affected contracts.
13. **Integrate the revision.** Merge the disjoint patches into one
   canonical version, reconcile shared terms, figures, paragraph order, and
   boundary handoffs, and maintain a unit ledger for every original unit.
14. **Presentation/logic repair (Round 2), then final English polish (Round 3).**
   Before the language-only pass, run an independent review of every sentence
   pair and paragraph boundary. Name the concrete endpoint and relation carried
   forward, distinguish parallel alternatives from lists, keep supporting
   mechanisms from becoming new main branches, split overloaded sentences, and
   remove redundant or bridge-only sentences. Route unknown technical terms,
   layer jumps, and unexplained questions to `Needs context` or the terminology
   alignment stage. Apply the Round 2 gate from the iterative prose workflow.
   Only after that gate passes, perform the bounded language-only pass. Improve
   grammar, articles and prepositions, idiomatic phrasing, sentence length,
   parallelism, pronoun antecedents, and paragraph-level transitions. Replace
   repetitive or mechanically stacked connectives such as `because`,
   `therefore`, or `however` only when the supported relation remains explicit;
   do not vary a connective merely for style. Preserve every claim, condition,
   causal edge, figure/table source clause, metric purpose, canonical term, and
   section responsibility. This pass may shorten or split a sentence, but it
   may not add a concept, evidence item, mechanism, or structural handoff.
   After each round, run an independent round-trip diff against the frozen
   render contract. Compare nodes, node order, paragraph roles and openings,
   `from`/`needs`/`link` edges, evidence, scope, and lexical IDs. An invented
   term such as `invocation`, first-paragraph drift, or a missing transition
   fails the round. Roll back to the last passing artifact and route the issue
   to outline, semantic-graph, or terminology alignment; never pass a failed
   artifact to the next round. Record only a passing output as a new manuscript
   version.
15. **Independent verification after polishing.** Give the exact polished
   artifact and its outline revision to the reviewer. Reapply the criteria to
   the complete requested scope, including unchanged text whose context
   changed. Reconstruct the high-level story, hierarchy, Motivation Recovery
   contract and leakage map when relevant, selected section patterns,
   first-sentence-only subsection summary, paragraph and sentence handoffs,
   first-use map, claim rendering, and evidence bindings against the fixed
   outline. Confirm that the language pass did not alter a logical relation or
   claim scope.
16. **Iterate through the named rounds.** Start each round from the last
   passing artifact and the same frozen render contract; preserve issue IDs.
   Round 1 renders the aligned contracts, Round 2 repairs presentation logic
   and transitions, and Round 3 polishes concise English. After every writer
   call, independently round-trip the complete output against the contract.
   Continue only for concrete required findings or regressions; do not loop for
   optional suggestions, stylistic disagreement, or a quota of changes. If a
   round introduces an object, term, edge, first-paragraph responsibility, or
   ordering change, roll back and return to the earliest affected stage before
   rerunning downstream rounds.
17. **Stop and report.** Stop with `Complete` when no required findings remain.
   Stop with `Needs context` when a missing fact, evidence gap, or substantive
   author decision blocks a faithful repair. Stop with `Needs revision` when
   the iteration limit is reached or required findings remain. Never call a
   self-checked draft independently verified.

When the story has two or more equally supported outline structures, choose
the simpler one in automatic mode and record the ambiguity in the fixed
outline. If the choice changes the
paper's scientific emphasis or contribution claim, stop for author discussion
instead of deciding silently.

## Manual interaction and handoffs

Manual work can alternate among the modes without losing state:

- `review` creates findings, a target map, and figure findings when requested.
- story/claim alignment records which findings and claim decisions are
  accepted, rejected, deferred, or unresolved.
- outline synthesis creates a versioned outline delta; outline alignment writes
  the selected hierarchy, order, grouping, handoffs, alternatives, and author
  decisions into the fixed outline.
- `discuss` turns an unresolved target map into author choices.
- `sections` creates the Motivation Recovery contract, leakage map, selected section patterns, and Design traceability map.
- `figures` creates figure briefs or discusses figure alternatives.
- `terms` creates or updates the terminology ledger and subsection map, and
  proposes glossary edits.
- `guided` renders author-supplied paragraph contracts into prose and returns a
  graph trace for review.
- `revise` applies the selected changes.
- `review` on the fixed revised version verifies them.

Pass the manuscript version, fixed outline revision/status and selected
subtree, issue IDs, acceptance conditions, target outline delta, and unresolved
decisions at every handoff. The reviewer never edits. The
revision workers edit only their owned units; the coordinator is the only agent
that merges patches into the canonical manuscript. If separate agents are
unavailable, perform these roles as sequential passes with the same boundaries.

For parallel subsection work, also pass the scope manifest, subsection
contracts, owned units, read-only boundary context, shared edges, and
coordinator. After the interfaces are frozen, parallelize independent
subsection revisions on the same fixed version and collect isolated patches.
Serialize interface changes, patch merging, and shared-edge decisions. Run a
section-level review after merging all subsection outputs.

## Output contract

Return the mode, scope, input version, output version when one exists, current
refinement stage, active rule profile, gate result, earliest failed stage when
applicable, and coverage limits. For prose or structure work, include the
paragraph-opening matrix or its verification result. For `review`, include findings and acceptance conditions. For
`discuss`, include options, the semantic object and logic graph, the
argument-node execution view, the sentence/logic-level human sync view, and
author decisions needed. For `figures`, include
figure decisions, briefs, placement, source inputs, and rendering status. For
`sections`, include the sealed Motivation Recovery contract, leakage map,
selected section patterns, Design traceability map, section findings, and open
author decisions. For `terms`, include the
terminology ledger, variant findings, subsection map, and
semantic operation/state contracts, and open author decisions. For `revise`, include the revised artifact or edited
file plus the change maps, the fixed outline path/revision/status, selected
subtree, presentation-organization moves, and any reverse-outline discrepancy. For
Evaluation scopes, also include the selected Evaluation question or archetype,
macro progression or local narrative order, claim–evidence matrix status, and
source-unit disposition map. For
`guided`, include the paragraph-contract trace, argument-node-to-prose trace,
sentence-level realization contract, sentence-to-slot trace, generated scope,
unresolved context, source outline path/status, and round-trip graph and
outline check.
For `rebuild-from-material`, include the immutable source version, material
ledger, source-unit disposition map, recovered story, target outline revision,
and contract-to-material trace. Do not report the source paragraph order as the
target unless it was explicitly protected.
For `auto`, include the iteration plan and per-round history,
resolved and open findings, structural
changes, figure decisions and artifacts, final verification status, and the
stopping reason. For automatic or multi-phase work, also report the selected
effort profile, any escalations, and whether the runtime enforced per-call
effort values.

For `revise` and `guided`, also report the iteration plan and per-round history
when prose refinement ran. A normal aligned edit should end with
`iteration_round=complete` and independent verification; a `draft-only` result
must be labeled as a Round 1 artifact and must not be presented as final prose.

For the default staged workflow, report the current workflow stage. After a
read-only review, report `Awaiting alignment` for claim decisions and
`Awaiting outline alignment` when the fixed outline's presentation structure is
not yet selected. Return the fixed outline path/revision/status and selected
subtree; after outline alignment, carry that exact revision into
interface compilation, revision, and verification.

Do not claim scientific validity, experimental adequacy, novelty, or conference
acceptance. Do not add experiments, design mechanisms, citations, or results.
If the available text cannot support a repair, preserve the best faithful
version and make the gap explicit.
