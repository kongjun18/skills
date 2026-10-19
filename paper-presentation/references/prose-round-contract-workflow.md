# Frozen Prose-Round Contract

Use this workflow after the story, structured outline, semantic object graph,
sentence/logic slots, and terminology decisions have been aligned. It prevents
later prose rounds from silently becoming a new outline, a new vocabulary, or a
new argument.

## 1. Freeze the rendering contract

Before the first prose round, the coordinator creates one immutable rendering
contract for the requested scope. Record:

- the input manuscript version and fixed outline revision;
- paragraph IDs, order, roles, opening responsibility, incoming endpoint, and
  outgoing handoff;
- sentence or logic-slot IDs in order, including node IDs, `from`, `needs`,
  `link`/`transition`, evidence, scope, and expected relation;
- the sentence-level realization contract for each slot, including its concrete
  proposition, reader question, allowed merge, canonical terms, and forbidden
  additions;
- the semantic-object graph, including node type, object, claim strength,
  purpose/question edges, causal edges, and handoffs;
- the active terminology ledger, lexical provenance, canonical forms,
  allowed variants, and technical modifier contracts; and
- the figure/table source clauses and metric-purpose contracts in the scope.

Give the contract a stable revision or content hash. Every writer, reviewer,
and verifier receives this same contract in every round. The previous prose is
an input artifact to improve, not a replacement for the contract.

The contract is closed-world for technical meaning. A writer may realize an
existing node in different grammatical words, but may not add an object,
claim, evidence item, modifier, actor, target, state transition, causal edge,
scope condition, or technical term. A term that appears in the draft but is
not in the active ledger is an `unknown-lexical` finding, even when it sounds
like a reasonable synonym. For example, `invocation` cannot be introduced to
rename a request or operation unless the author explicitly adds that concept
and its contract.

## 2. Keep outline decisions outside prose rounds

The aligned outline is frozen during the three prose rounds. In particular,
the following are not wording choices:

- changing the first paragraph's responsibility or opening subject;
- reordering paragraphs or logical nodes;
- changing a sentence's `from`, `needs`, or relation;
- adding or deleting a handoff;
- changing a concept's abstraction layer; or
- replacing a canonical term with a new technical noun or modifier.

If one of these repairs is needed, stop the current round and emit an outline
delta. The coordinator must run the presentation-organization or semantic-graph
stage, obtain the required alignment, update the rendering contract, and then
rerender from Round 1. Do not apply a structural change inside Round 2 merely
because it makes the current prose read more smoothly. Automatic mode may make
such a choice only in its separate outline stage; it must never hide that
choice inside a prose round.

## 3. Round-specific change budgets

### Round 1: semantic rendering

Render each slot from the frozen node sequence. Splitting an overloaded
sentence is allowed only when the resulting sentences preserve the same node
order and mappings. Keep the paragraph opening's central subject or purpose in
the opening clause and make its incoming relation explicit.

### Round 2: transition and presentation check

The independent reviewer checks sentence pairs and paragraph boundaries. The
writer may clarify an existing relation, shorten a sentence, or remove a
redundant bridge sentence only when the node set, node order, paragraph roles,
and edges remain unchanged. A missing or reversed relation is a contract
failure, not permission to invent a transition. Route it to the outline or
semantic-graph stage.

### Round 3: concise English polish

Change grammar, articles, prepositions, sentence length, parallelism,
pronouns, and idiomatic connective wording only. Do not add a technical noun,
adjective, adverb, verb, evidence clause, causal relation, or qualification.
Canonical-term substitutions are allowed only when they are already listed as
allowed variants; otherwise they are lexical drift.

## 4. Round-trip verification

After every writer call, an independent verifier reconstructs the semantic and
presentation graph from the complete output. Compare it with the frozen
contract, not only with the writer's change list. Report a diff for:

1. missing or invented nodes;
2. changed node type, object, claim strength, abstraction layer, or scope;
3. missing, reversed, or newly invented relations and handoffs;
4. changed paragraph order, role, opening responsibility, or first-sentence
   subject;
5. changed evidence, metric purpose, figure/table source clause, or condition;
6. unknown technical lexical items, modifier drift, or operation/state-verb
   drift; and
7. sentence slots that no longer map to the same ordered nodes or concrete
   propositions.

Classify a diff as `wording-only` only when the contract remains equivalent.
Any other diff fails the round. Roll back to the last passing artifact and
route the issue to its earliest affected stage:

```text
unknown term              → terminology alignment
node/object/claim drift   → semantic_graph or story alignment
edge/ordering/handoff     → presentation_organization or outline alignment
scope/evidence drift      → claim/evidence alignment
```

Never feed a failed artifact into the next prose round. A fluent output is not
accepted when its first paragraph or transition graph no longer matches the
aligned outline.

## 5. Round packet and acceptance record

Each round packet contains:

```text
render_contract_revision
input_passing_version
round
allowed_change_budget
protected_node_ids
protected_edge_ids
protected_lexical_ids
writer_output_version
independent_verification_version
round_trip_diff
gate: pass | rollback | outline-delta | needs-context
rollback_target
```

Only a `pass` output becomes the input to the next round. The coordinator,
not the writer, updates the outline or rendering contract after an accepted
structural decision.
