---
name: pull-recent-papers
description: >-
  Configurable weekly arXiv digest and research radar: fetch a recent window of preprints for chosen arXiv
  categories (the bundled default is a storage-systems taxonomy over cs.DB/OS/DC/AR/PF), classify them against a
  custom tier/topic taxonomy, evaluate them, and write a week-in-review with highlights and directions as JSON,
  Markdown, and frozen-style HTML in a user-chosen digest directory. Settings live in a per-user TOML config, and an
  optional reader context frames the digest without filtering it. Use for "weekly digest", "arXiv roundup", "what's
  new on arXiv", "recent papers this week", "last N days of papers", "customize my arXiv digest". For a survey of
  conference proceedings or evidence-bound research ideas from top venues, use system-research-scout.
---

# Pull Recent Papers

A five-stage pipeline that turns a window of arXiv papers into a curated,
evaluated digest for one reader:

```
configure (first launch)  →  fetch  →  filter  →  ranking  →  evaluation  →  presentation
```

- **fetch**: pull the raw candidates from arXiv (script).
- **filter**: keep only window- and field-relevant papers (script gate, then
  agent curation).
- **ranking**: order by tier and topic priority (script), then by strength
  within a topic (agent).
- **evaluation**: judge each kept paper for novelty, relevance, and promise,
  and read the week as a whole for trends (agent).
- **presentation**: week-in-review, highlights, and the grouped digest (agent),
  rendered to HTML by script.

Stages 1-3 are mostly deterministic; stages 4-5 are where the agent adds
judgment.

## Paths

- **`DIR`, the digest directory.** Ask the user where digests live (for example
  `~/notes/arxiv-digests/`). All outputs go there, never into the skills
  repository; the render scripts refuse such a path.
- **`$SKILL`**: the directory containing this file.
- **`$CONF`**: `${XDG_CONFIG_HOME:-~/.config}/agent-skills/pull-recent-papers/`,
  holding the user's `config.toml` and optional `context.md`.

The scripts use only the Python standard library (3.11+ for `tomllib`), plus
`pdftotext` for the affiliation fallback.

## Configuration

Everything field- or reader-specific lives in one TOML file. The fetch script
uses `--config PATH`, else `$CONF/config.toml`, else the bundled
[`assets/default-config.toml`](assets/default-config.toml) (a storage-systems
taxonomy with no personal settings). Sections: `[digest]` (title, field,
categories, `strict_categories`, window), `[reader]` (`context_file`,
`author_names`, and `interests` for readers without a context file),
`[ranking]` (within-topic preferences),
`[[tiers]]`, and `[[topics]]` (regex patterns, first match wins, unmatched
papers fall into the one catch-all tier).

Inspect and validate the resolved config, including the reader context path in
use, without fetching:

```bash
python3 $SKILL/scripts/fetch_arxiv.py --show-config
```

Read [references/configuration.md](references/configuration.md) when
customizing the config, fixing a `--show-config` error, or tuning coverage and
keyword misfires.

### First launch

If `$CONF/config.toml` does not exist, before fetching anything:

1. Run `--show-config` and summarize the default for the user: field,
   categories, tiers and their topics, that no author names are set, and
   which reader context (if any) was found.
2. Ask whether to **use the default** or **customize it**, and wait for the
   answer.
3. **Default:** copy it unchanged so later runs do not ask again:
   `mkdir -p $CONF && cp $SKILL/assets/default-config.toml $CONF/config.toml`.
4. **Customize:** follow "Customizing" in
   [references/configuration.md](references/configuration.md), then confirm
   the `--show-config` summary with the user before the first fetch.

Never overwrite an existing config or context file without asking. The bundled
default stays generic; personal settings go only in `$CONF`.

## Reader context

The reader context is free-form Markdown about who the digest is for. The fetch
script resolves it (`--show-config` prints the result) in this order:

1. `[reader] context_file`, relative to the config's directory (default
   `$CONF/context.md`), if the file exists;
2. else `${XDG_CONFIG_HOME:-~/.config}/agent-skills/user-profile/profile.md`,
   the user's personal profile kept by the separate `user-profile` skill, if it
   exists (read it only: never write, commit, or track it; this skill does
   not need that skill installed);
3. else no context.

When there is no context at all, offer once to create `$CONF/context.md`: ask a
few short questions following the sections of
[`assets/context-template.md`](assets/context-template.md) (background,
interests, current work, resources) and write the answers in that shape. If
the user skips, proceed without context and do not ask again this session.

**One source of truth for interests.** When a reader context exists, it is the
source of the reader's interests and `[reader] interests` is ignored; that list
is only for readers with no context file. If both exist, tell the user once that
the context file wins (`--show-config` flags it). Script-facing settings
(categories, `strict_categories`, topics, `author_names`, ranking) stay in
`config.toml`.

Read the context (or, without one, `[reader] interests`) before ranking and
evaluation.

**Context frames; it never filters.** Use the reader's interests to order
papers within the config's tier and topic priority and to note connections and
tractable openings. Never drop or demote a strong paper because it falls outside
the reader's interests. Keep breadth so unfamiliar directions still appear, and
when a paper outside those interests is among the week's strongest, put it in
the highlights.

## The pipeline

### 1. Fetch

The fetch script queries arXiv for the configured categories, filters to the
window, gates on primary category, tags each paper with a tier and topic, and
prints a grouped Markdown digest in tier order.

