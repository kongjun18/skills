# Final Deliverable Schemas

Schemas for every output the skill produces. The validator in `scripts/validate_outputs.py` enforces required fields. Do not invent new fields silently; if a new field is needed, add it here first.

## Coverage Ledger

`thinking/coverage_ledger.md`. The gate for every cross-year claim. Write one block per `(venue, year)` covered in the scope window.

```markdown
## {Venue} {Year}

- Source URL: {official accepted/program page}
- Status: {published | partial | accepted-list-only | not-yet-published | source-blocked}
- Expected papers: {integer, from program; "unknown" only if program is private}
- Observed papers: {integer, from papers/metadata.jsonl}
- Completeness: {observed / expected, two decimals; "n/a" if expected is unknown}
- Notes: {what was missing, what was blocked, whether trend comparison is allowed}
```

Rules:
- A venue/year with `completeness < 0.5` is **excluded** from reader-agent fan-out.
- A venue/year with `completeness < 0.9` is **excluded** from `direction:` labels in `topic_trend.md`.

## Per-Venue Catalog Digest

`thinking/catalog/{venue}-{year}.md`. One file per `(venue, year)`. The 5-line digest format is the unit of recall for synthesis agents.

```markdown
# Catalog — {Venue} {Year}

Source: {accepted papers URL}. Completeness: {from coverage_ledger.md}.

- **{Paper Title}** — {first-author last name} et al.
  - Curated tags: {≤3 tags from §5 taxonomy; or "other (subtopic: ...)"}
  - Claim: {one sentence — what the paper says it achieved}
  - Pain: {one sentence — quoted "future work" / "we assume" / "in practice" snippet, OR "—"}
  - PDF: papers/{venue}/{year}/{slug}.pdf  (or "metadata-only: {reason}")
```

Rules:
- No abstract pasting. The digest replaces the old per-paper abstract dump.
- `Curated tags` must come from the §5 taxonomy. The keyword-seed list from `metadata.jsonl` is *not* sufficient.
- `Pain` must be a quote when possible; if the paper has no surfaced pain, write `—` (the validator will not flag `—`).

## Venue Read

`thinking/venue_reads/{venue}-{year}.md`. Output of a reader agent.

```markdown
# Venue Read — {Venue} {Year}

Papers in scope: {N}. Read in detail: {n ≤ 25}. Skipped: {n - read} ({reason}).

## Taste

{≤3 sentences. Comparative against the same venue's prior year if available.}

## Top 10 by signal strength

1. **{Title}** — {one-line reason: deployment scale | novel mismatch | cross-cutting authors | follow-on potential | award status}
... (10 entries)

## Unnamed pains

- **{Paper Title}**, {section}: "{direct quote ≤2 sentences}"
- **{Paper Title}**, {section}: "{direct quote ≤2 sentences}"
- **{Paper Title}**, {section}: "{direct quote ≤2 sentences}"

## Venue-specific sparks

- {one-paragraph spark with paper citation; 2–3 entries}
```

## Topic By Conference-Year

`thinking/topic_by_conference_year.md`. Anchored in `venue_reads/*`, not in keyword tags.

```markdown
## {Venue} {Year}

- Taste summary: {one comparative sentence from the venue_read Taste section}
- Dominant curated tags: {tag: count — only tags with count ≥ 3; cite digest lines}
- Representative papers: {3–5 titles, each with a one-line "why representative"}
- What this venue rewarded: {derived from venue_read Top 10 reasons}
- Sour or underdeveloped points: {derived from venue_read Unnamed pains, paraphrased}
```

Forbidden: `infer from`, `look for`, `refine after`, `What this venue appears to reward` (passive scaffold language). State the claim or omit the line.

## Aggregated Topic By Year

`thinking/topic_by_year.md`.

