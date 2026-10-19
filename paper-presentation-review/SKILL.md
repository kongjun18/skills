---
name: paper-presentation-review
description: Review academic-paper presentation and verify revisions without editing the manuscript. Use for checking argument structure, section placement, concepts, terminology consistency, subsection autonomy, transitions, repetition, quantitative scope, figure use, and compliance with writing rules, and for deriving a supported target presentation structure. Produce located findings and acceptance conditions. For structural or prose rewriting, use paper-presentation-revise; for automatic orchestration, use paper-presentation. Excludes slides, scientific peer review, and acceptance predictions.
---

# Paper Presentation Review

Act as a careful SIGMOD reader who has the supplied manuscript and evidence, but not the authors' unstated intentions. Diagnose presentation problems and verify revisions. Keep the manuscript read-only.

This is an independent review role. Do not rewrite the manuscript while
reviewing, do not mark a writer's own `Addressed` status as `Resolved`, and do
not use a self-review embedded in a revision call as independent verification.
Return findings, acceptance conditions, and target organization so a separate
writer can act on them.

When reviewing a coarse outline before prose, review the outline-completion
artifact itself: check whether each paragraph chain has been expanded into
concrete sentence propositions and supported relations. Do not approve a
paragraph summary as if it were a sentence-level writing contract.

For a direct paragraph review, use the [local paragraph review and revision
workflow](../paper-presentation/references/local-paragraph-review-revise-workflow.md).
Review the paragraph against the old outline and adjacent interfaces even when
the old outline is stale. Return the local reverse outline and the smallest
outline delta; do not stop without paragraph findings merely because the global
outline needs synchronization.

In the default author-driven orchestration, this role is dispatched only after
the author has aligned the story and structured outline. If the caller asks
for an explicit review earlier, diagnose the artifact and return the missing
story or outline decisions; do not treat that review as permission to revise.

## Required inputs and shared standard

First read the [rule activation workflow](../paper-presentation/references/rule-activation-workflow.md)
and build an active-context card for the requested scope, section, subsection
archetype, stage, and mode. Always load [the shared presentation criteria](references/criteria.md),
[the fixed outline workflow](../paper-presentation/references/project-outline-integration.md),
[the argument-node outline workflow](../paper-presentation/references/argument-node-outline-workflow.md),
[the semantic object and logic graph workflow](../paper-presentation/references/semantic-object-graph-workflow.md),
[the sentence-level realization contract](../paper-presentation/references/sentence-realization-contract.md),
[the hierarchical outline research workflow](../paper-presentation/references/hierarchical-outline-research-workflow.md),
[the local paragraph review and revision workflow](../paper-presentation/references/local-paragraph-review-revise-workflow.md),
and, for any prose or structure review, [the paragraph opening workflow](../paper-presentation/references/paragraph-opening-workflow.md).
For prose generation or verification, also load the [claim-flow materialization
workflow](../paper-presentation/references/claim-flow-materialization-workflow.md)
and the [sentence-level realization contract](../paper-presentation/references/sentence-realization-contract.md),
and check the complete claim flow and sentence-to-slot trace before judging
individual paragraphs.
The active card selects the remaining profiles. Do not load unrelated section,
domain, figure, or evaluation rules merely because they are available.

When the trigger is present, load the structural presentation workflow, [Design
Presentation Patterns](../paper-presentation/references/design-presentation-workflow.md), section
responsibility workflow, section presentation playbook, [Evaluation
Presentation and Rebuild Workflow](../paper-presentation/references/evaluation-presentation-workflow.md), Motivation Recovery
Workflow, systems-paper presentation patterns, concept–claim logic flow
workflow, outline-based presentation structure workflow, coarse-to-fine
refinement pipeline, claim rendering and tension workflow, subsection flow and
abstraction workflow, [presentation organization gate](../paper-presentation/references/presentation-organization-workflow.md), terminology and subsection workflow, guided paragraph
generation workflow, parallel section scope workflow, and presentation figure
workflow. Their files are the same shared references used by the orchestrator.
Use the fixed outline's exact section files, preserve its IDs and relations,
and never search for alternate outline files.

