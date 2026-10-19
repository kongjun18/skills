---
name: paper-hygiene
description: Independently audit and safely clean an academic paper's source and rendered PDF for fatal submission blockers, mechanical errors, accidental duplication, terminology drift, section artifacts, figure/table clipping or placement errors, float whitespace, and very short final lines. Apply only meaning-preserving local fixes, with canonical technical terms and concept identities protected from unapproved synonym replacement; route argument, section-responsibility, and presentation-structure decisions to a presentation review or revision skill.
---

# Paper Hygiene

Use this skill for the paper's **surface integrity pass** after the technical
content is settled. It complements `paper-presentation-review` and
`paper-presentation-revise`; it does not replace them. The target is a paper
that says the same thing, uses the same objects and evidence consistently, and
renders without avoidable whitespace, float placement defects, or mechanical
errors. Every check below is an independently executable unit; running one
unit does not imply that the others ran.

## Fatal preflight: unresolved submission blockers

This is a release gate, not a cosmetic cleanup unit. Every invocation of this
skill begins with the `blockers` preflight, even when the user selects another
unit. The preflight scans the complete source scope and the rendered PDF for
unresolved placeholders and draft residue. A confirmed blocker stops the run's
editing work and produces `Needs revision` until it is removed or the author
explicitly classifies it as intentional.

Scan case-insensitively for standalone or macro forms of markers such as
`TODO`, `FIXME`, `TBD`, `TBC`, `XXX`, `XX`, `???`, `PLACEHOLDER`, `REPLACE`,
`INSERT`, `\todo{}`, `\TODO{}`, `\fixme{}`, `\placeholder{}`, angle-bracket
fill-ins such as `<value>` or `<author>`, and project-language equivalents such
as `待补`, `待定`, or `占位`. Also inspect visible draft notes, red review text,
unfinished citations, and blank result fields that use a marker rather than a
value. Use token boundaries and surrounding context so an intentional term
such as `xxHash` is not reported as the `XX` marker; do not silently discard an
ambiguous match.

The preflight must record every candidate's source location, rendered location
when visible, exact marker, surrounding text, and classification:

- **confirmed blocker:** unresolved text that cannot ship;
- **intentional content:** a marker shown as part of a documented example or
  notation, with the evidence recorded;
- **ambiguous:** requires author clarification and remains blocking until
  resolved.

Do not invent values, citations, names, or results to clear a blocker. A local
deletion is allowed only when the marker is demonstrably accidental and its
removal does not leave a missing claim or broken sentence. Otherwise stop and
report the blocker. This preflight is mandatory before any PDF handoff.

## Priority zero: protected terminology and concept inventory

This rule applies to every hygiene unit and every source/PDF update. It
overrides short-tail cleanup, whitespace reduction, concision, fluency, and
page-budget pressure.

Technical terms and concept-bearing phrases are protected interface names. This
includes component, operation, state, data-structure, metric, workload,
configuration, invariant, claim, figure, and table names. A shorter word can
change the operation or object while leaving the sentence broadly plausible.
For example, `routing-point rematerialization` and `routing-point rebuild` must
not be treated as interchangeable without an explicit author decision.

The failure mode is a local length optimization: the editor sees a long word,
chooses a fluent near-synonym, and checks broad sentence meaning instead of the
paper-level concept identity. A frequency count, dictionary similarity, or
shorter rendered line does not establish an alias.

Before any unit edits the source, build or refresh a terminology/concept ledger
with a stable concept ID, canonical surface form, definition and referent,
layer and scope, explicitly allowed grammatical forms or aliases, forbidden or
suspicious variants, and the evidence that establishes the choice. During each
edit, any phrase that may be technical but is not yet classified is
provisionally protected until the author or evidence resolves it:

1. Classify every changed span. If it contains or names a protected item,
   preserve the canonical form or an explicitly allowed form.
2. Use deletion of unprotected wording, local reflow, or an approved layout
   parameter before considering a lexical replacement.
3. Add or change an alias only after an explicit author decision and a ledger
   update. Never infer equivalence from shared words, morphology, apparent
   synonymy, or a reviewer suggestion.
4. Run a protected-token and concept-ID diff before accepting the edit. The
   canonical terms, referents, operation/state distinctions, qualifiers, and
   cross-section uses must match the baseline. If they do not, roll back and
   report `Needs context`.

If the ledger is missing or the intended referent is uncertain, retain the
original wording. A short final line is an acceptable result when removing it
would require changing a protected term.

## Non-negotiable boundary

An edit is eligible for direct application only when all of the following are
true:

1. The defect is visible in the supplied source or rendered artifact.
2. The intended correction is recoverable from the paper, its terminology
   guide, or an explicit author decision.
