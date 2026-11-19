# Reviewer lens: what reviewers want to see, and what they attack

Both the writer and the reviewer subagent use this file. In the Outline
stage, use it to choose the roles. In the Draft and Refine stages, use it to
check claims. In the Simplify stage, use it to decide which sentences carry
weight.

## What each paragraph must give the reviewer

| Role | The reviewer wants | Describing instead looks like |
|---|---|---|
| Context | Why this matters now, with one fact or number | A history of the field |
| Requirement | The property a solution must have, and why | A list of desirable features |
| Failed approach | The best form of the existing approach, and its measured failure | A weak strawman, or a failure with no number |
| Question | The one problem the paper solves, stated as a tension | "We study X" |
| Insight | The observation that makes a solution possible, with evidence; new to this paper | A technique the baselines also use |
| Design | Why each mechanism is necessary, and what it guarantees | A component list |
| Positioning | The relationship to each prior approach (alternative, foundation, extension target, complement, different trade-off) and the decisive difference on a substantive axis, with its consequence | A list of related systems, or a difference by data-structure name or domain |
| Results | Headline numbers against named baselines, with scope and costs | Gains only, or unscoped ratios |
| Contributions | What the reader can reuse or check, and where | A repeat of the design paragraph |
| Figure or table | One reviewer question, one takeaway readable without the text, and the named baselines | Data with no claim, a panel the text never cites, or a figure that repeats one sentence |

## What reviewers attack

### The idea
- **The obvious alternative design is unnamed.** Name it, give its cost as a
  number, and say why it falls short. If you do not, the reviewer names it
  and concludes the authors missed it.
- **"Insight" is used for something old.** A technique that the baselines
  also use is a first step, not an insight.
- **The nearest classic technique is missing.** Name the one a reader in the
  venue's community already thinks of, and state the real difference in one
  sentence. Do not describe the idea in words that describe that technique
  equally well.
- **A prior work is called deficient for not doing what it never aimed
  at.** A different objective is not a deficiency, and an unstudied
  extension is not an impossibility.
- **An inherited idea is not acknowledged.** A reviewer who knows the source
  reads the omission as a hidden overlap.
- **Related work is summarized wrongly.** One-clause summaries of other
  papers are easy to get wrong and easy for a reviewer to check. Verify each
  one against the paper.

### The claims
- **A bound has the wrong scope.** Say whether it holds per step, per
  request, or per lookup. A per-step bound written as global is false.
- **The correctness wording is too strong.** "Uses a result only after an
  exact check" may be true where "never misses" is not.
- **Extrapolated numbers pass as measured.** Lead with the measured anchor.
  Label fits and estimates. A rate often makes the point at any scale.
- **Units are mixed.** Do not give percentage points in one place and
  relative percent in another for the same quantity.
- **A ratio stands alone.** Give the absolute value and say who pays it.
- **Costs are hidden.** Say what the design gives up against each baseline.
  A cost the reviewer finds reads as a flaw.
- **Growth is overstated.** If state still grows linearly, say so and give
  the smaller constant.
- **The scope is missing.** Say why the obvious mitigations (replication,
  batching, caching) do not solve the problem. Claim only the workloads and
  regimes that the evaluation covers.

### The terms
- **A term is used before it is defined.** The abstract counts too.
- **Names differ from the body's.** Check baselines, metrics, and
  mechanisms, and watch for near-synonyms such as "snapshot" and
  "checkpoint". Treat a canonical term as protected: identify a mismatch and
  preserve the ledger's form rather than recommending a shorter synonym.
- **One word means two things.** Fix it so each term names one concept.

### Consistency
- **A number appears only in the introduction.** Every number there must
  also appear in the body or in a figure.
- **A cross-reference does not resolve.** Every one must resolve.
