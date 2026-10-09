# Stage 3: rethink and simplify

Drafts produced by AI agents are verbose. They restate, hedge, narrate their
own structure, and describe where they should argue. This stage rethinks
each paragraph from the reviewer's side, then makes it as short as the
argument allows.

## Rethink first, per paragraph

1. In one line, write what the reviewer must conclude from this paragraph.
2. Mark each sentence:
   - **carries:** a claim, evidence, definition, cost, or bridge that the
     conclusion needs;
   - **repeats:** says what another sentence, the caption, or an axis label
     already says;
   - **describes:** states a fact with no consequence for the conclusion;
   - **frames:** announces structure ("In this section we...", "Note that",
     "It is worth mentioning").
3. Keep the carriers. Cut the rest, or turn a describer into a carrier by
   adding its consequence: describe X, therefore Y.
4. If the paragraph has no single conclusion, it is two paragraphs or none.

## Then simplify sentences

- **One point per sentence.** Split any sentence with three or more clauses.
- **Merge** two sentences that make one point.
- **Replace a clause with a number** when the number says it ("much faster"
  becomes "6x faster").
- **Use plain words.** "Use", not "leverage"; "about", not "approximately";
  "shows", not "demonstrates".
- **Drop hedges** that the evidence does not need ("may potentially",
  "it can be seen that"). Keep a hedge that scopes a real uncertainty.
- **Drop transitions** that the logic already carries ("Furthermore",
  "Moreover", "Additionally").
- **List names only when they are needed.** In an introduction, name a
  mechanism once, with what it buys.
- **Figure walk-throughs** state the trend and the numbers the claim needs.
  They do not restate the axes or the caption.

## Guardrails

- Never cut a claim, number, formula, citation, figure reference, or
  definition that a later sentence uses. Repair it instead.
- Keep every term defined before its first use after the cuts too.
- Recheck each transition: a cut sentence is often the bridge.
- Report the cuts: the word count before and after, and the sentences
  removed, each with its reason.