When reviewing a rendered prose round, also load the [iterative prose
refinement workflow](../paper-presentation/references/iterative-prose-refinement.md)
and the [frozen prose-round contract](../paper-presentation/references/prose-round-contract-workflow.md)
when a render contract is supplied. Reconstruct the output against that
contract, not only against the previous prose. Report first-paragraph,
node/edge, handoff, scope, and lexical drift as round-trip failures.
and review only the active round's gate. Round 1 checks semantic rendering;
Round 2 checks transitions, sentence load, branch relations, redundancy, and
concept layers; Round 3 checks concise English and semantic equivalence. Do not
use a Round 3 language finding to silently reopen an aligned outline.

The selected profiles add checks but do not relax the core criteria, the
paper's writing guide, or accepted author decisions. If review changes the
scope or discovers a different subsection archetype, recompute the active card
before continuing. The detailed procedure below is a dispatcher: apply a
domain-specific check only when its active profile is present, while keeping
the core criteria active for every review.

This review is source-first. Do not compile, open, or inspect a PDF for page
layout unless the author explicitly requests `visual-qa`, a PDF review, or a
final layout check. Figure-role review remains a source-level question and
does not by itself trigger rendered-page inspection.

For a paper-wide or multi-section review, if the active card triggers the
`terminology` profile, read [the terminology and subsection workflow](references/terminology-workflow.md)
and build its terminology ledger and subsection map. Use a narrower audit for
a local excerpt.

Identify the requested scope, manuscript version, author constraints, adjacent context, and any previous findings. Bind the review to the manuscript and criteria versions using revision identifiers or content hashes when available. For chat excerpts, assign a version label and retain the actual text. Do not infer that an excerpt is the whole paper.

When the author presents a poor subsection as material for a rewrite, classify
the review as `rebuild-from-material`. Audit the source prose for supported
facts, claims, scope, evidence, and terminology candidates, but treat its
paragraph order, sentence roles, transitions, and wording as non-authoritative.
Return an independent story and target-structure proposal or the smallest
decision needed to recover them. Do not make a source sentence or source
paragraph boundary part of the target merely because it exists.

Read applicable `AGENTS.md` files, their linked writing guides, and the
paper's [glossary](references/glossary.md), then read
the fixed outline files for the requested scope. For a nested manuscript
repository, include applicable parent-project instructions. Keep project
terminology in its canonical guide. Current author decisions supersede stale
examples. Flag unresolved conflicts with technical definitions. Missing
context limits the review, but does not prevent independent checks.

## Review procedure

1. **Freeze the active rule profile.** Record the active-context card and the
   triggered profiles before judging the text. If the requested scope contains
   more than one section or archetype, keep separate cards and do not apply a
   local profile to the whole paper.
2. **Read the whole requested scope and its fixed outline.** Identify its central
   question, section responsibilities, paragraph takeaways, evidence, and
   dependencies before judging individual sentences. Load the exact outline
   subtree from the fixed root and compare its paragraph and sentence
   roles, `from`, `needs`, source mappings, and `link`/`transition` fields with
   the manuscript. Check all supplied sentences, concepts, headings, and
   captions, not just conspicuous defects.
