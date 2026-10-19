# Evaluation Patterns from Systems Papers

Use this reference only when selecting or reviewing an Evaluation structure.
It extracts reusable reasoning patterns from O3-LSM and the Remzi H.
Arpaci-Dusseau paper set. It is a source of decision rules, not a template for
section titles, subsection counts, or figure order.

## 1. The common macro pattern

Several strong systems papers make the Evaluation questions explicit, define
the shared setup, answer the main system-level question, explain the result,
and then test the consequences and boundaries of the design. A useful
candidate progression is:

```text
evaluation questions
→ shared setup and measurement scope
→ end-to-end or headline result
→ attribution: breakdown, ablation, or controlled comparison
→ secondary paths and design costs
→ real application, generality, robustness, or scalability
→ supported limits and implications
```

This is a dependency pattern, not a mandatory list. Omit a stage when the
paper has no supported claim for it. Combine stages when they answer one
question. Move a stage earlier only when a later result is required to
interpret an earlier one.

### Design-centered performance breakdowns

When a result group explains the proposed system's measured performance,
preserve an asymmetric narrative:

```text
proposed-system result → reason for attribution → proposed design effect
→ introduced cost → workload/configuration-dependent net effect
→ concise baseline contrast
```

The proposed design is the subject. Baselines anchor the comparison and are
usually described in one sentence each. Their implementation details belong in
the breakdown only when the evaluation question directly tests that mechanism
or when the detail explains the proposed system's result. A breakdown should
not begin with a baseline's numbers, and it should not introduce a design
operation merely because the operation appeared in the Design section.

This order keeps Evaluation explanatory: first establish what happened, then
explain why it happened. Use the measured effect's vocabulary—such as latency,
throughput, retrieval overhead, or storage traffic—unless the question itself
concerns an access path. The purpose of the breakdown should be visible in the
transition from the headline result, rather than inferred from a list of
figures.

### O3-LSM as a modern reference

O3-LSM opens its Evaluation with explicit questions about overall performance,
the contribution of each major design, and behavior in real applications and
at scale. It then uses a recognizable progression:

```text
experimental setup
→ overall performance against baselines
→ performance breakdown and ablation
→ detailed cost and path analyses
→ real-world application integration
→ scalability and resource elasticity
```

The transferable point is the question-to-evidence mapping. The paper does
not ask the reader to infer why a figure exists from its axes; each group of
results has an evaluation purpose. Its breakdowns also make the system-level
result explainable: write amplification, flush latency, read-path behavior,
network traffic, and shard-level effects expose where the benefit and cost
come from. The exact O3-LSM subsections should not be copied into another
paper. Use this pattern only when the target has the same claim dependencies.

The same pattern has an evidence boundary: a result group may establish a
component-level effect without establishing the end-to-end or request-level
effect of that component. Present that boundary as part of the evaluation
argument. Do not treat it as a missing prose step or as a reason to propose a
new experiment during presentation review.

## 2. Principles from the Remzi paper set

### WiscKey: test the decision and the consequences

Key–value separation is a central decision. Its Evaluation therefore tests the
headline throughput and write-amplification benefit, then separately checks
range queries, garbage collection, crash recovery, and known regressions. The
general principle is:

```text
central decision → claimed benefit → new path or invariant it affects
→ cost or failure mode introduced by the decision → measured boundary
```

A headline speedup is incomplete when the decision changes other operations.

### Slacker: validate the intended shift without hiding its cost

The paper first measures faster push and pull, then checks long-running
execution and cache behavior. This is necessary because lazy fetching moves
work from startup to later access. The reusable pattern is:

```text
primary benefit → possible cost transfer → steady-state or repeated-use test
→ workload-dependent net effect
```

The next experiment is motivated by the previous result. It is not an
unrelated collection of benchmarks.

### IRON: define the analysis frame before presenting many results

IRON defines a failure model and a taxonomy of detection and recovery before
summarizing behavior across file systems. The framework gives every result a
stable interpretation. Use this pattern when a result is ambiguous without a
shared vocabulary:

```text
failure or operating model → analysis categories → per-system observations
→ cross-system comparison → distilled policy or lesson
```

Do not add a taxonomy merely to make a short evaluation look structured. It is
useful when the evidence spans many cases or dimensions.

### All File Systems Are Not Created Equal: connect evidence to requirements

The paper starts from concrete crash states, identifies persistence properties,
and tests applications under different file-system behaviors. It then groups
vulnerabilities by atomicity, ordering, and durability, evaluates current file
systems, and studies the effect of a proposed property change. The principle
is:

```text
concrete failure → property or requirement → workload/checker evidence
→ pattern across applications → implication for system designs
```

The evaluation is organized by what must be established, not by the order in
which the tool happened to run experiments.

### The Unwritten Contract of Solid State Drives: turn measurements into rules

The paper uses many measurements to derive a small set of rules about SSD
behavior and then applies those rules to systems and workloads. The reusable
pattern is:

```text
measurement family → invariant or rule → consequences across layers
→ design guidance and conditions
```

When an Evaluation contains many charts, look for the rule or mechanism that
unifies them. Do not narrate each chart as an independent result if several
figures support one conclusion.

### Protocol-Aware Recovery: classify tradeoffs before comparing methods

Recovery methods are compared along safety, availability, recovery time, and
complexity. The general principle is to establish the shared outcome axes
before reporting which method is better:

```text
failure scenario → required safety/availability property
→ comparable method outcomes → recovery cost and boundary
```

This prevents a result that improves one axis from being presented as a
uniform improvement.

## 3. The general Evaluation argument unit

For each result group, build this contract before prose:

```text
question:
claim being tested:
metric and purpose:
baseline or comparison:
workload/configuration:
evidence source:
observed result:
supported explanation:
introduced cost or limitation:
net effect and scope:
next question or implication:
```

Keep these layers separate:

- **Claim:** what the experiment establishes.
- **Evidence:** what the figure, table, trace, or measurement reports.
- **Explanation:** what mechanism the evidence supports.
- **Condition:** when the result holds, changes, or stops holding.

Use a controlled comparison, ablation, or microbenchmark when attribution is
needed. Use an end-to-end comparison for system-level behavior. If the
measurement establishes a correlation but not a mechanism, state the
correlation and leave the mechanism unresolved.

## 4. Structural checks derived from these patterns

Before writing, the reviewer should answer:

1. What Evaluation question does this section or subsection answer?
2. Which result establishes the central claim before detailed attribution?
3. Which later result checks a cost, consequence, or workload boundary of that
   claim?
4. Does every breakdown component map to a Design decision or requirement?
5. Are setup, result, explanation, and scope ordered so the reader need not
   backtrack?
6. Are multiple figures supporting one claim grouped under that claim rather
   than narrated one by one?
7. Does the first-sentence-only sequence recover the evaluation progression?

For a design-centered performance breakdown, also ask:

8. Is the proposed system's headline result stated before the breakdown?
9. Does the breakdown state why attribution is needed and follow Design order?
10. Are baselines compact comparison anchors rather than co-equal implementation
    subjects?
11. Does every retained operation or detail explain the focal metric, an
    introduced cost, a supported boundary, or a direct comparison question?

If these answers are unavailable, the Evaluation structure is not ready for
prose rendering even when every figure has a correct local description.
