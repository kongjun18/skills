# Local Paragraph Review and Revision Workflow

Use this workflow when the author asks to review or rewrite one paragraph or a
small contiguous paragraph scope directly, especially when the fixed outline
may be stale. The old outline is a baseline and synchronization record. It is
not allowed to block a local diagnosis or force the writer to preserve a
contradicted paragraph structure.

## 1. Bind the local scope

Freeze:

```text
paragraph IDs in scope
previous paragraph's passing endpoint and last sentence
next paragraph's opening and required input
local manuscript version
fixed outline revision
paper-specific guide and terminology ledger
edit authorization
```

Read enough adjacent context to recover both interfaces. Do not read only the
target paragraph when its opening or outgoing claim depends on neighboring
text.

## 2. Compare prose with the old outline

Build a local reverse outline and classify the result:

- `outline-consistent`: paragraph role, claim, order, interfaces, evidence,
  scope, and terminology agree;
- `prose-defect`: the outline is still the right target, but the paragraph
  realizes it poorly;
- `outline-stale`: the paragraph has a supported responsibility or claim that
  the old outline does not record; or
- `interface-conflict`: the proposed local repair changes the incoming or
  outgoing claim shared with an adjacent paragraph.

Do not silently treat `outline-stale` as a prose defect. Do not silently treat
an `interface-conflict` as a local wording choice.

## 3. Direct review route

For a direct `review` request, always review the supplied paragraph even when
the old outline is stale. Return:

```text
local reverse outline
outline comparison status
paragraph-level findings
sentence-level claim and relation findings
terminology and first-use findings
incoming/outgoing interface findings
local outline delta, if needed
acceptance conditions
```

The review remains read-only. A stale outline is a finding and a synchronization
task, not a reason to omit the paragraph review.

## 4. Direct revision route

For a direct `revise` request with edit authorization:

1. If the outline is consistent, revise from the frozen paragraph and sentence
   contracts.
2. If the outline is stale but the paragraph's interfaces remain unchanged,
   reconstruct the local L0 paragraph responsibility, L1 paragraph claim, and
   L2 sentence contract, then revise from that local contract. Record the
   smallest outline delta and update the fixed outline when the caller permits
   it.
3. If the requested repair changes a shared incoming or outgoing interface,
   preserve the surrounding manuscript, return the local revision proposal and
   interface delta, and route the shared decision to outline alignment. Do not
   invent a new neighboring claim to make the paragraph fit.

The old paragraph text is reference material, not an authority. If the author
asks for a rewrite rather than a wording fix, rebuild the local presentation
from the recovered claim and evidence instead of copying the old sentence or
paragraph order.

## 5. Local writing and verification

After the local contract is fixed, write one paragraph only. Require a
sentence-to-slot trace and verify:

- the opening carries the previous endpoint and states the paragraph's own
  responsibility;
- every slot, claim, evidence item, scope condition, and canonical term is
  preserved;
- the outgoing endpoint remains the one required by the next paragraph;
- no new object, mechanism, modifier, causal relation, or unexplained term is
  introduced; and
- the paragraph remains understandable with its adjacent interface context.

Then run a boundary check against the next paragraph. A local prose revision
may finish without reopening the whole paper when both interfaces and the
section responsibility remain unchanged. Report `outline-sync-required` when
the local outline delta has not yet been written to the fixed outline.

## 6. Routing summary

```text
direct review
  → local reverse-outline comparison
  → findings and local outline delta

direct revise
  → local reverse-outline comparison
  → local contract repair if needed
  → paragraph rewrite
  → independent paragraph verification
  → boundary/interface check
```

This route prevents stale global planning artifacts from blocking a useful
local review while preserving the fixed outline as the synchronization record
for later section-level work.
