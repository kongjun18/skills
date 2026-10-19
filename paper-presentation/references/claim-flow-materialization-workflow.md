# Claim-Flow Materialization

Use this workflow after the story, semantic object graph, and structured outline
have been aligned, and before prose refinement. The primary object being
written is the supported claim flow. Prose is its reader-facing materialization;
it is not a second place to decide what the paper means.

For the exact writer input and output trace, also use the
[sentence-level realization contract](sentence-realization-contract.md).
This workflow freezes the graph and paragraph interfaces; that contract turns
each graph node into a concrete proposition that can be checked sentence by
sentence.

## 1. Freeze the whole claim flow first

Before writing any paragraph, inspect the complete subsection graph. Confirm:

- the subsection question and takeaway;
- the ordered claims and their evidence or reasoning basis;
- the objects, mechanisms, metrics, costs, conditions, and implications;
- each edge between adjacent nodes (`supports`, `purpose`, `consequence`,
  `contrast`, `specialization`, `evidence`, or another supported relation);
- each paragraph's responsibility, incoming endpoint, provided nodes, and
  outgoing endpoint; and
- the canonical terms and abstraction layer for every technical object.

Freeze all paragraph interfaces before writing the first paragraph. The writer
may write paragraphs sequentially, but it must not be asked to discover the
next paragraph's claim while rendering the current one. This is the boundary
between outline research and prose materialization.

Run the node-only test before prose: the ordered node labels must already tell
the subsection's argument. If the argument is unclear, merge, split, reorder,
relocate, or remove nodes in the outline and obtain alignment before writing.
Do not ask prose to discover a missing purpose or transition.

## 2. Compile paragraph and sentence materialization contracts

Compile one paragraph interface from the same graph. It contains:

```text
paragraph_id
responsibility
incoming_endpoint
incoming_relation
ordered_node_ids
claim_and_evidence_slots
required_terms
allowed_scope
outgoing_endpoint
next_paragraph_needs
opening_subject_or_purpose
```

Compile the sentence-level realization contract at the same time. Each slot
contains one concrete proposition, reader question, incoming relation,
evidence, scope, canonical terms, provided claim, opening requirement,
allowed merges, and forbidden additions. A slot that says only “explain the
result” is incomplete. Round 1 uses one slot per sentence by default and
records a sentence-to-slot trace.

The full claim flow remains visible to the coordinator. A paragraph writer also
receives its own contract, the last passing endpoint from the preceding
paragraph, and the next paragraph's required input. This gives enough context
for a natural transition without allowing neighboring prose to become an
unreviewed structure source.

## 3. Materialize paragraphs sequentially

Write one paragraph at a time in outline order. For each paragraph:

1. start from its responsibility and incoming relation;
2. introduce each required object through the role, purpose, input, or effect
   that the graph assigns to it;
3. render the ordered claim/evidence nodes with the required scope and
   canonical terms;
4. end at the declared outgoing endpoint when the paragraph needs to hand off
   to the next paragraph; and
5. record the output endpoint and the sentence-to-slot and node-to-sentence
   mappings.

The writer may split or combine sentences for clarity, but every output
sentence must map to existing ordered nodes. It may not add a technical noun,
modifier, causal relation, evidence item, or implementation detail to make the
paragraph sound complete. If the contract cannot be rendered naturally, mark
the missing context or graph defect; do not invent a bridge.

After each paragraph, run a focused independent check against its contract:

- the opening states the paragraph's own responsibility and carries the
  incoming relation;
- the node order, claims, evidence, scope, and terminology are preserved;
- the paragraph does not consume a node owned by another paragraph;
- the final endpoint is the one promised to the next paragraph; and
- no new concept, adjective, noun phrase, or state-changing verb has appeared.

Only a passing paragraph becomes input to the next paragraph. If it fails,
rerender it from the same contract rather than allowing the failure to propagate
through later paragraphs.

This is an execution rule, not only a review preference. Do not send a whole
subsection to one writer call and ask it to generate all paragraphs at once.
When the runtime exposes only one writer call, implement the same loop inside
the call: complete one paragraph, run its contract check, commit its passing
endpoint, and then start the next paragraph. Do not expose an unverified
paragraph as context for a later paragraph.

## 4. Check migration after the subsection is materialized

Once all paragraphs pass locally, run one subsection-level migration check.
Read only the paragraph openings and endpoints, then reconstruct the claim flow
without using the writer's explanation. Verify that:

- each paragraph follows from the endpoint before it;
- each opening states both the carried relation and its own responsibility;
- no paragraph repeats a prior handoff or preempts a later claim;
- sibling alternatives are visibly parallel or contrasted;
- the final paragraph answers the subsection question; and
- the prose graph is equivalent to the frozen claim graph.

Repair a local boundary sentence when the graph is correct but the migration is
hard to read. If the repair changes node order, paragraph responsibility,
abstraction layer, or an edge, stop and create an outline delta. Do not hide a
graph change inside a transition rewrite.

## 5. Relation to the three prose rounds

Paragraph materialization is the Round 1 execution method. Round 2 may improve
the realization of existing edges after the whole subsection exists; it does
not reopen the claim flow or silently regroup paragraphs. Round 3 is language
only. Both rounds use the frozen prose-round contract and must pass its
independent round-trip check.

This workflow is compatible with parallel subsection work. Paragraphs within a
subsection are sequential because each consumes the previous endpoint. Separate
subsections may proceed in parallel only after their incoming and outgoing
interfaces are frozen.
