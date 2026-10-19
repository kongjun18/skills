# Presentation Orchestration Contract

Use this state model for manual handoffs and automatic rounds. The structured
outline at the fixed project path is the durable presentation structure. This
state records which outline version and subtree a run used; it does not create
a parallel structure artifact. The argument-node execution view and human sync
view are projections of that same fixed outline.

## State

Maintain these fields for the current run:

- `mode`: `review`, `revise`, `rebuild-from-material`, `discuss`, `sections`,
  `figures`, `terms`, `guided`, `visual-qa`, or `auto`;
- `workflow_stage`: `material_audit`, `local_paragraph_review`, `local_paragraph_revision`, `awaiting_story_alignment`, `review`,
  `awaiting_alignment`, `outline_synthesis`,
  `outline_completion`,
  `awaiting_outline_alignment`, `section_planning`, `semantic_graph`, `evaluation_reconstruction`, `presentation_organization`, `interface_freeze`, `revision`,
  `prose_refinement`, `claim_flow_materialization`, `visual_qa`, or
  `verification`;
- `iteration_plan`: the finite prose-round plan, including the round limit,
  round goals, required gates, whether the run is automatic or manual, and
  whether `draft-only` was explicitly requested;
- `iteration_round`: `not-started`, `semantic-rendering`,
  `presentation-logic-repair`, `concise-english-polish`, or `complete`;
- `iteration_history`: per-round input/output versions, findings, gate result,
  reviewer, writer, and rollback target;
- `render_contract`: immutable prose-round contract revision, protected node,
  edge, lexical, evidence, scope, and paragraph-opening IDs, plus the
  round-specific allowed change budget. Every writer and verifier reads this
  same contract; a prior prose version never replaces it;
- `round_trip_diff`: the independent comparison of each output with the
  render contract, including missing or invented nodes, changed node order or
  roles, edge/handoff drift, lexical drift, scope/evidence drift, and the
  rollback target;
- `review_gate`: the immutable review artifact, reviewed manuscript and outline
  versions, required findings, acceptance conditions, author dispositions, and
  whether the review barrier passed before revision;
- `reviewer_identity`, `writer_identity`, and `verifier_identity`: separate
  agent or call identities for the current review, revision, and verification
  phases; a self-review is not an independent review;
- `agent_handoff_barrier`: the frozen input versions, outline revision,
  acceptance conditions, and role-specific readable artifacts passed to each
  agent. Reviewer findings are immutable inputs to revision, and writer
  process notes are unavailable to verification;
- `refinement_stage`: `motivation_recovery`, `story`, `architecture`, `section_planning`, `semantic_graph`, `evaluation_reconstruction`, `presentation_organization`, `claim_flow_materialization`, `paragraph`, `argument_nodes`, `sentence`,
  `claim_rendering`, `semantic_rendering`, `evidence`, `final_polish`,
  `visual_qa`, or `verification`, with its gate result and the
  earliest failed stage when verification finds a regression;
- `scope`: files, sections, paragraphs, or excerpt boundaries;
- `input_version` and `output_version`: content hashes or stable revision IDs;
- `reference_material`: the immutable source version, source-only scope, raw
  source locators, authority classification, and whether the source is a
  drafting template (normally `false` in rebuild mode);
- `source_disposition_map`: per-source-unit `retain`, `relocate`, `merge`,
  `split`, `defer`, `drop`, or `needs context` status, destination contract, evidence
  mapping, and reason;
- `source_structure_status`: the old paragraph order, roles, transitions, and
  wording marked as `non-authoritative`, plus any explicitly protected source
  structure;
- `constraints`: writing guide, paper [glossary](../../paper-presentation-review/references/glossary.md), author decisions,
  venue context, and edit authorization;
- `author_alignment`: accepted, rejected, deferred, and unresolved findings,
  selected outline changes, protected content, and approved scope changes;
- `continuation_route`: the author's response classified into finding, story,
  structure, prose, and authorization decisions; the automatically selected
  next stage; and the artifact or decision that stage requires;
- `outline`: `outline_root=<project-root>/scripts/paper/assets/outlines/`, its
  fixed index path, exact section files, outline status, outline revision,
  manuscript version, and selected subtree;
- `presentation_structure_view`: a transient section/subsection/paragraph
  projection compiled from `outline` for the current task; never persist it as
  a second structure artifact;
- `argument_node_view`: the execution projection of argument nodes, including
  stable IDs, roles, relations, evidence, scope, and sentence mappings;
