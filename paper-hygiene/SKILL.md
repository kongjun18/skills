---
name: paper-hygiene
description: Independently audit and safely clean an academic paper's source and rendered PDF for mechanical errors, accidental duplication, terminology drift, section artifacts, figure/table clipping or placement errors, float whitespace, and very short final lines. Apply only meaning-preserving local fixes; route argument, section-responsibility, and presentation-structure decisions to a presentation review or revision skill.
---

# Paper Hygiene

Use this skill for the paper's **surface integrity pass** after the technical
content is settled. It complements `paper-presentation-review` and
`paper-presentation-revise`; it does not replace them. The target is a paper
that says the same thing, uses the same objects and evidence consistently, and
renders without avoidable whitespace, float placement defects, or mechanical
errors. Every check below is an independently executable unit; running one
unit does not imply that the others ran.

## Non-negotiable boundary

An edit is eligible for direct application only when all of the following are
true:

1. The defect is visible in the supplied source or rendered artifact.
2. The intended correction is recoverable from the paper, its terminology
   guide, or an explicit author decision.
3. The change does not alter a claim, qualifier, number, evidence binding,
   causal relation, paragraph responsibility, section responsibility, float
   meaning, concept inventory, or canonical terminology.
4. The change can be checked again after recompilation.

Otherwise record a located finding and stop at `Needs context`. In particular,
do not invent a missing section, rewrite a section for better flow, merge two
paragraphs because they seem repetitive, or choose between two technical terms
from memory. Those are presentation or semantic decisions.

## What this skill covers

| Area | Directly fix when clear | Report and defer when unclear |
| --- | --- | --- |
| Mechanics | Grammar, spelling, punctuation, agreement, articles, malformed local sentences, and an unambiguous word-choice slip | A rewrite that changes emphasis, claim strength, or technical meaning |
| Repetition | Exact duplicate text, or a clearly accidental semantic duplicate with the same role and evidence | Two passages that share a topic but have different scope, role, or evidence |
| Sections | Duplicate/empty headings, orphaned `\input`/`\include`, broken local numbering or cross-reference, and visible TODO residue | A conceptually missing section, a section move, or a new subsection whose responsibility is not specified |
| Terminology | A local variant when a canonical term is established and the object is the same | A choice between distinct objects, layers, states, or operations |
| References and labels | Broken local references, mismatched figure/table/equation labels, unresolved keys, and stale local names | A citation or attribution whose correctness needs external or scientific judgment |
| Figures and tables | Clipped panel titles, missing labels, detached captions, wrong source order, a float before its first use, or a float that interrupts a paragraph or appears under the wrong subsection heading | A placement change that requires reordering the argument, changing a figure/table's role, or inventing a new visual |
| PDF layout | Safe float/caption spacing or local reflow that preserves order and content | Margin, font, figure size, float order, or template changes without authorization |
| Paragraph tails | Delete a demonstrably dispensable local word or phrase when a rendered final line has at most two words | Any shortening that changes scope, strength, terminology, concept inventory, or sentence logic |

The canonical object must win over a near-synonym. For example, if the paper's
ledger says that a prefix's candidate is an **alternative**, a later accidental
use of **continuation** is a terminology defect only when the surrounding
passage clearly denotes that same object. If the two words may denote different
objects, leave the text unchanged and request context.

## Modes

Every mode performs its own intake, baseline render, scoped check, and
verification. A mode must not silently depend on a previous mode's report or
edits.

- `mechanics`: grammar, spelling, punctuation, agreement, and unambiguous
  local word-choice errors.
- `duplicates`: exact or clearly accidental semantic duplicate paragraphs.
- `structure`: duplicate/empty headings, missing source inclusions, visible
  section artifacts, and broken local heading/label structure.
- `terminology`: canonical object and operation names, including local slips
  such as `continuation` for an established `alternative`.
- `references`: local figure/table/equation labels, cross-references, and
  unresolved keys.
- `floats`: figure/table clipping, panel-title visibility, caption attachment,
  source/PDF order, first-use placement, subsection ownership, and paragraph
  interruption.
