# Paper Glossary

A paper's glossary is the author-owned list of the terms agents must use,
must not use, and may choose between. It exists so that no agent writes a term
the author never approved. The author grows it each time an agent gets a term
wrong. The glossary governs term choice. The terminology ledger is a per-run
working copy built from it.

## Location and authority

- One file per paper: `GLOSSARY.md` at the manuscript root, linked from the
  root `AGENTS.md`.
- For term choice, the glossary outranks the writing guide, outlines, and
  agent preference. A current author instruction outranks the glossary; record
  it as a glossary edit (see below).
- If the writing guide or an outline conflicts with a glossary entry, report
  the conflict to the author. Do not silently edit either file.
- If no glossary exists, fall back to the writing guide and accepted author
  decisions. Do not create a glossary unless the author asks.

## Sharing

One glossary serves every agent that writes or reviews the paper: writers,
reviewers, verifiers, hygiene passes, coordinators, and every subagent or
parallel worker they dispatch.

- Every brief, packet, or prompt for such an agent includes the glossary
  path. The agent reads the file from disk, not a summary or ledger excerpt.
  A closed-world writer packet includes the full glossary text.
- No agent keeps a private term list that departs from the glossary. Per-run
  ledgers may add `Needs context` proposals but may not override an entry.
- Only the coordinator (or the single agent, when there is no coordinator)
  edits the glossary, and only after author approval. After an edit, agents
  dispatched later re-read the file. Re-run the banned-term scan on outputs
  that used a changed entry.

## Format

Three sections. Each entry is one bullet. Indent continuation lines. No dates:
git history records when an entry changed.

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

- **Use**: canonical terms. The note says what the term means and, if needed,
  where it may appear (full name vs. short form). `≠ X` marks a nearby term
  that must stay distinct.
- **Interchangeable**: two or more terms that name the same concept. The note
  gives the rule for choosing one by context. With no rule, either is allowed,
  but keep one choice within a paragraph.
- **Banned**: terms that must not appear in new or revised text. `→` gives the
  replacement. Write `→ rephrase` when no single word fits. A parenthesized
  sense limits the ban to that sense, so the word stays legal elsewhere.
- To remove an entry, delete its line. To change it, edit the line in place.
  Do not keep strikethroughs or history notes.

Example (from a systems paper):

```markdown
## Use
- prefix matching — the complete index operation. ≠ point lookup
- adaptive routing-point refinement — full name in title, first mention,
  paragraph headings; bare `refinement` only after it in the same subsection
- persistent index — umbrella for durable, restart-recoverable index.
  ≠ on-SSD index
- recovery time — snapshot loading until the index serves prefix matches

## Interchangeable
- candidate filtering ~ pre-retrieval filtering — mechanism (titles, lists,
  evaluation) vs. matching-path step when its position matters
- candidate-set size ~ posting-list size — both |C(p)| in Design

## Banned
- continuation(s) → alternatives — prefix-sharing sequences that diverge
- marker → routing point — historical component name
- lookup (prefix matching) → prefix matching — `point lookup` is a single key
- rebuild (rematerialization) → routing-point rematerialization — `rebuild`
  is reserved for the recovery stage
- restoration time → recovery time
```

## Agent rules

1. **Load first.** Read the glossary before any outline, prose, review, or
   hygiene pass. Use it to seed the terminology ledger: Use and Interchangeable
   entries become `active` with source `glossary`. Banned entries become
   forbidden variants.
2. **Use** terms exactly as written. Grammatical inflection is allowed;
   changes to word order, hyphenation, or capitalization (other than
   sentence-initial) are not. Never merge
   `≠` pairs.
3. **Interchangeable** terms: apply the selection rule. Do not treat
   interchangeability as license to vary terms for style.
4. **Banned** terms: never write them in new or revised text, including
   headings, captions, figure labels, tables, and alt text. Existing text in
   scope: a reviewer reports each occurrence as a finding. A writer or hygiene
   pass replaces it with the listed replacement; `→ rephrase` entries go to
   a writer, not to hygiene. Quoted names, citation titles, and code
   identifiers are exempt.
5. **No coined terms.** A recurring technical noun, operation, state, metric,
   or layer name that is neither in the glossary nor established in the
   manuscript is a proposal, not a wording choice. Use a glossary term or a
   plain description. If a new name is truly needed, route it to
   `Needs context` with the proposed glossary line. Ordinary one-off
   description is fine.
6. **Updating.** When the author corrects a term, or an agent finds drift the
   glossary does not cover, propose the exact line to add, edit, or delete,
   and name the section. Apply it only on the author's instruction or
   approval. Keep each entry to one line where possible.
7. **Verify.** After revision, search the edited scope for every banned term.
   Match whole words, case-insensitively, and include hyphen, space, and
   plural variants. Ignore file paths, labels, and LaTeX comments. For a
   sense-limited ban, check each hit's sense. Report the result as
   `banned-term scan: N hits` with locations.
