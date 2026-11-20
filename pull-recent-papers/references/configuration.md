# Configuration reference

Read this when customizing the config (first launch or later), when
`--show-config` reports an error, or when tuning coverage and keyword misfires.

The bundled [`../assets/default-config.toml`](../assets/default-config.toml) is
commented and is the schema reference; the active config is the ground truth
the classifier runs on, so read topics and patterns there rather than copying
them into prose.

## Sections

| Section | Customizes | Used by |
|---|---|---|
| `[digest]` | area: `title`, `field`, arXiv `categories`, `strict_categories`, `days`, `max_results` | script + agent |
| `[reader]` | `context_file` (Markdown, relative to `$CONF`, default `context.md`), `interests`, `author_names` | script resolves the context path; agent reads it |
| `[ranking]` | `preferences` for ordering papers within a topic | agent |
| `[[tiers]]` | priority bands in display order; exactly one `catch_all` tier | script + agent |
| `[[topics]]` | topics in match order, each with a `tier`, regex `patterns`, and optional `exclude` patterns that veto the topic | script |

`--show-config` validates the file (categories present, one catch-all tier,
known tiers, strict categories naming real topics, regex syntax) and exits
non-zero with a message on the first error.

## Tier and topic semantics

- Tiers are priority bands, highest first. The default uses three bands of
  storage proximity: core (the primary field), adjacent (neighboring fields,
  only where they touch the primary field), and a catch-all peripheral band
  (in-category papers with no angle on the field, kept terse so the reader can
  skim what was filtered out).
- Topics are matched in list order against title plus abstract,
  case-insensitively; the first match wins. A topic's `exclude` patterns veto it
  and the paper falls through to later topics.
- Match order is independent of tiers; display groups by tier, then list
  order. To keep broad core patterns from capturing a lower-tier topic's
  papers, list that topic earlier.
- Papers matching no topic land in the `catch_all` tier, so nothing
  in-category is silently dropped. No topic may belong to the catch-all tier.

## Customizing

Ask in one batch, skipping anything the user wants to keep:

- **Area**: the field, and which arXiv categories to pull (suggest candidates
  if they name a field but not categories).
- **Interests**: short phrases to flag connections for.
- **Author names**: the names they publish under, to recognize their own
  papers.
- **Priority**: tier bands and their order, topics to add, remove, or reorder,
  and ranking preferences within a topic.

Copy the default to `$CONF/config.toml` and edit it. For a new field, draft the
tiers and topics yourself: name topics, order them most central first, and
write `patterns` that catch the field's core vocabulary. Show the user the
`--show-config` summary and confirm before the first fetch. Never overwrite an
existing config or context file without asking.

## Tuning

- **Coverage.** Edit `categories`, `[[tiers]]`, and `[[topics]]` in
  `$CONF/config.toml`.
- **High-volume neighbors.** To pull a busy neighboring category for only a
  few topics, add it to `categories` and map it to those topics in
  `strict_categories` (for example `{ "cs.LG" = ["Storage for AI"] }`); its
  other papers are dropped.
- **Window size.** arXiv's `submittedDate` sort returns newest first. The
  script pages through results (1000 per request, 3 s apart) and stops once
  past the window start, so `max_results` is only a cap. The default 600
  covers a busy 7-day window for the default categories; raise it (or pass
  `--max-per-cat`) for broader categories or longer windows, for example
  `--days 30 --max-per-cat 5000`. The script warns when the window is
  truncated.
- **Keyword misfires.** When a generic word matches in an unrelated sense,
  tighten the pattern or add an `exclude` to the topic rather than fixing it by
  curation every week, and report the misfire to the user.
- **Thin weeks.** Weekends and holidays post fewer papers; an empty or thin
  window is normal, not a bug.
