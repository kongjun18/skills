---
name: pull-recent-papers
description: >-
  Weekly arXiv digest pipeline for a storage researcher. Use whenever the user wants a digest, roundup, weekly
  summary, or "what's new on arXiv" for storage/systems research.
---

# Pull Recent Papers

A five-stage pipeline that turns a week of arXiv systems papers into a curated,
evaluated digest for a storage researcher:

```
fetch  →  filter  →  ranking  →  evaluation  →  presentation
```

- **fetch** — pull the raw candidates from arXiv (script).
- **filter** — keep only the window + storage-relevant papers (script gate +
  agent curation).
- **ranking** — order by storage-proximity ring/topic (script), then by
  strength within a topic (agent).
- **evaluation** — read abstracts, judge each kept paper for
  novelty/relevance/promise, and read the week as a whole for trends (agent).
- **presentation** — the grouped digest, plus a week-in-review and a highlighted
  set of the most inspiring/promising papers (agent).

Stages 1–3 are mostly deterministic (script + light curation); stages 4–5 are
where the agent adds judgment.

## Reader context

Look for an optional **`context.md`** at the repository/workspace root (the same
directory that receives the digest outputs). This is a user-owned file: the user
may create or update it to describe who the digest is for, current projects,
research interests, nearby group or advisor lines, available testbeds, and desired
framing. It is free-form Markdown with no required schema.

- If `context.md` exists, read it before ranking/evaluation and use it to identify
  useful connections and tractable opportunities.
- If it does not exist, continue without it. Do not require, create, or overwrite
  the file.
- Treat its contents as context, not filtering rules. Storage-proximity remains
  the primary ranking principle, and work outside the reader's current projects
  can still be the most important opening.

Read the week as an opportunity radar: surface openings, tensions, and who's
working on what, while retaining enough breadth for unfamiliar directions to
appear.

## Storage-proximity taxonomy (three rings)

Papers are bucketed into three rings by how central they are to storage:

- **Ring 1 — Core storage** (top interest): the I/O & OS storage stack, memory &
  disaggregation, storage systems, distributed storage & consistency, DB storage
  engines, and storage-for-AI.
- **Ring 2 — Storage-facing adjacent** (secondary): databases, distributed data
  processing, LLM inference systems, cloud storage, and OS memory — *only where
  they touch storage/data/memory movement*.
- **Ring 3 — Peripheral** (skim only): in-category systems papers with **no**
  storage angle (e.g. FPGA accelerator design, consensus with no data plane, pure
  ML-accuracy work). Kept terse so the reader can skim what was filtered out.

