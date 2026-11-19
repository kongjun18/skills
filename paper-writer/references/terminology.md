# Terminology Contract

This is the shared terminology contract for every skill that writes, reviews,
or cleans paper text (`paper-writer`, `paper-presentation-review`,
`paper-hygiene`, `paper-review`). Other skills link here and do not restate it.

A technical term is a protected interface name, not ordinary prose. A shorter
or more familiar word can name a different operation, layer, state, or object.
The recurring failure is local optimization: an editor sees a long term, finds
a fluent near-synonym, and checks only the broad sentence meaning. Frequency,
dictionary similarity, a reviewer's wording, or a shorter line is not evidence
of equivalence. This lock outranks fluency, concision, line fitting, page
budget, and a request to use simpler words.

## 1. Authority

1. A current explicit author instruction. Record it as a glossary edit (§6).
2. The paper's glossary, `GLOSSARY.md` at the manuscript root, linked from the
   root `AGENTS.md`.
3. The project's writing guide and accepted outlines.
4. The first precise definition in the manuscript.

If the writing guide or an outline conflicts with the glossary, report the
conflict to the author. Do not silently edit either file. If no glossary
exists, use the writing guide and accepted decisions; do not create a glossary
unless the author asks.

One glossary serves every agent on the paper: writers, reviewers, verifiers,
hygiene passes, coordinators, and every subagent they dispatch. Every brief
includes the glossary path, and the agent reads the file from disk, not a
summary. A closed-world writer packet includes the full glossary text. No agent
keeps a private term list that departs from it. Only the coordinator (or the
single agent) edits it, and only after author approval; agents dispatched later
re-read it.

## 2. Glossary format

Three sections, one bullet per entry, continuation lines indented, no dates
(git history records changes).

```markdown
# Glossary

## Use
- term — meaning or scope; usage rule. ≠ distinct term

## Interchangeable
- term A ~ term B — how to choose between them

## Banned
- wrong term → replacement — reason
- wrong term (sense) → replacement — banned only in that sense
```

- **Use:** canonical terms. The note says what the term means and, if needed,
  where each form may appear (full name vs. short form). `≠ X` marks a nearby
  term that must stay distinct.
- **Interchangeable:** terms that name the same concept, with the rule for
  choosing. With no rule, either is allowed, but keep one choice per paragraph.
- **Banned:** terms that must not appear in new or revised text. `→ rephrase`
  means no single word fits. A parenthesized sense limits the ban to that sense.
- Delete a line to remove an entry; edit it in place to change it. No
  strikethroughs or history notes.

Example (neutral):

```markdown
## Use
- checkpoint — durable copy of in-memory state taken at a consistent point.
  ≠ snapshot (the on-disk file format)
- recovery time — from process start until the store serves reads
- write-ahead log — full name at first mention; `WAL` afterwards

## Interchangeable
- tail latency ~ p99 latency — `p99` only next to a figure that plots p99

## Banned
- restore time → recovery time
- flush (eviction sense) → evict — `flush` is reserved for log persistence
```

## 3. The terminology ledger

The ledger is a per-run working copy seeded from the glossary: Use and
Interchangeable entries become `active` with source `glossary`; Banned entries
become forbidden variants. Before outlining, drafting, refining, simplifying,
or accepting a reviewer rewrite, extend it with every recurring technical
item in scope: components, operations, states, data structures, metrics,
workloads, configurations, baselines, invariants, abbreviations, and figure
and table names. For each item record:

```text
concept_id | canonical form | definition and referent | layer
allowed forms | forbidden variants | distinct from | source | status
```

- `layer`: logical object, operation, mechanism, representation, backend
  encoding, implementation, metric, or example.
- `source`: author instruction, glossary, writing guide, aligned outline,
  cited source, or agent proposal.
- `status`: `active`, `provisional` (possibly technical, not yet classified;
  protect it until classified), `superseded`, or `disputed`.

