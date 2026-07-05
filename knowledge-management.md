---
name: knowledge-management
description: Manage repo-local knowledge during software development by using AGENTS.md as the root index, aligning CLAUDE.md, maintaining epic docs with status/progress/atomic notes, and preventing scattered temporal scratch notes. Use whenever Codex is working inside a repository, starting or continuing long-running tasks, discovering durable project knowledge, updating repo docs, routing notes/progress, or compacting work into trustworthy project memory.
---

# Repo Memory Steward Skill

## Purpose

This skill teaches an agent how to manage repo-local knowledge during software development.

It treats `AGENTS.md` as the root index for project knowledge and uses epic-level files to track long-running work. The goal is not to create excessive documentation. The goal is to keep useful project knowledge discoverable, current, and trustworthy while the agent iterates on development tasks.

This skill is about general knowledge management and development workflow. It should be active by default whenever the agent is working inside a repository.

## Core Ideas

- `AGENTS.md` is the root index for repo-local knowledge.
- `CLAUDE.md` should link to `AGENTS.md` instead of duplicating separate rules.
- An epic is a large task, similar to a Jira epic, that usually requires multiple tasks, commits, investigations, or iterations.
- Each important epic should have its own directory.
- Each epic should have a stable entry point, a current status file, a progress history, and atomic knowledge notes.
- Knowledge should be easy to discover from indexes.
- Notes should be atomic and useful for future work.
- Do not create ad hoc temporal memory files; route each memory write to the canonical status, progress, notes, repo knowledge, or ignored scratch location.
- The agent must clearly distinguish verified facts from guesses, assumptions, unresolved questions, and accepted decisions.
- Reusable knowledge discovered inside an epic should be promoted to repo-level knowledge when it is useful beyond that epic.

## Default Activation

Always apply this skill during repository work, especially when:

- starting a new development task
- continuing a long-running task
- creating or updating an epic
- discovering project behavior, architecture, constraints, bugs, or risks
- learning something that future agents or developers should know
- updating `AGENTS.md`, `CLAUDE.md`, project docs, or epic docs
- compacting previous work into durable project knowledge

Do not wait for the user to explicitly request knowledge management. Use this skill as part of normal development hygiene.

## Mandatory Write Routing

Before creating or updating any repo note, plan, status, progress, or knowledge file, classify the content and route it. This is a pre-write rule: do not create a temporary markdown file in the repo and classify it later.

- Scratch reasoning, raw logs, temporary plans, and debugging residue: keep in chat/terminal or an ignored scratch path such as `/tmp`; delete it before finishing if it is not needed.
- Current task or epic state: update the epic `status.md`.
- Iteration history: append a concise dated entry to the epic `progress.md`.
- Durable atomic finding, decision, constraint, hypothesis, or unresolved question: create or update one focused file in the epic `notes/` directory after searching existing knowledge.
- Knowledge useful beyond one epic: promote it to an indexed repo-level doc, and link back to the epic note when useful.
- Navigation, rules, or discovery paths: update `AGENTS.md` or an index file; do not place long-form knowledge there.

Do not create ad hoc temporal memory files such as `NOTES.md`, `TODO.md`, `progress-*.md`, `scratch.md`, `plan.md`, or task-summary files in the repo root or feature directories unless that exact path is already linked from `AGENTS.md` or the relevant epic `index.md`.

If a long-running task has no epic yet, create the canonical scaffold under `docs/epics/<epic-slug>/` and index it before writing status, progress, or notes. If the correct destination is unclear, keep scratch outside the repo or in chat until the canonical destination is known. For small one-turn tasks, usually write no memory file unless the work produced durable project knowledge.

## Root Index Rules

### `AGENTS.md`

`AGENTS.md` is the repo-local memory root index.

It should contain:

- project overview or links to project overview
- important project-level indexes
- active epic index or links to active epics
- build, test, lint, and development commands
- agent workflow rules
- links to repo-level knowledge areas
- rules for where durable knowledge should be written

It should not become a knowledge dump. Prefer links over long explanations. Good root index pattern:

```md
# AGENTS.md

- Project overview: `docs/index.md`
- Architecture: `docs/architecture/index.md`
- Epics: `docs/epics/index.md`
- Repo knowledge: `docs/knowledge/index.md`
- Start here for large tasks.
- For epic work, read the epic `index.md`, then `status.md`.
- Use `rg` or `grep` to search existing knowledge before creating new docs.
- Write verified atomic epic knowledge into the epic `notes/` directory.
- Promote reusable cross-epic knowledge to repo-level docs and update the relevant index.
```

### `CLAUDE.md`

If the repository uses `CLAUDE.md`, it should point to `AGENTS.md` instead of maintaining a separate, divergent knowledge system.

Recommended minimal `CLAUDE.md`: `Follow the repo instructions in AGENTS.md.` Claude-specific notes may be added only when they are truly specific to Claude Code behavior. Do not duplicate the main project knowledge rules there.

