---
name: paper-presentation-revise
description: Revise academic-paper prose, presentation structure, and authorized figure handoffs while preserving technical meaning and evidence. Use for polishing, rewriting, removing repetition, repairing transitions, reorganizing paragraphs or sections, searching for a supported target argument structure, and addressing presentation-review findings in English, Chinese, or LaTeX. Supports a review-revise-verify workflow with paper-presentation-review; for automatic orchestration, use paper-presentation. Excludes slides, inventing research content, and scientific redesign.
---

# Paper Presentation Revise

Act as the manuscript writer. Improve the reader's understanding through structure, precise concepts, clear reasoning, and economical prose. Own the revised text and its fidelity to the source. Independent acceptance belongs to the reviewer.

Do not perform or claim independent review in the same call that edits the
manuscript. The caller must provide a fixed-version review artifact with issue
IDs and acceptance conditions, or run the separate review phase before this
writer phase.

The writer starts only after the author has aligned the story and structured
outline. The aligned outline, rather than the source paragraph order or a
writer's preferred Design pattern, is the drafting target.

The aligned input may begin as a coarse paragraph chain. In that case, the
orchestrator must first run outline completion and independent outline review
to produce the sentence-level realization contract. This writer does not infer
sentence propositions, missing relations, or transitions from a coarse outline
or from neighboring prose.

For a direct paragraph or small contiguous-scope request, use the [local
paragraph review and revision workflow](../paper-presentation/references/local-paragraph-review-revise-workflow.md).
An old outline is a synchronization baseline, not a blocker: review the local
paragraph even when the outline is stale, and rebuild a local contract when
the adjacent interfaces remain unchanged. A shared interface change returns a
local outline delta before it changes neighboring claims.

## Required inputs and shared standard

First read the [rule activation workflow](../paper-presentation/references/rule-activation-workflow.md)
and build an active-context card for the requested scope, section, subsection
archetype, stage, and mode. Always load [the shared presentation criteria](../paper-presentation-review/references/criteria.md),
[the fixed outline workflow](../paper-presentation/references/project-outline-integration.md),
[the argument-node outline workflow](../paper-presentation/references/argument-node-outline-workflow.md),
[the semantic object and logic graph workflow](../paper-presentation/references/semantic-object-graph-workflow.md),
[the sentence-level realization contract](../paper-presentation/references/sentence-realization-contract.md),
[the hierarchical outline research workflow](../paper-presentation/references/hierarchical-outline-research-workflow.md),
[the local paragraph review and revision workflow](../paper-presentation/references/local-paragraph-review-revise-workflow.md),
[the Design Presentation Patterns](../paper-presentation/references/design-presentation-workflow.md),
and the [paragraph opening workflow](../paper-presentation/references/paragraph-opening-workflow.md)
for any prose, outline, guided-generation, or structure revision. Load the
[claim-flow materialization workflow](../paper-presentation/references/claim-flow-materialization-workflow.md)
before prose rendering. It treats the aligned claim graph as the writing
target and materializes paragraphs in outline order. Load the
remaining references only when the active card triggers them.

Conditional profiles include the structural presentation workflow, concept–claim
logic flow workflow, outline-based presentation structure workflow, coarse-to-fine
refinement pipeline, subsection flow and abstraction workflow, review-to-outline
continuation routing workflow, [presentation organization gate](../paper-presentation/references/presentation-organization-workflow.md), [Evaluation Presentation and Rebuild Workflow](../paper-presentation/references/evaluation-presentation-workflow.md), claim rendering and tension workflow, guided
paragraph generation workflow, parallel section scope workflow, systems-paper
presentation patterns, presentation figure workflow, section responsibility
workflow, section presentation playbook, Motivation Recovery Workflow, and
terminology and subsection workflow. When the story and outline are aligned but
the prose needs multiple passes, also load the [iterative prose refinement
workflow](../paper-presentation/references/iterative-prose-refinement.md) and
the [frozen prose-round contract](../paper-presentation/references/prose-round-contract-workflow.md).
Use
the final manuscript visual QA workflow
only for an explicitly requested PDF or rendered-layout pass. Do not compile or
inspect a PDF during ordinary revision.

