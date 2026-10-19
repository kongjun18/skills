# Iterative Prose Refinement

Use this workflow when the story and reader-facing outline are aligned but the
rendered prose still has weak transitions, overloaded sentences, unexplained
terms, or unnecessary repetition. Iteration is a sequence of different gates,
not a quota of similar rewrites. Before the first writer call, load the
[frozen prose-round contract](prose-round-contract-workflow.md) and create one
closed-world render contract. Every later round must pass an independent
round-trip check against that contract.
The contract must be compiled from the complete claim flow using the
[claim-flow materialization workflow](claim-flow-materialization-workflow.md).
Round 1 writes one paragraph at a time in outline order; Round 2 and Round 3
operate only on the resulting passing subsection.

## Preconditions

Do not start this workflow until the story, section responsibilities,
terminology decisions, evidence mappings, and scope conditions are aligned.
Paragraph grouping, sentence order, and openings remain reviewable
presentation decisions: the presentation organization gate may change them
when the story and substantive interfaces remain fixed. If a proposed move
changes a story claim, section responsibility, evidence scope, terminology
decision, or shared interface, stop the current round, update the outline and
its change log, and rerun the affected earlier gate.

Bind every round to:

- one immutable manuscript version;
- one fixed outline revision;
- the active rule profile and paper-specific writing guide;
- the owned paragraph and sentence IDs;
- protected claims, evidence, terminology, and scope; and
- the previous round's findings and acceptance conditions.

Also bind the round to the immutable render-contract revision, protected node
and edge IDs, protected lexical IDs, and its change budget. The previous prose
is never the structure source for a later round.

For `rebuild-from-material`, also bind the immutable material ledger and its
source-unit disposition map. Round 1 renders from the aligned contracts and
material IDs; the raw source prose is evidence lookup only, not the drafting
template.

## Three-round plan

The default automatic plan has three rounds. A user-supplied limit can shorten
the plan, but a round may not be repeated under a different name to claim
progress. If a later round finds a structural regression, return to the
earliest affected round and rerun its downstream rounds.

### Round 1: semantic rendering

Read the complete ordered claim graph, then render one paragraph contract at a
time in outline order. Do not batch unverified paragraphs into one writer
output. After a paragraph passes its local contract check, carry its endpoint
to the next paragraph. Preserve the story,
outline order, claims, evidence, scope, and terminology. Focus on:

- one main logical relation per sentence;
- splitting sentences that combine several new concepts, causal steps, or
  qualifications;
- introducing a concept through its role, input, purpose, or effect before its
  dependent claim;
- keeping each paragraph at its declared abstraction layer; and
- carrying each paragraph's incoming endpoint and responsibility in its opening
  sentence.

Do not add stylistic synonyms, generic transitions, new technical terms,
extra definitions, or implementation detail to make a sentence sound complete.

**Gate:** an independent verifier reconstructs the output and finds the same
ordered nodes, paragraph roles, opening responsibilities, edges, evidence,
scope, and active lexical items as the render contract. No sentence is
overloaded; every required concept is available before use; and the
first-sentence-only test still recovers the subsection framework. A missing or
invented node, relation, paragraph responsibility, or technical term fails the
round and is not passed to Round 2.

### Round 2: presentation and logic repair

Use an independent review of the Round 1 artifact. Check every adjacent
sentence and paragraph boundary for a concrete endpoint and a supported
relation. Name the relation explicitly in the review, such as consequence,
dependence, purpose, evidence, specialization, contrast, or parallel
alternative.

If the story remains correct but the presentation graph is weak, this round
must check whether the frozen contract was rendered incorrectly. Merge, split,
reorder, relocate, or delete units only in the separate presentation
organization stage, where the outline delta can be recorded and aligned. A
prose round may remove a redundant bridge or clarify an existing relation only
when node order, paragraph roles, opening responsibilities, and edges remain
unchanged. Do not preserve one source sentence per output sentence merely
because Round 1 produced it, but do not let a prose writer silently create a
new organization either.

