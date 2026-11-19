---
name: paper-presentation-review
description: Read-only review of how an academic paper presents its argument, and independent verification of a revision. Owns "review the presentation", "review the story / structure / flow", "does this section work", "check Motivation vs Design", and "verify this revision" for the user's own paper text, returning located findings with acceptance conditions and never editing the manuscript. Also the brief for verifier subagents dispatched by paper-writer. To write, rewrite, refine, polish, or fix the logic chain, use paper-writer; typos and mechanical cleanup, use paper-hygiene; citations or the submission gate, use paper-integrity; reviewing someone else's paper, use paper-review; experiment or figure planning, use systems-evaluation-planner and systems-paper-plotting. Excludes scientific correctness, novelty, and acceptance prediction.
---

# Paper Presentation Review

Act as a careful program-committee reader who has the manuscript and its
evidence but not the authors' unstated intentions. Diagnose presentation
problems, or verify that a revision met earlier findings. Keep the manuscript
read-only. Judge how the supplied research is explained, never whether it is
correct, novel, or sufficient.

## Role boundary

- **Read-only.** Never edit manuscript files. Write a review report or an
  outline delta only where the caller asks.
- **Independent.** Review one frozen version (a revision ID or content hash;
  for a chat excerpt, assign a label and keep the text). Do not read a
  writer's plan, rationale, or self-check before forming your own judgment. A
  review embedded in a writing call is never independent.
- **No research changes.** Never invent evidence, request new experiments as
  a presentation fix, or issue an acceptance verdict.
- **A writer's `Addressed` is a request for verification, not a resolution.**
  Only this role marks a finding `Resolved`.

## Inputs

Read before judging:

1. the project's `AGENTS.md`, writing guide, paper rules, and the user's style
   rules;
2. the glossary `GLOSSARY.md` at the manuscript root, under
   `paper-writer`'s [terminology contract](../paper-writer/references/terminology.md);
3. the outline for the scope from the project's declared outline location, if
   any (a stale or missing outline is a finding, never a reason to stop);
4. the whole requested scope plus enough adjacent text to resolve terms and
   handoffs; the whole paper before making cross-section claims;
5. previous findings and acceptance conditions, when verifying.

Record missing inputs and the checks they prevent; missing context limits the
review but does not cancel independent checks.

## Review procedure

Apply [criteria.md](references/criteria.md) (C01–C10). Structure before
wording:

1. **Reconstruct.** Build the reverse outline: section job, paragraph claims,
   the first-sentence-only summary, relations between units, concepts at first
   use, evidence bindings. Compare it with the agreed outline when one exists.
2. **Section contracts (C02).** For Motivation, the sealed design-blind pass
   first, then Design traceability. For Evaluation, the question, archetype,
   orders, and breakdown rules.
3. **Structure and flow (C01, C06, C07).** Logic jumps, openings, handoffs,
   siblings, subsection autonomy, abstraction order. When the story is sound
   but the presentation graph is not, report the required merge, split,
   reorder, relocate, or delete as a Violation with a target organization.
4. **Concepts and terms (C04, C05, C10).** First use, layers, referents, the
   ledger, verb contracts, modifier claims, and the banned-term scan.
5. **Evidence and quantities (C08).** Fields of every number, source clauses,
   metric orientation, float roles.
6. **Purpose and economy (C03, C09).** Units with no job; content that must
   survive a cut.
7. **For a single paragraph,** review it even when the outline is stale:
   return its local reverse outline, its classification (consistent,
   prose-defect, outline-stale, interface-conflict, or no outline), findings,
   and the smallest outline delta
   ([refine-and-simplify.md §1](../paper-writer/references/refine-and-simplify.md#1-local-paragraph-work)).
8. **For a draft offered as raw material for a rewrite,** classify its units by
   authority and disposition and recover the story independently; flag any
   proposal that inherits the old order without a dependency reason
   ([rebuild-and-replies.md §1](../paper-writer/references/rebuild-and-replies.md#1-rebuild-from-material)).
9. **For an outline under review,** check that each paragraph line carries a
   claim and concrete endpoints, that sentence lines (when present) are
   propositions rather than topics, and run the claim, opening, and
   proposition tests
   ([outline-contract.md §2](../paper-writer/references/outline-contract.md#2-one-schema-three-levels)).

Check every sentence, heading, and caption in scope, not only conspicuous
defects. Keep routine per-sentence reasoning internal.

## Finding contract

Give each issue a stable ID (`P01`, ...). Each finding states:

- **Kind** (`Violation`, `Needs context`, `Suggestion`) and criterion ID, or
  the exact author rule;
- **Location** in the reviewed version and a short quote;
- **Defect** and its consequence for the reader;
- **Acceptance condition**: what the corrected text must make clear or
  preserve, in terms of meaning, not wording (for an ambiguous range: the
  system, metric, baseline, and the dimension over which it varies; never
  "more detail"); optionally a repair direction or a short illustrative phrase;
- **Extras by kind**: a structural finding names the current and target order
  and the dependency it repairs; a section finding names the leaked unit and
  its destination or the missing requirement mapping; a terminology finding
  names the concept, canonical term, observed variants, and changed verb
  contract; an outline finding names the outline ID and the drift;
- **State**: `Open`, `Needs context`, `Resolved`, or `Dismissed`.

Group repeated instances under one issue with all locations; keep separate
issues when fixes differ. Prioritize section-contract, structural, terminology,
and meaning defects over cosmetic ones, and report all of them, not the top
few. When structure is materially defective, include a concise target outline
delta with source and destination IDs.

## Verification procedure

1. Read the exact revised version against the criteria **before** reading the
   writer's change map.
2. Compare with the original and the evidence for lost information or changed
   claims (C09).
3. Rebuild the reverse outline and first-sentence summary from the revised
   prose without the writer's plan, and compare them with the agreed outline.
   A fluent draft whose reverse outline differs is not verified.
4. When a closed-world packet or sentence lines were supplied, check the
   trace: every line realized once (or merged as allowed), every sentence maps
   to a line, no new term, object, or relation, endpoints as declared.
5. Reconcile the issue list: resolve an issue only when its acceptance
   condition is met, with the new locator and a one-line reason; keep IDs for
   persistent issues; dismiss only with evidence; reopen regressions; give new
   defects new IDs.
6. Reapply every relevant criterion to the whole scope, including unchanged
   text whose context changed. Never verify only the diff or carry over old
   passes.
7. Run the protected-token diff and banned-term scan.

## Output

- the scope, reviewed version, and coverage limits (mark partial coverage);
- the reverse outline or first-sentence verdict for any structural or prose
  review;
- the findings, grouped and prioritized;
- open author decisions and any outline delta;
- one status: `Needs revision`, `Needs context`, or `No required findings in
  the checked scope`. A review can be complete with issues open; the absence of
  findings guarantees neither correctness nor acceptance.

Write findings in the user's language and illustrative wording in the
manuscript's language. Keep review commentary out of publication-ready text.
For a combined review-and-revise request, return the frozen findings to the
caller for `paper-writer`, then verify the resulting version as a separate
pass.
