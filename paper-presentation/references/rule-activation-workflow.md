# Rule Activation Workflow

Use this workflow before a review, revision, guided generation, or automatic
iteration. Its purpose is to keep the full quality standard while presenting
the writer or reviewer with only the rules that apply to the current scope.
Conditional loading is a focus mechanism, not permission to skip a required
check.

## 1. Keep a small always-on core

The core rules apply to every paper and every stage:

- preserve the author's claims, evidence, scope, and terminology, and follow
  the paper's [glossary](../../paper-presentation-review/references/glossary.md) when one exists;
- reconstruct the argument before changing local prose;
- introduce a concept before a dependent claim, at the right abstraction
  level;
- give each sentence and paragraph one recoverable role;
- make adjacent units connected by a supported relation;
- keep prose simple enough to follow in one pass; and
- never invent facts, evidence, mechanisms, or causal links.

The core does not prescribe domain verbs, section-specific ordering, or a
particular paper structure. Those rules belong to conditional profiles.

## 2. Classify the current work before loading details

Create a small active-context card with these fields:

```text
scope: paper | section | subsection | excerpt
section: introduction | background | motivation | design | evaluation | related-work | other
archetype: story | comparison | logical-interface | algorithm | persistence |
           evaluation-result | evaluation-comparison | evaluation-breakdown |
           evaluation-ablation | evaluation-sensitivity | evaluation-scalability |
           evaluation-microbenchmark | evaluation-robustness | figure |
           terminology | other
stage: material-audit | story | structure | section-planning | semantic-graph | argument-nodes | evaluation-reconstruction | presentation-organization |
       local-paragraph-review | local-paragraph-revision | paragraph-outline | hierarchical-outline-research | outline-completion | claim-flow-materialization | concept-flow | semantic-render | presentation-repair |
       evidence | language-polish | verification
requested_mode: review | discuss | revise | rebuild-from-material | guided | auto | figures | terms
```

Infer the fields from the request and manuscript. If a field is ambiguous,
use the least specific profile and report the ambiguity. Do not activate a
profile merely because a word appears in the passage.

## 3. Load conditional profiles by trigger

Load only the profiles whose triggers are present, in this order:

| Profile | Activate when | Main responsibility |
| --- | --- | --- |
| `story-structure` | the task changes the story, order, grouping, or section responsibility | compare supported structures and freeze the reader path |
| `argument-nodes` | story alignment is complete and a structured outline, guided paragraph, or human sync view is being synthesized or checked | represent paragraph logic as role-tagged nodes with explicit relations, evidence, scope, and sentence mappings |
| `outline-completion` | the author supplies a paragraph-level chain or coarse internal logic without complete concrete sentence slots | expand the chain into the sentence-level realization contract, independently check it, and expose it for author alignment before prose |
| `hierarchical-outline-research` | the agent is expected to derive most of the outline from a rough story or paragraph plan | research and align L0 subsection claim, L1 paragraph claims/interfaces, and L2 sentence propositions in that order |
| `local-paragraph` | the request names one paragraph or a small contiguous scope for direct review or revision | compare the local reverse outline with the old outline, protect adjacent interfaces, and repair only the local contract when possible |
| `material-rebuild` | a poor source subsection is supplied as reference material or no aligned target exists for a rewrite | separate source evidence from non-authoritative source presentation and recover a new story before drafting |
| `presentation-organization` | the story is aligned but the prose graph, paragraph grouping, sentence order, or openings are weak | require an assertive organization review and permit supported merge/split/reorder/relocate/delete repairs |
| `section-planning` | the author provides a high-level section direction without a complete reader-facing outline | expand the direction into section purpose, content dimensions, argument nodes, evidence, and handoffs, then wait for outline alignment |
| `semantic-graph` | a story or structured outline is being prepared for author alignment or prose rendering | type the objects, claims, evidence, purposes, mechanisms, costs, conditions, lexical items, and supported relations before deriving sentence slots |
| `claim-flow-materialization` | the graph and paragraph contracts are aligned and prose is about to be written | freeze the complete claim flow, materialize one paragraph contract at a time in outline order, verify each paragraph, then check cross-paragraph migration |
| `motivation` | Motivation or Motivation–Design traceability is in scope | recover a design-independent opportunity and requirements |
| `design` | Design prose, Design–Motivation mapping, or component decomposition is in scope | use the Design pattern catalog while aligning the story and structured outline; check the selected pattern, responsibilities, relations, and consequences |
| `logical-interface` | a service, index, or component is described with operations and implementations | separate responsibility, selected operations, and implementation families |
| `comparison-tension` | alternatives or a design tradeoff are compared | align the comparison question, outcome axes, costs, and net effect |
| `evaluation` | Evaluation prose or any Evaluation subsection is in scope | recover the Evaluation question, macro progression, local archetype, claim–evidence relations, metric purpose, and evidence scope |
| `evaluation-rebuild` | Evaluation material is being rewritten from an old or structurally unreliable subsection | separate source, Design, figure, and narrative order; rebuild the target structure before prose |
| `figure` | a figure or table is selected, placed, or interpreted | bind reader question, source, placement, and takeaway |
| `terminology` | paper-wide terms, abbreviations, subsection independence, or technical lexical choices are audited | maintain the canonical term map, lexical provenance, modifier contracts, and first-use coverage |
| `prose-iteration` | the aligned story and outline are being rendered or refined through named rounds | activate only the checks for semantic rendering, presentation/logic repair, or concise English polish |
| `parallel` | independent subsection workers are dispatched | freeze versions, owned ranges, and shared edges |
| `visual-qa` | the author requests rendered-page or PDF inspection | inspect layout after source-level gates pass |

