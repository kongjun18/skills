# Presentation details

Read this when writing the week-in-review, highlights, and digest listing, and
when assembling the digest JSON (stage 5).

Produce the output in this order.

## a. Week in review

Lead with a short synthesis for the reader, framed by the reader context when
present. Cap each subsection at five bullets; if a subsection is thin, collapse
it rather than padding, so the review stays skimmable on a busy week.

- **Research trends**: the emerging themes this week. Name each cluster and
  cite the papers in it.
- **Most inspiring / novel**: 2-5 papers with the freshest ideas or biggest
  potential impact, each with a one-line why-it-matters.
- **Directions for you**: the direction candidates from evaluation, openings
  the reader should have on the radar. For each, say why it is a foothold
  (entry point, wide open, tractable) and note any connection to the reader
  context. This is orientation, not a shortlist of projects to commit to.
- **Gaps and open problems**: what is conspicuously absent or unsolved. Carry
  forward open threads: a direction that appeared in a recent week and then
  went quiet is worth flagging. Keep them as an `open_threads` list in the
  digest JSON so each week reads back the last one and tracks whether a thread
  is heating up or cooling off.

If the window is thin, say so briefly rather than manufacturing a trend.

## b. Highlights

The top picks from evaluation, before the full listing: title (linked) and a
one-line why-it-matters. Lead with a single "if you read one thing" pick, the
lowest-effort entry point for the reader, then the rest of the top set.
Highlights rank by the week's strength, not by fit to the reader (see Reader
context in SKILL.md).

## c. The digest

The full curated listing, in tier order. For each non-catch-all paper keep:
title (linked to the abstract), authors, affiliation(s) with an academia or
industry tag, date, primary category, arXiv id, and a 1-2 sentence takeaway.
Render the catch-all tier terse (title and a one-liner; affiliation optional).
If a section is empty after curation, say so briefly rather than padding it.

Optional card `badge`: a short label such as "Your paper", "Rescued", or "From
your group".

Topic labels and order come from the active config. Past digests may differ
(older taxonomies, longer takeaways); match their tone and open-thread
continuity, not their structure.

## Digest JSON

`digest-YYYY-Www.json` follows the schema in the header of
[`../scripts/render_html.py`](../scripts/render_html.py):

- `rings` are the non-catch-all tiers; `peripheral` is the catch-all tier (set
  its `title` to the tier title).
- `title` is the config's `[digest] title`.
- `window` (`start`/`end`) is copied verbatim from the fetch output; the next
  run starts from `window.end`.
- `highlights.items` reference papers by `url`; `render_highlights.py` joins
  each with its card.

This JSON is the agent's judgment captured as data. The HTML and highlights
files are rendered from it by script, never by hand, so the frozen CSS in
`render_html.py` keeps every week identical; to restyle all digests, edit the
`CSS` block there once and re-render. The Markdown digest is written directly
(it carries no styling to drift).
