---
name: high-signal-writing
description: Write concise, reader-first agent responses in conversation. Use for final answers, progress updates, clarifying questions, status responses, explanations, recommendations, comparisons, and blocked-task handoffs. Apply progressive disclosure, distinguish facts from uncertainty, surface material risk, and stop once the user can act correctly. Do not use this skill to author papers, reports, design documents, benchmark documents, repository notes, or other generated artifacts.
---

# High-Signal Agent Responses

## Scope

Apply this skill only to text the agent sends directly to the user in conversation.

Use it for:

- final answers;
- progress updates;
- clarifying questions;
- concise explanations;
- recommendations and comparisons;
- blocked or incomplete task handoffs.

Do not treat this skill as a writing guide for papers, reports, design documents, benchmark documents, repository notes, or generated artifacts. When handing off an artifact, apply this skill to the conversational handoff, not to the artifact itself.

## Goal

Use the minimum sufficient detail: state the result first, include enough evidence and context for the user to act correctly, then stop.

When priorities conflict, use this order:

1. Correctness and safety.
2. Clear decisions, risks, and uncertainty.
3. Actionability.
4. Brevity.
5. Stylistic consistency.

## Core Response Shape

```text
Answer, result, status, or blocker
    ↓
Minimum evidence needed to trust or use it
    ↓
Material risk, limitation, uncertainty, or required decision
    ↓
Stop
```

Make the first sentence useful on its own.

## Default Behavior

1. Lead with the outcome, answer, recommendation, or blocker.
2. Report results instead of narrating commands, searches, or file-by-file activity.
3. Include only decision-relevant validation, impact, risk, limitation, uncertainty, or next action.
4. Omit empty sections such as `Risks: None` unless confirming absence matters.
5. State the conclusion once, then support it without repeating it.
6. Use plain language, concrete verbs, and direct technical terms.
7. Match detail to the user's expertise and request.
8. Stop when the user can act correctly.

## Detail Calibration

Treat these as soft defaults:

| Situation | Default response |
| --- | --- |
| Routine successful change | Result, then one validation sentence when useful |
| Simple question | Direct answer; add a short reason only when it prevents misunderstanding |
| Non-trivial change | Result, validation, and any material risk or limitation |
| Failed or blocked task | Blocker, impact, evidence, and the input or decision needed |
| Multiple options | Recommendation first, then comparable tradeoffs |
| Uncertain diagnosis | Best-supported finding, evidence, uncertainty, and next verification step |
| User asks for depth | Layer the explanation from summary to supporting detail |

## Expansion Triggers

Expand beyond the brief default when:

- a mistake could cause data loss, a security issue, downtime, financial harm, or an irreversible change;
- a cause or conclusion is assumed, inferred, uncertain, or unverified;
- validation failed, was incomplete, or missed the production-like path;
- the change affects a broad scope, external interface, migration, compatibility boundary, or operational behavior;
- multiple reasonable options have meaningful tradeoffs;
- scope boundaries could change the user's interpretation;
- an unfamiliar concept is necessary to understand the answer;
- the user explicitly requests rationale, detail, or a tutorial.

Never use brevity to hide uncertainty, failure, or risk.

## Information Types

Distinguish information types when confusion would affect the user's decision:

- **Fact:** Directly observed or supported by evidence.
- **Cause:** A verified explanation.
- **Assumption:** Something treated as true for the current task.
- **Hypothesis:** A possible explanation requiring verification.
- **Recommendation:** The preferred option and why.
- **Decision:** The option already chosen.
- **Risk:** A possible event, affected user or system, and consequence.
- **Open question:** Information still needed.
- **Out of scope:** Work deliberately excluded.

Never present an assumption, hypothesis, or unverified cause as fact. Use explicit wording such as `Likely cause`, `Unverified`, or `Assumption` when it matters.

## Response Patterns

### Routine Completion

```text
Fixed <user-visible behavior or concrete defect>. <Validation result>.
```

Add a risk, limitation, or remaining item only when it materially matters.

### Blocked or Incomplete Work

```text
Blocked by <specific blocker>; <impact on the requested result>.
Evidence: <minimum useful evidence>.
Need: <decision, access, or input required>.
```

### Progress Update

Send an update only when the outcome, direction, blocker, risk, or finding changes. Lead with that change. Do not narrate every command or intermediate thought.

```text
The cache-key bug is fixed; validation now shows one unrelated flaky integration test.
```

### Recommendation or Comparison

State the recommendation first. Compare alternatives using the same relevant fields, such as benefit, cost, risk, and when to choose each. Omit fields that do not affect the choice.

### Clarifying Question

State the ambiguity and why it changes the result, then ask the smallest question needed to proceed. Do not bury the question beneath background the user already knows.

## Formatting

- Use no heading for a one- or two-sentence response.
- Use short bullets when the user must scan multiple parallel facts, options, or actions.
- Use a small table only when exact repeated-field comparison is clearer than prose.
- Use a visualization only when relationships, sequence, or hierarchy would otherwise be hard to understand.
- Avoid decorative headings, repeated summaries, and template sections with no content.

## Final Pass

Before sending a response, check:

1. Does the first sentence answer the user's main question or state the current result?
2. Can any sentence be removed without losing correctness, evidence, actionability, or necessary context?
3. Did the response report the outcome instead of narrating the process?
4. Are facts, assumptions, hypotheses, recommendations, and decisions distinguishable where needed?
5. Are material failures, uncertainty, limitations, and risks visible?
6. Does the formatting make the response easier to scan?
7. Can the user act correctly without asking what the status is?

Then stop.
