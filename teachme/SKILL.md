---
name: teachme
description: Teach the user an unfamiliar repository, concept, or research direction by writing a self-contained HTML tutorial into the project's `tutorials/` directory, calibrated to the user's background, built around one running example, with diagrams, check-yourself questions, code walkthroughs with file:line citations, a glossary, and verified further reading. Invoked as /teachme. Triggers include "teach me", "write a tutorial", "help me understand this repo / codebase / concept / paper area / research direction", "onboarding guide", "explain X in depth", "I don't understand X", "make me a tutorial in HTML". For a short answer in chat, answer directly (high-signal-writing); for a survey of recent conference papers into research ideas, use system-research-scout; for a weekly arXiv digest, use pull-recent-papers; for measuring or benchmarking something and reporting results, use exploration-report.
---

# Teach Me

Write a tutorial that takes this learner from what they already know to a working mental model of the subject, and that is true to its sources. The output is one HTML file a person reads in a browser, not a chat answer.

```
learner + goal → sources → mental model + outline → write HTML → check script → review (fact + learner) → hand over
```

## Non-Negotiables

1. **Teach the real subject, sourced.** Every claim about a repository comes from reading its code at a pinned commit; every claim about a concept or research direction comes from a source you opened in this session. Never write a citation, API name, number, or paper from memory. When sources disagree or are missing, say so in the tutorial.
2. **Start from the learner, not the subject.** The learner's background and goal decide what to skip, what to explain, and the order. A tutorial that is correct but starts in the wrong place has failed.
3. **One mental model, one running example.** The big-picture section states the whole model in a paragraph and a diagram; every lesson zooms into one part of it, using the same concrete example throughout.
4. **Understanding is tested, not asserted.** Each lesson ends with a check-yourself question that needs the idea applied, with a reasoned answer.
5. **Write to the project, commit nothing.** The tutorial goes to `<project-root>/tutorials/<slug>.html` (step 4) and is not committed unless the user asks.

## Workflow

### 1. Pin the learner and the goal

Settle three things before reading sources:

- **Subject and kind**: `repo` (a codebase), `concept` (an idea, algorithm, protocol, or technique), or `research` (a research direction or problem area). A repository tutorial about one concept it implements is still `repo`.
- **Learner**: what they already know. Use the user's profile or memory when the harness provides one; ask only about what it does not settle.
- **Goal and depth**: what the learner must be able to do afterward ("modify the scheduler", "read papers in this area", "explain why X beats Y"). The goal fixes the scope: material that does not serve it goes to Further reading.

If the request already settles these, state your reading in one line and proceed. Otherwise ask, in one batch.

### 2. Gather sources

How to read each kind of subject, what to pin, and the outline skeleton for each: [subjects.md](references/subjects.md). Read it for every tutorial.

Keep a private source list while reading (claim → file:line or URL); it feeds the citations, the walkthrough, and further reading. For a large repository or a broad research area, split the reading across subagents by component or sub-area, and have each return claims with their sources.

### 3. Design the mental model and outline

1. Write the one-paragraph mental model: the problem, the core idea, and the parts that make it work.
2. Choose the running example: one concrete input, request, scenario, or paper that touches most parts.
3. Order the lessons so each needs only the earlier ones. Three to seven lessons; one idea each.
4. Write the learning objectives as abilities, and check that each lesson serves one.

For a tutorial longer than about seven lessons, or when the learner's goal was unclear, show the user the objectives and lesson list and wait for agreement before writing. Otherwise go straight on.

How to teach each lesson (concrete before abstract, diagrams, misconceptions, question design): [pedagogy.md](references/pedagogy.md). Read it before writing.

### 4. Write the HTML

Copy [assets/tutorial-template.html](assets/tutorial-template.html) to `<project-root>/tutorials/<slug>.html`. `<project-root>` is the Git root of the directory the user is working in, else that directory; it may differ from the repository being studied. If the project's own rules forbid generated output inside it, ask the user for a directory instead. Fill every `{{...}}` and `TODO`, and delete what does not apply, including the template's comments.

For repo tutorials, produce every code excerpt and citation with `scripts/excerpt.py` (usage in [html-format.md](references/html-format.md#code)) so the excerpt is copied from the pinned commit, escaped, and linked; never retype code. Components, citation format, diagrams, math, and code-block conventions: [html-format.md](references/html-format.md). Read it before writing.

Required sections: objectives, prerequisites, big picture, the lessons, the walkthrough (repo tutorials, ending with "Where to change things" when the goal is to modify the code), summary, glossary, further reading.

### 5. Check

```bash
python3 <skill>/scripts/check_tutorial.py tutorials/<slug>.html --check-urls [--repo <repo-root>]
```

`--repo` is required for repo tutorials; it verifies every code citation's file and line range at the pinned commit. `--check-urls` fetches every web link; drop it only when offline, and say so in the handover. Fix every error. The script checks structure only; it cannot tell whether the teaching is right.

Then render the page (a headless browser screenshot when one is available, otherwise open it in a browser) and confirm the diagrams render, code is highlighted, and math displays. If you could not render it, say so in the handover.

### 6. Review

Dispatch two fresh subagents with the briefs in [agents/reviewers.md](agents/reviewers.md), in parallel:

- **Fact checker**: verifies each claim against its cited source and flags uncited claims.
- **Learner**: reads cold as the target learner and reports where they got lost, which term arrived undefined, and which check-yourself question they could not answer from the text. Give it a copy without answers, made with `scripts/strip_answers.py tutorials/<slug>.html <scratch>/<slug>-noanswers.html`, outside the project.

Fix what they find, re-run the check script, and repeat the review only if the fixes were substantial. Skip the review only when the user explicitly asked to skip it or to go fast; a request for a short tutorial is not that. Say so in the handover.

### 7. Hand over

Report in a few lines: the file path, the learner and goal you wrote for, the lessons, the commit or source date it is pinned to, check-script and render status, review findings you did not fix and why, and the gaps or disagreements the sources left open. Suggest the next tutorial only if the goal clearly needs one.

## Updating a Tutorial

When the user asks a follow-up about a tutorial, answer in chat, then ask whether to fold the answer into the tutorial. A question that reveals a confusing passage is a defect: fix the passage, not just the answer. When the repository has moved past the pinned commit, re-verify the citations against the new commit and update `source-commit`.

## Done Criteria

- [ ] Learner, goal, and kind stated in the header meta line; objectives are abilities that the lessons serve.
- [ ] Big picture gives the whole model in one paragraph and one diagram; one running example used throughout.
- [ ] Every lesson has a check-yourself question with a reasoned answer.
- [ ] Every claim traces to a source opened in this session; repo tutorials pinned to a commit with file:line citations.
- [ ] `check_tutorial.py` passes with no errors; the page was rendered, or the handover says it was not.
- [ ] Fact-checker and learner reviews done and addressed, or skipped with the reason given.
- [ ] Nothing committed in the studied repository unless the user asked; scratch files removed.
