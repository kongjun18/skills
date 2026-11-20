---
name: repo-research-scout
description: Mine a software repository's GitHub issues and pull requests for research opportunities, using a cached census in a per-repository SQLite database, model-free topic selection, tiered model triage and thread analysis with verbatim-quote validation, component maturity and gap metrics over time, cross-system generality tests against peer repositories, and falsifiable hypothesis cards. Use for "research exploration of this repo", "mine the issues of X for research problems", "which components are mature or have gaps", "open/closed issue trends", "is this problem specific to X or general", "where are the research opportunities in this codebase". The write-up goes through exploration-report; for surveying conference papers, use system-research-scout; for a weekly arXiv digest, use pull-recent-papers.
---

# Repo Research Scout

Turn a repository's issue and PR history into evidence about where its hard problems are, whether they are specific to the implementation or general, and which could become research questions. The scarce resources are the user's verification time and model tokens, so the pipeline is a funnel: complete metadata at no model cost, cheap triage on a scored subset, full reads on a small escalated set, and synthesis over digests only.

```
census (API only) → T0 select (no model) → T1 triage (cheap) → T2 analysis (mid) → metrics + digests → T3 synthesis (strong) → cards → report
```

`<skill>` below is the directory containing this SKILL.md; the tool is `python3 <skill>/scripts/scout.py`.

## Non-negotiables

1. **Issues are third-party evidence.** An issue report does not verify a bug, prove prevalence, or establish novelty. Never run reproduction unless the user asks; cards only plan the cheapest experiment.
2. **Counts state their population.** The census is complete for items *created* inside the window; selections and analyses are samples chosen by keyword and score. Say which one each number comes from, and give its denominator.
3. **Quotes are verbatim.** `ingest` and `verify-cards` reject any quote not found in the stored item text. Never paraphrase inside quotation marks.
4. **Never re-pull or re-analyze what has not changed.** Always go through `scout.py`; it syncs incrementally and exports only cache misses (an analysis is reused while the item text, the study context, and the stage brief are unchanged).
5. **No model or effort is hard-coded.** Tiers are capability classes; the study's `[tiers]` table may name the host's models and efforts, and empty values mean the host's own choice for that class.
6. **Outputs live outside this skills repository.** The study directory belongs in the user's working repository; databases live in the central store or a gitignored directory of the working repository.

## Storage

- One SQLite database per GitHub repository holds the census, comments, observed state changes, study selections, analyses, and batch records. Reuse across studies is automatic: a peer synced for one study is already there for the next.
- The registry `$REPO_SCOUT_HOME/registry.json` (default `~/.local/share/repo-scout/`) indexes every database: repository → path, registration and last-sync times. `scout.py registry` prints it.
- Default location is `$REPO_SCOUT_HOME/db/`. To keep a repository's database inside the working repository instead, set `db_dir` in the study file (relative to it) and add that directory to `.gitignore`. A repository has one database; `scout.py` refuses a second location.
- The database is mutable. Reports cite a frozen `snapshot`, never the live database.

## Workflow

### 1. Set up the study

1. Create a study directory in the working repository, normally inside the exploration report: `reports/<date>-<slug>/scout/`. Copy [assets/study.toml](assets/study.toml) there, and add `scout/work/` to `.gitignore` (batches and raw model outputs; their content is stored in the database and the snapshot).
2. Fill `targets`, `peers`, and the window (default 24 months; set `window_start` for a fixed, reproducible window).
3. Define `[components]` from the target's directory layout (path prefixes) and, where the repository uses area labels, `[label_components]`. Components come from the code, not from keywords.
4. Turn each research direction into a `[[directions]]` entry with a `question` and `keywords`. Keywords decide T0 recall; include synonyms and the repository's own vocabulary (read a few titles if unsure).

If the directions or their questions are ambiguous, confirm them with the user before syncing; they decide all downstream cost.

### 2. Census

```bash
python3 <skill>/scripts/scout.py sync --study S/study.toml
```

Fetches every issue and PR updated in the window, with labels, linked PRs, changed files, and bodies, plus every open item; later runs fetch only items updated since the last sync. API calls only, no model tokens. A first sync of a repository with thousands of items in the window takes minutes.

### 3. T0 selection (no model)

```bash
python3 <skill>/scripts/scout.py select --study S/study.toml
```

