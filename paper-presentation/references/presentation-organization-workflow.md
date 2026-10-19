# Presentation Organization Gate

Use this gate after the story or claim spine is aligned but before prose is
treated as a local wording problem. A correct story does not imply a good
presentation. The story graph says what the paper must establish; the
presentation graph decides how paragraphs and sentences let the reader recover
it.

## Activation

Run this gate whenever the author says that the story is right but the prose,
sentence relations, paragraph transitions, or openings are weak. Also run it
when a review finds repeated handoffs, overloaded sentences, list-like
paragraphs, buried paragraph topics, or unexplained jumps. It is required
before Round 1 when the source text is being substantially rewritten.

Do not treat this gate as optional English polishing. A presentation defect is
a structural finding when it changes grouping, order, sentence role, reader
backtracking, or the visibility of the paragraph's main claim.

## Independent presentation read

Read the current prose without relying on the author's story explanation or
the writer's intended transitions. Reconstruct:

1. the responsibility of each paragraph from its opening sentence;
2. the concrete endpoint and relation carried by every adjacent sentence;
3. the information order within each paragraph; and
4. the paragraph grouping and order a reader would infer.

Compare this reverse presentation graph with the aligned story and section
contract. If the story is recoverable but the presentation graph is not, keep
the story fixed and repair the presentation graph. Do not downgrade the defect
to a wording suggestion merely because all claims are technically present.

## Required organization diagnosis

For every affected sentence pair and paragraph boundary, record the defect and
the smallest structural move that repairs it:

- `merge`: two sentences or paragraphs repeat one job or one relation;
- `split`: one unit carries multiple independent concepts or logical steps;
- `reorder`: a prerequisite, claim, purpose, or consequence appears after the
  material that depends on it;
- `delete`: a bridge-only, repeated, or no-job sentence adds no information;
- `relocate`: a caveat, example, mechanism, or evidence belongs with another
  claim; and
- `rewrite`: the grouping is sound but the relation or topic is not visible.

Consider all six moves before choosing a wording-only repair. A target
organization must state the new paragraph roles, order, sentence roles, incoming
endpoints, relations, and outgoing handoffs. The change map must say what is
preserved from the story and what presentation unit moves.

## Opening-sentence rule

The opening must make the paragraph's own subject visible early. Use this
ordering when it fits the supported relation:

```text
[short incoming relation, if needed] → [central subject or operation]
→ [main claim or purpose]
```

The central concept need not be the first word, but it should normally be the
grammatical subject or appear in the first short clause. Do not satisfy the
handoff requirement by placing the important concept at the end of a long
sentence. If carrying the previous endpoint makes the opening overloaded,
shorten the relation, move the endpoint to a compact subordinate clause, or
make the paragraph responsibility the first sentence and carry the relation in
the next sentence. The opening must not be only a transition, a preview, or a
list of details.

Examples of the intended shape:

```text
To locate cached blocks across tiers, a global index tracks each prefix and
its block metadata.

The global index then supports prefix matching and prefix insertion.
```

The exact wording is paper-specific. The invariant is that the reader learns
what this paragraph is about before reaching its final clause.

## Assertive finding and decision policy

When story, claim strength, evidence, and terminology can remain unchanged,
presentation-only reorganization is an allowed repair. The reviewer should
report it as a `Violation` with an acceptance condition, not as an optional
style suggestion. The writer may merge, split, reorder, delete, or relocate
units within the authorized subsection and must update the outline and change
map.

Pause for author alignment only when the repair changes the story, a claim or
its strength, section responsibility, evidence scope, terminology decision,
or an inter-subsection interface. In automatic mode, select among supported
presentation organizations and record the rationale. Do not ask for permission
merely to remove a redundant sentence or make a paragraph's central concept
the subject of its opening.

## Gate

Pass only when:

- the first sentence of each paragraph states its responsibility and exposes
  its central concept early;
- every adjacent sentence pair has a named, supported relation;
- each paragraph has one dominant responsibility and no bridge-only unit;
- claims, mechanisms, evidence, caveats, and examples are grouped according to
  their declared roles;
- the first-sentence-only reading recovers the intended subsection path; and
- the target presentation graph is explicit enough for a writer to render
  without preserving the old sentence or paragraph boundaries.

If a later prose pass fails this gate, return to this gate and rerun the
affected semantic and language rounds. Do not patch a structural failure with
extra connectives or a final English polish.
