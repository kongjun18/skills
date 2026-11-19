# Logic Chain, Openings, and Flow

Read this when checking or repairing a logic chain, transitions, paragraph
openings, paragraph grouping, or subsection flow. Fix the chain before
polishing sentences: a paragraph in the wrong place wastes the polish.

## 1. Map the chain

1. Label each paragraph with one job: context, observation, pressure,
   requirement, failed approach, insight, design decision, mechanism,
   contract, tradeoff, evidence, result, limitation, or implication. A
   paragraph with two jobs is usually two paragraphs, or one job buried.
2. Write the one claim each paragraph establishes, in one line.
3. Read the claims in order as a standalone argument. This list is the logic
   chain. If it does not read as a forced progression, the prose will not
   either. If the project records a canonical narrative, check against it.

## 2. Detect logic jumps

A logic jump is any step that needs a fact, definition, or inference the
reader does not yet have:

- **Asserted bridge:** a pivotal claim is stated ("therefore, X") but not
  earned by what precedes it.
- **Term by fiat:** a mechanism or name appears before the text shows why such
  a thing is needed.
- **Skipped step:** the text promises step N and jumps to N+1.
- **Re-decision:** a paragraph re-argues a settled point; the chain looped.
- **Conflated roles:** two properties (for example a deterministic one and a
  workload one) are merged into one "together they let us" sentence. Split
  them and map each to what it licenses.
- **Unstated premise:** a definite noun phrase ("the X", "these X") or a
  "thus", "therefore", or "however" relies on something not yet stated.
- **Unmotivated requirement:** a requirement without the observation that
  forces it, or a mechanism without the requirement it serves.
- **Abstraction jump:** workload behavior to low-level detail with no
  intermediate design concept.
- **Dangling challenge:** numbered challenges or requirements are raised but
  never resolved, or are renamed later without a mapping.

For each jump, write the missing link in one sentence. If a premise is missing,
add it where the reader first needs it, usually upstream. If the premise exists
but the relation is invisible, repair the downstream opening (§4). A connective
cannot supply a missing premise or an unsupported causal edge. If the source
does not support the link, mark `Needs context`; never invent it.

## 3. Name every relation

For every adjacent sentence pair and paragraph boundary, name the supported
relation: claim and evidence, mechanism and result, consequence, contrast,
refinement, enumeration, specialization, purpose, or parallel alternative.

| Failure | Observable defect |
| --- | --- |
| Missing | The reader must supply a premise or relation to see why the next unit follows. |
| Redundant | The transition repeats an already clear relation, or both sides announce the move. |
| Incorrect | The wording claims causation, contrast, or verification the content does not support. |
| Indirect | Generic wording ("these gains", "such systems") hides the specific result or object. |

A direct continuation needs no connective. A transition promising to explain X
must be followed by analysis that does. Keep only the supported intermediate
causal steps; distinguish observation, established mechanism, and hypothesis.
Correlation, intended benefit, or a workload tendency is not causation. Align
an overpromising transition with what the analysis shows; if that changes a
scientific claim, it is an author decision.

## 4. The opening contract and handoff placement

**Rule (stated once):** the next paragraph's first sentence owns the
transition. It names the smallest concrete endpoint it needs from the previous
paragraph (an object, result, metric, or pressure), states the relation, and
states its own job. The previous paragraph ends on its own completed claim or
the concrete need it creates. No sentence exists only to announce the next
paragraph, and no paragraph opens on a brand-new noun with no link back.

```text
[short carried endpoint + relation] → [central subject] → [this paragraph's claim]
```

- Put the paragraph's central subject or operation early, normally as the
  grammatical subject or in the first short clause. Carrying the endpoint does
  not justify burying the subject in a long final clause. If both do not fit,
  shorten the endpoint, or state the job first and carry the endpoint in the
  second sentence.
- Keep the opening at the paragraph's abstraction level and to one main
  relation. Defer definitions, evidence, and details to later sentences.
- Do not restate the previous paragraph's explanation or preview a later one.

**First-sentence-only test.** Read only the first sentence of each paragraph in
order. Before Design, the reader recovers the setting or question, the
observation or pressure, the opportunity or requirement, and why each next
paragraph follows. In Design, the openings recover the selected order (for
example responsibility, operation, structure, consequence). In Evaluation,
they recover question, metric purpose, result, and interpretation. For a
comparison, they expose the shared question and the aligned alternatives. Fail
when a reader must read further to learn what a paragraph is about, must
reread the previous paragraph to resolve a referent, or sees details whose
hierarchy is invisible. A mismatch with the outline is a structural finding,
however fluent the sentences.

