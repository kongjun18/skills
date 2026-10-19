---
name: paper-review
description: Organize staged reviews of systems and database research papers for venues such as OSDI, FAST, EuroSys, SIGMOD, and VLDB. Currently implements editorial accuracy, consistency, and a quick citation check (built on the paper-integrity toolbox; full citation audits and the submission gate belong to paper-integrity) with a Markdown issue tracker; presentation quality, contribution, technical soundness, evaluation, and overall assessment remain framework-only stages. Use for paper-review planning or the implemented checks, without editing the manuscript.
---

# Paper Review

Organize a paper review around the questions a systems or database program committee must answer. This is a review framework with one implemented review stage, not an implemented end-to-end scientific reviewer. Keep editorial accuracy separate from presentation quality and scientific merit.

Do not modify the manuscript, bibliography, figures, code, or data. Use one Markdown review report and issue tracker, with stage labels, rather than separate per-stage review files. Preserve the authors' technical meaning in suggested corrections.

## Pipeline and implementation status

The following order is a working review sequence, not an official venue workflow or a requirement to finish every stage before revisiting an earlier one. Intake and reporting support the implemented checks; stages 2–7 define future scope and outputs only.

| Stage | Main question and scope | Expected output | Availability |
| --- | --- | --- | --- |
| 0. Intake and review context | What materials, revision, venue/year, track, paper type, and review scope are available? | Artifact inventory, coverage limits, selected stages, applicable venue guidance | Implemented below |
| 1. Editorial accuracy and citation integrity | Are the text, numbers, labels, references, and attributed statements accurate and internally consistent? | Located defects, evidence, local corrections, unresolved verification items | Implemented below; default review scope |
| 2. Presentation quality | Is the paper easy to follow? Does it explain the problem, challenges, key idea, and results in an effective order, with smooth transitions, useful examples, and appropriate detail? | Reader obstacles and prioritized changes to narrative, organization, and explanatory figures | Framework only |
| 3. Contribution, significance, and positioning | Is the problem important for the intended audience? What advances beyond the closest work, and how substantial and useful is that advance for this paper type? | Contribution map, closest-work comparison, significance and venue-fit assessment | Framework only |
| 4. Technical soundness and research logic | Do the assumptions, mechanisms, algorithms, proofs, and reasoning support the claims? Are failure cases and applicability boundaries handled? | Claim-to-argument map, correctness concerns, assumptions, and limitations | Framework only |
| 5. Evaluation and evidence | Do experiments or other appropriate evidence test the claims with fair comparisons and credible measurements? Are workload selection, scale, ablations, uncertainty, and generalization adequate where relevant? | Claim-to-evidence map, strengths, threats to validity, and prioritized evidence gaps | Framework only |
| 6. Reproducibility and responsible research | Can the work be understood and independently checked from the documented methods and available artifacts? Are deployment constraints, ethical considerations, and data provenance addressed where relevant? | Reproducibility gaps, applicable research-practice concerns, and verification limits | Framework only |
| 7. Overall review and revision plan | What are the decisive strengths and weaknesses, and which revisions matter most? | Paper summary, strengths, ranked weaknesses, author questions, reviewer confidence, and revision priorities; recommendation only when requested and supported by completed stages | Framework only |

Default to stages 0 and 1 plus the shared report. If the user requests a full review, expose the framework-only stages as unimplemented; do not silently execute an improvised rubric or imply that they passed. A stage-specific request narrows the work to that stage's available checks. Incidental observations belonging to future stages may be recorded as deferred questions, not assessed findings. Completing stage 1 does not establish scientific soundness or conference readiness.

For each requested stage, record a run status separately from implementation availability: `Not run`, `In progress`, `Complete`, `Partial`, or `Deferred`. State why a stage is partial or deferred. A completed review may still contain unresolved issues; completion records coverage, not paper quality.

### Venue and paper-type calibration

Use the target venue's official instructions for the specified year, track, and submission stage. Do not assume a universal scoring scale, page limit, rebuttal process, or artifact requirement. When the target is unspecified, use the shared review dimensions above and mark venue-specific checks as unassessed.

Calibrate future scientific review to the contribution type: a new system, algorithm, measurement study, benchmark, deployment/experience report, reproducibility study, or vision paper need not provide the same kind of novelty or evidence. Domain-specific concerns such as crash recovery, consistency, query semantics, or storage endurance apply only when relevant to the paper's claims.

The stage decomposition is this skill's synthesis, informed by the research calls for [OSDI 2026](https://www.usenix.org/conference/osdi26/call-for-papers), [FAST 2026](https://www.usenix.org/conference/fast26/call-for-papers), [EuroSys 2026](https://2026.eurosys.org/cfp.html), [SIGMOD 2026](https://2026.sigmod.org/calls_papers_sigmod_research.shtml), and [PVLDB Volume 20](https://www.vldb.org/2027/call-for-research-track.html). These are reference examples; retrieve the applicable edition when reviewing a specific submission.

## Stage 0: Intake and coverage

