# Anti-Patterns

Avoid these unless the user explicitly asks for a diagnostic sketch and the figure is not used as evidence:

- CDF from only p50/p95/p99.
- Normalized-only performance result with no absolute values.
- Truncated bar axis to exaggerate small differences.
- Dual y-axis.
- Bars on a log axis.
- Speedup on a linear axis that makes 0.5× look half as far from 1.0 as 2×.
- Type 3 fonts in PDF output.
- Axis labels without units, or Matplotlib offset text (`1e6`) in place of a unit.
- Missing or failed runs silently treated as zero.
- Percent-only breakdown with no absolute total.
- Reordered methods or components across panels.
- Connecting unordered categories with lines.
- Error bars over requests presented as independent-run uncertainty.
- Combined figure that averages incompatible datasets.