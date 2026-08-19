---
name: address-pr-comments
description: "Fetch all review comments on a GitHub PR, investigate each thread against the current code, and write the classification (address / investigate / fixed / skip / deferred), proposed fix, risk, and open questions to temp/PR_PR_ID_REVIEW.md, which then serves as the living progress tracker and final report. No code changes until the user asks. Triggers: address PR comments, respond to PR review, handle review feedback, work through PR comments, triage review threads."
---

# Address PR Comments

Triage and work through PR review feedback in five steps:

1. **Fetch** every review comment and PR-level comment from GitHub.
2. **Classify** — give each thread an ID and a provisional status.
3. **Investigate** — read the code behind each thread: is the concern real, is it already fixed, what is the fix, what does the fix risk.
4. **Write** `temp/PR_<pr-id>_REVIEW.md` — the classification and the analysis.
5. **Iterate** with the user, who drives from the doc.

Do not invoke this skill for a one-off "what does this comment mean?" question — just read that comment directly.

## Invariants

These hold at every step; the steps below do not restate them.

1. **Read-only until asked.** Investigate and document freely; change code only for items the user explicitly asks you to fix. No plan mode, no proposing a plan of action in chat, no pre-emptive "shall I start with X?". The doc is how you hand work back. Commits and GitHub writes (`gh pr comment`, thread replies) happen only on explicit request.
2. **Evidence, not inference.** Every Problem, Fix, and Risk comes from reading the code, not from reading the comment. Check the reviewer's premise before accepting it — reviewers and bots are sometimes wrong about surrounding context. A field you could have written without opening a file is not analysis.
3. **Uncertainty is a status, not a guess.** Unclear fix, risk, background, goal, purpose, or reviewer intent → `investigate`, even if that leaves most of the table there. Never guess to move a row out of it.
4. **Nothing is dropped or truncated.** Every thread is a row, including already-fixed and declined ones. Every `skip` carries a one-line reason.
5. **The doc is the index of record** — deliverable, progress tracker, and final report. A doc whose rows are all `fixed` *is* the report; never write a parallel summary, report, or fix-list file. It may *link out* to a companion doc in the rare case that one thread's analysis is both complex and long (Step 4), but status, ownership of the conclusion, and the row for every thread stay here. It must never lag the conversation: any change to a row's state lands in the file in the same turn it happens, before you report to the user.
6. **Fresh inputs only.** `temp/PR_REVIEW_COMMENTS.md` and `temp/PR_<pr-id>_REVIEW.md` are outputs, never inputs across sessions. Never classify from a prior run's comments, never carry rows forward from a prior run's doc.
7. **IDs are stable.** Thread and question IDs never change for the life of a doc, including as rows change status.

## Step 1: Fetch the comments

Every invocation starts with a fresh fetch. Use an authenticated GitHub connector when available; otherwise use `gh api` from the root of the repository being reviewed. Determine the repository from `origin` and the PR from the current branch unless the user supplies them.

Fetch and paginate all of the following before proceeding:

- PR number, title, URL, head branch, and base branch;
- PR-level comments in chronological order;
- inline review threads in file and line order;
- every reply in each thread, with author, timestamp, resolution state, and the original diff hunk.

Write the fresh result to `temp/PR_REVIEW_COMMENTS.md`, overwriting any previous result. Preserve enough structure to distinguish PR-level comments, threads, and replies.

If it reports "No PRs found for branch …", ask the user for the PR number rather than guessing.

**When the fetch fails, stop.** There is no fallback (invariant 6). Report the error verbatim and ask the user to provide a fresh complete export or enable authenticated GitHub access. Do not proceed on cached data even if the request implies urgency.

Take from the file header, for Step 4: PR number (the `<pr-id>`), PR title and URL, branch (`<head-ref>` → `<base-ref>`), and the fetch timestamp.

## Step 2: Read and classify

Read the fetched markdown end-to-end: PR metadata header, then PR-level comments, then inline review threads grouped by file and line — each with the diff hunk the reviewer saw, the top-level comment, then replies in order.

Work at *thread* granularity; replies belong to their thread, not to separate rows.

**Assign IDs.** Number threads `1, 2, 3, …` in the order they appear in the file — PR-level comments first, then inline threads by file and line. The ID is how you and the user refer to a thread for the rest of the conversation ("skip 4", "what's the risk on 11?").

