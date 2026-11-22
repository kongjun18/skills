---
name: teachme
description: Teach the user an unfamiliar repository, concept, or research direction with a self-contained HTML tutorial in the project's `_docs/tutorials/`. Writes the exam that would prove understanding first and builds the outline backward from it, calibrated to the user's background and focus points; the exam, not a fixed length, sets the size. Repo tutorials walk code with file:line citations; research tutorials are a light primer (why, how, landscape and timeline, issue-tracker field signals, gaps, and a research-direction plan list). Invoked as /teachme. Triggers include "teach me", "write a tutorial", "help me understand this repo / concept / research direction", "onboarding guide", "explain X in depth", "landscape and gaps of X". For a short chat answer, use high-signal-writing; a conference-paper survey into research ideas, system-research-scout; a full issue/PR census of a repository, repo-research-scout; a weekly arXiv digest, pull-recent-papers; benchmarks and measurements, exploration-report.
---

# Teach Me

Write a tutorial that takes this learner from what they already know to the point where they pass an exam on the subject, and that is true to its sources. The output is one HTML file a person reads in a browser, not a chat answer.

```
learner + focus → exam → sources → outline (backward from the exam) → write HTML → check script → review (fact, learner takes the exam, researcher) → hand over
```

## Non-Negotiables

1. **Exam first.** Before outlining, write the exam that would show the learner understands the subject: questions that need the model applied, each with a model answer and a pass criterion. Every lesson exists because an exam question needs it; material no exam question needs is cut, folded into a "Going deeper" aside, or moved to Further reading. The exam sets the length: a narrow goal gives a short tutorial, a broad one a long tutorial. There is no fixed lesson or page count.
2. **Teach the real subject, sourced.** Every claim about a repository comes from reading its code at a pinned commit; every claim about a concept, system, or paper comes from a source you opened in this session. Never write a citation, API name, number, or paper from memory. When sources disagree or are missing, say so in the tutorial.
3. **Start from the learner, not the subject.** The learner's background, goal, and focus points decide what to skip, what to explain, and the order. A tutorial that is correct but starts in the wrong place has failed.
4. **One mental model, one running example.** The big-picture section states the whole model in a paragraph and a diagram; every lesson zooms into one part of it, using the same concrete example throughout.
5. **Separate sourced from synthesized.** Gaps, research directions, and comparisons you draw yourself are labelled as your synthesis and cite the evidence they rest on.
6. **Write to the project, commit nothing.** The tutorial goes to `<project-root>/_docs/tutorials/<slug>.html` (step 5; the shared [`_docs/` layout](../repo-memory/references/docs-layout.md)) and is not committed unless the user asks.

## Workflow

### 1. Frame the learner, goal, and focus

Settle these before reading sources:

- **Subject and kind**: `repo` (a codebase), `concept` (an idea, algorithm, protocol, or technique), or `research` (a research direction or problem area). A repository tutorial about one concept it implements is still `repo`.
- **Learner**: what they already know. Read `${XDG_CONFIG_HOME:-~/.config}/agent-skills/user-profile/profile.md` if it exists, and any harness memory.
- **Goal**: what the learner must be able to do afterward ("modify the scheduler", "read papers in this area and spot open problems", "explain why X beats Y"). If the user did not say, choose the goal a person with this background most plausibly has.
- **Focus points** (optional): aspects the user says matter most. Each one gets at least one exam question.

You choose the outline and the questions; do not ask the user to design them. State your reading in one line and proceed. Ask, in one batch, only when the subject itself is ambiguous (two different things share the name) or the goal would change the kind.

### 2. Write the exam