3. The change does not alter a claim, qualifier, number, evidence binding,
   causal relation, paragraph responsibility, section responsibility, float
   meaning, concept inventory, protected-token sequence, concept ID, or
   canonical terminology.
4. The change can be checked again after recompilation.
5. The mandatory `blockers` preflight has no confirmed or ambiguous candidate.

Otherwise record a located finding and stop at `Needs context`. In particular,
do not invent a missing section, rewrite a section for better flow, merge two
paragraphs because they seem repetitive, or choose between two technical terms
from memory. Those are presentation or semantic decisions.

## What this skill covers

| Area | Directly fix when clear | Report and defer when unclear |
| --- | --- | --- |
| Mechanics | Grammar, spelling, punctuation, agreement, articles, malformed local sentences, and an unambiguous word-choice slip outside protected terminology | A rewrite that changes emphasis, claim strength, or technical meaning |
| Repetition | Exact duplicate text, or a clearly accidental semantic duplicate with the same role and evidence | Two passages that share a topic but have different scope, role, or evidence |
| Sections | Duplicate/empty headings, orphaned `\input`/`\include`, and broken local numbering or cross-reference | A conceptually missing section, a section move, or a new subsection whose responsibility is not specified |
| Terminology | Normalize only an explicitly allowed alias to the ledger's canonical term when the concept ID is the same | A near-synonym or a choice between distinct objects, layers, states, or operations |
| References and labels | Broken local references, mismatched figure/table/equation labels, unresolved keys, and stale local names | A citation or attribution whose correctness needs external or scientific judgment |
| Figures and tables | Clipped panel titles, missing labels, detached captions, wrong source order, a float before its first use, or a float that interrupts a paragraph or appears under the wrong subsection heading | A placement change that requires reordering the argument, changing a figure/table's role, or inventing a new visual |
| PDF layout | Safe float/caption spacing or local reflow that preserves order and content | Margin, font, figure size, float order, or template changes without authorization |
| Paragraph tails | Delete a demonstrably dispensable **unprotected** local word or phrase when a rendered final line has at most two words | Any replacement or shortening that changes scope, strength, terminology, concept inventory, or sentence logic |

The ledger's canonical surface form must win over every unapproved variant. A
near-synonym is not safe merely because the surrounding passage appears to name
the same broad object: `rematerialization` and `rebuild`, for example, can carry
different operation semantics. If the ledger does not explicitly establish the
alias and concept ID, leave the text unchanged and request context.

## Modes

Every mode performs its own intake, baseline render, scoped check, and
verification. A mode must not silently depend on a previous mode's report or
edits.

- `mechanics`: grammar, spelling, punctuation, agreement, and unambiguous
  local word-choice errors.
- `blockers`: mandatory fatal preflight for unresolved placeholders, draft
  markers, unfinished fields, and visible review residue.
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

If the user names one unit, run the mandatory `blockers` preflight first, then
run only that unit. `cleanup` may be accepted as a
compatibility alias for the explicitly named source units, but it must not
silently include `floats`, `whitespace`, or `tails`.

## Independent-run contract

For a selected unit, create a fresh run record containing the source revision,
PDF hash, build command, requested scope, and unit name. Rebuild or validate a
baseline before making edits, even if another unit was run earlier. Apply only
the selected unit's edits. Then run that unit's verification gate and report
unrelated findings as deferred observations rather than fixing them in the
same run. The run record must include the `blockers` preflight and its
candidate classifications; a unit cannot be reported `Complete` while that
preflight is unresolved.

## Pipeline

The intake and verification gates apply to every independent mode. Run
`blockers` first for every mode. In `auto`, run the units in this order:
`blockers`, `mechanics`, `duplicates`, `structure`,
`terminology`, `references`, `floats`, `whitespace`, and `tails`. In a
single-unit run, execute only the corresponding subsection below and omit
changes from every other unit.

### 0. Mandatory blockers preflight

Before any source edit, scan all included source files, bibliography entries,
captions, tables, figure text available as source, appendices, comments that
can leak into the artifact, and the rendered PDF. Search both literal text and
the macro forms listed above. Inspect every match in context and write a
blocker issue record. A match that cannot be proven intentional remains
`ambiguous` and blocks completion. If a confirmed blocker is visible in the
PDF, record its page and region; if it appears only in source, record the file
and line and still block the release gate.

The `blockers` gate passes only when every candidate is either removed or
explicitly documented as intentional by the author, with no unresolved or
ambiguous marker. It is a read-only audit by default. Apply a deletion only for
an unmistakable accidental marker; never fill in missing scientific content
from memory.

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
  citations, technical objects, canonical terms, and placeholder candidates.

