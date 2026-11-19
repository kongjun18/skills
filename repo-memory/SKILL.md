---
name: repo-memory
description: Owns repository-local project memory - durable knowledge notes, epic index/status.md/progress.md files, recorded decisions, spec-versus-code conformance conflicts, stale or conflicting notes, and the end-of-task memory closeout. Applies to every task inside a repository; the per-task part is cheap (read before writing, a three-question closeout). Triggers include record this finding, write down the decision, where should this knowledge go, start or continue an epic, update the epic status or progress file, consolidate or compact notes, notes contradict the code, memory closeout, knowledge across parallel worktrees. For exploration write-ups (benchmarks, feasibility studies) use exploration-report; for conversational replies, status or progress updates in chat, and handoffs use high-signal-writing.
---

# Repo Memory

Durable, non-obvious project knowledge lives in the repository, so later sessions and parallel agents read it instead of rediscovering it. This skill decides what is worth keeping, where it goes, and how each topic stays one current, trustworthy view.

## When It Applies

Every task inside a repository. The mandatory part is small: the [Begin](#begin) step, and the [Closeout](#closeout) questions, which for a small task end in one line of the reply. Read a reference only when its trigger in [References](#references) fires.

## Non-Negotiables

1. **One topic, one current note.** Correct a note in place. Never add a note that corrects, supersedes, or comments on another. See [One Current View](#one-current-view).
2. **Intended and observed behavior stay separate.** See [Authority](#authority).
3. **Knowledge status is visible.** A reader can tell verified facts, observations, inferences, hypotheses, proposals, accepted decisions, conflicts, and open questions apart. Never present a guess as a fact or a proposal as accepted.
4. **Stale knowledge is handled, not dropped.** Important stale claims are marked invalid, expired, or superseded in the note that carries them, not silently deleted.
5. **Knowledge follows the revision it describes.** Descriptive knowledge lives on the branch whose code it describes, and an agent writes only inside its own worktree.
6. **No ad hoc memory files.** No `NOTES.md`, `TODO.md`, `scratch.md`, `plan.md`, `progress-*.md`, or task summaries unless the repository defines that path as canonical. Classify content before writing; never create a temporary Markdown file in the repo to sort out later.
7. **Built-in agent memory is a cache.** Vendor or session memory may hold preferences, pointers, and unverified candidates. It is never authoritative and never the only home of a specification, decision, constraint, or reusable finding.
8. **The memory delta is reviewable on its own.** See [Commit Policy](#commit-policy).

## Authority

**Intended behavior.** The current explicit user or maintainer instruction governs the task. An accepted specification says what the system should do. An accepted decision records an authorized choice and may constrain later work. A proposal, draft, note, or agent memory is not accepted because an agent wrote it: an agent may propose a specification or decision, but must not mark it accepted without user or maintainer authority.

**Observed behavior.** Code, tests, configuration, migrations, logs, experiments, and reproducible runtime evidence say what a particular revision does. When they disagree with each other, investigate rather than assume one always wins.

**Notes** are not automatically authoritative. A descriptive claim in a note is a dated, re-checkable observation; a decision or requirement recorded in a note carries only the authority it is labeled with (proposed, or accepted by whom).

**Conformance conflict.** When implementation and specification disagree, record expected behavior, observed behavior, the relevant specification, the evidence, and the open choice (change the implementation or change the specification). Do not silently rewrite either side. Other conflicts: [lifecycle-and-conflicts.md](references/lifecycle-and-conflicts.md).

## Where Things Go

Use the repository's established layout when it has one, including an existing epic `notes/` directory, ADR folder, or specs location; do not migrate it. Otherwise use:

```
AGENTS.md                         root index: commands, links, memory rules
CLAUDE.md                         @AGENTS.md, plus Claude-only additions
docs/specs/                       accepted specifications, labeled drafts
docs/knowledge/                   repo-level knowledge useful across epics
docs/epics/index.md               list of epics
docs/epics/<slug>/index.md        stable entry point
docs/epics/<slug>/status.md       current state
docs/epics/<slug>/progress.md     milestones
docs/epics/<slug>/knowledge/NNN-<topic>.md   one durable topic per note
docs/epics/<slug>/archive/        inactive material
```

Create only what the work needs. An epic is for work that spans multiple tasks, sessions, or parallel workers; a one-turn task usually writes no memory at all.

| Content | Destination |
|---|---|
| Raw reasoning, temporary plans, command output, debugging residue | Chat, terminal, `/tmp`, or ignored scratch space |
| Current epic state, focus, blockers, next steps | `status.md`, replacing stale state |
| Meaningful milestone or direction change | `progress.md` |
| Durable finding, constraint, hypothesis, decision, conflict, open question | The existing note on that topic; a new note only when no note covers the topic |
| Accepted requirement | The specification |
| Knowledge useful beyond one epic | `docs/knowledge/`, indexed |
| Navigation, commands, workflow rules | `AGENTS.md` or an index |
| What the agent did this session | The reply or commit message, not a note |
| Exploration write-up with data | A report, via `exploration-report` |

When the destination is unclear, keep the content out of durable repository docs (in chat, `/tmp`, or ignored scratch space) until it is classified.

## One Current View

Apply this test before every write:

> After this write, can a reader get the current truth on this topic from exactly one `Current View`?

If not, the write scatters the topic; merge instead. In practice:

- **Same topic exists:** edit that note. Replace the dead claim in its `Current View` and add one `Semantic History` line saying what changed, why, and the evidence.
- **Several subtasks are one topic:** one note with a section per subtask, not one note per subtask, task, or session.
- **Split only for size or cadence:** when a part is long enough to hurt readability or changes on its own schedule. The parts then sit under an epic whose `index.md` shows the whole. Choose that container before writing the second note.
- **Two notes on one topic already:** merge them now, or move them under an epic with an index. Flat siblings that cross-link do not resolve the scatter.
- **A new topic invalidates part of an old note:** write the new note, and also remove the dead claim from the old note's `Current View` with a link to the new one.

Note shape, numbering, decisions, and promotion: [epic-layout.md](references/epic-layout.md).

## Begin

Before starting work:

1. Read `AGENTS.md`, `CLAUDE.md`, and any memory rules they link. Note the worktree and branch you are on; the [Commit Policy](#commit-policy) depends on it.
2. If the task belongs to an epic, read its `index.md` and `status.md`. If the work will span sessions and has no epic, create one ([epic-layout.md](references/epic-layout.md#epics)). Read the accepted specifications the task touches.
3. Search the active knowledge for the task's topic, excluding archives, so you work from what is already known and later update the right note:
   ```bash
   rg -i "term|synonym" AGENTS.md CLAUDE.md docs --glob '!**/archive/**'
   # fallback: grep -Rin "term" AGENTS.md CLAUDE.md docs --exclude-dir=archive
   ```
   Search archives only when investigating history or a regression.
4. If the repository provides `memoryctl begin` or an equivalent hook, run it before the first repository write.

Read the smallest relevant current view; do not load every note.

## Closeout

Before reporting completion, answer three questions:

1. **Did anything durable and non-obvious change?** A finding, constraint, decision or proposal, labeled hypothesis worth keeping, invalidated claim, conflict, open question, or epic state. Not what the code or diff already shows, trivial local details, private reasoning, or debugging residue.
2. **Which existing note owns it?** Update that note. Create a note only for a genuinely new topic, and link it from its index.
3. **Is anything now stale?** A claim the work contradicted, a status that is no longer current, a link that broke.

Then:

- **Small task, nothing to record:** one line in the reply, such as `memory: no durable knowledge (typo fix)`. Write no file.
- **Small task with a finding:** edit the owning note and say so in one line, such as `memory: updated <path> (cache is write-through, not write-back)`. Name any claim you invalidated and any proposal that needs the user's approval.
- **Epic work, edits to status, progress, specifications, or several notes, or a conflict that needs authority:** run the full closeout in [closeout-and-validation.md](references/closeout-and-validation.md), including the linter and the review summary.

If the repository provides `memoryctl closeout` and `memoryctl verify` or equivalent hooks, run them for every task, small ones included. Never create a note only to show that closeout ran.

## Commit Policy

Unless the repository or the user says otherwise:

- **In a repository with no docs or memory convention** (shared or company repositories, coauthored papers), on any branch: leave memory changes unstaged and list them for the user.
- **On the main line:** the same; leave them unstaged and list them.
- **On an epic branch, or a task branch under one** (work isolated per `good-agent` §7): commit memory changes with the work, as separate commits whose subject starts with `memory:`, so the user can review, edit, or drop them independently of code commits. Do not mix memory and code in one commit. The user's merge or squash of the epic is the review gate.

Unstaged memory does not reach other worktrees and is lost if the worktree is removed; say so when handing back.

## References

| Read | When |
|---|---|
| [epic-layout.md](references/epic-layout.md) | Creating or editing an epic, its `index.md`/`status.md`/`progress.md`, a knowledge note, a decision, repo-level knowledge, or `AGENTS.md`/`CLAUDE.md` |
| [lifecycle-and-conflicts.md](references/lifecycle-and-conflicts.md) | Knowledge became stale, sources or notes disagree, a specification and the code disagree, or parallel edits to one topic need reconciling |
| [closeout-and-validation.md](references/closeout-and-validation.md) | Closeout for epic work, broader consolidation, validation, the review summary, or wiring memory hooks or CI |
| [worktrees-and-branches.md](references/worktrees-and-branches.md) | Using several worktrees, coordinating parallel branches, merging branch-local notes, or abandoning a worktree |

[`scripts/lint_knowledge.py`](scripts/lint_knowledge.py) checks numbered notes (`NNN-<topic>.md`) wherever they sit, which covers epic `knowledge/`, legacy `notes/`, `docs/knowledge/`, and stray piles, plus relative links in every scanned Markdown file; the full closeout runs it.

## Done

- `AGENTS.md` (and the epic, when relevant) was read, and existing knowledge was searched before any knowledge write.
- Every write passes the one-current-view test, and no ad hoc memory file was created.
- Knowledge status is visible, and stale claims were handled in place.
- Closeout was answered: one line for a small task, the full closeout for epic work.
- Memory changes are in `memory:` commits on an epic branch, or left unstaged and reported.
