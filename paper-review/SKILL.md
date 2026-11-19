---
name: paper-review
description: Reviewer-side work on someone else's academic paper, with every review claim checked against the manuscript. Two modes. develop-my-review turns the user's notes, questions, or draft into an English conference review, auditing each opinion against the paper, verifying claims, refining, and formatting for Google Docs. independent-review writes a review from scratch with a compact rubric (contribution, soundness, evaluation, reproducibility, presentation). Use for "review this paper", "help me write my review", "check/refine my review", "is this criticism fair", "reviewer report". Does not edit the manuscript. For improving your own paper's presentation, use paper-presentation-review; for mechanical and number-consistency checks, use paper-hygiene in audit mode; for citation existence and support, use paper-integrity.
---

# Paper Review

Write reviews whose claims survive a check against the manuscript. Treat every
opinion as a hypothesis to verify, the user's opinions included. The
manuscript is the evidence, not the notes or a generated draft.

## Choose the mode

- **develop-my-review** (default whenever the user supplies notes, questions,
  or a draft): build the review around the user's surviving judgments.
- **independent-review** (the user asks for a review without supplying
  opinions): follow
  [references/independent-rubric.md](references/independent-rubric.md), then
  apply the verification and delivery sections below.

If the mode is unclear, ask.

## Shared rules

- Work from the exact manuscript version, including available appendices and
  supplements. Follow the user's format, recommendation, confidence, length,
  and language requirements. By default discuss in Chinese and write the
  formal review in English.
- If the paper is inaccessible, say that factual verification cannot be
  completed. Improve language and structure only, and never claim
  verification.
- **Confidentiality.** Never put a manuscript's distinctive title, text, or
  the reviewer's notes into public search queries or external services. For
  external facts, use primary sources and search only with public metadata.
- **Delegate specialist checks; don't improvise them.**
  - Presentation judgments: apply paper-presentation-review's criteria
    read-only.
  - Editorial, cross-reference, and number/unit consistency defects:
    paper-hygiene `audit` with the `consistency` unit.
  - Citation existence, metadata, and support: paper-integrity. Fold the
    results in as review details, not as a separate report.
- **Citation and novelty claims need evidence.** Before the review claims any
  of the following, verify it by paper-integrity's
  [citation rules](../paper-integrity/references/citation-rules.md):
  - a reference is wrong, misattributed, or fabricated;
  - closest work is missing;
  - the idea already appeared elsewhere.
  
  Read the source itself, not a title or snippet. For a whole-bibliography
  check, run paper-integrity at `offline` or `fast`; those levels send only
  reference metadata. If you cannot verify the claim, phrase it as a question
  to the authors.

## develop-my-review

**Scope of the request.** If asked only to verify claims, report findings
without rewriting the review. If asked only to reformat, do not restore
opinions or expand criticism. Always use the user's latest edits, and never
restore a concern they deleted.

**Audit each opinion.** Keep a working record for each one: opinion → paper
location → what the paper actually says → assessment → remaining concern.
Classify it as answered, partially answered, supported, contradicted, or
uncertain. Then:
- remove unsupported criticism and narrow partially answered concerns;
- correct false premises and every conclusion that depends on them;
- turn genuine uncertainty into a clarification request.

Explain important corrections outside the review. Show the full audit only on
request, and do not wait for routine confirmation.

Some things are not weaknesses:
- A question is not a weakness just because it was asked.
- The reviewer's unfamiliarity is not a paper weakness; explain unfamiliar
  terms outside the review.

Before claiming something is absent, inspect the relevant text, figures,
tables, captions, and appendices. A keyword search alone is insufficient.
Keep these apart:
- mentioning a problem vs addressing it;
- describing an evaluation method vs reporting its results;
- some evidence vs sufficient evidence for the conclusion.

**Develop supported judgments.** Build around the user's surviving priorities.
For each major concern, connect the paper's claim, the evidence or the gap,
the implication for the conclusion, and a specific useful clarification or
experiment. Add reasoning rather than a wish list of experiments, and keep
facts, inferences, and suggestions distinct.
- Say "not sufficiently demonstrated" when evidence is inadequate; don't
  claim the method fails.
