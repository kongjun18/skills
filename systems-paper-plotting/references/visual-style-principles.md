# Visual Style Principles

The house style for every publication figure rendered for a paper, in any field. Systems evidence rules are in [figure-family-rules.md](figure-family-rules.md); this file covers how figures look.

## Export

- PDF for the paper, plus a 300 DPI PNG for quick review; SVG only for a non-LaTeX consumer.
- Embed TrueType (Type 42) fonts, never Type 3: set `rcParams["pdf.fonttype"] = 42` and `rcParams["ps.fonttype"] = 42` (Matplotlib defaults to Type 3, which publisher PDF checks flag). Verify with `pdffonts <file>.pdf`.
- Use a non-interactive backend (`matplotlib.use("Agg")`) in scripts.

## Size and layout at placed size

- Set `figsize` to the width at which LaTeX places the figure (`\columnwidth`, `\textwidth`, or a stated fraction), so the scale is 1.00 and the set font size is the printed size. Resolve relative widths such as `0.48\textwidth` to inches.
- Do not save with `bbox_inches="tight"`: it crops the canvas to its ink, so the width and the LaTeX scale change from render to render. If ink touches the canvas edge, widen the margin.
- For multi-panel figures, compute every axes rectangle in inches and place it with `fig.add_axes`: fixed left, right, and bottom margins, a fixed gap between panels, and one band for a shared legend. A row, a column, or a grid then keeps equal panel sizes, and tick labels never collide with the next panel.
- Share identical axis labels across panels instead of repeating them.

## Text

- Sans-serif fonts (for example Arial, Helvetica, or DejaVu Sans as fallback), 7–9 pt at print size, close to the caption size; nothing below 7 pt. Effective size = set size × print width / figsize width.
- Keep in-figure titles short or absent; the caption carries the title.
- Label every quantitative axis with metric and unit, e.g. `Throughput (Mops/s)`. Rescale values into readable units (`Mops/s`, `GB`, `ms`) instead of letting Matplotlib add offset or scientific-notation text in the axis corner.

## Axes and scales

- Remove top and right spines; keep only light grid lines that help value reading.
- Bars start at zero on linear axes. Never draw bars on a log axis.
- Log axes for quantities spanning orders of magnitude; log₂ for ratios around 1.0 and for power-of-two scaling axes.

## Color and encoding

- Baseline methods: neutral gray. The proposed method: one primary accent color. Other methods: restrained, colorblind-safe secondary colors (for example from the Okabe–Ito palette). Use one accent for the key result only.
- Encode important distinctions with markers, line styles, or hatches in addition to color, and confirm on a grayscale render, not by reasoning.
- Keep method order and the method-to-color/marker/hatch mapping identical across every figure of the paper: define them once in a shared style module that every plot script imports.
- Borderless legends; label lines directly when there are only a few.

## Annotations

- At print size, check every text annotation, guide-line label, and marker against every curve.
- Put a guide-line label where no curve passes (often at the top of the line), and label it once, not once per panel. A label that must sit over data gets a white background box.

## Prohibited

3D effects, gradients, drop shadows, decorative icons, texture backgrounds, dual y-axes, bars on log axes, arbitrary axis truncation, and Type 3 fonts.

## Final-size review

Review every figure at its final physical width. A plot that is readable only when zoomed is not paper-ready.
