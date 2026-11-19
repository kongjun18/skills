---
name: system-research-scout
description: Survey the last two years of top systems, database, storage, and networking conference proceedings (OSDI, SOSP, FAST, SIGMOD, VLDB, SIGCOMM, NSDI, ATC, ASPLOS, EuroSys) and turn them into evidence-bound trends, sparks, and research ideas through reader, synthesis, and critic sub-agents, gated by a validator that checks every quote against the papers. Use for "survey recent systems papers", "what are the trends at OSDI/FAST/SIGMOD", "find research gaps", "brainstorm systems research ideas from recent papers", "scout research directions". For a weekly arXiv digest or "what's new on arXiv", use pull-recent-papers; for planning a paper's evaluation, use systems-evaluation-planner.
metadata:
  short-description: Survey top systems papers and brainstorm evidence-bound ideas
---

# System Research Scout

Read two years of top systems proceedings and produce ideas a human can triage quickly, each backed by quoted paper evidence and positioned against prior art. The goal is understanding taste, trends, gaps, and under-articulated pain; it is not validation or paper planning.

The user's scarce resource is verification time, not idea count. Ten sharp, prior-art-positioned, cheaply falsifiable ideas beat fifty buzzword ideas. Two failures are worse than producing too few ideas:

- **Rediscovery**: presenting published work as novel. Every idea is positioned against its closest prior art (Step 6).
- **Buzzword ideas**: idea-shaped text with no named mismatch ("X but for LLMs"). See the anti-patterns in [idea-lenses.md](references/idea-lenses.md).

## Reality and constraints

- **Volume is large.** One venue yields 40-250 papers a year; two years across all venues can exceed 1,000. Read all titles and abstracts; deep-read only a prioritized sample.
- **PDFs are not always reachable.** USENIX and VLDB are open; ACM DL is often bot-blocked. Record `source-blocked`; never fake content.
- **Two years is thin for trends.** With about two instances per venue, "rising vs fading" is weak evidence. State trend claims with calibrated confidence; gate B refuses direction labels for sparse coverage.
- **AI-systems monoculture risk.** Recent proceedings are dominated by LLM serving and training. Give deliberate coverage to durable areas: file systems, kernels, transactions, transport, fault tolerance, verification, isolation, energy. A reader budget that collapses into AI systems is a defect.

## Scope and workspace

- **Venues** (default): OSDI, SOSP, FAST, SIGMOD/PACMMOD, VLDB/PVLDB, SIGCOMM, NSDI, USENIX ATC, ASPLOS, EuroSys.
- **Window** (default): the current calendar year and the previous one. A venue-year that has not happened or has no public proceedings goes in the coverage ledger and is excluded from cross-year comparison.
- **Workspace**: ask the user for an output directory `DIR` outside this skills repository (for example `~/projects/research-radar/scout-<YYYY-MM>`). Every command takes `--out DIR`; the survey script refuses to write inside the skills repository.

`<skill-dir>` below is the directory containing this SKILL.md.

## Outputs

```
DIR/papers/
  metadata.jsonl                 # one row per paper; one row per missing venue-year
  {venue}/{year}/{slug}.pdf      # downloaded PDFs; _cache/ holds fetched HTML
DIR/thinking/
  coverage_ledger.md             # per-venue completeness; gates every cross-year claim
  catalog/{venue}-{year}.md      # 5-line digest per paper (not an abstract paste)
  venue_reads/{venue}-{year}.md  # reader-agent output
  topic_by_conference_year.md, topic_by_year.md, topic_trend.md,
  research_trend.md, research_ideas.md
DIR/sparking/
  {slug}.md                      # one spark = one mismatch
```

Schemas for every file: [final_deliverables.md](references/final_deliverables.md). Do not create `thinking/per_paper/`, paste abstracts into the catalog, or leave TODO-style scaffold sentences (gate A).

## Evidence rules

**Verbatim quotes.** Every quote in the outputs (Pain lines, unnamed pains, Observed mismatch, corroboration, `topic_tag_evidence`) is copied verbatim from the paper. If extraction garbles a passage, skip the quote rather than cleaning, paraphrasing, or completing it. A missing quote is better than a fabricated one.

**Checkable corpus (one rule, enforced by gate C).** A spark's `Observed mismatch` quote must appear, after whitespace, case, ligature, and line-break-hyphen normalization, in one of:

1. a paper's `abstract` in `metadata.jsonl`;
2. a paper's `introduction_excerpt` (the survey script extracts it from the local PDF with `pdftotext`);
3. the full text of the local PDF of a paper the spark cites by exact title.

So a quote from an Evaluation or Limitations section is valid when the cited paper's PDF is local. For a paper with no local PDF, only its abstract and introduction excerpt are checkable. Unnamed pains in venue reads should still come from the Introduction, Evaluation, or Limitations sections, not the abstract (abstracts are marketing copy and rarely surface real pain).

**Separate evidence from inference.** Name the paper and quote for evidence; label extrapolation `speculative`.

## Workflow

Run the steps in order; each step's output is the next step's input.

### Step 1: Verify sources and build the coverage ledger

1. Read [source_manifest.md](references/source_manifest.md); it records availability as last observed.
2. Re-check each venue-year's official page and record its current status. Update the manifest and the script's source tables for years it does not yet cover.
3. Write `thinking/coverage_ledger.md` with `expected_papers`, `observed_papers`, `completeness`, and `status ∈ {published, partial, accepted-list-only, not-yet-published, source-blocked}`.

The ledger gates Steps 4-7: a venue-year below 0.5 completeness gets no reader; below 0.9 it cannot support a direction label.

### Step 2: Collect machine metadata

```bash
python3 <skill-dir>/scripts/survey_top_systems.py --out DIR            # default years: last two
python3 <skill-dir>/scripts/survey_top_systems.py --out DIR --years 2025 2026 --no-download
```

A collection run needs `requests` and `beautifulsoup4` (for example `uv run --with requests --with beautifulsoup4 python ...`) and `pdftotext` for introduction excerpts. The script downloads directly available PDFs (reusing valid cached PDFs, marked `downloaded-cached`), records blocked downloads, parses USENIX awards, strips BibTeX boilerplate, assigns `topic_tags_keyword_seed` and `priority_seed`, extracts `introduction_excerpt`, and writes the per-venue catalog. It collects and scaffolds; it does not curate. `--print-intro PAPER.pdf` shows the excerpt for one PDF.

Start a fresh survey with empty `DIR/thinking` and `DIR/sparking`; stale outputs leak into reader context. Keep `DIR/papers`, the input cache. To re-fetch one paper, delete its PDF.

Metadata fields: `venue`, `year`, `title`, `authors`, `abstract`, `doi`, `pdf_url`, `source_url`, `local_pdf`, `download_source`, `download_error`, `source_status`, `awards`, `priority_seed`, `topic_tags_keyword_seed` (scaffold only), `topic_tags_curated` and `topic_tag_evidence` (filled in Step 4), `introduction_excerpt`.

### Step 3: Catalog digests

For each venue-year with `source_status ∈ {published, partial}`, check `thinking/catalog/{venue}-{year}.md`: exactly five lines per paper (title and lead author, curated tags, claim, pain, PDF). Readers replace the script's heuristic Pain line with a verbatim quote from the introduction when one exists.

### Step 4: Reader agents (parallel)

One reader per venue-year with `completeness ≥ 0.5`. Read [taxonomy-and-priority.md](references/taxonomy-and-priority.md) first.

- **Input:** that venue's catalog file and its `must-read` PDFs.
- **Budget:** at most 25 papers: `must-read`, then `should-read`; ignore `skim`.
- **Anti-monoculture sampling:** cluster candidates by keyword seed; for each cluster of 4 or more, read at most one flagship and one contrarian or outlier. Spend the rest on small clusters and durable areas. Record the sampling distribution at the top of the venue read.
- **Curate tags:** fill `topic_tags_curated` (at most 3) with a quoted abstract sentence per tag in `topic_tag_evidence`.
- **Output:** `thinking/venue_reads/{venue}-{year}.md` with Taste (at most 3 comparative sentences), Top 10 by signal strength with reasons, three Unnamed pains (quotes with exact section header), and 2-3 venue-specific sparks.

Readers do not see each other's output.

### Step 5: Synthesis agents (digests, not papers)

One synthesis agent per theme cluster chosen from what readers surfaced. Read [idea-lenses.md](references/idea-lenses.md) and apply its generation moves.

