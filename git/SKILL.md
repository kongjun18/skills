---
name: git
description: "Local Git conventions for any Git work in a repository: branch roles, worktrees, merge reminders, and safe history rewriting. Use when creating or naming a branch, finishing an epic, making a talk branch, creating, placing, listing, or removing a `git worktree`, isolating work on a branch in a separate checkout, or running parallel agents in separate trees; and before any `git rebase` or Graphite `gt restack`, or when resolving the conflicts they produce (backup branches and a restore doc first, `--onto` after a parent moves, the additive / base-rename / convergent layering rule). Triggers: new branch, branch naming, epic finished, ready to merge, talk branch, git worktree, add a worktree, new worktree, work in a worktree, isolate on a branch, parallel checkout, rebase, rebase onto main, gt restack, restack the stack, restack branches, fix the stack, resolve rebase or restack conflicts. For GitHub PR review feedback, use address-pr-comments."
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
- **One worktree per branch, and only your own.** Never edit, commit in, or remove another session's worktree. After the user merges a branch, remove its worktree and delete the branch, or keep an `archive/<slug>` tag when the user wants it kept.

## 3. Each branch has one role.

| Branch | Role | Created from | Merged by |
| --- | --- | --- | --- |
| `main` | Shared truth: merged work and shared knowledge (see `repo-memory`) | | |
| `epic/<slug>` | One unit of work: an experiment step, feature, or fix, with its code, results, and notes | `main` | The user |
| `talk/<yyyy-mm>-<slug>` | Output only: slides, demo material, a shared snapshot. May stay unmerged | `main` or an epic | Nobody, unless the user asks |
| `backup/<stamp>/<branch>` | Recovery point before a history rewrite (rule 2) | The branch it backs up | Never |

- **Start each epic from `main`.** Stack an epic on another only when it needs that epic's unmerged code, and record the base branch in the epic's plan or index. Long stacks delay merges, so `main` lags.
- **A talk branch is never the only home of knowledge.** Any fact, framing, or vocabulary decided while preparing output goes to `main` in the same session, per `repo-memory`.
- A repository's `AGENTS.md` may extend the names (for example, step IDs in epic slugs). Follow it.

```bash
git switch main && git pull --ff-only   # when a remote exists
BRANCH=epic/<slug>                     # then create its worktree with rule 1
```

## 4. Agents never merge an epic; they remind the user.

Never merge, squash, or fast-forward an epic into `main` yourself. When an epic's work is finished (its questions answered, its result recorded), remind the user to merge it, in one message:

- the branch name and its base;
- its commits since the base: `git log --oneline main..<branch>`;
- whether its worktree is clean: `git -C <worktree> status --short`;
- the shared-knowledge updates the merge should carry, such as decision records or a research-direction note, named by path, and whether they are already on `main`;
- anything that blocks the merge, such as an unmerged base epic or failing checks.

## 2. Back up before rewriting history; resolve restack conflicts by layering.

Before any `git rebase` or `gt restack`, make the old state recoverable, then rewrite. Read [rebase-restack.md](references/rebase-restack.md) before running the operation; it has the commands, the restore-doc format, and the conflict procedure.

- **Backups first.** Create `backup/<YYYYMMDD-HHMMSS>/<branch>` for every branch the operation will move (one stamp per operation, created without `-f`).
- **Restore doc second.** Record each branch's SHA, Graphite parent, upstream, and the backup prefix in `RESTACK-RESTORE-<YYYYMMDD>.md` at the repository root. Never overwrite an existing one: mark stale sections OUTDATED and append.
- **`--onto` after a parent moves.** Move a child with `git rebase --onto <new-parent-tip> <old-parent-tip> <child>`, never a plain `git rebase <parent>`.
- **Layering rule for conflicts.** Classify each hunk as additive (keep the descendant's), base rename or refactor (take the base's form, update the descendant), or convergent (take the base's copy and drop the empty commit). Use `zdiff3` conflict style so the ancestor is visible.
- **Verify, do not push.** Build and test every restacked tip, check its diff against the new base and against its backup, keep the backup branches, and push only when the user asks.
