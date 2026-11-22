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

A research-direction tutorial is a light research primer: it teaches the learner to read and judge work in the area and leaves them with candidate research questions, not a list of papers.

**Sources, in three lanes:**

- **Papers:** a recent survey if one exists, the founding paper(s), the papers that changed the direction, and the latest work. Find candidates by search, then open each one; verify title, authors, venue, and year from the paper or its publisher page, never from memory. Record which claims come from which paper.
- **Systems:** the documentation of the systems people actually use, for what each promises and what it leaves out.
- **Field signals:** what practitioners report as broken, missing, or confusing, from issue trackers ([below](#field-signals)).

**Skeleton:**

1. Big picture: the problem, why it is hard, and why it matters now.
2. Lessons, in roughly this order, each kept only if an exam question needs it:
   - Why: the workload or need, and why the obvious approach falls short.
   - What: the semantics or guarantees the approaches must provide, with the shared vocabulary.
   - How: the main families of mechanisms, each with its key idea, a representative paper or system, and the tradeoff it makes.
   - Landscape: a design-space table (a few axes that separate the families, one row per system or paper) and a timeline of how the direction evolved, which together form the road map.
   - Evaluation: the workloads, metrics, and baselines the area uses, and what they miss.
3. Gaps and research directions (`id="research-directions"`), labelled as your synthesis:
   - Gaps: an empty or contested cell of the design-space table, a problem the papers name as open, or a field signal the published work does not address. Each gap cites its evidence (paper, documentation, or issue link) and says why it is still open.
   - Plan list: one item per promising direction — the research question, the gaps it builds on, and two or three concrete first steps (a measurement, a prototype, a paper to read closely). Keep it to the directions the evidence supports.
4. Reading path: an ordered list in Further reading — what to read first, and what each paper adds.

## Field signals

A light pass over issue trackers that shows where practice hurts, used for every `research` tutorial with open-source systems, and in other kinds for misconception callouts. It reads titles, and bodies only when a title is promising; it is not a census.

1. Pick the three to five repositories of the systems the tutorial covers.
2. Search titles with the area's key terms, most-discussed first:

   ```bash
   gh search issues "<term>" --repo <owner/repo> --match title --sort comments --limit 30 \
     --json title,url,state,commentsCount,createdAt \
     --jq '.[] | "\(.state)\t\(.commentsCount)\t\(.createdAt[:10])\t\(.title)\t\(.url)"'
   ```

   Run `gh search prs` the same way for work in progress. Without `gh`, use the tracker's web search restricted to titles.
3. Group the hits into themes (for example: performance, correctness, missing feature, confusing semantics). Open the body of the few issues that anchor a theme; quote only what you read.
4. In the tutorial, report each theme with its issue links and the date of the search, and state the limits: the repositories searched, the terms used, and that titles undercount.

For a full census of one repository's issues and pull requests, with topic metrics over time, hand off to `repo-research-scout` and say so in Further reading.