When the author supplies a poor subsection as reference material, also load the
[reference-material rebuild workflow](../paper-presentation/references/reference-material-rebuild-workflow.md).
This changes the revision route: the source is audited for supported material,
but its wording, paragraph order, transitions, and local presentation are not
the target.

The selected profiles add checks and ordering without relaxing the core
criteria, the paper's writing guide, or accepted author decisions. If a
structural change changes the section or subsection archetype, recompute the
active card before rendering the affected text. Preserve the fixed outline's
stable IDs, roles, argument-node mappings, `from`, `needs`, `link`/`transition`,
source mappings, and
change log. The detailed revision procedure below is a dispatcher, not a
simultaneous checklist. Apply a domain-specific clause only when its active
profile is present.

When the target outline and edit authorization are aligned, a prose revision
continues through semantic rendering, presentation/logic repair, and concise
English polish by default. Do not stop after the semantic-rendered draft or
ask the user to trigger the next wording round unless the user requested
`draft-only` or a round exposes a substantive author decision.

The default rendering unit is one paragraph. Within a subsection, the writer
must finish and pass the current paragraph before receiving it as context for
the next paragraph. Do not issue a one-shot whole-subsection drafting request;
the subsection-level migration check runs only after all paragraph contracts
have passed. Independent subsections may run in parallel after their
interfaces are frozen.

Before the first writer call, freeze the prose-round contract. Pass the same
contract revision, protected node and edge IDs, paragraph-opening matrix,
sentence slots, and lexical ledger to every round. The writer may improve the
realization of those contracts, but may not use the preceding prose as a new
outline. An unknown technical term such as `invocation`, a changed first
paragraph responsibility, or a missing transition edge is a failed round-trip
check; return the last passing artifact and route the issue to outline,
semantic-graph, or terminology alignment.

Before rendering, compile the [sentence-level realization contract](../paper-presentation/references/sentence-realization-contract.md).
A paragraph outline that names only topics or intentions is incomplete. Every
slot must state one concrete proposition, its relation to the previous slot,
evidence, scope, canonical terms, and provided claim. Round 1 uses one slot
per sentence by default and requires a sentence-to-slot trace. If a slot
cannot be rendered without inventing a noun, adjective, operation, causal
relation, or scope condition, stop with `Needs context` or an outline delta
rather than letting the writer improvise.

When the story is aligned but the prose graph is weak, run the [presentation
organization gate](../paper-presentation/references/presentation-organization-workflow.md)
before semantic rendering. The writer is expected to consider merge, split,
reorder, relocate, delete, and rewrite moves. A presentation-only move that
preserves story, claim strength, evidence, terminology, and interfaces is an
authorized repair within the subsection; it must be recorded in the outline
change map rather than avoided in favor of sentence-level patching.

Identify the source version, requested scope, adjacent context, author constraints, and available evidence. Read applicable `AGENTS.md` files, linked writing guides, and the paper's [glossary](../paper-presentation-review/references/glossary.md), then read the fixed outline files for the requested scope, including applicable parent-project instructions for a nested manuscript repository. Keep paper-specific terms in that repository's glossary and other decisions in its canonical guide.

A reviewer issue list is useful but not required as user input. The caller must
run an independent review on the exact input version before this writer phase,
unless the author explicitly supplies a current review artifact bound to that
version. Retain its IDs and acceptance conditions, and check the findings
against the original text and evidence rather than treating every proposed fix
as authoritative.

Route a source-only request to `rebuild-from-material` when the author asks to
rewrite or reorganize a poor subsection, calls the old version reference
material, or does not provide an aligned target story and outline. In that
route, the old text is an immutable source snapshot. Its facts and evidence
candidates enter a material ledger; its organization and wording do not enter
the drafting target by default. If the author explicitly asks to preserve the
current structure, use ordinary `revise` instead.

## Revision procedure

1. **Freeze the active rule profile.** Record the active-context card and the
   triggered profiles before editing. Keep the paragraph-opening workflow
   active for every prose or structure revision. If the intended structural
   change reveals a different section or subsection archetype, stop rendering,
   recompute the card, and load the new profile.
