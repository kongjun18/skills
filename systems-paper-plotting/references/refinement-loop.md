# Figure Refinement Loop (review → verify → refine)

Use this loop after figures render, to polish presentation at print size. It is invoked by "refine figures", "review and fix figures", "polish figure X", or a figure/script target.

Roles:
- **Reviewer** — a fresh subagent each round. Sees the figure and its context, writes findings. Never edits files.
- **Main agent (you)** — builds the reviewer's context, decides whether each finding is correct, applies the accepted ones, regenerates the figure, and asks the human about anything you shouldn't decide alone.
- **Human** — decides escalations. Their answers are recorded in the ledger and never re-litigated.

Scope is **presentation/layout only** (overlaps, label/legend placement, axis ranges/ticks, fonts at print size, whitespace, naming/color consistency). Changes to data, panels, metrics, or chart types count as redesign: note them for the human and don't apply them. A layout fix must never break the Non-Negotiable Rules in `SKILL.md`; axis-range changes are the usual way that happens (truncated bars, clipped points, hidden failure markers).

Tool names below are Claude Code's (`Agent`, `AskUserQuestion`). In other harnesses, use the equivalent subagent-spawn and ask-the-user mechanisms.

## Phase 0 — Setup (once per run)

1. **Resolve targets.** For each figure, find: plot script, input data, output PNG/PDF, and `figsize`. Map it to the paper: grep the LaTeX sources (e.g. `main.tex` and its `\input` files) for the figure stem, a similar stem, or the section that discusses it; get the `\includegraphics` width, the caption, and the paragraph(s) that cite it. USENIX and acmart two-column templates: `\columnwidth` ≈ 3.33 in, `\textwidth` ≈ 7.0 in. Resolve relative widths such as `0.48\textwidth` to inches.
   - Output filenames often differ from the ones the LaTeX includes. If the paper location can't be found with confidence, **ask the human** (list candidates). Don't review without paper context, because the reviewer's goal comes from it.
2. **Write the context packet** to `.figreview/<stem>/context.md` (scratch, never committed):
   - *Claim*: the one sentence the figure must convince a reader of, quoted or paraphrased from the paper text. If the text never states it, ask the human.
   - Print width (in) and the scale factor = print width / figsize width. Font sizes at print size are what matter.
   - Caption and citing paragraph (verbatim, short).
   - Series/baseline names and colors used in *other* figures of the same paper (grep the other scripts), so the reviewer can check consistency.
   - Settled decisions from `.figreview/<stem>/ledger.md` (if it exists) and from persistent memory, if the harness has one.
3. **Confirm the goal once** with AskUserQuestion when anything is non-default: targets, the claim you inferred, max rounds (default 3). Skip this if the user already stated all of it.
   - Layout requests such as "merge figures A and B", "move figure C to one column", or "make it a 2 by 2 grid" can be read more than one way. Before acting, restate the result: the number of floats with their labels and captions, the panels and grid of each, and the placed width. When you ask with options, each option must name these consequences. "Combine into one figure" can mean merging two floats or arranging one figure's panels, and guessing wrong costs a full revert.
4. Render the baseline: run the script with the project's own command (Makefile target, virtualenv, etc.). If there is none, use an isolated run that includes every package the script imports, e.g. `uv run --no-project --with matplotlib --with numpy --with pandas python <script>`. View the PNG and snapshot it to `.figreview/<stem>/r0.png`.
5. Run the invariant check below on the baseline render. Report pre-existing violations to the human as out-of-scope content concerns; don't fix them silently.

## Phase 1 — Loop (per figure, round r = 1..max)

### 1. Review — spawn a fresh reviewer
Use `Agent` (general-purpose) with the brief in [Reviewer Brief](reviewer-brief.md), filled with the context packet, the current PNG path, the script path, and the ledger. Use a fresh agent every round. A continued agent tends to defend its earlier findings, and the ledger already carries the history. Figures are independent, so run their reviewers in parallel.