3. **Check section contracts when triggered.** When the active card includes a
   section-level or cross-section profile, select the supported section pattern.
   When Motivation and Design are in scope, run Motivation Recovery without
   using Design details. Record the setting, observations, pressure,
   opportunity, design-independent insight candidates, requirements, and
   unit-level leakage map. Then run a Design traceability pass and map each
   major choice to those prior requirements. Flag design leakage,
   naive-solution chains placed in Motivation, circular motivation, unmapped
   components, and requirements that remain open. For a local excerpt, keep
   the check to the section contract that the active card identifies.
   When Design is in scope, consult the [Design Presentation
   Patterns](../paper-presentation/references/design-presentation-workflow.md)
   and the aligned outline. Check the pattern selected during story/outline
   discussion, its node order, each unit's responsibility and contract, and
   the relations needed by that pattern. Flag a unit without a distinct
   responsibility, a lower-level mechanism introduced before its prerequisite
   when the selected pattern requires the separation, or a paragraph whose
   relations cannot be recovered. Do not impose a component/layout/update
   sequence when the aligned pattern does not use it.
   When the active card includes Evaluation, also run the [Evaluation
   Presentation and Rebuild Workflow](../paper-presentation/references/evaluation-presentation-workflow.md)
   and [Evaluation Patterns from Systems Papers](../paper-presentation/references/evaluation-reference-patterns.md).
   Recover the Evaluation-level progression when available, select the local
   archetype, and record the evaluation question before judging individual
   results. Keep the evaluation profile separate for each subsection when a
   scope contains multiple archetypes.
4. **Reconstruct the argument.** Build the argument inventory and dependency graph from the structural workflow. If an author blueprint is supplied, compile its paragraph contracts and first check whether the generated paragraph fulfills its declared role, incoming edge, evidence mapping, scope, and outgoing handoff. Also build the concept–claim node and edge inventory: identify undefined or premature nodes, dangling claims, broken or overstrong relations, wrong endpoints, lost scope, redundant nodes, and overloaded units. Record the current paragraph groups, their roles, the prerequisite each group needs, the evidence it interprets, and the handoff it should create. Mark each concept's abstraction layer and flag a term that is locally understandable but belongs to a later representation or implementation layer.
   In `rebuild-from-material`, keep the current paragraph groups only as
   source locators. Build a separate material ledger and classify each unit as
   protected fact/condition, candidate claim, scoped example, unresolved
   material, or non-authoritative presentation. Give each unit a disposition
   (`retain`, `relocate`, `merge`, `split`, `defer`, `drop`, or `needs context`)
   and recover the independent story before proposing the target paragraph
   order. For Evaluation, classify metric purpose, workload/configuration,
   evidence source, interpretation, cost, and limitation separately, and do
   not use the source paragraph grouping as the target.
   When the requested scope contains multiple subsections that may be revised
   in parallel, also record a subsection contract for each one: its local
   responsibility, incoming handoff, central claim, claims provided to later
   subsections, outgoing handoff, protected evidence and terminology, allowed
   local changes, and shared-edge owner. These contracts are revision
   interfaces, not additional prose requirements.
5. **Validate the outline-based structure.** Compile the current presentation-structure view from the fixed outline. If the prose or an author map conflicts with its hierarchy, grouping, order, roles, handoffs, evidence mappings, or protected content, report an outline delta. Generate alternatives only for decisions the outline marks as `proposal` or leaves explicitly open; do not maintain a second structure record. Compare alternatives by graph reachability, question answerability, forward flow, local context, reader backtracking, repetition, paragraph load, subsection autonomy, and restructuring cost. Do not force a linear chain when the supported argument branches, converges, compares, or qualifies a claim.
5a. **Run the presentation organization gate.** When the story and claim spine
    are already sound, independently reconstruct the presentation graph from
    the prose. Check paragraph grouping, sentence order, every adjacent
    sentence relation, and the information order of every opening. The opening
    must expose the paragraph's central subject or operation early; mentioning
    the incoming endpoint is not sufficient if the main concept is buried in a
    final clause. Consider merge, split, reorder, relocate, delete, and rewrite
    moves before accepting a wording-only repair. If the story, claim strength,
    evidence, terminology, and section responsibility remain unchanged, report
    a required presentation reorganization as a `Violation`, with a target
    organization and acceptance condition. Do not label it an optional style
    suggestion. Use the [presentation organization gate](../paper-presentation/references/presentation-organization-workflow.md)
    and return to outline alignment when grouping or sentence roles must change.
