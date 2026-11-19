# Presentation Criteria

The checklist a presentation reviewer or verifier applies. Each criterion
states what to check, when it fails, and what the acceptance condition must
name. The writing rules behind each criterion live in `paper-writer`'s
references, linked per criterion; this file does not restate them. Examples
are illustrations, never facts about the manuscript.

## Boundaries

- Explicit current author instructions, the project's paper rules, and the
  glossary take precedence. Paper-specific vocabulary and decisions live there,
  not here. Current author decisions supersede stale examples or outlines.
- Preserve mechanisms, assumptions, numbers, units, baselines, citations,
  uncertainty, conditions, and claim strength. A presentation finding never
  asks for a new design, experiment, citation, or unsupported reason.
- A **Violation** is a located breach of a criterion or explicit author rule.
  **Needs context** is missing essential meaning or evidence. A
  **Suggestion** is a defensible optional alternative with no demonstrated
  defect. Never turn preference into a Violation or manufacture a quota.
- Coverage is every sentence, concept occurrence, heading, and caption in
  scope. Ordinary words need scrutiny only when they act as technical labels.
- Private author notes can justify a correction but do not make a concept
  defined or a relation explained to the reader. A pass comes from the final
  text and the available context, never from the reviewer's familiarity with
  the topic or a writer's explanation.
