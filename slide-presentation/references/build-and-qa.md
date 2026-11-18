# Build, render and QA

## Requirements

- `uv` (runs the scripts with `python-pptx`, which brings Pillow and lxml).
- LibreOffice (`soffice`) and poppler (`pdftoppm`) for rendering.
- `fc-match` (fontconfig) lets the builder measure text with the real font; without it, it falls back to an average character width.

## Commands

`<skill>` is this skill's directory (for example `~/.claude/skills/slide-presentation`).

```bash
# outline and validation only (fast; run after every spec edit)
uv run --no-project --with python-pptx python <skill>/scripts/build_deck.py slides/<deck>_spec.md --check --outline

# build (draft: proposed/open slides are tagged; open slides are placeholders)
uv run --no-project --with python-pptx python <skill>/scripts/build_deck.py slides/<deck>_spec.md

# final build: every slide agreed, no warnings
uv run --no-project --with python-pptx python <skill>/scripts/build_deck.py slides/<deck>_spec.md --final

# lint and render
uv run --no-project --with python-pptx python <skill>/scripts/qa_deck.py slides/<deck>.pptx \
    --spec slides/<deck>_spec.md --render /tmp/<deck>-render

# does an existing deck still match the spec? (hand edits, stale build)
uv run --no-project --with python-pptx python <skill>/scripts/build_deck.py slides/<deck>_spec.md --verify slides/<deck>.pptx
```

Render output goes outside the repository (or to an ignored directory). Delete it when done.

## The grid

On the 10 × 5.625 in (16:9) Google Slides default; other 16:9 sizes scale uniformly.

| Element | Position (in) | Style |
|---|---|---|
| Part tag | top right, y 0.14 | 10 pt gray; "· PROPOSED" / "· OPEN" appended in draft builds |
| Title | x 0.34, y 0.40-1.00, bottom-anchored | 28 pt bold, one line |
| Claim line | y 1.02-1.40 | 15 pt muted gray, one line |
| Content | y 1.60 to 4.42 (4.95 without a band) | text 16 → 12 pt, tables 14 → 10 pt, largest tier that fits |
| Transition band | y 4.55-5.00, full body width | pale accent fill, accent bar at the left, "→" + 14 pt text |
| Source line | y 5.12 | 9 pt gray, one line |
| Slide number | template placeholder, bottom right | template style |

Figures placed `left` or `right` take `Width` of the content width (default 50%); the blocks share the other column. `below` and `above` give the figure the height the blocks leave free (at least 1.6 in).

Tables: no template style, light gray bold header, white body, thin gray rules; column widths follow content (wrapped when the table is wider than its column); cells with `**` get a pale accent fill.

## Visual QA

Open every PNG and check, slide by slide:

- [ ] The title is on one line and the claim line is on one line.
- [ ] Nothing overflows its area, overlaps another element, or runs into the transition band or source line.
- [ ] Table cells are not cramped; header text is readable; the highlighted cells are the deciding ones.
- [ ] Figure placeholders show the right label and caption; inserted images are legible at slide size.
- [ ] The transition band is present on every content slide except the last, in the same place.
- [ ] No missing glyphs (boxes or "?"); special characters (×, →, ≈, ÷) render.
- [ ] The part tags read in story order.

Then review every lint hit:

- Banned terms are errors: remove or rename on the slide (and in the notes).
- Over-stating words are prompts: rewrite with scope, or keep deliberately when the word is literally true and scoped ("integer only" describing hardware is fine; "the only option" is not).
- Path-like strings: move them to the sources index.

Builder warnings come from estimates; the render decides. If a warning says a line does not fit but the render shows it does, note it and move on; if the render shows an overflow the builder missed, shorten the text in the spec.

## Delegating the build to a sub-agent

Give the sub-agent the spec path, the skill path, the output path, the branch, and these rules:

1. The spec is authoritative. Do not change claims, numbers or wording. If something cannot be built as written (overflow, ambiguity), report it with a proposed spec change; do not apply it silently.
2. Build, render, lint, and look at every PNG; fix only layout issues that do not change wording (figure width or position, splitting a table caption), in the spec.
3. Stage only the deck's files by explicit path (spec, sources index, `.pptx`, figure files). Never `git add -A` or `git commit -a`.
4. Report: build summary line, lint hits and how each was resolved, the slides with layout problems, and any proposed spec changes.
