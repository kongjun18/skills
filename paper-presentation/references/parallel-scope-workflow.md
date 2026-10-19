# Parallel Section Scope Workflow

Use this workflow when multiple agents discuss or revise different
subsections of the same paper section. The use case is valid: subsection-local
revision can reduce turnaround time. The agents must still share a fixed
argument graph, terminology ledger, section contract, and subsection
interfaces because subsection boundaries carry claims and handoffs.

The governing rule is: **serialize review alignment and interface decisions;
parallelize subsection-local revision after the interfaces are frozen; then
serialize merge and integrated verification**. Never let writers edit the same
moving draft or silently redefine a shared boundary.

## 1. Create a scope manifest

Before dispatching agents, freeze an input version and create one manifest with:

- `section_contract` and the relevant story and concept–claim graph;
- the fixed outline revision, exact section file, and selected subtree/order;
- stable subsection and paragraph IDs;
- one exclusive `owned_units` set for each writer;
- read-only `context_units` on both sides of each owned range;
- shared terms, figures, claims, and graph edges;
- a subsection contract for each owned range, including its local
  responsibility, incoming handoff, central claim, provided claims, outgoing
  handoff, protected evidence, and allowed changes, derived from the aligned
  fixed structured outline;
- the owner of each shared edge and the exact edge semantics;
- protected facts and evidence mappings; and
- the coordinator responsible for merging proposals and boundary decisions.

The writable sets must be disjoint. A worker may read adjacent units but may
not rewrite them. Assign every shared edge—especially the last paragraph of one
subsection and the opening of the next—to the coordinator or to one named
owner. Freeze these contracts before dispatching revision workers. If a
contract is still undecided, keep that decision in the alignment or discussion
stage rather than asking multiple writers to infer it independently.

## 2. Separate parallel discussion from parallel revision

Parallel `discuss` agents may inspect the same fixed version and propose
different interpretations or structures. Their outputs are proposals, not
decisions. The coordinator merges them into one target map before any writer
revises prose and compiles the subsection contracts described above.

Parallel `revise` agents are safe only when each has an exclusive writable
range, a fixed input version, and a frozen subsection contract. Each worker may
rewrite its local prose, reorder its local paragraphs, and repair its local
transitions within that contract. It must not silently change a provided claim,
incoming or outgoing handoff, global terminology, section contract, figure
placement, or cross-subsection claim. Workers should write isolated artifacts
or patches; they do not edit the canonical moving draft directly.

A worker may find that the fixed outline is insufficient. It must return an
explicit outline delta describing the changed claim or handoff and the
affected downstream contracts. The coordinator updates the fixed outline,
then reruns only the impacted workers. Do not hide an outline change inside a
fluent local rewrite.

## 3. Give every worker a boundary packet

Pass each worker:

- its owned units and explicit non-owned units;
- the section and subsection question;
- the incoming handoff it must preserve;
- the central claim and provided claims it must establish;
- the owned argument-node IDs, node roles, relations, and sentence mappings;
- the outgoing handoff it must preserve or explicitly propose to change;
- the paper [glossary](../../paper-presentation-review/references/glossary.md) path and the shared terminology and
  concept–claim nodes it may use;
- allowed evidence and scope conditions; and
- the fixed input version, relevant issue IDs, and allowed local changes.

The worker returns its proposed role or prose, touched nodes and edges,
provided claims, expected incoming/outgoing handoffs, terminology changes,
unresolved context, and any outline delta or conflict with neighboring units.
It must not return a silent edit to a neighboring subsection.

## 4. Integrate parallel revisions

Local revisions do not need to be merged in dependency order because they were
all produced from the same frozen baseline. The coordinator first checks:

1. every patch uses the manifest's input version;
2. owned ranges and argument-node IDs are disjoint and complete;
3. each patch satisfies its subsection contract; and
4. any interface change is explicitly recorded.

The coordinator then applies the disjoint local patches to one canonical
version, reconciles shared terms, figures, and boundary edges, and updates the
interface map. If an interface change affects a downstream subsection,
invalidate only the stale patches in that dependency cone and regenerate them
from the updated contract.

Resolve conflicts at the smallest shared node or edge. Do not choose a winner
because one paragraph sounds smoother. If two proposals imply different
claims, evidence mappings, or section responsibilities, mark `Needs context` or
route the choice to `discuss` before committing the merged version.

## 5. Verify the integrated section

After merging, run a section-level review on the complete fixed artifact. Check
that every owned unit is accounted for, every shared edge has one consistent
meaning, subsection openings are locally understandable, and the final
handoffs form the declared section graph. Re-run terminology, figure, scope,
and concept–claim checks across subsection boundaries. Independent verification
must read the integrated artifact rather than the individual worker outputs.

If the baseline changes during parallel work, invalidate patches based on the
old version and regenerate or rebase them through the coordinator. Do not
silently apply stale proposals.
