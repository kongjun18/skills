# Reasoning Effort Policy

Use this policy to allocate reasoning effort by decision difficulty, not by
manuscript length alone. The policy controls the work required in each phase;
the caller or model runner must apply the selected `reasoning_effort` value when
that interface is available.

## Default profile

Use `high` as the default. The presentation skill must spend its deepest
reasoning on reconstructing and verifying the argument graph, not on local
wordsmithing.

| Phase or mode | Default effort | Use a higher effort when |
| --- | --- | --- |
| `discuss` and candidate-structure search | `xhigh` | there are competing stories, cross-section dependencies, or more than one supported order |
| Motivation Recovery and section-pattern selection | `high` | the current Motivation mixes a naive solution with the problem, or multiple design-independent insights remain plausible |
| `guided` contract validation | `high` | incoming/outgoing edges, evidence mappings, or scope conditions are incomplete or ambiguous |
| `guided` paragraph rendering | `high` | the paragraph introduces several concepts, interprets evidence, or crosses a subsection boundary |
| claim rendering and tension | `high` | a comparison frame, benefit/cost attribution, or figure-to-claim relation is ambiguous |
| local guided rewrite | `medium` | the graph and contract are already stable and only wording is changing |
| `review` | `high` | `xhigh` for paper-wide review, independent verification, or claim/scope regressions |
| `revise` | `high` | `xhigh` for cross-section reordering or a disputed target structure |
| `visual-qa` | `high` | `xhigh` when page layout changes paragraph, figure, table, or cross-column comprehension |
| `auto` planning and structure | `high` | `xhigh` when structure alternatives remain unresolved |
| prose Round 1 semantic rendering | `high` | `xhigh` when sentence contracts, concept layers, or paragraph edges are incomplete |
| presentation organization gate | `high` | `xhigh` when the story is sound but paragraph grouping, sentence order, openings, or relations require competing reorganizations |
| prose Round 2 presentation/logic repair | `high` | `xhigh` for overloaded sentences, sibling alternatives, repeated handoffs, or layer/term regressions |
| prose Round 3 concise English polish | `medium` | `high` when transitions remain ambiguous after Round 2 or the scope crosses subsection boundaries |
| `auto` final verification | `xhigh` | always use it when the revised artifact changes order, scope, or claim strength |

The active rule profile is selected before effort allocation. A mismatch between
the first-sentence-only summary and the fixed outline is a structure problem,
so promote the paragraph-outline and affected downstream passes to `xhigh`.
Do not compensate for a broad, unfocused rule set by lowering effort. Narrow
the active profile first, then spend the saved attention on graph reconstruction
and independent verification.

Do not use `xhigh` for every paragraph by default. Once the paragraph contract,
terminology, evidence mapping, and graph edges are fixed, local prose can be
rendered at `medium` or `high` without reopening the story.

## Adaptive escalation

Promote the current phase by one level when any of these conditions holds:

- the concept–claim graph contains an ambiguous, missing, contradicted, or
  overstrong edge;
- two or more candidate structures remain plausible;
- Motivation, Design, and Evaluation are being changed together;
- a figure, metric, or table changes the interpretation of a claim;
- a reviewer reports a scope, evidence, terminology, or handoff regression; or
- the writer cannot preserve a paragraph contract without adding a premise.

Do not promote for spelling, punctuation, a single canonical-term replacement,
or a local sentence rewrite after the graph has passed verification.

If escalation still leaves missing evidence or an author decision, stop with
`Needs context`; do not spend more effort inventing a repair.

## Dispatch contract

When the runtime supports per-call effort, pass the selected value to the
reviewer, writer, or verifier for that phase. Keep the phase, effort, reason
for escalation, and input version in the round ledger. When per-call control is
unavailable, execute the same phases sequentially and include the phase
objective, graph checks, and stopping conditions in each prompt; report that
the runtime could not enforce distinct effort levels.

Effort is not a substitute for independent verification. The final reviewer
must read the fixed revised artifact and reconstruct its graph without relying
on the writer's self-report.
