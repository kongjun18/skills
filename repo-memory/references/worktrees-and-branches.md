# Worktrees and Branches

Canonical paths are repo-relative, not tied to the physical main worktree.

An agent MUST:

- write only inside its current worktree;
- never directly modify another worktree, including the main worktree;
- keep notes about branch-local implementation on the same branch;
- publish code and descriptive memory through Git commits, PRs, merges, rebases, or cherry-picks;
- avoid treating the main worktree as a shared memory server.

Code and its descriptive note do not need to share one commit. They SHOULD enter the target branch through the same review or merge boundary.

Accepted specifications and decisions MAY be published before implementation to coordinate parallel workers. Their implementation status MUST remain explicit.

## Parallel Work in One Epic

Prefer an epic integration branch:

```text
main
  └── epic/<epic-slug>
        ├── task/<task-a>
        └── task/<task-b>
```

- Task branches keep branch-consistent code and notes.
- The epic branch is the accepted working view.
- Merging a task branch triggers scoped consolidation.
- Prefer a single writer or coordinator for `index.md`, `status.md`, and compacted `progress.md`.
- Concurrent edits to the same topic require semantic reconciliation.
- New-note ID collisions are renumbered during merge.

Other worktrees learn accepted memory by synchronizing Git history, not by reading uncommitted files from another worktree.

## Abandoning a Worktree

Before deleting or abandoning a worktree:

- publish branch-independent durable knowledge through Git;
- preserve unresolved proposals in the appropriate branch; or
- explicitly discard knowledge that only described the abandoned branch.

A failed implementation does not automatically make every investigation finding useless.