5b. **Reconstruct Evaluation when triggered.** Run the [Evaluation
   Presentation and Rebuild Workflow](../paper-presentation/references/evaluation-presentation-workflow.md)
   before accepting an Evaluation structure or sending findings to a writer.
   Record the Evaluation question, macro progression when the complete section
   is available, local archetype, and separate source, Design, evidence, and
   narrative orders. Build the claim–evidence matrix and map every result group
   to its question, metric purpose, workload/configuration, evidence,
   supported interpretation, cost or limitation, and outgoing handoff.
   If the local archetype is a design-centered performance breakdown, also
   record the proposed design as the focal subject, the headline result that
   precedes attribution, why the breakdown is needed, the baseline role and
   compression, and the relevance decision for each operation or implementation
   detail. The proposed design should receive the narrative weight; baselines
   are comparison anchors unless the question explicitly makes one a co-equal
   subject. Do not accept a baseline-first breakdown or an implementation tour
   that does not explain the focal metric, cost, boundary, or direct comparison.
   For a design breakdown, preserve Design order and locate the improved
   metric, introduced cost, and workload/configuration-dependent net effect for
   every component. For other archetypes, judge the narrative order from the
   question and dependency graph. In `rebuild-from-material`, mark inherited
   source organization as non-authoritative. If the proposed target retains the
   exact source order, require a dependency or evidence reason in the review;
   source order alone does not establish a valid presentation.
   Report the evaluation structure artifact and required moves, not only local
   metric or figure findings. The first-sentence-only verdict must recover the
   Evaluation question and progression without figure-by-figure backtracking.

5c. **Audit the semantic object graph and argument-node outline.** First
   reconstruct the typed object graph: concepts, claims, evidence, purposes,
   mechanisms, results, costs, conditions, and handoffs. Check that every
   mechanism, operation, metric, or result has a supported purpose or question
   edge, and that every cost and condition qualifies the right claim. Then for
   every paragraph in the requested
   scope, reconstruct or validate the argument nodes and their relations before
   judging prose. Check that each node has one main responsibility, a
   recoverable `from`, evidence or reasoning basis, scope, and a supported
   relation to the preceding node. Check that evidence nodes identify the claim
   they support, conditions remain attached to the claims they qualify, and
   handoff nodes provide the concrete endpoint needed by the next paragraph.
   Compare the full execution view with the sentence/logic-level human sync
   view and report any projection drift. A paragraph-only summary is an
   incomplete outline and must be reported before prose review proceeds. The
   reviewer must return node-level findings and acceptance conditions; it must
   not rewrite the manuscript or infer a target sentence from a writer's
   explanation.

