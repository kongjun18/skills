# Patterns from Model Papers

Read this when the outline lacks a good structure, when comparing candidate
structures, or when choosing a Motivation–Design boundary. Transfer the
underlying relationship, never a source paper's section order, headings,
terminology, or claims. Use a pattern only when the target paper has the same
dependency.

## 1. Finding model papers by presentation goal

When new text needs a structure, or an extracted outline has jumps that
reordering does not fix, a research subagent searches top-venue papers that
share the **presentation goal** (the argument shape), not necessarily the
topic. Example shapes: two existing designs each fail one requirement, and a
workload property lets a new design meet both; an old idea from another field,
adapted where its key assumption breaks. It reports how each paper orders its
paragraph roles, introduces its insight, positions against the nearest classic
idea, and states results and costs. Record the papers and role sequences in
scratch notes and in the outline header. Never copy wording.

For a new section, the same subagent can read 5 to 7 recent, closely related
papers from the target venue for abstract length, introduction length and
paragraph roles, and how they state headline numbers, and fetch the call for
papers for page limits.

## 2. Reference set

- [WiscKey, FAST 2016](https://www.usenix.org/system/files/conference/fast16/fast16-papers-lu.pdf)
- [Slacker, FAST 2016](https://www.usenix.org/system/files/conference/fast16/fast16-papers-harter.pdf)
- [IRON File Systems, SOSP 2005](https://doi.org/10.1145/1095809.1095830)
- [All File Systems Are Not Created Equal, OSDI 2014](https://www.usenix.org/system/files/conference/osdi14/osdi14-paper-pillai.pdf)
- [The Unwritten Contract of Solid State Drives, EuroSys 2017](https://doi.org/10.1145/3064176.3064187)
- [Protocol-Aware Recovery for Consensus-Based Storage, FAST 2018](https://www.usenix.org/system/files/conference/fast18/fast18-alagappan.pdf)
- [O³-LSM, arXiv 2026, §5](https://arxiv.org/html/2603.05439v1#S5)

## 3. Transferable patterns

1. **Start from a decision-relevant observation.** Strong openings establish an
   existing assumption, a measured workload property, or a failure scenario
   that makes a design decision consequential (WiscKey: LSM amplification
   meets SSD properties; Slacker: where container startup time goes; All File
   Systems: a concrete crash state). Test: if a sentence would not change what
   a reasonable designer chooses, it is context, not Motivation evidence.
2. **Derive the opportunity before naming the mechanism.** "Only a small
   fraction of container data is needed before useful work" supports avoiding
   eager transfer; it does not prescribe a particular file system or cloning
   method.
3. **State one central decision, then its consequences.** WiscKey separates
   values from sorted keys, then makes range queries, garbage collection, and
   crash consistency explicit problems; each later mechanism answers one.
4. **Align analysis units with design units** when the evidence supports it
   (Slacker's workload questions map onto its design subsections). Do not force
   one-to-one mappings.
5. **State goals as checkable constraints**, with a condition, resource, or
   compatibility boundary, not slogans.
6. **Define the failure model or taxonomy before comparing solutions** when
   "correct", "safe", or "fast recovery" has several meanings (IRON; All File
   Systems; Protocol-Aware Recovery's safety, availability, recovery time, and
   complexity axes). Not every paper needs one.
7. **Let figures carry what prose cannot hold locally:** a scenario timeline,
   a taxonomy table, a workload-to-design map. Motivation figures show the
   problem; architecture figures belong in Design.
8. **Evaluate the decision, its benefit, its cost, and its scope.** WiscKey
   follows its headline result with range queries, garbage collection, crash
   recovery, and known regressions; Slacker checks long-running performance
   because lazy fetching can move cost to later execution.
9. **Keep exceptions visible.** Name the workloads where the design loses and
   let the evaluation test that condition.
10. **Organize Evaluation as a claim sequence:** questions → setup → headline
    result → attribution → costs and secondary paths → generality, scalability,
    or limits. The Unwritten Contract turns many measurements into a few rules
    and organizes the analysis by them; group figures that support one
    conclusion instead of narrating each. O³-LSM maps each result group to a
    question and uses breakdowns to show where benefit and cost come from.

## 4. Comparing candidate structures

Ask of each candidate:

1. Does the decision-relevant observation come before the choice it motivates?
2. Can each major Design unit be traced to a prior observation or requirement?
3. Does each design consequence appear before the mechanism that addresses it?
4. Does Evaluation test benefit, cost, and scope in an order that follows the
   claims?
5. Can a reader understand Motivation with Design hidden?

Prefer the candidate with the fewest deferred definitions, the least
backtracking, and the smallest restructuring for the gain. Reject one that
places a unit before its prerequisite, separates evidence from its claim,
mixes section responsibilities, loses a protected fact, or needs an
unsupported relation. If candidates tie on the evidence, choose the simpler
and state the ambiguity; do not claim a unique optimum.

## 5. Five-answer reading worksheet

For a close reading of a model paper or of the target draft:

1. Which existing assumption does the paper challenge?
2. Which observation or failure makes the problem worth solving?
3. Which central idea changes a design decision?
4. Why does that decision require each later mechanism?
5. Which claim, cost, or condition does each evaluation group test?
