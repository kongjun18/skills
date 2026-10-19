# Presentation Figure Workflow

Use this workflow to decide whether a manuscript needs a figure, where the
figure belongs, what it must show, and how to validate it. A figure is a
reader aid for a supported argument, not decoration or a way to introduce an
unstated claim. The ordinary `figures` mode is source-first: it plans the
reader question, source mapping, placement, and visual encoding without
opening or compiling a PDF. Rendered-page inspection belongs to the explicit
`visual-qa` stage.

## Decide whether a figure is needed

Audit the story spine and argument inventory for concepts or relationships that
readers must carry across paragraphs or sections. A figure is usually useful
when at least one of these conditions holds:

- a core concept is reused across several later arguments and a compact visual
  model would prevent repeated prose definitions;
- the explanation depends on spatial, temporal, hierarchical, stateful, or
  many-to-many relationships;
- the motivation requires readers to mentally simulate a workflow, resource
  movement, bottleneck, or before-and-after situation;
- a system mechanism contains multiple entities and handoffs that are hard to
  track in adjacent sentences;
- a measured result has several dimensions whose comparison is clearer as a
  plot than as prose or a table.

A figure is usually unnecessary when one sentence or an existing table gives a
complete local explanation, or when the proposed visual would repeat another
figure without adding a distinct reader question. If the required relationship
is unsupported in the manuscript, mark the figure as blocked instead of using a
diagram to imply it.

Classify each candidate as `required`, `beneficial`, `unnecessary`, or
`blocked`. Treat `required` as a presentation finding only when prose and
existing evidence cannot make a necessary relationship understandable. Treat a
merely helpful visual as a suggestion unless the user requests figure
generation.

## Place the figure in the story

Choose the first placement where the reader needs the visual model, usually
after the motivating observation and before the paragraph that reasons over
multiple entities or steps. The surrounding prose must state the reader
question and introduce the figure with an explicit source clause such as
`Figure X shows ...`. The paragraph after the figure should use the visual to
advance the argument rather than repeat its caption.

When the figure explains a core design choice, place its first source clause
in the same paragraph as the first core claim about that choice, unless the
figure is a paper-level overview. Use the canonical design term in the source
clause and keep the following benefit, cost, or relationship aligned with the
figure's reader question.

Typical roles are:

- **Motivation:** explain a workload shape, core concept, resource movement,
  bottleneck, or causal chain that supports the opportunity;
- **Design:** explain architecture, data layout, request flow, state
  transitions, or component responsibilities;
- **Evaluation:** show measured comparisons, distributions, tradeoffs,
  breakdowns, or sensitivity that answer a stated evaluation question.

Do not place a figure only because the manuscript has a free page area. Keep
one figure focused on one reader question. Split unrelated questions into
separate figures or use a table when that is clearer.

## Write a figure brief before drawing

For every selected figure, record:

1. the reader question and the claim or relationship it supports;
2. the first paragraph that introduces it and the later paragraphs that reuse
   it;
3. the figure role and type, such as concept model, workflow, architecture,
   state transition, evidence plot, or breakdown;
4. the entities, relationships, ordering, and conditions that must appear;
5. the visual encoding for each relation, including arrows, grouping, color,
   line style, position, or panel sequence;
6. the takeaway that the caption and surrounding prose may state;
7. the source inputs, data mapping, or author decision required;
8. the output format, target paper size, and final-size readability checks.

Use the paper's established terminology and ordering. An arrow, label, color,
or spatial arrangement must correspond to a supported relationship. Do not add
an arrow merely to make a diagram look connected.

## Draw and validate

For conceptual figures, choose the simplest geometry that matches the relation:
flow for ordered processing, a timeline for temporal behavior, nested groups
for hierarchy, and explicit state nodes for transitions. Use a paper-ready
vector source such as TikZ or SVG when possible. Keep labels concrete, remove
implementation details that do not answer the figure's question, and preserve
the same names used in the text. Mermaid or an inline sketch can be used to
discuss alternatives, but is not a final paper artifact unless the requested
format supports it.

For quantitative figures, use measured data only. Delegate systems plots to
`systems-paper-plotting` when an evaluation plan and experiment data exist, or
use `scientific-figure-making` for publication-ready Matplotlib figures. Keep
normalization, baselines, statistical units, failures, component order, and
caption claims traceable to the data. Do not create a plot to fill a planned
slot when its input or semantics are missing.

When final figure generation or `visual-qa` is explicitly requested, check the
figure at final physical size and in grayscale when relevant. Verify labels,
units, legend, panel order, source mapping, caption, first mention, and whether
the figure reduces reader effort rather than duplicating nearby prose. A
rendered-figure check can pass only when the final text, caption, and artifact
agree. Without that explicit request, record the source-level figure brief and
defer physical-size and page-layout checks instead of compiling a PDF.
