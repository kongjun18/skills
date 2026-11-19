# Author Style

The author's conventions for every paper. Apply them to manuscript prose and
to review comments whenever you write, refine, review, or clean a paper. A
project's writing guide adds rules for that paper and wins on conflict for
that paper. Rules already stated elsewhere in this skill (scoped claims,
supported adjectives, correctness versus performance arguments, figures as
claims, leading observations with their evidence) are not repeated here.

## 1. Argument principles

- **Make the design feel necessary.** Derive each mechanism from workload
  structure, a correctness constraint, or a resource bottleneck.
- **Start from the reader's problem, not the artifact.** Establish the
  concrete pressure before naming the proposed mechanism, and introduce a
  mechanism name only when the reader needs it. The paper should not read like
  an implementation manual before the problem is clear.
- **Separate observation, requirement, design choice, and evidence.**
- **State contracts before implementation.** Say what a component guarantees
  and what it does not guarantee before describing its data structures or
  policies.
- **Make tradeoffs explicit.** State what is lost, how the loss is bounded,
  and which later step preserves correctness.
- **Keep the abstraction level stable.** Do not jump from workload behavior
  to code details without an intermediate design concept.
- **Name the target.** Name the workloads, resource regimes, and failure
  cases the design targets instead of making universal claims.

## 2. Review checks

Check every sentence and paragraph for:

- **Concept completeness:** every concept, term, abbreviation, parameter, and
  paper-specific label is defined at first use or cross-referenced to its
  earlier definition.
- **Concept use in context:** each operation, property, relation, and
  quantity applies to the named entity. Do not silently replace the object or
  change the level of description.
- **Logical continuity:** the premise and consequence of every sentence and
  the question every paragraph answers are clear. Required context comes
  before the claim that depends on it.
- **One role:** every sentence and paragraph has one role in the argument,
  such as purpose, definition, method, evidence, explanation, or limitation.
- **No logical duplication:** merge repeated setup, definitions, and
  conclusions unless repetition is needed for an unambiguous referent.
- **Purpose in the same sentence:** a sentence that says what is done or how
  it is done also says why, with a concrete purpose supported by the evidence.
  - A purpose, constraint, or causal clause satisfies the check without
    `because`.
  - It applies to actions and methods, including experimental choices, not to
    observations. Do not relabel an action as an observation to escape it.
  - If no reason is supported, leave an explicit open item rather than
    inventing intent.

## 3. Prohibited wording and punctuation

Do not use the word `must`, semicolons, or dash punctuation in manuscript
prose or review comments.

- The `must` ban covers every capitalization. Keep the requirement's strength
  with `requires` or `is necessary for`.
- The semicolon ban covers the full-width `；`. The dash ban covers em and en
  dashes and LaTeX `--` and `---` in prose. Write `to` for prose ranges.
- The bans apply to headings and captions too. They do not apply to
  compound-word hyphens, minus signs, code, LaTeX syntax, identifiers, URLs,
  bibliography metadata, or verbatim quotations. Never substitute blindly
  across the source.

## 4. Prose rules

- **Name the object of an operation.** Name what is reused, recovered,
  restored, or matched whenever omitting it would make the reader infer it:
  `cache reuse`, not bare `reuse`, when the claim concerns cache availability.
- **Name the relation, not a nominal phrase.** State what a component does
  with an object: `the index maps each key to its location`, not `recorded
  entries`.
- **Avoid wrapper phrases.** Name the mechanisms directly: `existing systems
  use X and Y for Z`, with X and Y already introduced and the scope supported,
  not `existing systems generally implement these operations with ...`.
- **Introduce entities before they qualify claims.** Identify an entity and
  its role before calling it an instance, service, node, or replica. A state
  description does not identify the entity that holds that state.

## 5. LaTeX conventions

- **Cross-references:** write `\autoref{label}`, never `Figure~\ref`,
  `Table~\ref`, `Section~\ref`, `\S\ref`, or a hardcoded number. Append a
  panel letter directly, as in `\autoref{fig:x}a`.
- **Paragraph headings:** write a run-in heading as `\textbf{Title.}` at
  normal paragraph indentation, with no `\noindent` and no `\emph` or
  `\textit` styling. Use paragraph headings only in a group of parallel
  headings, and remove a lone heading or one that repeats its subsection title.
  Label steps inside a paragraph as `(1)~\emph{Step.}`.
- **Captions:** keep them short. Name what is plotted, map each panel, and
  include only visual-encoding keys the figure cannot show by itself. Put
  configurations, measurement procedures, timing boundaries, counting rules,
  and metric definitions in the body at or before the first reference. A
  caption may state the figure's main claim in one sentence with its number.
- **Accessibility descriptions** (`\Description`): state the chart or diagram
  type, the axes or visual objects, and the main trend or relation for screen
  readers. Do not copy the caption or the body text.
- **Clean up after a fix:** remove coauthor review annotations and obsolete
  commented prose once the requested fix is addressed.