Draft the exam from the goal, the focus points, and a first skim of the subject; revise it after the sources are read. How to write exam questions, model answers, and pass criteria: [pedagogy.md](references/pedagogy.md#the-exam). Read it now.

The exam covers the core mental model and every focus point; for `research` it also asks the learner to place a new system or paper in the landscape and to judge a gap. Each objective in the tutorial corresponds to one exam question.

### 3. Gather sources

How to read each kind of subject, what to pin, how to collect field signals from issue trackers, and the outline skeleton for each: [subjects.md](references/subjects.md). Read it for every tutorial.

Keep a private source list while reading (claim → file:line, URL, or issue link); it feeds the citations, the walkthrough, and further reading. For a large repository or a broad research area, split the reading across subagents by component or sub-area, and have each return claims with their sources.

### 4. Design the mental model and outline

1. Write the one-paragraph mental model: the problem, the core idea, and the parts that make it work.
2. Choose the running example: one concrete input, request, scenario, or paper that touches most parts.
3. Work backward from the exam: for each exam question, list what the learner must know to answer it; group that into lessons, one idea each, ordered so each needs only earlier ones. Each lesson's check-yourself question is a smaller step toward an exam question.
4. Cut every lesson no exam question needs. If the exam has grown past what the goal needs, cut the exam first.

Go straight on to writing; the handover lists the exam so the user can redirect a follow-up. How to teach each lesson (concrete before abstract, diagrams, misconceptions, depth): [pedagogy.md](references/pedagogy.md). Read it before writing.

### 5. Write the HTML

Copy [assets/tutorial-template.html](assets/tutorial-template.html) to `<project-root>/_docs/tutorials/<slug>.html`. `<project-root>` is the Git root of the directory the user is working in, else that directory; it may differ from the repository being studied. If the project's own rules forbid generated output inside it, ask the user for a directory instead. Fill every `{{...}}` and `TODO`, and delete what does not apply, including the template's comments.

For repo tutorials, produce every code excerpt and citation with `scripts/excerpt.py` (usage in [html-format.md](references/html-format.md#code)) so the excerpt is copied from the pinned commit, escaped, and linked; never retype code. Components, citation format, diagrams, math, and code-block conventions: [html-format.md](references/html-format.md). Read it before writing.

Required sections: objectives, prerequisites, big picture, the lessons, the walkthrough (repo tutorials, ending with "Where to change things" when the goal is to modify the code), gaps and research directions (research tutorials), the exam, summary, glossary, further reading.

### 6. Check

```bash
python3 <skill>/scripts/check_tutorial.py _docs/tutorials/<slug>.html --check-urls [--repo <repo-root>]
```

`--repo` is required for repo tutorials; it verifies every code citation's file and line range at the pinned commit. `--check-urls` fetches every web link; drop it only when offline, and say so in the handover. Fix every error. The script checks structure only; it cannot tell whether the teaching is right.

Then render the page (a headless browser screenshot when one is available, otherwise open it in a browser) and confirm the diagrams render, code is highlighted, and math displays. If you could not render it, say so in the handover.

### 7. Review

Dispatch fresh subagents with the briefs in [agents/reviewers.md](agents/reviewers.md), in parallel:

- **Fact checker**: verifies each claim against its cited source and flags uncited claims.
- **Learner**: reads cold as the target learner, then takes the exam. Give it a copy without answers, made with `scripts/strip_answers.py _docs/tutorials/<slug>.html <scratch>/<slug>-noanswers.html`, outside the project. A failed exam question is a defect in the lessons, unless the question asks for more than the goal needs; then fix the exam.
- **Researcher** (research tutorials only): checks that each gap rests on its cited evidence and is not already solved, and that each direction's first steps are concrete.

Fix what they find, re-run the check script, and repeat the review only if the fixes were substantial. Skip the review only when the user explicitly asked to skip it or to go fast; a request for a short tutorial is not that. Say so in the handover.

### 8. Hand over

Report in a few lines: the file path; the learner, goal, and focus you wrote for; the exam questions, one line each, with the learner reviewer's result on each; the lessons; the commit or source date it is pinned to; check-script and render status; review findings you did not fix and why; and the gaps or disagreements the sources left open. Suggest the next tutorial only if the goal clearly needs one.

## Updating a Tutorial

When the user asks a follow-up about a tutorial, answer in chat, then ask whether to fold the answer into the tutorial. A question that reveals a confusing passage is a defect: fix the passage, not just the answer. A question the exam did not anticipate becomes an exam question.

Fold new material into the existing outline: extend the exam, then put each new idea in the lesson it belongs to. Never append a chapter or deep dive that repeats an existing lesson's subject; merge them. When the repository has moved past the pinned commit, re-verify the citations against the new commit and update `source-commit`.

## Done Criteria

- [ ] Learner, goal, focus, and kind stated in the header meta line; each objective has one exam question; each lesson serves at least one exam question.
- [ ] Big picture gives the whole model in one paragraph and one diagram; one running example used throughout.
- [ ] Every lesson has a check-yourself question; every exam question has a model answer and a pass criterion.
- [ ] Every claim traces to a source opened in this session; repo tutorials pinned to a commit with file:line citations; synthesis labelled.
- [ ] `check_tutorial.py` passes with no errors; the page was rendered, or the handover says it was not.
- [ ] Fact-checker, learner (exam taken), and, for research, researcher reviews done and addressed, or skipped with the reason given.
- [ ] Nothing committed in the studied repository unless the user asked; scratch files removed.
