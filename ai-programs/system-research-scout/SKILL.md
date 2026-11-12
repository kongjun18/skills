---
name: system-research-scout
description: Use when an agent must survey recent top systems/database/storage/networking conference papers, download available PDFs, curate evidence-bound topic and trend analyses, fan out reader/synthesis/critic sub-agents, preserve falsifiable sparks, and synthesize promising systems research ideas grounded in papers. The skill enforces an evidence chain from quoted paper claims to ideas; outputs that lack that chain fail the pre-flight gates and are not considered complete.
metadata:
  short-description: Survey top systems papers and brainstorm evidence-bound ideas
---

# System Research Scout

Use this skill to read the last two years of top systems papers and brainstorm promising research ideas. The goal is not validation or paper planning; the goal is to understand taste, trends, gaps, sour points, and under-articulated opportunities, and to write down the *evidence* that supports each spark and idea so a peer can audit it.

The skill is opinionated. Outputs that mix topics with ideas, paste TODO-style scaffold sentences, or list paper titles without quoting what those papers actually claim do not pass the pre-flight gates in §10 and are not considered complete.

### What "good output" means

The user's scarce resource is **human verification time**, not idea count. Optimize every deliverable for **triage speed**: ten sharp, prior-art-positioned, cheaply-falsifiable ideas beat fifty buzzword ideas. The single highest-value thing this skill does is save the human from spending a week on an idea that (a) was already published or (b) rests on an assumption that isn't actually violated in practice.

Two failure modes are worse than producing too few ideas:

- **Rediscovery** — presenting something already published as if novel. Every idea must be positioned against its closest prior art (Step 6 below).
- **Buzzword ideas** — idea-shaped text with no concrete named mismatch ("X but for LLMs", "add ML to the scheduler"). See §7c for the kill-on-sight list.

### Reality and constraints

- **Volume is large.** A single OSDI/SOSP yields ~40–60 papers; SIGMOD/VLDB each yield 150–250+/year. Two years across all default venues can exceed 1,000 papers. You cannot deep-read all of them — read all titles+abstracts, then deep-read only the prioritized sample (§3 Step 4, §6).
- **PDFs are not always reachable.** USENIX (OSDI/SOSP-recent/FAST/ATC/NSDI) and VLDB are open; ACM DL (SOSP older, SIGMOD, SIGCOMM, ASPLOS, EuroSys) is often bot-blocked. For *scouting*, title + abstract + intro is usually enough; reserve full-PDF reads for the deep-read sample. Record `source-blocked`, never fake content.
- **Two years is thin for trend claims.** With ~2 instances per venue, "rising vs fading" is a weak statistical signal — this is exactly why gate B (§10.B) refuses `direction:` labels for sparse venues. State trend claims with calibrated confidence and never present a 2-point trend as established.
- **AI-systems monoculture risk.** 2024–2026 proceedings are flooded with LLM serving/training/RAG papers, and most models over-weight them. Deliberately give balanced coverage to durable, "boring" areas too: file systems, OS kernels, consistency & transactions, network transport, fault tolerance, verified systems, isolation/security, energy. A reader budget that collapses into AI-systems is a defect, not a feature.

## 1. Scope

Default venues: OSDI, SOSP, FAST, SIGMOD/PACMMOD, VLDB/PVLDB, SIGCOMM, NSDI, USENIX ATC, ASPLOS, EuroSys.

Default time window: the last two calendar years implied by the current date. For 2026-06-09, use 2025 and 2026. If a conference has not happened or proceedings are not published, record it in the coverage ledger (§10.B) and **exclude it from any cross-year comparison**.

## 2. Required Outputs

Store PDFs and machine metadata in `./papers/`. Store curated analysis in `./thinking/`. Store tentative ideas in `./sparking/`.

```
papers/
  metadata.jsonl                 # one row per real paper; one row per missing venue-year
  {venue}/{year}/{slug}.pdf      # downloaded PDFs

thinking/
  coverage_ledger.md             # per-venue completeness, drives every cross-year claim
  catalog/{venue}-{year}.md      # 5-line digest per paper (NOT a full abstract paste)
  venue_reads/{venue}-{year}.md  # reader-agent output: top papers, taste, unnamed pains
  topic_by_conference_year.md    # per-venue taste, anchored in venue_reads/*
  topic_by_year.md               # aggregated yearly topics, normalized by coverage
  topic_trend.md                 # cross-year comparison, gated on coverage_ledger.md
  research_trend.md              # broad trends, including ambiguous signals
  research_ideas.md              # detailed evidence-bound ideas

sparking/
  {slug}.md                      # one file per spark; one spark = one mismatch
```