6. **Audit lexical items, first use, and subsection autonomy.** Build the terminology ledger and extract technical nouns, noun phrases, adjectives, adverbs, verbs, and relation words used by the outline or prose. Every item needs a canonical concept, provenance, abstraction layer, scope, and semantic contract. Treat technical modifiers such as `efficient`, `fast`, `compact`, `direct`, or `scalable` as claims: require the property, comparison axis, scope, and support, or remove the modifier. Reject a new noun, adjective, synonym, operation verb, or relation verb that is not in the ledger, supplied material, or an author decision. For every needed concept, operation, input, and output, locate its first substantive use and check that the surrounding sentence gives an operational orientation: what it is, what it acts on, why it appears here, or what it enables. Check the concept's abstraction layer as well as its local definition. For every operation or state-changing verb, also check its semantic contract: actor, target or input, precondition, state transition, observable effect, and scope. A grammatical synonym is a violation when it changes that contract. For example, `resume` implies that a paused operation continues; it cannot stand for an unavailable index that cannot serve a request. In Motivation, require the capability or purpose before a proposed representation, encoding, identifier, data structure, or component. Flag a bare `request`, `sequence`, `state`, or similar noun when readers cannot recover its role. Flag defensive or tautological introductions such as `we define X as X` or an isolated `X is ...` sentence when the concept could be introduced naturally through the action or claim that uses it. Allow a standalone definition only for a central named abstraction, formal notation, invariant, or critical boundary that the paper repeatedly depends on. Flag variant drift when recurring concepts change form without a supported distinction. When the active profile concerns indexing, tracking, mapping, or association, check that the prose names the actual relation instead of using a passive or nominal phrase that hides it. For each subsection, verify a local question or purpose, the minimum required context, a canonical term mapping, and a forward-oriented handoff that does not require rereading the previous subsection. An ambiguous backward reference or an earlier-only premise is a finding when it blocks local understanding. Apply the [paragraph opening workflow](../paper-presentation/references/paragraph-opening-workflow.md): reading only the first sentence of each paragraph must reveal the subsection's progression, especially in Introduction, Motivation, and other sections before Design. Report the opening matrix for any structural or prose review.
7. **Audit figure roles when requested.** Use the figure workflow to classify candidate visuals as `required`, `beneficial`, `unnecessary`, or `blocked`. For each selected or existing figure, check its reader question, first placement, relation to the story spine, supported visual encodings, caption, source inputs, and final-size readability. A missing `required` figure is a finding only when the necessary relationship is not understandable from the supplied prose and evidence. A `beneficial` figure is a suggestion.
8. **Apply C01 through C09.** Record brief coverage notes with locators for definitions, relationships, evidence, and retained information. Review structure before local wording. Keep routine notes internal unless an audit record is requested. A pass comes from the final text and available context, not from familiarity with the topic or a writer's explanation.
9. **Check evaluation breakdowns when present.** After the Evaluation
   reconstruction gate, verify that the components follow the Design section's
   order. For every component, locate the improved metric, the introduced cost,
   and the net effect under the stated workload and configuration. A missing
   link, unsupported cost, or net conclusion that is detached from the measured
   conditions is a located presentation finding, not a request to run another
   experiment. This local check does not replace the question, archetype,
   narrative-order, and claim–evidence checks above.
   For a design-centered performance breakdown, additionally require the
   headline result before the breakdown and an explicit reason for the
   attribution. Check that the proposed design remains the subject, each
   baseline is compressed to the outcome or distinction needed for comparison,
   and unrelated Design operations are removed or relocated. Use performance
   vocabulary for a performance question; flag an access-path framing unless
   the evaluation question actually concerns access-path behavior.
10. **Check evidence introductions and metric-result openings.** For body prose that reports a figure or table observation, verify that the sentence leads with an explicit source clause such as `Figure X shows ...` or `Table Y reports ...`. Treat a parenthetical-only reference as insufficient when it is the sentence's only evidence introduction. For an Evaluation paragraph that introduces a metric or starts a metric-specific result, verify that its opening sentence briefly defines the metric or states its purpose before numbers or comparisons. Accept a direct continuation only when the immediately preceding context already provides a complete definition and purpose.
11. **Check local graph handoffs, claim rendering, and sentence simplicity.** At every adjacent sentence pair and paragraph boundary, identify the concrete result, object, metric, or pressure passed to the next unit. Verify that the next unit names the smallest necessary endpoint and states a supported relation or condition. The first sentence of the next paragraph must carry the transition and introduce that paragraph's responsibility; do not accept a detached handoff sentence at the end of the previous paragraph followed by an unrelated opening. Treat vague anaphora such as `These gains` as a finding when the referent is not recoverable without rereading or could refer to multiple outcomes. A transition is broken when the next unit requires an unstated premise, endpoint, or causal relation; adding a generic connective alone is not a repair. Check that a supported causal chain reaches the next paragraph's question and that the next paragraph does not reintroduce motivation that belongs at the end of the preceding paragraph. For a comparison, check that alternatives answer one shared question on comparable outcome/path axes and that the intended tension is visible. For a core tradeoff, check that both benefit and cost trace to the design choice or mechanism, with the net effect tied to its workload or configuration. For a design introduction, prefer the purpose-bearing opening and canonical term, and keep the first figure source clause next to the claim it explains. Flag sentences that combine multiple new concepts, causal steps, or nested qualifications when splitting them would make the relation easier to follow. Prefer a short sentence with one main logical relation; do not sacrifice a necessary condition or claim qualifier for brevity.
12. **Check supplied paragraph contracts.** When a blueprint is present, verify
    that every generated paragraph fulfills its declared role, incoming edge,
    evidence mapping, scope, and outgoing handoff. Treat a fluent paragraph
    that changes one of these as a presentation finding even if its local
    sentences sound polished.
