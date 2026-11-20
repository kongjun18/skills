# Rebase and Restack

Detail for section 2 of the [git skill](../SKILL.md). Read this before running `git rebase` or `gt restack`, and when resolving the conflicts they produce.

Rebasing and restacking rewrite history and can move several branches at once. A mistake can leave a stack that is hard to recover by hand, so every such operation starts by making the old state recoverable.

## 1. Back up, then write the restore doc

1. **Create a timestamped backup branch for every branch you are about to rewrite**: the current branch and every descendant a restack will move. Use one shared stamp per operation, so one restack's backups share a prefix and sort by time. Create them without `-f`; a name clash means the stamp was reused, so pick a new one.

   ```bash
   STAMP=$(date +%Y%m%d-%H%M%S)
   for b in <branches-to-rewrite>; do
     git branch "backup/$STAMP/$b" "$b"
   done
   ```

   Branches are the contract (they show in `git branch` and restore by name); a parallel tag is an optional extra.

2. **Record the current state in a restore doc** before running anything. For every branch in the stack (at least the current branch, its ancestors, and its descendants) record:
   - branch name and commit SHA (`git rev-parse <branch>`; `gt log` or `git branch -vv` for the layout);
   - the backup prefix `backup/<YYYYMMDD-HHMMSS>/` from step 1;
   - the Graphite parent of each branch, so parents can be re-pointed on restore;
   - the upstream or tracking ref, and one line on the operation you are about to run and why.

3. **Save it** as `_docs/scratch/restack/RESTACK-RESTORE-<YYYYMMDD>.md` in the checkout you operate in ([`_docs/` layout](../../repo-memory/references/docs-layout.md)). It is recovery scratch and never committed.

4. **Never overwrite an existing restore doc.** Read it and understand the state it records. If branches have moved since, mark that section **OUTDATED** (keep its content) and append a new dated section with the current state and its own backup prefix. The doc is append-only history.

5. Run the rebase or `gt restack` only after the backups exist and the doc reflects the current state.

6. **If the operation goes wrong**, tell the user what happened, then restore each branch by name and rebuild the stack metadata before retrying:

   ```bash
   for b in <branches>; do git branch -f "$b" "backup/<YYYYMMDD-HHMMSS>/$b"; done
   gt restack   # re-point parents and rebuild metadata; re-attach any worktree that held a rewritten branch
   ```

## 2. Resolve restack conflicts by layering

A descendant branch is *its parent's code plus the descendant's own additive change*. When the parent is rewritten, a conflict is not two rival versions to blend: take the new parent's version of anything shared or renamed, and replay the descendant's own additive lines on top. Do not pick whichever side "looks complete".

1. **Use `--onto` once a parent has moved.** After rewriting parent `P`, move child `C` with

   ```bash
   git rebase --onto <new-P-tip> <old-P-tip> C   # old tip = backup/<stamp>/P
   ```

   A plain `git rebase P` falls back to the old merge-base, replays `P`'s already-restacked commits again, and re-surfaces every conflict you already solved. `gt restack` does this for you; by hand, always pass `--onto`.

2. **Classify every hunk** into exactly one bucket:
   - *Additive*: only the descendant has it. Keep it.
   - *Base rename or refactor*: the base renamed a symbol or reshaped a function (for example `oldName` became `newName`, or two functions were merged). Take the base's new form and update the descendant's references to match.
   - *Convergent*: the descendant did what the base now also does. Take the base's copy; the descendant's commit becomes empty and should be dropped (`git rebase --empty=drop`).

3. **Show the common ancestor**: `git config merge.conflictstyle zdiff3`. Without the ancestor you cannot tell a descendant's addition from a base change.

4. **When a descendant owns a whole file**, let its version win for its own commits (`git rebase -X theirs`, or `git checkout --theirs <file>` per conflict), then re-apply any base API change the file needs as a separate tip commit. Do not hand-merge large hunks the refactor already superseded.

5. **API adaptations are their own commits.** If the descendant's call sites must change to compile against the new base API, make a small, clearly labelled commit (or amend the owning commit) on that branch rather than hiding the change inside a conflict resolution. Do not add new code comments while resolving.

6. **Validate every restacked branch two ways:**
   - `git diff <new-base> <branch>` shows only that branch's own additive delta (no base change leaking in);
   - `git diff backup/<stamp>/<branch> <branch>` shows only the base renames it inherited (no feature dropped).

   If either check fails, the resolution is wrong; redo it.

7. **Rebase a branch from the worktree that has it checked out.** Git refuses to move a branch checked out in another worktree, and force-moving its ref corrupts that worktree. Run `git worktree list` first to find where each branch lives.

8. **Keep commits buildable.** Prefer resolutions that keep each replayed commit self-consistent (apply a rename even in a commit a later commit changes again). Build and test the final tip of every branch before declaring it restacked; a clean rebase is not a passing build.

## 3. After the operation

- Leave backup branches in place; the user prunes them once the stack is confirmed good and pushed.
- Do not push unless the user explicitly asks.
