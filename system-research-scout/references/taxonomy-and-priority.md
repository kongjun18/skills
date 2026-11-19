# Topic Taxonomy and Read Priority

Read this when curating `topic_tags_curated` (Step 4), assigning or overriding `priority_seed`, or choosing synthesis clusters (Step 5).

## Curated topic tags

Use these 16 leaves for `topic_tags_curated`. Apply a tag by reading the abstract and introduction, not by matching keywords. At most 3 tags per paper. Each tag needs a one-sentence quote from the paper's abstract in `topic_tag_evidence` (validator gate E).

| Tag | Apply if the paper's primary contribution targets |
|---|---|
| `llm-serving-engine` | Inference scheduler, attention kernel, request batching, decoding parallelism. |
| `llm-training-substrate` | Distributed training, collective communication, parallelism strategies, fault tolerance for training. |
| `kv-cache-mgmt` | Lifecycle, placement, sharing, eviction, compression of KV state across tiers. |
| `vector-retrieval` | ANN index structure, recall/latency tradeoffs, hybrid retrieval, vector storage. |
| `rag-data-plane` | Pipelines, contracts, and freshness between source data, embeddings, retrievers, and LLMs. |
| `cxl-disagg-memory` | CXL pods, remote memory pools, tiered memory, coherence under disaggregation. |
| `cloud-object-storage` | Object stores at scale, geo-distribution, erasure coding, archival/tape tiers. |
| `local-flash-storage` | SSD/NVM file systems, request-to-I/O transformations, write-ahead logs, recovery. |
| `learned-index-or-optimizer` | ML-driven indexes, query optimizers, caches, tuners; learned heuristics in core systems. |
| `verification-and-checkers` | Formal verification, invariants, fuzzing, semantic checkers, deterministic replay. |
| `gpu-network-and-collectives` | GPU communication, collectives, in-network aggregation, optical/RDMA fabrics, congestion control. |
| `agentic-data-workflows` | LLM agents calling tools and mutating data; replay, rollback, provenance of model actions. |
| `ebpf-and-kernel-bypass` | XDP, eBPF schedulers, user-space networking and I/O, VFS bypass. |
| `confidential-computing-tees` | CPU and GPU TEEs, side-channel mitigation, attestation. |
| `serverless-and-scale-to-zero` | Cold-start mitigation, snapshotting, FaaS isolation, stateful serverless. |
| `sustainable-and-power-aware` | Power capping, carbon-aware scheduling, stranded power, energy-proportional storage. |

Anything that does not fit takes `other` with a free-form `subtopic` note. Never use `general-systems` (gate G); it hides unrelated papers.

The taxonomy reflects the current proceedings. When a run finds a recurring topic with no leaf, add the leaf here first and say so in the run's coverage notes; do not invent tags per run.

`topic_tags_keyword_seed` (written by the survey script) is a scaffold biased by title vocabulary. Never derive trend or taste claims from it.

## Read priority

The survey script fills `priority_seed`; reader agents may upgrade or downgrade a paper and record a one-line reason.

- `must-read`: any award (best paper, runner-up, distinguished artifact); or an industry paper at scale whose abstract mentions deployment; or the first session of its track.
- `should-read`: the abstract says "in production", "deployed", "we observed", "at scale", or "{N} GPUs/nodes"; or the paper clusters with at least 3 others on the same keyword seed in the same year.
- `skim`: everything else.

Readers spend their 25-paper budget on `must-read` first.

## Synthesis clusters

Choose clusters from what reader agents surfaced, never from a fixed list. A good cluster names a pressure across venues, not a topic, for example "lifecycle of derived data (embeddings, features) under source updates" rather than "vector databases". Do not create a cluster that no venue read supports.
