# Iterative Method: refine -> rethink -> refine

The paragraph-level method used inside stage 2 (writing) and stage 3
(simplify) of the three-stage loop. A paragraph reaches top-conference
quality through **repeated structural reconsideration**, not one polishing
pass. "Rethink" is
the load-bearing step: it forces you to question the *argument*, not just the
sentences.

## Why two refines around a rethink

- The first **refine** fixes what you can see: the paragraph's stated job, the
  obvious reviewer objection, vague words, undefined terms.
- The **rethink** is where you leave editor mode and re-enter reviewer mode. It
  exposes the defects that survive a fluent rewrite: a mechanism presented as a
  heuristic, a design that reads as a choice rather than a necessity, an
  observation doing a requirement's job, a term arriving by fiat.
- The second **refine** fixes *structure*, which the rethink revealed. This is
  usually the edit that actually moves the paragraph to conference quality.

If you find yourself only swapping adjectives on the second pass, you skipped the
rethink.

## Per-paragraph loop

For each paragraph (or tightly-coupled pair):

1. **Name the job** in one phrase: bottleneck, failed strawman, observation,
   requirement, mechanism, contract, tradeoff, evidence, or implication. A
   paragraph with two jobs is usually two paragraphs, or one job buried.
2. **Write the reviewer objection** the paragraph must defeat. Be specific and
   hostile: "Why wouldn't the obvious existing structure just work?" not "could be clearer."
3. **Refine (pass 1):** make the paragraph follow
   observation -> requirement -> design choice -> consequence. Introduce notation
   only where it pins an invariant, resource model, or bound. Strip unsupported
   intensifiers. Ensure every term/symbol/label/citation is introduced before
   use.
4. **Rethink (the triggers below).** Read it once as the skeptical reviewer.
5. **Refine (pass 2):** apply the structural fix the rethink exposed — reorder,
   split, re-anchor the topic sentence, demote an observation, promote a
   requirement, replace an adjective with a bound, or earn a term before naming
   it.
6. **Stop test (below).** If it passes, move on. If not, loop 4–5 again. Do not
   loop forever: if two consecutive rethinks find only wording nits, stop.

## Rethink triggers (the skeptical-reviewer questions)

Ask these after pass 1. A "no" or an uneasy "sort of" means structure is wrong:

- **Necessity.** Does the design read as *forced* by resource pressure,
  correctness, and workload structure — or as one option the authors happened to
  pick? Top papers make the design feel inevitable.
- **Right argument.** Is this the *strongest* reason, or just the first one? Did
  the rewrite improve the wording of a weak argument instead of replacing it?
- **Strawman fairness.** If a prior approach "fails," is it given its best form?
  A reviewer who builds that approach will resent a weak strawman.
- **Observation vs. requirement vs. mechanism.** Are these separated? Workload
  observations motivate requirements; requirements justify mechanisms; evidence
  validates them. Collapsing them hides logic jumps.
- **Contract before implementation.** For a component, is what it *guarantees*
  (and deliberately does not) stated before how it works?
- **Correctness vs. performance.** Are they untangled? Correctness should rest on
  an invariant or exact check; performance on locality/bounds/measurement.
- **Terms earned.** Is every named mechanism introduced only when the reader
  needs it, as a consequence of the preceding sentence — not dropped in as a
  definition?
- **Adjectives -> evidence.** Is every "efficient / lightweight / scalable /
  large / small / robust" tied to a unit, bound, figure, or invariant? If not,
  cut it or ground it.
- **Reviewer value.** Does every sentence give a reviewer useful information
  for judging the problem, design, or evidence? Cut sentences that only carry
  minor details (implementation trivia, names of files or flags, tuning knobs,
  setup steps no claim depends on).
  A paragraph that walks through a figure should not restate what the axis
  labels or caption already say; it states the trend and the numbers the
  claim needs.
- **Reviewer's wording.** When a reviewer suggests a sentence, is every part
  of it supported by the paper? A better-sounding claim that holds for two of
  four workloads, or a causal claim no measurement shows, is a regression.
- **Overclaim.** What is the one sentence a reviewer would circle as
  overclaiming? Scope it.
- **Abstraction jump.** Does it leap from workload behavior to low-level detail
  without an intermediate design concept?

## Formula discipline (when the paragraph carries one)

A formula needs three parts, in order: a sentence that **motivates** it,
**definitions** for every symbol, and a prose **takeaway** stating what it proves
or bounds. If any of the three is missing, the rethink failed. State explicitly
which terms are assumptions, workload observations, or worst-case bounds. Repair
weak notation; do not delete the formula to make prose flow.

## Per-unit stop test

A paragraph is done when **all** hold:

- It does exactly one job, and a hostile reviewer's objection is answered in the
  text (not just in your head).
- It accepts the handoff from the previous paragraph and sets up the next (see
  `logic-chain.md`).
- Every term, symbol, label, citation, and figure ref is introduced before use
  and still resolves.
- Every sentence gives a reviewer useful information; no minor detail is left
  in for its own sake.
- No intensifier is doing an evidence's job; no formula is missing
  motivation/definitions/takeaway.
- Another pass would only churn wording.

When the stop test passes, **stop**. Over-editing introduces drift and risks the
preservation rules.
