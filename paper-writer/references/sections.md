# Section Contracts, Motivation, and Design

Read this when outlining or restructuring a section, or when Motivation and
Design are in scope. Each section answers its own question at its own
abstraction level. Orders below are menus of supported patterns, not
templates: pick the one the dependency graph supports and record the choice
and reason in the outline. For transferable patterns from published papers,
see [model-paper-patterns.md](model-paper-patterns.md).

## 1. Section contracts

| Section | Answers | Common order |
| --- | --- | --- |
| Abstract | the problem, the central insight or approach, the main supported result | problem → insight → approach → result → implication |
| Introduction | why the problem matters, the opportunity, the approach, the evidence | setting → decision-relevant problem → evidence or pressure → insight → approach preview → contributions |
| Background | concepts, assumptions, and existing behavior later reasoning needs | concept or interface → relevant operation → existing behavior or constraint → implication for the next section |
| Motivation | what problem or opportunity follows from workload, existing behavior, constraints, and observations (§2) | setting → observation → limitation or pressure → opportunity → insight or requirements |
| Design | how the proposed choices satisfy the requirements, and what each costs (§3) | selected pattern from §3 |
| Implementation | the data layout, control flow, state transitions, and engineering choices needed to reproduce or assess the system | design contract → choice → operation or state transition → invariant or exception → resource cost |
| Evaluation | what question is tested, under which conditions, and what the evidence shows | see [evaluation.md](evaluation.md) |
| Related Work | how the design relates to each prior approach | see [related-work.md](related-work.md) |
| Discussion / Limitations | where the design applies, what it gives up, what remains open | claim or mechanism → bound or condition → consequence |
| Conclusion | the problem, the insight, and the supported result, closing the story | no new evidence, mechanisms, or unprepared claims |

The Introduction may preview Design and results; that preview never licenses
implementation detail in Motivation. Background may explain a baseline
mechanism when an observation needs it, but never presents the proposed
mechanism as established context. Related Work is not a second Motivation.

## 2. Motivation: recover a design-independent argument

**Two chains, kept apart.**

```text
Motivation: setting → observation or existing behavior → limitation or pressure
            → opportunity or missing capability → design-independent insight or requirements
Design:     requirements → obvious or naive solution → its limitation
            → design principle → proposed mechanism
```

The Design chain can explain why the final design is needed, but it is never
evidence for the Motivation chain. A naive solution is useful as a failed
approach; its home is the Design opening, not the core Motivation argument.

**Abstraction firewall.** Motivation may name established domain objects and
the needed capability or relation. It does not introduce or reverse-engineer
the proposed component, data structure, encoding, identifier, algorithm step,
or policy. A term that is understandable locally is still a leak when its
meaning comes from a later implementation layer; treat it as a leak, not as a
definition to add. Removing a mechanism's name or adding "could" does not turn
it into an opportunity. "To reduce communication, we introduce a three-level
cache" introduces a solution without the observation.

**Sealed pass (before reading Design).** From Background, Motivation, and the
evidence only, record:

```text
setting and reader question | observations and sources | limitation or pressure
opportunity | design-independent insight candidates | requirements and scope
highest abstraction level allowed | unresolved premises or evidence gaps
```

If an opportunity cannot be stated without a proposed detail, report `Needs
context` or a leak; never import the detail.

**Concept layers.** For each concept record its first use, prerequisite, and
layer: `motivation-visible` (setting, workload, existing behavior, pressure,
capability, requirement), `background-known` (established interface or
baseline behavior), or `design-only` (proposed structure, encoding,
identifier, algorithm, component, placement). State the purpose or pressure
first, then the object at the level that purpose needs, then the relation;
defer the representation to Design. Prefer "To locate retained state, the
system tracks each item and where it is stored" over "the system keeps a global
table". If an existing system's representation is itself the observation, keep
it with the scope that makes it relevant.