- `semantic_object_graph`: typed concept, claim, evidence, purpose, mechanism,
  result, cost, condition, metric, and handoff nodes; supported relations;
  lexical-item provenance; and graph-gate findings. This is the canonical
  semantic intermediate representation used to derive argument nodes and
  sentence slots;
- `human_sync_view`: the author-facing sentence/logic-level projection of the
  same outline, including paragraph navigation, every sentence slot or logical
  node, role-tagged summaries, and visible relations. It is generated from
  `outline` and cannot become an independent source of truth;
- `outline_drift`: missing or changed paragraph/sentence roles, `from`,
  `needs`, `link`/`transition`, source mappings, figure contracts, or change
  log entries between the outline and prose;
- `motivation_contract`: the sealed high-level setting, observations, pressure,
  opportunity, design-independent insight candidates, requirements, and
  unit-level leakage map established without reading Design;
- `motivation_recovery`: sealed input scope, classified units, candidate
  opportunities or insights, evidence mappings, unresolved alternatives, and
  alignment status;
- `section_playbooks`: selected section pattern, local reader question,
  abstraction level, handoffs, evidence scope, and rationale for each section;
- `design_presentation`: when Design is in scope, the pattern selected during
  story/outline discussion, its rationale, reader-facing node order,
  component responsibilities and contracts, and any applicable
  representation, operation, invariant, cost, or handoff relations. This is
  part of the aligned outline and is absent when Design is not in scope;
- `design_traceability`: the mapping from each major Design choice to a prior
  Motivation requirement, including unmapped choices and open requirements;
- `terminology_ledger`: seeded from the paper glossary; concept IDs, canonical terms, definitions, allowed
  forms, variants, distinctions, lexical-item provenance, and technical
  modifier contracts;
- `term_provenance`: for each technical term, its concept ID, abstraction layer,
  canonical form, decision source, status (`active`, `superseded`, or
  `disputed`), allowed context, and forbidden generalization;
- `term_validation`: semantic contracts for operation/state terms, including
  actor, target or input, precondition, state transition, observable effect,
  scope, observed wording, and reviewer verdict;
- `subsection_map`: local questions, required context, takeaways, and forward
  handoffs;
- `author_blueprint`: the author's supplied section or paragraph roles, order,
  graph edges, protected facts, evidence mappings, and scope conditions;
- `outline_completion`: the coarse-to-sentence expansion artifact, including
  the input paragraph chain, generated slot propositions and relations,
  independent outline-review findings, author edits, unresolved alternatives,
  and the frozen execution-contract revision;
- `hierarchical_outline`: the aligned L0 subsection contract, L1 paragraph
  claims and incoming/outgoing interfaces, L2 sentence propositions and
  relations, plus the author-facing projection and outline-research findings;
- `local_paragraph_route`: the frozen local paragraph scope, adjacent
  interface endpoints, reverse-outline comparison status, local contract,
  outline delta, and whether the shared interfaces remained unchanged;
- `paragraph_contracts`: contracts compiled from outline subtrees, including
  local role, incoming and outgoing edges, required concepts, allowed evidence,
  protected claims, and unresolved context;
- `claim_flow_materialization`: the frozen subsection claim graph, ordered
  paragraph contracts, per-paragraph passing versions and node-to-sentence
  mappings, plus the subsection-level opening/endpoint migration result;
- `paragraph_execution`: the current subsection's ordered paragraph queue,
  current paragraph, passing paragraph versions, verified endpoints, failed
  rerender attempts, and the gate that permits the next paragraph to start;
- `sentence_contracts`: sentence IDs, roles, required content, `from`,
  `needs`, `link`/`transition`, relation type, sentence-load expectation,
  semantic object IDs, argument-node IDs, evidence mappings, and protected
  scope;
- `sentence_realization_contract`: the closed-world ordered slots for each
  paragraph, including one concrete proposition, reader question, incoming
  relation, evidence, scope, canonical terms, provided claim, opening
  requirement, allowed merges, and forbidden additions. It also records the
  proposition/opening gate and the sentence-to-slot trace for each passing
  paragraph;
- `presentation_organization`: reverse presentation graph, paragraph opening
  findings, sentence and paragraph organization moves (`merge`, `split`,
  `reorder`, `relocate`, `delete`, `rewrite`), target organization, and gate
  result;
- `evaluation_presentation`: selected Evaluation-level progression or local
  archetype, evaluation question, separate `source_order`, `design_order`,
  `evidence_order`, and `narrative_order`, claim–evidence matrix, paragraph
  responsibilities, source-unit dispositions, and reconstruction gate result.
  For a design-centered performance breakdown, also store the focal design,
  headline result before attribution, breakdown purpose, baseline role and
  compression, and operation/detail relevance decisions;