- **Input:** only the union of `thinking/venue_reads/*.md`. Synthesis agents do not read raw papers or full catalogs; this keeps the evidence chain auditable.
- **Output:** notes the orchestrator merges into `thinking/topic_by_year.md` and draft `sparking/*.md`.
- **Required:** reconcile contradictions across venues by naming both positions and quoting one paper from each side.

### Step 6: Critic agent

Runs after synthesis, in two phases:

- **6a Novelty check (never skip).** For each draft spark and idea: search the catalog for papers that already do it; web-search the specific framing and at least two nearest baselines; land on 2-5 closest prior-art papers, each with one line on how the idea differs and what they leave open. If prior art already does it, kill it (`Status: killed-by-critic: already-published`, cite the paper) or sharpen it into the gap and say so. Without a prior-art line, an item cannot be ranked; it stays a spark with `Status: needs-novelty-check`.
- **6b Kill attempt.** Try to kill each survivor with a catalog digest line that solves most of it, an absent workload (no venue read quotes anyone needing it), a charitable reading of an existing system, a violated physical or theoretical bound (CAP, PACELC, speed of light, PCIe/CXL/HBM/NIC ceilings), or access the intended researcher lacks (`Status: access-blocked`).

Killed items stay in their files with the reasoning; they teach later runs what not to propose. A survivor records `Critic notes: survived: {what the critic conceded}`.

### Step 7: Trends, sparks, ideas

Write the remaining `thinking/` files and `sparking/*.md` from the schemas, with a `Lens applied:` field on every spark and idea. Promote a spark to `research_ideas.md` only through the promise filter in [idea-lenses.md](references/idea-lenses.md).

`topic_trend.md` references `coverage_ledger.md`, uses `signal_strength ∈ {strong, weak, insufficient}`, and uses `direction ∈ {rising, stable, fading, emerging}` only when both compared years reach 0.9 completeness in the same venue set; otherwise `direction: unknown — partial coverage`.

### Step 8: Validate

```bash
python3 <skill-dir>/scripts/validate_outputs.py --out DIR
```

Fix every flagged issue and re-run. The skill is not complete until it exits 0.

## Sub-agent contract

| Agent | Inputs | Output | Hard rules |
|---|---|---|---|
| Reader | one catalog file, its PDFs (`must-read` first) | `venue_reads/{venue}-{year}.md`, curated tags | at most 25 papers; three quoted unnamed pains with section headers, never from the abstract |
| Synthesis | union of `venue_reads/*.md` only | merged notes, draft sparks | no raw papers or full catalogs; quote both sides of cross-venue disagreements |
| Critic | draft sparks and `research_ideas.md` | `Status:` and `Critic notes:` annotations | novelty check first; attempt to kill every item; killed items stay |

## Pre-flight gates (`validate_outputs.py`)

- **J. Non-empty outputs:** metadata has papers, at least one paper has curated tags, at least one spark exists, venue reads, the coverage ledger, and at least one idea exist. An empty run fails.
- **A. No scaffolding:** no `TODO`, `TBD`, `refine after`, `infer from`, `look for`, `Title TBA`, `to be filled`, `placeholder` outside code fences.
- **B. Coverage-gated trend:** `topic_trend.md` cites the ledger; every row has `Completeness:`; direction labels need 0.9 in both years.
- **C. Evidence chain:** every spark has an Observed mismatch quote that satisfies the checkable-corpus rule above.
- **D. Spark diversity:** no two sparks share more than 50% of cited papers.
- **E. Tag justification:** every curated tag has an evidence quote found in the abstract.
- **F. Lens applied:** every spark and idea names one or two of L1-L11.
- **G. No forbidden tag:** no `general-systems`.
- **H. Awards parsed:** award markers in authors or notes imply a non-empty `awards`.
- **I. Idea grammar:** each idea has `One-sentence idea`, `Baseline that breaks`, `Closest prior art`, and at least three papers with role tags.

## Done criteria

- Every venue-year in scope is analyzed or recorded in the coverage ledger; no fake rows for unavailable venue-years.
- Every ranked idea names the changed workload, the stale assumption, the missing abstraction, the baseline that breaks, and 3-8 role-tagged papers, and survived the critic.
- Solo signals are kept as `solo-signal`, not deleted; ambiguous sparks are welcome when grounded in quotes.
- `validate_outputs.py --out DIR` exits 0, and all outputs live in `DIR`, outside the skills repository.