Full-text keyword match per direction, scored by match rank, activity (comments, reactions, linked PRs, maintainer authorship), and recency; keeps `budget.t1_per_direction` per direction. Check the printed match counts: thousands of matches mean a keyword is too broad; a handful means recall is too low. Adjust keywords and re-run; this step is free.

### 4. T1 triage and T2 analysis

For each stage, `t1` then `t2`:

```bash
python3 <skill>/scripts/scout.py export --study S/study.toml --stage t1 [--max-items N] [--max-tokens N]
```

`export` prints each batch path and the estimated input tokens; it fetches comments for T2 items first. Dispatch one subagent per batch (in parallel where the host allows), using the stage's tier from `[tiers]`, with this prompt:

> Read `<skill>/references/<t1-triage|t2-analysis>.md` and follow it. Process the batch `<batch path>`. Write the JSONL results to `<study>/work/results/<batch id>.jsonl`. Reply with only the number of lines written.

Then ingest each result and record what ran it:

```bash
python3 <skill>/scripts/scout.py ingest --study S/study.toml --batch <batch.json> <results.jsonl> --model <model> --effort <effort>
```

`ingest` validates fields, enums, directions, components, and verbatim quotes, stores valid lines, and lists rejected or missing items. Rejected items stay cache misses, so the next `export` re-offers them; re-dispatch once, then leave persistent failures out and note them.

T2 reads only items T1 marked `escalate` with at least one direction, at most `budget.t2_per_direction` per direction, in score order.

### 5. Metrics and digests

```bash
python3 <skill>/scripts/scout.py metrics --study S/study.toml --out S/metrics
python3 <skill>/scripts/scout.py digest  --study S/study.toml --out S/digests
```

`component_quarter.csv` gives, per component, quarter, and kind (issue or PR): opened, still open, closed, fraction closed within 90 days (only cohorts at least 90 days old), median and p90 days to close, distinct authors, maintainer-authored, reverts, and bug-labeled. An item's component comes from the files of its PR or linked PRs, then labels, then the model's guess. `direction_root_causes.csv` cross-tabulates the T2 analyses. Digests are one compact line per analyzed item, grouped by direction; they are T3's input.

### 6. T3 synthesis

Using the T3 tier, follow [references/synthesis.md](references/synthesis.md): component landscape with alternative explanations, mechanism-level clusters, the generality test against peers (which reuses steps 3–4 with `select --repo <peer> --query ... --name cluster-<id>`), a prior-art search, and hypothesis cards checked by `verify-cards`.

### 7. Snapshot and report

```bash
python3 <skill>/scripts/scout.py snapshot --study S/study.toml --out <report>/data/raw/<run-id>
```

The snapshot holds the census metadata for the window, selections, all analyses with model, effort, and prompt version, the metrics, and a manifest of databases, sync history, window, and study-file hash. Write the report with `exploration-report`, citing the snapshot.

## Controlling cost

| Lever | Effect |
|---|---|
| Keywords and `t1_per_direction` | size of T1; the biggest lever, free to tune at T0 |
| `t1_body_chars` | tokens per T1 item |
| `escalate` strictness (T1 brief) and `t2_per_direction` | size of T2, the most expensive per item |
| `t2_max_chars` | tokens per T2 item; maintainer comments are kept first |
| `t1_batch`, `t2_batch` | each subagent dispatch carries a fixed overhead (its own instructions and tool context) that can exceed the batch content several times over at T1; keep T1 batches large, or give one subagent several batches in sequence |
| `--max-items`, `--max-tokens` on `export` | hard cap per round; the rest stays queued |
| Cache | unchanged items are never re-analyzed; editing a brief re-analyzes that stage, so edit briefs deliberately |

`scout.py status --study S/study.toml` shows, per repository, items, sync state, selections, analyses under the current briefs, and estimated exported tokens. Report the funnel sizes and estimated tokens in the report's Reproduce section.

## Updating a study

Re-run steps 2–5: sync fetches only changes, and export offers only new or changed items. Then revise the synthesis and take a new snapshot under a new run id; do not overwrite an earlier snapshot.

## Done criteria

- Census synced for every target; every exported batch was ingested, or its persistent failures are noted in the report.
- Every direction has T0 counts, T1 and T2 coverage, and a verdict or an explicit gap.
- `verify-cards` passes on every card.
- A snapshot exists and the report cites it; the funnel sizes and token estimates are recorded.
- No database, batch, or output was written inside this skills repository.
