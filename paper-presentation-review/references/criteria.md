# Shared Paper Presentation Criteria

This is the single standard used by `paper-presentation-review` and `paper-presentation-revise`. It governs manuscript prose, headings, and captions within the requested scope. Apply it to English, Chinese, and LaTeX. It concerns how supplied research is explained, not whether the research is novel, correct, or experimentally sufficient.

## Interpretation and evidence boundaries

- Explicit current user instructions take precedence. Read applicable repository guides and accepted outlines. Store paper-specific vocabulary and decisions there, not in this generic standard. Do not import facts from examples below or from an older draft.
- Preserve mechanisms, assumptions, numerical results, units, baselines, citations, uncertainty, applicability conditions, and technical claim strength. Preserve source syntax such as equations, macros, labels, and cross-references. Do not add designs, experiments, literature, or unsupported reasons to satisfy a presentation rule.
- Required corrections have a located criterion violation or an explicit author constraint. Missing essential context is an unresolved question. An alternative with no demonstrated defect is a suggestion. The concrete prose restrictions in C09 and same-sentence rationale in C07 are this author's requirements, not universal conference rules.
- Coverage extends to every concept occurrence, sentence, and paragraph in the supplied scope. Ordinary words need scrutiny when used as technical labels or specialized quantities, not dictionary definitions for every word of an explanation. A concise description can supply a definition without introducing a named abstraction.
- Distinguish manuscript-visible context from private author notes and raw supporting evidence. Private notes can establish a faithful correction, but do not make a concept defined or a relationship explained to the paper's reader.
- Factual fidelity constrains every repair. If two requirements cannot be met using available evidence, report the conflict rather than silently weakening a requirement, changing a claim, or fabricating support. Keep reviewer notes and author decisions separate from publication-ready text.

## C01. Argument structure and section placement

**Check:** Identify the central question, intended conclusion, and supporting steps across the available paper, sections, and paragraphs. Check main line, hierarchy, dependency order, completeness, placement, and proportion. For each unit, identify what readers learn and why it belongs here.

**Fail when:** The text merely lists related facts, mixes a main claim with auxiliary detail at the same level, scatters one explanation, leaves a raised question unanswered, lacks a necessary prerequisite, or answers another section's question. A meaningful sentence can still be misplaced. Headings and connectives alone do not establish structure.

| Section | Intended contribution |
| --- | --- |
| Background | Establish concepts and operating assumptions needed by the later argument. |
| Motivation | Derive an opportunity or requirement from supported observations about a workload, limitation, or resource cost. |
| Design | Explain the proposed choices, how they work, and their supported reasons in relation to the problem. |
| Evaluation | State the assessed question and supported result, then connect the evidence and available explanation with their conditions. |
| Related work | Explain the supplied relationship and essential distinction without unsupported positioning claims. |

In Motivation, check the reasoning dependency **observation → opportunity**, not merely **desired benefit → proposed design**. "To reduce communication, we introduce a three-level cache" introduces a solution without establishing the observation. Proposed components, data layouts, and algorithm steps belong in Design. Removing their names or adding "could" does not turn them into an opportunity. Existing-system behavior, baseline mechanisms, and measurement conditions can remain when necessary to understand the observation. A high-level opportunity identifies what may be improved and why, without prescribing the proposed implementation.

### Motivation independence from Design

Motivation is a design-blind section. Review it first without using Design to
explain, justify, or repair its argument. Its supported output is a high-level
problem, insight, opportunity, or requirement derived from workload properties,
existing behavior, constraints, and observations. It may name established
domain objects and operations needed to state that problem. It should not
introduce or reverse-engineer the proposed component, data structure, encoding,
algorithm step, routing policy, or implementation-specific mechanism.

Use a counterfactual check: hide Design and ask whether Motivation still
establishes why the problem matters and what a solution must provide. If
removing a design-specific noun breaks the reasoning, rewrite the sentence as a
requirement or move the mechanism to Design. Do not use a later design detail,
evaluation result, or proposed architecture as evidence for the Motivation's
problem statement. Design is reviewed afterward to verify that its choices map
to the requirements already established by Motivation.