- `claim_rendering_contracts`: comparison questions and aligned outcome/path
  axes, reader-visible effects, mechanisms, causal sources, net-effect
  conditions, canonical terms, and figure anchors for the units that need
  them;
- `generation_trace`: the contract-to-prose mapping, sentence-to-slot trace,
  unresolved gaps, and round-trip graph findings for guided generation;
- `effort_policy`: the selected default, phase-specific effort, escalation
  triggers, and whether the runtime enforced per-call values;
- `scope_manifest`: fixed manuscript version, fixed outline revision, owned
  subsection and paragraph IDs, read-only boundary context, shared edges, and
  coordinator;
- `subsection_contracts`: local responsibility, incoming handoff, central
  claim, provided claims, outgoing handoff, protected evidence and terminology,
  allowed local changes, and shared-edge owner for each owned subsection;
- `parallel_proposals`: proposal outputs from workers, including touched nodes
  and edges, expected handoffs, terminology changes, and unresolved context;
- `outline_deltas`: explicit changes proposed or applied to hierarchy, order,
  roles, claims, evidence, source mappings, or sentence relations;
- `revision_patches`: isolated worker patches tied to an input version,
  outline revision, and owned-unit set, plus merge status and conflicts;
- `merge_conflicts`: overlapping units, stale-version patches, boundary
  disagreements, and their resolution or `Needs context` status;
- `story_spine`: supported question, problem setting, observations,
  opportunity, insight, design, evidence, result, and conclusion;
- `figures`: candidate classification, figure briefs, placement, source inputs,
  rendering route, artifact version, and visual verification;
- `visual_qa`: bound source and rendered-artifact versions, compilation route,
  pages inspected, page/source locators, visual findings, authorized fixes,
  rerun status, and unresolved layout or source-flow issues;
- `concept_inventory`: concepts, operations, observations, claims, requirements,
  evidence items, design decisions, mechanisms, results, and limitations;
- `logic_graph`: supported, ambiguous, missing, or contradicted edges among
  those nodes, including prerequisite, support, motivation, explanation,
  contrast, scope, and subsection-handoff relations;
- `argument_inventory`, `dependency_graph`, `issues`, `change_map`, and
  `verification`: the corresponding review, change, and verification state.

Keep claims and decisions distinct from hypotheses. Do not carry a writer's
`Addressed` status forward as reviewer `Resolved`.

## Version handoff

Every review or verification pass reads one fixed manuscript version and one
fixed outline revision. A writer receives both, the relevant outline subtree,
issue list, acceptance conditions, protected-content list, and unresolved
decisions, plus the argument-node execution view. The author-facing sync view
is for alignment and is regenerated from the same outline revision. After
writing, record a new manuscript version; update the outline only when
structure, claims, evidence requirements, argument-node relations, or sentence
relations changed. Never verify only a diff when a move or merge changes
context.

The reviewer, reviser, and verifier are separate calls or sub-agents, and
each receives the glossary path. The
reviewer is read-only; the reviser receives the frozen review artifact but
cannot rewrite its findings; the verifier receives the integrated revision and
acceptance conditions without relying on the reviser's self-check or process
explanation. The coordinator alone updates the canonical outline, merges
patches, and resolves shared edges.

## Status values

- `Complete`: no required findings remain in the checked scope;
- `Awaiting alignment`: review is complete, but claim decisions remain;
- `Awaiting story alignment`: source material has been audited, but the
  independently recovered story or its alternatives still need author choice;
- `Awaiting outline alignment`: story or claims may be aligned, but hierarchy,
  order, grouping, or handoffs in the fixed outline remain open;
- `Needs revision`: required findings remain and supported edits are possible;
- `Needs context`: progress depends on missing evidence or an author decision;
- `Partial`: requested scope or verification inputs were unavailable; and
- `Limit reached`: the iteration limit stopped the loop before all findings
  closed.

These statuses describe workflow state. They are not scientific quality scores
or acceptance recommendations.

## Round ledger

For each automatic round, record:

1. iteration ID, named round, round goal, and input manuscript version;
2. fixed outline revision, active profiles, and selected effort;
3. focused findings, protected claims, and round acceptance conditions;
4. outline changes, author decisions, and any rollback to an earlier round;
5. revision output version, patch merge, and change map;
6. independent verification result, including reverse-outline and
   first-sentence status;
7. final English-polish semantic-equivalence result when Round 3 ran;
8. visual QA result when the explicit `visual-qa` mode was requested; and
9. next action or stopping reason.

Keep the ledger concise. It should let a reader reconstruct why the final
manuscript and outline versions were selected without rereading discarded
drafts.