13. **Classify each finding.** Use `Violation` for a located breach of a criterion or explicit author rule, `Needs context` when essential meaning or evidence cannot be determined, and `Suggestion` for a defensible but optional alternative. Explain the concrete reader obstacle or violated constraint. Do not turn preferences into mandatory changes or manufacture a quota of findings.
14. **Specify an acceptance condition.** State what the corrected text needs to make clear or preserve. For a Motivation finding, require a design-blind observation-to-opportunity chain, identify any leaked mechanism or naive-solution chain, identify concepts that are premature for the Motivation abstraction level, and state which units belong in Design or which high-level opportunity should replace them. For a Design mapping finding, require an explicit mapping from the component to a prior Motivation requirement. For a terminology finding, require one canonical mapping across prose, headings, captions, figure labels, equations, and tables, with intentional distinctions defined. For a first-use finding, require a short operational introduction integrated into the sentence that uses the concept, identifying its role, input or source, and purpose before its first dependent use; do not require a formal `we define` or isolated `X is ...` sentence when ordinary prose is sufficient. For an operation finding, require its relevant input, purpose, and effect/output to be locally recoverable. For a subsection finding, require a local question, minimum context, and an explicit forward handoff. For a first-sentence finding, require the paragraph opening to state its responsibility while carrying the smallest necessary endpoint from the preceding paragraph. For a structural finding, state the target unit order or grouping, the dependency it repairs, and the protected information that should survive. For an Evaluation structure finding, name the selected question or archetype, target narrative order, repaired dependency, and source units that move, merge, split, or remain. For a figure finding, require a supported reader question, placement, figure brief, source mapping, and consistent text/caption handoff. For an evaluation breakdown, name the required Design order and the missing metric, cost, or workload/configuration-dependent net effect. For evidence introductions, require a sentence-initial source clause. For metric-result paragraphs, require a brief definition or purpose sentence before the reported result. For a cross-paragraph handoff, require an explicit shared object, result, metric, or pressure and a supported relationship between the two paragraphs, carried by the next paragraph's opening rather than a detached closing sentence alone. For a claim-rendering finding, identify the shared comparison question, aligned outcome/path axes, reader-visible effect, causal source, and net-effect conditions. For a concept–claim flow finding, identify the missing, ambiguous, unsupported, overstrong, premature, or incorrectly connected node or edge and require the smallest supported repair. For a fluency finding, require a shorter sentence or a split at a concrete logical boundary without losing a qualifier or claim. For a guided-generation finding, require the paragraph's declared role, incoming and outgoing edge, evidence mapping, and scope to be preserved. Suggest a repair direction or a short illustrative phrase when useful, but do not produce a replacement manuscript. Acceptance concerns meaning and constraints, not whether the writer copies the reviewer's wording.
15. **Report complete findings.** Group repeated instances and list their locations. Prioritize section-contract, structural, terminology, subsection, visual, and meaning defects before cosmetic ones. Separate unresolved context from optional improvements. Do not limit coverage to the top few issues. When structure is materially defective, include a concise target outline delta with source and destination IDs so the writer can execute it without guessing. For a multi-subsection scope, also include the subsection interface map so independent writers can revise from one frozen baseline without reading one another's in-progress text. Report the active rule profile and why it was selected, the fixed outline path, revision/status, selected subtree/order, selected section pattern, Evaluation question/archetype/order artifact when Evaluation is active, Motivation Recovery status when relevant, alternatives, open decisions, and any drift from the reviewed artifact. For prose or structure review, include the paragraph-opening matrix or a concise first-sentence-only verdict. Include sentence-level role drift, missing `needs` or `from` mappings, broken `link`/`transition` relations, sentence-load findings, branch-relation findings, presentation-organization moves, and required outline changes. When an iterative prose round is active, identify the round-specific gate and do not report a later-round language preference as a structural defect. For a design-centered performance breakdown, report whether the headline result precedes attribution, why the breakdown is needed, whether the proposed design remains the focal subject, whether baselines are compressed to relevant comparison anchors, and which operation or implementation detail should be removed or relocated.

