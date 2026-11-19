---
name: exploration-report
description: Run an agent-driven exploration (benchmarks, measurements, feasibility studies, literature-backed comparisons, design-space sweeps) and record it as a reproducible, in-repo report with a short TL;DR, a scorecard that mirrors the task checklist, findings, caveats, anomalies, detailed per-question analysis, a data index, and reproduction steps. Use when the user hands over an exploration checklist or research questions and wants conclusions they can trust and rerun later. Trigger phrases include explore and report, exploration report, investigate and write up, benchmark report, feasibility study, "tell me the conclusions", "make it reproducible", update or conclude an exploration report, questions about or discussion of an exploration report the user has read.
---

# Exploration Report

## Goal

Turn an exploration checklist into a report that serves two readers:

- the user, who reads only the TL;DR and scorecard and must come away with the correct conclusions;
- a future agent or person, who must be able to check every claim against data and rerun the work.

```
checklist item → question (+ hypothesis) → method → data → result → verdict → TL;DR line
```

The report is a deliverable, not a log. It describes what is currently known about the exploration, with each claim traceable to evidence, and it keeps accumulating knowledge as the user discusses it (see [Accumulate Discussion Knowledge](#6-accumulate-discussion-knowledge)).

## Non-Negotiable Principles

1. **Every TL;DR claim traces to data.** A reader must be able to follow any number in the TL;DR to an analysis subsection, then to a data file, then to the script that produced it.
2. **Goals are hypotheses, not conclusions.** When an item says "prove X", record X as a hypothesis and report the verdict the evidence supports: supported, refuted, mixed, or inconclusive. A refuted hypothesis belongs in the TL;DR.
3. **Every checklist item appears in the scorecard.** That includes items not run, blocked, deprioritized, or added mid-exploration. Silence about an item reads as "done".
4. **Every number declares its source.** Measured, cited, derived, and estimated numbers are never interchangeable; see [Evidence Tags](#evidence-tags).
5. **Capture reproduction context while running, not afterward.** Hardware, software versions, commits, inputs, and command lines cannot be reconstructed reliably once the session ends.
6. **Separate caveats from anomalies.** A caveat is a known limit of the evidence. An anomaly is an observation that is not yet explained. Merging them hides the leads worth chasing.

## Workflow

### 1. Plan

Before running anything, turn each checklist item into a question with an answer criterion: what measurement or source would answer it, and what result would count as yes, no, or mixed. Record goals phrased as "prove", "show", or "demonstrate" as hypotheses.

Note dependencies between items. For example, a claim that a stage is "not a bottleneck" needs the ceiling it is compared against (peak throughput, bandwidth, or the neighboring stage's rate), so measure that ceiling first.

Ask the user only about items whose answer criterion is genuinely ambiguous. Otherwise state your reading in the report's Scope section and proceed.

The plan lives in the report's Scope and Scorecard sections. Do not write a separate plan document.

### 2. Run

Create the report directory first (see [Report Directory](#report-directory)) and run every experiment that the report will cite from a script under `scripts/`. Promote an ad hoc command to a script before citing its output.

For each run, save under `data/raw/<run-id>/`:

- the raw output, never edited afterward;
- the exact command line and parameters;
- an environment snapshot: host and hardware identifiers, OS and driver or firmware versions, tool and library versions, and the commit of the code under test, plus its diff if the tree was dirty.

Produce `data/derived/` files and `figures/` only from scripts that read `data/raw/`. Note surprises in the report's Anomalies section as they happen, while the context is still fresh.

Repeat measurements enough to report variability, and report what you repeated. If a measurement is a single run, say so.

### 3. Write

Start from [assets/report-template.md](assets/report-template.md). Write the Analysis sections first, then the Findings, Caveats, and Anomalies sections, then the Scorecard, and the TL;DR last. Writing the summary last keeps it from claiming more than the analysis shows.

### 4. Verify

Run the linter, [scripts/lint_report.py](scripts/lint_report.py):

```
python3 <skill-dir>/scripts/lint_report.py reports/<date>-<slug>/report.md
```

It checks the required sections, the status line, scorecard statuses, the TL;DR length, and relative links, and it fails on any template placeholder left in the report (`TODO`, `YYYY-MM-DD`); record unfinished items in the Scorecard as `not run` or `blocked` instead. It also traces every TL;DR quantity into the body with its unit (`42 GB/s` must reappear as `42 GB/s`, not `42 MB/s`) and checks each TL;DR bullet for an evidence tag and a confidence; these TL;DR checks warn while the report is `active` and fail once it is `concluded`. It cannot judge whether the evidence supports a claim. For that, spawn a reviewer subagent with a fresh context and ask it to:

- check that each TL;DR line and finding follows from the linked data, at the stated scope and confidence;
- look for comparisons with unstated or unequal controls;
- check that the Reproduce section names everything needed to rerun the work: prerequisites, inputs, commands, expected outputs, and approximate runtime.

Fix what the reviewer confirms, and re-run the linter.

### 5. Hand Off

In chat, give the TL;DR, the scorecard's unanswered or blocked items, and the path to the report. Apply `high-signal-writing` to the chat message, not to the report.

### 6. Accumulate Discussion Knowledge

Discussion after the user reads the report creates knowledge: answers, corrections, new interpretations, explanations ruled out, implications, decisions, and new questions. The report is where that knowledge accumulates, so a later reader gets everything the discussion established without the chat. A question is also a signal of a gap: if it needed asking, the report should have answered it.

1. Answer in chat first, from the report's data and sources. If the answer needs new experiments or sources, collect them under the Run rules. If the report is concluded, first ask whether to reopen it or start a follow-up report.
2. After each round, list what the discussion established and record each item where a reader would look for it:
   - an answer the report should already have given: the section that raised the question, such as a definition where the term first appears, or the method or setup of an Analysis subsection;
   - a corrected or narrowed conclusion: every place that states it, including TL;DR, Scorecard, Findings, and Analysis;
   - a new interpretation or mechanism: the Analysis subsection's interpretation, and Findings if it changes decisions;
   - an explanation considered and ruled out: the interpretation or the Anomalies entry it concerns, with what ruled it out;
   - an implication or decision agreed with the user: Findings;
   - a limit of the evidence: Caveats; an unexplained observation: Anomalies;
   - a new question or follow-up experiment: Open Questions.
3. Keep provenance. Tag claims that rest on discussion rather than on report data with `[discussion: YYYY-MM-DD]`, and state the reasoning or who asserted it. Record untested ideas as hypotheses, not facts.
4. Integrate rather than append. Rewrite the affected text so the report reads as one coherent account of current knowledge. Do not add a Q&A or FAQ section, and do not quote the user's questions in the report.
5. Add one dated Changelog entry per round that says what knowledge was added or changed, such as "defined the throughput denominator in Q2; ruled out PCIe contention as the cause of the 4 KiB dip; narrowed TL;DR 1 to 64 KiB blocks".
6. Promote knowledge that outlives this exploration, such as a hardware property, a rule of thumb, or a design decision, to the topic's repo-memory note, linking back to the report.
7. Verify by giving a fresh-context subagent only the updated report, the user's questions, and your list of established items, without the chat history. Fix every question it cannot answer from the report or answers differently from you, and every item it cannot find, then re-run the linter.

In chat, answer each question and list what you recorded and where.

## Report Directory

Keep reports in the repository where the exploration runs. Use the repository's existing reports location if it has one; otherwise use:

```
reports/<YYYY-MM-DD>-<slug>/
├── report.md
├── scripts/          experiment and analysis scripts the report cites
├── data/
│   ├── raw/<run-id>/ raw outputs, command lines, environment snapshots
│   └── derived/      processed tables, produced only by scripts
└── figures/          produced only by scripts
```

The date is the exploration's start date and does not change as the report is updated.

Commit data with the report. When a file is too large for the repository's conventions, keep it outside git and record in the Data Index its location, size, checksum, and the command that regenerates it.

## Report Structure

The required top-level sections, in order, are shown below. The template contains guidance for each.

| Section | Contents |
|---|---|
| Header | Title, `Status: active` or `Status: concluded`, start and last-updated dates, commit of the code under test, environment summary |
| Scope | The original checklist verbatim, your reading of any ambiguous item, and anything explicitly out of scope |
| TL;DR | The conclusions. At most five bullets: claim, key number with unit, the condition it holds under, and confidence |
| Scorecard | One row per checklist item: status, one-line answer (hypothesis verdict first), confidence, link to its analysis subsection |
| Findings | Facts that should change the user's decisions or expectations, including surprises and negative results |
| Caveats | Limits of the evidence: proxy workloads, single runs, cited instead of measured, untested regimes, unequal controls |
| Anomalies | Unexplained observations, each with what was seen, where, what was ruled out, and a suggested next check |
| Analysis | One subsection per question: question, method, setup, results, interpretation, evidence links |
| Reproduce | Prerequisites, setup, commands in order, expected outputs, approximate runtime, known pitfalls |
| Open Questions | Unanswered or newly raised questions, with suggested next steps |
| Data Index | Every data file and figure the report cites: path, what produced it, raw or derived, short description |
| Changelog | Dated entries for material changes while the report is active |

### TL;DR Rules

- Each bullet is one conclusion the user can act on. State it as a claim, not as a topic ("the new copy path costs 3.1x more CPU time per byte than the baseline", not "copy cost results").
- Include the key number, its unit, and the denominator (per byte of input or of output, per core or per device).
- State the condition under which the claim holds when it is narrower than the reader would assume.
- End with a confidence level and the evidence tag of the key number.
- Do not introduce anything in the TL;DR that the Analysis section does not support.

### Scorecard Statuses

Use exactly one status per row:

- `answered`: the answer criterion from planning was met.
- `partial`: some evidence exists, but the criterion was not fully met; say what is missing.
- `not run`: deliberately not attempted (deprioritized or out of time); say why.
- `blocked`: attempted but could not be completed; say what blocked it.

For hypothesis items, begin the answer with `Supported`, `Refuted`, `Mixed`, or `Inconclusive`.

### Confidence Levels

- **High:** measured directly, repeated with small variability, under conditions that match the claim.
- **Medium:** measured, but once, with notable variability, or under proxy conditions.
- **Low:** estimated, cited from external sources without a matching setup, or extrapolated.

### Evidence Tags

Tag every reported number with its source:

- `[measured]`: produced by this exploration; link the data file.
- `[cited: <source>]`: taken from a paper, datasheet, or public benchmark; give the reference and the setup it was measured under.
- `[derived]`: computed from other numbers; show the formula or link the script.
- `[estimated]`: an assumption or back-of-envelope value; state the assumption.
- `[discussion: YYYY-MM-DD]`: established in discussion with the user rather than by report data, such as domain knowledge or agreed reasoning; state the reasoning or who asserted it.

When a comparison mixes tags, such as a measured number against a cited one, say so in the claim and list the setup differences in Caveats.

### Analysis Rules

- State what was held fixed in every comparison: inputs, sizes, parameters, hardware, warmup, and repetitions. A comparison with unequal controls is a caveat, not a result.
- Report variability (range, standard deviation, or percentiles) and the number of repetitions next to each central value.
- Present the numbers in a table or figure, then interpret them. Keep interpretation separate from observation.
- When a claim is relative ("not a bottleneck", "fast enough", "matches"), report the ratio against the explicit reference it is relative to.
- Link the exact data file and script behind each table or figure.
- Record explanations considered and ruled out, with what ruled them out, so later readers do not re-derive dead ends.

## Living Reports

A report is `active` while its exploration continues. Update it in place: revise the TL;DR, Scorecard, and Analysis sections to reflect current evidence, and add a dated Changelog entry for each material change. Add rows for checklist items added later.

When the user concludes the exploration, set `Status: concluded` and stop editing it, except to fix errors and to record discussion knowledge that needs no new evidence (see [Accumulate Discussion Knowledge](#6-accumulate-discussion-knowledge)); each gets a dated Changelog entry. Follow-up work that needs new evidence starts a new report that links back to this one, unless the user reopens this one.

## Relation To Other Skills

- `repo-memory`: a report is a dated record of one exploration. Durable conclusions that should guide future work, including those established in discussion, go into the topic's repo-memory note, which links back to the report.
- `systems-evaluation-planner` and `systems-paper-plotting`: use them when report results are headed for a paper; the planner takes the report's `data/derived/` (with its Data Index and Reproduce section) as input data.
- `high-signal-writing`: applies to the chat handoff only.

## Done Criteria

- Every checklist item has a scorecard row with a valid status.
- Every TL;DR number is tagged and traceable to an analysis subsection and a data file.
- Caveats and anomalies are recorded separately, or each section states that there are none.
- The Reproduce section names prerequisites, inputs, commands, expected outputs, and runtime.
- The linter passes, and the reviewer subagent's confirmed findings are addressed.
- After a discussion round, a fresh reader answers each of the user's questions and finds each established item from the report alone.
- The report, scripts, and data are committed together.