**Do not create** `thinking/per_paper/`. Do not paste abstracts verbatim into `thinking/catalog/*` — use the 5-line digest. Do not write TODO-style sentences (the pre-flight gate in §10.A will reject them).

**Strict quote rule.** Every quote in this skill's outputs (Pain lines, Unnamed pains, Observed mismatch, Cross-paper corroboration, topic_tag_evidence) must be copy-pasted verbatim from the paper's actual text. If PDF extraction yields garbled or mojibake'd text in a passage, **skip the quote rather than cleaning it up, paraphrasing, or hallucinating words**. A missing quote is better than a fabricated one — the evidence-chain gate in §10.C is built on this rule.

## 3. Mandatory Workflow

Run the workflow in order. Each step's output is the next step's input; do not skip ahead.

### Step 1 — Verify sources and build the coverage ledger

1. Read [the source manifest](references/source_manifest.md).
2. Re-check each venue/year's official page; record current status.
3. Write `thinking/coverage_ledger.md` using the schema in `references/final_deliverables.md`. For each `(venue, year)` row include `expected_papers` (from the program), `observed_papers` (from metadata.jsonl), `completeness = observed / expected`, and `status ∈ {published, partial, accepted-list-only, not-yet-published, source-blocked}`.

The coverage ledger is the **gate** for §6–§7. Any cross-year claim must cite it.

### Step 2 — Collect machine metadata

Run the recommended script (§4) to populate `papers/metadata.jsonl` and download PDFs. The script does not assign curated topic tags or ideas — it only collects, normalizes, and flags.

Metadata fields (per paper): `venue`, `year`, `title`, `authors` (BibTeX-stripped, UTF-8 normalized), `abstract`, `doi`, `pdf_url`, `source_url`, `local_pdf`, `download_source`, `download_error`, `source_status`, `awards` (list, e.g. `["best-paper"]`), `priority_seed ∈ {must-read, should-read, skim}`, `topic_tags_keyword_seed` (list — *first-pass scaffold only*), `topic_tags_curated` (list — filled by an agent in Step 4), `topic_tag_evidence` (map: tag → one quoted abstract sentence).

