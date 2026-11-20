# Pedagogy

Read before writing. How to turn sources into lessons a learner can follow.

## Order

- **Problem before solution.** Open each lesson with the question it answers or the failure it fixes. A mechanism without its problem is a list of facts.
- **Concrete before abstract.** Show the running example doing the thing, then state the general rule. A definition that arrives before any instance is hard to hold on to.
- **Known to new.** Connect each new idea to something the learner already knows (from their background or an earlier lesson), and say where the analogy breaks.
- **One idea per lesson.** If a lesson needs two key-idea callouts, split it.
- **Prerequisites are explicit.** If a lesson needs something the learner may lack, give a one-line refresher or a link in Before you start, not a detour mid-lesson.

## Words

- Define each term at first use with `<dfn>`, in plain words, and add it to the glossary. Use one name per thing for the whole tutorial; if the sources use several, list the aliases once in the glossary.
- Prefer short sentences and active voice. Name the actor: "the scheduler picks", not "a choice is made".
- Do not hide uncertainty. Mark what the sources do not settle ("the code does not say why; a likely reason is ...") and keep guesses visibly labelled.

## Diagrams

- The big picture always has a diagram. Add one to a lesson when the idea is about structure, flow, state, or time; skip it when prose is clearer.
- One diagram, one point. Label it with the tutorial's terms, not the code's abbreviations, and say in the caption what to notice.
- Reuse the big-picture diagram's layout in later diagrams so the learner can locate each zoom.

## Examples and walkthroughs

- The running example stays the same across lessons; each lesson adds the part it covers.
- Keep excerpts short (about 5–25 lines). Trim unrelated lines with a comment marker, and say what was trimmed if it matters.
- In a walkthrough, each step says what happens and why, and cites where.

## Misconceptions

Add a misconception callout where learners commonly go wrong: a plausible but wrong belief, and why it is wrong. Take them from the sources (FAQs, issue trackers, paper discussions) or from your learner reviewer; do not invent straw men.

## Check-yourself questions

A good question needs the idea applied, not a sentence recalled.

- Prediction: "What happens if ...?", "Which component handles ... and why?"
- Transfer: "Would this still work if ...?", "Where would you add ...?"
- Contrast: "Why does X need ... while Y does not?"

Avoid questions answered by copying a phrase from the lesson. Every answer gives the reasoning, not only the result, and every question is answerable from the tutorial plus the stated prerequisites.

## Depth

- Match depth to the goal. Detail the goal does not need goes into a collapsed `details.aside` ("Going deeper") or Further reading.
- Do not pad. A short tutorial that builds the right model beats a long one that covers everything.
