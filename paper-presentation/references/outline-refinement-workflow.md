# Structured Outline Refinement Workflow

Use this workflow inside `discuss` before returning a structured outline to the
author. It applies three different gates to the semantic intermediate
representation. It is not three prose rewrites.

## Round 1: construct the semantic graph

From the aligned story, section purpose, evidence, writing guide, and
terminology ledger, build the [semantic object and logic graph](semantic-object-graph-workflow.md).
Create typed nodes for concepts, claims, evidence, purposes, mechanisms,
metrics, results, costs, conditions, and handoffs. Add supported relations and
derive paragraph roles, argument nodes, and sentence slots from the graph.

The round fails when a node has no object, purpose/question edge, evidence or
reasoning basis, scope, or downstream role. It also fails when the output is
only a paragraph summary.

## Round 2: independent graph and lexical review

Use a separate reviewer call or clean review pass. It must not write prose.
Check:

- claim–evidence direction and support;
- purpose edges for Design mechanisms and Evaluation metrics/results;
- benefit, cost, condition, and net-effect relations;
- undefined, premature, duplicated, or dangling objects;
- technical nouns, noun phrases, adjectives, adverbs, verbs, and relation
  words against provenance and canonical forms;
- technical modifiers against property, comparison axis, scope, and support;
- sentence slots that would need to invent a concept or causal relation; and
- paragraph handoffs and first-sentence responsibilities.

Return findings with node or lexical IDs and acceptance conditions. The
coordinator repairs the graph and reruns the affected checks. Do not hide a
missing edge by writing a smoother summary.

## Round 3: author-facing projection

Render the approved graph as the human sync view. Show section navigation,
paragraph roles, and every sentence slot or logical node with its object, type,
short semantic payload, relation, evidence, purpose/question edge, and
handoff. Remove internal metadata, but do not remove logical nodes or collapse
them into vague instructions such as “explain the result.”

The round fails when the projection is not a faithful graph view, when a term
appears without provenance, or when the author cannot inspect the complete
logic chain without reading draft prose.

## Output gate

Return the outline only after all three rounds pass. Include the semantic graph,
the execution outline, the sentence/logic-level human sync view, open author
decisions, and the exact status `Awaiting outline alignment` when user choice
is still required. Prose review and revision start only after that alignment.

When the input was only a paragraph-level chain, these three rounds are also
the outline-completion pass: the coordinator supplies the missing concrete
sentence propositions and relations, the independent reviewer checks them, and
the author may edit the human sync view before the execution contract is
frozen. The user is not expected to author every slot. A coarse outline is
accepted as input, but it is never passed directly to a prose writer.
