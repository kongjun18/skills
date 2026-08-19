---
name: systems-evaluation-planner
description: Plan evidence chains and figure sets for systems research papers targeting venues such as SIGMOD, FAST, OSDI, SOSP, NSDI, EuroSys, and ASPLOS. Use when Codex needs to turn paper claims, experiment outputs, or author goals into a defensible evaluation_plan.yaml; decide which baselines, workloads, load sweeps, repetitions, robustness checks, and figure families are needed; separate figures that can be generated now from recommended follow-up experiments and unsupported claims; or prepare a handoff to systems-paper-plotting. This skill plans what to plot and why, but does not implement visual styling or rendering.
---

# Systems Evaluation Planner

## Goal

Turn paper claims into an auditable, executable, and traceable evaluation plan. Optimize for evidence responsibility, not for producing the largest possible figure list:

```
paper claim → research question → controls and variables → metric and statistical unit → figure → supported conclusion
```

This skill decides what evidence and figures are needed and why. Leave concrete visual style, layout, export, processed data, captions, and audits to `systems-paper-plotting`.

## Operating Modes

- **Full planning mode:** Use for new or substantially revised systems evaluations.
- **Direct figure mode:** Use when the user already specifies figures and data; ask only the minimum semantic questions needed to make those figures valid.
- **Review mode:** Use to audit an existing evaluation plan, figure list, or paper draft for unsupported claims and missing evidence.

## Non-Negotiable Principles

1. **Resolve blocking semantics first.** If `opening_questions.blocking` is non-empty, the plan status must not be `executable`.
2. **Never invent data.** Do not fabricate benchmarks, infer numbers from prose, or turn failures and missing values into zero.
3. **Separate facts, inferences, and recommendations.** Mark user-confirmed facts, file evidence, safe inferences, and suggested follow-up experiments separately.
4. **Give every figure one clear evidence job.** A figure may support related subclaims, but must not mix unrelated research questions.
5. **Require fair comparisons.** Name the strongest baseline, versions, hardware, data scale, load, tuning budget, and failure semantics.
6. **Prefer absolute values.** Normalized figures may supplement or summarize, but should not be the only evidence when absolute values are available.
7. **Plan single and combined figures together.** Multi-facet figure specs must request standalone plots, paper-ready combined plots, and complete overview plots.
8. **Keep claims within evidence.** “Faster,” “scalable,” “robust,” “low tail latency,” and “lower cost” require different evidence.

## Phase 1: Opening Question Gate

Read all user-provided context before asking questions. Do not ask again for information already present.

Maintain four buckets:

```yaml
opening_questions:
  resolved: []
  inferred: []
  blocking: []
  non_blocking: []
```

For each item record `question`, `answer`, `basis`, and `impact`.

### Prioritize These Semantics

- Core claims and the research question for each candidate figure.
- Proposed system, strongest baseline, and comparison fairness.
- Metric meaning, unit, direction, and statistical unit.
- Whether repetitions are independent runs, random seeds, clients, requests, or samples.
- Offered load versus achieved throughput.
- Timeout, out-of-memory, crash, missing-value, and out-of-range semantics.
- Whether performance-breakdown components are mutually exclusive and additive.
- Whether quantiles come from raw samples or pre-aggregated summaries.
- Facet semantics and the scope of standalone versus combined figures.
- Target output: main paper, appendix, group meeting, talk, or defense.

### Question Strategy

- Ask one coherent batch of blocking questions instead of interrogating column by column.
- Safely infer from data and context only when the basis is explicit.
- Use recommended defaults for visual-only issues and record them as non-blocking.
- In direct figure mode, ask only the semantics needed for the requested figures.

## Phase 2: Read-Only Data Inspection

You may inspect CSV, TSV, JSON, JSONL, and Parquet files. Do not modify raw data.

Check manually or with ordinary local tools for:

- files, rows, columns, types, missing values, duplicate keys, and unique values;
- candidate dimensions, metrics, facets, method columns, and repetition columns;
- mixed units or ambiguous units;
- unbalanced repetitions, missing combinations, and explicit failure records;
- raw samples needed for CDF/CCDF plots;
- independent repetitions needed for confidence intervals.

Do not finalize a semantic role just because a column name “looks like” that role. Put important semantics back into the opening question gate.

Read [Data Semantics And Failure Handling](references/data-semantics-and-failures.md) when classifying metrics, repetitions, failures, or load columns.

## Phase 3: Build The Claim-Evidence Matrix

For each core claim, record:

- research question;
- compared systems or configurations;
- independent variables, controls, and confounders;
- metric, unit, and direction;
- baseline and fairness conditions;
- statistical unit, repetition count, and uncertainty policy;
- best evidence family;
- whether current data is sufficient;
- strongest wording the evidence can support.

