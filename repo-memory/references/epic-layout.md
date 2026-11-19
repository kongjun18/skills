# Epic Layout and Knowledge Notes

Read when creating or editing an epic, its files, a knowledge note, a decision, repo-level knowledge, or the root files. The canonical tree and the write-routing table are in [SKILL.md](../SKILL.md#where-things-go).

## Root Files

**`AGENTS.md`** is the memory root. Keep it short and navigational, with links rather than explanations:

- project overview links;
- build, test, lint, and development commands;
- links to specifications and repo-level knowledge;
- links to active epics (or to `docs/epics/index.md`);
- the memory workflow and where durable knowledge belongs.

**`CLAUDE.md`**, when Claude Code is used, should contain `@AGENTS.md` plus only truly Claude-specific rules. It does not restate the memory system.

## Directory Roles

- `docs/specs/`: accepted specifications, and drafts labeled as drafts.
- `docs/knowledge/`: repo-level knowledge useful across epics, with an `index.md`.
- `docs/epics/index.md`: one line per epic, linking its `index.md`.
- `docs/epics/<slug>/knowledge/`: the epic's atomic topic notes. Named `knowledge/` so nobody reads it as temporary notes. A repository that already uses `notes/` keeps it; do not keep both in one epic.
- `docs/epics/<slug>/archive/`: inactive material kept for context. `archive/` is a location, not a status: archived content already says whether it is superseded, expired, invalid, or completed, and indexes do not list it as current.

## Epics

Create an epic only for work that spans multiple tasks, commits, sessions, modules, or parallel workers and benefits from persistent state. When long-running work has no epic, create the smallest useful scaffold and list it in `docs/epics/index.md` before writing epic memory.

**`index.md`** is the stable entry point. It answers: what the epic is and why it exists, its goal and scope, which modules matter, where status and progress live, and which notes matter most. Link notes rather than copying their content; keep it stable rather than using it as a log.

**`status.md`** is the current working state. It answers: where the work is now, the current focus, what is blocked, which questions are open, and what happens next. Start it with `Last updated: YYYY-MM-DD`. Keep it short and replace stale state instead of accumulating history.

**`progress.md`** is the milestone view: dated entries for meaningful completed work, direction changes, blocker changes, and links to important notes. Do not record every command, turn, or debugging step. Compact older entries into milestones when the file becomes hard to scan.

## Knowledge Notes

A note holds durable knowledge about one stable topic. A topic may hold many findings; one finding per note is fragmentation, not atomicity. A note is not a task transcript or scratchpad.

### Numbering

- Name notes `<ID>-<short-kebab-topic>.md`, with a three-digit ID.
- Each epic has its own sequence starting at `000`; different epics reuse the same IDs freely.
- IDs increase monotonically within an epic and are never reused, including archived or deleted IDs. Check active and archived notes before choosing the next one.
- Parallel branches may pick the same next ID; resolve that at merge ([worktrees-and-branches.md](worktrees-and-branches.md#parallel-work-in-one-epic)).

### Shape

```markdown
# <Topic>

## Current View
Current facts, constraints, decisions, conflicts, and open questions,
each with its status visible (verified, hypothesis, proposed, accepted).

## Evidence
Code paths, tests, configs, migrations, commits, issues, experiments,
logs, or user confirmation that let a reader recheck the claims.

## Semantic History
- YYYY-MM-DD: one line per important change in understanding.
```

The headings are optional; what is not optional is that the current conclusion is easy to find and that facts, guesses, proposals, and accepted decisions are distinguishable. Do not require frontmatter or a schema unless tooling needs it.

**Log and view.** Git history is the complete change log. `Current View` is the normal read path. `Semantic History` records only important invalidations, expirations, supersessions, accepted or reversed decisions, resolutions, and scope changes; it does not repeat ordinary Git history. `status.md`, `progress.md`, and indexes are compact views, not logs. A closeout summary records what an agent did; it is not project knowledge. Never keep two independently current versions of one claim.

**Evidence.** For important claims, keep enough context to recheck them. Link or summarize logs; do not paste large raw output.

**Semantic History entries** are one line by default:

```markdown
- 2026-09-12: "cache is write-back" invalidated; it is write-through
  (`src/cache.c:220`). The earlier measurement came from a branch that never landed.
```

Keep the original reasoning at greater length only when the mistake itself is instructive, such as a recurring trap or a reverted change that would otherwise be reattempted.

## Decisions

A decision is an authorized choice among meaningful alternatives that constrains later work. Record:

- the question and the alternatives;
- the outcome;
- proposed or accepted, and who accepted it;
- the rationale;
- scope and consequences;
- a revisit condition, when useful.

Record a local epic decision in the relevant topic note. Promote it to an ADR or dedicated decision record only when it is long-lived, cross-cutting, expensive to reverse, formally reviewed, or likely to outlive the epic. When an accepted decision changes an accepted requirement, update the specification once authorized, so two divergent current truths never coexist.

## Promotion to `docs/knowledge/`

Promote knowledge that is useful beyond the epic: architecture behavior, domain rules, test or deployment practice, recurring failures, long-term constraints, accepted cross-cutting decisions. To promote:

1. update the canonical repo-level document, abstracting away temporary epic detail;
2. update `docs/knowledge/index.md` (or the relevant index);
3. link the epic note and the repo-level document when useful.

The repo-level document becomes the shared current view; the epic note keeps local evidence and context and does not maintain a second copy of the current claim.