Start from user-provided files, links, and project instructions. Discover the actual manuscript, included content, references, rendered document, figures, and supporting artifacts from those inputs and their links. Do not assume filenames, directory names, document format, build system, or figure-production layout. A PDF-only or excerpt-only review is valid with explicit coverage limits; source files and experimental data are optional inputs, not prerequisites for starting.

Identify the revision and requested scope. Read the complete available manuscript before finalizing cross-section findings; for an excerpt, restrict conclusions to that excerpt. Inspect rendered pages for visual defects, since source text alone cannot establish legibility or layout. If compilation is needed and available, follow discovered build instructions, place generated files in scratch space, and preserve the source tree. Determine whether rendered and source artifacts correspond; record uncertainty when this cannot be established.

Record unavailable inputs and their consequences. Missing data limits numerical verification; missing cited full texts may limit citation-support checks; missing rendered pages limits visual verification. Continue supported checks without describing unperformed checks as passed.

## Stage 1: Editorial accuracy and citation integrity

Find concrete, evidence-backed defects. This stage does not judge whether the overall presentation is compelling, smooth, or well organized. Citation-to-claim fidelity is an explicit part of this stage: verify that an attribution represents the cited work, without deciding whether the paper's own scientific argument is valid.

### Scope boundary

| In scope for stage 1 | Deferred to later stages |
| --- | --- |
| Undefined metric, symbol, acronym, or technical term | Whether the metric adequately tests the claim |
| Conflicting numbers for the same experiment | Whether the experiment or baseline is fair |
| Missing explanation of error bars or aggregation | Whether the statistical method is appropriate |
| Ambiguous description of a component or operation | Whether the design or algorithm is correct |
| A summary says “all workloads,” but the corresponding evaluation explicitly says “three of five” | Whether the evidence justifies generalizing to other workloads |
| Unrelated citation, misreported cited result, nonexistent reference, or wrong author attribution | Whether related work is comprehensive or novelty is established |
| Illegible figure labels or an incorrect panel reference | Whether the figure explains the key idea effectively |
| An undefined term or a sentence with an ambiguous referent | Whether the narrative is smooth, engaging, or easy to follow overall |

Within stage 1, do not recommend new experiments, different baselines, design changes, or a new argument. Do not assess proofs or causal explanations. When resolving an ambiguity requires a research judgment, record the wording problem and request author clarification without inventing the answer. Do not turn stylistic preferences into defects.

### Editorial checklist

Apply relevant checks across the abstract, introduction, design, evaluation, conclusion, appendices, and captions. These are review categories, not quotas for findings.

| Category | Checks |
| --- | --- |
| Grammar and mechanics | Agreement, articles, tense, singular/plural, punctuation, spelling, malformed sentences, and incorrect word choice. Follow the paper's established English variant. |
| Clarity and precision | Ambiguous pronouns, unclear actor or object, misplaced modifiers, overloaded sentences, vague comparisons such as “better,” and unclear referents such as “this overhead.” Offer a rewrite only when meaning is recoverable. |
| Terminology and naming | Consistent system, component, baseline, workload, and configuration names; distinguish terms the paper uses differently, such as a request versus an I/O operation. Expand nonstandard acronyms at first use and define unfamiliar terms before relying on them. If the paper has a [glossary](../paper-presentation-review/references/glossary.md), report every banned term and every use that breaks a Use or Interchangeable rule. |
| Notation and mathematical presentation | Defined symbols, consistent subscripts and typography, accidental symbol reuse, readable equations, and agreement between notation and prose. Check transcription and presentation, not derivations or algorithm correctness. |
| Numerical consistency | Match reported values, ranges, rankings, workload counts, and stated result scope across prose, tables, figures, and available data. Compare only matching experiments and configurations; account for stated rounding. |
| Units and comparisons | Explicit units and denominators; distinguish bits/bytes, GB/GiB, per-node/aggregate, absolute/relative changes, and percent/percentage points. Identify the reference baseline, ratio direction, and normalization. Flag ambiguous phrases such as “2× faster.” |
| Evaluation reporting clarity | Ensure readers can identify the workload, configuration, measurement scope, and aggregation for a reported result, locally or through a clear reference. Explain mean/median/percentile, throughput versus offered load, error-bar meaning, and repetition count where needed to interpret the displayed statistic. Report missing descriptions without demanding additional experiments. |
| Figures and tables | Readable labels at final size, units, legends, panel identifiers, scales and axis breaks, explicit normalization, explained abbreviations and error bars, consistent series names, distinguishable marks, adequate contrast, unclipped content, and sensible numerical precision. Captions should identify what is shown and the relevant conditions without requiring readers to guess. Check figure descriptions when applicable. |
| Diagrams and pseudocode | Labeled components, arrows, interfaces, inputs, outputs, and relevant state; defined line references and symbols; names consistent with the text. Check whether the representation is understandable, without judging the mechanism's correctness. |
| Navigation and cross-references | Correct section/figure/table/equation/appendix references, matching panel letters, references to absent material, and accidental duplicate text. Leave section order, transitions, and overall reading flow to stage 2. |
| Citations and bibliography | Citation-to-claim mismatch, nonexistent or unverifiable works, incorrect authors or other metadata, internal attribution conflicts, unresolved keys, duplicate entries, and formatting defects. Follow the quick citation check below; leave literature coverage and novelty judgments to stage 3. |
| Typography and rendering | Missing glyphs, broken math, visible placeholders or editing notes, overflowing lines, clipped tables, low-resolution images, bad float placement, detached captions, and unintended spacing. Treat build warnings as leads to inspect, not automatic findings. |
| Venue and submission presentation | If the target venue and stage are known, check the applicable template, page limits, font/margin rules, required visible metadata, and anonymization presentation. Use supplied or current official instructions; do not import another venue's rules or apply camera-ready requirements to a review submission. |

