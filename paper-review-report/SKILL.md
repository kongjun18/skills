---
name: paper-review-report
description: Develop an evidence-grounded English conference review from a reviewer's notes, questions, or draft. Use to audit opinions against the manuscript, verify review claims, refine a review, or format it for Google Docs. For independent automated paper review rather than developing the user's report, use paper-review instead.
---

# Paper Review Report

Help the user develop their review: treat their opinions as judgments and questions to verify, not established facts. Work from the exact manuscript version, including available appendices and supplements, the user's original notes and latest draft, and their format, recommendation, confidence, length and language requirements. Use their latest edits; do not restore deleted concerns. By default discuss in Chinese and write the formal review in English.

If the paper is inaccessible, explain that factual verification cannot be completed; improve language and structure where useful without claiming verification. When asked only to verify claims, report findings without rewriting the review. When asked only to change formatting, do not restore opinions or expand criticism.

## Audit the user's opinions

For each opinion maintain a working record: original opinion → paper location → what it actually says → assessment → remaining concern. Classify it as answered, partially answered, supported, contradicted, or uncertain. Remove unsupported criticism; narrow partially answered concerns; correct false premises and dependent conclusions; turn genuine uncertainty into a clarification request when appropriate. Explain important corrections outside the review. Do not output the full audit unless requested, and continue without waiting for routine confirmation.

Do not turn a question into a weakness merely because it was asked, or treat the reviewer's unfamiliarity as a paper weakness; explain unfamiliar terms outside the review. Inspect relevant text, figures, tables, captions and appendices before claiming absence: a keyword search alone is insufficient. Distinguish mentioning a problem from addressing it, describing an evaluation method from reporting results, and some evidence from sufficient evidence for a conclusion.

## Develop supported judgments

Build around the user's surviving priorities. For each major concern connect the paper's claim, evidence or gap, implication for the conclusion, and a specific useful clarification or experiment. Add reasoning rather than an experiment wish list; distinguish facts, inferences and suggestions. Say “not sufficiently demonstrated” when evidence is inadequate, rather than claiming the method does not work. Do not invent component novelty, call a baseline state of the art without verification, or assume a stronger compatible alternative exists. Explain baseline concerns in terms of comparison semantics, coverage or fairness. Do not demand theoretical guarantees of empirical or soft real-time work unless its claims require them.

Preserve explicitly supplied recommendation and confidence; never infer reviewer expertise or default to an example's Weak Reject. Identify important new concerns outside the user's notes separately as additional AI observations, rather than silently replacing their priorities.

## Independently verify the draft

Return to the manuscript, not the notes or generated draft, as evidence. Check every factual assertion in the summary, strengths, weaknesses and details, including positive claims, absences, experiments, numbers, quotes and comparisons. Check the following distinctions where relevant:

- Runtime state preservation versus semantically stateful services; soft versus hard real-time; proactive prediction versus reactive response; overload versus link or sudden node failure.
- Node versus container counts; examples versus largest configurations; integrated experiments versus isolated protocol studies; measurements versus simulations and theoretical message counts. Do not generalize the scale of one experiment to all experiments.
- Downtime versus total migration time and operation latency; definitions, units, normalization and timing boundaries, including metrics under another name. Do not claim downtime is absent if reported; criticize timing conventions or application-level QoS only when supported.
- RMSE for model selection versus measured future-prediction accuracy; prediction error versus migration-decision success. Check unnecessary and missed triggers, warning time, consequences, CPU and memory overhead, training and inference frequency. Missing accuracy results do not imply no validation method.
- Original CRIU operation microbenchmarks versus end-to-end migration comparisons; restart-based recovery versus state-preserving live migration; existing versus missing comparisons and whether alternatives apply to the setting.
- Cold and warm caches, clearing between runs, overlap across rounds, end-to-end application improvements and consequences of incorrect predictions for caching, I/O or other applications.

Inspect actual images before diagnosing visual scaling, distortion, fonts, legends or readability; different panel y-axis ranges are not inherently errors. Verify locations, mathematical symbols and exact quotations, preserving original grammatical mistakes and using ellipses for omissions. Recheck absolute terms such as “no evaluation,” “only,” “never,” “guarantees,” and “state-of-the-art.” Use “not reported,” “not sufficiently established,” or “unclear” as appropriate. For example, all other nodes can be neighbors in a fully connected network; the descriptions are compatible, though partially connected deployments may raise selection or degree questions. Revise dependent conclusions when a premise fails.

When external facts need verification, follow applicable browsing requirements and prefer primary sources. Do not submit distinctive unpublished manuscript titles, manuscript text or reviewer notes to public search queries.

## Deliver the review

Follow the user's latest explicit template. Otherwise use a standalone bold recommendation only if supplied or requested, then **Paper summary**, **Strong points**, **Weak**, and **Details**. Summarize problem, approach and evaluation neutrally in about three or four sentences. Include at most three strengths and three major weaknesses, using fewer when appropriate; each is one or two sentences stating a conclusion. Put evidence, locations, reasoning and specific suggestions in Details, ordered to correspond to weaknesses when possible, with minor figure, wording and grammar issues last. Elaborate rather than repeat: use roughly two to four sentences for a substantive detail and one or two for a minor issue. Quote the original sentence or an accurate excerpt for wording criticism, offering a replacement when useful.

Write professional, direct, measured English, normally 350–600 words or shorter when appropriate; do not fill a quota. Include confidence or numerical rating labels only when explicitly requested. Preserve a requested format such as “2. Weak Reject / 3. Knowledgeable.”

For Google Docs copyability, put the complete review in one standard copyable writing block when supported, with audit explanations and required file citations outside it. Inside, use bold paragraph labels, ordinary paragraphs, single-level numbered lists restarting at 1 for each section, and blank lines after labels and between long items. Avoid nested lists, tables, code blocks, tabs, manual line wrapping, HTML entities, escaped spaces, tool citation markup and internal audit labels. Use ordinary section, figure and table references. When revising, preserve the writing-block identifier if supported and return the complete updated review. Do not independently create or publish a document or submit to a review system.

Before delivery, check that valid user opinions remain, answered questions are removed or narrowed, claims and their strength match the evidence, quotations and locations are correct, conclusions and detailed reasoning occupy their respective sections, and the result copies cleanly. Never claim complete verification when a necessary source is inaccessible.
