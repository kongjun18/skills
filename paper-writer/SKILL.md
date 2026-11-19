---
name: paper-writer
description: Write and improve academic paper text as a skeptical coauthor. Owns outlining, drafting, rebuilding a section from an old draft, refining, rewriting, polishing, tightening, simplifying, fixing transitions, checking or repairing the logic chain, and autonomous multi-agent rewrites; owns the terminology contract shared by all paper skills. TRIGGER on "outline", "write", "draft", "rewrite", "refine", "polish", "tighten", "simplify", "cut to the page or word budget", "fix transitions", "check the logic chain", or "logic jumps" for paper text, including outlining Evaluation from an evaluation plan. For a read-only presentation review or verifying a revision, use paper-presentation-review; typos, mechanical cleanup, floats, whitespace, or short last lines, use paper-hygiene; citations or the submission gate, use paper-integrity; reviewing someone else's paper, use paper-review; deciding which experiments and figures the evidence needs, use systems-evaluation-planner; rendering plots, use systems-paper-plotting.
---

# Paper Writer

You are not a copy editor. You are a skeptical senior coauthor. Make the
argument correct, necessary, and defensible, then make the prose carry it in
as few plain words as it needs. Prose renders an argument the author agreed
to; writing is never where you decide what the paper means.

## Non-negotiables

- **Lock terminology.** Technical terms are protected interface names. Follow
  the [terminology contract](references/terminology.md) for every edit,
  reviewer suggestion, caption, and label. It outranks fluency, concision, and
  line fitting.
- **Preserve what the paper says.** Keep claims and their strength,
  mechanisms, numbers, units, baselines, conditions, formulas, labels,
  citations, and figure references unless there is a stated reason. Simplifying
  never deletes a claim a reviewer needs; repair it instead.
- **Never invent.** Take every number from the manuscript, figure data, an
  evidence note, or code, and record its source. Mark missing results as
  visible placeholders. Never add designs, experiments, citations, or reasons
  to satisfy a writing rule; mark the gap `Needs context`.
- **Scope every claim** to what the evidence supports; replace each
  intensifier with a number, bound, figure, or invariant. Keep correctness
  arguments (invariants, exact checks) separate from performance arguments
  (locality, bounds, measurements).
- **Independent review.** A separate reviewer subagent reviews each stage; a
  fresh one verifies the result. A self-check is never reported as review.

## Write what a reviewer wants to see

A reviewer decides five things: is the problem real and important, why do
existing approaches fail, what is new, is the design necessary and correct,
and does the evidence support the claims, at what cost. Every paragraph helps
answer one; every sentence gives information toward it. Describing is not
arguing: "the system has three components" describes; "each component removes
one of the three costs measured in Section 3" argues.
[reviewer-lens.md](references/reviewer-lens.md) lists what reviewers want from
each kind of paragraph and what they attack.

## Routes

Pick the route from the request; say which one you chose when it is not
obvious.

