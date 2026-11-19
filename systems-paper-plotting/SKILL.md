---
name: systems-paper-plotting
description: Render publication-quality figures for papers and own their styling. Use for any paper figure made from data in Matplotlib (any field) — house style, print-size layout, fonts, export — and for systems evidence figures from an evaluation_plan.yaml and local experiment data — end-to-end comparisons, normalized speedups, performance breakdowns, load-latency curves, CDF/CCDF tails, scalability, ablation, sensitivity, resource time series, tradeoff scatter, heatmaps, with combined and overview outputs, captions, and audits. Also use to audit figures for misleading normalization, statistics, axes, or layout, and to iteratively polish rendered figures with a reviewer subagent ("refine figures", "review and fix figures", "polish figure X"). For deciding which experiments and figures a paper needs, use systems-evaluation-planner; for whether a manuscript needs a figure and where it goes, use paper-presentation-review; for interactive dashboards or web charts, not this skill.
---

# Systems Paper Plotting

Turn data into paper-ready figures whose every plotted number traces to input data and whose visual choices preserve the evidence semantics. This skill owns the house style for all paper figures; the systems evidence rules apply whenever a figure carries a systems performance claim.

This is a guidance skill: it ships no renderer. You write the plotting code (Matplotlib by default), so every transform from raw data to plotted number is inspectable.

## Inputs

- For systems evidence figures: an executable `evaluation_plan.yaml` from `systems-evaluation-planner`, or equivalent figure specs, following the [data contract](references/data-contract.md). If the plan is not executable (blocking questions remain), resolve them or hand back to the planner before plotting.
- The raw data root; metric units, directions, baselines, repetitions, and failure semantics.
- Target placement: main paper, appendix, presentation. For a styled figure without a plan, ask only for what changes the figure: placed width, data source, and the claim it must support.

## Non-negotiable rules

1. **No invented values.** Never fabricate, interpolate, or zero-fill; zero only when zero was measured.
2. **Absolute before normalized.** Normalized figures are separate, name their baseline, and draw a 1.0× reference line.
3. **The statistical unit is explicit.** Independent runs are the default; request samples do not become runs.
4. **Failures stay visible** as gaps, markers, warnings, or separate failure evidence.
5. **Stacked breakdowns add up**: only mutually exclusive, additive components.
6. **Multi-facet figures produce the full output scope** (standalone, combined paper, combined overview).
7. **Readable at final size**: figsize equals placed width; no text below 7 pt at print size.
8. **Captions are reproducible**: every quantitative caption claim recomputes from processed data.
9. **No misleading decoration**: no 3D, gradients, dual y-axes, truncated bars, bars on log axes, or Type 3 fonts.

## Workflow

1. **Validate the plan.** Status executable, blocking questions empty, inputs exist, and each figure has data, columns, metric, baseline, and output scope ([data contract](references/data-contract.md)).
2. **Inspect data semantics.** Units, directions, repetition and failure columns, and whether raw samples exist for distribution plots.
3. **Choose the form from the evidence family.** Read the matching sections of [figure-family-rules.md](references/figure-family-rules.md), and its Statistics and Anti-Patterns sections for every figure. Do not force every result into bars.
4. **Style once.** Apply [visual-style-principles.md](references/visual-style-principles.md) through one shared style module (method order, colors, markers, hatches, component order) imported by every plot script.
5. **Render the output scope.** Standalone per facet, combined-paper parts, and the complete overview, plus presentation variants when requested, in the output layout of the [data contract](references/data-contract.md#output-layout).
6. **Write processed data, caption drafts, and audits** per [captions-and-audits.md](references/captions-and-audits.md). Read raw data directly, filter to successful rows, compute center and error explicitly, and save the table each figure is drawn from.
7. **Review at final size**, including a grayscale render. For iterative polishing, run the refinement loop below. When a render or refactor behaves unexpectedly, check [pitfalls.md](references/pitfalls.md).

## Figure refinement loop

To polish rendered figures, run review → verify → refine: a fresh reviewer subagent critiques each figure against its paper claim at print size; you verify every finding against the image, script, and data; apply only accepted layout fixes; regenerate; re-check the rules above; repeat. Scope is presentation and layout only. Changes to data, panels, metrics, chart type, figsize, or shared naming go to the human, not into the script.

Read [refinement-loop.md](references/refinement-loop.md) for the phases, verdicts, escalation triggers, and ledger format, and fill [reviewer-brief.md](references/reviewer-brief.md) as the reviewer's prompt.

## Routing

- Which experiments, baselines, and figures a paper needs, and what claims they support: `systems-evaluation-planner`.
- Whether the manuscript needs a figure, where it goes, and conceptual (non-data) figures: `paper-presentation-review` and its figure workflow.
- Figures for slides built from a deck spec: `slide-presentation` places them; produce them here with the `presentation` profile.
- Results recorded in an exploration report: plot from its `data/derived/`, keeping the report's Data Index as the provenance link.

## Done criteria

- No blocking data semantics remain unresolved.
- Every figure is readable at final physical size and distinguishable in grayscale.
- Multi-facet figures include standalone, combined-paper, and complete overview outputs.
- Absolute and normalized views are separate; breakdown additivity passes or the figure type changed.
- Error-bar semantics are explicit in every caption.
- PDF (TrueType fonts) and PNG, processed data, captions, and audits exist for every figure.
- Audits have no errors, and every warning is explained.