These are section responsibilities, not a mandatory order for every sentence or a mandate to invent sections. A result or opportunity may lead if understandable and clearly supported by what follows. Respect an explicitly combined motivation/design section while keeping its argumentative roles distinct. In an excerpt, identify content to relocate and its destination without pretending the other section was edited. Reordering, regrouping, or relocating can repair structure when connectives cannot.

### Design presentation

When reviewing Design, trace each component from a prior Motivation requirement
through a supported Design challenge, decision, responsibility, contract,
mechanism, and consequence. Check that the selected component granularity is
meaningful: a component should own a distinct problem, contract, decision,
downstream operation, or later evaluation claim.

Check the information order separately from factual correctness. The prose
should introduce a component's logical role before its physical layout or
identifier, and should distinguish aggregation, representation, and updates
when they carry different relations or invariants. Flag a component list with
no explanation of how the overall design uses each unit, a layout introduced
before its logical component, or a paragraph that combines architecture,
aggregation, layout, and updates without recoverable transitions. A concise
first component paragraph may defer those details, but it must state the
component's incoming challenge and role in the overall design.

### Evaluation breakdowns

When an Evaluation subsection breaks down the effects of design components, present the components in the order established by the Design section. Do not reorder them by measured magnitude, figure position, or ease of explanation. For each component, make one connected account of three points:

1. the metric or outcome it improves, including the direction of the change.
2. the cost it introduces, such as memory, retrievals, latency, write work, or lost reuse.
3. the net effect of that improvement and cost under the evaluated workload and configuration.

The net effect should explain the reported result at the level supported by the evidence. Distinguish an intended benefit from an observed effect, and do not infer a cost or a net effect that the available measurements do not establish. If the evidence cannot support one of the three points, mark the item as unresolved instead of filling the gap with a generic claim. This rule governs presentation and interpretation of an existing breakdown. It does not request new experiments.

### Design-centered performance breakdowns

When the breakdown explains the proposed system's measured performance, check
the dependency and narrative focus separately from the three per-component
effect points. The proposed system's headline result should appear before the
breakdown, followed by a short statement of why attribution is needed. The
breakdown should then follow Design order and explain the proposed design's
measured effects, costs, and workload/configuration-dependent net impact.
Baselines are normally comparison anchors and should receive at most one
sentence each for the outcome or causal distinction relevant to that result.
Flag baseline implementation tours, baseline-first data, and details that do
not explain the focal metric, cost, boundary, or direct comparison question.
Flag “access path” or similar implementation vocabulary when the evaluation
question is about performance rather than access-path behavior. An operation
from Design is not evaluation material merely because it exists; retain it
only when its measured effect or cost is part of the supported explanation.

### Evaluation argument-first writing

For every Evaluation paragraph, identify the one claim it establishes before
checking its numbers. For every sentence, identify whether it states the
question or purpose, reports evidence, interprets the evidence, compares
alternatives, qualifies scope, states a cost or net effect, or hands off to
the next claim. A sentence that only describes a figure, repeats a value, lists
a configuration, or names a baseline fails when it does not advance one of
these roles.

**Fail when:** a paragraph can be summarized only as “the figure shows X,”
when evidence is presented without the claim it supports, or when several
data sentences appear without an interpretation, evidence boundary, or scoped
implication. Move the claim before the evidence, attach each result to the
question it answers, or remove data that does not change the argument. This
check does not require every sentence to contain a number. It requires every
number to serve a supported argument. It does not require a stronger
interpretation than the experiment supports and does not request a new
experiment; an explicit evidence boundary is a valid result.

## C02. Purpose, repetition, and unnecessary text

**Check:** Give every paragraph a discernible reader question or takeaway and every sentence a useful contribution. Distinguish main claims, definitions, premises, evidence, explanations, implications, and limitations. These roles can recur. Two sentences may both provide evidence while contributing different information.