2. **Establish protected content.** In ordinary revision, identify the claims,
   assumptions, definitions, core numerical evidence, scope conditions, causal
   links, and source syntax that the revision needs to preserve. In
   `rebuild-from-material`, run the material audit first: classify each source
   unit as protected fact/condition, candidate claim, non-authoritative
   presentation, scoped example, or unresolved material; assign `retain`,
   `relocate`, `merge`, `split`, `defer`, `drop`, or `needs context`; and record the
   source locator and destination contract. Do not call every original sentence
   protected merely because it is present.
   When Evaluation is active, additionally classify metric purpose,
   workload/configuration, evidence source, supported interpretation, cost,
   limitation, and source order separately. Do not use the old Evaluation
   paragraph grouping as the drafting target.
3. **Check section contracts when triggered.** When the active card includes a
   section-level or cross-section profile, select a supported section pattern.
   For a multi-section scope, run Motivation Recovery before reading Design
   details. Record the high-level setting, observations, pressure,
   opportunity, design-independent insight candidates, requirements, and
   leakage map. Then map Design choices to that contract. Do not rewrite
   Motivation to make an existing Design appear necessary. Rewrite leaked
   mechanisms as requirements only when the evidence supports that abstraction,
   or move them to Design as a naive-solution or proposed-mechanism unit, and
   flag unmapped choices or open requirements. For a local excerpt, keep this
   pass to the section contract named by the active card.
   When Design is active, use the [Design Presentation
   Patterns](../paper-presentation/references/design-presentation-workflow.md)
   and the aligned outline selected during story discussion. Preserve the
   selected pattern, reader-facing node order, unit responsibilities, and only
   the representation, operation, invariant, cost, or update relations that
   the pattern requires. Do not invent a component/layout/update sequence
   while rewriting.
   When the active card includes Evaluation, run the [Evaluation Presentation
   and Rebuild Workflow](../paper-presentation/references/evaluation-presentation-workflow.md)
   and [Evaluation Patterns from Systems Papers](../paper-presentation/references/evaluation-reference-patterns.md).
   Freeze the Evaluation question, macro progression or local archetype,
   separate source/design/figure/narrative order, and build the claim–evidence
   matrix before rendering. For a design breakdown, preserve Design order; for
   other archetypes, derive narrative order from the evaluation question and
   evidence dependencies. If the archetype is a design-centered performance
   breakdown, also freeze the proposed design as the focal subject, the
   headline result before attribution, the reason for the breakdown, the
   baseline role and compression, and the relevance decision for each
   operation or implementation detail.
4. **Reconstruct the argument.** Build the argument inventory and dependency graph from the structural workflow, then build the concept–claim node and edge inventory. If an author blueprint is supplied, compile paragraph contracts from its roles, incoming and outgoing edges, evidence mappings, and scope conditions. Identify the section question, paragraph takeaways, prerequisite definitions, evidence mappings, causal links, final handoffs, undefined or premature nodes, dangling claims, wrong endpoints, lost scope, and unsupported relations. Check Motivation's observation-to-opportunity argument before elaborating a proposed mechanism.
5. **Use the fixed outline as the target structure.** Load the exact outline subtree and its revision for the requested scope. In ordinary revision, use its hierarchy, selected order, unit roles, sentence contracts, evidence mappings, and handoffs as the target. In `rebuild-from-material`, do not derive a target from the source paragraph order. First recover the story independently, obtain author story alignment, synthesize a new outline, and obtain outline alignment. If the fixed outline is `proposal`, stale against the manuscript, or contradicted by the supplied author map, report an outline delta and stop for whole-scope structural edits before changing the manuscript unless the author explicitly supplied a complete replacement target and edit authorization. For a direct paragraph or small contiguous-scope request, use the local paragraph workflow: rebuild only the local contract when the shared interfaces remain unchanged and proceed with the authorized local rewrite. A changed incoming or outgoing interface returns to outline alignment before neighboring claims change. First report any missing premise, contradictory edge, unsupported evidence mapping, or ambiguous endpoint that prevents faithful rendering. Test reviewer target maps against the original text and evidence rather than accepting them mechanically. Reject changes that violate dependencies, section responsibilities, evidence mappings, or protected content. If two supported outline alternatives remain, choose the simpler one only in an authorized automatic run and record the choice in the fixed outline.
   If the fixed root and index exist but the requested rebuild subsection has no
   mapped subtree, create a `proposal` at that fixed location only after story
   alignment; never search another outline directory.
   When Evaluation is active, the target subtree also carries the selected
   Evaluation question or archetype, narrative order, claim–evidence bindings,
   and source-unit dispositions. A fixed outline that merely mirrors an old
   Evaluation subsection is provisional until this reconstruction is recorded.
   For every aligned scope, the target subtree also carries the semantic
   object/logic graph, argument-node execution view, sentence/logic-level human
   sync projection, and sentence-level realization contract. Treat all
   projections as views of the fixed outline, not as independent targets; a
   paragraph-only synopsis is insufficient for rendering.
   Before any prose call, freeze the complete ordered claim flow and compile
   paragraph and sentence materialization contracts. The writer receives one
   paragraph's complete ordered sentence slots, each with a concrete
   proposition, relation, evidence, scope, and canonical terms, together with
   the incoming endpoint and next paragraph's required input. It writes
   paragraphs in outline order and returns a sentence-to-slot trace; it does
   not infer missing claims or transitions from neighboring prose.
