# Review-to-Outline Continuation Routing

Use this protocol when the author responds to a review, a story discussion, or
an earlier alignment turn. The response is a workflow event as well as prose:
it updates the shared state and determines the next stage. Do not make the
author repeat the next pipeline command when the response already supplies the
needed decision.

For story and outline transitions, also use the [argument-node outline
workflow](argument-node-outline-workflow.md). The coordinator must return both
the semantic object and logic graph, the full execution outline, and its
sentence/logic-level human sync view from the same fixed outline revision.
Apply the [structured outline refinement workflow](outline-refinement-workflow.md)
before returning that projection to the author.

## Interpret the response

First classify each author statement as one or more of:

- finding decision: accepted, rejected, deferred, or unresolved;
- story or claim decision: the problem, opportunity, insight, requirement, or
  claim that should be retained;
- structure decision: section/subsection grouping, order, paragraph role,
  handoff, or sentence relation;
- prose constraint: terminology, tone, compactness, or a local wording
  preference; and
- edit authorization: whether the manuscript may be changed now.

Also classify the input mode. If the author supplies a poor subsection as
reference material, or asks to rewrite or reorganize without an aligned
target, set `mode=rebuild-from-material`. Preserve the raw source version as
an immutable reference. Do not infer that its paragraph order, wording, or
transitions are accepted decisions.

Record these decisions against the fixed outline and its change log. Preserve
the manuscript version and outline revision that the response refers to. Do
not treat agreement with a finding as agreement with an unstated paragraph
order or subsection boundary.

## Route the next stage

For the ordinary author-driven workflow, discussion is the first stage. If the
author is still deciding the story or has not aligned a structured outline,
continue with story alignment and outline synthesis rather than dispatching a
prose reviewer or writer. Section-specific references, including the Design
pattern catalog, are used while forming that story and outline; they do not
create a separate section workflow.

Use the first applicable route:

0. **Source-only rewrite.** For `rebuild-from-material`, run the
   [reference-material rebuild workflow](reference-material-rebuild-workflow.md)
   first. Return the material ledger, authority classification, source-unit
   disposition map, independently recovered story, and open story decisions.
   In a manual run, stop at `Awaiting story alignment`; do not produce a
   lightly edited subsection or synthesize its outline from the old paragraph
   order.

1. **Direction-only section planning.** If the author gives a high-level
   section direction but no complete reader-facing outline, load the [section
   content planning workflow](section-content-planning-workflow.md). Return the
   section purpose, supported content dimensions or categories, candidate
   evidence and citations, paragraph responsibilities, argument nodes, and
   handoffs, together with the execution outline and sentence/logic-level human
   sync view.
   Set `workflow_stage=section_planning` and `Awaiting outline alignment`.
   Do not dispatch a prose reviewer or writer yet.
2. **Review response without a complete structure.** If the author accepts or
   discusses the findings but has not supplied a complete reader-facing
   structure, run outline synthesis automatically. Produce the structured
   outline delta with section/subsection hierarchy, paragraph order and roles,
   semantic object types and relations, argument-node summaries and relations,
   incoming and outgoing handoffs,
   sentence `from`/`needs`/`link` fields, and evidence and terminology
   bindings. Render the sentence/logic-level human sync view and set the state
   to `Awaiting outline alignment`. Do not dispatch a prose writer yet.
   If the active scope is Evaluation, run the [Evaluation Presentation and
   Rebuild Workflow](evaluation-presentation-workflow.md) and [Evaluation
   Patterns from Systems Papers](evaluation-reference-patterns.md) during outline
   synthesis. The outline is incomplete until it records the Evaluation
   question or archetype, narrative order, claim–evidence bindings, and
   source-unit dispositions.
3. **Author-supplied complete structure.** If the response contains a complete
   outline subtree or explicit paragraph contracts, validate it against the
   fixed outline, manuscript, evidence, and protected claims. If it passes,
   record it as aligned and continue to interface compilation. If it is
   incomplete or contradictory, return the smallest outline delta and remain
   at `Awaiting outline alignment`.
4. **Story-only agreement.** If the author has aligned the story but not the
   reader-facing grouping and order, preserve the story decision and still run
   outline synthesis. A correct story graph does not select a presentation
   structure by itself.
5. **Explicit direct revision.** Skip outline synthesis only when the author
   supplies an aligned target structure or concrete acceptance conditions and
   explicitly authorizes editing. Otherwise route through outline synthesis.
6. **Unresolved substantive choice.** If the response leaves multiple
   supported structures or motivation insights equally plausible, record the
   alternatives and stop at `Awaiting alignment` or `Awaiting outline
   alignment`, whichever decision is still open.

The normal manual continuation for an already structured manuscript is:

```text
story discussion → story alignment → outline synthesis
→ present structured outline and sentence/logic-level human sync view → author outline alignment
→ independent review → presentation organization → interface freeze
→ Round 1 rendering → Round 2 presentation repair
→ Round 3 English polish → integrate → verify
```

If the user explicitly requested a review before discussing the story, use the
review-first route only for diagnosis, then return to story and outline
alignment before revision:

```text
review → author response → story alignment → outline synthesis
→ present structured outline and sentence/logic-level human sync view → author outline alignment
→ presentation organization → interface freeze → revision → verify
```

For a poor source subsection, the normal manual continuation is:

```text
material audit → independent story recovery → author story alignment
→ outline synthesis → present structured outline and sentence/logic-level human sync view
→ author outline alignment → independent review → presentation organization
→ interface freeze → Round 1 rendering → Round 2 presentation repair → Round 3 English polish
→ integrate → verify
```

The next assistant turn should state the routed stage and deliver its concrete
artifact. For example, after “这些 review 意见都对，按这个方向改”, return the
updated review decisions plus the proposed structured outline and wait for
outline alignment; do not silently rewrite the manuscript. Once the author
aligns that outline and authorizes writing, start the three prose rounds without
requiring another user command. Pause only if a round exposes a substantive
decision, or if the author explicitly requests `draft-only`.

## Do not confuse similar events

- “这个问题确实存在” accepts a finding; it does not authorize a rewrite.
- “故事按这个方向” aligns the story; it does not align paragraph order.
- “按这个大纲改” can authorize revision only after the outline is complete
  and validated.
- “参考这段重写” does not authorize preserving its order or wording. It
  authorizes material extraction; story and outline alignment still precede
  prose generation.
- “先润色一下” does not reopen story or structure; once the outline is aligned,
  route through the three prose rounds unless the author explicitly requests
  `draft-only`.

## Handoff record

Every continuation should return:

- the input manuscript version and fixed outline revision;
- decisions extracted from the author response;
- the routed `workflow_stage` and `refinement_stage`;
- the outline artifact or delta produced by the route;
- the semantic object and logic graph, argument-node execution view, and
  sentence/logic-level human sync view produced from
  that artifact;
- the next author decision, if any; and
- the condition that permits interface compilation or revision.

