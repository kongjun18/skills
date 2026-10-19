# Outline-Based Presentation Structure

The structured outline is the canonical presentation structure. Do not create
a second structure record. The outline contains the full sentence-level logic;
the presentation-structure view is the same outline projected to the levels
needed for a task.

Read [the fixed outline workflow](project-outline-integration.md) first. It
defines the only outline location, the section-file map, the stable IDs, and
the synchronization rules.
Also read [the argument-node outline workflow](argument-node-outline-workflow.md)
when the author is aligning a story, outline, or sentence-level logic. It
defines the execution view and the sentence/logic-level human sync view
derived from the same outline. A paragraph-only synopsis is not an aligned
outline.

For section responsibilities and default argument patterns, also read [the
section presentation playbook](section-presentation-playbook.md). When
Motivation and Design are both in scope, run [Motivation Recovery](motivation-recovery-workflow.md)
before compiling the Design traceability view.

## 1. Two views of one structure

Keep the paper's **story contract** as a diagnostic graph of supported
questions, observations, opportunities, requirements, design claims, evidence,
results, and limitations. It answers what the paper must establish.

Use the **presentation-structure view** to answer how the reader encounters
that story. It is generated from the fixed outline at all of these linked
levels:

- section/subsection: hierarchy, local question, responsibility, and handoff;
- paragraph: ordered argument units, roles, central claims, and evidence; and
- sentence: definitions, claims, evidence, costs, qualifiers, and transitions.

Within the sentence level, keep argument nodes explicit. A node is a logical
responsibility such as a claim, evidence item, explanation, condition, or
handoff; it may map to one sentence or to an authorized combination of adjacent
nodes.

For comparison and tradeoff units, sentence contracts also expose the shared
comparison question, aligned outcome/path axes, reader-visible effects, causal
sources, and net-effect conditions. These fields sharpen rendering without
creating a second presentation structure.

The story graph may expose a missing relation, but it cannot override the
outline's reader-facing order. A fluent story with an incomplete outline is
not ready for revision.

The outline is a target specification, not proof that its current sentence or
paragraph organization is good. After story alignment, independently compare
the prose's reverse presentation graph with the outline. If the story is
preserved but the organization is weak, update the outline through the
presentation organization gate. Do not preserve a poor grouping, sentence
order, or opening merely to avoid changing stable IDs. Stable IDs identify
argument units; they do not make their current boundaries authoritative.

## 2. Read and validate the fixed outline

Start from `<project-root>/scripts/paper/assets/outlines/README.md`, resolve the
requested section to the exact file named there, and read that file plus its
`_section.md` and `_figures.md` companions when present. Do not scan for other
outline-like files.

Validate the outline before writing:

1. every section and subsection has one local question and responsibility;
2. every paragraph has an ordered role and a recoverable incoming and outgoing
   handoff;
3. every sentence introduces concepts before dependent use and states its
   `from`, `needs`, and nontrivial `link`/`transition`;
4. every claim has an evidence or reasoning basis and a protected scope, and
   comparison or tradeoff claims record their reader-visible effects and
   causal sources;
5. every figure or table has a takeaway, source, placement, and citing sentence
   IDs; and
6. Motivation can establish its high-level problem and opportunity without
   reading later Design details, while Design choices map back to requirements.

Report a missing or contradictory field as an outline issue. Do not invent a
plausible endpoint, definition, number, or transition to make the outline
look complete.

## 3. Discuss and align the outline

When review finds a structural problem, propose a small outline delta with:

- the affected stable IDs;
- the current and proposed hierarchy or order;
- each unit's local question, role, incoming handoff, central claim, provided
  claims, and outgoing handoff;
- sentence-level changes to `from`, `needs`, `link`/`transition`, or scope;
- affected figures, terminology, and dependency edges; and
- the reason the proposed order improves reader answerability, local context,
  forward flow, subsection autonomy, or evidence proximity.

Store alternatives and the author's decision in the fixed outline's proposal
or change-log section. The status remains `proposal` until the author aligns
the grouping, order, and handoffs. Use `Awaiting outline alignment` and do not
dispatch writers while those choices are open.

After alignment, update the exact outline files and their change logs. The
outline revision is the structure version. The orchestrator should report the
outline path, version/status, and affected IDs rather than inventing a separate
`structure_id`.

Automatic mode may select among supported alternatives under its stated
policy, but it must write the selected choice and rejected alternatives into
the fixed outline. It may not keep the decision only in orchestration state.

## 4. Compile interfaces from the outline

For parallel subsection revision, derive each boundary packet from the exact
outline subtree and one frozen manuscript version. Include:

- owned paragraph and sentence IDs;
- the subsection's local question and responsibility;
- the incoming handoff from the preceding subtree;
- the central claim and claims provided to later subtrees;
- the outgoing handoff;
- protected evidence, terminology, qualifiers, workload, and configuration;
- allowed local reordering or rewriting; and
- shared-edge ownership.

The workers may revise prose within their subtree in parallel. A worker that
needs to change a handoff, order, role, or claim returns an outline delta. The
coordinator updates the fixed outline first, invalidates the affected
dependency cone, and then reruns those workers.

## 5. Verify the outline round trip

After integrating prose, reconstruct the hierarchy and sentence logic from the
final manuscript without looking at the outline. Compare the reverse outline
with the fixed files. Check missing, duplicated, reordered, or invented units;
lost definitions, qualifiers, evidence, or transitions; and boundaries whose
handoff no longer matches the declared claim. If the prose requires a real
structural change, update the outline and its change log rather than accepting
an unrecorded divergence.