## Finding contract

When a presentation-organization finding is required, include the affected
paragraphs or sentence units, the reverse presentation graph that failed, the
selected organization move (`merge`, `split`, `reorder`, `relocate`, `delete`,
or `rewrite`), the target order or grouping, and the protected story/evidence
that remains unchanged. Treat this as a `Violation` when the reader cannot
recover the paragraph responsibility, sentence relation, or central opening
concept without backtracking. Do not classify it as a `Suggestion` merely
because the existing wording is grammatical.

For terminology review, include the active canonical term map and semantic
operation/state contracts for the affected terms. A review is incomplete if it
checks spelling or variants but does not verify that verbs preserve the actual
actor, precondition, state, effect, and availability behavior.

Give each issue a stable ID such as `P01`. Include:

- Kind and criterion ID, or the exact local author rule.
- Location in the reviewed version, plus a short quote or other direct evidence.
- The specific defect and its consequence for understanding or compliance.
- A concrete acceptance condition and, where helpful, a supported repair direction.
- For a section-contract finding, the sealed section result, leaked dependency or missing prerequisite, and the required cross-section mapping.
- For a terminology finding, the concept ID, canonical term, observed variants, and any distinction that must remain separate.
- For a semantic-term finding, the canonical operation or state contract,
  observed wording, changed actor/target/precondition/effect, and the required
  replacement or `Needs context` decision.
- For a subsection finding, the local question, missing context, and required forward handoff.
- For a guided-generation finding, the paragraph contract, the generated text
  that violates it, and the missing or changed role, edge, evidence mapping, or
  scope condition.
- For a fixed-outline finding, the outline path and stable paragraph or
  sentence ID, the declared role or `needs`/`from`/`link` contract, the prose
  drift, and whether the outline or manuscript is authorized to change.
- For a structural finding, the affected argument units, current and target order or grouping, and the dependency or section responsibility that justifies the change.
- For an argument-node finding, the node ID or paragraph location, role,
  missing or incorrect relation, evidence or scope mapping, and the acceptance
  condition for the execution and human sync views.
- For a semantic-object finding, report the node type and object, missing or
  unsupported purpose/question edge, evidence or scope gap, lexical-item
  provenance problem, and the acceptance condition for the semantic graph.
- For a figure finding, the classification, reader question, intended placement, source mapping, and visual property that must be corrected or preserved.
- State: `Open`, `Needs context`, `Resolved`, or `Dismissed`.

For example, an acceptance condition for an ambiguous numerical range identifies the system, metric, baseline, and dimension over which the range varies. It does not merely request "more detail." Keep separate issues when they require different fixes. When one passage violates several criteria through one defect, use one issue with the relevant IDs.

In `rebuild-from-material`, report the source-unit disposition map and the
independently recovered story before recommending prose changes. Distinguish
protected material from non-authoritative source presentation, and flag any
target proposal that simply inherits the old paragraph order without a
supported dependency reason.

