# Worktrees and Branches

Read before using several worktrees, coordinating parallel branches, merging branch-local notes, or abandoning a worktree. Canonical memory paths are repo-relative, not tied to the physical main worktree.

An agent:

- writes only inside its current worktree and never modifies another worktree, with one exception: the path-limited shared-knowledge commit to the main line from the main checkout, in repositories that opt in ([commit policy](../SKILL.md#commit-policy));
- keeps knowledge about branch-local implementation on that branch;
- publishes code and descriptive memory through Git (commits, PRs, merges, rebases, cherry-picks), following the [commit policy](../SKILL.md#commit-policy);
- does not treat any worktree's uncommitted files as shared memory; shared knowledge is shared only once it is committed on the main line.

Code and its descriptive note need not share one commit, but they should reach the target branch through the same review or merge boundary.

Accepted specifications and decisions may be published before implementation to coordinate parallel workers; their implementation status stays explicit.

## Parallel Work in One Epic

Prefer an epic integration branch:

```text
main
  └── epic/<epic-slug>
        ├── task/<task-a>
        └── task/<task-b>
```

- Task branches carry branch-consistent code and knowledge notes.
- The epic branch is the accepted working view; merging a task branch into it triggers scoped consolidation.
- Prefer a single writer or coordinator for `index.md`, `status.md`, and compacted `progress.md`.
- Concurrent edits to one topic need semantic reconciliation ([lifecycle-and-conflicts.md](lifecycle-and-conflicts.md)), not last write wins.
- Two branches that picked the same next note ID are a mechanical collision, not a semantic conflict: renumber one new note at merge. `lint_knowledge.py` reports the collision as `duplicate-id`.

Other worktrees learn accepted memory by synchronizing Git history, not by reading uncommitted files in another worktree.

## Abandoning a Worktree

Before deleting or abandoning a worktree:

- publish branch-independent durable knowledge through Git;
- keep unresolved proposals on an appropriate branch; or
- explicitly discard knowledge that only described the abandoned branch;
- tell the user about memory changes the commit policy left unstaged, since removing the worktree loses them.

A failed implementation does not make every investigation finding useless.
