---
name: git
description: "Local Git conventions to follow whenever working with Git in a repository. Use for any Git operation covered by the rules below, starting with worktrees: creating, placing, listing, or removing a `git worktree`, isolating work on a branch in a separate checkout, or running parallel agents in separate trees. Triggers: git worktree, add a worktree, new worktree, work in a worktree, isolate on a branch, parallel checkout."
---

# Git

Repository-local Git conventions. Each rule: the rule, then the commands that implement it.

## 1. Worktrees live in `.worktree/` inside the repository.

Create every worktree under `<main-repo-root>/.worktree/<name>`, never beside or outside the repository (no `../repo-feature`, no `/tmp/...`).

- **Root is the main worktree**, not the current one. When you are already inside a linked worktree, `git rev-parse --show-toplevel` returns that worktree, which would nest `.worktree/` directories. Use the first entry of `git worktree list` instead.
- **Keep `.worktree/` out of Git** with the repository's local exclude file (`info/exclude` in the common Git directory), so the rule leaves no tracked change. If the project's `.gitignore` already ignores `.worktree/`, leave it as is.
- **Name** the directory after the branch, replacing `/` with `-` (`epic/foo` -> `.worktree/epic-foo`).

```bash
ROOT=$(git worktree list --porcelain | sed -n '1s/^worktree //p')
EXCLUDE="$(git rev-parse --path-format=absolute --git-common-dir)/info/exclude"
mkdir -p "$(dirname "$EXCLUDE")"
grep -qxF '.worktree/' "$EXCLUDE" 2>/dev/null || echo '.worktree/' >> "$EXCLUDE"

BRANCH=epic/foo
DIR="$ROOT/.worktree/${BRANCH//\//-}"
git worktree add -b "$BRANCH" "$DIR"   # new branch from HEAD; drop -b for an existing branch
```

- A new worktree has no gitignored files (env files, local config, `.venv`, `node_modules`, build output). Reinstall or copy what the task needs before building or testing in it.
- Remove with `git worktree remove "$DIR"` (it refuses on uncommitted changes; inspect them before adding `--force`), then `git worktree prune`. Do not `rm -rf` a worktree directory.
- If a tool creates worktrees elsewhere by default, pass it a path under `.worktree/` or create the worktree yourself with the commands above.
