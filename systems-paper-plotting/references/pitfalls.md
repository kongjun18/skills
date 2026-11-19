# Pitfalls

Failures seen in practice that the general rules do not make obvious. Read when a render or a script change behaves unexpectedly.

- **Refactors change output silently.** After refactoring a plot script (shared style module, new helper), render the old configuration first and confirm it matches the previous output pixel for pixel before making any visible change.
- **Caption numbers drift from the figure.** Print every number the caption or paper text quotes from the processed data, and compare before handing off.
- **Explicit `markevery` indices past the end of a series** raise an error only at save time; clamp them to each series' length.
- **Axis-limit fixes break evidence rules.** Tightening `ylim` to remove whitespace is the usual way bars stop starting at zero, points get clipped, or failure markers disappear; re-check the data range against `get_xlim()`/`get_ylim()` after every limit change.
- **Ambiguous layout requests.** "Merge figures A and B" or "make it a 2 by 2 grid" can mean merging two floats or rearranging one figure's panels. Before acting, restate the result: the number of floats with their labels and captions, the panels and grid of each, and the placed width.
- **Missing environments.** When the project has no plotting command, run scripts in an isolated environment that includes every imported package, e.g. `uv run --no-project --with matplotlib --with numpy --with pandas python <script>`.
