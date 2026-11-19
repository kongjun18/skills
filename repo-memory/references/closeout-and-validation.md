# Full Closeout, Validation, and Enforcement

Read for closeout on epic work, or whenever a task edited status, progress, specifications, or several notes, or left a conflict that needs authority. Small tasks use the one-line closeout in [SKILL.md](../SKILL.md#closeout).

## Full Closeout

Scoped to what the task touched, and idempotent: running it twice changes nothing.

1. **Inspect the delta:** code, tests, configs, migrations, and docs.
2. **Extract semantic changes:** findings, decisions, invalidations, conflicts, constraints, open questions.
3. **Classify each:** normative or descriptive; verified or unverified; local, epic-wide, or cross-epic.
4. **Search and reconcile:** update the owning notes, remove duplication, and expose unresolved conflicts ([lifecycle-and-conflicts.md](lifecycle-and-conflicts.md)).
5. **Publish the smallest correct memory delta:** notes, specifications, `status.md`, `progress.md`, indexes. Most closeouts edit existing notes and add none.
6. **Compact the touched scope:** remove inactive claims from current views; archive only when appropriate.
7. **Validate:** the checklist below, including the linter.
8. **Report:** the review summary below, with the repo delta and the memory delta separate.
9. **Run repository hooks:** `memoryctl closeout` and `memoryctl verify`, or their equivalents, when the repository provides them.

## Broader Consolidation

A normal closeout does not reorganize the knowledge tree. Consolidate an epic more broadly when it is merged, completed, paused, or changes direction; when progress or indexes are hard to scan; when notes repeat or overlap; when conflicts accumulate; when inactive material crowds out active knowledge; or when a user or maintainer asks. Consolidation may reconcile conflicts, retire stale claims, merge redundant notes, split mixed topics, promote cross-epic knowledge, and compact progress. Preserve stable links where practical and avoid churn without a clear benefit.

## Validation Checklist

Run the linter over the touched scope:

```bash
python3 <skill-dir>/scripts/lint_knowledge.py docs/epics/<slug>   # or docs
```

It exits 1 on findings and 2 when the path is missing or holds no Markdown at all. It reports pointer-only and empty notes, duplicate title stems, reused IDs (including archived ones), an epic with both `knowledge/` and `notes/`, flat piles without an index, and broken relative links. It skips ADR folders (`adr/`, `adrs/`, `decisions/`), whose superseded-by links are their convention. It cannot tell whether two differently named notes cover one topic, so a clean run is necessary, not sufficient. Then check by reading:

- active knowledge was searched before anything new was created;
- note IDs are unique within each epic and were assigned in increasing order;
- each topic has exactly one `Current View`; corrections edited the owning note;
- inactive claims are absent from unlabeled current views, and archived files are not indexed as current;
- accepted specifications and decisions carry the required authority; proposals stay labeled as proposals;
- conformance conflicts remain explicit;
- descriptive notes match the branch revision they describe;
- `status.md` is current, not historical; `progress.md` holds milestones, not activity;
- promoted knowledge is indexed;
- the closeout produced a real memory delta or a stated no-op.

## Review Summary

Present at the end of epic work, omitting empty sections:

```
Code changes
Validation and tests
Memory changes                     (paths; commits, or unstaged)
Invalidated, expired, or superseded knowledge
Conflicts and open questions
Proposals requiring approval
No-op reason, when no memory changed
```

Separate evidence from interpretation: the Git diff, tests, and hook receipts show what the agent did; notes preserve reusable understanding.

## Enforcement

A skill states policy; it is not an enforcement boundary. A repository that needs hard enforcement provides shared commands, hooks, or CI, for example `memoryctl begin`, `memoryctl closeout`, and `memoryctl verify`. When it does:

- `begin` runs before the first repository write;
- `closeout` runs after the final intended change;
- `verify` passes before completion is reported, and any later repository change invalidates it;
- hooks or CI reject missing or stale closeout state.

Put bootstrap enforcement in repository or organization configuration, not only in this skill; otherwise an agent that never loads the skill bypasses it. A minimal `AGENTS.md` rule:

```markdown
Before the first repository write, use the repo-memory skill's begin step.
Before reporting completion, answer its closeout questions; a one-line
"no durable knowledge" is a valid closeout, skipping it is not.
```

Enforce observable outcomes, not claims about an agent's private reasoning.
