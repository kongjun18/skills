# Three-stage loop: outline, writing, simplification

Each stage runs the same loop:

1. **Produce** the stage's artifact.
2. **Review** it with a reviewer subagent.
3. **Verify** every finding yourself.
4. **Refine.**

Leave the stage after 3 rounds, or earlier once every high-priority issue is
fixed. Then go to the next stage.

Keep the artifacts in ignored scratch space, one file per round: the outline
rounds, the extracted chains, and the verdicts. If the project keeps shared
outlines, the final outline goes there.

## Phase filter

Read the `Phase: Early`, `Phase: Draft`, or `Phase: Submission` line in the
section outline before every round. Run all three stages, but apply the phase
filter to the review:

- **Early** reviews focus on claims, roles, the logic chain, evidence, and
  cross-section contradictions. Budget, wording, layout, figure style, and
  final-number checks go in a short `Later` list.
- **Draft** reviews focus on prose following the agreed outline, scoped claims,
  definitions, and transitions. A gross page overrun is a low-priority
  `Later` item; detailed layout work waits.
- **Submission** reviews focus on budget, layout, figure size, simplification,
  consistency, citations, and final numbers. Restructuring is deferred unless
  a logic defect blocks the checks.

Items in `Later` are never high priority and do not justify another round.
If the outline has no phase line, ask the author before reviewing.

## Stage 1. Outline: roles only

For Related Work, stage 1 builds a positioning map instead; see
[Related Work](related-work.md).

The outline fixes structure before any wording exists. It holds **roles, not
sentences**.

**Paragraph line:** `P3 [role] answers: <the reviewer question>`. Roles are
context, requirement, failed approach, question, insight, design, contract,
tradeoff, positioning, evidence, results, and contributions.

**Sentence lines:** `3.1 [role] needs: <evidence>`. Sentence roles are
context, claim, evidence, contrast, definition, consequence, bridge,
question, cost, and scope. "Needs" names the number, figure, or citation the
sentence must carry, with its source. Leave it empty if the sentence needs
none.

**Figure and table blocks:** one block per float, placed after the paragraph
that first cites it. It gives the float's role, not its drawing:

```
FIG:<label> [result | explanation] answers: <the reviewer question>
- takeaway: <the one conclusion a reader should draw from it>
- shows: <the designs, workloads, and metrics compared; the panels, if several>
- explains: <for an explanation figure only: the result it decomposes, and
  whether its parts add up to or multiply to that result>
- why a figure: <why a sentence or a table cannot carry it>
- cited by: <the sentence IDs that cite it>
- needs: <its data source, or "missing experiment">
```

Use `TAB:` for a table.

**The rest of the outline:**
- for a section with subsections, a section-level outline first: the
  reviewer question each subsection answers, and the logic chain, one line
  per subsection. Then one outline per subsection;
- a header with the budget: words per part, and where the section should end
  on the page;
- the logic chain, one line per paragraph, read as a standalone argument;
- the model papers, if any, and which of their role sequences the outline
  follows (see "Model papers by presentation goal" in the skill);
- open issues that the text will not settle;
- from round 2 on, "Changes from round N", mapping each change to the
  finding it answers.

### Stage 1 review brief

Use one reviewer for all rounds of this stage, continuing the same agent.
Ask it to read the manuscript first, then the outline. Ask for:
1. A verdict.
2. Logic jumps, by line ID, each with a fix.
3. Reviewer questions the outline leaves unanswered. Check problem, why
   existing fails, what is new, necessity, evidence, and cost.
4. Evidence that is missing, wrong, or unscoped. Every number checked against
   the manuscript, saying which ones it verified.
5. Figure and table roles. Does each answer one reviewer question with one
   takeaway? Does each sentence that cites a figure point to a panel that
   shows its claim? Is any figure redundant, or any key claim left without
   one?
6. Positioning gaps against related work.
7. A phase-appropriate budget check. In Early, put budget findings in
   `Later`; in Draft, report only gross overruns; in Submission, check the full
   budget.
8. Prioritized changes, each marked high or low priority.

From round 2 on, ask for the change in the verdict, the remaining issues
only, and an explicit "ready / not ready".

If the user asked for the outline, leaving stage 1 means showing it to the
user, not starting stage 2. See "When the user asks for an outline" in the
skill.

## Stage 2. Writing

Write the prose from the final outline, one sentence per sentence line,
unless two lines merge naturally. Then:
- build the document and look at the rendered pages;
- count words per paragraph with a script;
- find where the section ends on the page.

In Draft or Submission, trim to the budget before the review. In Early, leave
length and layout unchanged and put any budget finding in `Later`.

### Stage 2 review brief

Use a fresh reviewer that has not seen stage 1. Ask it to:
1. Read the rendered text first (for example `pdftotext -layout`), so its
   first impression is a reader's.
2. Then read the source, the rest of the paper, and the final outline.
3. Extract the logic chain from the prose itself, one claim per paragraph,
   and compare it with the outline. Each difference is a defect or a
   deliberate change.

Ask for:
- scores from 1 to 5: motivation, novelty as presented, soundness, clarity,
  overall;
- a transition audit: P1 to P2 and so on, each "holds" or a fix;
- problem sentences, quoted, each with a replacement;
- the main weakness a real reviewer would write;
- prioritized changes, each marked high or low priority, that do not make
  the text longer.

In later rounds, tell the reviewer what you applied and what you rejected,
and why. Ask for the change in its scores.

## Stage 3. Rethink and simplify

See [Simplify](simplify.md). Measure the word count before and after.

In Early, simplification is allowed when it clarifies the logic, but word-count
reduction is a `Later` concern. In Draft and Submission, apply the phase's
normal prose and budget priorities.

### Stage 3 review brief

Use a fresh reviewer. Give it the before and after text. Ask:
1. Is anything a reviewer needs now missing: a claim, number, definition,
   cost, or citation?
2. Does the chain still hold at every transition?
3. Which sentences still describe instead of argue, or still say one thing
   twice? Quote each, with a cut or a replacement.
4. Which sentences now read as too compressed to follow?

## Verify, every stage

- Check each finding in the manuscript, the data, or the code. Settle
  factual questions in the source; for example, read the code before stating
  what a baseline keeps in memory.
- Give each finding a verdict: accept, accept in part, or reject, with a
  one-line reason. Record the verdicts so later rounds do not reopen them.
- Reject suggested wording that is better written but less true. For
  example, a claim that holds for only some workloads, or a causal claim no
  measurement shows. Replace it with what is plainly true.
- Decide disagreements between rounds or reviewers by evidence, and say why.

## Exit rule

Leave a stage when either holds:
- 3 rounds are done;
- the last review found no high-priority issue, or every one is fixed.

High priority means:
- a logic jump;
- a wrong or unsupported claim;
- an unanswered reviewer question;
- an undefined term;
- a contradiction with the rest of the paper;
- in Submission, a budget or layout overrun.

If high-priority issues remain after 3 rounds, list them for the user rather
than looping on.