- For an excerpt, conclusions are limited to the excerpt ("definition not in
  the supplied context", not "undefined in the paper").

## C01. Argument structure and placement

**Check:** the central question, conclusion, and supporting steps; main line,
hierarchy, dependency order, completeness, placement, and proportion. For each
unit: what the reader learns and why it belongs here. Reconstruct the reverse
outline and the paragraph claim list first
([flow-and-openings.md §1](../../paper-writer/references/flow-and-openings.md#1-map-the-chain)).

**Fail when:** the text lists related facts; a main claim and an auxiliary
detail sit at one level; one explanation is scattered; a raised question is
unanswered; a prerequisite is missing; a unit answers another section's
question; a logic jump exists
([§2](../../paper-writer/references/flow-and-openings.md#2-detect-logic-jumps)).
Headings and connectives alone do not establish structure.

**Accept:** the target order or grouping, the dependency it repairs, source
and destination IDs, and the protected content that must survive.

## C02. Section contracts

**Check:** each section answers its own question at its own level
([sections.md §1](../../paper-writer/references/sections.md#1-section-contracts)).
When Motivation is in scope, run the sealed design-blind pass before reading
Design and record its contract and leakage map; then map each Design choice to
a requirement ([sections.md §2](../../paper-writer/references/sections.md#2-motivation-recover-a-design-independent-argument)).
For Design, check the pattern, granularity, and logical-before-physical order
([§3](../../paper-writer/references/sections.md#3-design-choose-the-readers-path)).
For Evaluation, check argument-first paragraphs, archetype, the four orders,
and breakdown rules ([evaluation.md](../../paper-writer/references/evaluation.md)).

**Fail when:** Motivation needs a proposed mechanism to state its problem; a
naive-solution chain sits in Motivation; Motivation is circular with Design; a
Design choice maps to no requirement; a component has no prior challenge; an
Evaluation paragraph is a data inventory; a breakdown leads with a baseline,
omits the headline result or the reason for attribution, or leaves Design
order.

**Accept:** for Motivation, the design-blind observation-to-opportunity chain
and which units move to Design; for Design, the mapping to a requirement; for
Evaluation, the question or archetype, target narrative order, and the missing
metric, cost, or net effect.

## C03. Purpose, repetition, and unnecessary text

**Check:** every paragraph has a reader question or takeaway and every
sentence a contribution (claim, definition, premise, evidence, explanation,
implication, limitation). Compare reasoning across nonadjacent passages too.

**Fail when:** removing a unit loses nothing necessary; a proposition repeats
in different words; a detour, empty preview, or signpost adds nothing; a
sentence describes without serving the argument. A repeated noun that keeps a
referent clear is not repetition.

**Accept:** which unit to cut or merge and where its necessary content
survives (C09).

## C04. Concepts and first use

**Check:** inventory technical concepts, abbreviations, metrics, and symbols;
for each, its necessary distinction, first substantive use, definition, and
abstraction layer
([terminology.md §5](../../paper-writer/references/terminology.md#5-words-that-carry-claims)).

**Fail when:** a label adds no distinction; a needed concept is used before
the reader can tell what it is, does, and relates to; an introduction is
tautological ("we define X as X"); a definition relies on another unexplained
concept; a concept is explained locally but belongs to a later layer.

**Accept:** a short operational introduction folded into the sentence that
first uses the concept (role, input or source, purpose), or removal or
deferral of the label.

## C05. Referents and accurate concept use

**Check:** every group name, shorthand, pronoun, and demonstrative identifies
one object or member set the reader has met; every claim keeps its actor,
object, counting unit, and level of description
([terminology.md §4](../../paper-writer/references/terminology.md#4-lock-rules)).
Factual mappings between a named system and a structure or placement are
checked against the source.

**Fail when:** a referent is ambiguous ("these approaches"); a statement only
works after the reader swaps the named object for a related one (an entity for
its representation, participants for observations); a system-to-structure
mapping has no source (classify `Needs context`).

**Accept:** the exact referent or relation, supported by the available text.

## C06. Relations, transitions, and openings

**Check:** every adjacent sentence pair and paragraph boundary has a named,
supported relation; every opening follows the opening contract; the
first-sentence-only reading recovers the subsection's progression; siblings
read as alternatives; comparisons share one question and outcome axes;
tradeoffs trace benefit and cost to one design choice
([flow-and-openings.md §3-§5, §8](../../paper-writer/references/flow-and-openings.md#3-name-every-relation)).

**Fail when:** a relation is missing, redundant, incorrect, or indirect; a
connective stands in for a premise; an opening buries the paragraph's subject
or relies on a detached closing handoff; an anaphor such as "these gains" is
unrecoverable; a transition overpromises; a causal claim rests on correlation.

**Accept:** the shared endpoint and supported relation, carried by the next
paragraph's opening. A required regrouping (merge, split, reorder, relocate,
delete) is a Violation with a target organization, not a style suggestion
([§7](../../paper-writer/references/flow-and-openings.md#7-organization-moves)).

## C07. Subsection autonomy and abstraction flow

**Check:** each subsection's local question, minimum context, owned object,
abstraction level, and forward handoff; whether the order moves through
supported levels; whether a logical interface precedes its implementations
([flow-and-openings.md §6](../../paper-writer/references/flow-and-openings.md#6-subsection-autonomy-and-flow)).

**Fail when:** a subsection opens with an ambiguous backward reference or a
premise found only earlier; it restates the prior handoff; alternatives appear
before the operation they serve; a representation alias becomes a concept
with no later use; a selected subset is presented as a complete interface.

**Accept:** a local question, the minimum context, and an explicit forward
handoff.

## C08. Quantities and evidence

**Check:** every value, ratio, range, and comparison has its subject, metric,
unit, comparator, and conditions; every figure or table observation is
introduced by a source clause; a new metric is oriented before its numbers;
each float has one reader question and placement
([evaluation.md §7-§8](../../paper-writer/references/evaluation.md#8-quantitative-reporting),
[outline-contract.md §3](../../paper-writer/references/outline-contract.md#3-figures-and-tables)).

**Fail when:** the reader must guess the operation, denominator, ratio
direction, or scope ("accesses take 90% of the time": whose accesses, which
total, under what conditions); ratios, relative changes, and percentage points
are mixed; "(Figure 3)" is the only evidence introduction; a bare number opens
a new metric; a needed relationship has no figure when prose cannot carry it
(`required`); a figure has no claim.

**Accept:** the missing fields, the source clause, or the figure brief.

## C09. Retention under compression

**Check:** before accepting a cut, merge, or move, locate where each essential
definition, comparison, condition, causal link, and purpose survives.

**Fail when:** an edit removes information needed to interpret the argument,
changes claim strength or scope, substitutes a related entity, or replaces a
core comparison with "better"; a relocation silently drops content outside the
edit scope; an unsupported claim was deleted only to pass review.

**Accept:** the survival location for each essential item.

## C10. Terminology lock

**Check:** the glossary, ledger, lock rules, verb contracts, modifier claims,
and banned-term scan in
[terminology.md](../../paper-writer/references/terminology.md).

**Fail when:** one concept has several forms without a distinction; a form
change suggests a new concept; distinct concepts are collapsed; a coined term
names a recurring concept; a verb changes the actor, precondition, or effect;
a modifier lacks support; a banned term appears.

**Accept:** one canonical mapping across prose, headings, captions, labels,
equations, and tables, with intentional distinctions defined, or a proposed
glossary line marked `Needs context`.
