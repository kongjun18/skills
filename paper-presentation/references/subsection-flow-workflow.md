# Subsection Flow and Abstraction Workflow

Use this workflow after section and paragraph responsibilities are aligned and
before rendering manuscript prose. It compiles each subsection's local
question, concept set, information hierarchy, and boundary handoffs. It is
especially useful when a draft has correct facts but repeats handoffs, adds
unnecessary representation terms, mixes abstraction levels, or inserts
bridge-only paragraphs.

## 1. Compile the subsection contract

For each subsection, record:

- its local reader question and opening purpose;
- the concrete incoming endpoint from the preceding subsection;
- the object, operation, or result that the subsection owns;
- its abstraction level and the levels of its paragraphs;
- the concept layer allowed at this point and the concepts deferred to a
  later layer;
- concepts that are needed as independent objects or operations;
- concepts that should remain inline descriptions rather than named terms;
- the central claim and the claims it provides;
- the outgoing endpoint and the next subsection's need; and
- the transition mode at each boundary: direct continuation, purpose,
  consequence, contrast, or no explicit transition.

The subsection opening should answer what the subsection handles and why it is
the next step. It may carry a short concrete endpoint from the preceding unit,
but it should not restate the preceding unit's explanation.

## 2. Select the information hierarchy

Use the hierarchy that matches the subsection's question. A common Design
sequence is:

```text
responsibility or contract → supported operation → structure or policy
→ implementation detail → consequence or tradeoff
```

This is a reasoning aid, not a fixed template. A subsection can use another
order when its dependency graph supports it. Do not move from a low-level
representation to a higher-level purpose without an explicit reason. Do not
describe alternative structures before stating the operation or requirement
they serve.

Each paragraph should stay at one main level. A paragraph may explain a lower
level when that detail answers the question established at the current level.
Its first sentence should state the local responsibility, and later sentences
should explain it rather than silently changing the question.

Before prose rendering, run a concept-layer check. A concept can be locally
understandable and still be premature if it belongs to a later implementation
layer. In particular, do not introduce a proposed representation, encoding,
identifier, or data structure before the operation or requirement it serves.
For a high-level section, describe the needed capability or relation first and
defer the concrete realization to Design. If an existing system's concrete
realization is itself the observation, identify it as existing behavior and
preserve the scope that makes the observation relevant.

For a subsection that introduces an index, service, or other interface, compile
the logical interface separately from its implementations. Record the service's
responsibility, the operations selected for discussion, each operation's input,
purpose, output or effect, and the implementation families that realize it.
Use “we focus on” or “the operations relevant here are” when the subsection
selects representative operations. Reserve “exposes,” “provides,” or “consists
of” for an exhaustive interface claim supported by the source. This prevents a
discussion of two important operations from being read as a claim that the
system has only two operations.

Use this order when it matches the dependency graph:

```text
responsibility and stored association → selected logical operations
→ implementation families → per-family representation and procedure
```

Do not introduce a structure family before the logical operation it serves, and
do not let a structure detail silently redefine the operation's input or
result. Map representative systems to structures only when the manuscript or
an authoritative source supports the mapping.

## 3. Compile purpose-bearing boundaries

At every subsection and paragraph boundary, identify the smallest endpoint the
reader must carry forward. Render the next opening with:

```text
purpose or relation → current object/operation → local responsibility
```

Use a purpose opening when the next unit introduces an operation or structure,
for example, “To locate retained items, the index maps each item to metadata
for its stored representation.” Use a
consequence or contrast opening when that is the supported relation. Do not
restate the preceding paragraph's full causal chain.

The previous unit should end with its substantive claim or the smallest need
that makes the next unit necessary. The next unit should own the forward
transition. A sentence whose only job is to announce the next subsection is a
bridge-only sentence and should be removed when the next opening already
expresses that purpose.

Do not use a generic anaphor such as “this design” or “these structures” when
the shared object or operation can be named directly. If the source supports a
scope such as “commonly” or “in many systems,” preserve that calibration. Do
not turn a presentation transition into an unsupported universal claim.

## 4. Minimize and orient concepts

Give a concept a separate name only when later reasoning needs to distinguish,
refer to, measure, or operate on it as an independent node. A representation
alias, temporary encoding, or one-use implementation detail should remain an
inline description unless the argument depends on it later.

Introduce an ordinary concept through the sentence that uses it. State what it
acts on, what it enables, or why it appears here. A formal definition is useful
for a central abstraction, notation, invariant, or boundary that recurs in the
argument. Avoid defensive forms such as “we define X as X” and isolated “X is
...” sentences that add no role or purpose.

For every clause, record its reader-facing job: introduce a needed concept,
state a purpose, explain a claim, preserve a condition, or identify a
consequence. Delete a clause that only anticipates a hypothetical question and
has no later dependency. In particular, do not retain conversion or
representation details merely because they are plausible implementation steps.

Prefer responsibility-first wording for a central object. State the purpose or
operation, then the object and its relation, rather than opening with a generic
subject and a storage verb such as “the system keeps ...”. Choose an active
relation that matches the domain and evidence. In the `logical-interface`
profile, an index may track each sequence and map it to metadata for cached
state when that is the supported meaning. In another profile, the appropriate
relation may be stores, routes, compares, or produces. Avoid nominal wording
such as “recorded sequences” when it hides the actual relation.

Avoid wrapper phrases such as “generally implement these operations with” when
the intended claim is simply about which structures existing systems use.
Name the actor, operation, and scope directly, for example, “Existing systems
use X and Y for ...”, only when X and Y are already introduced and the supplied
scope supports the statement. This check is generic: it does not license a
new mechanism or a stronger universal claim.

## 5. Apply the simple-sentence rendering rule

Render the compiled contract in simple, direct English. A sentence may contain
an essential subordinate clause, but it should normally carry one main logical
relation. Split a sentence when it introduces several new concepts, chains
multiple causal steps, or places a qualification far from the claim it
qualifies. Prefer concrete subjects and verbs over stacked noun phrases.

Keep a clause when it preserves a necessary condition, scope, comparison axis,
or causal link. Shortening is not a reason to remove information needed to
interpret the claim. Avoid repetitive connectives, but retain the relation they
express through sentence order or a concise purpose, contrast, or consequence
clause.

## 6. Verify the compiled flow

Run these checks before semantic prose rendering:

1. The first sentence of the subsection states its object and purpose without
   requiring the reader to reread the previous subsection.
2. The first sentences of the paragraphs recover the subsection's progression.
3. The previous unit ends with a substantive claim, not a duplicated preview.
4. Each named concept has a later distinction or use that justifies the name.
5. Each clause has a current or downstream reader-facing job.
6. The order moves through supported abstraction levels without unexplained
   jumps.
7. A transition names the concrete relation and uses calibrated scope.
8. No sentence is long only because it is carrying several independent
   relations that can be stated more clearly as separate sentences.
9. No concept is merely defined locally while remaining premature for the
   subsection's abstraction level.
10. Openings state a purpose or responsibility before introducing a central
    object, and the active relation matches the domain-specific profile when
    the text describes indexing, mapping, tracking, or use.

After prose rendering, reconstruct the subsection contract without consulting
the plan. If the first-sentence summary, concept set, abstraction order, or
boundary ownership differs, return the issue to this workflow rather than
fixing it only through English polish.