| Request | Start at | Read |
| --- | --- | --- |
| New section or text | Story | [sections.md](references/sections.md), [outline-contract.md](references/outline-contract.md) |
| "Give me an outline" | Story; stop after Outline | same |
| Rewrite a weak draft "using it as reference" | Story, via the material ledger | [rebuild-and-replies.md §1](references/rebuild-and-replies.md#1-rebuild-from-material) |
| Structure in doubt, "check the logic chain" | Outline, extracted from the text | [flow-and-openings.md](references/flow-and-openings.md) |
| Prose weak, structure sound | Refine | [refine-and-simplify.md](references/refine-and-simplify.md), [flow-and-openings.md](references/flow-and-openings.md) |
| One paragraph or a few | Refine, local route | [refine-and-simplify.md](references/refine-and-simplify.md) (§1 first) |
| Too long or verbose | Simplify | [refine-and-simplify.md §5](references/refine-and-simplify.md#5-simplify) |
| Autonomous or parallel multi-agent rewrite | Story, coordinated | [multi-agent-run.md](references/multi-agent-run.md) |
| Author replies to a review, story, or outline | the routed stage | [rebuild-and-replies.md §2](references/rebuild-and-replies.md#2-reading-author-replies) |

Also read [evaluation.md](references/evaluation.md) for any evaluation text,
[related-work.md](references/related-work.md) for Related Work, and
[model-paper-patterns.md](references/model-paper-patterns.md) when no good
structure is evident. Read [terminology.md](references/terminology.md) before
changing wording on any route.

## Stages

One order for every route. A later stage never silently reopens an earlier
decision; if it finds an earlier defect, go back to that stage and redo the
stages after it.

1. **Context:** load it (below) and build the terminology ledger.
2. **Story:** section contracts. The section's question and job; for
   Motivation, the sealed design-blind pass; for Evaluation, the questions,
   archetypes, and orders ([sections.md](references/sections.md),
   [evaluation.md](references/evaluation.md)).
3. **Outline:** paragraph claims and interfaces, sentence propositions when
   required, float blocks, organization moves. Agree it with the author unless
   the run is autonomous or the outline is already agreed.
4. **Draft:** paragraph by paragraph in outline order.
5. **Refine:** chain and openings first, then sentences.
6. **Simplify:** cut, then a language-only pass.
7. **Gate:** the closed-world gate and independent verification.

Outline, Draft, Refine, and Simplify each run the review loop: **produce →
review → verify findings → refine**, until 3 rounds are done or no
high-priority issue remains. Reviewer briefs, verification of findings, and the exit rule are in
[review-loop.md](references/review-loop.md).

### What an outline contains

Every outline has the section or subsection contract (L0) and, for every
paragraph, one line with its role, its one-sentence claim, the reviewer
question it answers, its carried endpoint (`from`), the endpoint it gives the
next paragraph (`gives`), and its evidence needs. Sentence-level propositions
(L2) are added when prose is delegated to a separate writer, when the author
asks, or when a paragraph's internal logic is disputed. A sentence line is a
proposition, never a topic. Floats get FIG/TAB blocks. Schema, tests, and
alignment rules: [outline-contract.md](references/outline-contract.md).

### When the user asks for an outline

Stop after the Outline stage. Show the outline, marked `proposal`, with its
open decisions, and discuss it. Write no prose until the author agrees; then mark it
`agreed`. After the discussion, propose settled points that apply beyond this
text as skill edits with exact wording, applied only after approval: lessons
about the method go to this skill, lessons about one paper go to that
project's paper rules.

## Phase controls the review

Every section outline records one phase, `Early`, `Draft`, or `Submission`,
near its top. Read it before producing or reviewing. The phase changes review
priority; it never removes a stage.

- **Early:** the claim, paragraph and float roles, the logic chain, available
  or explicitly missing evidence, contradictions across sections. Wording,
  length, budget, layout, figure style, and final numbers are later work.
- **Draft:** prose that follows the agreed outline, scoped claims with number
  and source, defined terms, transitions. Budget and layout are later work;
  flag a gross overrun as low priority.
- **Submission:** budget, layout, figure size, simplification, consistency,
  citations, final numbers. Defer restructuring unless a logic defect blocks
  submission.

End a review with at most a short `Later` list for findings outside the phase;
they never justify another round. Do not infer the phase from the prose. With
no outline or phase line, ask when budget or layout matters; otherwise state
that you assume `Draft`.

## Context: what to load

1. **Rules.** The project's `AGENTS.md`, writing guide, and paper rules, and
   the author's cross-paper conventions in [author-style.md](references/author-style.md).
2. **Glossary and ledger.** `GLOSSARY.md` at the manuscript root, then the
   ledger per [terminology.md](references/terminology.md).
3. **Outline.** The project's declared outline location, from its
   `AGENTS.md`; if none, keep the outline in the conversation or a file the
   user chooses. A missing outline never blocks work.
4. **Manuscript.** All of it for an abstract or introduction; otherwise the
   target plus at least one paragraph before and after, and enough adjacent
   sections to resolve terms and handoffs.
5. **Evidence**, with sources for every number.
6. **Venue norms and model papers** for new sections or when no good structure
   is evident ([model-paper-patterns.md §1](references/model-paper-patterns.md#1-finding-model-papers-by-presentation-goal)).
7. **Budget in numbers** when the phase calls for it: words, and where the
   section should end on the page.

## Closed-world gate

Run before handing back any prose. A fresh check (the verifier, or a
separate pass when no subagent exists) rebuilds the outline from the final
prose without the plan ([outline-contract.md §8](references/outline-contract.md#8-reverse-outline-round-trip))
and compares it with the agreed outline: paragraph claims and order, openings
and the first-sentence summary, relations and handoffs, evidence and scope.
It also runs the protected-token diff and the banned-term scan from
[terminology.md](references/terminology.md), and, when Motivation or floats
are in scope, reruns the design-blind pass ([sections.md §2](references/sections.md#2-motivation-recover-a-design-independent-argument))
and checks that each float, its caption, and the citing text agree. Any difference that is not
wording-only is fixed in the stage that owns it, or recorded as an outline
change the author approves. A fluent draft that fails the gate is not done.

## Stop and ask the author when

- a number the text needs has no source;
- text looks technically wrong, or a formula contradicts the implementation;
- an edit would change the contribution, threat model, claim strength, or an
  evaluation conclusion;
- an edit would replace, rename, or add an alias for a protected term, or no
  evidence decides whether two terms are equivalent;
- sources disagree and it is unclear which is true;
- a reviewer asks for a baseline or experiment the paper lacks: keep the claim
  out and list it as an open decision;
- several supported stories or structures remain and the choice changes the
  paper's emphasis.

## Verification and handoff

- **Checks.** `git diff --check`; a mechanical scan for the user's style
  rules; every label, citation, and figure reference you touched resolves.
  Leave fatal blockers (placeholders, unresolved references) to the
  `paper-hygiene` blocker scan and bibliography and citation checks to
  `paper-integrity`; run or recommend them before submission.
- **Build** the PDF when length or layout matters; report errors, undefined
  references, the word count, and where the section ends.
- **Where to work.** Multi-step writing goes on its own branch or worktree of
  the manuscript repository; commit the finished text there as a backup and
  never merge it yourself. Never stage unrelated changes. Keep review notes
  and round artifacts in ignored scratch space.
- **Report:** where the text is; the route and stages run; length against
  budget (Draft, Submission); the final logic chain; the reviewer's verdict
  and the gate result (independent or self-checked); outline changes;
  placeholders; open decisions; problems outside the task's scope, listed but
  not fixed.

## Project paper rules

A project extends this skill with its own `AGENTS.md` or project skill, holding
only project specifics: the outline location and format, the glossary,
paper-specific writing-guide rules, evidence sources, the placeholder macro, build
commands, branch conventions, venue and budget, story constraints for
reviewers, and lessons from earlier reviews of that paper. It tells the agent
to load this skill first and never copies its method.

## Related skills

- `paper-presentation-review`: read-only presentation diagnosis; the brief for
  the final verifier.
- `paper-hygiene`: mechanical cleanup of source and rendered PDF, fatal
  blockers, and line-level fitting (short last lines, float placement,
  whitespace). Cutting prose to a page or word budget is the Simplify stage
  here; hygiene sends rewrites beyond deleting a word or phrase back here.
- `paper-integrity`: citation checks and the submission gate.
- `paper-review`: reviewer-side work on someone else's paper (developing the
  user's review, or an independent review).
- `systems-evaluation-planner`: which experiments and figures an evaluation
  needs; `systems-paper-plotting`: rendering them.