**Fail when:** Removing a unit loses no necessary definition, premise, evidence, conclusion, limitation, connection, or distinct summary function. Compare reasoning across nonadjacent passages too. Different wording does not make a repeated proposition new. Also check non-repetitive detours, empty previews, needless signposting, and unnecessarily long explanations.

Repeated nouns that preserve reference are useful. An abstract recap and a detailed evaluation can have different purposes. A concise sentence can be unnecessary, and a long causal explanation can be essential. Distinguish a provable duplication from a preferred phrasing. Apply C08 before deletion or merging.

## C03. Necessary and understandable concepts

**Check:** Inventory technical concepts, entities, abstractions, specialized ordinary words, abbreviations, metrics, and symbols. For each, identify its necessary distinction, reasoning contribution, or useful recurring reference, its first substantive use, and its definition. Check later uses against that meaning, including standard domain concepts.

**Fail when:** A new label adds no useful distinction, suggests an unsupported entity, or adds detail with no role here. If established vocabulary or a direct description conveys the same precise content, another name is unnecessary. A definition does not justify retaining an unnecessary concept.

For a needed concept, readers can identify what it denotes, its relevant role, and its relationship to established concepts at or before substantive use. Prefer an operational introduction that tells the reader what the object is doing here, where it comes from, or what it enables. For example, introduce an input as the records or items that an operation consumes, and introduce an inserted item by stating what later operation can use it. A concise inline explanation or unambiguous reference to an available earlier definition suffices. A name, acronym expansion, or near-synonym alone does not establish meaning. Avoid defensive or tautological introductions such as `we define X as X`; use a formal definition only when the concept has a precise boundary, notation, or invariant that the later argument needs. A definition that relies on another unexplained technical concept or an unstated relationship fails. Do not exempt a technical concept solely because a reviewer knows it, or mechanically demand a standalone glossary entry for a concept already explained in ordinary language.

Check semantic order as well as local intelligibility. A term can be explained in
the sentence where it appears and still be premature when it belongs to a later
representation or implementation layer. In a high-level section, introduce the
capability, purpose, or relation before its proposed encoding, identifier, data
structure, or component. For a central object, prefer a responsibility-first
opening that says what problem or operation it serves before describing what the
system stores or keeps. Do not use a locally repaired definition to justify a
Design detail in Motivation.

Check independently readable abstracts and captions for locally sufficient descriptions. Recheck when scope or operational meaning changes. For an excerpt, report "definition unavailable in the supplied context" rather than claiming a paper-wide omission. Never invent a definition. Remove an unnecessary label or defer its introduction, while retaining actual technical objects and distinctions necessary for accuracy.

### Terminology consistency and glossary

For a paper-wide or multi-section review, maintain a terminology ledger with a
canonical term, definition, allowed grammatical forms, first definition, later
uses, accidental variants, and nearby concepts that must remain distinct. Use
the paper's [glossary](glossary.md), then the repository writing guide and
accepted author decisions, as the authority for the canonical form. Any
glossary-banned term in the reviewed scope is a finding. A recurring concept such as `range query` should not drift to
`range-query` or `query` when those forms refer to the same concept. Conversely, do not collapse terms that denote different objects,
operations, or descriptive levels merely because their strings are similar.

**Fail when:** the manuscript uses multiple forms for one recurring concept
without a supported distinction, changes hyphenation or word order in a way
that suggests a new concept, introduces an abbreviation or synonym before its
mapping is clear, or uses a different term where the distinction changes the
claim. A grammatical inflection is allowed when it preserves the same mapping.
The acceptance condition is a consistent mapping across prose, headings,
captions, figure labels, equations, and tables, with every intentional
distinction recorded or defined.

For technical terms that connect a logical object to an implementation, also
record the term's abstraction layer and decision provenance. Distinguish a
logical object, its operation or mechanism, its representation, a backend
encoding, and an implementation example. Check each important
subject–relation–object sentence against those layers. A backend encoding must
not silently become the object it represents, and an example must not be
generalized into the category containing it. A current author instruction
supersedes an older guide or outline; mark the older term `superseded`, update
the paper-specific ledger, and regenerate dependent outline contracts.