Use [Claim To Evidence Mapping](references/claim-to-evidence-mapping.md) to match claim wording to the evidence it requires.

## Phase 4: Select Figure Families

Choose the evidence family first, then suggest a figure form. The plotting skill makes the final low-level visual choice.

| Evidence Question | Preferred Figure Family |
| --- | --- |
| End-to-end comparison across workloads | Absolute grouped bars, dot plots, or small multiples |
| Baseline-normalized comparison | Separate speedup/slowdown plot with a 1.0× reference line |
| Capacity and latency as load increases | Throughput-latency or offered-load-latency curve |
| Tail behavior | p95/p99 curve, empirical CDF, or CCDF |
| Source of overhead | Absolute breakdown; stacked only when components are additive |
| Thread/core/node scaling | Scalability curve, speedup, or scaling efficiency |
| Component contribution | Ablation; change one clear factor at a time |
| Parameter impact | Sensitivity curve or ordered small multiples |
| CPU, memory, I/O over time | Aligned resource time series |
| Performance-cost or performance-quality tradeoff | Scatter/Pareto plot |
| Two-control-variable response surface | Heatmap, optionally with contours or slices |

## Phase 5: Organize The Evaluation Narrative

The default order is not a rigid template, but a strong systems evaluation usually covers:

1. experimental environment and fairness;
2. headline end-to-end results;
3. deeper analysis: latency, breakdown, resource, or mechanism evidence;
4. conclusion synthesis: convert scattered results into checkable conclusions;
5. ablation: isolate component contributions;
6. robustness: scale, skew, failure, burstiness, hardware, or parameter changes.

Classify figures as:

- `main_core`: directly supports a primary contribution;
- `main_explanation`: explains why the result happens or where boundaries are;
- `appendix_completeness`: provides full workload coverage, sensitivity, or repetition checks;
- `presentation`: selects from existing evidence without changing statistical meaning.

## Phase 6: Require Standalone And Combined Outputs

When a figure has multiple facet values, require:

```yaml
output:
  standalone: true
  combined_paper: true
  combined_overview: true
```

Combined figures are small multiples with shared visual encoding, not forced averages across datasets. Allow cross-dataset aggregation only when the statistical meaning is explicit.

If there are too many panels:

- split the paper combined figure into parts with a controlled panel count;
- keep every panel in the complete overview by enlarging the vector canvas or using multipage PDF;
- keep method order, colors, markers, hatches, and component order globally consistent.

## Phase 7: Emit Three Outcome Classes

The plan must clearly separate:

```yaml
direct_figures:
  - current data is sufficient and plotting is allowed
suggested_experiments:
  - recommended follow-up work for a claim; do not invent values
unsupported_claims:
  - current evidence is insufficient; state what is missing and acceptable weaker wording
```

## Plan File

Output exactly one plan named:

```
evaluation_plan.yaml
```

Use English keys throughout.

At minimum include:

- study information and core claims;
- opening question status;
- data files and semantics;
- global baseline, ordering, and statistical policy;
- directly generatable figure specs;
- suggested follow-up experiments;
- unsupported claims;
- standalone and combined output requirements;
- risks, assumptions, and audit focus.

Recommended top-level structure:

```yaml
version: "1.0"
status: draft | blocked | executable
study:
  title: ...
  target_venue: ...
  proposed_system: ...
  core_claims: []
opening_questions:
  resolved: []
  inferred: []
  blocking: []
  non_blocking: []
data:
  root_dir: data
  failure_status_column: status
  success_status_value: ok
global:
  baseline: ...
  highlight_method: ...
  method_order: []
  statistics:
    default_center: mean
    default_error: 95% confidence interval
    confidence_level: 0.95
  output:
    profiles: [paper-double]
    generate_standalone: true
    generate_combined_paper: true
    generate_combined_overview: true
direct_figures: []
suggested_experiments: []
unsupported_claims: []
risks_and_assumptions: []
```

Before handing off, review the plan against the done criteria below. If the plan is not executable, do not send it to the plotting skill as ready-to-render.

## Handoff To Plotting

Provide:

1. `evaluation_plan.yaml`;
2. raw data root directory;
3. data inspection notes;
4. remaining non-blocking assumptions;
5. which figures are for main paper, appendix, and presentation.

Do not pre-decide pixel-level style. You may specify evidence intent such as “separate absolute and normalized values,” “use CCDF for the tail,” or “facet by dataset,” but let the plotting skill choose bars, points, lines, axes, and layout details.

## Done Criteria

Finish only when:

- `opening_questions.blocking` is empty for executable plans;
- every core claim maps to evidence or is listed as unsupported;
- every figure has a research question, data source, metric, baseline, statistical unit, and output scope;
- every multi-facet figure requests standalone and combined outputs;
- no data is invented and failure semantics are explicit;
- the plan passes the quality checklist or clearly states why it is still blocked.
