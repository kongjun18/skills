# Visual Style Principles

## Paper Defaults

- Use PDF for camera-ready figures; add SVG only for non-LaTeX consumers.
- Also export PNG for fast review.
- Embed Type 42 (TrueType) fonts, never Type 3. In Matplotlib set `rcParams["pdf.fonttype"] = 42` and `rcParams["ps.fonttype"] = 42`; verify with `pdffonts`.
- Use readable sans-serif fonts at 7–9 pt at print size, close to the caption size.
- Remove top and right spines.
- Use light grid lines only where they improve value reading.
- Avoid chart titles that duplicate captions.

## Axes

- Label every quantitative axis with metric and unit, e.g. `Throughput (Mops/s)`.
- Rescale values into readable units rather than letting Matplotlib add offset or scientific-notation text in the axis corner.
- Use log axes for quantities spanning orders of magnitude; use log₂ for ratios around 1.0 and power-of-two scaling axes.
- Never draw bars on a log axis: bar length has no meaning there. Use dots or lines.

## Encoding

- Baseline: neutral gray.
- Proposed system: one primary accent color.
- Other methods: restrained secondary colors.
- Add markers, line styles, or hatches so the figure survives grayscale printing and color-vision variation. Check this on a grayscale render, not by reasoning.
- Keep method order and visual mappings consistent across all figures.

## Prohibited Defaults

Avoid 3D effects, gradients, drop shadows, decorative icons, texture backgrounds, dual y-axes, bars on log axes, Type 3 fonts, and arbitrary axis truncation.

## Layout At Placed Size

- Set `figsize` to the width at which LaTeX places the figure (`\columnwidth`, `\textwidth`, or a fraction of it), so the scale is 1.00 and the set font size is the printed size.
- Do not save with `bbox_inches="tight"`: it crops the canvas to its ink, so the width and the LaTeX scale change from render to render.
- For multi-panel figures, compute every axes rectangle in inches and place it with `fig.add_axes`. Fix the left, right, and bottom margins, the gap between panels, and a top band for one shared legend or key. Then a row, a column, or a 2 by 2 grid keeps equal panel sizes, and tick labels never collide with the next panel.
- Share axis labels across panels when they are identical, rather than repeating them on every panel.
- If ink touches the canvas edge, widen the margin; do not crop.

## Annotations

- At print size, check every text annotation, guide-line label, and marker against every curve.
- Put a guide-line label where no curve passes, often at the top of the line. Give a label that must sit over data a white background box.
- Label a guide line once, not once per panel.
- Clamp explicit `markevery` indices to the length of each series; an index past the end raises an error at save time.

## Final-Size Review

Review paper figures at final physical width. A plot that is readable only when zoomed is not paper-ready.