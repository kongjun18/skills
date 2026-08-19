---
name: repo-memory
description: Mandatory repo-local memory protocol for repository work. Use before the first repo write and before reporting completion, especially for long-running tasks, Git worktrees, parallel agents, specifications, status, progress, decisions, conflicts, and durable knowledge.
---

# Repo Memory Steward

## Purpose

Keep repository knowledge reusable by any agent, readable by humans, consistent with the code revision it describes, and small enough to review.

Apply this skill to every task performed inside a repository.

A task MAY produce no memory changes, but it MUST still run closeout and record a reason for the no-op.

## Non-Negotiable Rules

1. Accepted specifications describe what the system should do.
2. Code, tests, configuration, migrations, and reproducible evidence describe what the current revision does.
3. Notes preserve useful knowledge but are not automatically authoritative.
4. A specification/implementation mismatch is an explicit conformance conflict.
5. Facts, hypotheses, proposals, accepted decisions, conflicts, and stale claims MUST be distinguishable.
6. Important stale knowledge MUST be invalidated, expired, or superseded rather than silently deleted.
7. Durable descriptive knowledge MUST follow the branch and revision it describes.
8. An agent MUST modify only its current worktree.
9. Every completed task MUST run a scoped, idempotent memory closeout.
10. The user MUST be able to review both the repo delta and the memory delta.

## Authority

Keep intended behavior separate from observed behavior.

### Intended behavior

- Current explicit user or maintainer instruction has the highest authority for the task.
- An accepted specification is authoritative for what the system should do.
- An accepted decision explains an authorized choice and may constrain later work.
- A proposal, draft, note, or agent memory is not accepted merely because an agent wrote it.

An agent MAY propose a specification or decision. It MUST NOT mark it accepted without the required user or maintainer authority.

### Observed behavior

Use code, tests, configs, migrations, logs, experiments, and reproducible runtime evidence to determine what a particular revision actually does. Investigate disagreements among these sources instead of assuming one is always correct.

Built-in or external agent memory is never authoritative.

### Conformance conflict

When implementation and specification disagree, record:

- expected behavior;
- observed behavior;
- the relevant specification;
- supporting evidence;
- the unresolved choice: change implementation or change specification.

Do not silently rewrite either side.

## Log-and-View Model

Use a lightweight log-centric model:

- Git history is the complete file-change log.
- A note's `Current View` is the normal read path for current knowledge.
- A note's `Semantic History` records only important changes in understanding.
- `status.md`, `progress.md`, and indexes are compact views, not raw logs.
- A closeout summary or tooling receipt records what the agent did; it is not durable project knowledge.

Do not maintain two independently authoritative versions of the same claim. `Current View` is current; `Semantic History` explains important invalidations, supersessions, accepted decisions, and resolutions. It MUST NOT duplicate ordinary Git history.

## Canonical Layout

Use the repository's established structure when one exists. Otherwise prefer:

```
AGENTS.md
CLAUDE.md
docs/
  specs/
  knowledge/
  epics/
    index.md
    <epic-slug>/
      index.md
      status.md
      progress.md
      notes/
        000-<short-title>.md
        001-<short-title>.md
      archive/
```

Only create directories that are needed.

- `AGENTS.md`: root index and mandatory workflow.
- `CLAUDE.md`: imports `AGENTS.md`; only Claude-specific additions belong here.
- `docs/specs/`: accepted specifications and clearly labeled drafts.
- `docs/knowledge/`: durable knowledge useful across epics.
- epic `index.md`: stable entry point.
- epic `status.md`: current working state.
- epic `progress.md`: concise milestone history.
- epic `notes/`: atomic durable knowledge.
- epic `archive/`: inactive material retained for context.

`archive/` is a location, not a semantic status. Archived content should already say whether it is superseded, expired, invalid, completed, or otherwise inactive.

## Root Files

### `AGENTS.md`

Treat `AGENTS.md` as the repository memory root. Keep it short and navigational. It SHOULD include:

- project overview links;
- build, test, lint, and development commands;
- links to specifications and durable knowledge;
- active epic links;
- the mandatory memory workflow;
- rules for where durable knowledge belongs.

Prefer links over long explanations. Do not turn it into a knowledge dump.

### `CLAUDE.md`

When Claude Code is used, prefer:

```markdown
@AGENTS.md
```

Add only truly Claude-specific rules. Do not duplicate the repository memory system.

### Built-in agent memory

Treat vendor-specific memory as a local cache or candidate inbox. It MAY contain local preferences, shortcuts, pointers, and unverified candidates. It MUST NOT be the only location of an accepted specification, decision, constraint, or reusable finding.

## Epics

An epic is work that spans multiple tasks, commits, investigations, sessions, modules, or parallel workers and benefits from persistent status and knowledge.

Do not create an epic for every small change. For a small one-turn task, usually write no memory unless it produces durable non-obvious knowledge.

When long-running work has no epic, create and index the smallest useful scaffold before writing epic memory.

### Epic `index.md`

The stable entry point. It answers:

- what the epic is and why it exists;
- its goal and scope;
- where status and progress live;
- which modules matter;
- which notes are important.

Keep it stable. Link to notes instead of copying their contents.

### Epic `status.md`

The current working state. It answers:

- where are we now;
- what is the current focus;
- what is blocked;
- which questions remain open;
- what should happen next.

Keep it short. Replace stale state rather than accumulating history.

### Epic `progress.md`

The human-readable milestone view. Record meaningful completed work, major direction changes, blocker changes, and links to important notes.

Do not record every command, agent turn, or debugging action. Compact older entries into milestones when the file becomes hard to scan.

## Mandatory Write Routing

Classify content before writing it:

- Raw reasoning, temporary plans, command output, and debugging residue: chat, terminal, `/tmp`, or ignored scratch space.
- Current epic state, focus, blockers, and next steps: `status.md`.
- Meaningful milestones: `progress.md`.
- Durable finding, constraint, hypothesis, decision, conflict, or open question: an atomic note.
- Accepted requirement: canonical specification location.
- Knowledge useful beyond one epic: indexed repo-level knowledge.
- Navigation and workflow: `AGENTS.md` or an index.
- Agent activity review: closeout output or a tooling-generated receipt, not a knowledge note.

Do not create ad hoc root or feature files such as `NOTES.md`, `TODO.md`, `scratch.md`, `plan.md`, `progress-*.md`, or task summaries unless the repository explicitly defines them as canonical.

If the correct destination is unclear, keep the content outside durable repo docs until it is classified.

## Atomic Notes

A note is durable knowledge about one stable topic. It is not a task transcript or scratchpad.

### Numbering and naming

Each epic has an independent sequence:

- Start at `000` in every epic.
- Increase monotonically within that epic.
- Never reuse an ID, including archived or deleted IDs.
- Different epics MAY each contain `000`, `001`, and the same later IDs.
- IDs only need to be unique within one epic.
- Use `<ID>-<short-kebab-title>.md`.
- Keep one stable topic per note.

Inspect active and archived notes before choosing the next ID.

Parallel branches from the same epic revision may choose the same next ID. Resolve that mechanical collision during merge by renumbering one new note. An ID collision is not itself a semantic conflict.

### Search before writing

Before creating a note, specification, ADR, or repo-level document, search active knowledge:

```bash
rg "keyword|related term" AGENTS.md CLAUDE.md docs --glob '!**/archive/**'
```

Fallback:

```bash
grep -R "keyword" AGENTS.md CLAUDE.md docs --exclude-dir=archive
```

Use search to avoid duplicates, find related specifications and decisions, update an existing topic, detect stale claims, and choose the correct destination. Search archives only when investigating history or regressions.

### Recommended shape

```markdown
# Topic

## Current View

Current facts, constraints, decisions, conflicts, and open questions.

## Evidence

Relevant code, tests, configs, migrations, commits, issues,
experiments, logs, or user confirmation.

## Semantic History

Only important invalidations, expirations, supersessions,
accepted or reversed decisions, resolutions, and scope changes.
```

The exact headings are optional. The current conclusion MUST be easy to find. Facts MUST NOT be confused with guesses, and proposals MUST NOT be confused with accepted decisions.

Do not require frontmatter or a complex schema unless tooling needs it. Human readability is the default.

### Evidence

For important claims, preserve enough context to recheck them, such as code paths, tests, configs, migrations, commands, commits, issues, experiments, logs, or explicit user confirmation.

Do not copy large raw logs into notes. Link or summarize the relevant evidence.

## Decisions

