# Hierarchical Outline Research Workflow

Use this workflow when the author provides a rough story, a paragraph-level
plan, or an incomplete outline and expects the agent to work out most of the
presentation structure before the author edits it. The output is a research
artifact for discussion, not prose. It has three reader-facing levels and one
execution trace:

```text
L0 subsection claim and question
  → L1 paragraph claims and interfaces
    → L2 sentence propositions and relations
      → execution trace used by the prose writer
```

The author may enter at any level. The agent fills missing lower levels from
the supported claims, evidence, terminology, and section responsibility. It
does not invent facts or silently choose an unsupported claim. If a missing
lower-level relation cannot be recovered, mark it as unresolved and show the
smallest decision needed from the author.

## 1. L0: subsection contract

The highest level states the reader's local question and the answer the
subsection should establish:

```text
subsection_id
local_question
subsection_claim
why_the_reader_needs_it
scope_and_abstraction_level
incoming_claim_or_pressure
outgoing_claim_or_handoff
allowed_evidence
forbidden_later-layer_details
```

The subsection claim is one answer, not a list of topics. It should tell the
reader what the subsection establishes and why the next subsection can follow.
The agent derives candidate L0 contracts from the manuscript, adjacent
sections, evidence, and the paper-specific guide, then records alternatives
when the evidence supports more than one answer.

## 2. L1: paragraph claims and interfaces

Every paragraph is a unit in the subsection argument. Record:

```text
paragraph_id
role
local_question
paragraph_claim
incoming_endpoint
incoming_relation
provided_claims
evidence_and_scope
outgoing_endpoint
next_paragraph_need
opening_responsibility
abstraction_layer
```

`paragraph_claim` is the one result the reader should retain from the
paragraph. `incoming_endpoint` and `outgoing_endpoint` are the paragraph
interfaces. They are semantic endpoints, such as a measured pressure, a
design requirement, or a supported result, rather than vague labels such as
“transition.” `incoming_relation` states why this paragraph follows. The next
paragraph owns the transition in its opening; do not create a detached
handoff sentence merely to connect paragraphs.

The agent must first decide the paragraph order and these interfaces. Reading
only the paragraph claims and interfaces should recover the subsection's
argument. If it does not, revise L1 before expanding L2.

For Evaluation, an L1 paragraph claim is the result or explanation the
paragraph establishes. A metric, figure, table, configuration, or baseline is
evidence or context inside that claim, not the paragraph claim itself.

## 3. L2: sentence propositions and relations

For each paragraph, expand its claim into ordered sentence slots. Each slot
contains the fields in the [sentence-level realization contract](sentence-realization-contract.md):

```text
slot_id
role
proposition
reader_question
from
relation
evidence
scope
canonical_terms
introduces
provides
opening_requirement
allowed_merge
forbidden
```

The `proposition` is a concrete subject–predicate–object or
condition–consequence statement. “Explain the result” is not an L2 slot. Each
slot must have a supported edge to the previous slot and a downstream job.
Round 1 prose uses one slot per sentence by default.

Reading only the L2 propositions must recover each paragraph claim and the
relation to the next paragraph. If an L2 slot adds a claim that is absent from
L0 or L1, either add the supported claim explicitly at the higher level or
remove the slot. Do not let prose smuggle a new claim into a lower level.

For Evaluation, reject an L2 sequence of the form “metric → number → more
numbers” unless an interpretation, comparison, condition, cost, net effect, or
implication connects those values to the parent claim.

## 4. Agent research pass

The discussion agent performs the following research before presenting the
outline to the author:

1. Read the complete requested manuscript scope, adjacent context, fixed
   outline, paper-specific guide, terminology ledger, and available evidence.
2. Recover the section responsibility and candidate L0 claims. For Motivation,
   keep the opportunity independent of later Design details. For Evaluation,
   recover the question, result order, evidence scope, and design-centered
   breakdown requirements when active.
3. Build the semantic object and claim graph, including purposes, evidence,
   costs, conditions, and handoffs.
4. Propose the L1 paragraph order and interfaces. Compare alternatives when
   grouping or order is not determined by the evidence.
5. Expand each L1 unit into L2 sentence propositions, first-use order,
   evidence mappings, and canonical terms.
6. Run an independent outline review against the graph, terminology ledger,
   evidence, first-sentence-only view, and node-only view.
7. Return the hierarchical outline, unresolved decisions, alternatives, and a
   compact human sync view. Do not return a prose draft as a substitute.

In an automatic run, the agent may select a supported L0/L1 alternative when
one is clearly preferable and the choice does not change scientific meaning.
Record the rejected alternative and reason. In a manual run, stop at
`Awaiting outline alignment` after presenting the research result. The author
can edit any level before the execution contract is frozen.

## 5. Freeze interfaces before writing

After author alignment, freeze L0, L1, and L2 together. A later prose round
may improve wording, but it cannot change a paragraph claim, interface,
sentence proposition, relation, evidence scope, abstraction layer, or
canonical term without returning to the outline stage.

The prose writer receives the complete subsection L0/L1 context, the current
paragraph's L2 slots, the previous paragraph's passing outgoing endpoint, the
next paragraph's required input, and the terminology ledger. It writes only
the current paragraph and returns a sentence-to-slot trace and produced
endpoint. An independent reviewer checks the paragraph before the next one is
written. A failed paragraph is rerendered from its contract; it is never used
as an unverified interface for the next paragraph.

Once all paragraphs pass, the coordinator reads only the paragraph openings and
endpoints to verify subsection migration. Then the ordinary three prose rounds
may run over the passing subsection under the frozen contract.

## 6. Required research output

Return these artifacts in order:

```text
L0 subsection contract
L1 paragraph/interface table
L2 sentence-slot tables grouped by paragraph
outline alternatives and unresolved decisions
independent outline-review findings and acceptance conditions
human sync view
status: Awaiting outline alignment | Frozen execution contract
```

Do not collapse the three levels into a paragraph synopsis. The author needs
the hierarchy to modify the logic at the appropriate level, while the writer
needs the L2 contract to materialize the already aligned logic without
reorganizing it.
