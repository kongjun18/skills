# Paper Hygiene: Ledgers and Unit Procedures

Read the section for each unit you run. The rules in
[SKILL.md](../SKILL.md) and the
[terminology contract](../../paper-writer/references/terminology.md) apply to
every unit and are not repeated here.

## Blockers

Search the included sources, captions, tables, appendices, bibliography text,
source comments that could leak into the output, and the rendered PDF,
case-insensitively and on token boundaries, for `TODO`, `FIXME`, `TBD`, `TBC`,
`XXX`, `XX`, `???`, `PLACEHOLDER`, `REPLACE`, `INSERT`, macros such as
`\todo{}`, `\fixme{}`, `\placeholder{}` or the project's placeholder macro,
angle-bracket fill-ins such as `<value>`, equivalents in the project's
language, visible review-colored text, blank result fields, and unfinished
citations.

Use context, so an intentional token (`xxHash`) is not reported as a marker.
Record ambiguous matches; do not skip them. A source comment that records an
author decision is evidence, not residue.

For each candidate record the marker, `file:line`, the PDF page when visible,
the surrounding text, and its class: `confirmed` (unresolved draft or fill-in
text), `intentional` (documented example or notation, with the evidence), or
`ambiguous` (needs the author; blocks the release verdict until resolved).

## Ledgers

Build only the ledgers the selected units need. Use stable IDs so findings
survive later edits.

| Ledger | Columns | Used by |
| --- | --- | --- |
| Heading tree | ID, level, heading, source, label, included by | `structure`, `references` |
| Paragraph inventory | ID, source, section, opening, local role, key object or evidence | `duplicates` |
| Terminology ledger | As defined in the terminology contract | every editing unit |
| Artifact and float map | ID, kind, label, source, placement option, first use, owning subsection, rendered pages, caption status, order | `references`, `floats`, `whitespace` |

## Issue record

```text
ID: H-###     Unit: <unit>     Severity: S0 | S1 | S2
Status: applied | deferred | needs-context | needs-revision | retained
Location: path:line and/or PDF page/region (both sides for inconsistencies)
Evidence: smallest useful excerpt, competing values, or before/after render
Action: exact local change, or reason for deferral and the skill to route to
Invariant: the claim, number, object, order, or protected term preserved
Verification: command, page render, or ledger check
```

## Mechanics and references

Read each changed sentence together with its neighbors. A shorter
near-synonym is not an "unmistakable" word-choice error. For a
cross-reference, check both the source key and the rendered target. Pointing
a reference at a different figure because the story flows better is a
presentation decision, not a hygiene fix.

## Duplicates

Two passages are one accidental unit only when their proposition, scope,
evidence, and reader role all match. A summary and the detailed explanation it
summarizes are not duplicates. When both are required but the repetition is
too large, defer to paper-presentation-review.

## Consistency (read-only)

Check three things. **Numbers:** reported values, ranges, rankings, workload
counts, and stated result scope agree across abstract, introduction,
evaluation, conclusion, captions, tables, and available data. **Units and
comparisons:** units and denominators are explicit (bits vs bytes, GB vs GiB,
per-node vs aggregate, absolute vs relative, percent vs percentage points), and
each comparison's baseline, ratio direction, and normalization are
identifiable; flag an ambiguous "2× faster". **Evaluation reporting:** for each
result a reader can find the workload, configuration, measurement scope,
aggregation (mean, median, percentile), error-bar meaning, and repetition
count, locally or through a clear reference.

The procedure:
1. Before calling two values a conflict, match workload, hardware,
   configuration, baseline, metric, units, aggregation, and version.
   Different settings may legitimately give different values.
2. Where artifacts allow, trace the value: raw data → selection and
   aggregation in plotting code → plotted value or table cell → evaluation
   prose → summaries elsewhere. Recompute simple arithmetic. For example,
   10 ms → 5 ms is a 50% reduction and a 2× speedup, not a 100% reduction.
3. The evaluation usually wins over a summary, but verify it against its
   artifacts first: prose, data, and figures can each be stale. If provenance
   is missing, show the competing values and mark the finding
   `needs-context`. Never silently pick a value or read exact numbers off a
   plot.
4. Keep qualifiers such as "up to", "on average", and workload restrictions in
   any suggested wording. Report missing reporting details; do not demand new
   experiments.

## Floats

For each float, compare source order, first textual use, owning subsection,
and rendered page, and inspect the render at final size. Local placement
defects: a float before its introducing paragraph (unless the paper is
deliberately figure-led); a float splitting a paragraph or sitting between a
heading and its opening paragraph; a float crossing into another subsection; a
float pushed past the page of its introducing result when it could stay; and a
panel title, axis, legend, or table header clipped by the image box,
`trim`/`clip`, a subcaption width, or the page edge.

Repair the smallest cause: a permitted `[t]`, `[b]`, or `[tbp]` option, a
move to a paragraph boundary, a fixed panel box, or a local `\FloatBarrier` at
a real section boundary. Use `\afterpage` or `\clearpage` only if the template allows them and lighter
fixes fail. Never use global `[H]`, and never shrink a figure below readable
print size to hide clipping. Re-render the page and its neighbors afterwards.
The caption must stay attached, no heading or opening paragraph may be
stranded, and the float must stay in its owning scope.

## Whitespace

Classify each gap first: caption gap (`\abovecaptionskip`,
`\belowcaptionskip`), text/float gap (`\textfloatsep`, `\intextsep`,
`\floatsep`, or the `dbl` variants), widow or orphan (template-permitted
penalties), deferred float, template stretch, or intentional break. Check the
class file before changing a parameter, and use the smallest change.
Values like `5pt plus 2pt minus 2pt` are starting candidates, not defaults.
Never change float order, captions, sizes, margins, or fonts to hide a gap,
and never use negative vertical space first. Whitespace work changes no words
and moves no floats: report those as `tails` or `floats` findings.

## Tails

`pdftotext -layout` finds candidate pages. Confirm each candidate in the
source and visually, ignoring headings, captions, equations, lists, and
bibliography entries.

Per iteration, delete at most one dispensable unprotected word or phrase: a
repeated modifier, a phrase the sentence already states, or an optional
discourse adverb. Prefer deletion to replacement. A replacement is allowed only for unprotected
words, and only when the objects, relations, scope, qualifiers, modality,
tense, evidence, and terms are identical before and after. Never introduce a
new compound, nominalization, abbreviation, or synonym while shortening. Never
delete a qualifier, condition, unit, technical noun, citation, or causal
connector to gain a line. If exact equivalence cannot be shown, keep the tail
and report it. The edit counts only if the final render shows the line saved
with no new widow, overflow, or bad break.

## Final gate

The pass is complete only when all of these hold:
- every applied issue has a location and a verification record;
- protected tokens are unchanged, except for approved alias normalization:
  numbers, units, symbols, citations, labels, canonical terms, and qualifiers;
- the heading tree, paragraph roles, artifact identities, and float order are
  unchanged unless a float repair intended the change;
- the final PDF has no new unresolved references, overfull boxes, clipping,
  collisions, or detached captions;
- every unresolved case is listed with its reason and its next owner.
