# Outline Contract

Read this when producing, completing, aligning, or drafting from an outline,
and when checking prose against one. The outline fixes the argument before any
wording exists; prose renders the agreed outline and is never the place to
discover a missing claim, purpose, or transition. For Related Work, the outline
is a positioning map instead; see [related-work.md](related-work.md).

## 1. Location, status, phase

- **Location.** Use the outline location that the project declares in its
  `AGENTS.md` or project skill, and follow its file map exactly. If the project
  declares none, keep the outline in the conversation or in a file the user
  chooses. A missing location never blocks work.
- **Status** on every outline: `proposal` (under discussion; no prose from it
  yet), `agreed` (preserve its claims, order, and interfaces unless the author
  approves a change), or `stale` (the manuscript changed after the outline;
  report the drift before relying on it).
- **Phase line** near the top: `Early`, `Draft`, or `Submission` (defined in
  the [skill](../SKILL.md#phase-controls-the-review)).
- The outline is the only structure record. Do not keep a second story file,
  graph, or "presentation structure" beside it; derived views are regenerated
  from it.

## 2. One schema, three levels

**L0, the section or subsection contract (always):**

```text
S2.3 local question: <the question this subsection answers>
     claim: <the one answer it establishes>
     level: <abstraction level; later-layer details it must not use>
     from: <incoming claim or pressure>   gives: <outgoing claim or handoff>
     evidence: <what may support it>
```

**L1, one line per paragraph (always):**

```text
P3 [role] claim: <one sentence: what the reader retains>
   answers: <the reviewer question>
   from: <carried endpoint> (<relation>)   gives: <endpoint the next paragraph uses>
   needs: <numbers, figures, citations, with sources>
```

`from` and `gives` are concrete endpoints (a measured pressure, a requirement, a
result), never "transition". Paragraph roles: context, observation, pressure,
requirement, failed approach, question, insight, design decision, mechanism,
contract, tradeoff, positioning, evidence, results, limitation, contributions.

**L2, sentence propositions (when delegating prose to a separate writer, when
the author asks, or when a paragraph's internal logic is disputed):**

```text
P3.2 [evidence] <one concrete subject–predicate–object or condition–consequence
     statement>   rel: supports P3.1   evidence: Fig. 4   scope: <workloads>
     terms: <canonical terms>   introduces: <concepts first used here>
     merge: none | P3.3   forbidden: <objects that belong elsewhere>
```

Each line carries one meaning: split independent claims, effects, and costs
into separate lines. A topic is not a proposition: "report the throughput result" fails; "The
system achieves the highest request throughput on all three workloads (Fig. 4)"
passes. An L2 line that adds a claim absent from L1 is either promoted to L1 or
removed. Sentence roles: purpose, setting, claim, evidence, explanation,
contrast, definition, condition, cost, net effect, evidence boundary,
implication, limitation.

**Tests before any prose:**

- **Claim test:** the L1 claims, read in order, are the subsection's argument.
- **Opening test:** the planned first sentences pass the first-sentence-only
  test in [flow-and-openings.md §4](flow-and-openings.md#4-the-opening-contract-and-handoff-placement).
- **Proposition test (with L2):** the propositions, read in order, recover
  every paragraph claim and its handoff.

If a test fails, repair the outline (merge, split, reorder, relocate, or drop
units). Do not ask prose to repair it with connectives.

## 3. Figures and tables

One block per float, after the paragraph that first cites it. Describe what it
shows; do not draw it.

```text
FIG:<label> [role] answers: <the reviewer question>
- takeaway: <the one conclusion a reader draws>
- shows: <designs, workloads, metrics compared; panels>
- explains: <explanation figures only: the result it decomposes, and whether
  the parts add or multiply to it>
- why a figure: <why a sentence or table cannot carry it>
- cited by: <sentence or paragraph IDs>
- needs: <data source, or "missing experiment">
```

Use `TAB:` with `why a table:` for tables. Roles: result, explanation,
motivation, overview, mechanism, example, tradeoff, setup, positioning.

Classify each candidate float as `required` (prose and existing evidence cannot
make a needed relationship clear), `beneficial`, `unnecessary` (one sentence or
an existing float already does it), or `blocked` (the relationship it would
show is unsupported; never use a diagram to imply it). Place a float where the
reader first needs it, introduce it with a source clause ("Figure X shows ..."),
and let the following prose use it rather than repeat the caption. In a
conceptual figure, every arrow, grouping, color, and position encodes a
supported relation, and labels use the text's terms. For which experiments and
figures an evaluation needs, use `systems-evaluation-planner`; to render
quantitative plots, use `systems-paper-plotting`.

## 4. The rest of the outline

- a header with the phase and the budget (words per part; where the section
  should end on the page);
- for a section with subsections, a section-level outline first (L0 per
  subsection and one chain line per subsection);
- the logic chain, one line per paragraph;
- model papers used, if any, and which role sequence the outline follows;
- open issues the text will not settle;
- from round 2 on, "Changes from round N", each mapped to its finding.

## 5. Building or completing an outline

The author may enter at any level: a direction, a story, a paragraph chain, or
a full outline. Fill the missing levels from supported material; never invent
a fact, mechanism, term, causal edge, evidence item, or scope.

1. Read the requested scope, adjacent sections, the writing guide, the
   glossary, and the evidence.
2. Recover the section's job from [sections.md](sections.md). For Motivation,
   run the sealed pass there before reading Design. For Evaluation, use
   [evaluation.md](evaluation.md).
3. Draft L0, then the L1 order and interfaces. When grouping or order is not
   determined by the evidence, keep two or three alternatives with their
   tradeoffs; never choose the old draft's order by default.
4. Add L2 where §2 requires it.
5. Run the three tests, then an independent outline review (see the
   [review loop](review-loop.md)).

## 6. Aligning with the author

Show the outline itself, with its open decisions; it is the author's view and
the writer's input at once. Agreement on the story is not agreement on
grouping, order, or handoffs, and accepting a finding is not authorization to
rewrite (see [rebuild-and-replies.md §2](rebuild-and-replies.md#2-reading-author-replies)).
Keep the status `proposal` until the author agrees, then mark it `agreed` and
write the decisions into the outline. Propose a change as an **outline delta**:
affected IDs, current and proposed order or rows, the dependency or reader
question it repairs, and what must survive. The author may edit any level.

## 7. Drafting from an agreed outline

Write paragraphs in outline order, one at a time. For each paragraph the
writer uses the L0 and L1 context, the paragraph's rows, the endpoint the
previous (already checked) paragraph actually produced, the next paragraph's
`from`, and the glossary. It never infers the next paragraph's claim from
neighboring prose. With L2 present, write one sentence per line unless `merge`
allows combining, and return a sentence-to-line trace. Before writing the next
paragraph, check the current one: opening carries its endpoint and job, claims
and evidence and scope preserved, endpoint as promised, no new term or object.
A paragraph that cannot be written without inventing content is `Needs
context` or an outline delta, not an improvisation.

## 8. Reverse-outline round trip

After writing or revising, rebuild the outline from the prose without looking
at the plan: hierarchy, paragraph claims, first-sentence summary, relations,
concepts at first use, evidence bindings. Compare it with the agreed outline.
Any missing, invented, reordered, or merged unit, lost qualifier, or changed
handoff is either a prose defect to fix or an outline change to record. A
fluent draft whose reverse outline differs is not done.