```markdown
## {Year}

- Coverage: {list of venues with completeness ≥ 0.9; list partial venues separately}
- Most important topics: {tag: cross-venue prevalence ratio = (venues_with_tag / venues_covered); only tags with ratio ≥ 0.5}
- Cross-venue topics: {tag — list of venues where it dominated, with at least one digest-line citation per venue}
- Venue-specific topics: {tag — venue, with one digest-line citation; only if the tag dominated in exactly one venue}
- Why these topics matter: {≤3 sentences linking ratios to the §7 lenses}
- Papers anchoring the analysis: {≤5 titles per topic, each with venue and curated tags}
```

## Topic Trend

`thinking/topic_trend.md`. **Gated on coverage_ledger.md.** The validator rejects rows that label `direction:` without sufficient completeness.

```markdown
> See `coverage_ledger.md`. Trend rows compare venues with completeness ≥ 0.9 in BOTH years; rows with partial coverage are labeled `direction: unknown — partial coverage`.

## {Tag}

- Year A signal: {prevalence ratio across complete venues}, supported by {paper count}
- Year B signal: {prevalence ratio across complete venues}, supported by {paper count}
- Completeness: A={list venues}, B={list venues}
- Signal strength: {strong | weak | insufficient}
- Direction: {rising | stable | fading | emerging | unknown — partial coverage}
- Evidence: {≥2 digest-line citations per year, OR if labeled unknown: "n/a — see Completeness"}
- Interpretation: {one sentence; if Direction is unknown, explain what data would resolve it}
```

## Research Trend

`thinking/research_trend.md`. Broad, possibly ambiguous trends. Each trend cites at least two venue_reads.

```markdown
## {Trend Name}

- Evidence venues: {≥2 venue_reads citations}
- Lens applied: {one of L1–L11 from SKILL.md §7}
- Trend: {≤4 sentences naming the changed workload/hardware/scale, and what abstraction it strains}
- Open question: {one sentence — the question this trend raises but does not answer}
```

## Spark

`sparking/{normalized-idea-title}.md`. One spark = one mismatch.

```markdown
# {Spark Title}

- Status: {vague | promising | solo-signal | not-yet-falsifiable | killed-by-critic | survived}
- Lens applied: {one or two of L1–L11}
- Related topics: {tags from §5 taxonomy}
- Observed mismatch: "{verbatim quote ≤2 sentences from one paper}" — {Paper Title} ({Venue Year}), {section}
- Cross-paper corroboration: "{quote from a DIFFERENT paper hitting the same pain}" — {Paper Title} ({Venue Year}), {section}.
  IF NONE: set Status to `solo-signal` and write "none found — single-paper signal".
- Disconfirming evidence: {a paper or sentence that, if true, would weaken the spark, with paper title and one-line reason}.
  IF NONE: set Status to `not-yet-falsifiable` and write "no candidate disconfirmation found".
- Trigger: {what made the reader/synthesizer notice this — ≤2 sentences}
- Rough idea: {≤3 sentences. Name the missing abstraction; do not propose a design.}
- Why it might matter: {≤2 sentences. Specific to this spark — no boilerplate.}
- Critic notes: {filled by critic agent in Step 6; "n/a — not yet reviewed" until then}
```

Rules:
- The Observed mismatch quote must be findable in `papers/metadata.jsonl` (validator gate §10.C).
- Do not reuse the same `Why it might matter` sentence across sparks.
- The set of cited papers must differ by >50% from every other spark file (validator gate §10.D).

## Detailed Research Idea

`thinking/research_ideas.md`. One H2 per idea.