An unlisted technical term that names a recurring concept, operation,
representation, or layer is an alignment finding, not a stylistic synonym.
Replace it with the established term or route it to `Needs context` with a
proposed glossary line. Ordinary one-use wording does not need a
new glossary entry.

For an operation or state-changing verb, also check the semantic contract:
actor, target or input, precondition, state transition, observable effect, and
scope. Fail when a word changes that contract even if it is used only once or
is grammatically fluent. For example, `resume` describes continuing a paused
operation; it does not describe an unavailable component being unable to serve
a request. Use the canonical availability or failure wording supported by the
paper.

## C04. Referents and accurate concept use

**Check:** For every group name, shorthand, pronoun, and demonstrative, identify the exact object or member set and where readers learned that mapping. Introducing several methods does not define a later group such as "these two approaches," "conventional schemes," or "other systems."

For each claim, check who acts, what is acted on or measured, whose property is described, and the level of description. Include qualifiers such as "across," "per," "among," and "for." Preserve distinctions between an entity and its representation, a whole and its component, a collection and its members, and a procedure and its output.

When the intended relation is indexing, tracking, mapping, or association,
prefer an active verb or an explicit relation. A phrase such as “recorded
sequences” may describe an event rather than the sequences tracked by an index.
Use wording that identifies the actual object and relation, and do not
introduce a new synonym merely to make the sentence sound formal.

**Fail when:** A referent is not uniquely recoverable, or the statement only works after readers silently replace the named object with a related one, invent a relationship, or change the counting unit or descriptive level. Having defined a term does not make every use accurate. For example, participants and observations, or models and predictions, are related but not interchangeable in counts or operations.

Use the paper's established term consistently, without stylistic synonym changes that imply another entity. Retain shorthand when its referent and meaning remain clear. Diagnose the particular statement instead of blacklisting a word. A proposed replacement needs support in the available text.

For a factual mapping between a named system and an implementation, storage
placement, data structure, or operation, check the supplied paper text and
authoritative source before accepting the mapping. Do not infer the mapping
from a system's name or from a familiar implementation pattern. If the source
does not establish it, classify the finding as `Needs context` and preserve the
uncertainty rather than inventing a corrected assignment.

## C05. Relationships, transitions, and causal explanation

**Check:** For every adjacent sentence pair and paragraph boundary, identify the actual relationship, such as claim/evidence, mechanism/result, comparison under shared conditions, or parallel explanations of one question. Also check dependencies on earlier material. Correct individual statements can still form an unconnected list.

When two paragraphs are sibling alternatives under one umbrella claim, check
that the second opening names the shared parent or endpoint and makes the
parallel or contrast relation visible. Do not accept two correct paragraphs
that read as unrelated items. Mark supporting mechanisms and caveats as side
branches when the outline does not give them ownership of the main progression.

| Failure | Observable defect |
| --- | --- |
| Missing | Readers need to supply a premise or relationship to understand why the next unit follows. |
| Redundant | A transition repeats an already clear relationship or both sides announce the same move. |
| Incorrect | The wording claims causation, contrast, verification, or another relation that the content does not support. |
| Indirect | Generic wording hides the specific preceding result, next question, or evidence being examined. |

A direct continuation can establish the relationship without a separate bridge sentence or connective. Distinguish missing wording from a missing premise. Adding "therefore" cannot supply evidence. A transition promising to verify X or explain X's effect on Y needs following analysis that actually does so. Studying one component does not by itself explain an overall result. For further analysis, identify which preceding result needs explanation and what evidence is examined next.

Retain the supported intermediate causal links. A possible chain is scenario property → configuration rule → available resources → system behavior → metric. The actual chain depends on the evidence, and this example is not a required template. Distinguish observations, established mechanisms, and hypotheses. Correlation, an intended benefit, or a workload tendency does not establish causation or a guarantee.

