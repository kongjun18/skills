---
name: rebase-restack
description: "Safely rebase a branch or restack a Graphite stack (`gt restack`), and resolve the conflicts it produces. Always writes a restore doc capturing the pre-operation branch/SHA state first, so the stack can be recovered if the rebase/restack goes wrong; includes the layering rule for resolving restack conflicts (additive vs base-rename vs convergent) and using `-onto` after a parent is rewritten. Triggers: rebase, gt restack, restack the stack, restack branches, rebase onto main, fix the stack, resolve restack/rebase conflicts, restack conflict."
---

# Rebase / Restack

Workflow for running a `git rebase` or `gt restack` safely. Rebasing and restacking rewrite history and move multiple branches at once — a mistake can leave the stack in a state that is hard to recover by hand. This skill makes every such operation recoverable by writing a **restore doc** first.

## When to Use

- User asks to `git rebase` a branch (onto `main`, another branch, or interactively).
- User asks to `gt restack`, restack a Graphite stack, or fix a stack after amending an earlier commit.
- Any operation that amends/reorders commits in a stack or moves dependent branches.

## The Rule: timestamped backup branches + restore doc before any rebase / `gt restack`

**Create timestamped backup branches first, then write a restore doc**, so the pre-operation state can be recovered if the rebase/restack goes wrong.

1. **Create a timestamped backup branch for every branch you are about to rewrite** (the current branch and every descendant a restack will move). This is the primary recovery mechanism — a branch, so it shows in `git branch` and restore is a plain `git branch -f` by name, no SHA lookup needed.
    - **Naming convention:** `backup/<YYYYMMDD-HHMMSS>/<original-branch-name>`, where the timestamp is one shared value for the whole operation (`STAMP=$(date +%Y%m%d-%H%M%S)`), so all of one restack's backups share a prefix and sort by time.

    ```bash
    STAMP=$(date +%Y%m%d-%H%M%S)
    for b in <branches-to-rewrite>; do
      git branch "backup/$STAMP/$b" "$b"    # omit -f: a name clash means you reused a stamp — pick a new one
    done
    ```

    - Prefer branches over tags for backups: they are easier to discover, check out, and restore by name. (A parallel tag is fine as an extra, but the branch is the contract.)
2. **Capture current state in a restore doc** before running the rebase/restack. Record, for every branch in the stack (or at least the current branch and its ancestors/descendants):
    - Branch name and its current commit SHA (`git rev-parse HEAD` per branch; `gt log` / `git branch -vv` for the stack layout).
    - **The backup-branch prefix** (`backup/<YYYYMMDD-HHMMSS>/`) created in step 1, and the Graphite parent of each branch (so parents can be re-pointed on restore).
    - The upstream/tracking ref each branch points at, and a short note on what operation you are about to run and why.
3. **Save it** to a dated file at the repo root, e.g. `RESTACK-RESTORE-<YYYYMMDD>.md`.
4. **If a restore doc already exists** (from an earlier operation), do **not** overwrite it:
    - Read it and make sure you understand the state it records.
    - If it is outdated (branches/SHAs have moved since it was written), mark the existing entry as **OUTDATED** (leave its content intact for recovery), then append a new dated section with the current latest status.
    - The doc is append-only history: each rebase/restack adds a new current-status section (with its own backup-branch prefix); old sections are kept and flagged outdated.
5. Only after the backup branches exist and the restore doc reflects the current state should you run the rebase/`gt restack`.
6. If the operation fails, restore each branch by name from its backup branch, then re-point Graphite parents and rebuild:
Tell the user what happened before retrying.

    ```bash
    for b in <branches>; do git branch -f "$b" "backup/<YYYYMMDD-HHMMSS>/$b"; done
    gt restack   # re-point parents / rebuild metadata; re-attach any worktree that held a rewritten branch
    ```


## Resolving Conflicts During a Restack

Frame each conflict before touching it. A stack's descendant is **its parent's code + the descendant's own additive change**. When the parent is rewritten, a restack conflict is *not* two rival versions to blend — it is "take the new parent's version of anything shared or renamed, and replay the descendant's own additive lines on top." Resolve by this layering rule, not by eyeballing which side looks more complete.

