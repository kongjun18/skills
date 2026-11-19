# Independent Review Rubric

Use this rubric when the user asks for a review without supplying opinions.
Its output is a draft that then goes through the verification and delivery
sections of [SKILL.md](../SKILL.md). Every judgment must be traceable to a
manuscript location.

## Intake

- Record the manuscript version and what is available: full paper, excerpt,
  appendices, artifacts. Restrict conclusions to what you read, and read the
  complete paper before making any cross-section judgment.
- Record the target venue, year, track, and paper type if known. Use that
  venue's current official instructions for scale, length, and artifact
  expectations. Never import another venue's rules or assume a universal
  scoring scale.
- List the paper's claimed contributions in the authors' own words, each with
  its location. This list drives every dimension below.

## Calibrate to the paper type

A new system, algorithm, measurement study, benchmark, deployment or
experience report, reproducibility study, or vision paper each owes a
different kind of novelty and evidence. Domain-specific concerns (crash
recovery, consistency, query semantics, device endurance, and so on) apply
only when the paper's claims depend on them.

## Dimensions

Assess each dimension against the contribution list. For each one record the
evidence, the strengths, and the concerns, ranked by their effect on the
paper's conclusions. Mark a dimension `not assessed` when inputs are missing;
an unassessed dimension never counts as passed.

| Dimension | Question | Notes |
| --- | --- | --- |
| Contribution and positioning | Is the problem important to the intended audience? What does the paper advance beyond the closest work, and by how much? | Verify every "already done in X" or "missing related work" claim through paper-integrity's citation rules before stating it |
| Technical soundness | Do the assumptions, mechanisms, algorithms, and reasoning support the claims? Are failure cases and applicability limits handled? | Build a claim-to-argument map; flag unstated assumptions |
| Evaluation and evidence | Do the experiments test the claims with fair baselines, credible measurement, adequate workloads and scale, ablations, and uncertainty? | Build a claim-to-evidence map; distinguish "not shown" from "shown false" |
| Reproducibility and responsible research | Could others understand and check the work from the methods and artifacts? Are data provenance, deployment constraints, and ethics addressed where relevant? | Report gaps; do not demand artifacts the venue does not expect |
| Presentation | Can a reader follow the problem, challenges, key idea, and results? | Apply paper-presentation-review's criteria read-only; summarize only what affects the review |
| Editorial accuracy | Are numbers, units, labels, and cross-references consistent? | Use paper-hygiene `audit` with `consistency`; minor items go last in Details |

## Synthesize

- Pick the decisive strengths and weaknesses: at most three of each, ranked
  by their effect on the paper's conclusions.
- For each weakness, give the claim, the gap, why the gap matters, and the
  specific clarification or experiment that would resolve it.
- Write questions for the authors where the answer could change your
  assessment.
- State your confidence and its limits: unread sections, inaccessible
  sources, areas outside your expertise.
- Give a recommendation only when the user asks for one and every dimension
  it depends on was assessed.