- `whitespace`: physical gaps and widow/orphan spacing only; it does not move
  figures or tables.
- `tails`: rendered prose paragraphs whose final line has at most two words.
- `audit`: read-only run of one or more selected units; produce findings and
  acceptance conditions without editing.
- `auto`: run all units in a fixed sequence. Use this only when the user asks
  for the complete hygiene pass.

If the user names one unit, run only that unit. `cleanup` may be accepted as a
compatibility alias for the explicitly named source units, but it must not
silently include `floats`, `whitespace`, or `tails`.

## Independent-run contract

For a selected unit, create a fresh run record containing the source revision,
PDF hash, build command, requested scope, and unit name. Rebuild or validate a
baseline before making edits, even if another unit was run earlier. Apply only
the selected unit's edits. Then run that unit's verification gate and report
unrelated findings as deferred observations rather than fixing them in the
same run.

## Pipeline

The intake and verification gates apply to every independent mode. In `auto`,
run the units in this order: `mechanics`, `duplicates`, `structure`,
`terminology`, `references`, `floats`, `whitespace`, and `tails`. In a
single-unit run, execute only the corresponding subsection below and omit
changes from every other unit.

### 1. Intake and freeze

Locate the manuscript source, bibliography, build command, template/style
files, current PDF, figures, and applicable `AGENTS.md` or writing guide.
Record the source revision and PDF identity. If only a PDF is available,
perform `audit` and report the limits; do not edit a PDF as if it were source.

Create build products and page renders in a scratch directory outside the
manuscript tree. Preserve unrelated working-tree changes. Read
[the detailed workflow and ledgers](references/workflow.md) when the paper has
multiple source files or more than one class of finding.

### 2. Establish a baseline

Compile using the repository's documented command. If no command exists, use
the least invasive available command (`latexmk`, then the documented TeX
engine) and record it. Save:

- the PDF page count and a content hash;
- compiler warnings, especially overfull/underfull boxes and unresolved
  references;
- `pdftotext -layout` output for line and paragraph inspection;
- page renders at a readable print-oriented resolution (normally 150--200
  dpi); and
- a baseline inventory of headings, paragraphs, labels, floats, captions,
  citations, technical objects, and canonical terms.

Source text alone cannot establish a visual defect. A layout finding requires a
rendered page or an equivalent layout trace.

### 3. Run the selected source integrity unit

Read the complete requested scope before editing. Build only the ledgers needed
by the selected unit; a paper-wide run may use these four shared ledgers:

1. **Heading tree:** section/subsection order, source location, labels, and
   included files.
2. **Paragraph inventory:** stable source locator, heading, opening, role,
   key object, evidence, and outgoing endpoint.
3. **Terminology ledger:** canonical object, allowed aliases, forbidden or
   suspicious variants, abstraction layer, and evidence for the choice.
4. **Artifact map:** figure/table/equation labels, captions, float placement,
   and cross-references.

The source integrity stage is split into independent units:

- `mechanics` checks grammar, spelling, punctuation, agreement, malformed local
  sentences, and unmistakable word-choice slips.
- `duplicates` compares proposition, scope, evidence, and role for exact and
  semantic duplicate paragraphs. It does not merge paragraphs for smoother
  flow.
- `structure` checks empty or duplicated headings, missing `\input`/`\include`
  files, duplicate labels, visible TODO residue, and accidental source
  inclusion. A conceptually missing section remains a deferred presentation
  finding.
- `terminology` checks the canonical object ledger and repairs a local variant
  only when the referent is already established.
- `references` checks figure/table/equation keys, local labels, and rendered
  targets. Citation correctness that needs external or scientific judgment is
  deferred.

For the selected unit, check the complete requested scope for its concrete
defects:

- grammar, spelling, punctuation, agreement, and malformed local sentences;
- exact duplicate paragraphs and semantic duplicates across sections;
- empty, duplicated, unreachable, or visibly accidental headings;
- missing source inclusions, stale local labels, unresolved references, and
  editing notes;
- inconsistent names for the same system, component, operation, state, metric,
  workload, or configuration; and
- mismatched figure/table/equation names or caption references.

