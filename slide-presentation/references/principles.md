# Slide principles

Every rule here came from a correction a user made on a real deck. Each "Mistake" line records what went wrong so it is not repeated. Profiles and project overrides may tighten or relax a rule; when one does, it says so explicitly.

## Contents

1. [Content before format](#1-content-before-format)
2. [Storyline](#2-storyline)
3. [One point per slide](#3-one-point-per-slide)
4. [Calibrated claims](#4-calibrated-claims)
5. [Evidence and numbers](#5-evidence-and-numbers)
6. [Words](#6-words)
7. [Figures and tables](#7-figures-and-tables)
8. [Layout](#8-layout)
9. [Process](#9-process)

## 1. Content before format

- Claims and story are cheap to change in a spec and expensive to change in a built deck. Agree on the content first; build after.
- Discuss slides in batches (for example, the background slides, then the motivation slides). Mark each slide `agreed`, `proposed` or `open` in the spec, with the date and, for a change, the user's reason.
- Never build an `open` slide as final; it stays a placeholder until the user agrees.
- Start lean. A first draft usually has too many slides and too much detail; merge slides that make the same point.
  - Mistake: a 14-slide first draft became 11 after the user merged repeated points and removed the outline slide.
- No talk-outline, agenda or section-outline slides unless the user or the profile asks for them. Show the part name as a small tag instead.
- Ask whether the talk length matters before cutting or padding for it. Estimate speaking time at about 100-110 words per minute when it does.

## 2. Storyline

- Write the logic chain before the slides: one clause per slide, each answering the question the previous slide raised.
- Check every pair of consecutive slides for a gap. If the audience would ask "why?" between them, a slide or a sentence is missing.
  - Mistake: the chain went from "networks are slow" straight to "decompressing the data is costly"; the "so systems compress it" step was missing.
- For research talks the structure follows the paper (see the profile): Background states the case existing work already makes; Motivation states the gap that calls for this work. They must not overlap: a background slide that already argues the gap leaves the motivation slide with nothing new.
- When a claim needs a breakdown and a cause, use a short sequence of slides (overview → where it goes → mechanism → consequence) rather than one crowded slide.

## 3. One point per slide

Every content slide reads: title → claim line → minimal evidence → transition. Everything else goes to the speaker notes.

- **Title = a short, punchy claim**, 3-7 words, subject + strong verb + outcome. No hedges, no scope, no numbers unless the number is the point. Example: "Caching the index on SSD cuts p99 query latency by 40% under mixed load" becomes "SSD index caching cuts tail latency".
- **Claim line** under the title: one line, about 12-16 words, saying the point plainly with its scope. The longer sentence goes to `Full claim` (notes).
- **Body**: only what the audience needs to accept the claim at a glance: one figure, one small table, 1-3 numbers, or a one-sentence cause. At most three bullets.
  - Mistake: background slides carried several tables and five-bullet explanations; the user asked for one point per slide.
- **Why**: when a slide gives a cause, one sentence that explains why, in everyday words. Not a restatement of the measurement, not an implementation walkthrough.
- **Transition**: one sentence at the bottom that hands over to the next slide. It must be visible (the tinted band), not small gray text.
- **Notes**: scope, caveats, extra data, derivations, and what to say aloud.

## 4. Calibrated claims

- Avoid absolutes: "must", "never", "always", "cannot", "no one", "exactly", absolute "only". Prefer scoped statements: "on this hardware", "in the tested settings", "up to".
- Check every novelty or gap claim against related work before it goes on a slide. Prefer "unexplored", "partly explained", "not studied for X".
  - Mistake: "no one has studied this accelerator for this workload" was false; a published system did. "Never adapted" was false too, because that system did adapt its design.
- Do not call a prior system wrong when its explanation is incomplete; say what it leaves unexplained.
- When the talk presents research questions of ongoing work, give directions, not early answers or results, unless the user asks. Exclude design content when the user excludes it.
- Label models and estimates as such ("estimate", "a model"); never present a question as answered when only a model answers it.

## 5. Evidence and numbers

- In background and motivation, prefer other papers' data. Cite on the slide ("System [3]"); give the figure, table or section in the source line.
- Verify every quoted number against the source's own data. When a paper's percentage does not match its own rates, quote the rates.
  - Mistake: a paper's text said "an additional 59%" drop where its figure's rates gave 45%; the slide quotes the rates.
- Label derived numbers "derived" or "estimate" and say how they were derived (in the caption or notes).
- Scope every number: which component, which data, which hardware, and what a ratio divides by.
  - Mistake: a reduction factor was quoted without saying it was relative to 8-bit, not 16-bit, data.
- Keep a single source per table column, or name the source in each cell.
- Compare like with like: the same setting in every row of a comparison, or say in the cell why not.
- Keep lossy and lossless results apart, or label which is which.
- Record every number's origin in the sources index ([assets/sources-template.md](../assets/sources-template.md)), not on the slide.

## 6. Words

- Build a small vocabulary before writing slides: each term, its definition, and the internal name it replaces.
- Define each term at its first use in the deck, including first use inside a figure label or legend.
- Avoid terms that clash with another meaning in the domain.
  - Mistake: "encode/decode" for compression clashed with a phase of the system under study that is also called "decode".
- Name things by role and concrete identity together: "Fast: Huffman-only (no repeat search)", not either alone.
- Never on slides or in notes: internal step IDs, run IDs, host names, repository paths, code names. Put them in the sources index. List them as banned terms so the lint catches them.
- Choose units per domain, state them once, and never convert silently. When a source reports a quantity in another unit, convert it in the notes and say so.

## 7. Figures and tables

- A figure must carry one message and be readable at a glance. Replace a dense figure with a simpler one or a highlighted table.
- A figure the user will copy from a paper is a labelled placeholder with caption and citation; do not redraw it unless asked.
- Architecture or hardware slides show what the user asked for (for example the specification only); performance numbers and extra detail go to the notes.
- Tables: one row per option compared, one column per metric, units in the cells, readable font, light header, no cramped cells. Keep only the columns the claim needs.
- Highlight only the cells that carry the claim.

## 8. Layout

- Use the template the user names; the bundled default is the Google Slides default theme.
- Fixed grid on every content slide: part tag (top right), title, claim line, content area, transition band, source line, slide number. The title's left edge matches the body margin.
- One accent color, used for key numbers, highlighted cells, the transition arrow and band accent; everything else neutral.
- Part tag and source line are small and gray.
- After every build, render and look at every slide: titles on one line, claim lines on one line, nothing overflowing or overlapping, nothing running into the band or footer, no glyphs the font lacks.

## 9. Process

- The spec is authoritative. A builder sub-agent does not change claims or wording silently; it reports any deviation it believes is needed and lets the user decide.
- Commit decks on the deck's branch and stage only the deck's files, by path. Never `git add -A` or `git commit -a`.
- When the user corrects style or wording, apply the correction, then record it as a dated rule in the project profile (or the case profile, if it is general) so it is not repeated. See [customization.md](customization.md).
- When the user says an earlier version was better, restore it and change only what they asked.
- When the user cites slide numbers, map them to titles before acting and state the mapping; numbering shifts.
