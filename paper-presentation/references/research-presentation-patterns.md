# Research Presentation Patterns from Systems Papers

Use this reference when discussing a paper's story, searching for a target
structure, or deciding whether Motivation and Design have the right boundary.
The purpose is to extract transferable reasoning patterns, not to copy a source
paper's section order, headings, terminology, or narrative surface.

Separate three levels when using this reference:

1. **Presentation invariants** apply to almost every technical paper: each
   sentence and paragraph must advance a recoverable relationship; terms and
   evidence must be introduced before they are used; and each subsection must
   remain locally understandable.
2. **Transferable reasoning patterns** are useful when the manuscript has the
   same kind of problem, such as a workload-driven opportunity, a design
   tradeoff, or a failure model.
3. **Paper-specific structures** are historical examples only. Copy them only
   when the target paper independently has the same dependency graph, and even
   then copy the relationship rather than the visible layout.

Preserve the target paper's actual contribution and evidence.

## Source set

- [WiscKey, FAST 2016](https://www.usenix.org/system/files/conference/fast16/fast16-papers-lu.pdf)
- [Slacker, FAST 2016](https://www.usenix.org/system/files/conference/fast16/fast16-papers-harter.pdf)
- [IRON File Systems, SOSP 2005](https://doi.org/10.1145/1095809.1095830)
- [All File Systems Are Not Created Equal, OSDI 2014](https://www.usenix.org/system/files/conference/osdi14/osdi14-paper-pillai.pdf)
- [The Unwritten Contract of Solid State Drives, EuroSys 2017](https://doi.org/10.1145/3064176.3064187)
- [Protocol-Aware Recovery for Consensus-Based Storage, FAST 2018](https://www.usenix.org/system/files/conference/fast18/fast18-alagappan.pdf)

## Presentation invariants

### 1. Make every sentence move the argument

A sentence should continue, qualify, contrast, explain, or conclude something
that the previous sentence made available. A useful local chain is:

```text
sentence A: observation or claim
→ sentence B: interpretation, condition, or contrast
→ sentence C: consequence, pressure, or requirement
→ sentence D: the next concept or operation
```

Do not use a connective as a substitute for the missing relationship. If the
reader cannot say whether the next sentence is a continuation, cause,
consequence, contrast, scope condition, or example, the transition is not yet
presented clearly.

Use the smallest concrete phrase that carries the relationship forward. Repeat
the object, metric, result, or pressure when needed. Replace vague references
such as “this,” “these gains,” or “such systems” when their antecedent is not
recoverable from the immediately preceding sentence or paragraph.

### 2. Give each paragraph one job and a visible handoff

A paragraph normally contains a local claim, the evidence or reasoning needed
to support it, and an implication that makes the next paragraph necessary. The
last sentence should establish the carried object, result, or unresolved
question; the next paragraph should begin with that object or question and
state its new role. Do not add two bridge sentences that announce the same
move.

### 3. Make every subsection autonomous

Open a subsection with its local question or purpose, name its subject, and
state the minimum conditions needed to follow the argument. A short migration
sentence may connect it to the prior subsection, but the reader should not have
to reread the prior subsection to reconstruct the subject or purpose. End with
the implication that the next subsection needs.

### 4. Introduce evidence and concepts before interpretation

Orient the reader to a metric or operation before reporting its number or
explaining its implementation. State what the object acts on, why it appears
here, and what its result enables; for an input, state where it comes from and
what the system does with it. Introduce an entity before using it to qualify a
claim, and state the evidence source before interpreting a figure or table.
Prefer this operational orientation to a defensive or tautological sentence
such as `we define X as X`; use a formal definition only for a precise boundary,
notation, or invariant. Separate measured observation, intended benefit,
mechanism, and hypothesis. This invariant applies at sentence, paragraph,
subsection, and section boundaries.

### 5. Preserve scope and claim strength through transitions

Carry workload, configuration, baseline, and exception conditions with the
claim they qualify. A transition must not silently turn a workload tendency
into a guarantee, or an intended benefit into a measured result. If the next
unit changes scope, state the change explicitly.

## Transferable reasoning patterns

### 1. Start from a decision-relevant observation

The strongest openings do not begin with a broad claim that the system is
important. They establish an existing design assumption, a measured workload
property, or a failure scenario that makes a design decision consequential.
WiscKey first connects LSM amplification to SSD properties. Slacker first
measures where container startup time and transferred data are spent. All File
Systems first shows a concrete crash state before naming persistence properties.

Use this test: if a sentence does not change what a reasonable system designer
would choose, it is probably context rather than Motivation evidence.

### 2. Derive an opportunity before naming the mechanism

The normal chain is:

```text
existing assumption or workload property
→ measured limitation, failure, or resource pressure
→ high-level opportunity or requirement
→ design decision
```

The opportunity must remain true if the proposed implementation is replaced.
For example, “only a small fraction of container data is needed before useful
work” supports avoiding eager transfer; it does not by itself prescribe NFS,
snapshot IDs, or lazy cloning. Keep the implementation in Design.

### 3. Make a central decision explicit, then enumerate its consequences

WiscKey states a simple central decision—sort keys while storing values
separately—then makes the resulting range-query, garbage-collection, and crash
consistency problems explicit. Each later mechanism answers one consequence of
that decision. A design subsection should therefore be explainable as:

```text
decision → new problem or invariant → mechanism → measured benefit and cost
```

Do not present the mechanisms as an unexplained component list.

### 4. Align analysis units with design units when the evidence supports it

Slacker's four workload-analysis questions in §4 correspond directly to its
four design subsections in §5. The transferable pattern is the explicit
observation-to-decision mapping, not the number four or the section order. Use
this correspondence when the manuscript's dependency graph supports it, but do
not force a one-to-one mapping when several observations motivate one design or
one observation requires several mechanisms.

### 5. State design goals as constraints, not slogans

Slacker states goals such as fast push/pull, no long-running slowdown, reuse of
existing storage, and limited Docker changes before explaining the architecture.
Goals are useful when each later choice can be checked against them. Convert
generic goals into observable constraints with a condition, resource, or
compatibility boundary.

### 6. Define the failure model or taxonomy before comparing solutions

IRON builds a failure model and analysis categories before its system. All File
Systems introduces concrete crash states and persistence properties before
studying applications. Protocol-Aware Recovery classifies recovery actions by
safety, availability, recovery time, and complexity before introducing its
protocol-aware approach. This pattern is appropriate when “correct,” “safe,” or
“fast recovery” otherwise has multiple meanings. It is conditional, not a
required section in every paper.

### 7. Let figures carry the reasoning that prose cannot carry locally

Use a scenario timeline for a failure sequence, a taxonomy table for competing
behaviors, or a workload-to-design mapping when the reader must track several
states or correspondences. A Motivation figure should show the problem,
pressure, or opportunity. An architecture or mechanism figure belongs in
Design. Every figure must answer a reader question and have a prose claim that
it supports.

### 8. Evaluate the decision, its benefit, its cost, and its scope

The evaluation should follow the paper's design decisions and test the claims
that motivated them. WiscKey evaluates throughput and amplification, then
separately tests range-query behavior, garbage collection, crash recovery, and
known regressions. Slacker checks startup improvements and also long-running
performance, because reducing startup work could otherwise move the cost to
steady-state execution. Record for each design unit:

```text
claim or improved metric → introduced cost → net effect under workload/configuration
```

Do not let a headline speedup stand in for the cost or applicability analysis.

### 9. Keep scope and exceptions visible

WiscKey explicitly names workloads where it can lose to LevelDB. A good story
does not hide a counterexample; it states the condition under which the
decision is useful and lets Evaluation test that condition. If a requirement
is out of scope, mark it as a boundary rather than silently weakening it.

### 10. Organize Evaluation as a claim sequence

Strong systems evaluations usually make the evaluation questions explicit,
establish the shared setup once, answer the central end-to-end question, and
then explain the result through breakdowns, ablations, or controlled analyses.
They finish with the conditions that determine whether the result generalizes:
real applications, workload variation, scalability, stability, or known
limits. The exact parts vary, but a useful candidate progression is:

```text
questions → setup → headline result → attribution or breakdown
→ cost and secondary paths → generality, scalability, or limits
```

WiscKey follows a headline storage result with separate checks for range
queries, garbage collection, and crash recovery because key–value separation
changes those paths. Slacker first measures the startup benefit, then checks
long-running performance and cache sharing because lazy transfer can move cost
to later execution. IRON and All File Systems define the failure or crash
model and analysis categories before presenting large result sets, so the
reader can interpret each observation against a stable vocabulary. The
Unwritten Contract turns many measurements into a small set of reusable rules
and uses those rules to organize the analysis rather than presenting isolated
charts.

Transfer the reasoning pattern, not the source paper's subsection names. For a
target paper, record the central evaluation question and the claim each result
group tests. A result group should answer one question, state its metric and
conditions, report the observation, explain only the supported mechanism, and
state the cost, boundary, or consequence that determines how the result should
be used.

When a result group is a performance breakdown, keep the proposed design as
the subject. State its headline result first, explain why attribution is
needed, and then walk through the relevant design decisions in Design order.
Use baselines as compact comparison anchors; a baseline's implementation is
not a second topic unless the evaluation question makes it one. Retain an
operation or internal detail only when it explains the focal metric, an
introduced cost, a measured boundary, or a direct comparison. This prevents
Evaluation from becoming a sequence of data descriptions followed by detached
analysis.

### 11. Test the decision and its consequences

Evaluation should test the central design decision and the problems it creates,
not merely repeat the implementation's component list. For each design unit,
trace:

```text
design decision → claimed benefit → affected metric or path
design decision → introduced cost or risk → affected metric or path
workload/configuration → observed net effect and scope
```

Use a controlled comparison, ablation, or microbenchmark when the paper needs
to attribute a result to one mechanism. Use an end-to-end result when the
claim concerns system behavior. Keep intended benefits, measured effects, and
interpretations separate. If the evidence cannot establish the mechanism,
report the correlation or leave the explanation unresolved.

### 12. Make Evaluation answerable without figure backtracking

The opening of the Evaluation section or subsection should state the question
or purpose, not start with a raw number or an unexplained figure reference.
The first-sentence-only sequence should recover the progression from question
to result to explanation or scope. Figures and tables are evidence anchors;
they do not automatically define the narrative order. A figure-by-figure
rewrite is a warning sign when several figures answer one question or when a
later figure supplies the condition needed to interpret an earlier one.

## Paper-specific structures: use only as evidence for a relationship

The following source structures illustrate relationships that may be reused
when independently supported by the target paper:

- WiscKey's `central decision → new challenges → mechanisms` sequence.
- Slacker's `workload question → corresponding design response` mapping.
- IRON, All File Systems, and Protocol-Aware Recovery's
  `failure model/example → taxonomy or invariant → design` progression.

Do not copy their section names, subsection counts, or paragraph order. First
reconstruct the target paper's dependency graph; then select only the pattern
that repairs or clarifies that graph.

## Structure-search procedure

When comparing candidate structures, ask:

1. Does the candidate expose the decision-relevant observation before the
   design choice it motivates?
2. Can each major Design unit be traced to a prior observation or requirement?
3. Does each design consequence appear before the mechanism that addresses it?
4. Does Evaluation follow the Design order and test benefit, cost, and scope?
5. Can a reader understand Motivation with Design hidden?

Prefer the candidate that answers these questions with the fewest deferred
definitions and the least reader backtracking. Apply presentation invariants
before optional source-paper patterns. Do not adopt a paper's exact section
order merely because it appears in the source set.

## Five-answer reading worksheet

For a close reading or a story discussion, record these answers for each paper
before proposing a revision:

1. Which existing system assumption does the paper challenge?
2. Which observation or failure makes the problem worth solving?
3. Which central idea changes a design decision?
4. Why does that decision require each subsequent mechanism?
5. Which claim, cost, or applicability condition does each evaluation group
   test?

The worksheet is an analysis aid. Do not copy a source paper's terminology,
section names, or claims into the manuscript without evidence from the target
paper.

