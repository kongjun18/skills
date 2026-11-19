# Rebuild from Material and Author Replies

Read §1 when the author supplies a poor draft to be rewritten, and §2 when the
author replies to a review, a story, or an outline. For one paragraph or a few,
see [refine-and-simplify.md §1](refine-and-simplify.md#1-local-paragraph-work).

## 1. Rebuild from material

**Use this route** when the author says the old text is only reference
material, asks to rewrite or reorganize a weak subsection without an agreed
outline, or when the draft's structure is unreliable. Use ordinary refinement
only when the author wants the current structure kept or supplies an agreed
outline. If unclear, say which route you chose and why before drafting.

**Authority.** The old text is evidence, not a plan.

| Source material | Authority | Use |
| --- | --- | --- |
| Source-backed fact, result, condition, scope | protected | keep meaning and source |
| Explicit author decision, glossary term | protected | use canonical form |
| Plausible claim or interpretation | candidate | verify against evidence |
| Paragraph order, sentence roles, transitions, framing | none | rediscover from the story |
| Wording, synonyms, local definitions | none | discard unless protected |
| Example or named-system mapping | scoped | keep its scope; do not generalize |

**Material ledger.** Give each source unit an ID, locator, one-line content,
type, evidence, scope, terminology status, and a disposition: `retain`,
`relocate`, `merge`, `split`, `defer`, `drop` (repetition, unsupported framing,
no role), or `needs context`. Record the old order as `source_order` only. An
unused unit has a recorded reason, so omission is a decision, not an accident.

**Recover the story independently** from the section's job, adjacent context,
evidence, and ledger (smallest supported chain: question → prerequisite →
observation or claim → pressure or opportunity → consequence). Apply
[sections.md](sections.md) and, for Evaluation, [evaluation.md](evaluation.md).
The **first artifact** returned to the author is the ledger, the recovered
story, alternatives, and open decisions. It is not a lightly edited draft.
After the author agrees on the story, build a new outline
([outline-contract.md](outline-contract.md)) without copying old paragraph
boundaries; after the outline is agreed, draft from the outline and ledger.

**Anti-copy guard.** Trace each output paragraph to the outline rows and
material IDs it uses, not to source sentences. Do not quote or closely
paraphrase a source sentence unless it is a protected technical statement or
the author approved it. If the new order matches the old one, record the
dependency reason; otherwise rebuild the structure before polishing. Verify
that every retained claim has support, every dropped unit has a disposition,
no source claim was strengthened, and the reverse outline follows the new
outline. Unexplained inheritance of the old organization is a finding even
when the prose is fluent. High lexical overlap is fine when canonical terms or
technical statements must stay.

## 2. Reading author replies

Treat a reply as a state change. Classify each statement as a finding decision
(accepted, rejected, deferred), a story or claim decision, a structure decision
(grouping, order, role, handoff), a prose constraint, or an edit
authorization. Record decisions in the outline, then deliver the next artifact
in the same turn instead of waiting for another command:

- story agreed, no complete structure → build the outline and wait for
  agreement;
- findings accepted, no complete structure → build the outline delta and wait;
- a complete outline or paragraph map supplied → validate it against the
  manuscript and evidence; if it passes, mark it agreed; otherwise return the
  smallest delta;
- outline agreed and edits authorized → draft and refine through the review
  loop and the closed-world gate without asking for each pass;
- several supported structures or insights remain → show them and the
  smallest decision needed.

Do not confuse similar events:

- "This problem is real" accepts a finding; it does not authorize a rewrite.
- "The story should go this way" settles the story, not paragraph order.
- "Revise per this outline" authorizes writing only after the outline is
  complete and checked.
- "Rewrite using this as reference" authorizes extracting material (§1), not
  keeping its order or wording.
- "Just polish it" does not reopen story or structure.

If a reply is ambiguous about a claim, structure, or section responsibility,
ask one focused question rather than choosing silently.