**Before Design**, every opening is a setting, observation, pressure,
opportunity, requirement, or design-independent insight. A proposed
representation, identifier, data structure, algorithm, or component never
appears in an opening merely because it will later solve the problem. The test
is about structure, not vagueness: later sentences add detail at the right
level.

## 5. Siblings and side branches

When adjacent paragraphs are alternatives under one umbrella claim, the second
opening names the shared parent and makes the parallel or contrast visible; it
does not read as an unrelated list item. A supporting mechanism, caveat, or
example that does not own the main progression stays a side branch.

## 6. Subsection autonomy and flow

Each subsection is locally understandable. Its opening states the local
question or purpose, names the object, and gives the minimum context, so the
reader need not reread the previous subsection. Prefer a forward bridge
("Because records live on several tiers, the system must locate them") over a
backward pointer ("As discussed above, this approach..."). Do not repeat a
stable definition when a short canonical noun phrase suffices.

Within a subsection, move through supported levels, commonly responsibility →
operation → structure or policy → implementation detail → consequence. Each
paragraph stays at one main level; a lower-level detail answers a question set
at the current level. Describe alternative structures after the operation or
requirement they serve. A concept is premature if it belongs to a later layer,
even when it is explained locally. Give a concept its own name only when later
reasoning distinguishes, measures, or operates on it; a one-use representation
stays an inline description. Every clause has a current or downstream job;
delete clauses that only anticipate a hypothetical question.

**Logical interface before implementations.** When a section presents a
service, index, or component and its implementations, state the responsibility
and the selected operations first, each operation's input, purpose, and output
before the structure that realizes it, then the implementation families. Say
"we focus on two operations" for a representative subset; reserve "exposes" or
"consists of" for an interface the source shows is exhaustive. Map named
systems to structures only when a source establishes the mapping.

## 7. Organization moves

A correct story does not make the current grouping, sentence order, or
openings correct. For each defect consider all six moves before a wording-only
repair: `merge` (two units do one job), `split` (one unit carries independent
steps), `reorder` (a prerequisite comes after its use), `relocate` (a caveat,
example, or evidence belongs with another claim), `delete` (bridge-only,
repeated, or no-job unit), `rewrite` (grouping sound, relation invisible).

**When a move is allowed (stated once):** a presentation-only move is allowed
during outline, drafting, and refinement work, with no extra approval, when
the story, claims and their strength, evidence, terminology, section
responsibilities, and the interfaces shared with neighboring scopes all stay
unchanged. Record it as an outline change and report it. A move that touches
any of those is an outline delta for the author. No move is allowed in the
final language pass (closed-world gate).

## 8. Comparisons and tradeoffs

- Put alternatives on one shared question and the same outcome axes, so the
  tension is visible ("A keeps reads fast but recovers slowly, whereas B
  recovers quickly but slows reads"). Preserve real asymmetry.
- State the reader-visible effect before the mechanism that explains it
  ("recovery is slow because the state is rebuilt after restart").
- A design choice is the source of both its benefit and its cost. Tie the net
  effect to the evaluated workload or configuration. "Shifts cost" needs
  evidence of a transfer; otherwise name the added cost directly.
- At a problem-to-design boundary, the opening carries the pressure and the
  purpose ("To shorten recovery, the system persists ...").
- Cite a figure that explains a core design choice in the same paragraph as
  the first core claim about it, with the canonical term in the source clause.

## 9. Sentence load

One main logical relation per sentence. An essential subordinate clause is
fine; split when a sentence introduces several new concepts, chains several
causal steps, or puts a condition far from the claim it qualifies. Prefer
concrete subjects and verbs over stacked noun phrases, and an active verb that
names the actual relation over a nominal phrase that hides it. Never drop a
condition, scope, or qualifier for brevity.

## 10. Section read-through checklist

- [ ] Each paragraph has one job and one claim; the claim list is a forced
      progression.
- [ ] Every opening carries its endpoint and its own job; the first-sentence
      summary matches the outline.
- [ ] Every concept is introduced once, before use, at the right layer.
- [ ] No paragraph re-decides a settled point; every numbered challenge is
      resolved or mapped.
- [ ] Correctness arguments (invariants, exact checks) stay distinct from
      performance arguments (locality, bounds, measurements).
- [ ] The section's last paragraph gives the next section its starting point.
