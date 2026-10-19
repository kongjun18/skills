# Semantic Object and Logic Graph

Use this workflow before sentence rendering whenever the agent is discussing a
story, expanding a section direction, synthesizing an outline, or reviewing a
structured outline. It is the canonical intermediate representation between
the story and the prose. The agent should reason about objects, claims,
evidence, purposes, and relations first; prose is generated only after this
graph and its sentence slots are aligned.
The graph is the primary writing object: prose materializes its nodes and edges
for the reader. Do not use prose generation to discover a missing claim,
purpose, object, or transition.

## 1. Build typed semantic nodes

Create nodes for the objects and reasoning units that the reader must follow.
Typical node types are:

```text
concept | purpose | question | requirement | challenge | decision | mechanism
operation | claim | evidence | result | explanation | comparison | condition
cost | limitation | net_effect | implication | handoff | figure | metric
```

For every node, record:

```text
node_id
type
object                 # the object, metric, system, or relation discussed
semantic_payload       # a short meaning-bearing phrase, not draft prose
from                   # source observation, prior node, or section
relation_to_previous
supports_or_answers    # claim, purpose, question, or requirement served
evidence               # figure, table, citation, measurement, or reasoning basis
scope                  # workload, configuration, condition, or abstraction layer
provided_to            # later node, paragraph, subsection, or section
canonical_terms        # term IDs, not newly invented wording
status                 # supported | author-choice | unresolved
```

`semantic_payload` should name the meaning compactly, such as `storage-access
overhead`, `request throughput`, or `additional prefix retrieval during
insertion`. It should not be a fluent sentence that hides several claims.
Split independent claims, effects, and costs into separate nodes.

## 2. Make purpose and causal relations explicit

Every Design mechanism, operation, layout, or update node should connect to a
supported requirement, challenge, or purpose. Every Evaluation metric, result,
breakdown, or component explanation should connect to the question it answers.
Use the relation that the evidence supports:

```text
requirement/question → purpose → decision or metric → mechanism/result
→ effect or interpretation → cost/condition/net effect → handoff
```

This is a relation inventory, not a mandatory prose order. A different
section pattern may use `contrast`, `explains`, `qualifies`, or `measures`, but
the graph must make the reason for each node recoverable. A mechanism without a
purpose edge, or a result without a question/metric edge, is incomplete.

For example, a Design graph may contain:

```text
D1 [requirement] amortize storage-access overhead
D2 [purpose] reduce accesses needed for related blocks
D3 [mechanism] aggregate blocks into a segment
D4 [effect] one access serves multiple blocks
D5 [cost] update or placement overhead introduced by aggregation
```

An Evaluation graph may contain:

```text
E1 [question] whether the design improves request throughput
E2 [metric] request throughput as completed requests per second
E3 [result] proposed system has the highest throughput on the evaluated workloads
E4 [breakdown purpose] identify the source of the throughput difference
E5 [benefit] fewer storage accesses during insertion
E6 [cost] prefix retrieval added to insertion
E7 [net_effect] benefit exceeds cost under the evaluated workload/configuration
```

Do not add a purpose or causal edge merely because it sounds plausible. Mark
the edge `unresolved` when the supplied material does not support it.

## 3. Audit lexical items as semantic objects

Before the graph is accepted, extract the technical lexical items that will
appear in the outline or prose:

```text
lexical_id
surface_form
kind: noun | noun_phrase | adjective | adverb | verb | relation
concept_id
canonical_form
semantic_contract
first_use
abstraction_layer
source_or_author_decision
scope
allowed_variants
status: active | candidate | forbidden | unresolved
```

Audit technical adjectives and adverbs as claims, not decoration. A modifier
such as `efficient`, `fast`, `compact`, `direct`, `lightweight`, or `scalable`
needs a property, comparison axis, scope, and support. If these are absent,
remove the modifier or replace it with a direct supported description. Do not
invent a noun, adjective, synonym, operation verb, or relation verb during
outline generation. A term is available only when it comes from the paper's
terminology ledger, supplied material, or an explicit author decision.

Generic English words need not enter the ledger unless they carry technical,
comparative, or state-changing meaning. The audit is intended to prevent
semantic drift, not to forbid ordinary language.

## 4. Derive sentence slots from the graph

Only after nodes and edges are checked, group them into paragraphs and derive
sentence slots. Each slot records:

```text
sentence_slot
node_ids_rendered
role
from
needs
link_or_transition
opening_or_handoff
```

One slot normally renders one main node. Adjacent nodes may share a sentence
only when their relation is simple and both mappings remain visible. The
sentence slot is a rendering contract, not a draft sentence.

## 5. Graph gates before prose

The graph is ready for author alignment only when:

- every claim has evidence or an explicit reasoning basis;
- every mechanism, operation, metric, and result has a supported purpose or
  question edge;
- every cost and condition qualifies the correct benefit or claim;
- every node has a recoverable object and abstraction layer;
- every technical lexical item has provenance, canonical form, and scope;
- no active node depends on an unintroduced or unresolved term;
- every paragraph has an incoming endpoint, local responsibility, and outgoing
  handoff; and
- sentence slots can render the graph without adding nodes.

If a check fails, return a graph finding or `Needs context`; do not repair the
problem by writing a smoother sentence.

## 6. Author-facing projection

The human sync view shows the paragraph navigation followed by every sentence
slot or logical node. It should expose the node type, object, short semantic
payload, relation, evidence, purpose, and handoff. It may hide internal IDs and
confidence fields, but it must not replace the graph with paragraph summaries.

After the author aligns this projection, compile paragraph materialization
contracts from the graph. Each contract names the paragraph responsibility,
incoming and outgoing endpoints, ordered node IDs, evidence, scope, required
terms, and the next paragraph's required input. Write paragraphs in that order
and verify each contract before moving to the next. If prose requires a new
node or edge, return to graph or outline alignment instead of adding it during
rendering.