- Do not invent novelty claims about components.
- Do not call a baseline state of the art without verifying it.
- Do not assume a stronger compatible alternative exists.
- Frame baseline concerns as comparison semantics, coverage, or fairness.
- Do not demand theoretical guarantees from empirical or soft-real-time work
  unless its claims require them.

Preserve a recommendation and confidence the user supplied. Never infer the
reviewer's expertise or default to any particular score. Report important new
concerns outside the user's notes separately, as additional AI observations;
they do not replace the user's priorities.

## Verify the draft independently

Go back to the manuscript and check every factual assertion in the summary,
strengths, weaknesses, and details: positive claims, absences, experiments,
numbers, quotes, and comparisons. The distinctions reviewers most often blur:

- **What property is claimed.** Mechanism vs guarantee: preserving some state
  vs preserving full semantics, soft vs hard guarantees, proactive vs reactive
  behavior, and which failure or load conditions the claim covers.
- **What was measured, at what scale.** The unit being counted; an example
  configuration vs the largest one; an end-to-end experiment vs an isolated
  component study; measurement vs simulation vs analytical count. Do not
  extend one experiment's scale to all of them.
- **What a metric covers.** Its definition, units, normalization, and timing
  boundaries, including metrics reported under another name. Do not call a
  metric missing if it is reported. Criticize a timing convention only when
  the paper supports the criticism.
- **Predictor vs decision.** A model-selection metric vs measured accuracy on
  the real task; prediction error vs decision quality (false and missed
  triggers, lead time, consequences); training and inference cost. Missing
  accuracy results do not mean there is no validation method.
- **Which comparisons exist.** Microbenchmarks of an underlying tool vs
  end-to-end comparisons; alternatives with different semantics; whether a
  suggested alternative applies to the setting at all.
- **Experimental conditions.** Cache and warm-up state, isolation between
  runs, overlap between rounds, and the end-to-end cost of wrong decisions.

Two descriptions that look contradictory may be compatible: a general claim
and a special configuration can both hold. Check before calling it a
contradiction.

Also:
- Inspect the actual images before diagnosing scaling, fonts, legends, or
  readability. Different y-axis ranges across panels are not inherently
  errors.
- Verify locations, symbols, and exact quotations. Keep the original's
  grammatical mistakes and mark omissions with ellipses.
- Recheck absolute terms ("no evaluation", "only", "never", "guarantees",
  "state-of-the-art"). Use "not reported", "not sufficiently established", or
  "unclear" where accurate.
- Revise dependent conclusions whenever a premise fails.

## Deliver the review

Follow the user's latest template. Otherwise use this default:
- a standalone bold recommendation, only if supplied or requested;
- **Paper summary**: problem, approach, and evaluation, stated neutrally in
  about three or four sentences;
- **Strong points**: at most three, each one or two sentences stating a
  conclusion;
- **Weak**: at most three major weaknesses, same form;
- **Details**: evidence, locations, reasoning, and specific suggestions,
  ordered to match the weaknesses where possible, with minor figure, wording,
  and grammar issues last.

Use about two to four sentences for a substantive detail and one or two for a
minor one. Quote the original sentence for any wording criticism and offer a
replacement when useful. Write professional, direct, measured English,
normally 350-600 words, and never pad to a quota. Include confidence or rating
labels only when requested, and preserve a requested format such as
"2. Weak Reject / 3. Knowledgeable".

**Google Docs copyability.**
- Put the complete review in one copyable block; audit explanations and file
  citations go outside it.
- Inside the block, use bold paragraph labels, ordinary paragraphs, and
  single-level numbered lists that restart at 1 in each section, with blank
  lines after labels and between long items.
- Inside the block, avoid nested lists, tables, code blocks, tabs, manual line
  wrapping, HTML entities, tool citation markup, and internal audit labels.
- When revising, return the complete updated review.
- Never create or publish a document, or submit anything to a review system.

**Done when:**
- the user's valid opinions remain, and answered questions are removed or
  narrowed;
- the strength of each claim matches its evidence;
- quotations and locations are correct;
- conclusions and detailed reasoning sit in their own sections;
- the result copies cleanly;
- the review never claims complete verification when a needed source was
  inaccessible.
