# Reference-Material Rebuild Workflow

Use this workflow when the author provides a poorly written subsection and
wants it rewritten or reorganized. In this route, the supplied subsection is
raw material for a new presentation. It is not the target structure and its
wording is not a style reference unless the author explicitly protects part of
it.

When the scope is Evaluation, also load the [Evaluation Presentation and
Rebuild Workflow](evaluation-presentation-workflow.md). Its evaluation
material audit and claim–evidence matrix refine this generic ledger; in
particular, they keep source order separate from Design order, evidence order,
and target narrative order.

## Route selection

Choose `rebuild-from-material` when any of the following is true:

- the author says that the old text is only reference material;
- the author asks to rewrite, reorganize, or improve a poor subsection without
  supplying an aligned target story and outline; or
- the current prose has structural, abstraction, or presentation defects that
  make its paragraph order an unreliable presentation plan.

Use ordinary `revise` only when the author explicitly wants to preserve the
current structure or supplies an already aligned story and outline. If the
request is ambiguous, use the rebuild route in a manual run and expose the
route decision before drafting. Do not silently treat a source-only request as
sentence polishing.

## Authority model

Keep the source text immutable and classify each source unit before writing.
The classification is about authority, not usefulness:

| Source material | Default authority | How to use it |
|---|---|---|
| Source-backed fact, result, condition, or scope qualifier | protected content | preserve its meaning and source mapping |
| Explicit author decision or canonical term from the writing guide | protected decision | use the canonical form |
| Plausible claim or interpretation in the old prose | candidate | verify against evidence and author decisions |
| Paragraph order, sentence role, transition, rhetorical framing | non-authoritative | rediscover from the story and section contract |
| Existing wording, synonym, metaphor, or local definition | non-authoritative | discard unless explicitly protected |
| Example implementation or named system mapping | scoped material | keep its scope; do not generalize it |

The old text is therefore a source of evidence candidates, not a source of
presentation authority. A source sentence does not become a required claim
merely because it is present. A source term does not become canonical merely
because it is repeated.

## Material audit

Before proposing prose, create a material ledger. Give each unit a stable ID,
source locator, concise content statement, type, confidence, evidence mapping,
scope conditions, terminology status, and tentative disposition:

- `retain`: the aligned target needs this fact, claim, condition, or evidence;
- `relocate`: retain the content but place it under another paragraph role;
- `merge`: combine it with another material unit without preserving its old
  sentence boundary;
- `split`: divide a source unit when it contains multiple target claims or
  evidence roles;
- `defer`: move it to a later subsection or section;
- `drop`: repetition, unsupported framing, obsolete wording, or content with
  no role in the target story; and
- `needs context`: meaning or support cannot be recovered faithfully.

Record the source paragraph order separately as `source_order`; never copy it
into the target outline by default. Record any source units deliberately not
used so that omission is a visible decision rather than accidental loss.

## Independent story recovery

Build the target story from the section responsibility, adjacent context,
evidence, and material ledger, not from the source paragraph sequence. Recover
the smallest supported chain of:

```text
local question → setting or prerequisite → observation or claim
→ pressure/opportunity → consequence or next need
```

Use the applicable section pattern. For Motivation, keep the recovery
design-independent and separate the high-level opportunity from naive
solutions and Design mechanisms. For Design, identify the responsibility,
operation, structure or policy, and consequence. For Evaluation, first recover
the Evaluation question and subsection archetype, then preserve Design order
only for a design breakdown while selecting the narrative order from claim and
evidence dependencies. Record the metric, cost, and workload/configuration-
dependent net effect. Keep competing story candidates as explicit alternatives
when the material does not determine one.

The first artifact returned to the author is a material audit plus the
independently recovered story and its open decisions. It is not a rewritten
subsection. In a manual run, wait for story alignment before synthesizing the
sentence-level outline.

## Outline recovery and alignment

After the author aligns the story, synthesize a new reader-facing outline. Do
not derive paragraph roles by copying the old paragraph boundaries. For every
new paragraph and sentence, record its role, incoming endpoint, relation,
required concepts, evidence mapping, provided claims, and outgoing handoff.
Run the first-sentence-only test and the subsection-autonomy check before
drafting. Present this outline for author alignment. Story agreement alone is
not structure agreement.

Only after the outline is aligned should the writer receive the material
ledger, approved contracts, terminology ledger, evidence mappings, and
read-only context. The raw source text remains available for evidence lookup,
but it is not the drafting template. If a source phrase or exact ordering must
be retained, mark it as an explicit author decision.

## From-scratch rendering and verification

Render the new subsection from the aligned contracts and material ledger. Run
the three named prose rounds in order:

1. semantic rendering from contracts;
2. presentation and logic repair; and
3. concise English polish.

The writer must preserve supported content and scope, but may split, merge,
relocate, or omit source units according to the disposition map. It must not
silently preserve a source transition, paragraph role, or term just because it
was in the old prose.

Verification compares the result with both the target outline and the
material ledger. Check that every retained claim has support, every dropped
unit has a disposition, no unsupported source claim was strengthened, and the
reverse outline follows the new target rather than the old paragraph order.
Report accidental source-structure inheritance as a finding even when the
sentences are fluent. A high lexical overlap is not by itself a defect when a
canonical term or technical statement must remain, but unexplained reuse of
the old organization is a rebuild failure.

## Anti-copy guard

During Round 1, prefer a contract-to-prose trace over a source-sentence-to-
sentence rewrite. For each output paragraph, record the material IDs used and
the target contract that requires them. Do not quote or closely paraphrase a
source sentence unless it is a protected technical statement or the author
approved the wording. If the new text follows the old order, require an
explicit dependency reason in the outline; otherwise regenerate the affected
structure before language polishing.

`draft-only` may stop after Round 1 only when the author explicitly requests
it. It does not change the rebuild route or make the source text authoritative.