**Assign a provisional status.** Step 3 confirms or revises it; the doc records the post-investigation status, not this first guess. The five statuses, written lowercase everywhere they appear:

| Status | Meaning |
| --- | --- |
| `address` | Need to fix. Actionable feedback whose problem, fix, and scope you understand: typos, bugs, naming, missing error handling, missed review items. |
| `investigate` | Need to investigate. Any uncertainty about the fix, risk, background, goal, purpose, or reviewer intent — including unclear requests, reviewer questions, thread disagreement, and "is this concern even real". |
| `fixed` | Already true in the working tree, confirmed by the Step 3 code check — or fixed later at the user's request. |
| `skip` | Denied. Nitpicks the user already pushed back on, off-topic suggestions, bot noise with no concrete ask, feedback the user declined. |
| `deferred` | Understood and accepted, but not for this PR — the fix has a blocker (missing dependency, upstream change, unavailable data), or is large enough to warrant a standalone PR. Say which, and name the blocker. |
- Use `deferred`, not `address`, when you know what to do but cannot land it in this PR.
- Bot-only threads (e.g. `arcticowl-ai-review-emu[bot]`) with no human follow-up default to `skip` unless the finding survives the Step 3 check.
- A reviewer who explicitly accepted a pushback ("sgtm", "ok, fine to leave") → `skip`, reason: reviewer accepted pushback.

GitHub-`RESOLVED` threads are already stripped by the fetch script (the header says how many were hidden), so anything in the file is unresolved on GitHub. What you still have to catch are threads open on GitHub but settled in substance — that is Step 3's job.

## Step 3: Investigate the code

For each thread:

1. **Locate it.** Read the current file at `<file>:<line>`. The diff hunk is the snapshot the reviewer saw; `original_commit_id` in the raw API data says which commit that was.
2. **Already fixed?** Compare the current code against the concern.
    - Code no longer matches the hunk *and* the feedback no longer applies (reviewer flagged a missing null check; current code has one) → `fixed`, with the evidence (`null check present at <file>:N`, commit sha if known). An author reply saying "done" is not evidence on its own.
    - Code changed but the issue survives → keep it active, and state the problem against the *current* code, not the hunk.
    - Code unchanged → keep the reviewer's original concern.
    - Can't tell → `investigate`.
3. **Is the concern real?** A "missing" check may live in the caller; a "leak" may be owned by an arena. If the finding is wrong, the Problem field says so and cites what refutes it.
4. **What is the fix?** Trace it far enough to name the files and call sites it touches. Follow the symbol to its definition and callers, and look for other instances of the same pattern. "Rename the field" is not a fix if the field has 40 references.
5. **What does the fix risk?** What behavior changes, who depends on it, and whether a test covers it — an untested fix is a different risk from a covered one. Name the blast radius, not just "low risk".
6. **Settle the status.** Uncertainty at any of 3–5 → `investigate`. Understood but unlandable here → `deferred`.

`Read`, `Grep`, and `LSP` (`findReferences`, `goToDefinition`) are the tools for this. This step is allowed to be the expensive one; that is the point. Do not shortcut it by writing speculative rows and promising to check later.

## Step 4: Write the review doc

Write to `temp/PR_<pr-id>_REVIEW.md`, `<pr-id>` being the PR number (e.g. `temp/PR_12345_REVIEW.md`). If the file exists from an earlier session, overwrite it without reading it (invariant 6) — its statuses describe an older revision and older comments. The same goes for any `temp/PR_<pr-id>_*` companion docs left behind: they belong to the previous run's thread IDs, so do not link to one until this run's investigation has rewritten it. Tell the user you overwrote the doc, and ask them to restate any prior-session decisions that still apply, since IDs are re-derived and may have shifted.

**Header** — the provenance of the review:

```markdown
# PR <pr-id> review — <PR title>

- **PR:** <pr-url>
- **Branch:** `<head-ref>` → `<base-ref>`
- **Reviewed:** <YYYY-MM-DD>
- **Comments fetched:** <fetch timestamp from temp/PR_REVIEW_COMMENTS.md>
- **Head commit:** `<short-sha>` (`git rev-parse --short HEAD`)
- **Status:** N address · N investigate · N fixed · N skip · N deferred
```

