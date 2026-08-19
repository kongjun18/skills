# Statistics And Error

## Statistical Unit

Independent runs are the default unit for uncertainty. Request-level samples, time windows, or operations are not independent runs unless the experiment design says so.

## Center And Error

- Roughly symmetric repeated-run data: mean with 95% confidence interval.
- Skewed latency: median, quantiles, CDF, or CCDF.
- Small samples: Student-t confidence interval.
- Too few runs: show individual run points.

## Caption Requirements

Captions must state what error bars mean: standard deviation, standard error, confidence interval, quantile range, or something else.

## Common Mistakes

- Treating every request as a repetition to shrink error bars.
- Reporting confidence intervals without enough independent runs.
- Mixing standard deviation and confidence interval language.
- Applying arithmetic means to normalized ratios when geometric means are required.