**Classify each unit** as context, observation, pressure, opportunity, insight,
requirement, naive solution, proposed design, or design consequence. The last
three generally belong after Motivation. Return a **leakage map**: unit,
role, reason, destination. Moving a unit to Design beats deleting a supported
premise.

**Tests for each candidate opportunity or insight:**

1. *Substitution:* could a different implementation satisfy it? If not, it is
   a design choice.
2. *Redaction:* without mechanism names and operations, does the
   observation-to-opportunity argument still hold?
3. *Evidence:* does it rest on workload behavior, existing systems,
   constraints, or measurements, not on the proposed design's success?
4. *Requirement:* can it be stated as a capability, boundary, or condition
   without naming a component?
5. *Scope:* does it keep the workload, resource regime, or failure case that
   makes it meaningful?

Prefer the shortest insight that survives; never fall back to a slogan such as
"improve performance". If several survive, show them to the author with their
observations and the design assumptions each avoids. In autonomous work,
select one only when the evidence leaves no substantive ambiguity.

**Traceability (after the sealed pass).** Read Design and map each major
choice: Motivation requirement → design choice → mechanism → consequence. Mark
each choice mapped, unmapped, or depending on a missing requirement. A
requirement with no Design mapping is open, out of scope, or an author
decision. Never rewrite Motivation to make an existing Design look necessary.
Record the sealed contract in the outline so later passes do not rediscover a
different problem statement. After revision, repeat both passes: Motivation
must stand with Design hidden, and Design must map back to it.

## 3. Design: choose the reader's path

Record the supported relations first: requirement or opportunity, **design
challenge** (the implementation-independent constraint the design must meet
once Motivation has established the opportunity; neither a repeat of
Motivation nor the component's name), decision, component responsibility or
contract, mechanism or representation, operation or state transition,
consequence or cost. Every mechanism, operation, layout, or update has a
supported requirement, challenge, or purpose; a unit that only says what the
system does is incomplete. A missing edge is `Needs context`, never "for
performance".

| Pattern | Reader-facing order | Use when |
| --- | --- | --- |
| decision–consequence–mechanism | decision → new tension or invariant → mechanism → consequence | a choice creates the problem the next mechanism solves |
| component contract | responsibility → contract → realization → boundary or cost | the reader first needs what a component promises |
| workflow or dataflow | input or state → stages → ownership or invariant → result and cost | the design is a path through states or data |
| invariant first | invariant → representation or algorithm → preserving operations → limits | correctness is the organizing idea |
| interface then implementations | responsibility → selected operations → implementation families → per-family realization | several implementations serve one interface |
| lifecycle | initial state → event → observable state → recovery or update | behavior over time is the main dependency |
| failure to mechanism | failure or constraint → required property → mechanism → residual cost | a concrete failure explains the mechanism |
| architecture overview | system responsibility → component roles → critical flow → details | the reader first needs the map |

These are alternatives, not steps. If two fit, show both to the author. Never
pick a pattern because the old draft used it.

- **Granularity.** A component is its own unit when it has a distinct
  challenge, contract, non-parameter decision, dependent mechanism, or later
  evaluation claim. Otherwise it stays inside its parent. Do not promote every
  data structure into a named unit.
- **Overview only when needed.** An overview states the challenge, the overall
  principle, the major components and their relations, and where details
  follow. It does not explain layouts or update algorithms.
- **Logical before physical.** State a component's role and what it associates
  before its layout, identifier, or backing file; give the reason for the
  representation in the same unit. Separate aggregation, representation, and
  updates when they carry different invariants or costs. Do not describe an
  update before saying what state it changes and why that state matters.
- **First unit concise.** Challenge → responsibility → role in the overall
  design → deferred details. Not the whole architecture in one paragraph, and
  no bridge paragraph that only repeats a name.
- **Flags:** a component without a prior challenge; a representation before
  the concept it implements; aggregation, layout, and updates mixed without a
  reason; a component list that never says how the design uses each unit; a
  Motivation restatement or Evaluation result inside Design; a named unit no
  different from its parent.
