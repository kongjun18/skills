# Sentence-Level Realization Contract

Use this workflow after story alignment and before any prose writer is
dispatched. It closes the gap between a correct story and prose that merely
sounds related to that story. A paragraph summary is not an executable writing
input. The writer receives ordered, typed sentence slots whose propositions,
relations, evidence, scope, and vocabulary are already decided.

The contract has one purpose: preserve the author's claim flow while giving
the writer enough structure to express it in clear English. It does not ask
the writer to discover the story, choose a presentation order, or fill in
missing technical meaning.

The author does not need to supply every slot. A paragraph-level chain and its
internal major relations are sufficient input for the discussion agent. The
discussion agent expands them into slots, runs the dry-run checks below, and
returns a human sync view. The author may revise any paragraph, slot, relation,
term, or scope before the coordinator freezes the execution contract.

## 0. Complete a coarse outline before prose

When the input contains only section or paragraph responsibilities and a few
internal steps, use this planning route:

```text
coarse story/paragraph chain
→ claim and object graph
→ paragraph interfaces
→ sentence-slot expansion
→ independent outline review
→ human sync view and author discussion
→ frozen execution contract
```

The expansion pass may choose ordinary connective wording and fill in a
supported intermediate explanation, but it may not invent a fact, mechanism,
term, causal edge, evidence item, or scope. If more than one supported
sentence-level completion remains, present the alternatives and the decision
needed. In an authorized automatic run, select the simpler supported
completion and record the choice. In a manual run, stop at
`Awaiting outline alignment` until the author accepts or edits it.

Run this completion and its independent outline review before dispatching a
prose writer. It is an outline-generation task, not a prose-refinement round.

## 1. Keep four linked artifacts

Keep these artifacts distinct but linked by stable IDs:

1. **Story and claim graph:** what the paper establishes and why each claim
   follows from the previous one.
2. **Paragraph interface map:** what each paragraph receives, owns, and passes
   to the next paragraph.
3. **Sentence realization contract:** the ordered propositions that each
   paragraph must render.
4. **Prose and trace:** the English text plus a mapping from each output
   sentence to the contract slots it realizes.

The writer must never receive only the first artifact or a paragraph synopsis.
The coordinator may keep the full graph, but the human sync view and the
writer packet must expose the complete sentence realization contract.

## 2. Compile a real sentence slot, not a topic label

Each slot represents one proposition or one explicit relation. A slot is not
“explain the result,” “discuss the baseline,” or “introduce the index.” Those
are topics. Rewrite them into a proposition that specifies what the reader
should know after the sentence.

Use this schema for every slot:

```text
slot_id: S1
paragraph_id: P1
role: purpose | setting | claim | evidence | explanation | contrast |
      condition | cost | net_effect | evidence_boundary | implication |
      limitation | transition
proposition: <one subject–predicate–object or condition–consequence statement>
reader_question: <the question this sentence answers>
from: <the preceding slot or paragraph endpoint>
relation: <supports | explains | qualifies | contrasts | motivates | ...>
evidence: <figure, table, citation, measurement, or reasoning basis>
scope: <workload, configuration, comparison, or logical boundary>
canonical_terms: <only terms permitted in this slot>
introduces: <concepts first made available here>
provides: <claim or object needed by a later slot>
opening_requirement: <only for the first sentence of a paragraph>
allowed_merge: none | [adjacent slot IDs]
forbidden: <objects, mechanisms, modifiers, or relations that belong elsewhere>
```

`proposition` must be concrete enough to distinguish, for example,
“recovery is slow because the index state must be rebuilt” from “explain
recovery.” `relation` must identify the edge, not merely say that the sentence
comes next. `evidence` and `scope` must say what supports the proposition and
where it holds. If a field is unknown, mark `Needs context`; do not let the
writer infer it from neighboring prose.

For example, these are different contract qualities:

```text
weak:   S2 [Result] report the throughput result
usable: S2 [Result] The proposed index achieves the highest request
        throughput on the evaluated workloads.
        from: S1  relation: answers the metric purpose
        evidence: Figure <id>  scope: evaluated workloads
```

