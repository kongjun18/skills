# Structural Presentation Workflow

Use this workflow when a review or revision must determine whether the
manuscript's presentation structure and reasoning chain are the best supported
ones. It applies to paragraph order, regrouping, section placement, and local
argument flow. It does not redesign the system, add experiments, or change a
scientific claim.

For cross-section work, combine it with the [section responsibility
workflow](section-workflow.md). Seal Motivation before reading Design, then use
the resulting contract as a prerequisite for the Design traceability map.
When the target structure needs a research precedent, consult the [systems-paper
presentation patterns](../../paper-presentation/references/research-presentation-patterns.md)
and transfer the underlying observation-to-design relationship rather than
copying a paper's surface section order.

## 1. Build an argument inventory

Read the complete requested scope and enough adjacent context to identify the
paper's question and terminology. Split the text into meaningful argument
units, which can be a sentence, a group of sentences, a paragraph, or a
heading-plus-body unit. For every unit, record:

- its role: question, observation, premise, definition, design choice,
  mechanism, evidence, result, interpretation, limitation, or implication;
- its concrete content and locator;
- the facts, numbers, conditions, and claim strength that must survive;
- the unit it answers, supports, motivates, or depends on;
- the evidence or context needed to understand it.

Do not treat a sentence as a unit merely because it ends with a period. Keep
one causal explanation together when splitting it would break the reasoning.

## 2. Reconstruct the dependency graph

Represent supported relationships between units explicitly. Useful edge types
include:

- `requires`: the reader needs A before B can be understood;
- `supports`: A is evidence for B;
- `causes` or `explains`: A supplies the supported reason for B;
- `motivates`: A establishes why B is needed;
- `contrasts`: A and B must be compared under a shared frame;
- `specializes`: B narrows or instantiates A.

Mark each edge as supported, ambiguous, or missing. A connective cannot repair
a missing premise or unsupported causal edge. The graph is a reasoning aid,
not a license to infer facts that the manuscript does not establish.

## 3. Generate and compare candidate structures

Do not assume that the current order is the target order, and do not apply a
reviewer's proposed order mechanically. Generate the smallest useful set of
candidate structures, usually the current order plus one or two alternatives.
Each candidate should specify paragraph groups, their order, and any units to
move, merge, split, or defer.

Reject a candidate that violates a hard constraint:

- it places a unit before a required premise or definition;
- it separates evidence from the claim it interprets without a clear reason;
- it mixes section responsibilities or changes the paper's scope;
- it loses a protected fact, condition, qualifier, or source mapping;
- it requires an unsupported relationship.

Compare the remaining candidates by these reader-facing criteria:

1. The section question is introduced and answered in a recoverable order.
2. Each paragraph has one main takeaway and advances the argument.
3. The next unit's prerequisites are available without backtracking.
4. Observations lead to opportunities, design choices, or conclusions through
   supported intermediate links.
5. Evidence is introduced before interpretation and remains near the claim it
   supports.
6. The structure minimizes repeated motivation, forward references, and
   reader rereading while retaining necessary context.
7. The amount of movement and restructuring is proportionate to the gain in
   comprehension.

Choose the candidate with the strongest supported reader path. If candidates
are equivalent under the available evidence, choose the simpler one and state
the ambiguity. Do not claim that a structure is globally optimal when the
manuscript does not determine a unique choice.

## 4. Produce a structural target

The target structure must be concrete enough to execute. For every changed
unit or group, state its source locator, target location, role in the target
argument, and the dependency it now satisfies. The target should also name:

- the opening question or observation;
- the paragraph-level takeaways in order;
- the final implication or handoff to the next section;
- any unresolved edge that cannot be repaired without author input or new
  evidence.

For a section transition, make the preceding section establish the reason the
next section is needed. Let the next section begin with its responsibility or
operation instead of repeating that motivation.

## 5. Execute and verify structural changes

During revision, apply the target order before sentence-level polishing. Keep a
unit ledger with `kept`, `moved`, `merged`, `split`, `deferred`, or `removed`
for every original unit. A removal requires a reason that the information is
duplicated or outside the authorized scope. A move across the requested edit
scope must be reported as a handoff rather than silently performed.

After revising, reconstruct the dependency graph from the final text. Recheck
all protected facts and source mappings, then read the final scope without the
plan or writer's explanation. A structural revision is complete only when the
reader can follow the target argument from the final text and no required
finding remains open.