## Verification procedure

Read the exact revised version and the shared criteria before examining the writer's explanations. Compare with the original and evidence to detect lost information or changed claims. Then reconcile the previous issue list and the writer's change map.

- Resolve an issue only when its acceptance condition is met in the revised artifact. Record the new locator and a short reason. The writer's `Addressed` status is a request for verification, not a resolution.
- Retain IDs for persistent issues. Dismiss a finding only with evidence that it was inapplicable or mistaken. Reopen regressions and give genuinely new defects new IDs.
- Reapply every relevant criterion to the entire requested scope, including unchanged sentences whose context or referents changed. Do not verify only the edited lines or carry over old pass judgments.
- Reconstruct the final hierarchy, unit order, responsibilities, sentence
  roles, and handoffs from the revised prose without consulting the writer's
  plan. Compare this reverse outline with the fixed outline and retain any
  mismatch as an outline finding. A fluent draft is not structurally verified
  when its reverse outline differs from the fixed outline.
- Reconstruct the argument-node graph from the revised prose without using the
  writer's process explanation. Compare node roles, relations, evidence,
  conditions, and sentence mappings with the canonical outline and its human
  sync projection.
- When a sentence-level realization contract is supplied, verify the closed-
  world trace before judging fluency: every slot has one concrete proposition,
  every output sentence maps to an existing slot, and no slot is silently
  replaced by a topic summary. Check the paragraph opening, incoming relation,
  evidence, scope, canonical terms, and produced endpoint for every paragraph.
  An untraceable or topic-only draft fails Round 1 even when its prose sounds
  plausible.
- For paragraph-by-paragraph materialization, verify each paragraph against its
  assigned node sequence, incoming/outgoing endpoint, evidence, scope, and
  canonical terms before checking the next paragraph. Then verify the
  subsection-level opening/endpoint migration. A local paragraph pass does not
  compensate for a broken cross-paragraph edge.
- When a frozen prose-round contract is supplied, perform the independent
  round-trip diff against that contract. Report first-paragraph responsibility
  drift, node or edge drift, handoff loss, evidence/scope drift, and unknown or
  changed lexical items as verification findings. Do not pass a failed artifact
  to a later prose round merely because it is fluent.
- If the manuscript or criteria change during review, identify the reviewed versions and recheck the affected scope before claiming the review is current. Do not let reviewer and writer modify the same draft concurrently.

Conclude with one scoped status: `Needs revision`, `Needs context`, or `No required findings in the checked scope`. Mark coverage as partial when material was unavailable or not checked. A review can be complete while issues remain open. Absence of findings is not a guarantee of an error-free paper, technical validity, or acceptance.

## Role boundary and handoff

The reviewer reads the manuscript and may write a review report or the
explicitly requested fixed-outline change to its destination.
Otherwise return findings and the outline delta in the conversation. Never change
manuscript files, invent evidence, request new experiments as a presentation
fix, or issue a scientific acceptance verdict.

For a combined review-and-revision request, pass findings, the target outline delta, and the version identifier to the caller for [paper-presentation-revise](../paper-presentation-revise/SKILL.md), then verify the resulting version. Do not treat completion of this review as completion of the combined task. The caller coordinates agents and owns final delivery.

The caller must preserve this role boundary: complete the review on one fixed
input version, freeze the findings and acceptance conditions, and only then
dispatch a separate writer call or sub-agent. If separate delegation is not
available, run the writer after a clean sequential handoff; do not combine
review and revision in one call and label the result independent.

For an automatic presentation loop, [paper-presentation](../paper-presentation/SKILL.md) is the caller. It owns round limits, fixed-version handoffs, and stopping conditions.

Use the user's language for findings and the manuscript's language for illustrative wording. Keep review commentary outside publication-ready text. Honor the requested reporting format, preserving all required findings and coverage limits.