### Quick citation check

Stage 1 runs a small citation check to catch citation errors. The full audit, the S0/S1/S2 tiers, and the submission gate belong to [paper-integrity](../paper-integrity/SKILL.md). This check reuses its toolbox scripts and follows its [citation rules](../paper-integrity/references/citation-rules.md).

1. Run paper-integrity at the `offline` level (`scripts/run.py --level offline`). When the user accepts sending public reference metadata to Crossref, OpenAlex, and arXiv, run `--level fast` instead, then `run.py --finish` without launching its triage agents. Treat suspected reference findings as `Needs verification`. Put the run directory outside the manuscript tree.
2. For each citation use in the reviewed scope, listed in the run's `ledger.md`, read the sentence and check that the cited work plausibly matches the clause, using the record and abstract in `identity.json`. Read the cited source itself only for high-risk uses: specific numbers, named-author or named-system attributions, claims about "all" or "most" systems, and descriptions of competing work.
3. Record citation defects in this skill's tracker with stage 1 and category Citations. Put the paper-integrity tier in the evidence, and map it to this tracker's severity: S0 to `Major`, S1 to `Major` or `Minor`, S2 to `Polish`. Never call a reference fabricated without affirmative evidence, and never invent a replacement citation.
4. This check does not certify the citations. When a suspected S0 appears, or the user asks about submission readiness, recommend a paper-integrity `full` run and name the unchecked classes (claim support across all uses, uncited borrowed work, copied text) in the coverage limits.

### Resolving numerical and terminology inconsistencies

For every suspected numerical conflict, first match the workload, hardware, configuration, baseline, metric, units, aggregation, and version. Different settings may explain different values.

Trace the result where artifacts permit: source data → selection and aggregation in plotting code → plotted value or table cell → evaluation prose → summaries elsewhere in the paper. Recompute simple arithmetic and conversions when useful. For example, latency changing from 10 ms to 5 ms is a 50% reduction and a 2× speedup under a baseline/new latency ratio; it is not a 100% latency reduction.

Preserve the original preference for evaluation results when reconciling evaluation with other sections, but verify the evaluation against its underlying artifacts before recommending a replacement. Evaluation prose, raw data, and generated figures can each be stale or refer to different runs. If provenance is missing or artifacts disagree, show the competing values and mark the correction as needing verification. Never silently select a value or infer exact numbers from an imprecise plot.

For nonnumeric inconsistencies, identify both locations and the conflicting text. Preserve technical qualifiers such as “up to,” “on average,” and workload restrictions in suggested edits.

## Shared report and issue tracker

Reuse the user's report path or an existing review tracker and follow repository document-routing rules. If no destination is established, present the Markdown report in the response rather than assuming a project path. Do not create a separate report for each stage. Record the reviewed revision or artifact identifiers, inputs, venue context, requested stages, run statuses, and checks that could not be completed.

Maintain a table with these columns:

| ID | Stage | Severity | Category | Location | Evidence and issue | Suggested correction | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |

- **Location:** source path and line or a stable section/figure/table identifier; include PDF page when useful. For inconsistencies, cite both sides and the relevant data/script location.
- **Evidence and issue:** quote the smallest useful passage or give the conflicting values and explain the reader-visible problem. Distinguish verified defects from uncertainties.
- **Suggested correction:** give replacement wording or a concrete local action. Use “author clarification needed” when intent is uncertain; do not manufacture definitions or results.
- **Severity:** For stage 1, `Major` changes the apparent result, materially misattributes a claim, or blocks interpretation; `Minor` causes local ambiguity or a noticeable reading problem; `Polish` is a clear mechanical or visual defect with little effect on meaning. These are editorial priorities, not acceptance recommendations. Future stages need their own assessment criteria; do not mechanically turn counts of editorial defects into scientific scores.
- **Status:** `Open`, `Needs verification`, `Resolved`, or `Dismissed`. Retain stable IDs across reviews; resolve only after checking the updated artifact and retain a brief rationale for dismissals. Reopen recurring defects.

Sort active findings by severity. Group repeated instances of one defect while listing affected locations; separate issues that need different fixes. Carry forward existing statuses and avoid duplicate findings. Keep deferred questions for future stages separate from verified stage-1 findings. End with a short count by severity and status plus outstanding verification limits. If no issues are found, state the coverage and limits rather than claiming the paper is error-free. Do not produce an overall acceptance recommendation from stage 1 alone.
