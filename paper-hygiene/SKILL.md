---
name: paper-hygiene
description: Mechanical cleanup of an academic paper's LaTeX source and rendered PDF with meaning-preserving local fixes. Covers placeholder and draft-residue scans (TODO, XX, ???), typos and grammar, accidental duplicate text, heading and label artifacts, glossary-alias drift, broken cross-references, figure/table clipping and float placement, float whitespace, short last lines, and a read-only check that numbers, units, and evaluation reporting match across the paper. Runs edits, or read-only in audit mode. Use for "clean up", "fix typos", "TODO/placeholder scan", "float placement", "whitespace", "short last line", "check numbers match", or a final mechanical pass. To cut prose to a page or word budget, use paper-writer. For citation correctness, use paper-integrity; for argument, structure, or section responsibility, use paper-presentation-review; for rewriting or shortening prose, use paper-writer.
---

# Paper Hygiene

The surface pass, run after the technical content has settled: the paper should
say the same thing it said before, use the same objects and evidence
consistently, and render without mechanical, layout, or draft-residue defects.
Each unit below runs on its own. Running one unit does not mean the others ran.

## Non-negotiables

1. **Terminology lock.** Follow the shared
   [terminology contract](../paper-writer/references/terminology.md). Load the
   paper's `GLOSSARY.md` and build its ledger before any edit. In hygiene this
   means:
   - A line-fitting, whitespace, or concision edit never swaps a protected
     term, even if the new line reads well and is shorter.
   - The `terminology` unit only changes an explicitly allowed alias to its
     canonical form, or a banned term to its single listed replacement.
     `→ rephrase` entries and choices between distinct terms go to
     paper-writer.
   - If the ledger is missing or a referent is unclear, keep the text as it is.
2. **Local and recoverable.** Apply an edit directly only when the defect is
   visible in the source or render; the correction is recoverable from the
   paper, its glossary, or an explicit author decision; the edit leaves every
   claim, qualifier, number, evidence binding, causal relation, paragraph or
   section responsibility, float meaning, and protected term unchanged; and
   the result can be rechecked after recompiling. Otherwise record a located
   finding as `Needs context`.
3. **Never invent content.** Do not fill a placeholder, number, citation,
   name, or definition from memory. Do not write a missing section or merge
   paragraphs "for flow". Those decisions belong to the author or to
   paper-writer.
4. **Edit source, not the PDF.** If only a PDF is available, run `audit` and
   state the coverage limits. Build products and page renders go to scratch
   space outside the manuscript tree. Preserve unrelated working-tree changes.
5. **Classify rendered findings before fixing them:** layout-only (fix here),
   source flow (route to paper-writer), or content (route to the author). Do
   not rewrite prose only to move a harmless page or column break.

## Units

| Unit | Checks | Fixes directly when clear | Reports and defers |
| --- | --- | --- | --- |
| `blockers` | Placeholders, draft markers, visible review notes, unfinished fields | Deletes a marker only when it is plainly accidental and the sentence stays complete | Everything else; read-only by default |
| `mechanics` | Grammar, spelling, punctuation, agreement, articles, malformed sentences, unmistakable word-choice slips | Local corrections outside protected terms, keeping the paper's English variant | Rewrites that change emphasis or claim strength |
| `duplicates` | Exact and semantic duplicate paragraphs | Removes an occurrence whose proposition, scope, evidence, and role all match the other | Overlap with a different scope or role (route to paper-presentation-review) |
| `structure` | Duplicate or empty headings, missing `\input`/`\include` files, duplicate labels, accidentally restored text | Local removal or relabeling | A conceptually missing or misplaced section |
| `terminology` | Ledger aliases and glossary banned terms | Changes an allowed alias to canonical, or a banned term to its listed replacement | Near-synonyms, `→ rephrase`, choices between distinct objects |
| `references` | Figure/table/equation/section references and labels, unresolved `??` | Points a reference at the target its sentence is clearly about | Whether a different figure would argue better; citation correctness (route to paper-integrity) |
| `consistency` | Numbers, units, comparisons, and evaluation reporting across prose, tables, figures, and data | Nothing: read-only | All findings, with both locations |
| `floats` | Clipped panels or headers, caption attachment, source vs rendered order, float before first use, float splitting a paragraph or crossing into another subsection | The smallest local placement or box repair | Moves that reorder the argument or change a figure's role |
| `whitespace` | Caption gaps, float gaps, widows and orphans | Template-permitted spacing parameters | Changes to margins, fonts, figure sizes, or float order; anything needing word changes (use `tails`) |
| `tails` | Prose paragraphs whose last rendered line has at most two words | Deletes one dispensable unprotected word or phrase | Any replacement or move that changes scope, strength, or terms |