PR number, title, URL, branch refs, and fetch timestamp are copied from the fetched file's header, not re-derived. `Reviewed` is today's date. `Head commit` is what Step 3 investigated against — it is what makes a `fixed` row checkable later. Keep the status counts in sync with the table on every change.

**Summary table** — one row per thread, exactly these fields:

| ID | Description | Problem | Fix | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| 1 | `foo.cc:120` @alice — null check | `cfg` deref at 118 precedes guard at 121 | move guard above 118 | `address` | — |
| 2 | `bar.py:44` @bob — why retry cap 3? | cap unjustified; no comment or test pins it | unknown until Q2.1–Q2.2 | `investigate` | Q2.1, Q2.2 |
| 3 | `baz.h:12` @alice — doc typo | typo `recieve` | corrected spelling | `fixed` | already correct as of `a1b2c3d` |
| 4 | `qux.cc:88` @carol — flat_hash_map | log(n) per lookup on a hot path | swap container, 6 call sites | `deferred` | standalone PR; analysis → §4 |
| 5 | `main.cc:9` bot — header guard | none; `#pragma once` at line 1 | — | `skip` | finding wrong, no follow-up |

**Keep the table aligned.** Pad every cell so the pipes line up in the source, including the separator row, and re-pad the affected column after any edit that changes a cell's width — a row moving from `investigate` to `fixed` shortens that cell and breaks the column. Aligned source is why the table stays readable as it grows to thirty rows; an agent that appends ragged rows has made the tracker harder to read than the raw comments.

Alignment only stays practical if cells stay short, so hold each cell to a single terse clause — roughly 45 characters, no line breaks, no bullet lists, no sentences. The table is the index; the depth belongs in the thread's section below it. When a cell wants to be a paragraph, that is the signal to shorten it and let the section carry the rest.

- **ID** — the thread's ID from Step 2.
- **Description** — `<file>:<line>` (or *PR-level*), reviewer login, and the subject in a few words.
- **Problem** — the concern *as the investigation found it*, with the code fact that makes it true. "none — finding is incorrect" when that is the case.
- **Fix** — the proposed fix; `unknown until Q<id>` for `investigate`; `—` for `skip`.
- **Status** — exactly one of `address`, `investigate`, `fixed`, `skip`, `deferred`. Lowercase, no other values, no "partially" or "in progress" — a half-done fix is still `address` until it lands.
- **Notes** — open-question IDs, the blocker or standalone-PR reason, the denial reason, the `fixed` evidence, the pointer to a deep-dive doc, and the latest status transition (Step 5).

**Status sections** — one per status, in order `address` / `investigate` / `fixed` / `skip` / `deferred`. Head each thread's subsection with its ID (`#### 4 — qux.cc:88 (@carol)`) so the user can jump by number, and carry the detail that does not fit a table cell:

- Thread link (reuse the `[link](...)` from the fetched file) and reviewer login.
- The reviewer's ask, quoted or summarized.
- **Analysis** — what the current code does, why the concern holds or fails, and the evidence read (`<file>:<line>`, test name, commit sha).
- **Proposed fix** — concrete enough to act on, naming the files and call sites that change. Describe it; do not implement it.
- **Risk** — what could break, who depends on current behavior, what coverage exists.
- **Goal** — what must be true for the thread to be settled.
- **Open questions** — as below.
- **History** — once the row has moved, the status-transition chain (Step 5). Absent on rows that have not changed yet.

**Open question IDs** — `Q<thread-id>.<n>`, with `n` starting at 1 within each thread: thread 2's questions are `Q2.1` and `Q2.2`; thread 12's first is `Q12.1`. The dot is load-bearing — bare concatenation makes `Q121` ambiguous between thread 12 question 1 and thread 1 question 21. One per line, phrased so a short answer unblocks it:

```markdown
**Open questions**

- **Q2.1** — Was the cap of 3 chosen to match the upstream 30s timeout budget, or is it arbitrary?
- **Q2.2** — If arbitrary, do you want it configurable or just documented?
```

Cite the IDs in the row's Notes so the table alone shows what is blocked on what. Any status may carry questions — a `deferred` row might ask whether the follow-up PR is worth filing now.

**When one thread's analysis is genuinely complex *and* long**, do not inline it and do not compress away the reasoning. Write it to a companion doc and leave a conclusion behind:

