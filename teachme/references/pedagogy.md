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

## The exam

The exam is the tutorial's definition of done for the learner: a person who passes it has the model the goal needs. Write it before the outline (SKILL.md step 2), and teach so the learner can pass it.

**What to ask.** Pick the abilities the goal needs, then write one question per ability:

- Explain why: "Why does X need ... while Y does not?"
- Predict: "What happens to ... if ...?"
- Trace: "Follow this input through the system; what does each part do?"
- Transfer or design: "Would this still work if ...?", "Where would you add ...?"
- Critique: "A paper claims ...; what evidence would you ask for?"
- For `research`: place a system or paper the tutorial did not cover on the landscape, and judge whether a stated gap is real and what a first experiment would be.

Cover the core mental model and every focus point the user named. Ask each ability once; write as many questions as the goal needs and no more. Prefer questions whose wrong answers reveal a specific misconception.

**Answers.** Each question has a model answer that gives the reasoning, and a pass criterion: the one to three points a passing answer must contain ("A passing answer says ... and ..."). The learner reviewer is graded against the criterion.

**Fairness.** Every question is answerable from the tutorial plus the stated prerequisites, and none is answered by copying a sentence from it. If the model answer needs a fact the lessons do not teach, add it to a lesson or drop the question.

## Check-yourself questions

Each lesson ends with one: a smaller step toward an exam question, under the same rules — the idea applied, not a sentence recalled, and an answer that gives the reasoning.

## Depth

- The exam sets the depth. Detail no exam question needs goes into a collapsed `details.aside` ("Going deeper") inside the lesson it extends, or into Further reading.
- One subject, one place. A paper, system, or idea is taught in the lesson its exam question needs; a deep dive on it goes in that lesson's aside, not in a second chapter.
- Do not pad. A short tutorial that builds the right model beats a long one that covers everything.