The usable row is still a planning statement rather than manuscript prose, but
it fixes the proposition, comparison scope, and evidence that the writer must
materialize. Do not let a writer turn a weak row into a claim by guessing the
missing comparison or scope.

The default is one slot to one output sentence in Round 1. Combining adjacent
slots is allowed only when `allowed_merge` explicitly permits it and the
writer returns both slot IDs in the trace. A sentence carrying independent
relations is split. Do not use one overloaded sentence as a shortcut for a
missing slot.

## 3. Compile slots in reader order

For each paragraph, compile slots in this order:

```text
P1 responsibility and incoming relation
  S1 opening purpose or carried endpoint
  S2 central claim or observation
  S3 evidence or concrete explanation
  S4 interpretation, condition, cost, or contrast
  S5 completed local consequence (only if needed)
P2 opening carries P1's declared endpoint and states P2's responsibility
```

This is a pattern for ordering, not a requirement to create all five roles.
Use only supported slots. A transition normally belongs in the opening slot
of the next paragraph, where it connects the previous endpoint to the new
responsibility. Do not append a detached handoff sentence at the end of one
paragraph and make the next paragraph rediscover the relation.

Before writing, run two tests:

- **Proposition test:** reading the slot propositions in order recovers the
  subsection's complete claim flow without prose.
- **Opening test:** reading only the first slot of each paragraph recovers the
  subsection framework, and each noninitial opening names both the carried
  endpoint and the paragraph's own responsibility.

If either test fails, repair the graph or outline. Do not ask prose to repair
it with connectives.

## 4. The writer packet is closed-world

For each paragraph, send the writer:

```text
global subsection question and takeaway
paragraph interface: responsibility, incoming endpoint/relation,
  outgoing endpoint, next paragraph's required input
ordered sentence slots: complete fields for S1...Sn
full paper glossary text, plus canonical terminology and allowed variants
allowed evidence and exact scopes
previous passing endpoint (not unreviewed neighboring prose)
```

The writer returns:

```text
paragraph prose
sentence_trace:
  output sentence 1 -> [S1]
  output sentence 2 -> [S2]
  ...
new lexical items: []
unresolved slots: []
endpoint produced: <declared outgoing endpoint>
```

The prose may improve grammatical form, sentence rhythm, and connective
wording. It may not add a technical object, noun, adjective, operation,
state-changing verb, evidence item, causal edge, scope condition, or hidden
implementation detail. A term absent from the canonical ledger is an
`unknown-lexical` finding even if it sounds like a synonym. A slot that cannot
be rendered naturally is a graph or context problem, not permission to invent
content.

Write and verify paragraphs in outline order. Only a paragraph whose trace and
endpoint pass the independent check becomes context for the next paragraph.
Separate subsections may run in parallel only after their interfaces and
sentence contracts are frozen.

## 5. Verify the trace, not the writer's explanation

An independent reviewer checks every generated paragraph against the contract:

1. every slot is realized exactly once, unless an authorized merge or drop is
   recorded;
2. every output sentence maps to an existing slot and preserves its role,
   proposition, relation, evidence, and scope;
3. the paragraph opening carries the declared incoming relation and its own
   responsibility;
4. no sentence consumes a node owned by another paragraph;
5. the produced endpoint is the declared endpoint; and
6. every lexical item and modifier is canonical and used at the right
   abstraction layer.

After all paragraphs pass, read only their openings and endpoints. If the
subsection no longer follows the frozen graph, roll back and route the defect
to outline alignment. Do not accept a fluent paragraph whose trace is
incomplete or whose graph has changed.

## 6. Relation to prose refinement

Round 1 renders the slots one-to-one. Round 2 may improve existing relations,
transitions, and sentence load while preserving slot IDs, order, paragraph
roles, and endpoints. Round 3 changes English only. Any change to a
proposition, relation, scope, paragraph responsibility, or canonical term is
an outline or semantic-graph delta and restarts rendering from the updated
contract.

The contract is therefore the stable interface between discussion and prose:
the author aligns the claim flow and sentence slots; the writer materializes
those slots; the independent reviewer verifies that the materialized prose
still expresses exactly that flow.