## Searching Existing Knowledge

Before creating a new note, new topic doc, or new repo-level knowledge entry, search the existing knowledge base.

Prefer `rg` when available:

```bash
rg "keyword|related term" AGENTS.md CLAUDE.md docs
```

Fallback to `grep`:

```bash
grep -R "keyword" AGENTS.md CLAUDE.md docs
```

Use search to:

- avoid duplicate notes
- find related existing knowledge
- identify stale or conflicting information
- decide whether to update an existing note instead of creating a new one
- link new knowledge to existing indexes

If existing knowledge conflicts with code, tests, configs, logs, or explicit user instructions, verify against the source of truth and update or mark stale documentation accordingly.

## Epic Definition

An epic is a large development effort, similar to a Jira epic. It usually contains multiple tasks, requires several iterations, spans multiple files/modules/decisions, may produce reusable project knowledge, and benefits from persistent status and progress tracking. Examples include a payment rewrite, authentication migration, search infrastructure upgrade, onboarding flow redesign, or database schema refactor.

## Epic Directory Structure

Use this structure for long-running epics:

```text
<epic>/
  index.md
  status.md
  progress.md
  notes/
    000-<short-title>.md
    001-<short-title>.md
```

A common location is:

```text
docs/epics/<epic-slug>/
```

For very small epics, `status.md` or `progress.md` may be omitted and summarized in `index.md`. For any epic that will be resumed across multiple iterations, prefer the full structure.

## Epic `index.md`

`index.md` is the epic entry point.

It should explain:

- what the epic is
- the goal
- why it exists
- key files or modules
- where the current status lives
- where progress history lives
- where atomic notes live
- the most important notes or knowledge links

It may contain a small amount of epic-level knowledge if the file remains readable. If the knowledge grows, split it into atomic notes under `notes/` and link to them.

Suggested shape, not a required template:

```md
# Epic: Payment Rewrite

## Overview

This epic rewrites the payment flow to support subscription billing and safer webhook processing.

## Goal

- Support subscription checkout.
- Make webhook processing idempotent.
- Preserve existing one-time payment behavior.

## Start Here

- Current status: `status.md`
- Progress history: `progress.md`
- Atomic notes: `notes/`

## Key Files

- `apps/api/src/billing/`
- `apps/web/src/billing/`
- `tests/billing/`

## Important Notes

- `notes/000-webhook-idempotency.md`: webhook duplicate delivery and idempotency requirements.
```

Keep `index.md` relatively stable. It should not become the main iteration log.

## Epic `status.md`

`status.md` is the current working state of the epic.

It answers:

- where are we now?
- what is the current focus?
- what is blocked?
- what questions are open?
- what should happen next?

Use `status.md` for current state, blockers, current problems, and next steps.

Suggested shape, not a required template:

```md
# Status

Last updated: 2026-06-13

## Current State

The epic is active. The current focus is webhook idempotency and duplicate delivery tests.

## Current Focus

- Verify whether provider event IDs are already stored.
- Add duplicate delivery tests.

## Blockers

- Need migration review before adding a processed events table.

## Open Questions

- Should deduplication happen in the database layer or queue layer?

## Next Steps

1. Search for existing provider event ID storage.
2. Inspect webhook tests.
3. Create or update an atomic note if reusable knowledge is found.
```

Keep `status.md` short and actionable. Update it when the current state changes.

## Epic `progress.md`

`progress.md` is the historical iteration log.

It records:

- what happened over time
- meaningful completed work
- important iteration summaries
- links to notes produced during iterations
- changes to blockers or scope

It should not be used as a durable knowledge dump.

Suggested shape, not a required template:

```md
# Progress

## 2026-06-13

- Inspected billing webhook handler.
- Confirmed duplicate delivery tests were missing.
- Created `notes/000-webhook-idempotency.md`.
- Updated `status.md` with next steps.
```

Periodically compact `progress.md` so it remains useful. Preserve current milestones, important completed work, links to notes, and important historical context. Remove or summarize stale iteration detail.

## Atomic Epic Notes

Use `<epic>/notes/` for durable, atomic epic knowledge.

Each note must:

- focus on one topic
- use the filename format `<ID>-<short-title>.md`
- start IDs at `000`
- increase IDs monotonically
- never reuse old IDs
- use a short kebab-case title
- contain knowledge checked enough to be useful for future work
- be linked from the epic `index.md` when important

Examples:

```text
notes/000-webhook-idempotency.md
notes/001-billing-state-transitions.md
notes/002-refund-scope.md
```

A note is not a scratchpad. Do not store raw reasoning, unfiltered chat history, or random debugging noise.

Notes do not need to follow a fixed section template. Use whatever structure best fits the topic.

## Knowledge Clarity Requirement

This is an agent-level requirement, not a fixed document template.

When writing or updating epic knowledge, the agent must make the knowledge status clear. The exact wording and structure are flexible, but the reader must be able to tell whether a statement is:

- a verified fact
- an observation
- an inference
- a guess or hypothesis
- an accepted decision
- an unresolved question
- an obsolete or superseded idea

The agent must never present an unverified assumption or guess as a verified fact.

Guesses and hypotheses may be recorded when they are valuable, but they must be explicitly described as guesses, hypotheses, or unverified ideas. They should also include enough context for future agents to understand why they were considered worth recording.

For important claims, include enough supporting context, such as:

- code paths
- tests
- configs
- logs
- experiments
- user confirmation
- issues
- PRs
- commits
- related docs

## Sources of Truth

Documentation is a map, not the final authority.

For behavior and implementation details, prefer these sources of truth:

1. current user instruction
2. code
3. tests
4. configs and migrations
5. logs or runtime evidence
6. explicit issue, PR, or commit history
7. repo documentation
8. external or agent memory

If documentation conflicts with code or tests, verify and update the documentation or mark it stale.

## Cross-Epic Knowledge Promotion

Epic work often produces knowledge that is useful beyond the current epic.

When an epic note contains reusable knowledge, promote it to the appropriate repo-level knowledge location.

Repo-level knowledge may live in places such as:

```text
docs/index.md
docs/knowledge/index.md
docs/architecture/index.md
docs/testing/index.md
docs/domain/index.md
```

or a document linked from one of those indexes.

Promote knowledge upward when it is useful for:

- future epics
- future maintenance work
- architecture understanding
- domain understanding
- testing strategy
- deployment or operations
- recurring bug patterns
- long-term project constraints
- important design direction

Promotion should abstract the knowledge for long-term reuse. Do not simply copy raw epic iteration detail into repo-level docs.

When promoting knowledge:

- update the relevant repo-level index
- link from the repo-level knowledge back to the epic note when useful
- link from the epic note to the promoted repo-level knowledge when useful
- preserve knowledge clarity: facts, guesses, decisions, and unresolved questions must remain distinguishable

## Creating or Updating a Note

When the agent learns something potentially useful during epic work:

1. Search existing knowledge using `rg` or `grep`.
2. Decide whether to update an existing note or create a new one.
3. If creating a new note, choose the next monotonically increasing ID.
4. Keep the note focused on one topic.
5. Make the knowledge status clear: verified fact, observation, inference, guess, decision, or open question.
6. Add supporting context when the claim is important.
7. Link important notes from the epic `index.md`.
8. If the knowledge is reusable beyond the epic, promote it to repo-level knowledge and update the relevant repo index.
9. Update `status.md` or `progress.md` if the iteration state changed.

## Updating Epic Status and Progress

At the end of a meaningful iteration:

- update `status.md` with current state, current focus, blockers, open questions, and next steps
- append a concise entry to `progress.md` if meaningful work occurred
- create or update atomic notes for durable knowledge
- link new important notes from `index.md`
- promote cross-epic knowledge upward when useful

Do not turn `status.md` into history. Do not turn `progress.md` into a knowledge dump. Do not turn `notes/` into raw scratch space.

## Compacting

Long-running epics should be compacted periodically.

Compact when:

- `progress.md` becomes long or hard to scan
- status information is stale
- notes contain overlapping knowledge
- the epic has completed, paused, or changed direction

Compacting means:

- summarize stale iteration detail
- preserve important milestones
- preserve links to important notes
- update `status.md` to the current state
- mark obsolete knowledge clearly instead of silently deleting important context
- promote reusable knowledge to repo-level docs if it has not already been promoted

## Minimalism Rules

Avoid over-documenting.

Do record:

- durable project knowledge
- non-obvious system behavior
- important constraints
- validated findings
- useful hypotheses with clear status
- decisions or design direction
- blockers and current status for long-running epics
- cross-epic reusable knowledge

Do not record:

- trivial implementation details
- raw chain-of-thought or private reasoning
- noisy debugging output
- temporary task chatter
- obvious facts visible from a small local code snippet
- unsupported guesses written as facts
- duplicate knowledge that should update an existing note

## Completion Checklist

Before finishing a repo task, the agent should check:

- Was every repo memory or documentation write classified before creating or updating the file?
- Did the current state of an epic change?
- Should `status.md` be updated?
- Should `progress.md` get a concise iteration entry?
- Did this work produce durable knowledge?
- Should an atomic note be created or updated?
- Did the agent search existing knowledge before creating new knowledge?
- Is any note linked from the epic `index.md` if important?
- Did the work produce knowledge useful beyond this epic?
- If yes, was it promoted to repo-level knowledge and indexed?
- Are verified facts, guesses, decisions, and open questions clearly distinguished?
- Is any stale knowledge marked or corrected?

## One-Sentence Summary

Use `AGENTS.md` as the repo knowledge root; use each epic's `index.md` as its entry point, `status.md` for the current state, `progress.md` for history, and `notes/` for atomic durable knowledge; promote reusable epic knowledge upward into repo-level docs and keep every important claim's knowledge status clear.