Source text alone cannot establish a visual defect. A layout finding requires a
rendered page or an equivalent layout trace.

### 3. Run the selected source integrity unit

Read the complete requested scope before editing. Build only the ledgers needed
by the selected unit; a paper-wide run may use these four shared ledgers:

1. **Heading tree:** section/subsection order, source location, labels, and
   included files.
2. **Paragraph inventory:** stable source locator, heading, opening, role,
   key object, evidence, and outgoing endpoint.
3. **Terminology ledger:** stable concept ID, canonical surface form,
   definition/referent, allowed grammatical forms or aliases, forbidden or
   suspicious variants, abstraction layer/scope, and evidence for the choice.
4. **Artifact map:** figure/table/equation labels, captions, float placement,
   and cross-references.

The source integrity stage is split into independent units:

- `mechanics` checks grammar, spelling, punctuation, agreement, malformed local
  sentences, and unmistakable word-choice slips.
- `duplicates` compares proposition, scope, evidence, and role for exact and
  semantic duplicate paragraphs. It does not merge paragraphs for smoother
  flow.
- `structure` checks empty or duplicated headings, missing `\input`/`\include`
  files, duplicate labels, and accidental source inclusion. Placeholder and
  draft-residue findings belong to the mandatory `blockers` unit. A
  conceptually missing section remains a deferred presentation finding.
- `terminology` checks the canonical object ledger and repairs only an explicitly
  allowed alias to the canonical form; it never invents a near-synonym.
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

Edit the smallest source span that resolves the defect. Before editing, run the
protected-token/concept-ID gate and classify the changed span. Keep a change
ledger with the issue ID, source location, before/after text, evidence for the
fix, and the invariant it preserves. Do not perform a document-wide synonym
sweep, and do not replace a protected term to save space, even when a shorter
word sounds equivalent.

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

Do not change prose words as a whitespace repair. If a short final line is the
cause, use the `tails` unit and its protected-term gate; physical whitespace
work must not silently become lexical rewriting.

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
dispensable **unprotected** local phrase per iteration. Prefer deletion-only
edits: a redundant modifier, repeated noun, or optional discourse word. Do not
replace a protected term. The fact that a replacement token appears in the
terminology ledger authorizes only the exact form or an explicitly listed
alias; it does not authorize arbitrary swaps between canonical terms. A
phrase replacement is allowed only for unprotected wording when the
before/after proposition, objects, relations, scope, modality, tense, evidence,
and terminology IDs are identical. Do not introduce a new compound,
nominalization, abbreviation, synonym, or technical term while shortening. For
example, never change `tokens matched by exact matching` to `exact-match token`:
it introduces a new term and changes the visible concept form even if the words
appear related.
Do not remove qualifiers, numbers, conditions, evidence, technical terms,
causal links, or words needed for grammar. Do not shorten a paragraph just to
meet a line-count target when exact semantic preservation cannot be proven.

Recompile after each batch and verify both the sentence meaning and the actual
rendered line count. Compare the before/after sentence contract: every object,
relation, qualifier, evidence binding, scope marker, modality, protected token,
and canonical term must have the same ID and role. A tail fix is accepted only
when it saves the line or removes the targeted short tail without creating a new
widow/orphan, overflow, bad page break, terminology inconsistency, or new
concept. If exact correspondence cannot be established, abandon the edit and
report the retained tail to the user. If no terminology ledger or sentence
contract exists for the paragraph, treat equivalence as unverifiable and do not
edit it.

### 8. Independent verification

Compare the final source and PDF against the frozen baseline:

- rerun the heading, paragraph, terminology, artifact, and cross-reference
  ledgers;
- compare protected tokens exactly: numbers, units, symbols, citations, labels,
  canonical surface forms, concept IDs, operation/state names, and qualifiers;
- compare float order, caption attachment, page count, and all changed pages;
- confirm no new compiler warnings or unresolved references;
- confirm that no section responsibility, paragraph order, argument edge, or
  evidence binding changed; and
- keep every deferred or uncertain finding with its location and reason.

Any changed protected token or concept ID without an explicit author-approved
ledger update is a failed gate, even when the sentence remains fluent and the
rendered line is shorter. An unapproved alias always fails the gate.

If an independent verification pass finds a semantic or presentation change,
roll back to the last passing artifact and route the issue to the appropriate
presentation or author-alignment workflow. Never present a draft-only source
edit as a completed hygiene pass.

## Output contract

Return:

- `mode`, selected unit, requested scope, input source/PDF identity, output
  identity, and build command;
- mandatory `blockers` preflight result, every candidate marker and its
  classification, and any source/PDF locations;
- terminology/concept-ledger identity and protected-token gate result;
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