For semantic duplication, compare proposition, scope, evidence, and role. Keep
the occurrence that is better supported by the local section contract. Delete
or compress the other occurrence only when its role is clearly accidental;
otherwise report both locations and defer to presentation review.

### 4. Apply bounded source fixes

Edit the smallest source span that resolves the defect. Keep a change ledger
with the issue ID, source location, before/after text, evidence for the fix,
and the invariant it preserves. Do not perform a document-wide synonym sweep
without a canonical ledger and a reviewed object map.

After each coherent batch, recompile and rerun the local checks. If a fix
changes a paragraph's role, adds a concept, changes claim scope, or requires a
new transition, revert that fix and return it as `Needs context`.

### 5. Inspect and repair figure/table placement (`floats`)

Run this unit independently from `whitespace`. Build a float ledger containing
the figure/table ID, source location, environment and placement options, first
textual reference, owning section/subsection, rendered page, panel/caption
status, and the order of neighboring floats.

Inspect the source and rendered pages together. For every figure and table,
check:

- panel titles, axis labels, legends, table headers, and captions are fully
  visible and not clipped by an image bounding box, `trim`/`clip`, subcaption
  box, or page edge;
- the caption is attached to the correct object and every panel identifier is
  visible at print size;
- the rendered order does not contradict source order or place a float before
  its first explanatory use without an explicit reason;
- a float does not split a prose paragraph, appear between a subsection heading
  and its opening paragraph, or sit under a heading that belongs to the
  preceding subsection; and
- a figure or table does not drift past the section or subsection that owns it,
  or move to a later page after the paragraph that introduces the result when
  a safe placement on the current page is possible.

Use the smallest placement repair that preserves the paper's existing reading
order. Depending on the template, this may be a local `[t]`, `[b]`, `[tbp]`, or
starred float option, moving the environment to the next paragraph boundary,
or a local `\FloatBarrier` at a real section boundary. Use `\afterpage` or
`\clearpage` only when the existing build policy allows it and the page-level
comparison shows that a lighter repair cannot work. Do not add `[H]` globally;
it commonly creates larger gaps and stranded headings.

For the known failure patterns, apply these checks:

- **Clipped panel title (for example, Figure 6):** inspect the panel box,
  subcaption width, image `trim`/`clip`, and page bounding box. Fix the cause
  and re-render at print size; shrinking the entire figure until the title is
  technically visible is not sufficient if it becomes unreadable.
- **A table interrupting the body (for example, Table 4):** place it after the
  complete paragraph or at the next safe top/bottom position. Keep the prose
  continuous and preserve the table's first-use relationship.
- **A figure pushed after its introducing section (for example, Figure 6 after
  Overall Performance):** keep it with the introducing result when it fits;
  otherwise place it at the top of the next page before an unrelated heading,
  or defer it only with an explicit float-policy reason.
- **A figure directly below a subsection heading (for example, Figure 11
  below 6.7):** put the subsection's opening paragraph first, unless the
  manuscript explicitly uses a figure-led subsection and the caption is the
  opening contract. If the figure belongs to the previous subsection, prevent
  it from crossing the boundary with a local barrier.

The `floats` gate passes only when panel and table content is fully visible,
caption attachment is correct, source and rendered order are accounted for,
the float remains in its owning scope, and no paragraph or heading is stranded.

### 6. Inspect and repair rendered whitespace

Render the baseline and the post-source-fix PDF. Inspect every changed page at
normal reading size and the page pair around each figure or table. Classify
whitespace before changing it:

- float-to-text or float-to-float gap;
- caption-to-float gap;
- a widow/orphan or short final line;
- a float deferred to a later page;
- bottom-of-page stretch caused by the template; or
- an intentional section break or protected layout.

When the template permits spacing changes, use the smallest preamble-level
change that addresses the observed cause. Candidate lengths include
`\textfloatsep`, `\floatsep`, `\intextsep`, `\dbltextfloatsep`,
`\dblfloatsep`, `\abovecaptionskip`, and `\belowcaptionskip`. For a
widow/orphan caused by paragraph breaking, the class may also permit
`\clubpenalty`, `\widowpenalty`, or `\displaywidowpenalty`; inspect the
template before changing them. Values such as