```markdown
## {Idea Title}

- One-sentence idea: {one plain sentence naming artifact, workload, mechanism, baseline, metric, and falsifier}
- Lens applied: {one or two of L1–L11 from SKILL.md §7}
- Relevant topics: {tags from §5 taxonomy}
- Key papers (each with role tag):
  - {Title} ({Venue Year}) — motivating: {one sentence on why}
  - {Title} ({Venue Year}) — corroborating: {one sentence on why}
  - {Title} ({Venue Year}) — solves-one-piece: {one sentence on what piece}
  - {Title} ({Venue Year}) — competing-approach: {one sentence on the alternative}
  - {Title} ({Venue Year}) — disconfirming: {one sentence on what would invalidate the idea}
- Background: {≤4 sentences. Quote one paper sentence.}
- Motivation: {≤4 sentences. Quote one paper sentence naming the pain.}
- Missing point / sour point: {what no paper currently names}
- Workload or architecture mismatch: {pick L1 specifically: workload/hardware/scale/operations}
- Why now: {what changed in the last 2 years that makes this idea timely; cite ≥1 paper}
- Core research question: {one sentence, falsifiable}
- Baseline that breaks: {specific stack + workload + metric. e.g. "vLLM v0.6 + FAISS + Postgres under 1% per-minute row churn at 32k context — recall drops to X% within Y minutes"}
- What this idea is NOT: {≤3 sentences naming scope creep to avoid}
- Closest prior art: {2–5 papers, each on one line: "{Title} ({Venue Year}) — how this differs / what they leave open". Populated by the Step 6a novelty check.}
- Rough feasibility: {≤3 sentences. Name the prototype stack and the experiment that would settle the core question.}
- Why it might be a dead end: {one or two sentences naming an honest failure mode or access/data barrier — e.g. "needs hyperscale RAG traffic we don't have", "depends on CXL switches that aren't shipping yet".}
- Score: novelty {1–5} · tractability {1–5} · impact {1–5} · evidence {1–5}
  - Novelty: distance from the closest prior art listed above (5 = no one is doing this).
  - Tractability: can a small team test the *core claim* cheaply, ideally with a measurement study before any system is built? (5 = a one-week experiment could validate or kill it).
  - Impact: does solving it matter to real deployments (multi-tenancy, cost, tail latency, durability, correctness), not just a microbenchmark? (5 = changes how a class of systems is built).
  - Evidence: how grounded the mismatch is in observed paper pain vs your extrapolation.
- Uncertainty: {what could make this idea wrong}
- Critic notes: {survived | killed-by-critic + reasoning | needs-novelty-check | access-blocked}
```

Rules:
- `One-sentence idea` is required and must be specific enough that a student can start implementing or measuring it this week.
- ≥3 papers, each with a role tag. Flat title lists are rejected (validator gate §10.I).
- `Baseline that breaks` must be a concrete stack and workload, not "trace-driven evaluation".
- `Closest prior art` must list 2–5 real papers from `papers/metadata.jsonl` or from the web-search novelty check (in which case cite the source URL).
- Citing papers that do not appear in `papers/metadata.jsonl` is rejected *unless* they are listed under `Closest prior art` with a URL — the novelty check is expected to reach outside the scrape window.

## Idea Identification Lens (apply when drafting any spark or idea)

For every trend, spark, or detailed idea, ask:

- L1 — What mismatch changed: workload/software, hardware/software, scale/assumption, or operations/abstraction?
- L2 — What unnamed pain did a paper mention vaguely? (Quote it.)
- L3 — Is this structural, or only an incremental optimization?
- L4 — Does the topic recur across venues? (List them.)
- L5 — What did current papers ignore: multi-tenancy, recovery, freshness, observability, cost, correctness, durability, security, or deployment?
- L6 — Is this a bottleneck caused by the success of a new system pattern?
- L7 — Are solutions fragmented across storage, networking, scheduling, database, and OS communities?
- L8 — Operational reality: skew, failures, noisy neighbors, tail latency, upgrades, cost?
- L9 — Topic vs idea: have you named a missing abstraction, or only a research area?
- L10 — What is the falsifiable claim, and what observation would weaken it?
- L11 — What user-space workaround reveals a missing OS, network, runtime, or database primitive?

Record the one or two lenses you used as `Lens applied:`.