### 2. Verify — adjudicate every finding yourself
Open the PNG and check each finding against the image, the script, and the CSV. Assign exactly one verdict:

| Verdict | When |
|---|---|
| **accept** | You can see the defect yourself, the fix is layout-only, it doesn't conflict with the ledger, and it keeps every invariant below. |
| **reject** | Not visible, factually wrong about the data/script, a matter of taste with no readability gain, re-raises a settled decision, would hurt another element, or would break an invariant (e.g. a `ylim` that no longer starts bars at zero). Record a one-line reason. |
| **escalate** | See the triggers below. |

**Escalation triggers (stop and ask the human):**
- *Redesign*: changes data, panels, metrics, chart type, normalization, or which series are shown.
- *Breaking change*: output filename/path, figure size or aspect ratio (it moves the LaTeX layout), series names/colors/markers shared with other figures, or anything the caption/text refers to ("the red line", "left panel").
- *Missing context*: the correct label, unit, or baseline name isn't recoverable from the script, the data, or the paper.
- *Conflict*: the finding contradicts the caption/text, a prior human decision, or another accepted finding. Also, if the data looks wrong, report it and don't touch it.
- *Oscillation*: a fix would undo an earlier round's accepted fix.
- *Manuscript layout*: float environment or placement, captions, and float spacing lengths (`\textfloatsep`, `\floatsep`, `\intextsep`, caption skip). Templates may forbid spacing changes, and bottom-aligned columns stretch these gaps, so present the trade-off instead of applying it.

Batch every escalation of the round into **one** AskUserQuestion call (≤4 questions, recommended option first, include the concrete before/after). Keep applying the non-blocked accepts while you wait. Pause only if an escalation blocks the rest, e.g. a figsize decision that everything else depends on.

### 3. Refine — apply accepted fixes
- Make minimal edits in the plot script, matching its style. Change only the parameters the finding is about.
- Regenerate immediately, view the PNG, and snapshot it to `.figreview/<stem>/r<r>.png`.
- Check each accepted fix against the new render: is the defect gone, and did nothing regress (new overlaps, clipped text, changed bounding box)? If a fix didn't work, revert it or retry once. Don't claim it's fixed.
- Re-run the invariant check. Revert any fix that introduced a violation, and record it as a reject.

**Invariant check** (check it from the script and data, not only by eye):
- Bars on linear axes start at zero; no bars on log axes.
- Every plotted value lies inside the axis limits: compare data min/max from the input with the final `get_xlim()`/`get_ylim()`.
- Failure, timeout, and OOM markers and gaps are still visible and not covered by legends or annotations.
- Log axes contain only positive values; ratio plots keep the 1.0× reference line.
- Text is at least 7 pt at print size (set size × scale).
- Every series stays distinguishable in a grayscale render.
- The PDF embeds its fonts with none of type 3 (`pdffonts <file>.pdf`).

### 4. Record — append to `.figreview/<stem>/ledger.md`
```
## Round r
- F3 accept  — legend overlapped series B at x∈[8,16] → moved legend to upper left (verified r2.png)
- F4 reject  — "fonts too small": 7.9pt at print, already ≥ caption size
- F5 human   — rename "Ours" → "AlpsANN"? → human: yes, in all figures
```
The ledger is the settled-decision list for the next reviewer. If the human gives a rule that should last beyond this run (e.g. "never change figsize"), offer to save it to memory.

### 5. Stop condition
Stop the figure when any of these holds:
- the round produced no accepted major/minor finding (nits alone don't justify another round);
- r = max rounds;
- oscillation was detected.

Otherwise go to round r+1.

## Phase 2 — Hand back
- Report per figure: rounds run, fixes applied (verified against the render), invariant-check result, rejected findings worth knowing about, open human questions, and out-of-scope content concerns (one line each).
- Show the final PNG paths. Offer to commit the script + regenerated outputs (stage explicitly; never `.figreview/`).
- Delete `.figreview/` only if the user says so. It holds the review history.