```tex
\setlength{\textfloatsep}{5pt plus 2.0pt minus 2.0pt}
\setlength{\abovecaptionskip}{6pt plus 1.0pt minus 1.0pt}
\setlength{\dbltextfloatsep}{5pt plus 2.0pt minus 2.0pt}
```

are starting candidates, not defaults. Check the class/template first. Never
change float order, caption text, figure/table dimensions, margins, font size,
or placement specifiers merely to hide a gap. If the gap is an intentional
template behavior or fixing it would move a float across a section boundary,
report it instead.

The `whitespace` gate passes only if the new PDF preserves float order and
caption attachment, removes the targeted avoidable gap, introduces no
collision or clipping, and does not add overfull/underfull or unresolved-
reference warnings. It must not silently perform a `floats` repair; report
that finding for a separate `floats` run.

### 7. Tighten short paragraph tails

Run this pass after source and layout fixes. A candidate is a prose paragraph
whose rendered final line contains zero, one, or two words. Ignore headings,
captions, bibliography entries, equations, lists, code/pseudocode, and
intentionally one-line paragraphs.

For each candidate, inspect the source and remove at most one small,
dispensable local phrase per iteration. Prefer deletion-only edits: a redundant
modifier, repeated noun, or optional discourse word. A phrase replacement is
allowed only when every replacement token is already present in the same
sentence or the canonical terminology ledger, and the before/after proposition,
objects, relations, scope, modality, tense, evidence, and terminology IDs are
identical. Do not introduce a new compound, nominalization, abbreviation,
synonym, or technical term while shortening. For example, never change
`tokens matched by exact matching` to `exact-match token`: it introduces a new
term and changes the visible concept form even if the words appear related.
Do not remove qualifiers, numbers, conditions, evidence, technical terms,
causal links, or words needed for grammar. Do not shorten a paragraph just to
meet a line-count target when exact semantic preservation cannot be proven.

Recompile after each batch and verify both the sentence meaning and the actual
rendered line count. Compare the before/after sentence contract: every object,
relation, qualifier, evidence binding, scope marker, modality, and canonical
term must have the same ID and role. A tail fix is accepted only when it saves
the line or removes the targeted short tail without creating a new
widow/orphan, overflow, bad page break, terminology inconsistency, or new
concept. If exact correspondence cannot be established, abandon the edit and
report the retained tail to the user. If no terminology ledger or sentence
contract exists for the paragraph, treat equivalence as unverifiable and do not
edit it.

### 8. Independent verification

Compare the final source and PDF against the frozen baseline:

- rerun the heading, paragraph, terminology, artifact, and cross-reference
  ledgers;
- compare protected tokens: numbers, units, symbols, citations, labels,
  canonical object names, and qualifiers;
- compare float order, caption attachment, page count, and all changed pages;
- confirm no new compiler warnings or unresolved references;
- confirm that no section responsibility, paragraph order, argument edge, or
  evidence binding changed; and
- keep every deferred or uncertain finding with its location and reason.

If an independent verification pass finds a semantic or presentation change,
roll back to the last passing artifact and route the issue to the appropriate
presentation or author-alignment workflow. Never present a draft-only source
edit as a completed hygiene pass.

## Output contract

Return:

- `mode`, selected unit, requested scope, input source/PDF identity, output
  identity, and build command;
- baseline and final warning summaries;
- applied fixes with issue IDs, locations, and preserved invariants;
- figure/table placement findings and changes with affected pages, owning
  subsection, first-use relation, and before/after rationale;
- whitespace changes with affected pages and before/after rationale;
- paragraph-tail candidates, accepted tightenings, and intentionally retained
  tails;
- deferred findings and coverage limits; and
- a gate result: `Complete`, `Review only`, `Needs context`, or `Needs revision`.

`Complete` means the requested checks ran, all applied changes passed the
rendered verification gate, and no required hygiene finding remains. It does
not claim scientific correctness, stronger presentation, novelty, or venue
readiness.
