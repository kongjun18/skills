# Paragraph Opening Workflow

Use this workflow for outline design, guided generation, prose revision, and
verification. It gives paragraph-first sentences a separate structural gate.

## Opening contract

The first sentence of a paragraph carries two jobs:

1. it states the paragraph's own reader-facing responsibility or claim; and
2. when the paragraph is not the first in its unit, it carries the smallest
   concrete endpoint needed from the preceding paragraph and states the
   supported relation.

The sentence may also state a condition or scope when the paragraph's claim
would otherwise be misread. It should not repeat the preceding paragraph's
full explanation, preview a later paragraph, or introduce a lower-level term
before the paragraph needs it.

The paragraph's central subject, operation, or claim should appear early in the
opening, normally as the grammatical subject or in the first short clause. Do
not satisfy the incoming-endpoint requirement by placing the paragraph's main
concept in a long final clause. If the relation and responsibility overload one
sentence, shorten the relation, split the opening, or state the responsibility
first and carry the endpoint in the next sentence.

Use the following conceptual form, adapting it to the supported relation:

```text
[carried endpoint + relation] → [this paragraph's responsibility or claim]
```

Examples of relations include consequence, dependence, contrast, evidence,
specialization, and purpose. Choose the relation from the argument graph. Do
not add a generic “therefore” or “these gains” when the endpoint can be named
directly.

When adjacent paragraphs are sibling alternatives under one umbrella concept,
record that relation as `parallel-alternative` or `contrast`. The next opening
should name the shared parent or the relevant endpoint and make its branch
relationship visible. It should not introduce a second object as if it were an
unrelated list item. A supporting mechanism, caveat, or example should be
marked as a side branch when it does not own the subsection's main progression.

Keep the opening at the paragraph's current abstraction level. Before Design,
prefer the problem, observation, pressure, opportunity, or requirement over a
representation or mechanism. Keep one main logical relation in the opening;
move supporting definitions, evidence, and implementation details to later
sentences unless the paragraph cannot be understood without them.

## First-sentence-only test

Read only the first sentence of every paragraph in order. Before Design, a
reader should recover the subsection's high-level framework: the setting or
question, the observation or pressure, the resulting opportunity or
requirement, and the reason the next paragraph follows. The test does not
require every detail or every caveat. It requires the correct sequence of
responsibilities and the main claims.

For a Design subsection, the first sentences should recover the selected
order, such as responsibility, operation, structure, procedure, and
consequence. For Evaluation, they should recover the question, metric or
evidence purpose, result, and interpretation. For a comparison, they should
expose the common question and the aligned alternatives.

Fail the test when a reader must inspect later sentences to learn what the
paragraph is about, must reread the preceding paragraph to identify the
referent, or sees a list of details whose hierarchy is not visible from the
openings.

## Paragraph-opening review matrix

For each opening, record:

| Field | Check |
| --- | --- |
| carried endpoint | Is the shared object, result, metric, or pressure named directly when needed? |
| relation | Does the opening say why this paragraph follows? |
| responsibility | Can the reader state what this paragraph establishes? |
| abstraction | Does it stay at the section's current level? |
| prerequisites | Are required concepts available without backtracking? |
| scope | Are workload, configuration, or comparison conditions attached when needed? |
| terminology | Does it use the canonical term? |
| branch relation | If this paragraph is a sibling alternative, does the opening name the common parent and branch relation? |
| handoff | Does the paragraph provide a concrete endpoint for the next opening? |

## Before-Design protection

For Introduction, Motivation, and other sections before Design, classify every
opening as one of `setting`, `observation`, `pressure`, `opportunity`,
`requirement`, or `design-independent insight`. A proposed representation,
identifier, data structure, algorithm, policy, or component cannot appear in an
opening merely because it will later solve the problem. If an opening only
makes sense after reading Design, rewrite it at the opportunity or requirement
level or move it to Design.

The first-sentence-only test is a structure test, not a request to make every
sentence vague. Once the framework is recoverable, later sentences may add
definitions, evidence, mechanisms, and qualifications at the appropriate
level.

## Revision and verification

During revision, repair the paragraph contract or order before polishing the
opening. Preserve the paragraph's claim, evidence, scope, and outgoing
handoff. Do not append a handoff-only sentence to the previous paragraph when
the next opening can carry the relation directly.

If the story is already correct but the opening, grouping, or sentence order
is not, explicitly consider merging, splitting, reordering, relocating, or
deleting units. A fluent local rewrite is insufficient when the reader still
cannot see the paragraph's responsibility from its first sentence.

After revision, run the test without consulting the outline or writer's
explanation. Compare the resulting first-sentence summary with the fixed
outline. A mismatch is a structural finding, even if every individual
sentence is fluent.