6. **Repair structure first.** Reorder, regroup, merge, split, defer, or move supplied content when the target structure requires it. Perform these changes before sentence-level polishing. In ordinary revision, keep a unit ledger for every original unit and preserve its facts, conditions, claim strength, and source mapping. In `rebuild-from-material`, use the source disposition map instead: source units may be retained, relocated, merged, split, deferred, or dropped, but each choice must have a destination or reason. A source sentence is not a required unit. If relocation goes outside the authorized scope, report its intended destination and retain the material in the handoff rather than silently deleting it or changing an unrelated section.
   For supplied paragraph contracts, render one contract at a time using the
   preceding handoff, current contract, terminology ledger, allowed evidence,
   and next incoming edge as local context. Preserve the declared role,
   incoming edge, outgoing handoff, evidence mapping, and scope; do not
   silently redesign the story or invent a missing premise.
   Verify each paragraph independently against its claim-flow contract before
   starting the next paragraph. After the complete subsection passes locally,
   run the opening/endpoint migration check across paragraph boundaries. If a
   boundary repair changes a node, edge, paragraph responsibility, or
   abstraction layer, return to outline alignment rather than hiding the change
   in a transition sentence.
   When Evaluation is active, pass the paragraph claim and sentence roles
   before the result values. Reject a paragraph that only inventories figures,
   measurements, configurations, or baselines without an interpretation,
   comparison, condition, cost, net effect, evidence boundary, or implication
   tied to the claim. Do not add an experiment or a stronger interpretation to
   fill an attribution gap.
   When the story is already aligned but the presentation is weak, do not
   preserve one source sentence per output sentence. Run the presentation
   organization gate and record the chosen merge, split, reorder, relocate,
   delete, or rewrite moves. Make each paragraph opening lead with its central
   subject or operation; carrying an incoming endpoint does not justify
   burying that subject in a final clause. Pause only when a proposed move
   changes a substantive story or interface decision.
   This organization gate runs before the prose-round contract is frozen. Once
   the contract is active, a merge, split, reorder, relocate, delete, changed
   opening responsibility, or changed transition is an outline delta and must
   not be performed silently by a prose round.
   When Evaluation is active, make these moves against the frozen evaluation
   structure and claim–evidence matrix. Do not preserve one source paragraph
   per result group by default, and do not let figure order replace the selected
   narrative order. Keep a design breakdown in Design order while presenting
   each component's benefit, cost, and workload/configuration-dependent net
   effect as one connected account. For a design-centered performance
   breakdown, render the proposed-system headline result first, state why the
   breakdown is needed, and then explain the proposed design in Design order.
   Keep each baseline to the outcome or causal distinction needed for
   comparison unless the evaluation question makes that baseline a co-equal
   subject. Remove or relocate operations and implementation details that do
   not explain the focal metric, introduced cost, measured boundary, or direct
   comparison. Use performance terms for a performance question; do not
   introduce access-path framing unless that is the question being evaluated.
   Render from the aligned semantic object graph, argument-node execution view,
   and sentence-level realization contract. Map each sentence to its slot and
   node IDs, preserve every slot's role and relation, and do not invent a node
   that is absent from the aligned outline. If two adjacent nodes can be
   expressed naturally in one sentence, preserve both mappings rather than
   dropping one; if one sentence carries independent relations, split it.
   Use only active canonical terms and allowed forms from the frozen terminology
   ledger. Validate every operation or state-changing verb against its actor,
   target, precondition, state transition, observable effect, and scope. A new
   synonym or a semantically different verb requires a review finding or an
   author decision; it is not a polishing choice.