`topic_tags_keyword_seed` is a starting point. **Do not derive trend or taste analyses from it**; it is biased by title vocabulary (e.g. SIGMOD's "Data Chunk Compaction in Vectorized Execution" looks like AI). Use `topic_tags_curated` instead, which the reader agent fills with a quoted justification.

### Step 3 — Split the catalog and build digests

For each `(venue, year)` with `source_status ∈ {published, partial}`, write `thinking/catalog/{venue}-{year}.md`. Each paper is one entry of **exactly five lines**:

```
- **{Title}** — {first-author last name} et al.
  - Curated tags: {≤3 from §5 taxonomy}
  - Claim: {one sentence — what the paper says it achieved}
  - Pain: {one sentence — the "future work", "we assume", or "in practice" snippet, OR "—" if none surfaced}
  - PDF: papers/{venue}/{year}/{slug}.pdf
```

Do **not** paste the abstract. The digest is the unit of recall for synthesis agents in Step 5.

### Step 4 — Reader agents (parallel fan-out)

Spawn one **reader agent** per `(venue, year)` whose `source_status ∈ {published, partial}` and `completeness ≥ 0.5`. The reader agent contract:

- Input: the venue's `thinking/catalog/{venue}-{year}.md` and the PDFs flagged `must-read` (see §6).
- Budget: ≤25 papers per reader. If a venue exceeds 25, the reader prioritizes `must-read` first, then `should-read`, and ignores `skim`.
- **Sampling rule (anti-monoculture):** after sorting by priority, before reading, cluster the candidates by `topic_tags_keyword_seed`. For each cluster with ≥4 candidates, read **at most one flagship** (highest priority) **and one contrarian or outlier** (e.g. an industry paper that disagrees with the cluster, or a small-team paper attacking the cluster's premise). Spend the remaining budget across small clusters and the durable-systems areas listed in "Reality and constraints" above. A reader budget that collapses into a single keyword cluster is a defect — record the sampling distribution at the top of the venue read.
- Output: `thinking/venue_reads/{venue}-{year}.md` with these required sections:
  - **Taste** (≤3 sentences): what this venue rewarded *this year*, written as a comparative statement against the *same venue's* prior year if available.
  - **Top 10 by signal strength**: titles + one-line reason — *why* it is a strong signal (deployment scale, novelty of mismatch, cross-cutting authors, follow-on potential), not just citation count.
  - **Unnamed pains**: three direct quotes drawn **strictly from the Introduction, Evaluation, or Limitations/Future Work sections** (never the Abstract — abstracts are PR copy and rarely surface real pain). Each quote ≤ 2 sentences, with paper title and exact section header.
  - **Venue-specific sparks**: 2–3 sparks the reader saw only in this venue.

Reader agents run in parallel. They do not see each other's output.

### Step 5 — Synthesis agents (read digests, not papers)

Spawn one **synthesis agent** per theme cluster. Suggested clusters (adjust based on what readers surfaced; do not invent clusters with no reader evidence):

- `kv-cache-lifecycle` — HBM/DRAM/SSD/network placement, sharing, eviction, privacy of KV state.
- `derived-data-freshness` — embeddings, features, summaries, generated queries; refresh/lineage/staleness contracts.
- `disaggregated-memory-operability` — CXL/remote memory observability, blame assignment, isolation.
- `learned-component-risk` — learned indexes, optimizers, caches; regression budgets, fallback.
- `silent-failures-in-training` — SDC, drift, checkpoint integrity, recovery.
- `agentic-data-pipelines` — LLM agents mutating databases/tools; isolation, replay, compensation.

Synthesis agent contract:

- Input: **only** the union of `thinking/venue_reads/*.md`. Synthesis agents do **not** read raw papers or full catalog files; this prevents context-overflow regression and keeps the evidence chain auditable.
- Output: short notes used by Step 6 and 7. Synthesis agents append to a scratch buffer the orchestrator merges into `thinking/topic_by_year.md` and `sparking/*.md`.
- Required behavior: reconcile contradictions across venues. If FAST 2025 and OSDI 2026 disagree on whether KV cache is a storage or memory problem, the synthesis agent **names both positions** and quotes one paper from each side.

### Step 6 — Critic agent

Spawn one **critic agent** after synthesis. The critic runs two phases.

**Phase 6a — Novelty check (do not skip).** This is the acceleration step that saves the human the most time. For each draft spark and detailed idea, the critic must:

- Search the catalog (`thinking/catalog/*`) for any paper that already does this thing or a substantial part of it.
- Web-search the specific framing (`{verb}{noun}` of the idea title) and at least two nearest baselines named in `Closest prior art`. Use the venue+year+core-mechanism phrase, not vague keywords.
- Land on 2–5 closest prior-art papers. For each, write one line: *how this idea differs* and *what those papers leave open*.
- If the closest prior art already does the idea: either kill it (mark `Status: killed-by-critic — already-published`, cite the paper) **or** sharpen the idea into the specific gap they left and say so explicitly.

A spark or idea with no prior-art line cannot enter the ranked output. Sparks with weak prior-art lines stay in `sparking/` with `Status: needs-novelty-check`.

**Phase 6b — Kill attempt.** After novelty check survives, the critic tries to **kill** the surviving items by:

- Naming a paper from `thinking/catalog/*` that already solved a substantial part of it (cite the digest line).
- Arguing the workload isn't real (e.g., no paper in `venue_reads/*` quotes operators asking for it).
- Showing the "mismatch" disappears under a charitable reading of an existing system.
- **Asserting physical or theoretical bounds.** Argue the idea violates CAP, PACELC, the speed of light (minimum round-trip latency given geography), or strict hardware ceilings (PCIe/CXL bandwidth, HBM capacity, NVLink fan-out, NIC packet rate). If a paper claims a target that requires breaking a bound, the idea is killed or restated.
- **Untestable by the intended researcher.** If validating the core claim needs proprietary workloads or hardware the user cannot access, the critic notes this and the idea moves to `sparking/` with `Status: access-blocked` — it is not promoted to ranked ideas without an alternative experiment.

If the critic kills a spark or idea, mark it `Status: killed-by-critic` with the critic's reasoning. **Do not delete it** — killed ideas teach future runs what NOT to propose.
If the critic cannot kill it, record `Critic notes: survived — {one sentence on what the critic conceded}`. A surviving idea is the strongest endorsement the skill produces.

### Step 7 — Trends, sparks, ideas

Write `thinking/topic_by_conference_year.md`, `thinking/topic_by_year.md`, `thinking/topic_trend.md`, `thinking/research_trend.md`, `thinking/research_ideas.md`, and `sparking/*.md` using the schemas in `references/final_deliverables.md`. Apply the principles in §7 as an explicit `Lens applied:` field on every spark and idea.

The trend file (`topic_trend.md`) is **gated**: rows must reference `coverage_ledger.md` and use `signal_strength ∈ {strong, weak, insufficient}`. Use `direction ∈ {rising, stable, fading, emerging}` only when both compared years have `completeness ≥ 0.9` *in the same set of venues*. Otherwise, set `direction: unknown — partial coverage` and explain in the row.

### Step 8 — Run the pre-flight validator

Run `python system-research-scout/scripts/validate_outputs.py --thinking thinking --sparking sparking --papers papers`. If it returns non-zero, fix the flagged issues and re-run. The skill is not complete until the validator passes.

## 4. Recommended Script

Run from the caller workspace:

```bash
python system-research-scout/scripts/survey_top_systems.py \
  --years 2025 2026 \
  --out-papers papers \
  --out-thinking thinking \
  --out-sparking sparking
```

The script downloads directly available PDFs, records blocked downloads, removes stale `thinking/per_paper/`, writes the per-venue catalog files under `thinking/catalog/`, tags papers with `topic_tags_keyword_seed`, parses USENIX award markers and industry-track signals into `awards` and `priority_seed`, strips BibTeX boilerplate from authors, and normalizes UTF-8. The script is the **collection and scaffolding step, not the researcher**. Curated tags, sparks, and ideas are filled by agents in Steps 3–7.

**Re-run is idempotent for PDFs.** If `papers/{venue}/{year}/{slug}.pdf` already exists, starts with the `%PDF` magic, and is at least 4 KB, the script reuses it and marks `source_status: downloaded-cached` instead of re-fetching. This protects the user's previously-downloaded corpus across runs and avoids hammering USENIX/VLDB. Agents must treat `downloaded-cached` identically to `downloaded` for reading purposes. To force a re-download of a specific paper, delete its local PDF before running the script; to force a full re-download, delete the relevant `papers/{venue}/{year}/` subdirectory.

**Clean run-environment.** Before starting a fresh survey, ensure `thinking/` and `sparking/` are empty (or absent). Stale outputs from previous runs trip the validator's no-scaffolding gate and can leak into reader-agent context. Leave `papers/` alone — it is the *input* cache, not output. The recommended reset is `rm -rf thinking sparking` from the caller workspace; the script will recreate them.

Validate the run:

```bash
python system-research-scout/scripts/validate_outputs.py \
  --thinking thinking --sparking sparking --papers papers
```

## 5. Topic Taxonomy

Use these 16 leaves for `topic_tags_curated`. Apply by reading the abstract and intro — *not* by matching keywords. Each tag requires a one-sentence quoted justification in `topic_tag_evidence`. Multi-tag is allowed but ≤3 tags per paper.

| Tag | Definition (apply if the paper's primary contribution targets this) |
|---|---|
| `llm-serving-engine` | Inference scheduler, attention kernel, request batching, decoding parallelism. |
| `llm-training-substrate` | Distributed training, collective comm, parallelism strategies, fault tolerance for training. |
| `kv-cache-mgmt` | Lifecycle, placement, sharing, eviction, compression of KV state across tiers. |
| `vector-retrieval` | ANN index structure, recall/latency tradeoffs, hybrid retrieval, vector storage. |
| `rag-data-plane` | Pipelines/contracts/freshness between source data, embeddings, retrievers, and LLMs. |
| `cxl-disagg-memory` | CXL pods, remote memory pools, tiered memory, coherence under disaggregation. |
| `cloud-object-storage` | Object stores at scale, geo-distribution, erasure coding, archival/tape tiers. |
| `local-flash-storage` | SSD/NVM file systems, request-to-IO transformations, write-ahead logs, microkernel recovery. |
| `learned-index-or-optimizer` | ML-driven indexes, query optimizers, caches, tuners; learned heuristics in core systems. |
| `verification-and-checkers` | Formal verification, invariants, fuzzing, semantic checkers, deterministic replay. |
| `gpu-network-and-collectives` | GPU comm, NCCL/HCCL, in-network aggregation, optical/RDMA fabrics, congestion control. |
| `agentic-data-workflows` | LLM agents calling tools and mutating data; replay, rollback, provenance of model actions. |
| `ebpf-and-kernel-bypass` | XDP, eBPF schedulers (sched_ext), user-space networking (DPDK/io_uring), VFS bypass. |
| `confidential-computing-tees` | Intel TDX, AMD SEV-SNP, ARM CCA, GPU TEEs, side-channel mitigation, attestation. |
| `serverless-and-scale-to-zero` | Cold-start mitigation, snapshotting (CRIU/firecracker), FaaS isolation, stateful serverless. |
| `sustainable-and-power-aware` | Power capping, carbon-aware scheduling, stranded-power utilization, energy-proportional storage. |

Anything that does not fit takes `other`, with a freeform `subtopic` note. **Do not use `general-systems`** — it concealed tribute talks and unrelated papers in earlier runs.

A tag without a quoted justification in `topic_tag_evidence` is invalid and will be rejected by the validator.

## 6. Read Priority and Awards

The script populates `priority_seed`. Reader agents may upgrade/downgrade; they record the change with a one-line reason.

- `must-read`: paper has any `award` ∈ {best-paper, best-paper-runner-up, distinguished-artifact}; OR is from an industry track at scale (FAANG, Alibaba, ByteDance, Tencent, Meituan, Microsoft, Google, Anthropic, NVIDIA, etc.) and abstract mentions deployment; OR appears in the first session of its track.
- `should-read`: abstract contains "in production", "deployed", "we observed", "at scale", "{N} GPUs/nodes"; OR clusters with ≥3 other papers on the same `topic_tags_keyword_seed` within the same year.
- `skim`: everything else.

Reader agents spend their 25-paper budget on `must-read` first.

## 7. Principles For Identifying Promising Ideas

Use these principles as the main research lens. Every spark and detailed idea must record a `Lens applied:` field naming **one or two** of these principles. Picking the right lens forces thinking; an idea with no lens is not yet an idea.

Promising systems ideas usually have three properties at once: a **real pressure** visible in recent papers, a **missing structural primitive** rather than a local optimization, and a **cheap falsification path** before a full system is built. Treat popularity as weak evidence; a crowded topic is often a novelty trap unless the idea names a gap the crowded papers leave unsolved.

**Idea atomicity rule.** A ranked research idea must fit in one plain sentence that names the artifact to build, the exact workload, the mechanism to change, the baseline to beat, and the falsifying observation. If the sentence still sounds like a field, trend, agenda, or umbrella system after removing adjectives, it is not an idea; keep drilling until it is a project a small team could start this week.

- **L1 — Mismatch**: workload changed but the system did not; hardware changed but the software stack did not; scale changed but assumptions did not.
- **L2 — Unnamed pain**: phrases like "in practice", "we assume", "not considered", "future work", "hard to deploy" hide research problems. Quote the sentence.
- **L3 — Structural over incremental**: missing abstractions, lifecycle semantics, consistency models, scheduler contracts, or resource boundaries are stronger than isolated speedups.
- **L4 — Cross-venue convergence**: if SIGMOD and FAST, or OSDI and SIGCOMM, touch the same pressure from different angles, the topic is likely important.
- **L5 — What current papers ignore**: multi-tenancy, failure recovery, freshness, observability, cost, correctness, durability, security boundaries, deployment complexity.
- **L6 — Bottleneck-caused-by-success**: when a system pattern becomes successful, it creates new bottlenecks — KV cache, memory bandwidth, freshness, lineage, checkpoint traffic.
- **L7 — Fragmented solutions**: if storage, networking, scheduling, and database papers each solve one piece independently, a unifying abstraction may be the idea.
- **L8 — Operational reality**: skew, failures, noisy neighbors, tail latency, upgrades, observability, cost.
- **L9 — Topic ≠ idea**: "vector databases" is a topic; "freshness-aware derived-data contracts for embeddings under bounded recomputation cost" is an idea.
- **L10 — Falsifiable**: identify the workload, the baseline that breaks, the metric/property that should improve, and what observation would weaken the idea.
- **L11 — User-space duct tape**: look for patterns where application developers repeatedly build complex workarounds in user space (app-level caches, custom retry loops, manual sharding, hand-rolled lock services, ad-hoc rate limiters) because the underlying OS, network, runtime, or database lacks the right structural primitive. The duct tape *is* the missing abstraction.

### 7a. Promise filter (evidence -> ranked idea)

Before promoting a spark into `thinking/research_ideas.md`, force it through this filter. If any item fails, keep it in `sparking/` and mark the limiting status.

1. **Pressure is named.** At least one paper quote says what is hard, assumed away, expensive, unstable, or not handled. The quote is evidence; your inference from it is separate.
2. **Gap is structural.** The missing thing is a contract, invariant, resource boundary, control plane, data model, lifecycle semantic, or observability primitive. A kernel, index, scheduler, or cache tweak without such a primitive stays a spark.
3. **Closest prior art leaves a wedge.** The idea differs from 2-5 nearest papers by more than workload substitution. If the difference is only "bigger", "with LLMs", or "using GPUs", kill it or sharpen it.
4. **Why-now is credible.** Name the last-two-years change that made the problem newly painful: workload composition, model context length, memory hierarchy, accelerator/network topology, deployment practice, regulation/security boundary, or cost curve.
5. **A small team can falsify the core claim.** Prefer ideas where a measurement study, replay harness, open workload, simulator, or prototype on commodity hardware can kill the claim in days to weeks. If validation needs confidential traces or scarce hardware, mark `access-blocked` unless there is a substitute experiment.
6. **Impact survives success.** Ask what happens if the proposed system works. Strong ideas change how a class of systems is built or operated; weak ideas only win a benchmark until the next implementation improves.

Before scoring, write a `One-sentence idea:` line. It must have the shape "Build/measure/modify {artifact} for {workload} by {mechanism}, beating {baseline} on {metric}; kill it if {observation}." Do not keep the template wording, but make those six slots obvious.

Use this scoring rubric only after the filter:

- `novelty`: 5 means closest prior art leaves the core mechanism open; 3 means the wedge is mostly in workload/assumption; 1 means likely rediscovery.
- `tractability`: 5 means the key claim is testable with open code/data or commodity hardware; 3 means simulation or partial traces; 1 means proprietary access or unavailable hardware.
- `impact`: 5 means correctness, durability, cost, isolation, or tail latency for real deployments; 3 means material performance on a known workload; 1 means narrow microbenchmark.
- `evidence`: 5 means cross-venue quotes plus a disconfirming paper; 3 means one strong quote plus adjacent corroboration; 1 means plausible but mostly speculative.

### Worked examples

**Good idea (kept):**
> *Crash-consistent vector-index refresh under mixed OLTP/RAG updates*
>
> - Lens applied: L1 (workload mismatch), L6 (bottleneck caused by RAG success).
> - Observed mismatch: Quake (OSDI '25) §2 says "we assume the index is rebuilt periodically", but Mooncake (OSDI '26) §6 reports source documents being updated continuously; no paper currently models crash recovery of the derived vector index.
> - Baseline that breaks: vLLM + FAISS + Postgres under 1% per-minute row churn at 32k context — current systems either rebuild from scratch (kills throughput) or skip refresh (kills recall).
> - Disconfirming evidence: if OdinANN's "direct insert" (FAST '26) scales to mixed OLTP traffic, the structural problem dissolves into a perf problem.

**Rejected idea (taught the skill what NOT to propose):**
> *"A unified abstraction for AI workloads"*
>
> - Killed by critic: no Lens applied — "unified abstraction" is the answer, not the question. No paper quote names the missing abstraction concretely; no falsifiable claim. This is the shape an idea takes when the agent skipped Step 4 reader output and synthesized from keyword tags.

Do **not** write Mad-Libs-style templates ("Because {workload} changed, existing systems that assume {old assumption} now suffer from {pain}...") as your *output*. They generate grammatically uniform but content-empty ideas. Imitate the worked example's specificity instead.

### 7b. Generation moves (signal -> idea)

The §7 lenses tell you how to read for signal. These moves tell you how to *combine* signal into ideas. Run them explicitly during synthesis; do not just restate a topic as an idea.

1. **Triangulation.** Pick a *pain* from venue A, a *capability or abstraction* from venue B, and a *workload / hardware shift*. Force them into one sentence: "Because {shift}, {pain} now bites systems that {assumption}; the {abstraction from B} could be re-purposed to {control the missing thing}." Most non-obvious ideas come from crossing venues, not from staying inside one.
2. **Second-order — success creates bottlenecks.** Take a pattern that *succeeded* in the last two years and ask what its own success now strains. KV-cache reuse → cache lifecycle and placement across HBM/DRAM/SSD/network; disaggregated memory → failure and consistency semantics; learned components → silent regressions and retraining budgets; checkpointing at scale → checkpoint traffic and storage. The *next* bottleneck is often a better bet than the current hot topic.
3. **Cross-layer.** The richest gaps live *between* layers — storage × scheduling, network × database, OS × accelerator, compiler × runtime — where each venue solves only its own slice and no one owns the seam. A unifying contract across the seam is frequently the idea.
4. **Fragmentation → unification.** If storage, networking, scheduling, and database papers each solve one piece of the same problem independently, the missing piece is often a single shared abstraction, not a fifth point solution.
5. **Assumption inversion.** Take an assumption every paper in a cluster shares ("the index fits in memory", "writes are rare", "the model is static", "the network is reliable") and ask what breaks, and what would need to exist, if it were false under a now-realistic workload.

### 7c. Anti-patterns (kill on sight)

If a draft spark or idea matches one of these, the critic in Step 6 must either fix it or drop it. **Do not put it in the ranked list.**

- **"X but for LLMs / for AI"** with no specific named mismatch. The AI angle is not an idea by itself.
- **"Add ML to the {scheduler/cache/optimizer}"** without naming the concrete regression or failure the current heuristic causes, *and* without a story for handling the ML component's own regressions.
- **Pure speedup, no structure.** "Make X 2× faster" with no new abstraction, contract, or semantics is engineering, not a research direction. (L3 covers this from the reading side; this is the writing side.)
- **Topic restated as idea.** "Vector databases", "serverless", "disaggregation", "RAG" are topics. An idea names the workload, the stale assumption, and the missing mechanism.
- **No "why now".** If the idea was equally doable and equally relevant five years ago, it is probably already solved or not yet ripe — investigate before listing it.
- **Untestable by the intended researcher.** If validating the core claim needs proprietary workloads or hardware the user cannot access, the idea moves to `sparking/` with `Status: access-blocked`. Do not pretend it is cheap.

### 7d. Falsifiability diagnostic (use during synthesis, never as output)

When a spark is fuzzy, run it through this template *as a diagnostic* to see if it can be made falsifiable:

```
Because {workload / hardware / operational trend} changed,
existing systems that assume {old assumption} now suffer from {pain}.
A new system should expose / control {missing abstraction},
so that {important metric or property} improves under {realistic workload}.
The cheapest way to find out I'm wrong is {measurement or prototype} —
if {observation}, the idea is dead.
```

If you cannot fill the last two lines, the idea is not yet falsifiable enough to rank — send it to `sparking/` with `Status: not-yet-falsifiable` and note what is missing. **Never paste a filled-in template as the actual idea body** — use the schema in `references/final_deliverables.md` instead. The template is a thinking tool, not a deliverable.

## 8. Sub-Agent Fan-Out Contract

| Agent type | Inputs | Output | Hard rules |
|---|---|---|---|
| Reader | `thinking/catalog/{venue}-{year}.md`, PDFs (must-read first) | `thinking/venue_reads/{venue}-{year}.md` | ≤25 papers; output must include 3 quoted unnamed-pain sentences drawn **strictly from Introduction, Evaluation, or Limitations/Future Work sections** (never the Abstract). |
| Synthesis | Union of `thinking/venue_reads/*.md` only | Scratch text merged into `topic_by_year.md` and `sparking/*.md` | **Forbidden** from reading raw papers or full catalog. Must reconcile cross-venue disagreement by quoting both sides. |
| Critic | Draft `sparking/*.md` + `thinking/research_ideas.md` | Annotated drafts with `Status:` and `Critic notes:` | Must attempt to kill every spark and idea using one of: a `catalog/*` digest line, an absent workload, a charitable reading of an existing system, or a violated physical/theoretical bound (CAP, PACELC, speed of light, PCIe/CXL/HBM ceilings). Killed items stay in the file. |

Run readers in parallel. Run synthesis after readers. Run critic last.

## 9. Sparks and Ideas — Required Fields

Both schemas live in [the final deliverables reference](references/final_deliverables.md). Summary of new required fields versus prior versions:

- **Sparks** add: `Lens applied`, `Observed mismatch` (verbatim quote ≤2 sentences from one paper, with title and section), `Cross-paper corroboration` (a quote from a *different* paper hitting the same pain — if missing, `Status: solo-signal`), `Disconfirming evidence` (a paper or sentence that would weaken the spark — if missing, `Status: not-yet-falsifiable`).
- **Detailed ideas** add: `Lens applied`, **per-paper role tags** (`motivating | corroborating | solves-one-piece | competing-approach | disconfirming`), `Baseline that breaks` (a specific stack + workload, not "trace-driven evaluation"), `What this idea is NOT` (defends against scope creep), `Closest prior art` (2–5 papers with a one-line *how this differs / what they leave open* note — populated by the Step 6a novelty check), `Why it might be a dead end` (honest failure mode or access/data barrier — protects the user against starting work that is gated by resources they don't have), `Score` (novelty / tractability / impact / evidence, each 1–5), `Critic notes`.

Flat lists of paper titles without role tags are rejected.

## 10. Pre-flight Quality Gates

`scripts/validate_outputs.py` enforces these. Agents must run it before declaring the skill complete.

### A. No TODO scaffolding

No file under `thinking/` or `sparking/` may contain (outside code fences) any of: `TODO`, `TBD`, `refine after`, `infer from`, `look for`, `Title TBA`, `to be filled`, `placeholder`.

### B. Coverage-gated trend

`thinking/topic_trend.md` must reference `coverage_ledger.md` at least once. Every row must include a `Completeness:` line. Rows with `direction:` set to `rising|fading|stable|emerging` must have both compared years at `completeness ≥ 0.9` *in the same venue set*; otherwise use `direction: unknown — partial coverage`.

### C. Evidence chain

Every `Observed mismatch` quote in `sparking/*.md` must appear (case-insensitive, whitespace-normalized) verbatim in at least one paper's `abstract` or `introduction_excerpt` field in `papers/metadata.jsonl`. Quotes the validator cannot find are flagged as fabricated.

### D. Spark diversity

No two `sparking/*.md` files may share more than 50% of their cited papers (set-overlap on paper titles). High overlap is a signal that the synthesis agent collapsed distinct sparks.

### E. Tag justification

Every paper with `topic_tags_curated` non-empty must have a `topic_tag_evidence` entry for each curated tag, and that evidence quote must appear in the paper's abstract.

### F. Lens applied

Every spark and detailed idea must contain a `Lens applied:` line naming one or two of L1–L11.

### G. No forbidden tag

`general-systems` may not appear anywhere in `topic_tags_curated`.

### H. Awards parsed

For every USENIX paper whose `source_url` page contains "Best Paper" or "Distinguished Artifact", the metadata row must have a non-empty `awards` field.

### I. Spark/idea grammar

Detailed ideas in `research_ideas.md` must contain `Lens applied`, `Baseline that breaks`, `Closest prior art`, and at least three papers with role tags. The `Closest prior art` line is populated by the Step 6a novelty check; without it, the idea cannot enter the ranked output.

## 11. Quality Bar

- Use official sources wherever possible and record source URLs.
- Do not silently skip a venue-year; either analyze it or record it in `coverage_ledger.md`.
- Do not create fake paper rows for unavailable venue-years.
- Research ideas must be specific enough to be recognizable systems projects; they do not need full designs.
- A strong idea names the changed workload, the stale assumption, the missing abstraction, the baseline that breaks, and 3–8 related papers with role tags.
- Ambiguous sparks are welcome when grounded in observed paper quotes. Solo signals are recorded as `solo-signal`, not deleted.
- Separate evidence from inference: name papers/quotes for evidence; label speculative extrapolation as `speculative`.
- The skill is not complete until `scripts/validate_outputs.py` exits zero.
