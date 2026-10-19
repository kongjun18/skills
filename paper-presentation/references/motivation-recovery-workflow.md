# Motivation Recovery Workflow

Use this workflow before revising Motivation when the current text may have
been written backward from Design. It recovers the high-level argument from
the supplied observations and separates it from the later reasoning that
turns requirements into a concrete system. The workflow is generic and does
not assume a particular research area.

## 1. Keep the two reasoning chains separate

The design-independent Motivation chain is normally:

```text
setting or workload
→ observation or existing behavior
→ limitation, failure, or resource pressure
→ opportunity or missing capability
→ design-independent insight or requirements
```

The Design chain may then be:

```text
requirements
→ obvious or naive solution
→ limitation of that solution
→ design principle
→ proposed mechanism
```

The second chain can explain why the final design is needed, but it should not
become the evidence for the first chain. A naive solution can remain useful in
the paper as a failed approach or design-space comparison. Its normal home is
the Design opening or a design subsection, not the core Motivation argument.

Keep an abstraction firewall between these chains. Motivation may name the
reader-facing capability or missing relation, but it should not preempt the
representation, encoding, identifier, data structure, algorithm, or component
that Design later uses to provide it. A term can be understandable and still
be misplaced when its meaning comes from a later implementation layer. Treat
such a term as a Design leak rather than repairing it with an inline
definition.

## 2. Run a sealed extraction pass

Before using Design to justify or repair Motivation, read only the material
needed to establish the setting, observations, existing behavior, constraints,
and evidence available to the reader. Build a temporary contract with:

- setting and reader question;
- observations and their sources;
- limitation, failure, or pressure;
- opportunity or missing capability;
- design-independent insight candidates;
- requirements and scope conditions;
- the highest abstraction level that Motivation is allowed to use; and
- unresolved premises or evidence gaps.

Do not use proposed components, data structures, algorithms, encodings,
routing policies, placement decisions, or implementation-specific mechanisms
to complete this contract. If the available Motivation cannot establish an
opportunity without one of those details, report `Needs context` or a design
leak instead of silently importing it.

## 3. Enforce concept order and abstraction level

For each sentence, build a small first-use map with the concept's layer and
its prerequisite. Use these layers as a guardrail, not as a fixed taxonomy:

- `motivation-visible`: setting, workload, existing behavior, resource
  pressure, high-level capability, or design-independent requirement;
- `background-known`: established interface or baseline behavior that the
  reader needs before the opportunity can be understood; and
- `design-only`: a proposed structure, encoding, identifier, algorithm,
  component, placement, or implementation step.

Check the map in this order:

1. State the purpose, pressure, or reader question.
2. Name the object or capability at the level needed for that purpose.
3. Explain the relation or consequence.
4. Defer a lower-level representation until the operation or requirement that
   it serves has been established in Design.

A sentence such as “a serving system keeps a global index” is weak when it
gives the reader a component before saying what locating or association
problem the component addresses. Prefer a responsibility-first form such as
“To locate retained state, the system tracks each item and the metadata for its
stored representation,” when that is the supported relationship. This is an
illustrative rendering pattern, not a paper-specific term.

Do not introduce an encoding, ID, or data structure merely to make an abstract
object sound concrete. If a representation is needed only to explain the later
implementation, classify it as `design-only` and move it to Design. If an
existing system's representation is itself the observation, keep it only with
the scope and purpose that make it relevant to the Motivation claim.

## 4. Classify the current units

For every paragraph and sentence in the requested Motivation scope, assign an
argument role:

- `context`: setting or established terminology;
- `observation`: workload property, existing behavior, or measured fact;
- `pressure`: limitation, failure, resource cost, or tension;
- `opportunity`: a high-level capability that could be improved;
- `insight`: a design-invariant relation or principle that several solutions
  could satisfy;
- `requirement`: a condition a solution should meet;
- `naive solution`: an obvious approach introduced to expose a limitation;
- `proposed design`: the paper's concrete choice or mechanism; or
- `design consequence`: a mechanism-specific cost, benefit, or evaluation
  result.

The last three roles generally belong after Motivation. Keep an existing
baseline or failed approach in Motivation only when it is necessary evidence
for the high-level pressure and is presented as existing context rather than
as the paper's solution.

Return a leakage map with the unit ID, role, reason, and suggested destination.
Moving a unit to Design is preferable to deleting a supported design premise.
Also record premature concepts, their first dependent use, the missing
prerequisite, and the abstraction layer where they belong.

## 5. Recover the design-independent idea

Apply these tests to each proposed opportunity or insight:

1. **Substitution test:** could a different implementation satisfy the same
   statement? If not, the statement is probably a design choice.
2. **Redaction test:** after removing proposed mechanism names and operations,
   does the observation-to-opportunity argument still hold?
3. **Evidence test:** is the statement supported by workload behavior,
   existing-system behavior, a constraint, or a measured observation rather
   than by the success of the proposed design?
4. **Requirement test:** can the statement be rewritten as a capability,
   boundary, or condition without naming a component?
5. **Scope test:** does it retain the workload, resource regime, failure case,
   or other condition that makes the opportunity meaningful?
6. **Layer test:** can the statement remain true when the proposed
   representation and mechanism are replaced by another implementation? If
   not, it belongs to Design or to a clearly identified baseline observation.

Prefer the shortest supported insight that survives these tests. Do not
replace a missing high-level idea with a vague slogan such as “improve
performance.” If several insights survive, keep them as alternatives with
their supporting observations and the design assumptions each one avoids.

## 6. Reconcile with Design after the contract is stable

Only after the sealed contract is recorded, read Design and run a traceability
pass:

```text
Motivation requirement or insight → design choice → mechanism → consequence
```

Mark each Design choice as mapped, unmapped, or dependent on a missing
requirement. When the current Motivation is actually a naive-solution chain,
split it into:

```text
Motivation: observation → pressure → opportunity/requirement
Design: requirement → naive solution → failure → proposed design
```

Do not rewrite Motivation merely to make an existing Design appear necessary.
If the Design is not supported by the recovered requirements, return the gap
for author discussion.

## 7. Modes and outputs

In `review`, return the sealed Motivation contract, the unit classification,
the leakage map, the recovered opportunity or insight, and located evidence
gaps. Keep the manuscript read-only.

In `discuss`, provide a small set of supported design-independent insight
options. For each option, show the observations it uses, the requirements it
implies, the Design choices it can support, and the information it intentionally
leaves out. Keep the run at `Awaiting alignment` until the author chooses or
adjusts the motivation contract.

In `revise`, use the aligned contract to move or rewrite leaked units, then
reconstruct the Motivation in the selected pattern. Preserve supported
observations and evidence, and return the movement map.

In `auto`, select one option only when the evidence and role classification
leave no substantive ambiguity. Otherwise stop with `Needs context` or
`Awaiting alignment` instead of recovering an insight from later Design facts.

Persist the result as the paper's high-level story or Motivation contract so
later section and prose passes do not rediscover a different problem statement.