For sibling paragraphs that realize alternatives under one umbrella concept,
record the common parent and the branch relation. The opening of the second
branch must make the parallel or contrast relation visible; it must not merely
introduce another object as a list item. Treat a supporting mechanism or caveat
as a side branch rather than as a new main line when the outline says it is
supporting context.

Also check:

- a sentence does not move from a caveat to the next main claim without a
  supported relation;
- a background subsection does not turn a declarative explanation into an
  unexplained question;
- a paragraph does not repeat its opening, its preceding handoff, or its next
  paragraph's claim;
- bridge-only sentences and summary sentences with no new job are removed;
- an unknown technical term is replaced with the established term or routed to
  `Needs context`;
- a term is used at its declared layer and a backend example is not generalized
  to the logical system object; and
- the prose states the reader-visible claim before a lower-level mechanism that
  explains it.

**Gate:** every sentence pair and paragraph boundary has a recoverable
relation, sibling alternatives read as alternatives, no unsupported term or
layer jump remains, and any required organization move is recorded. The
independent verifier must also find no node, edge, paragraph-role, opening, or
lexical diff from the frozen render contract. A presentation-only outline delta
is handled outside this round; until it is aligned, the current artifact fails
and is not passed to Round 3.

### Round 3: concise English polish

Run a bounded language-only pass on the Round 2 artifact. Improve grammar,
articles, prepositions, sentence length, parallelism, pronoun antecedents, and
natural transitions. Remove redundant modifiers, repeated subjects, and
mechanically stacked connectives such as `because`, `therefore`, and
`however` when the relation remains explicit.

Do not reopen the story, paragraph order, sentence roles, terminology
decisions, evidence mappings, or claim scope. A proposed change that would do
so returns to Round 1 or Round 2 instead of being applied here.

**Gate:** the prose is concise and idiomatic, while an independent blind
round-trip check recovers the same claims, relations, paragraph openings,
scope, and terminology as the frozen render contract. A new technical noun,
adjective, adverb, operation verb, or relation verb is lexical drift even when
the sentence is fluent. Language polish cannot repair a structural or semantic
mismatch.

## Review and handoff protocol

Each round is:

```text
fixed render contract + last passing artifact → focused review
→ bounded revision → independent round-trip verification
```

The reviewer and writer must be separate calls or agents. A writer's self-check
can identify likely issues but cannot close a required finding or substitute
for the independent review gate.

Record for each round:

```text
iteration_id
round: 1 | 2 | 3
goal
input_version
outline_revision
active_profile
findings_opened
findings_addressed
gate: pass | rerun-earlier-round | needs-context | limit-reached
output_version
verification_version
render_contract_revision
protected_node_ids
protected_edge_ids
protected_lexical_ids
allowed_change_budget
round_trip_diff
rollback_target
```

Once the outline and edit authorization are aligned, continue through all three
rounds in both manual and automatic workflows. Manual mode controls story,
claim, hierarchy, terminology, evidence, and scope decisions; it does not
require the user to trigger each wording round. Pause when a round exposes one
of those substantive decisions. Record any automatically selected wording or
supported relation in the change map. Stop after Round 1 only for an explicit
`draft-only` request. Never use iteration to silently decide an unresolved
author choice.

## Stopping and rollback

Stop with `Needs context` when a transition, term, mapping, or claim cannot be
resolved from the manuscript, writing guide, evidence, or author decisions.
Stop with `Awaiting outline alignment` when the repair changes grouping, order,
responsibility, handoff, sentence relation, or concept layer. Roll back to the
last passing artifact when a round-trip diff reports an invented node, changed
edge, first-paragraph drift, or unknown technical term; route the issue to the
earliest affected outline, semantic-graph, or terminology stage. Stop with
`Needs revision` when the requested round limit is reached with required
findings open. Otherwise finish only after Round 3's independent verification.