**Pick the window so consecutive digests neither overlap nor leave gaps.** Find
the newest `digest-*.json` in `DIR`; if it has `window.end`, start there with
`--since`. Otherwise (first digest, or an older digest without `window`) use the
config's `days`:

```bash
python3 $SKILL/scripts/fetch_arxiv.py --since 2026-10-20T14:43:00+00:00   # previous window.end
python3 $SKILL/scripts/fetch_arxiv.py                                     # first run: last `days` days
```

The window is `[start, end)` with `end` = now. If the gap since the last digest
is unusually long (say, over three weeks), tell the user and ask before pulling
it all at once.

Flags: `--config PATH`, `--days N` or `--since TIME`, `--max-per-cat N`
(overrides `max_results`), `--json` (full structured output, every abstract),
`--curated-json` (same, but strips catch-all papers' abstracts). JSON output
carries `window` (`start`/`end`), `context_file`, `raw_count`, `oldest_raw`, and
`truncated`; papers carry `topic`, `priority` (the tier id), and `skim` (true
for the catch-all tier).

- **Check truncation.** A `WARNING: window truncated` line (`truncated: true` in
  JSON) means the query hit `max_results` inside the window. Re-run with a
  larger `--max-per-cat` and tell the user to raise `max_results`.
- **Default to the cheap path.** The Markdown output truncates abstracts to
  about 500 characters, enough to curate and rank. Pull full abstracts
  (`--curated-json`, or WebFetch on one paper) only for highlight candidates.
- **First-submission date.** The window filters on arXiv `published`, not the
  last revision, so a months-old paper revised this week does not appear.

### 2. Filter

The script applied the hard filters (window and primary category). Now apply
the semantic filter the keywords cannot: decide whether each paper truly
belongs to the configured `field`.

- **Demote or drop by relevance, not keyword.** A paper that hit a generic
  keyword in an unrelated sense (in the default, "cache" in an edge-ML paper)
  goes to the catch-all tier or is dropped.
- **Rescue** relevant papers the keywords missed from the catch-all tier into
  the right topic, and fix obviously mis-slotted topics.
- To claim a theme is absent from the window, search the full `--json` output;
  `--curated-json` strips catch-all abstracts.
- **The reader's own papers.** A paper with an author in `[reader]
  author_names` (check the affiliation too; names collide) is the reader's own.
  Keep it in its topic with `"badge": "Your paper"`, leave it out of
  highlights, most-inspiring, and directions, and note its closest neighbors.

### 3. Ranking

- **Across topics:** keep the config's tier order and topic order.
- **Within a topic:** apply `[ranking] preferences` in order, then the reader
  context as described above.

### 4. Evaluation

Work from abstracts; fetch the abstract page or PDF only when the abstract is
insufficient for a likely highlight. Score each kept paper informally:

- **Novelty**: a new idea or an incremental delta?
- **Relevance**: how central to the configured field (its tier and topic),
  plus any connection to the reader context.
- **Promise**: could it change how systems in the field are built, or open a
  direction? Strong results, a surprising finding, or a clean general
  mechanism all count.

For the stronger papers, add an **opportunity read**; this turns the digest
from a survey into a radar:

- **Entry point?** Does it open or survey a subfield, or list open problems?
- **Crowded or wide open?** Use the affiliation data to tell an emerging
  opening (one or two groups) from a crowded thread (several groups racing).
- **Tractable?** A clean mechanism the reader can learn from and build on, or
  an impressive industry system that is hard to approach? Note it; discard
  neither.
- **Connection?** Note any link to the reader context as an aside.

A paper that opens a direction the reader could plausibly pursue is a
**direction candidate** for "Directions for you". Also read the week as a
whole: cluster papers into themes so you can speak to trends.

**Affiliations.** For every curated paper, extract who is behind it with
`scripts/affiliations.py` and clean the names and academia/industry tag
yourself. Read [references/affiliations.md](references/affiliations.md) for the
procedure.

### 5. Presentation

Produce, in order: (a) the **week in review** (research trends, most inspiring,
directions for you, gaps and open threads; at most five bullets each), (b)
**highlights** led by one "if you read one thing" pick, and (c) the full
**digest** in tier order, with the catch-all tier terse. Read
[references/presentation.md](references/presentation.md) for the content of
each part and the digest JSON fields.

**Output files.** Write into `DIR`, named by the ISO week of the window end:
`digest-YYYY-Www.{json,md,html}` and `digest-YYYY-Www-highlights.md`. Read the
previous digest JSON in `DIR` for its `open_threads` first. If files for that
week already exist, ask before overwriting.

1. Write the curated content as `DIR/digest-YYYY-Www.json`, following the
   schema in the header of [`scripts/render_html.py`](scripts/render_html.py).
2. Write `DIR/digest-YYYY-Www.md` directly.
3. Render the HTML and highlights deterministically from the JSON; never
   hand-write them:

   ```bash
   python3 $SKILL/scripts/render_html.py DIR/digest-YYYY-Www.json --out-dir DIR
   python3 $SKILL/scripts/render_highlights.py DIR/digest-YYYY-Www.json --out-dir DIR
   ```

## Done when

- The four output files exist in `DIR`, and the HTML and highlights were
  rendered by the scripts from the JSON.
- The JSON carries the fetch output's `window` and an `open_threads` list.
- Truncation warnings, keyword misfires, and an unusually long gap were
  reported to the user.