An overpromising transition can be aligned with what the following analysis already establishes. If the correction would change a substantive scientific claim, identify that as an author decision rather than silently weakening or strengthening the claim. Missing support remains a gap, not permission to invent a cause or demand a new experiment in a presentation review.

### Logical interface versus implementation

When a section introduces a service, index, or component together with its
implementations, separate the logical interface from the implementation
families. State the responsibility and the selected operations first. For each
selected operation, make the input, purpose, output, or effect recoverable
before naming the structure that realizes it. Use scope-calibrated wording such
as “we focus on two operations” when the text discusses representative
operations. Reserve “exposes two operations” or similar exhaustive wording for
cases where the source establishes that the interface has exactly those
operations. Then transition explicitly from the logical interface to the
implementation families and map named systems to structures only when the
mapping is source-backed.

**Fail when:** the prose presents a selected subset as a complete interface,
jumps from an operation name to a structure without its contract, lets an
implementation detail change the operation's input or result, or attributes a
structure to a named system without evidence.

### Cross-paragraph handoffs

When a paragraph depends on a result, object, metric, or pressure from the preceding paragraph, check the handoff in both directions. The preceding paragraph should name the result or condition that the next paragraph will use. The next paragraph should repeat the smallest concrete noun phrase needed to identify that dependency and state the relationship, such as dependence, consequence, or motivation. A generic anaphor such as "these gains," "this benefit," or "such systems" fails when its antecedent is ambiguous or requires rereading the preceding paragraph. Repeating a short metric or object phrase is preferable to making the reader recover it from context.

If the transition contains a causal chain, present only the supported steps needed to reach the next paragraph's question. For example, a reuse benefit can lead to retaining state, then to capacity pressure, data movement, and a need to locate that state. Do not move the final motivation into the next paragraph when the preceding paragraph already establishes why that next concept is needed. The next paragraph can then begin with the concept's responsibility or operation.

### Claim rendering and design tension

For a comparison, identify the single question the alternatives answer and
check that both sides use comparable outcome and path dimensions. A sentence
that describes one option's operation and the other option's access path can be
factually correct while hiding the tension the reader needs to see. When the
evidence supports it, render the tradeoff at the outcome level, such as one
option keeping matching queries fast while recovering slowly and another
recovering quickly while slowing matching queries. Preserve genuine asymmetry when
the alternatives do not have opposite effects.

For a core design tradeoff, treat the design choice or mechanism as the source
of its benefit and cost branches. State the reader-visible effect before using
an operation or access path to explain it. Tie the observed net effect to the
evaluated workload or configuration. A phrase such as "shifts cost" needs
evidence of a cost transfer; otherwise describe the added latency, retrieval,
or resource use directly.

When a design paragraph follows a problem paragraph, its opening should carry
the concrete pressure and purpose that motivate the design. When a figure
explains the first core claim about a design choice, its first source clause
should appear beside that claim unless it is a paper-level overview. Use the
canonical term for the design choice throughout this rendering pass.

### Paragraph-opening framework

For each paragraph, record its local responsibility, incoming endpoint,
supported relation, opening claim, provided claims, and outgoing endpoint. The
first sentence carries the paragraph's own responsibility. For every
noninitial paragraph, it also names the smallest concrete object, result,
metric, or pressure needed from the preceding paragraph and states the
relationship that makes the paragraph follow. The paragraph may carry a scope
condition when the claim would otherwise be misread.

The paragraph's central subject or operation should appear in the opening's
early subject or short first clause. A sentence does not pass merely because
it mentions the incoming endpoint if the paragraph's main concept is buried in
a long final clause. If the endpoint and responsibility cannot both fit
clearly, shorten the endpoint, split the opening, or lead with the paragraph's
responsibility and carry the endpoint in the next sentence.