```markdown
**Analysis** — the crash is a lock-ordering inversion, not the missing null check
@alice diagnosed: `Session::Close()` takes `mu_` then `pool_mu_`, while the reaper
path takes them in the opposite order. The null check would hide the symptom on
this path only. Full trace, the two stacks, and three candidate fixes with their
tradeoffs: [PR_12345_07_lock_ordering.md](PR_12345_07_lock_ordering.md).
```

- **Inline is the default; a companion doc is the exception.** Most threads — including most `deferred` ones — need a few sentences of Analysis and Risk and nothing more. Splitting a thread that did not need it scatters the review across files for no gain, and costs the reader a hop to learn something that fit in a paragraph.
- **Trigger — both conditions, not either.** Split only when the analysis (a) is *complex*: it needs multi-file call traces, a repro, measurements, or a table of alternatives with their tradeoffs; **and** (b) is *long*: written out honestly it runs past roughly 30 lines and would dominate the review doc. One condition alone is not enough — a complex finding that fits in a paragraph stays inline, and a long-but-simple enumeration gets tightened rather than exported. When in doubt, inline it.
- **Naming** — `temp/PR_<pr-id>_<thread-id-zero-padded>_<slug>.md`, e.g. `temp/PR_12345_07_lock_ordering.md`. One doc per thread, so the filename says which row it belongs to.
- **Split of content** — the companion doc holds the trace, the excerpts, the measurements, and the rejected alternatives with reasons. The review doc holds the conclusion: what is true, what you propose, and what it risks, in a few sentences a reader can act on without opening the link.
- **The conclusion must stand alone.** "See the deep dive" is not a conclusion. A reader who never opens the link must still learn the finding and the recommendation.
- **Status and questions never move out.** The row, its status, its transitions, and its `Q<id>` questions live in the review doc only — the companion doc is evidence, not a second tracker (invariant 5). It needs no status field and is not updated as the row progresses; if the conclusion changes, the review doc's Analysis changes and the companion doc gains a dated correction.
- Reference the companion doc from the row's Notes (`analysis → PR_12345_07_lock_ordering.md`) as well as the section, so the table shows where the depth went.

Keep the table scannable and put the depth in the sections — or, in the rare case above, in a linked companion doc.

## Step 5: Iterate with the user

Point the user at `temp/PR_<pr-id>_REVIEW.md` with a one-paragraph orientation: counts per status, and the open questions (by ID) blocking the most rows. Then let them drive.

From here it is a conversation that may run many turns: they answer questions, dispute an analysis, ask you to dig deeper on one thread, restatus rows, request fixes a few at a time, or come back after pushing new commits. Handle each request at the scope asked.

Per invariant 5, the doc absorbs every state change in the same turn. The row's Notes carries the **latest** transition; the thread's section carries the full chain under **History**, so the table stays short and aligned as a row moves several times:

```markdown
| 2  | `bar.py:44` @bob — why retry cap 3? | cap unjustified; nothing pins it | document the cap, keep 3 | `deferred`    | blocked on PR #991; history → §2 |
```

```markdown
**History**

- `investigate` → `address` (2026-08-10): Q2.1 answered — 3 matches the upstream 30s budget.
- `address` → `deferred` (2026-08-11): needs the upstream constant exported first (blocker: PR #991).
```

- **Status transitions** log as `<old>` → `<new>` with a date and a reason: `investigate` → `address` when a question is answered, `address` → `deferred` when a fix turns out blocked mid-way, `address` → `skip` when the user declines, `address` → `fixed` when the fix lands. Never leave a row at `address` after learning it cannot be done.
- **Answered questions** are recorded against their ID (`Q2.1 answered: …`) in History, folded into Analysis and Fix, and removed from the open list.
- **Applied fixes** move the row to `fixed` with what you actually did, how it differs from the proposal if it does, and the verification you ran (`bazel test //foo:bar_test — 12 passed`). Move the subsection into the `fixed` section. Fixing several items means updating the doc after each one, not in one batch.
- **Deepened investigation** replaces the shallower Analysis and Risk in place; if the conclusion reverses, log that in History (`concern refuted on closer read: guard exists in the caller at <file>:N`). If the deepened analysis outgrows the section, move it to a companion doc per Step 4 and leave the conclusion behind.
- **Re-pad the table** after every edit — status tokens differ in width, so a transition that is not followed by re-alignment leaves the column ragged.

In chat, say what changed and point at the doc — the doc carries the detail.
