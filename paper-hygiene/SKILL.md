---
name: paper-hygiene
description: Audit and safely clean an academic paper's source and rendered PDF for mechanical errors, accidental duplication, terminology drift, section artifacts, float whitespace, and very short final lines. Apply only meaning-preserving local fixes; route argument, section-responsibility, and presentation-structure decisions to a presentation review or revision skill.
---

# Paper Hygiene

Use this skill for the paper's **surface integrity pass** after the technical
content is settled. It complements `paper-presentation-review` and
`paper-presentation-revise`; it does not replace them. The target is a paper
that says the same thing, uses the same objects and evidence consistently, and
renders without avoidable whitespace or mechanical defects.

## Non-negotiable boundary

An edit is eligible for direct application only when all of the following are
true:

1. The defect is visible in the supplied source or rendered artifact.
2. The intended correction is recoverable from the paper, its terminology
   guide, or an explicit author decision.
3. The change does not alter a claim, qualifier, number, evidence binding,
   causal relation, paragraph responsibility, section responsibility, or float
   meaning.
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
| PDF layout | Safe float/caption spacing or local reflow that preserves order and content | Margin, font, figure size, float order, or template changes without authorization |
| Paragraph tails | Remove a dispensable local word or phrase when a rendered final line has at most two words | Any shortening that changes scope, strength, terminology, or sentence logic |

The canonical object must win over a near-synonym. For example, if the paper's
ledger says that a prefix's candidate is an **alternative**, a later accidental
use of **continuation** is a terminology defect only when the surrounding
passage clearly denotes that same object. If the two words may denote different
objects, leave the text unchanged and request context.

## Modes

- `audit`: read-only source and PDF audit. Produce findings and acceptance
  conditions; do not edit.
- `cleanup`: apply safe source-level fixes, then verify the rendered artifact.
- `layout`: inspect and repair only physical whitespace and float/caption
  spacing.
- `tighten`: inspect and repair only rendered paragraph tails with at most two
  words on the final line.
- `auto`: run the complete sequence below. Use this when the user asks for the
  whole hygiene pass; otherwise honor the requested mode.

## Pipeline

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

### 3. Run the source integrity audit

Read the complete requested scope before editing. Build four small ledgers:

1. **Heading tree:** section/subsection order, source location, labels, and
   included files.
2. **Paragraph inventory:** stable source locator, heading, opening, role,
   key object, evidence, and outgoing endpoint.
3. **Terminology ledger:** canonical object, allowed aliases, forbidden or
   suspicious variants, abstraction layer, and evidence for the choice.
4. **Artifact map:** figure/table/equation labels, captions, float placement,
   and cross-references.

Check every paragraph and heading for the following concrete defects:

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

### 5. Inspect and repair rendered whitespace

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

The layout gate passes only if the new PDF preserves float order and caption
attachment, removes the targeted avoidable gap, introduces no collision or
clipping, and does not add overfull/underfull or unresolved-reference warnings.

### 6. Tighten short paragraph tails

Run this pass after source and layout fixes. A candidate is a prose paragraph
whose rendered final line contains zero, one, or two words. Ignore headings,
captions, bibliography entries, equations, lists, code/pseudocode, and
intentionally one-line paragraphs.

For each candidate, inspect the source and remove at most one small,
dispensable local phrase per iteration: a redundant modifier, repeated noun,
optional discourse word, or equivalent compression such as `in order to` →
`to`. Do not remove qualifiers, numbers, conditions, evidence, technical
terms, causal links, or words needed for grammar. Do not shorten a paragraph
just to meet a line-count target when no safe deletion exists.

Recompile after each batch and verify both the sentence meaning and the actual
rendered line count. A tail fix is accepted only when it saves the line or
removes the targeted short tail without creating a new widow/orphan, overflow,
bad page break, or terminology inconsistency.

### 7. Independent verification

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

- `mode`, input source/PDF identity, output identity, and build command;
- baseline and final warning summaries;
- applied fixes with issue IDs, locations, and preserved invariants;
- layout changes with affected pages and before/after rationale;
- paragraph-tail candidates, accepted tightenings, and intentionally retained
  tails;
- deferred findings and coverage limits; and
- a gate result: `Complete`, `Review only`, `Needs context`, or `Needs revision`.

`Complete` means the requested checks ran, all applied changes passed the
rendered verification gate, and no required hygiene finding remains. It does
not claim scientific correctness, stronger presentation, novelty, or venue
readiness.
