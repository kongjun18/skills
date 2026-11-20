# Subjects: Sources and Outline Skeletons

Read for every tutorial. Each kind has what to read, what to pin, and an outline skeleton. The skeletons are starting points; reorder to fit the learner's goal.

## Repo

**Pin first.** Record the full `git rev-parse HEAD` before reading. Every citation refers to that commit; it goes in `<meta name="source-commit">` and the header. Read the code as it is at that commit (`git show <commit>:<path>`), not the working tree. If `git status` shows uncommitted changes to code you will teach, ask the user whether to teach the committed version (default) or wait for a commit; never cite uncommitted lines, because nothing can pin them.

**Read in this order:**

1. The project's own words: README, `AGENTS.md` / `CLAUDE.md`, design docs, architecture notes. Treat them as claims to check against code, not facts; where they disagree with the code, the code wins and the tutorial says so.
2. The shape: directory tree, build files, entry points (`main`, CLI handlers, server startup, public API).
3. The core data structures: the few types that most code reads or writes.
4. One operation end to end: pick the operation the learner's goal cares about and trace it from entry point to effect. This becomes the walkthrough and usually the running example.
5. Tests for the parts you explain: they show intended behavior and make good examples.

Use a code-intelligence index when the harness has one; otherwise search and read. Read the code you cite, not only its name.

**Skeleton:**

1. Big picture: what problem the system solves, its main components, and how data flows between them (diagram).
2. Lessons, one per core concept or component the goal needs, each tied to the running example.
3. Walkthrough: the traced operation, step by step, each step with a file:line citation and a short excerpt.
4. "Where to change things" (the `<h3>` at the end of the walkthrough): for a goal like "modify X", the files and functions to start from and the tests that cover them.

## Concept

**Sources, in order of preference:** the original paper or specification, authoritative textbooks or lecture notes, official documentation, then well-regarded tutorials. Open each one; record title, authors, year, and URL. Prefer one or two primary sources read properly over many skimmed.

**Find the canonical example.** Most concepts have a standard small example (a worked trace, a toy input, a classic failure case). Use it or build a smaller one; compute every number in it yourself and check it.

**Skeleton:**

1. Big picture: the problem the concept solves, why the obvious approach falls short, and the core idea in one paragraph.
2. Lessons: the mechanism, built up in steps on the running example; then why it works (the invariant or argument); then its costs and limits.
3. Variants and where it is used, only as far as the goal needs.
4. Misconceptions: the standard confusions, each with why it is wrong.

## Research

A research-direction tutorial teaches the learner to read and judge work in the area, not to list papers.

**Sources:** a recent survey if one exists, the founding paper(s), and the papers that changed the direction. Find candidates by search, then open each one; verify title, authors, venue, and year from the paper or its publisher page, never from memory. Record which claims come from which paper.

**Skeleton:**

1. Big picture: the problem, why it is hard, and why it matters now.
2. Lessons: the shared vocabulary and evaluation setup (workloads, metrics, baselines); the main families of approaches, each with its key idea, a representative paper, and the tradeoff it makes; a comparison table across families.
3. Open problems: what the papers themselves name as unsolved or contested, with sources. Separate these from your own synthesis, which you label as such.
4. Reading path: an ordered list in Further reading — what to read first, and what each paper adds.
