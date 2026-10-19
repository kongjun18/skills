# Final Manuscript Visual QA Workflow

Use this workflow only when the author explicitly requests a final visual
check, PDF/layout review, page-break review, or `visual-qa`. It is a post-
manuscript stage for a completed or deliberately frozen scope. It is not part
of the default `review`, `revise`, `guided`, `figures`, or `auto` workflows.

The source-level presentation workflow and this visual workflow answer
different questions. Source review checks whether the argument, concepts,
transitions, evidence, and terminology work. Visual QA checks whether the
rendered artifact preserves that presentation on the page. Do not compile or
open a PDF merely because one exists in the project.

## 1. Bind the visual artifact

Record the source manuscript version, fixed outline revision, writing-guide
revision, PDF or rendered-artifact version, compilation route, and requested
visual scope. Prefer an author-provided final PDF. If no artifact exists, use
the repository's documented compilation route only after this workflow has
been explicitly requested. Do not guess a compiler, alter build settings, or
run an unrelated build to obtain a PDF.

If the PDF does not correspond to the bound source version, report `Needs
context` or rebuild it through the documented route. Do not treat a visual
inspection of a stale artifact as verification of the current manuscript.

## 2. Inspect the rendered pages

Inspect every page in the requested scope at final physical size. For a
multi-column paper, check both columns and the page boundary between them. Use
the rendered pages to check:

- paragraph, subsection, and heading breaks;
- orphaned headings, short fragments, and awkward sentence or paragraph
  continuations across pages or columns;
- figure and table placement, caption separation, panel order, and references
  to visuals on the same or a nearby page;
- equations, algorithms, lists, footnotes, citations, and references that are
  clipped, split, or detached from their explanation;
- whitespace, column balance, unexpected blank areas, and overflow; and
- whether page layout changes the reader's ability to recover the intended
  local argument or visual relationship.

Do not treat every page break as a defect. A break is a finding when it creates
a misleading grouping, strands a heading or caption, makes a sentence hard to
follow, or separates a visual from the claim it explains.

## 3. Classify findings before proposing edits

For each finding, identify the page and source locator and classify it as:

- `layout-only`: a spacing, break, placement, or rendering issue that does
  not require changing manuscript meaning;
- `source-flow`: a source paragraph or figure handoff should move or be
  rewritten to preserve readability on the page; or
- `content/presentation`: the rendered artifact exposes a real ambiguity,
  missing explanation, or terminology/claim problem.

Do not fix a `source-flow` or `content/presentation` finding with arbitrary
spacing or manual page breaks. Do not change argument structure, claims,
terminology, or evidence during visual QA without returning the issue to the
corresponding source-level stage. Likewise, do not rewrite prose solely to
avoid a harmless page break.

## 4. Apply authorized fixes and rerun the affected check

Visual QA is read-only unless the author has authorized source or layout
edits. For an authorized `layout-only` fix, make the smallest supported
change, regenerate the artifact through the documented route, and recheck the
affected pages plus neighboring boundaries. For a source-flow or
content/presentation fix, update the source and fixed outline when required,
then rerun the relevant source-level review before accepting the visual result.

Do not claim that a source-level revision is complete because the PDF looks
clean. Visual QA is an additional gate after source-level verification.

## 5. Return a visual QA report

For each finding, report:

- page, column, figure/table, or other rendered locator;
- source locator when it can be recovered;
- classification and severity;
- the reader-visible consequence;
- the smallest supported repair; and
- whether the affected page was rechecked after the repair.

Return the bound source and artifact versions, pages inspected, compilation
route, unresolved items, and whether the result is `Complete`, `Needs
revision`, or `Needs context`. A visual QA pass does not replace independent
source-level verification.
