# Concept–Claim Logic Flow Workflow

Use this workflow as an internal representation for presentation generation,
review, and revision. It is a diagnostic model, not a manuscript template.
Most papers contain local reasoning chains, but the whole argument may also
branch, converge on shared evidence, compare alternatives, qualify claims, or
hand responsibility from one section to another.

## 1. Inventory the reasoning nodes

Record only items that readers must carry, distinguish, or use later:

- concepts and operations;
- observations and problems;
- claims and requirements;
- evidence and measured results;
- design decisions and mechanisms; and
- limitations, conditions, or scope boundaries.

Do not create a node for every noun or sentence. Give each node a stable
description and a locator in the source text. Mark whether the node is
introduced before its first dependent use and whether its scope is clear.

## 2. Inventory the supported edges

For each adjacent or non-adjacent dependency, record the relation that the
reader must understand. Useful relation types include `introduces`, `requires`,
`supports`, `motivates`, `explains`, `contrasts`, `specializes`, `limits`, and
`hands off`. Mark every edge as supported, ambiguous, missing, or contradicted
by the supplied text or evidence.

For a comparison or tension, record the shared question and the outcome/path
fields used by each alternative. For a design tradeoff, identify the design
choice as the source of its benefit and cost edges, and record the workload or
configuration that conditions the observed net effect. This prevents a result
such as fast recovery from being treated as the cause of a query-path cost.

Do not infer a causal or logical edge from adjacency, a connective word, or an
author's likely intention. If a paragraph says that a result motivates a
design, verify that the result actually establishes the need for that design.

## 3. Diagnose flow defects

Look for an undefined node, a first-use dependency, a dangling claim, a broken
edge, the wrong endpoint, lost scope, a redundant node, a premature node, or an
overloaded paragraph. A missing transition is usually one of these concrete
defects, not merely the absence of `therefore` or `however`.

Repair a broken edge by supplying the smallest supported premise, naming the
shared object or result, stating the relevant relation or condition, or moving
the unit after its prerequisites. If the source does not support the edge,
mark `Needs context`; do not repair it with a plausible but invented fact.

## 4. Search the reader's path

Compare candidate structures by asking whether each node is reachable after
its prerequisites, whether claims stay near the evidence that supports them,
whether each section answers its own question, and whether each local handoff
names the object, result, or pressure carried forward. Prefer fewer backtracks,
less repetition, and the shortest complete argument. Do not force a linear
order when the supported graph has a branch, convergence, comparison, or
qualification that is clearer in another arrangement.

Keep section contracts in force: Motivation must remain valid without Design
details; Design must map decisions to prior requirements; Evaluation must test
the claimed benefits, costs, and scope under the stated workload and
configuration.

## 5. Render and round-trip verify

Write prose from the selected graph, with one main relation per sentence and
one local subgraph per paragraph. Add a transition only when it makes a
supported relation or endpoint easier to recover; do not add generic bridge
sentences that introduce no node or edge.

When rendering a comparison, state the reader-visible outcome on a common
comparison frame before or together with the mechanism. When rendering a
tradeoff, keep the design choice as the causal source of both branches. When a
paragraph introduces a design to address a prior pressure, carry that pressure
and purpose into the opening sentence.

After revision, reconstruct the graph from the final prose without consulting
the writer's plan. Report nodes that became undefined or premature, edges that
became missing or ambiguous, and claims whose scope or strength changed. This
round trip is required before an automatic round can be considered complete.
