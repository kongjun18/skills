# Terminology and Subsection Workflow

Use this workflow to keep technical terms stable and make each subsection
locally understandable while preserving a short logical handoff from the
previous subsection.

## Build a terminology ledger

Seed the ledger from the paper's [glossary](glossary.md) when one exists; its
entries are `active` with source `glossary`, and its banned terms are
prohibited variants. Then, before reviewing or revising a broad scope,
inventory every recurring technical
concept, entity, metric, operation, configuration, workload, abbreviation,
technical noun phrase, adjective, adverb, and relation word.
For each concept, record:

- a stable concept ID;
- the canonical manuscript term;
- its definition and role;
- allowed grammatical forms, capitalization, and hyphenation;
- the first substantive definition and all important later uses;
- variants that are accidental drift or prohibited when they refer to the same
  concept;
- nearby terms that must remain distinct.

For each technical modifier, also record the property it asserts, the
comparison axis, the scope, and the evidence or design relation that supports
it. Words such as `efficient`, `fast`, `compact`, `direct`, `lightweight`, and
`scalable` are claims when they affect the reader's interpretation. Remove an
unsupported modifier or route it to `Needs context`; do not keep it merely
because it makes a sentence sound stronger.

Choose the canonical form from the glossary, the repository writing guide, an
accepted author decision, or the first precise definition when no decision exists. Do not
silently merge terms that denote different objects, operations, or levels of
description. A spelling or hyphenation difference is a drift only when the
paper uses both forms for the same concept.

## Track semantic layer and decision provenance

For technical terms that connect system behavior to an implementation, add the
term's semantic layer and decision provenance to the ledger. At minimum record:

- `layer`: logical object, operation, mechanism, representation, backend
  encoding, implementation, metric, or example;
- `source`: current author instruction, glossary, paper-specific writing guide, aligned
  outline, cited source, or agent proposal;
- `status`: `active`, `superseded`, or `disputed`;
- `allowed_context` and `forbidden_generalization`; and
- the parent/child or `represented_by` relation when the term is a lower-level
  representation of another concept.

For every operation, state-changing verb, or relation word, also record its
semantic contract:
the actor, target or input, precondition, state transition, observable effect,
and scope. A word is not an acceptable variant merely because it is grammatical
or sounds idiomatic. It must preserve that contract. For example, `resume`
normally means that a previously paused operation continues; it must not be
used to mean that an unavailable index cannot serve a request. Use the
canonical state or availability wording instead, or route the proposed term to
`Needs context`.

Check every important subject–relation–object sentence against these layers. A
backend encoding must not silently become the logical object it represents, and
an implementation example must not define the category that contains it. The
exact vocabulary is paper-specific; the layer check is generic.

If a current author instruction conflicts with an older guide or outline, mark
the older decision `superseded`, propose the glossary edit (or the
paper-specific guide edit when no glossary exists) during the alignment stage, and regenerate dependent outline contracts before writing.
Do not preserve a stale term merely because it is already in the ledger.

Examples of drift include changing one recurring term's word order, inserting
or removing a hyphen, switching between a noun and an unexplained synonym, or
using a shortened form before its definition. A grammatical plural or a
necessary inflection is allowed when it preserves the same concept.

## Check subsection autonomy

For every subsection, record its local question, opening orientation, required
definitions, main takeaway, evidence, and handoff to the next subsection. A
subsection should be understandable from its own text plus the minimum shared
terminology established by the paper. Readers should not need to reread the
previous subsection to recover the subject, purpose, or relationship being
discussed.

Allow one short migration sentence from the previous subsection, but make it
forward-oriented and explicit. It should name the previous result or condition,
the current object or question, and the relationship between them. For example,
"Because records can reside across storage tiers, the next subsection explains
how the system locates them." The following prose should still state enough
local context to proceed.

Flag a subsection when its opening depends on vague backward references such as
"as discussed above," "this approach," or "these results," when it introduces
a term in a different form, or when the reader must search an earlier
subsection for the definition needed to interpret the current one. Do not
repeat a full definition when a short canonical noun phrase supplies the
necessary context.

## Repair and verify

Revise terminology before polishing sentence rhythm. Replace accidental
variants and semantically incorrect substitutions with the canonical term,
update dependent references, and preserve distinct concepts. Then revise
subsection openings and handoffs so each local
question is explicit and the transition carries only the supported dependency.

An unlisted technical term is not automatically an error if it is an ordinary
description used once, but a word that changes the actor, state, precondition,
effect, or availability semantics is a terminology violation even if it occurs
only once. A new name for a recurring concept, operation, representation, or
layer is a proposal: either replace it with the established term, or route it
to `Needs context` with the proposed glossary line and discuss it with the
author before adding it. Do not silently add it to the ledger.
Distinguish this generic unknown-term rule from a paper-specific disagreement
about which already-recorded term is correct.

After revision, re-scan every occurrence and every subsection boundary, and
run the glossary's banned-term scan. Verify
that the glossary, headings, captions, figure labels, equations, and prose use
the same mapping and pass the semantic contract check. A terminology or
subsection check is complete only when the final text is locally understandable
without relying on the discarded draft or the reader's memory of an earlier
subsection.
