# Related Work: position the design

Related Work places the design in its design space. It is not a survey. For
each prior approach, the reader should learn three things:
- what the design shares with it;
- what the design changes;
- why the change matters.

Text that only describes what other systems do fails this purpose, even when
every description is correct.

The two common defects are a weak link between each prior work and the
paper's own argument, and detail that does not match how close each work is.
The positioning map below prevents both before any prose exists.

## Stage 1 for Related Work: the positioning map

For Related Work, stage 1 produces a positioning map instead of a
sentence-role outline. The map has one row per work, or per coherent group
of works:

| Work or group | Relationship | Decisive axis | Shared | Changed, and the consequence | Closeness | Words |
|---|---|---|---|---|---|---|

- **Relationship**: one of
  - an alternative,
  - a foundation (an inherited idea),
  - an extension target,
  - a complementary technique,
  - a different trade-off.
- **Decisive axis**: the substantive choice that separates the work from the
  design. Candidates:
  - the abstraction;
  - the information available when a decision is made;
  - what stays on the critical path;
  - the maintained state: what it is, where it lives, and how it grows;
  - the guarantee;
  - who pays which cost.

  A data-structure name, a deployment setting, or an application domain is
  not an axis.
- **Closeness**: rank 1 is the work a reviewer would cite as "this is just
  X".
- **Words**: allot the budget by closeness. The closest work gets the most
  words. A distant group gets one sentence.

Then build the section from the map:
- **Tie the axes to the paper's argument.** Take the axes from the problem
  statement in the introduction and motivation: its requirements, and why
  the existing approaches fail. Each paragraph's positioning claim should
  read as a position on those axes, so the reader can trace it back to the
  paper's argument. This is the logic chain of Related Work.
- **Group by design choice.** Group the rows into three or four paragraphs
  by the approach or design choice they represent, not by venue or system
  type. Each paragraph makes one positioning claim.
- **Choose an order and record why.** Either follow the axes in the order
  the problem statement raises them, or order by closeness.
- **Run the closest-work test.** For the closest one or two rows, answer in
  the map: "Would adopting or straightforwardly extending this work already
  give our contribution?" If it would, narrow the claim. Never invent a
  limitation.
- **List inherited ideas.** The text must acknowledge them.

The stage 1 reviewer checks the map, not wording. Ask it:
- which rows have no clear relationship;
- which distinctions rest on names only;
- whether the closeness ranks and word shares match;
- whether a closer work is missing.

## Writing the comparison

- **State the relationship directly.** Prefer one compact comparative
  sentence ("X shares A but keeps B, so C") over a separate description of
  each system ("X does A. We do B.").
- **Name shared mechanisms when they delimit what is new.** Hiding them
  makes a reviewer who knows the work suspect the overlap is concealed.
- **Give context only as far as the comparison needs.** A short clause is
  often enough. Use the paper's terms and its established motivation. Do not
  repeat the design exposition; refer to the section instead.
- **Expand only for the closest work,** and only to answer a likely novelty
  objection.
- **Leave out** architecture inventories, and performance numbers unless
  positioning needs them.
- **Keep the qualifying trade-off.** If the design gives something up
  against the work, say so in the same comparison.
- **There is no fixed template.** These are review criteria, not elements
  that every paragraph must state.

## Accuracy and scope

- **Verify each mechanism against the cited version** of the paper or
  documentation, and record what was verified. One-clause summaries are easy
  to get wrong, and easy for a reviewer to check.
- **A different objective is not a deficiency.** An unstudied extension is
  not an impossibility.
- **Explain complementarity through a concrete decision, cost, or layer.**
  "Orthogonal" alone explains nothing.
- **Scope each comparison.** A claim about one specific system does not
  characterize its whole class.
- **Keep every claim consistent with the rest of the manuscript.**

## Examples, weak and stronger

The author provided these examples, from the cited versions:
- **AIFM** (OSDI'20, section 2).
  - Weak: "Kernel systems operate on pages, whereas AIFM operates on
    objects."
  - Stronger: "AIFM replaces page-based swapping with object-granular
    access, reducing I/O amplification for small objects and exposing
    application semantics to the runtime."
- **WiscKey** (FAST'16, section 5).
  - Weak: "FAWN stores values in a log. WiscKey uses an LSM-tree and a value
    log."
  - Stronger: "WiscKey shares the append-only value layout of hash-indexed
    stores but retains an ordered LSM index, preserving range-query
    support."
- **Fastswap** (EuroSys'20, section 7).
  - Weak: "Fastswap is orthogonal to existing cluster schedulers."
  - Stronger: "The paper's local/far-memory allocation policies complement
    the compared cluster schedulers by specifying how each job's memory is
    split across tiers."

Model Related Work sections, by the pattern they show:
- **NOMAD** (OSDI'24, 2.3): which operations remain on the critical path,
  while acknowledging prior background migration.
- **BetrFS** (FAST'15, 8): which benefits prior designs would gain by
  moving into the kernel, and the data-structure distinction that remains.
- **FASTER** (SIGMOD'18, 8): how combining known techniques allocates
  costs differently for hot data and for storage.
- **ALEX** (SIGMOD'20, 7): a shared indexing principle, then the added
  routing, insertion, and adaptation decisions.
- **Wormhole** (EuroSys'19, 5): cache or parallelism optimizations,
  separated from changes in how index-access cost grows.

## Review brief for Related Work (stages 2 and 3)

Ask the reviewer to:
1. **Extract the positioning map from the prose**: relationship, decisive
   axis, and consequence for each work. Compare it with the planned map.
   Flag rows with no stated relationship, and distinctions that rest on
   names only.
2. **Check the logic chain.** Does each paragraph's claim connect to the
   paper's problem axes? Does the order follow a stated principle?
3. **Check balance.** Do the words per row match the closeness rank?
4. **Run the closest-work test as a skeptic.**
5. **Verify every claim about prior work** against its source, saying which
   claims it verified.
6. **Find removable sentences.** Which sentences can go without losing
   positioning information? Is the section within its budget?