A per-run ledger may add `Needs context` proposals but never overrides the
glossary. When an author instruction supersedes an older term, mark it
`superseded`, propose the glossary edit, and regenerate any outline rows that
used it before writing.

## 4. Lock rules

1. **Use terms exactly.** Grammatical inflection is allowed. Changes to word
   order, hyphenation, or capitalization (other than sentence-initial) are not.
   Never merge `≠` pairs, and never collapse different objects, operations, or
   levels because their strings look similar.
2. **Interchangeable terms** follow their selection rule. Interchangeability is
   not license to vary terms for style.
3. **Banned terms** never appear in new or revised text, including headings,
   captions, figure labels, tables, and alt text. Quoted names, citation
   titles, and code identifiers are exempt.
4. **No coined terms.** A recurring technical noun, operation, state, metric,
   or layer name that is neither in the glossary nor established in the
   manuscript is a proposal, not a wording choice. Use the established term or
   a plain description. If a new name is truly needed, route it to
   `Needs context` with the proposed glossary line. Ordinary one-off
   description is fine.
5. **Keep layers apart.** A backend encoding does not silently become the
   logical object it represents, an implementation example does not define its
   category, and an entity is not interchangeable with its representation, a
   whole with its component, or a collection with its members.
6. **Referents are recoverable.** Every group name ("these approaches"),
   pronoun, and demonstrative identifies one exact object or member set that
   the reader has already met. Repeating a short noun phrase beats an ambiguous
   anaphor.
7. **Brevity never replaces a term.** To shorten a line, delete or reorder
   unprotected words. If a term cannot be preserved, leave the long line or
   report `Needs context`.

## 5. Words that carry claims

**Modifiers are claims.** `efficient`, `fast`, `compact`, `direct`,
`lightweight`, `scalable`, `robust`, `small`, and similar words need a
property, a comparison axis, a scope, and support (a number, bound, figure, or
invariant). Otherwise cut the modifier or replace it with the supported fact.

**Verbs carry contracts.** For every operation or state-changing verb, the
actor, target or input, precondition, state transition, observable effect, and
scope are part of its meaning. A verb that changes one of these is a
terminology violation even if it occurs once and reads fluently. For example,
`retry` implies an earlier attempt failed; it cannot describe a first attempt
that was merely delayed.

**Introduce concepts operationally.** At first substantive use, the sentence
that uses a concept says what it is doing here: what it acts on or comes from,
and what it enables. Avoid defensive or tautological introductions such as
`we define X as X` or an isolated `X is ...` sentence. Use a standalone
definition only for a central named abstraction, formal notation, invariant,
or boundary that later reasoning depends on. A name, acronym expansion, or
near-synonym alone does not establish meaning.

## 6. Procedure for every edit

1. Load the glossary and writing guide; build or refresh the ledger.
2. Mark protected items in the outline and in the target passage.
3. Before changing a span, check whether it intersects a protected item. If it
   does, keep the canonical (or explicitly allowed) form and edit the
   surrounding words instead.
4. A new alias or replacement of a protected term requires an explicit author
   decision and a ledger update before the prose edit. Without that, keep the
   original wording and report `Needs context`.
5. **Protected-token diff.** Before accepting the edit, compare old and new
   text: canonical terms, their referents, operation and state distinctions,
   qualifiers, and cross-section uses still match. Any mismatch rolls the edit
   back; semantic similarity is not a passing condition.
6. **Glossary updates.** When the author corrects a term, or drift appears that
   the glossary does not cover, propose the exact line to add, edit, or delete
   and name its section. Apply it only on the author's instruction.

## 7. Banned-term scan

After any revision, search the edited scope for every banned term: whole words,
case-insensitive, including hyphen, space, and plural variants. Ignore file
paths, labels, and LaTeX comments. For a sense-limited ban, check each hit's
sense. Report `banned-term scan: N hits` with locations.

Role duties: a reviewer reports each banned occurrence in scope as a finding;
a writer replaces it with the listed replacement; a mechanical cleanup pass
replaces only entries with a single listed replacement and sends `→ rephrase`
entries to a writer.