Apply the first-sentence-only test before Design: reading only the first
sentence of each paragraph should let a reader recover the subsection's
setting or question, observation or pressure, opportunity or requirement, and
progression. For Design and Evaluation, the openings should similarly recover
the local order of responsibilities. A vague anaphor, detached handoff, or
opening that exposes details without its paragraph's hierarchy is a structural
finding. See the [paragraph opening workflow](../../paper-presentation/references/paragraph-opening-workflow.md)
for the matrix and revision procedure.

When the story is sound but the presentation graph is not, classify merging,
splitting, reordering, relocating, or deleting redundant units as a required
presentation repair. Do not reduce a grouping or sentence-relation defect to
an optional wording preference.

### Subsection autonomy

Treat each subsection as a locally understandable argument unit. Its opening
should state the local question or purpose, name the object under discussion,
and provide the minimum definitions and conditions needed to proceed. A short
logical migration sentence may connect it to the previous subsection, but the
reader should not need to reread that subsection to recover the subject,
purpose, or relationship. Prefer an explicit bridge such as "Because records can reside across
storage tiers, the next subsection explains how the system locates them" over
a backward pointer such as "As discussed above, this approach...".

**Fail when:** a subsection opens with an ambiguous backward reference, a term
whose canonical form is not recoverable, or a premise that appears only in an
earlier subsection and is needed to understand the current one. Do not require
full repetition of definitions that are already stable and locally identifiable.
The acceptance condition is a forward-oriented handoff plus enough local
context for the subsection's argument to be followed without backtracking.

### Subsection flow and abstraction

For each subsection, identify its local question, opening purpose, incoming
endpoint, owned object or operation, abstraction level, and outgoing endpoint.
The opening should state what the subsection handles and why it is the next
step. It may name the concrete endpoint from the preceding subsection, but it
should not repeat the preceding explanation. Check that the subsection moves
through supported levels such as responsibility, operation, structure, and
implementation, and that a lower-level detail answers the question established
at the current level.

**Fail when:** a subsection starts by restating the prior handoff, introduces a
representation alias as a new concept without a later distinction or use,
describes alternative structures before stating the operation or requirement
they serve, or changes abstraction level without a recoverable relation. A
sentence whose only function is to announce the next subsection is redundant
when the next opening already carries that purpose. For every clause, identify
the current or downstream reader-facing job. Remove or flag clauses that only
anticipate a hypothetical implementation question.

## C06. Interpretable quantitative claims

**Check:** For every value, ratio, percentage, comparison, and range, locate the fields needed to interpret it. For empirical claims these include the subject/system, metric, units where applicable, comparator or denominator, and relevant conditions. These can come from the same sentence or explicit adjacent context. State the dimension a range spans, such as datasets, systems, or configurations.

Distinguish empirical results, design parameters, structural counts, and identifiers. A dimensionless ratio has no physical unit. A count of three stages needs identifiable stages, not an experimental baseline. "Algorithm 2" is a reference identifier, not a measured quantity. Mark a field inapplicable only when its absence does not change interpretation.

**Fail when:** Readers have to guess the operation, setup, counting unit, denominator, ratio direction, or scope. For "accesses account for 90% of total time," establish whose access time, the total time of which operation, and under what conditions. A range across datasets is not automatically a bound for every system. "Better" requires a recoverable metric and comparison target.

Preserve distinctions among ratios, relative percentage changes, and percentage-point differences. Use figures, captions, or supplied data only when their mapping to the claim is established. Do not infer exact values or causes from a vague plot, or turn a scope question into an evaluation redesign.

### Evidence introductions and metric-result paragraph openings

When body prose reports an observation supported by a figure or table, lead the observation with an explicit source clause, such as "Figure X shows ..." or "Table Y reports ...". A parenthetical-only reference such as "(Figure X)" or "(Table Y)" may supplement an explicit source clause, but it cannot be the sole introduction of the evidence for the sentence.

When an Evaluation paragraph introduces a metric or begins a metric-specific result, open with one short sentence that defines what the metric measures or states why it is reported. Put numeric values, rankings, and comparisons after that orientation sentence. For example, "We report recovery time from opening the database until the index is available." If a complete definition and purpose are already clear in the immediately preceding context, the paragraph may continue from that context without repeating it. A bare number, ranking, or improvement claim cannot be the paragraph's first explanation of a newly introduced metric.