A decision is an authorized choice among meaningful alternatives that constrains later work.

A useful decision states:

- the question or alternatives;
- the chosen outcome;
- whether it is proposed or accepted;
- who or what authority accepted it;
- the rationale;
- its scope and consequences;
- a revisit condition when useful.

Record a local epic decision in the relevant topic note by default.

Promote it to an ADR or dedicated decision record only when it is long-lived, cross-cutting, expensive to reverse, formally reviewed, or likely to outlive the epic.

When an accepted decision changes an accepted requirement, update the specification after authorization. Do not leave two divergent current truths.

## Knowledge Lifecycle

Use these meanings for a note or individual claim:

- `active`: currently usable in its stated scope;
- `disputed`: credible claims or evidence conflict and resolution is pending;
- `superseded`: replaced by newer knowledge or a newer decision;
- `expired`: formerly valid, but only for an older revision, version, or context;
- `invalid`: disproved, mistaken, or unsupported from the start.

When knowledge becomes stale:

1. classify it correctly;
2. remove the inactive claim from the current conclusion;
3. record why it changed and cite evidence;
4. link the replacement when one exists;
5. update active files that depended on it;
6. archive only when it is no longer needed for active navigation.

Do not silently delete important context. Do not keep contradictory old and new claims together in `Current View` unless they are explicitly marked disputed.

## Conflict Handling

Do not use last-write-wins for semantic conflicts.

- Same claim and scope: consolidate duplicates.
- Overlapping claims: merge into one clearer current view.
- Different scopes or versions: state each scope explicitly.
- Old claim was wrong: mark invalid.
- Old claim was once true: mark expired.
- New knowledge or choice replaced it: mark superseded.
- Evidence remains inconclusive: mark disputed.
- Specification differs from implementation: record a conformance conflict.

If resolution requires user or maintainer authority, preserve the conflict and list it in closeout instead of inventing a decision.

## Cross-Epic Promotion

Promote knowledge when it is useful beyond the current epic, such as architecture behavior, domain rules, test or deployment practices, recurring failures, long-term constraints, or accepted cross-cutting decisions.

When promoting:

1. update the canonical repo-level document;
2. abstract away temporary epic detail;
3. update the relevant index;
4. link the epic note and repo-level document when useful;
5. avoid maintaining two divergent copies of the same current claim.

The repo-level document becomes the shared current view. The epic note keeps local evidence and context.

## Worktrees and Branches

Read [Worktrees and Branches](references/worktrees-and-branches.md) before using multiple worktrees, coordinating parallel branches, merging branch-local notes, or abandoning a worktree.

Always write only inside the current worktree and keep descriptive knowledge on the branch containing the revision it describes.

## Required Workflow

### Begin

Before the first repo write:

1. Read `AGENTS.md` and repo-specific instructions.
2. Identify the current worktree, branch, task, and relevant epic.
3. Read the epic `index.md` and `status.md`, when present.
4. Read relevant accepted specifications.
5. Search active notes and repo-level knowledge, excluding archives.
6. Create an epic scaffold only when the work is truly long-running.
7. If the repo provides `memoryctl begin` or an equivalent hook, run it.

Read the smallest relevant current view first. Do not load every note by default.

### During work

- Keep scratch and raw operational logs outside durable docs.
- Preserve evidence paths for important claims.
- Do not publish hypotheses as facts.
- Update an existing topic instead of creating a task-specific duplicate.
- Keep branch-local implementation knowledge on its branch.

### Closeout

Every completed task MUST run this scoped, idempotent pipeline:

1. **Inspect the delta:** code, tests, configs, migrations, and docs.
2. **Extract semantic changes:** findings, decisions, invalidations, conflicts, constraints, and questions.
3. **Classify:** normative or descriptive; verified or unverified; local, epic-wide, or cross-epic.
4. **Search and reconcile:** update existing knowledge, remove duplication, and expose unresolved conflicts.
5. **Publish the smallest correct memory delta:** notes, specs, status, progress, and indexes.
6. **Compact the touched scope:** remove inactive claims from current views and archive only when appropriate.
7. **Validate:** structure, links, authority, branch consistency, and stale claims.
8. **Report:** summarize the repo delta and memory delta separately.
9. If provided, run `memoryctl closeout` and `memoryctl verify` or equivalent commands.