The **exact topics and their keyword patterns are the `TOPICS` table at the top of
`scripts/fetch_arxiv.py`** — that table is the ground truth the classifier runs on,
so read it there rather than duplicating the keyword lists here (kept in one place,
they can't drift). Topics are matched in order, most storage-central first, so the
first match wins.

## The pipeline

### 1. Fetch

Run the fetch script. It queries arXiv (cs.DB, cs.OS, cs.DC, cs.AR, cs.PF),
filters to the window, gates on primary category, tags each paper to a
ring/topic, and prints a grouped Markdown digest (Core → Adjacent → Peripheral).

```bash
python3 scripts/fetch_arxiv.py --days 7
```

Flags: `--days N` (window, default 7), `--max-per-cat N` (cap on results pulled,
default 200), `--json` (full structured output, every abstract), `--curated-json`
(same but strips peripheral papers' abstracts — ~⅓ smaller, and you never read
those abstracts anyway).

**Default to the cheap path.** The plain Markdown output already truncates
abstracts to ~500 chars, which is enough to *curate and rank*. Do that from
Markdown, and only pull full abstracts — via `--curated-json`, or `WebFetch` on a
single paper — for the handful of **highlight candidates** you actually need to
judge in depth. Don't pull all full abstracts up front.

The script uses only the Python standard library — no install step. arXiv
requires HTTPS (plain http returns a 301). The final "Peripheral" topic is a
catch-all, so nothing in-category is silently dropped — the script casts wide;
later stages trim.

The window filters on **first-submission date** (arXiv `published`), not last
revision — so a paper first posted months ago but revised this week will *not*
appear. This is a *newly-submitted* digest by design; don't expect revisions to
resurface.

### 2. Filter

The script already applies the hard filters (window + primary-category gate).
Now apply the *semantic* filter the keywords can't: read each paper and decide
whether it truly belongs.

- **Demote/drop by storage relevance, not keyword.** A paper that only hit
  "cache" or "offload" in an ML/edge context (e.g. cross-timestep activation
  caching, MCU inference offload) is *not* storage — push it to Peripheral or
  drop it.
- **Rescue** genuinely storage-relevant papers the keywords missed from
  Peripheral into the right Ring-1/Ring-2 topic.
- Correct any obviously mis-slotted topic within a ring.

### 3. Ranking

Order the survivors.

- **Across topics:** keep the ring order (Core → Adjacent → Peripheral) and the
  topic order within each ring (see the taxonomy above; it runs most- to
  least-storage-central).
- **Within a topic:** float the strongest work to the top — real systems with
  results over position papers, general mechanisms over narrow point solutions,
  and anything that reads as an *opening* for the reader (use `context.md` when
  present). Don't down-rank a paper for being outside any particular sub-area.

### 4. Evaluation

Judge the ranked papers. **Work from abstracts.** Only fetch the arXiv abstract
page or PDF (WebFetch) when the abstract is genuinely insufficient to evaluate a
paper you think might be a highlight — don't fetch by default.

Keep the reader context in mind when present: evaluation is not just "is this
good work?" but "**is this an opening a storage researcher should know about?**"
Use `context.md` to identify connections worth noting, not as a gate that filters
everything else out.

Score each kept paper informally on three axes:

- **Novelty** — is the idea new, or an incremental delta?
- **Relevance** — how central is it to storage, plus any reader connection from
  `context.md`?
- **Promise** — could it change how storage systems are built, or open a
  direction? Strong results, a surprising finding, or a clean general mechanism
  all count.

Then, for the stronger papers, add an **opportunity read** — this is what turns
the digest from a survey into an orientation/opportunity radar:

- **Entry point?** — does it open a subfield, survey it, or (better) *explicitly
  list open problems / future work*? Call these out; they are useful footholds for
  exploring a direction.
- **Crowded vs. wide-open?** — use the affiliation data below (how many distinct
  groups are on this thread) to tell an *emerging* opening (one or two papers, no
  incumbent) from a *crowded thread* (several groups already racing). Say which —
  it shapes where attention pays off. Both are worth knowing about.
- **Tractable to reason about?** — a clean, general mechanism the reader can learn
  from and imagine building on, or a large industry system that's impressive to
  read but hard to approach? Note the difference; don't discard either.
- **Connection?** — does it touch anything in `context.md`? Note this as a helpful
  aside — a connection to flag, **not** a filter. Something outside that context
  can still be the best opening; don't down-rank it for that.

A paper that opens a direction the reader could plausibly pursue is a **direction
candidate** (feed it to "Directions for you" in presentation), not just a good
read. The goal is awareness of openings, not a shortlist of projects to commit to.

Also read the week *as a whole* — cluster papers into themes so you can speak to
trends, not just individual papers.

**Affiliations (endorsement signal).** For every curated paper, show *who's
behind it* at a glance. This is a two-part job: the script does the deterministic
extraction; **you interpret**.

Run the helper to get the raw author/affiliation text:

```bash
# curated subset straight from the fetch output (skips peripheral tier)
python3 scripts/fetch_arxiv.py --days 7 --curated-json \
  | python3 scripts/affiliations.py --from-json --curated

# or pass ids explicitly
python3 scripts/affiliations.py 2607.13604 2607.13276 ...
```

It emits `{id: {"block": "<raw author/affiliation text>", "emails": [...],
"email_domains": [...], "source": "html|pdf|none"}}` and prints the source +
email domains per paper to stderr. It reads `https://arxiv.org/html/{id}` (ar5iv
author block), falling back to the PDF author region via `pdftotext`. It does
**no** name cleanup or classification — that is intentionally yours.

Then **read each `block`** (with `email_domains` as a hint) and produce, for the
digest:
- the **distinct institution name(s)**, cleaned to a recognizable short form
  (e.g. "ETH Zürich", "AWS", "MIT CSAIL") — the raw block is often messy
  (author names run into institutions, city/country trailing);
- an **academia / industry / both** tag — `.edu`/`.ac.*`/university → academia;
  a company domain (`amazon.com`, `microsoft.com`, …) or company name →
  industry.

Why a script for the fetch but not the parse: the arXiv Atom API carries **no**
affiliations, and OpenAlex has none for fresh preprints (indexed but un-enriched
for days), so the text must come from the paper — but turning that text into a
clean name is judgment, so it stays with the agent.

- `--delay` (default 1.5s) spaces fetches to avoid arXiv **HTTP 429**; raise it
  for large batches.
- `source: "none"` / empty `block` means neither the HTML render nor the PDF
  resolved — show the affiliation blank, never guess.

### 5. Presentation

Produce the output in this order:

**a. Week in review** (lead with this). A short synthesis for the reader, using
`context.md` when present. **Cap each subsection at ≤5 bullets**; if a subsection
is thin, collapse it rather than padding — the review should stay skimmable even
on a busy week. Cover:
- **Research trends** — the emerging themes/directions this week (e.g. "CXL
  tiering picking up", "KV-cache offload converging on X"). Name the cluster and
  cite the papers in it.
- **Most inspiring / novel** — 2–5 papers with the freshest ideas or biggest
  potential impact, each with a one-line *why it matters*.
- **Directions for you** — the direction candidates from evaluation: openings the
  reader should be aware of. For each, say why it's a foothold (entry point /
  wide-open / tractable) and note any connection to `context.md` when available.
  This is orientation — *openings to have on the radar*, not a shortlist of
  projects to commit to. See the opportunity read in stage 4.
- **Gaps & open problems** — what's conspicuously absent or unsolved this week.
  Also carry forward **open threads**: a direction that appeared in a recent week
  then went quiet is exactly the kind of opening worth flagging. Keep these as an
  `open_threads` list in the digest JSON (below) so each week can read back the
  last one and track whether a thread is heating up or cooling off.

If the window is thin, say so briefly rather than manufacturing a trend.

**b. Highlights.** Call out the top picks from evaluation at the top of the
digest, before the full listing — title (linked), one-line why-it-matters. Lead
with a single **"if you read one thing"** pick — the lowest-effort entry point for
the reader — then the rest of the top set.

**c. The digest.** The full curated listing, Core first. For each Ring-1/Ring-2
paper keep: **title (linked to the abstract)**, authors, **affiliation(s) with an
academia/industry tag** (the endorsement signal from the evaluation step), date,
primary category, arXiv id, and a 1–2 sentence takeaway. Render Peripheral terse
(title + one-liner; affiliation optional). If a section is empty after curation,
say so briefly rather than padding it.

**Output files.** Write the week's digest to the repo root as
`digest-YYYY-Www.{json,md,html}` (ISO week):

1. Assemble the curated content — rings/topics/papers with cleaned affiliations
   and sectors, plus the week-in-review and highlights prose — into
   **`digest-YYYY-Www.json`** following the schema in the header of
   `scripts/render_html.py`. This JSON is the agent's judgment, captured as data.
2. Render the HTML **deterministically** from it — never hand-write the HTML, so
   the style is identical every week:

   ```bash
   python3 scripts/render_html.py digest-YYYY-Www.json -o digest-YYYY-Www.html
   ```

   The CSS/layout is frozen inside `render_html.py`; to restyle *all* digests,
   edit the `CSS` block there once and re-render. The Markdown digest can be
   written directly (it carries no styling to drift).

## Notes & tuning

- To widen or narrow coverage, edit `CATEGORIES` and the `TOPICS` taxonomy at
  the top of `scripts/fetch_arxiv.py`. Topics are matched in order; the first
  match wins, so more storage-central topics are listed first. Tiers are
  `core` / `adjacent` / `peripheral` (see `PRIORITY_ORDER` and
  `SECTION_TITLES`).
- arXiv's `submittedDate` sort returns the newest first; `--max-per-cat 200`
  comfortably covers a 7-day window for these categories. If a run looks
  truncated (the oldest paper shown is still inside the window), raise it.
- Weekends/holidays post fewer papers; an empty or thin week is normal, not a
  bug.
- Style consistency across weeks comes from `scripts/render_html.py` (frozen
  CSS) fed by `digest-YYYY-Www.json`. Keep HTML generation going through the
  script, not by hand, or the look will drift.