**Modes.** Name one or more units to run only those. `audit` runs the
selected units read-only. `auto` runs every unit in table order, only when the
user asks for the full pass. `cleanup` means the source units (`mechanics`
through `references`) and never includes `floats`, `whitespace`, or `tails`.

## Blockers decide the verdict, not whether you may edit

Every invocation starts with a read-only `blockers` scan of the full source
scope and the rendered PDF. Use the marker list and classification rules in
[workflow.md](references/workflow.md#blockers). Each candidate is classified
`confirmed`, `intentional` (with evidence), or `ambiguous`.

- A confirmed or ambiguous blocker makes the release verdict `Needs revision`.
  Hygiene never reports the paper ready to submit while a blocker remains.
- Blockers do **not** stop local edits elsewhere. A draft full of TODOs can
  still get typo, reference, and float fixes. Do not edit inside a sentence
  that contains an unresolved marker, except to delete a plainly accidental
  one.

## Severity

Hygiene uses paper-integrity's tiers
([severity.md](../paper-integrity/references/severity.md)), applied to
surface defects:

| Tier | Hygiene meaning | Examples |
| --- | --- | --- |
| **S0** | Must be fixed before submission: visible draft residue, or a defect that changes the apparent result | Confirmed or ambiguous blocker; `??` in the PDF; conflicting values for the same reported result |
| **S1** | Changes the apparent object or scope, or blocks interpretation | Wrong figure reference; undefined term or unit; "all workloads" against "three of five"; clipped axis labels |
| **S2** | Clear mechanical or visual defect with little effect on meaning | Typo, agreement, stray whitespace, a short tail |

These are cleanup priorities, not scientific scores.

## Workflow

1. **Intake and baseline.** Locate the source root, bibliography, build
   command, template, current PDF, writing guide, `GLOSSARY.md`, and the
   author's [style conventions](../paper-writer/references/author-style.md)
   (its prohibited wording and LaTeX conventions are `mechanics` checks). Build in
   scratch space with the repository's documented command. Record the source
   revision, PDF hash, page count, and warning summary, and render the pages.
   A layout finding needs a rendered page; source text alone cannot establish
   one.
2. **Run the selected units.** Read the full requested scope first. Use
   [workflow.md](references/workflow.md) for ledgers, the issue record, and
   per-unit procedures. Read it whenever more than one unit runs, the paper
   has several source files, or you run `consistency`, `floats`,
   `whitespace`, or `tails`.
3. **Apply bounded fixes.** Edit the smallest span. Before each edit, run the
   protected-token check from the terminology contract. After each coherent
   batch, recompile and recheck. Revert any fix that changes a paragraph's
   role, adds a concept, changes claim scope, or needs a new transition, and
   report it as `Needs context`.
4. **Verify against the baseline.** Run the final gate in
   [workflow.md](references/workflow.md#final-gate). Any changed protected
   token without an author-approved ledger update fails the gate. Roll back to
   the last passing state.

## Output

Return the mode, units, and scope; source and PDF identity before and after,
and the build command; the blockers result with every candidate's class; the
protected-token gate result and `banned-term scan: N hits`; baseline and final
warning summaries; applied fixes as issue records; deferred findings, each
with its next owner; coverage limits; and a verdict.

| Verdict | Meaning |
| --- | --- |
| `Complete` | Requested units ran, every applied change passed the rendered gate, no blocker remains |
| `Review only` | `audit` run; findings only |
| `Needs context` | Some fixes need an author decision or another skill |
| `Needs revision` | A confirmed or ambiguous blocker, or an S0, remains |

`Complete` says nothing about scientific correctness, presentation quality, or
whether the paper is ready for a venue.

## Routing

- Citation existence, metadata, support, or uncited work: paper-integrity.
- Argument, section responsibility, repetition with different roles,
  transitions, figure roles: paper-presentation-review to diagnose,
  paper-writer to fix.
- Shortening or rewriting prose beyond deleting one word or phrase:
  paper-writer.
- A conflicting number whose correct value needs data provenance: the
  authors.