Before the final language pass, verify the logical-interface boundary. If the
scope discusses selected operations, mark them as a focus rather than an
exhaustive interface unless the source establishes completeness. Render each
operation's input, purpose, and output before introducing the structure family
that implements it, and keep representative system-to-structure mappings
source-backed.

8. **Final English polish.** After all structural and evidence changes are
   integrated, make a language-only pass over the authorized scope. Improve
   grammar, articles and prepositions, idiomatic wording, sentence length,
   parallelism, pronoun antecedents, and transitions. Reduce repetitive or
   mechanically stacked connectives such as `because`, `therefore`, and
   `however` only when the supported relation stays explicit. Preserve the
   outline, claim strength, qualifiers, canonical terms, evidence, figure/table
   source clauses, metric-purpose openings, and subsection handoffs. If a
   proposed wording change would alter one of these, return it to the earlier
   structural or claim-rendering stage instead of applying it here.
   Before the final self-check, reconstruct the semantic object graph from the
   prose: concepts, claims, evidence, purposes, mechanisms, results, costs,
   conditions, lexical items, and handoffs. Compare its purpose/question edges
   and lexical provenance with the aligned graph; an added object, modifier, or
   causal relation is a finding even when the prose is fluent. Apply the
   round-trip gate from the frozen prose-round contract before accepting this
   version. A language-only pass cannot change paragraph order, sentence
   relations, opening responsibilities, canonical technical terms, or scope.
   Do not pass a failed artifact to the next round.
9. **Self-check the complete section-contract, structural, logic-flow, terminology, subsection, claim-rendering, visual, and language revision.** Reconstruct the dependency graph and the concept–claim graph from the final text without relying on the writer's plan. Compare both with the fixed outline subtree. Reconstruct a reverse outline of the final hierarchy, unit order, local responsibilities, sentence roles, `from`, `needs`, and `link`/`transition` relations; report any mismatch as an outline change rather than silently accepting it. Run the [paragraph opening workflow](../paper-presentation/references/paragraph-opening-workflow.md) without consulting the writer's explanation: compare the first-sentence-only summary with the fixed outline, and verify that every noninitial opening carries both its incoming endpoint and its own responsibility. Do this especially before Design. At each paragraph boundary, verify that the next paragraph's opening carries the transition and responsibility rather than relying on a detached closing handoff. Check the entire supplied scope, including unchanged text affected by new ordering. Re-run Motivation Recovery without using Design and verify that the recovered opportunity and requirements remain design-independent, that leaked or naive-solution units are separated, and that Design choices map to the resulting Motivation contract. Confirm that each original unit is accounted for, all required dependencies are available before use, evidence remains mapped to the claims it supports, and no move changed section responsibility or claim strength. Re-scan every concept and operation at first use: verify that its role, input or source, purpose, and effect are locally recoverable, and that no tautological or unnecessarily isolated definition was added. Verify that each sentence pair has a concrete endpoint and supported relation, and split or simplify any sentence whose conceptual load makes that relation hard to follow. Verify comparisons against one shared question and comparable outcome/path axes, and verify that every core tradeoff traces benefit and cost to the correct design source with the net effect scoped to its workload or configuration. Verify that each subsection is locally understandable with a forward handoff. For every selected figure, confirm that its reader question, placement, caption, visual encoding, source inputs, and final artifact agree with the text, and that a core design figure is first cited beside the claim it explains. For an evaluation breakdown, confirm that all three effect points remain supported for every component and that unresolved evidence is marked explicitly. Also confirm that figure and table observations have explicit source clauses, metric-result paragraphs orient the reader before reporting values, every paragraph handoff names a recoverable shared object or result, and factual system-to-mechanism mappings are either source-backed or explicitly unresolved. Report any node that became undefined or premature, any edge that became missing or ambiguous, and any silent strengthening or weakening of a claim. Fix supported issues before handoff. Self-checking does not constitute independent verification.
   Also reconstruct the argument-node graph from the final prose without using
   the writer's process explanation. Compare node roles, relations, evidence,
   conditions, and sentence mappings with the canonical outline and human sync
   view. Report missing, invented, reversed, or overstrong nodes before
   language-only acceptance. Rerun the presentation organization gate: verify
   that each paragraph
   opening exposes its central subject or operation early, that every required
   organization move was recorded, and that no unresolved relation was hidden
   by a connective or a final English polish.
   When Evaluation is active, verify the final text against the frozen
   evaluation structure and claim–evidence matrix. Confirm that the selected
   question and archetype remain visible, narrative order has not drifted to
   source or figure order, every claim has evidence and scope, and each
   breakdown component retains its Design order, benefit, cost, and
   workload/configuration-dependent net effect. For a design-centered
   performance breakdown, also confirm that the headline result precedes
   attribution, the breakdown purpose is explicit, the proposed design is the
   focal subject, baselines are concise anchors, and unrelated operations or
   implementation details are absent.