## C07. Supported reason in the action sentence

**Check:** A sentence saying what a system, component, algorithm, or author does, or how it does it, includes the supported reason in that same sentence. This author requirement applies to action and method descriptions, including experimental choices. A reason only in a neighboring sentence does not satisfy it.

**Fail when:** The action lacks a reason, the reason merely repeats the action, or a generic benefit substitutes for its rationale. "We group records to group them" and "to improve performance" without a concrete connection do not explain the choice. When supported, "The system groups records requested together to reduce the number of separate retrievals" connects an action to an identified cost. This example supplies no facts about the manuscript being reviewed.

A purpose, constraint, or causal clause can satisfy the check without the word "because." Do not demand an intention for every factual observation or treat every verb as a design action. For observed behavior, causal support is checked under C05. When a sentence does describe an action or method, do not relabel it as an observation merely to evade this requirement.

Check C01 before improving a design sentence in Motivation. A complete what/how/why explanation does not establish correct placement. Distinguish intended purpose from demonstrated effect. If available evidence supplies no reason, leave an explicit unresolved item rather than inventing intent. Split an overloaded sentence into understandable action-and-reason units, without generic repeated justifications.

## C08. Information retained during compression

**Check:** Before shortening, deleting, merging, or relocating, identify the essential definitions, quantitative comparisons, conditions, causal links, and analysis purpose. Locate where each survives in the revised scope or the explicitly reported relocation. Compare the actual final text with its source and supporting context.

**Fail when:** The edit removes information needed to interpret or verify the argument, changes claim strength or scope, or substitutes a related entity. Expand shortened noun phrases back to their established referents and recheck operation, property, relation, and level of description. Do not replace a core numerical comparison with "lower" or "better" solely because its magnitude appears in a figure.

Prefer removing repeated reasoning over essential evidence. Necessary relocation is not permission to silently lose content, especially when the destination is outside the edit scope. Unsupported information can be flagged, but deleting a substantive unresolved claim merely to obtain a clean review is not a faithful repair.

## C09. Prose constraints and clarity

**Required author style:** No standalone `must`, in any capitalization, in authored manuscript prose. Preserve genuine requirement strength with an accurate equivalent such as "requires" or "is necessary for." No semicolons (`;` or `；`) or prose dash punctuation, including em dashes, en dashes, and LaTeX `--` or `---`. Use grammatical clauses or sentences with the same relationship. Use "to" for prose ranges when appropriate.

Apply these restrictions to prose headings and captions too. Preserve compound-word hyphens, mathematical minus signs, and required code or LaTeX syntax, identifiers, URLs, bibliography metadata, and verbatim quotations. Flag conflicts in immutable quotations separately. Inspect rendered meaning when source syntax is ambiguous. Do not perform a blind source-wide substitution. Apply broader local restrictions to review comments when the author explicitly requires them.

**Clarity:** Prefer concrete subjects, precise verbs, and manageable sentences.
An essential subordinate clause is allowed, but split a sentence when it
introduces several new concepts, chains multiple independent logical relations,
or places a condition far from the claim it qualifies. Flag ambiguous grammar,
overloaded noun chains, promotional wording that misstates evidence, and
headings that overpromise. Familiar-to-new order, sentence-end emphasis, and
splitting or combining sentences are writing options, not universal
pass/fail conditions. "Novel," "powerful," or "significantly" is problematic
when unsupported, not a word blacklist independent of meaning.

## Using the criteria

Reviewers locate defects and state meaning-based acceptance conditions. Writers select repairs consistent with the same criteria and evidence. Neither role can treat examples as facts, an internal checklist assertion as proof, or a previous review as validation of a changed draft. After revision, apply all relevant criteria afresh to the whole requested scope. Keep routine per-sentence reasoning internal, but make findings and any requested coverage record traceable to the final text.
