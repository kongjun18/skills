# Paper Hygiene Workflow and Ledgers

Read this reference when the paper has multiple source files, a substantial
number of figures or tables, or findings that cross section boundaries. It
defines the evidence needed for a safe local edit; it is not a presentation
rubric.

## Baseline commands

Use the paper's own build instructions first. These commands are fallbacks,
not a required toolchain:

~~~sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
pdfinfo main.pdf
pdftotext -layout main.pdf baseline.txt
pdftoppm -png -r 180 main.pdf scratch/page
~~~

Keep all outputs in scratch space. Record the exact source root, engine,
options, page count, warning summary, and PDF hash. If the build has known
baseline warnings, record them separately from regressions.

## Ledgers

Use stable IDs so that findings survive a later edit. A compact ledger can be
kept in the response, in a user-provided tracker, or in scratch space when no
repository destination is specified.

### Heading tree

| ID | Level | Heading | Source | Label | Included by | Notes |
| --- | --- | --- | --- | --- | --- | --- |

Check for duplicate labels, an empty heading with no intended content, an
include that is never reached, a missing file referenced by input or include,
and a heading that appears twice because an old copy was restored. Do not
infer a missing conceptual section from the heading tree alone.

### Paragraph inventory

| ID | Source | Section | Opening | Local role | Key object/evidence | Tail words |
| --- | --- | --- | --- | --- | --- | --- |

For semantic duplicate candidates, add:

| Candidate pair | Proposition | Scope | Evidence | Role | Decision |
| --- | --- | --- | --- | --- | --- |

Use same accidental unit only when proposition, scope, evidence, and reader
role all match. If one occurrence is a summary and the other is a detailed
explanation, they are not automatically duplicates. If both are required but
the repetition is too large, defer to presentation revision.

### Terminology ledger

| Object ID | Canonical term | Allowed aliases | Suspicious variants | Layer/scope | Evidence |
| --- | --- | --- | --- | --- | --- |

An evidence entry can be a definition in the paper, a notation table, an
author-provided guide, or a repeated unambiguous usage. A frequency count is
not evidence that two terms are interchangeable. Mark a change as safe only
when the local referent is the same object and the canonical term is already
established.

### Artifact map

| ID | Kind | Label | Source | Page(s) | Caption | Referenced from | Order |
| --- | --- | --- | --- | --- | --- | --- | --- |

Use it to verify that a local label fix did not change a figure/table/equation
identity and that a layout fix did not reorder floats.

## Issue record

Use one record per independent repair:

~~~text
ID: H-###
Class: mechanics | duplicate | section-artifact | terminology | reference
      | layout | short-tail
Severity: major | minor | polish
Status: applied | retained | deferred | needs-context
Location: source path:line or PDF page/region
Evidence: smallest useful excerpt, competing terms, or before/after render
Action: exact local change or reason for deferral
Invariant: claim/number/object/edge/ordering/layout property preserved
Verification: command, page render, or ledger check
~~~

Major means the local defect changes the apparent object, scope, or
interpretation. Minor means it causes a concrete local reading or navigation
problem. Polish means a clear mechanical or visual defect with little effect
on meaning. These are cleanup priorities, not scientific scores.

## Mechanical audit details

Read each changed sentence with its preceding and following sentence. Correct
agreement, punctuation, spelling, article use, and an unmistakable local
word-choice error. Preserve the paper's established English variant and
technical capitalization.

For cross-references, check both the source key and the rendered target. A
reference to the wrong but existing figure is a terminology/navigation defect;
choosing a different figure because it makes the story flow better is a
presentation decision.

Treat comments, TODOs, draft markers, duplicate labels, and accidentally
uncommented archival text as artifacts only when their status is clear from the
source. A comment that contains an author decision is not disposable evidence.

## Rendered whitespace audit

Inspect the baseline page and the corresponding final page together. Mark the
cause and the smallest safe parameter before editing:

1. Caption gap: abovecaptionskip or belowcaptionskip.
2. Text/float gap: textfloatsep, intextsep, or floatsep.
3. Double-column float gap: dbltextfloatsep or dblfloatsep.
4. Widow/orphan: local reflow, or the template's permitted widow/club
   penalties.
5. Deferred float: leave it alone unless the existing placement policy
   authorizes a local change.

After the change, check the entire page, not only the gap: headings must not be
stranded, captions must stay with their objects, columns must remain balanced,
and the next page must not acquire a new bad break. Do not use negative
vertical space as a first response.

## Short-tail audit

pdftotext -layout is a locator, not a semantic parser. Use it to find
candidate pages, then identify the paragraph in the source and confirm the
line visually. Count words after removing only layout whitespace; do not count
equation tokens or a citation-only marker as prose words.

Safe candidates usually include a repeated adjective, an optional discourse
adverb, or a redundant phrase already stated in the same sentence. Do not
delete a qualifier (only, at least, up to), condition, metric/unit, technical
noun, citation, or causal connector merely to gain a line. If the candidate
requires moving a sentence, changing paragraph boundaries, or rewriting a
transition, defer it.

## Final gate

The pass is complete only when all of these are true:

- every applied issue has a source location and a verification record;
- protected tokens and canonical terms are unchanged except for approved local
  normalization;
- heading tree, paragraph roles, artifact identities, and float order are
  unchanged;
- the final PDF has no new unresolved references, overfull boxes, clipping,
  collisions, or detached captions;
- each accepted tail change is visible in the final render; and
- every unresolved case is listed with a reason and the workflow that should
  handle it next.