Before returning, also verify the abstraction firewall: no Motivation concept
is merely locally explained while still belonging to a later representation or
implementation layer, and every central object is introduced through its
purpose or operation before its stored representation. Recheck that indexing,
tracking, and mapping relations use direct active wording when supported.
When Design is active, reconstruct the selected Design pattern and its
reader-facing node order from the final prose. Check that unit granularity,
responsibilities, contracts, and any pattern-specific representation,
operation, invariant, cost, or update relations match the aligned outline.
Before returning, treat figure checks as source-level checks by default. Confirm
each selected figure's reader question, placement, caption, visual encoding,
source inputs, and text handoff. Inspect the final artifact and physical-size
rendering only when the author explicitly requested `visual-qa` or supplied a
bound rendered artifact. Otherwise defer page-layout inspection.
9. **Return a reviewable version.** Provide the revised text or edit the explicitly requested manuscript files, identify the resulting version, and include the fixed outline path/revision/status, selected subtree, and concise outline-change map when structure changed. For parallel subsection work, also return the fixed base version, owned units, preserved incoming and outgoing handoffs, provided claims, and any outline delta; return an isolated patch when another worker owns adjacent units. When files may change concurrently, supply a content hash or immutable snapshot for review. Never stage or commit unrelated changes.

## Handling findings and evidence gaps

For each reviewer ID, give one writer disposition:

- `Addressed`: state the new location and how the text meets the acceptance condition. Only the reviewer can mark it `Resolved`.
- `Needs context`: identify the exact missing definition, premise, condition, or reason. Complete independent edits without fabricating the missing information.
- `Disputed`: cite evidence that the requested fix is inapplicable or would lose information or change the research claim. Provide a supported alternative when possible.
- `Not adopted`: for optional suggestions only, explain briefly why the existing choice remains suitable.

Do not silently drop a required finding or weaken an unsupported substantive claim to make the review pass. Narrow an overpromising transition only when this faithfully describes the analysis already present. Changes to scientific meaning require an explicit author decision. Avoid repeatedly requesting the same missing context or cycling between equally valid phrasings.

## Output contract

- For a rewrite-only request, return the revised passage in the manuscript's language and format. Keep unresolved facts unmistakable. If a faithful complete rewrite is impossible, use an explicit author placeholder and disclose the gap outside publication-ready prose, rather than delivering invented content as final.
- For `rebuild-from-material`, return the material ledger and source-unit
  disposition map before prose when story or outline alignment is still open.
  After alignment, return the new target structure and a contract-to-material
  trace. Do not present a lightly edited source passage as the rebuild result.
