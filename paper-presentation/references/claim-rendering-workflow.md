# Claim Rendering and Tension Workflow

Use this workflow after the story, section structure, paragraph order, and
sentence dependencies have been aligned. It addresses the last translation
from a correct argument to concise, direct, and technically precise prose. It
does not reopen the story or invent evidence.

The workflow is especially useful for comparison paragraphs, design tradeoffs,
core claims, paragraph openings, and the first paragraph that introduces a
figure or a named design choice. It is a focused pass rather than a second
full review of every sentence.

## 1. Render the reader-visible tension

For a comparison, identify the single question the alternatives answer and
put both alternatives on the same semantic axes. A useful internal record is:

```text
comparison question:
alternative A: reader-visible benefit | reader-visible cost | affected path
alternative B: reader-visible benefit | reader-visible cost | affected path
shared conditions and evidence:
```

The prose should let the reader see the tension directly, for example,
“A keeps matching queries fast but recovers slowly, whereas B recovers
quickly but slows matching queries,” when those effects and conditions are
supported by the paper. The exact wording depends on the evidence. The point
is to compare outcomes at the same level, rather than describing one option's
operation and the other option's access path.

Do not force a symmetric tradeoff when the alternatives do not have symmetric
effects. In that case, state the shared comparison question and preserve the
asymmetry explicitly.

For a design tradeoff, record the design choice as the source of the branches:

```text
design choice → benefit and affected metric/path
design choice → cost and affected metric/path
workload/configuration → observed net effect
```

This keeps a benefit such as fast recovery from being written as the cause of
an unrelated cost. Use “shifts cost” only when the supplied evidence supports
an actual cost transfer. Otherwise describe the added latency, retrieval, or
resource use directly.

## 2. State the effect before explaining the mechanism

When the outline records an operation but the reader needs an outcome, render
the outcome in the claim and use the operation as its explanation. For
example, “recovery is slow because persistent state is rebuilt after a restart”
is more direct than leaving the reader to infer slow recovery from “requires
rebuilding persistent state.” Likewise, “matching queries pay storage-access
latency to fetch persistent records” states the consequence before elaborating
the access path.

Keep the mechanism when it explains the result, but do not let it replace the
result. A claim contract should therefore distinguish:

- `reader_effect`: what becomes faster, slower, cheaper, or more expensive;
- `affected_path`: recovery, query processing, insertion, or another concrete
  path;
- `mechanism`: the operation or resource behavior that explains the effect;
- `metric_or_scope`: the metric, workload, configuration, or condition; and
- `causal_source`: the design choice, existing behavior, or workload property
  that supports the relation.

The shortest complete sentence normally names the subject, effect, and
relevant condition, then adds the mechanism when it improves understanding.

## 3. Render paragraph handoffs as purpose-bearing openings

At a paragraph boundary, carry the smallest concrete endpoint from the prior
paragraph into the next paragraph's first sentence. For a problem-to-design
boundary, the opening should name the pressure, the relation, and the next
responsibility, for example, “To reduce restart recovery time, the system
persists the state needed for recovery.” A generic “This design” or “These
results” is insufficient when the
reader cannot recover the endpoint immediately.

The previous paragraph may make the next need visible, but a separate closing
handoff is unnecessary when the next opening can carry the relation directly.
Do not add a transition word without the object, result, or pressure that it
connects.

## 4. Lock terminology while polishing

Use the canonical term from the terminology ledger when rendering a claim.
Prefer the established name of a persistent structure over a newly coined
alternative when both refer to the same object, and do not introduce a new
design dimension when the argument is about the persistent structure itself. A
semantic rendering or final English-polish pass should not create a new
technical noun,
abstraction level, or synonym merely to avoid repetition. If a genuinely new
distinction is needed, record it in the outline and terminology ledger before
using it in prose.

## 5. Anchor figures to the claim they support

When a figure explains a core design choice, place its first explicit source
clause in the same paragraph as the first core claim about that choice, unless
the figure is a paper-level overview. Use the established term in the figure
sentence, for example, “Figure 1 shows the persistent index and its two access
paths.” Follow the figure with the benefit, cost, or relationship that the
visual is meant to make easier to understand. Keep the figure's role and
caption synchronized with that claim.

## 6. Verification checks

Run these focused checks after claim rendering and before semantic prose
rendering or final English polishing:

1. **Parallel comparison:** both alternatives answer the same comparison
   question and use comparable outcome/path fields.
2. **Direct effect:** the intended metric or path consequence is visible
   without making the reader infer it from an operation alone.
3. **Causal source:** benefits and costs trace back to the correct design,
   mechanism, workload, or existing behavior.
4. **Purpose-bearing opening:** every noninitial paragraph carries its
   inherited endpoint and states its own responsibility.
5. **Term lock:** no unapproved technical variant or abstraction appears.
6. **Figure anchor:** the first figure sentence is adjacent to the concept or
   claim it supports.

If a check fails because the evidence or comparison frame is unclear, return
an outline delta or `Needs context` rather than making the prose sound more
decisive than the supplied material allows.