A closeout MAY be a no-op when no durable, non-obvious knowledge changed or existing memory already describes the result. State the concrete reason. Do not create a note merely to prove closeout ran.

## Consolidation and Compaction

Every task performs scoped closeout. Do not reorganize the entire knowledge tree after every task.

Run broader consolidation when:

- an epic is merged, completed, paused, or changes direction;
- progress or indexes become hard to scan;
- notes contain repeated or overlapping claims;
- conflicts accumulate;
- inactive material dominates active knowledge;
- a user or maintainer requests it.

Broader consolidation may reconcile conflicts, deprecate stale claims, merge redundant notes, split mixed topics, promote cross-epic knowledge, compact progress, and improve the touched epic's structure.

Preserve stable links when practical. Avoid broad filesystem churn without clear benefit.

## Validation

Before reporting completion, verify the touched scope:

- relevant active knowledge was searched;
- note IDs are unique and monotonic within each epic;
- important links resolve;
- archived files are not indexed as current truth;
- inactive claims are absent from unlabeled current views;
- accepted decisions and specifications have appropriate authority;
- proposals remain labeled as proposals;
- conformance conflicts remain explicit;
- descriptive notes match the branch revision they describe;
- status is current rather than historical;
- progress contains milestones rather than raw activity;
- promoted knowledge is indexed;
- closeout produced a real memory delta or a justified no-op.

## Human Review

At closeout, present:

```
Code changes
Validation and tests
Memory changes
Invalidated, expired, or superseded knowledge
Conflicts and open questions
Proposals requiring approval
No-op reason, when no memory changed
```

Separate evidence from interpretation. Git diff, tests, hooks, or a tooling-generated receipt show what the agent did. Notes preserve reusable understanding.

## Enforcement

A skill defines policy and procedure. It is not by itself a deterministic enforcement boundary.

Repos that require hard enforcement SHOULD provide shared commands, hooks, or CI, for example:

```
memoryctl begin
memoryctl closeout
memoryctl verify
```

When such a mechanism exists:

- `begin` MUST run before the first repo write;
- `closeout` MUST run after the final intended change;
- `verify` MUST pass before reporting completion;
- any later repo change invalidates the previous verification;
- hooks or CI SHOULD reject missing or stale closeout state.

Put bootstrap enforcement in repo or organization configuration, not only inside this skill. Otherwise an agent that never activates the skill can bypass skill-local hooks.

A minimal `AGENTS.md` rule is:

```markdown
Before the first repository write, use the repo-memory skill and run the
memory begin step. Before reporting completion, run scoped closeout and
verification. A justified no-op is valid; skipping closeout is not.
```

Enforce observable outcomes, not claims about an agent's private reasoning.

## Minimalism

Record durable non-obvious knowledge, accepted requirements and decisions, important constraints, validated findings, useful labeled hypotheses, unresolved material conflicts, current state, and meaningful milestones.

Do not record private reasoning, raw transcripts, noisy debugging output, temporary chatter, trivial local details, unsupported guesses as facts, duplicate current knowledge, or one new note per task.

The goal is the smallest trustworthy memory that prevents rediscovery and misalignment.

## Completion Checklist

- [ ]  Repo and epic instructions were read.
- [ ]  Active knowledge was searched before creating new knowledge.
- [ ]  Intended and observed behavior were kept separate.
- [ ]  Durable findings were routed to the correct canonical location.
- [ ]  Facts, hypotheses, proposals, decisions, conflicts, and questions are distinguishable.
- [ ]  Stale claims were invalidated, expired, or superseded.
- [ ]  Notes remain consistent with the current branch revision.
- [ ]  Note numbering starts at `000` and is monotonic within each epic.
- [ ]  `status.md`, `progress.md`, and indexes contain only their intended views.
- [ ]  Cross-epic knowledge was promoted and indexed when appropriate.
- [ ]  Scoped closeout ran and validation passed, or a justified no-op was recorded.
- [ ]  The user can review both the repo delta and memory delta.

## One-Sentence Summary

Use `AGENTS.md` as the root index; accepted specifications for intended behavior; branch-consistent atomic notes for durable knowledge; `Current View` for what is usable now; `Semantic History` for important changes; Git for publication across worktrees; and mandatory scoped closeout plus verification before completion.
