# Refine and Simplify

Read this when refining or rewriting existing paragraphs, including a request
about one paragraph, or when shortening a verbose draft. A paragraph reaches
conference quality through repeated structural reconsideration, not one
polishing pass. Apply the
[terminology contract](terminology.md) to every edit.

## 1. Local paragraph work

An old or missing outline never blocks a local review or rewrite.

1. **Bind the scope:** the paragraphs in scope, the previous paragraph's last
   sentence and endpoint, the next paragraph's opening and what it needs, the
   glossary, and the outline rows if any. Read enough neighbors to recover
   both interfaces.
2. **Classify against the outline** (build a local reverse outline first):
   `consistent`; `prose-defect` (outline right, prose weak);
   `outline-stale` (the paragraph has a supported job the outline lacks);
   `interface-conflict` (the repair would change what the paragraph receives
   from or gives to a neighbor); or `no outline`.
3. **Read-only review request:** that belongs to `paper-presentation-review`,
   which uses this classification and returns findings and the smallest
   outline delta. A stale outline is a finding, never a reason to stop.
4. **Rewrite request:** revise from the outline if consistent; if stale or
   absent but both interfaces stay unchanged, rebuild the local paragraph claim
   and interfaces (and L2 rows if needed), revise from them, and record the
   delta. If the repair changes a shared interface, keep the neighbors
   untouched, return the proposal with the interface delta, and ask the
   author. Never invent a neighboring claim to make the paragraph fit. When the
   author asks for a rewrite rather than a wording fix, rebuild from the claim
   and evidence instead of keeping the old sentence order.
5. **Finish:** check the opening and endpoint against both neighbors and run
   the closed-world gate. Report `outline-sync-required` when an outline
   delta has not yet been written back.

## 2. Per-paragraph loop: refine → rethink → refine

For each paragraph (or tightly coupled pair):

1. **Name the job** in one phrase (see the job list in
   [flow-and-openings.md §1](flow-and-openings.md#1-map-the-chain)).
2. **Write the reviewer objection** the paragraph must defeat. Be specific and
   hostile: "Why would the obvious existing structure not work?", not "could
   be clearer".
3. **Refine, pass 1.** Fix what is visible: make the paragraph follow its
   supported order (often observation → requirement → design choice →
   consequence), check the opening contract, strip unsupported intensifiers,
   and make every term, symbol, label, and citation appear before use.
4. **Rethink.** Leave editor mode and read once as the skeptical reviewer,
   using the triggers in §3.
5. **Refine, pass 2.** Apply the structural fix the rethink exposed: reorder,
   split, re-anchor the opening, demote an observation, promote a requirement,
   replace an adjective with a bound, or earn a term before naming it. Within
   the rules of
   [flow-and-openings.md §7](flow-and-openings.md#7-organization-moves).
6. **Stop test (§4).** If it fails, repeat 4 and 5. If two consecutive rethinks
   find only wording nits, stop.

If the second pass only swaps adjectives, the rethink was skipped.

## 3. Rethink triggers

A "no" or an uneasy "sort of" means the structure is wrong:

- **Necessity.** Does the design read as forced by resource pressure,
  correctness, and workload structure, or as one option the authors picked?
- **Right argument.** Is this the strongest reason or only the first one? Did
  the rewrite polish a weak argument instead of replacing it?
- **Strawman fairness.** Is a "failing" prior approach given its best form?
- **Observation, requirement, mechanism.** Are they separated? Observations
  motivate requirements; requirements justify mechanisms; evidence validates.
- **Contract before implementation.** Is what a component guarantees (and
  does not) stated before how it works?
- **Correctness vs. performance.** Correctness rests on an invariant or exact
  check; performance on locality, bounds, or measurement.
- **Terms earned.** Is each named mechanism introduced when the reader needs
  it, as a consequence of the previous sentence?
- **Adjectives to evidence.** Is every quality word tied to a number, bound,
  figure, or invariant?
- **Describing vs. arguing.** "The system has three components" describes;
  "each component removes one of the three costs measured in Section 3"
  argues. A describing sentence either gains its conclusion or goes.
- **Reviewer value.** Does every sentence give a reviewer information for
  judging the problem, design, or evidence? Cut implementation trivia, file or
  flag names, tuning knobs, and setup steps no claim depends on. A figure
  walk-through states the trend and the numbers the claim needs, not the axes.
- **Reviewer's wording.** Is every part of a suggested sentence supported? A
  better-sounding claim that holds for two of four workloads is a regression.
- **Overclaim.** Which sentence would a reviewer circle? Scope it.
- **Abstraction jump.** Does it leap from workload behavior to low-level detail
  without an intermediate design concept?

**Formulas.** A formula needs a sentence that motivates it, a definition for
every symbol, and a prose takeaway stating what it proves or bounds. Say which
terms are assumptions, workload observations, or worst-case bounds. Repair weak
notation; never delete a formula to make prose flow.

## 4. Stop test

A paragraph is done when all hold:

- it does one job and answers the hostile objection in the text;
- its opening carries the previous endpoint and its own job, and it ends on a
  claim the next paragraph can use;
- every term, symbol, label, citation, and figure reference is introduced
  before use and resolves;
- protected terms keep their canonical or explicitly allowed form;
- no intensifier does an evidence's job, and no formula lacks its three parts;
- another pass would only churn wording.

Then stop. Over-editing introduces drift.

## 5. Simplify

Agent drafts are verbose: they restate, hedge, narrate their own structure, and
describe where they should argue. Rethink first, per paragraph:

1. Write in one line what the reviewer must conclude from the paragraph.
2. Mark each sentence: **carries** (a claim, evidence, definition, cost, or
   bridge the conclusion needs), **repeats** (said by another sentence, the
   caption, or an axis label), **describes** (a fact with no consequence for
   the conclusion), or **frames** ("In this section we...", "Note that").
3. Keep the carriers. Cut the rest, or turn a describer into a carrier by
   adding its consequence.
4. A paragraph with no single conclusion is two paragraphs or none.

Then simplify sentences:

- One point per sentence; split a sentence with three or more clauses.
- Merge two sentences that make one point.
- Replace a clause with a number when the number says it ("much faster"
  becomes "6× faster").
- Plain words: "use", not "leverage"; "shows", not "demonstrates".
- Drop hedges the evidence does not need; keep a hedge that scopes a real
  uncertainty.
- Drop transitions the logic already carries ("Furthermore", "Moreover"), and
  mechanically stacked connectives, while keeping the relation explicit.
- In an introduction, name a mechanism once, with what it buys.

Guardrails:

- Never cut a claim, number, formula, citation, figure reference, condition,
  or definition that a later sentence uses. Repair it instead.
- Never replace a protected term with a shorter near-synonym to save words or
  fix a short last line.
- Recheck every transition after cuts: a cut sentence is often the bridge.
- Report the word count before and after and each removed sentence with its
  reason.

## 6. Language-only pass

The last edit before the closed-world gate (see the gate in the
[skill](../SKILL.md#closed-world-gate)) is language only: grammar, articles,
prepositions, idiom, sentence length, parallelism, pronoun antecedents. It may
shorten or split a sentence. It does not add or remove a concept, claim,
evidence item, qualifier, mechanism, figure source clause, or handoff, does
not reorder paragraphs or change an opening's job, and does not vary a term for
style. A wording change that would alter one of these goes back to refinement.
