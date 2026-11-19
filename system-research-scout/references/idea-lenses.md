# Idea Lenses, Promise Filter, and Anti-Patterns

Read this before synthesis (Step 5), before the critic pass (Step 6), and whenever you draft or promote a spark or idea (Step 7). Every spark and idea records a `Lens applied:` line naming one or two lenses (gate F).

Promising systems ideas usually combine three things: a **real pressure** visible in recent papers, a **missing structural primitive** rather than a local optimization, and a **cheap falsification path** before a full system is built. Popularity is weak evidence; a crowded topic is a novelty trap unless the idea names a gap the crowded papers leave open.

**Idea atomicity.** A ranked idea fits in one plain sentence naming the artifact to build, the workload, the mechanism to change, the baseline to beat, and the falsifying observation. If the sentence still reads like a field, trend, or agenda after removing adjectives, keep drilling.

## Lenses (reading for signal)

- **L1 Mismatch**: the workload, hardware, or scale changed but the system or its assumptions did not.
- **L2 Unnamed pain**: "in practice", "we assume", "not considered", "future work", "hard to deploy". Quote the sentence.
- **L3 Structural over incremental**: missing abstractions, lifecycle semantics, consistency models, scheduler contracts, or resource boundaries beat isolated speedups.
- **L4 Cross-venue convergence**: different communities touch the same pressure from different angles.
- **L5 What papers ignore**: multi-tenancy, recovery, freshness, observability, cost, correctness, durability, security boundaries, deployment complexity.
- **L6 Bottleneck caused by success**: a successful pattern creates its own next bottleneck.
- **L7 Fragmented solutions**: several communities each solve one piece; a shared abstraction may be the idea.
- **L8 Operational reality**: skew, failures, noisy neighbors, tail latency, upgrades, cost.
- **L9 Topic is not an idea**: "vector databases" is a topic; "freshness-aware contracts for derived embeddings under bounded recomputation cost" is an idea.
- **L10 Falsifiable**: name the workload, the baseline that breaks, the metric that should improve, and the observation that would weaken the idea.
- **L11 User-space duct tape**: applications keep building workarounds (app-level caches, retry loops, manual sharding, hand-rolled lock services) because a lower layer lacks a primitive. The duct tape is the missing abstraction.

## Generation moves (combining signal into ideas)

1. **Triangulation.** A pain from venue A, a capability from venue B, and a workload or hardware shift, forced into one sentence.
2. **Second order.** Take a pattern that succeeded in the last two years and ask what its success now strains.
3. **Cross-layer.** Look at the seam between layers (storage and scheduling, network and database, OS and accelerator) that no single community owns.
4. **Fragmentation to unification.** Several point solutions to one problem suggest a missing shared abstraction.
5. **Assumption inversion.** Take an assumption every paper in a cluster shares and ask what breaks if it is false under a realistic workload.

## Promise filter (spark to ranked idea)

Promote a spark into `thinking/research_ideas.md` only if all six hold; otherwise keep it in `sparking/` with the limiting status.

1. **Pressure is named.** At least one paper quote says what is hard, assumed away, expensive, or unhandled. The quote is evidence; your inference is separate.
2. **Gap is structural.** The missing thing is a contract, invariant, resource boundary, control plane, data model, lifecycle semantic, or observability primitive.
3. **Closest prior art leaves a wedge.** The idea differs from its 2-5 nearest papers by more than workload substitution ("bigger", "with LLMs", "on GPUs" is not a wedge).
4. **Why-now is credible.** Name the recent change that made the problem newly painful.
5. **A small team can falsify the core claim** in days to weeks with a measurement study, replay harness, open workload, simulator, or commodity prototype. Otherwise mark `access-blocked` unless a substitute experiment exists.
6. **Impact survives success.** If it works, it changes how a class of systems is built or operated, not just one benchmark.

Write the `One-sentence idea:` line with six obvious slots: build/measure/modify {artifact} for {workload} by {mechanism}, beating {baseline} on {metric}; kill it if {observation}. Do not keep the template wording.

Score only after the filter (each 1-5):

- `novelty`: 5 = closest prior art leaves the core mechanism open; 3 = wedge is mostly workload or assumption; 1 = likely rediscovery.
- `tractability`: 5 = testable with open code/data or commodity hardware; 3 = simulation or partial traces; 1 = proprietary access or unavailable hardware.
- `impact`: 5 = correctness, durability, cost, isolation, or tail latency in real deployments; 3 = material performance on a known workload; 1 = narrow microbenchmark.
- `evidence`: 5 = cross-venue quotes plus a disconfirming paper; 3 = one strong quote plus adjacent corroboration; 1 = mostly speculative.

## Anti-patterns (the critic kills or fixes these)

- **"X but for LLMs/AI"** with no named mismatch.
- **"Add ML to the scheduler/cache/optimizer"** without naming the regression the current heuristic causes and how the ML component's own regressions are handled.
- **Pure speedup, no structure.** "Make X 2x faster" with no new abstraction, contract, or semantics.
- **Topic restated as idea**, or **an answer without a question** ("a unified abstraction for AI workloads" with no quoted missing abstraction and no falsifiable claim).
- **No why-now.** Equally doable five years ago means probably solved or not yet ripe.
- **Untestable by the intended researcher.** Move to `sparking/` with `Status: access-blocked`.

## Falsifiability diagnostic (thinking tool, never output)

When a spark is fuzzy, fill this privately:

```
Because {trend} changed, systems that assume {old assumption} now suffer from {pain}.
A new system should expose or control {missing abstraction},
so that {metric or property} improves under {realistic workload}.
The cheapest way to find out I'm wrong is {measurement or prototype};
if {observation}, the idea is dead.
```

If you cannot fill the last two lines, file the spark with `Status: not-yet-falsifiable` and note what is missing. Never paste a filled template as the idea body; use the schema in [final_deliverables.md](final_deliverables.md).

## Example of the required specificity

> *Crash-consistent vector-index refresh under mixed transactional and retrieval updates*
>
> - Lens applied: L1 (workload mismatch), L6 (bottleneck caused by retrieval success).
> - Observed mismatch: Paper A, §2: "we assume the index is rebuilt periodically"; Paper B, §6, reports source rows updated continuously; no paper in the catalog models crash recovery of the derived index.
> - Baseline that breaks: an LLM server plus an ANN library plus a relational store under 1% per-minute row churn: rebuilding kills throughput, skipping refresh kills recall.
> - Disconfirming evidence: if Paper C's direct-insert path scales to mixed transactional traffic, the structural problem reduces to a performance problem.