1. **Use `-onto` once a parent has moved.** After rewriting branch `P`, restack its child `C` with `git rebase --onto <new-P-tip> <OLD-P-tip> C` (old tip = `P`'s `backup/<stamp>/…`). A plain `git rebase P` regresses the merge-base to the common ancestor and re-replays `P`'s already-restacked commits, re-surfacing every conflict you already solved. `gt restack` does this for you; when driving by hand, always pass `-onto`.
2. **Classify every hunk into one of three buckets:**
    - *Additive* — only the descendant has it (its own feature/optimization): **keep it**.
    - *Base rename/refactor* — the base renamed a symbol or reshaped a function (e.g. `TombstoneCover`→`ClearToCover`, two functions merged into one): **take the base's new form**, and rename the descendant's references to match.
    - *Convergent* — the descendant did the same thing the base now also does: **take the base's copy**; the descendant's commit becomes empty and should drop (`git rebase --empty=drop`).
3. **Turn on diff3 conflict style** (`git config merge.conflictstyle zdiff3`). Seeing the common ancestor between the two sides is what makes "additive vs base-rename vs convergent" decidable; without it you cannot tell a descendant's addition from a base change.
4. **When a descendant owns a whole file, resolve with `X theirs`.** If a branch wholesale-refactored a file the base only lightly touched (or only renamed a symbol in), let that branch's version win for its own commits (`git rebase -X theirs`, or `git checkout --theirs <file>` per conflict), then re-apply any base-API change the file needs as a separate tip commit. Do not hand-merge large hunks that the refactor already superseded.
5. **API adaptations are their own commits, not smuggled into a conflict resolution.** If a descendant's call sites must change to compile against the new base API, make that a small, clearly-labelled commit (or `-amend` on the owning commit) on that branch. This keeps each branch's tip buildable and the adaptation reviewable, separate from the mechanical rebase.
6. **Validate every restacked branch two ways:**
    - `git diff <new-base> <branch>` should show **only that branch's own additive delta** (no base change leaking in).
    - `git diff <old-branch-tip> <branch>` should show **only the base-API renames it inherited** (no feature dropped).
    If the first shows a base change, or the second shows a lost feature, the resolution is wrong — redo it.
7. **A branch checked out in another worktree cannot be rebased from elsewhere.** `git` refuses to move a branch checked out in another worktree, and force-moving its ref corrupts that worktree. Rebase it from within its own worktree; run `git worktree list` first to find where each branch lives.
8. **Intermediate commits should compile; the tip must compile and pass tests.** Prefer resolutions that keep each replayed commit self-consistent (e.g. apply a rename even in a commit that a later commit will change again), so a mid-stack checkout still builds. Always build and test the final tip before declaring a branch restacked — a clean rebase is not a passing build.

## Things To Avoid

- **Do not resolve a restack conflict by picking whichever side "looks complete."** Classify the hunk (additive / base-rename / convergent) and apply the layering rule.
- **Do not plain-`git rebase` a child after its parent was rewritten** — use `git rebase --onto <new-parent-tip> <old-parent-tip> <child>`, or the merge-base regresses and re-replays already-restacked commits.
- **Do not run `git rebase` or `gt restack` without timestamped backup branches and a current restore doc.** Create the `backup/<YYYYMMDD-HHMMSS>/<branch>` branches first, then write (or update, never overwrite) the `RESTACK-RESTORE-<date>.md` doc.
- **Do not reuse a backup timestamp/prefix across operations** — each restack gets its own `<YYYYMMDD-HHMMSS>` so no backup is ever clobbered (create backups without `f`).
- **Do not overwrite an existing restore doc.** Mark outdated sections **OUTDATED** and append the current status.
- **Do not delete backup branches** as part of cleanup — leave them for the user to prune once the stack is confirmed good and pushed.
- **Do not push** after a rebase/restack unless the user explicitly asks — leave that to them.
- *Do not add new comments ** during rebase/restack.
