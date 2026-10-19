# Logic Chain and Transitions

A section is more than good paragraphs. As a coauthor you own the **chain**: the
paragraphs must form one causal line a reviewer can follow without a leap, and
each transition must hand off on purpose. Do this pass **before** polishing
sentences — fixing a paragraph that sits in the wrong place wastes the work.

## Step 1 — Map the chain

For the section in scope:

1. Label each paragraph with its **job**: bottleneck / failed strawman /
   observation / requirement / mechanism / contract / tradeoff / evidence /
   implication.
2. Write the **one claim** each paragraph establishes, in one line.
3. Lay the claims in order and read them as a standalone argument. This bullet
   list *is* the logic chain. If the bullets don't read as a forced progression
   on their own, the prose won't either.

If the repository records a canonical narrative (for example a
motivation-to-design chain in a writing guide), check the actual order
against it.

## Step 2 — Detect logic jumps

A **logic jump** is any place where moving from one claim to the next requires a
fact, definition, or inference the reader does not yet have. Hunt for:

- **Asserted bridge.** A pivotal claim is *stated* but not *earned* by the
  preceding paragraph ("therefore, X..."). The prior paragraph must make the
  bridge inevitable.
- **Term by fiat.** A mechanism/name appears before the text motivates why such a
  thing is needed.
- **Skipped step.** The chain promises step N ("the next section shows why X")
  but the next paragraph jumps to N+1 and never delivers X.
- **Re-decision.** A paragraph re-argues a point already settled earlier,
  signalling the chain looped instead of advancing.
- **Conflated roles.** Two properties (e.g. a deterministic one and a workload
  one) are blurred into one "together they let us..." sentence, hiding which
  property licenses which conclusion. Split them and map each to what it buys.
- **Unstated premise.** A sentence relies on a fact the text has not stated
  yet, such as "if all in-memory copies are lost" before the text says the
  index lives in memory and is replicated. Check every definite noun phrase
  ("the X", "these X", "its copies") and every "thus", "therefore", and
  "however": its antecedent or cause must appear earlier, preferably in the
  sentence before.
- **Unmotivated requirement.** A requirement appears without the observation that
  forces it, or a mechanism without the requirement it satisfies.
- **Abstraction jump.** Workload behavior -> low-level detail with no
  intermediate design concept.
- **Dangling challenge.** Numbered challenges/requirements (C1/C2/C3) are raised
  but never explicitly resolved, or are silently renamed later (B1/B2/B3) without
  a mapping.

For each jump, write the **missing link** in one sentence. The fix is usually to
add that sentence to the *upstream* paragraph (earn the bridge) rather than to
patch the downstream one.

## Step 3 — Audit each transition

Every paragraph boundary is a contract: the last sentence **offers** a
consequence; the first sentence **accepts** it. Classify and check each seam:

- **Consequence ("therefore / as a result")** — the prior paragraph's result
  forces this paragraph's topic. Verify the result was actually established.
- **Contrast ("but / however / this is not enough")** — this paragraph corrects
  or limits the prior one. Verify the limitation is real and stated, not a
  strawman.
- **Refinement ("more precisely / concretely")** — same idea at finer grain.
  Verify it doesn't silently introduce a new claim.
- **Enumeration ("first / second / the remaining problem")** — parts of one
  structure. Verify the structure was announced and all parts are delivered.

- **Topic turn inside a paragraph.** When the text turns to a new option
  (for example, from an in-memory index to an on-SSD one), start a new
  paragraph whose first sentence links back ("Keeping the index on SSD
  avoids this rebuild").

Bad transitions to fix: a topic sentence that restates the previous paragraph's
conclusion (redundant — advance instead), a "thus" with no prior cause, a new
paragraph that opens on a brand-new noun with no link back.

## Step 4 — Section read-through

After paragraph-level edits, read the **whole section top to bottom** as a
reviewer seeing it once:

- Does each paragraph advance the chain, or does any stall / loop / re-decide?
- Is there exactly one place each concept is introduced, before all uses?
- Are correctness and performance threads kept distinct throughout?
- Do raised challenges get resolved (and mapped if renamed)?
- Does the section end where the next section needs to begin?

## Chain-integrity checklist (run before finishing a section pass)

- [ ] Paragraph jobs are labeled and each establishes exactly one claim.
- [ ] The claim list reads as a forced progression with no jump.
- [ ] Every bridge sentence is earned by the paragraph above it.
- [ ] Every term/mechanism is introduced as a consequence, not by fiat.
- [ ] No paragraph re-decides a settled point.
- [ ] Conflated deterministic/empirical (or observation/requirement) roles are
      split and each mapped to what it licenses.
- [ ] Every numbered challenge/requirement is resolved or explicitly mapped.
- [ ] Each transition's offer/accept contract holds; no dangling "thus".
- [ ] The section's last sentence sets up the next section.
- [ ] Formulas, labels, citations, and figure refs are intact (`git diff
      --check`, refs resolve).