- For revision with review findings, provide the complete revised scope plus a concise issue-to-change map and all unresolved items. For file edits, reference the edited artifact instead of duplicating a long manuscript unless requested.
- When an author blueprint supplied paragraph contracts, also provide the
  sentence-level realization contract, contract-to-prose and sentence-to-slot
  traces, unresolved context, and the round-trip graph check.
- When structure changed, include the target structure or a concise structure-change map with moved, merged, split, deferred, or removed units and their destinations. For file edits, reference the edited artifact instead of duplicating a long manuscript unless requested.
- For review-and-revision output, summarize the main problems in at most three groups if a summary is useful. This is a presentation limit, not a limit on findings or coverage.
- Report the active rule profile, its selection reason, and the first-sentence-only verdict or paragraph-opening matrix for prose and structure revisions.
- When an iterative prose round is active, report its named round, focused gate,
  input/output versions, and whether any finding requires rollback to an
  earlier round.
- When a frozen prose-round contract is active, report its revision, protected
  node/edge/lexical IDs, allowed change budget, independent round-trip diff,
  gate result, and rollback target. A failed diff is not a publishable round
  output.
- When the presentation organization gate ran, report its reverse
  presentation graph, required merge/split/reorder/relocate/delete/rewrite
  moves, target organization, and whether the move was presentation-only or
  required author alignment.
- Report the argument-node execution view, human sync projection, and
  sentence-level realization contract, node-to-prose and sentence-to-slot
  traces for the revised scope. State whether each node was
  retained, merged, split, relocated, or dropped, and whether the final graph
  round-trips to the aligned outline.
- When semantic-object reasoning was active, also report the semantic object
  graph, purpose/question edges, evidence mappings, lexical-item audit, and
  any node or term that remained unresolved. The prose must not add an object,
  claim, modifier, or causal relation absent from the aligned graph.
- When Design is active, also report the Design pattern selected during
  story/outline discussion, its reader-facing node order, unit boundaries and
  responsibilities, and any pattern-specific consequences.
- When Evaluation is active, report the selected Evaluation question or
  archetype, macro progression or local narrative order, claim–evidence
  matrix status, source-unit disposition map, and any reason the target order
  intentionally matches source order. For a design-centered performance
  breakdown, also report the focal design, headline-result gate, breakdown
  purpose, baseline compression, and operation/detail relevance decisions.
- Put LaTeX passages in a `latex` block and preserve commands, labels, citations, equations, macros, and values. Treat author comments as instructions, preserving or resolving them according to the request. Keep commentary in the user's language and outside the manuscript text.
- State whether the result has only been self-checked or independently verified, and name any unresolved limits. Do not claim reviewer approval from a writer's own disposition or predict conference acceptance.

## Coordinating review, revision, and verification

For every presentation revision, the caller uses [paper-presentation-review](../paper-presentation-review/SKILL.md) on the original, freezes the findings, sends them to the writer, then gives the reviewer the exact integrated revised artifact for verification. Separate reviewer and writer calls or agents are required. Review and author alignment happen before revision. After subsection interfaces are frozen, independent writers may revise disjoint owned units in parallel from the same fixed version and return isolated patches. The coordinator is the only agent that merges patches into the canonical manuscript and resolves shared edges. Reviewer and writers never modify a moving draft concurrently.

For automatic presentation iteration, [paper-presentation](../paper-presentation/SKILL.md) owns the orchestration and supplies the fixed artifact, target structure, issue IDs, and round limit.

The reviewer first reads the revised artifact against the criteria, then checks the issue/change map. This reduces reliance on the writer's account. The caller delivers the revision and verification result together, preserving unresolved findings.

Continue only for concrete, supported required findings that can be repaired. Finish when the scoped checks find no required issues. If missing evidence, a substantive author decision, or a persistent unresolved disagreement prevents further supported progress, return the best faithful revision with those items explicitly open. Do not continue merely to exhaust optional suggestions or satisfy a quota of rounds. Honor any user-specified iteration limit and do not call an unverified draft verified when that limit is reached.

Every presentation revision requires a separate review before writing and a
separate verification after writing. If an independent reviewer cannot be
run, return a proposed or self-checked revision with an explicit incomplete
status; do not present it as reviewed or verified. The same reviewer role and
criteria may be reused for verification, but it must read the new fixed
version as a separate pass.
