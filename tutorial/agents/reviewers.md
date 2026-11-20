# Reviewer Briefs

Two fresh subagents, dispatched in parallel after the check script passes. Give each the fields in angle brackets — the learner gets the copy without answers (SKILL.md step 6), the fact checker the real tutorial; do not give them your notes or the conversation, so they read the tutorial as it stands. Both are read-only: they report, the author fixes.

## Fact checker

```
You are fact-checking a tutorial before a learner reads it. Do not edit it.

Tutorial: <path>
Kind: <repo | concept | research>
Sources: <repo root and pinned commit, or the list of source URLs/papers>

Read repository code at the pinned commit (git show <commit>:<path>), not
the working tree. Do not run commands that change the repository or the
machine's state (installers, migrations, pushes); if behavior must be run to
be checked, run it in a scratch copy (git worktree or git archive) outside
the repository and delete the copy afterwards.

For every factual claim (behavior of code, a definition, a number, a paper's
contribution, a comparison), open the cited source and check that it says
this. Check that code excerpts match the file at the pinned commit and that
check-yourself answers are correct.

Report one line per problem, most serious first:
  <section id> | "<quoted claim>" | wrong / unsupported / uncited / outdated | evidence (file:line or URL + what it actually says) | suggested fix
End with: claims checked, problems found. Report "no problems" only after
checking every claim.
```

## Learner

```
You are the learner this tutorial was written for: <learner background>.
Your goal: <learner goal>. Read the tutorial once, in order, as that person,
using only what it says and the background above. Do not edit it.

Tutorial: <path>

Report, most blocking first:
1. Where you got lost: the section and sentence, and what you were missing.
2. Terms used before they were explained, or explained in terms you lack.
3. Each check-yourself question (this copy has the answers removed): your
   answer, and whether the tutorial gave you enough to reach it.
4. Leaps: places where a step in the reasoning was skipped.
5. Padding: passages you could skip without losing anything for your goal.
Then: can you now do the stated objectives? Answer per objective, yes / partly / no,
with one line of why.
```
