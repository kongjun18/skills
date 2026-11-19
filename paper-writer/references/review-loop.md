# Review Loop and Reviewer Briefs

Read this before dispatching a reviewer subagent or when deciding whether a
stage is finished. The Outline, Draft, Refine, and Simplify stages run the same loop:

1. **Produce** the stage's artifact.
2. **Review** it with an independent reviewer subagent (§1).
3. **Verify** every finding yourself (§3).
4. **Refine.**

Leave the stage after 3 rounds, or earlier once no high-priority issue
remains (§4). Keep round artifacts (outline rounds, extracted chains, verdicts)
in ignored scratch space, one file per round; the final outline goes to the
project's outline location if it declares one.

## 1. Reviewer subagents

- **Independence.** The reviewer is a separate subagent, read-only, run at high
  effort. A writer's self-check is never reported as review. If no subagent is
  available, run the review as a separate pass over a frozen copy and label the
  result self-checked.
- **Brief.** Give each reviewer:
  - its role: a program-committee member of the target venue;
  - the outline's phase and the phase rules in the
    [skill](../SKILL.md#phase-controls-the-review);
  - this skill's `SKILL.md`, [reviewer-lens.md](reviewer-lens.md), the
    stage's references, and the project's paper rules, to read from disk;
  - the files to read first, and the frozen version it reviews;
  - author constraints it must not argue against;
  - the glossary path and the terminology ledger, with the instruction not to
    propose near-synonyms for protected terms or any banned term
    ([terminology.md](terminology.md));
  - the stage's report format (below) with a word limit.
- **Who reviews.** Keep one reviewer for all rounds of a stage, continuing the
  same agent. Use a fresh reviewer at the start of each stage, so the writing
  review is a cold read. The final verifier is always fresh and never sees the
  writer's plan or rationale; brief it with `paper-presentation-review`.
- **Reviewers overreach.** Reject a suggested wording the paper does not
  support, however well it reads.

## 2. Stage briefs

**Outline stage.** Ask the reviewer to read the manuscript first, then the
outline, and return:

1. a verdict;
2. logic jumps by line ID, each with a fix
   ([flow-and-openings.md §2](flow-and-openings.md#2-detect-logic-jumps));
3. reviewer questions left unanswered: problem, why existing approaches fail,
   what is new, necessity, evidence, cost;
4. evidence that is missing, wrong, or unscoped, with every number checked
   against the manuscript and a list of those verified;
5. float roles: one reviewer question and one takeaway each; citing sentences
   point to a panel that shows the claim; redundant floats; key claims with
   none;
6. positioning gaps against related work;
7. a phase-appropriate budget check;
8. prioritized changes, each high or low.

From round 2, ask for the change in verdict, remaining issues only, and an
explicit "ready / not ready".

**Draft and Refine stages.** A fresh reviewer at the start of Draft (Refine
continues it):

1. reads the rendered text first (for example `pdftotext -layout`), so its
   first impression is a reader's;
2. then reads the source, the rest of the paper, and the final outline;
3. extracts the logic chain from the prose, one claim per paragraph, and the
   first-sentence summary, and compares both with the outline; each difference
   is a defect or a deliberate change.

It returns scores from 1 to 5 (motivation, novelty as presented, soundness,
clarity, overall), a transition audit (P1→P2, ... each "holds" or a fix),
problem sentences quoted with replacements, the main weakness a real reviewer
would write, and prioritized changes that do not lengthen the text. In later
rounds, tell it what you applied and rejected, and ask for the change in its
scores.

**Simplify stage.** A fresh reviewer gets the before and after text and
answers:

1. Is anything a reviewer needs now missing: a claim, number, definition,
   cost, or citation?
2. Does the chain still hold at every transition?
3. Which sentences still describe instead of argue, or say one thing twice?
4. Which sentences are now too compressed to follow?
5. Did any cut change a protected term, concept, operation, state, or
   qualifier? Reject it unless the author updated the ledger first.

**Related Work.** Use the briefs in [related-work.md](related-work.md).

## 3. Verify every finding

- Check each finding in the manuscript, the data, or the code; settle factual
  questions in the source (for example, read the code before stating what a
  baseline keeps in memory).
- Give each a verdict: accept, accept in part, or reject, with a one-line
  reason. Record verdicts so later rounds do not reopen them, and tell the
  reviewer what you rejected and why.
- Reject wording that is better written but less true: a claim that holds for
  some workloads only, or a causal claim no measurement shows. Replace it with
  what is plainly true.
- Reject a shorter near-synonym for a protected term.
- Decide disagreements between rounds or reviewers by evidence, and say why.

## 4. Exit rule

Leave a stage when 3 rounds are done, or when the last review found no
high-priority issue or every one is fixed. High priority means a logic jump, a
wrong or unsupported claim, an unanswered reviewer question, an undefined
term, a contradiction with the rest of the paper, a terminology-lock
violation, or, in Submission, a budget or layout overrun. Nits never justify
another round. If high-priority issues remain after 3 rounds, list them for the
author instead of looping.
