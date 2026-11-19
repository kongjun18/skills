# Multi-Agent and Autonomous Runs

Read this when the user asks for autonomous end-to-end improvement of a
section, or when several subagents write different subsections in parallel.
Single-agent work does not need it.

## 1. Roles and the governing rule

- **Coordinator** (this agent): owns the outline, the glossary edits, the
  version ledger, merging, and every decision that touches a shared interface.
- **Reviewers**: read-only; return findings with acceptance conditions.
- **Writers**: edit only their owned units, from a frozen packet.
- **Verifier**: fresh, read-only; checks the integrated result against the
  outline and acceptance conditions without the writers' rationale. Brief it
  with `paper-presentation-review`.

**Serialize decisions, parallelize local writing, serialize the merge.**
Story, outline, and interface decisions are made once by the coordinator.
Writers then work in parallel only on disjoint subsections whose incoming and
outgoing interfaces are frozen. Merging and integrated verification are
sequential. No two agents edit the same moving draft.

**Autonomous choices.** In an autonomous run the coordinator may choose among
supported presentation alternatives (order, grouping, pattern) when the choice
changes neither a claim, its emphasis, nor the contribution; it writes the
choice and the rejected alternatives into the outline. A choice that would
change those stops the run for the author. When alternatives tie, choose the
simpler and record the ambiguity.

## 2. Freeze before dispatch

Bind every handoff to a content hash or revision ID of the manuscript and of
the outline. Create one scope manifest:

```text
manuscript version | outline revision and status | glossary path
owned units per writer (disjoint) | read-only context units on both sides
per-subsection contract: question, claim, from, gives, protected evidence,
  terms, allowed local changes | owner of each shared edge
```

The boundary between the last paragraph of one subsection and the opening of
the next belongs to one named owner, normally the coordinator.

## 3. The writer packet (closed world)

For each paragraph or subsection, the writer receives:

```text
subsection L0 and the L1 lines of every paragraph in it
the owned paragraphs' L2 lines (always present when delegating)
the endpoint the previous paragraph actually produced (checked text, not a draft)
what the next paragraph needs
full glossary text and the active ledger
allowed evidence and exact scopes
```

The writer returns the prose, a sentence-to-line trace, a list of new lexical
items (expected: none), unresolved lines, and the endpoint produced. It may
improve grammar, rhythm, and connective wording. It may not add a technical
object, term, modifier, operation, state-changing verb, evidence item, causal
edge, scope condition, or implementation detail; an unlisted term is an
`unknown-lexical` failure even when it sounds like a synonym. A line it cannot
render naturally is returned as unresolved, never improvised.

Within a subsection, paragraphs are written in order, and only a paragraph that
passed its check becomes context for the next. If the runtime offers only one
writer call, run the same loop inside it.

## 4. Check, roll back, route

After each writer call, an independent check rebuilds the paragraph or
subsection blind and compares it with the frozen packet. Classify the diff as
`wording-only` only if the contract is unchanged. Otherwise roll back to the
last passing text and route the issue to its earliest cause:

| Diff | Route to |
| --- | --- |
| unknown or changed term | terminology decision ([terminology.md](terminology.md)) |
| invented, missing, or changed claim or object | outline or story decision |
| changed order, opening job, relation, or handoff | outline delta |
| changed evidence or scope | claim and evidence decision |

Never feed a failed artifact to the next step. A writer that needs a changed
interface returns an outline delta; the coordinator updates the outline,
invalidates only the affected patches, and reruns those writers.

## 5. Merge and integrated verification

The coordinator checks that every patch uses the manifest's version, owned
units are disjoint and complete, each patch meets its contract, and interface
changes are recorded. It applies the patches to one canonical version,
reconciles terms, figures, and boundary edges, and resolves conflicts at the
smallest shared claim or edge; it never picks a winner because one sounds
smoother. If two proposals imply different claims or responsibilities, ask
the author. If the baseline changed during the run, invalidate stale patches.

Then a fresh verifier reads the integrated artifact (not the worker outputs)
and checks the whole scope: reverse outline, first-sentence summary, shared
edges with one meaning each, subsection autonomy, terminology and banned-term
scan, evidence and scope.

## 6. Run ledger and status

Keep one short ledger entry per round:

```text
round | goal | input version | outline revision | findings opened and closed
writer output version | verification result | rollback target | next action
```

Finish with one status: `Complete` (no required findings in the checked
scope), `Awaiting author` (a story, outline, or term decision is open),
`Needs context` (missing evidence or fact), or `Needs revision` (the round
limit was reached with required findings open). Spend the deepest reasoning on
structure and independent verification, not on local wording. Never call a
self-checked result verified.
