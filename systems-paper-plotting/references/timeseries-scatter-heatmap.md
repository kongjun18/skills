# Time-Series Scatter Heatmap

## Resource Time-Series

- Put wall-clock or experiment time on x with its unit and origin (e.g. seconds since load start).
- State the sampling interval; if you smooth, state the window and keep raw points in the processed data.
- Mark or exclude warm-up explicitly; do not silently crop it.
- Annotate injected events (failures, compaction, GC, reconfiguration, load changes) with vertical lines at their logged timestamps.
- Plot different resources (CPU, memory, I/O) in stacked panels that share the time axis, not on dual y-axes.

## Tradeoff Scatter

- Label both axes with metric, unit, and direction; mark the "better" corner or add a direction arrow.
- Keep method colors and markers identical to the other figures.
- Draw a Pareto frontier only through measured points, never interpolated ones.
- Label points directly when there are few; use a legend otherwise.

## Heatmap

- Use a perceptually uniform sequential colormap (e.g. `viridis`) for magnitudes, or a diverging colormap centered at 1.0 (log-normalized) for ratios. Avoid `jet` and rainbow maps.
- Always include a colorbar with metric and unit.
- Annotate cell values when the grid is small enough to read at print size; pick text color by cell luminance.
- Show missing or failed cells with a distinct pattern or color outside the colormap, not as the minimum value.