The section playbook selects the section pattern. The archetype profile then
selects the local information order. For Evaluation, read the [Evaluation
Presentation and Rebuild Workflow](evaluation-presentation-workflow.md) and
[Evaluation Patterns from Systems Papers](evaluation-reference-patterns.md) after
the section playbook. It first recovers the Evaluation-level progression and
then selects the local archetype. A stage profile controls what may still
change. For example, a Background logical-interface subsection normally loads
`story-structure` only if order is under discussion, `logical-interface`,
`terminology` when needed, and the current stage rules. It does not load
Motivation Recovery or Evaluation breakdown rules just because those files
exist in the skill.

When `section=evaluation` and `requested_mode=rebuild-from-material`, activate
both `evaluation` and `evaluation-rebuild`. The former selects the Evaluation
question and pattern; the latter prevents source paragraphs, figure order, and
old result grouping from silently becoming the new structure.

When `section=design`, activate the `design` profile and read the [Design
Presentation Patterns](design-presentation-workflow.md) while discussing the
story and structured outline. When Motivation and Design are both in scope,
run Motivation Recovery first, then use its sealed requirements as the Design
input. Do not use Design details to repair or justify Motivation. The Design
profile does not create a separate workflow stage; after outline alignment,
the independent reviewer and reviser check and render the selected pattern.

Set `stage=argument-nodes` after story alignment and before prose rendering
when the run is synthesizing, aligning, reviewing, or verifying an
argument-node outline or its human sync view. This stage is subordinate to the
fixed outline: it does not authorize a writer to change story, claims, or
shared edges.

Set `stage=semantic-graph` before `argument-nodes` when the run is building or
checking the intermediate semantic representation. A failed object, purpose,
evidence, or lexical-provenance gate keeps the run at this stage; do not hide
the failure in sentence wording.

Set `stage=claim-flow-materialization` only after the semantic graph, paragraph
contracts, sentence/logic slots, and terminology ledger pass alignment. This
stage freezes the claim flow and writes paragraphs sequentially. A paragraph
failure is rerendered from its contract; a cross-paragraph edge failure is
returned to outline or presentation-organization alignment.

Set `stage=outline-completion` when the author has supplied a story,
paragraph-level outline, or internal paragraph chain but not complete concrete
sentence slots. The discussion agent expands and independently checks the
sentence-level realization contract in this stage. It may fill supported
intermediate relations, but it cannot invent facts, mechanisms, terms,
evidence, or scope. Manual runs stop for author alignment; authorized
automatic runs record the selected supported completion before entering
`claim-flow-materialization`.

Set `stage=hierarchical-outline-research` when the agent is deriving the
outline itself from a rough story or paragraph plan. Produce and review the L0
subsection contract first, then the L1 paragraph claims and interfaces, then
the L2 sentence propositions. Preserve the parent-child mapping between the
levels. The author can edit any level after the research pass. Do not dispatch
a prose writer until the hierarchy and its interfaces are frozen.

Set `stage=local-paragraph-review` or `stage=local-paragraph-revision` when
the user directly requests work on one paragraph or a small contiguous scope.
Load the local paragraph workflow, compare the paragraph with the fixed outline
and both adjacent interfaces, and continue the local review even when the old
outline is stale. Rebuild only the local contract when interfaces are stable;
route a shared-edge change to outline alignment before changing neighboring
claims.

## 4. Use a narrow profile without weakening verification

The active profile controls drafting and local diagnosis. At the end of a
stage, run the core checks and every profile triggered by the final artifact,
including profiles whose boundary was changed during revision. Do not reread
unrelated examples or apply their vocabulary mechanically. A profile may add
checks, ordering, or terminology, but it cannot relax the core or a
paper-specific author decision.

Record the selection before dispatching a worker:

```text
active_profiles: [core, logical-interface, terminology]
inactive_profiles: [motivation, evaluation, visual-qa]
profile_reason: "Background subsection explains a global index and two selected operations"
stage_gate: "responsibility → operations → implementation families"
```

If a later finding changes the section, archetype, or stage, recompute the
card and reload the newly triggered profile before revising. Do not let a
worker silently import a rule from a different profile.

## 5. Keep domain relations conditional

Generic guidance should ask for the relation that the evidence supports. It
should not prescribe `tracks`, `maps`, `records`, or another domain verb for
all papers. The `logical-interface` profile may choose `tracks` for an index
that associates a sequence with block metadata, or `maps` when that is the
supported relation. A different component may store, routes, compares, or
produces something. Check the actor, object, and effect before selecting the
verb.

For an index or service, use this local profile order when supported:

```text
responsibility → stored association → selected logical operations
→ operation input/purpose/output → implementation families
→ per-family representation or procedure
```

Use “we focus on” for a representative subset of operations. Use exhaustive
interface language only when the source supports it. Do not introduce token
IDs, block IDs, radix trees, hashes, or other representations before the
operation or requirement that makes them relevant.

## 6. Pass the paragraph-opening matrix to every writer

For every paragraph, record:

```text
paragraph_id
local_responsibility
incoming_endpoint
supported_relation
opening_claim
provided_claims
outgoing_endpoint
design_boundary: before-design | design | post-design
```

The opening claim is the information a reader should recover from the first
sentence. It is not a heading paraphrase and it is not a detached preview.
The matrix is checked before prose rendering and again after revision.

