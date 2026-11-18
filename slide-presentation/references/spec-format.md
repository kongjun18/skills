# Deck spec format

The deck spec is one Markdown file, normally `<deck>_spec.md` beside the deck. It is the single source of truth: the user reviews and edits it, and `scripts/build_deck.py` builds the `.pptx` from it directly. There is no second content file. Wording changes go into the spec first; then rebuild. [assets/deck-spec-template.md](../assets/deck-spec-template.md) is a buildable example of every feature below.

## File structure

```
# <any title>                     ignored by the builder
<free text>                        ignored (status line, review notes)

## Deck                            parsed: deck settings (field lines only)
## <Goal and audience>             free sections, any names, ignored by the builder:
## <Storyline>                     audience, logic chain, vocabulary, units, words to avoid,
## <Vocabulary and units>          acceptance checklist, data that must not appear
## References                      parsed: "- [n] full reference" lines or "| [n] | short | full |" rows
## Slides                          parsed: one "### N. Title" heading per slide
```

- Section names are case-insensitive. Only `Deck`, `References` and `Slides` are parsed.
- HTML comments (`<!-- ... -->`) are removed before parsing; use them for guidance the deck must not show.
- Code fences are not allowed inside `Deck` or `Slides`.
- Do not keep a separate slide table (number, title, status) in a free section; it drifts. Print it instead with `build_deck.py SPEC --outline --check`.

## Field lines

Inside `Deck` and each slide, every line is a field or a continuation:

```
- **Field name:** value on the same line
  continuation lines are indented by two spaces;
  blank lines inside a field separate content blocks
```

`- **Field name**: value` (colon outside the bold) is accepted too. Any other unindented line is an error, as is an unknown or duplicated field name. Field names are case-insensitive.

## Deck fields

| Field | Meaning | Default |
|---|---|---|
| Profile | case profile in `references/profiles/` (guidance for the agent, not parsed) | none |
| Project profile | path to the project's `slide-profile.md`, relative to the spec | auto-discovered; see [customization.md](customization.md) |
| Template | `.pptx` template, relative to the spec | project profile's, else the bundled Google Slides default |
| Output | output `.pptx`, relative to the spec | spec name without `_spec`, extension `.pptx` |
| Banned terms | comma-separated, or one per `- ` continuation line; `/regex/` allowed | merged with the project profile's |
| Font | font family for all text | Arial |
| Accent | the one accent color, hex | 1967D2 |
| Length | talk length, for the reader | none |

## Slides

Heading: `### N. Title`. `N` is the slide number, 1..N in order (the user cites slides by number). The title is the heading text; there is no Title field.

| Field | Required | Goes to |
|---|---|---|
| Layout | no; `content` (default), `title` or `references` | — |
| Status | yes: `agreed`, `proposed` or `open`, optionally followed by a date and reason | part tag in draft builds |
| Part | content slides (warning if missing) | small tag, top right |
| Minutes | no | notes ("Time: 1.5 min (ends 4:30)") and the outline total |
| Claim | content slides that are not open | the line under the title, muted |
| Full claim | no | notes, first line ("Claim in full: ...") |
| On the slide | usually | content area; grammar below |
| Figure | no | figure placeholder or image; sub-items below |
| Transition | content slides except the last (warning) | tinted band at the bottom, and the notes |
| Notes | no | speaker notes, line by line |
| Sources | no | source line at the bottom ("Sources: ..."); citations only, never file paths |
| Subtitle, Authors, Affiliation | title slide | title slide; Authors and Affiliation fall back to the project profile |

Status behavior:

- `agreed`: built normally.
- `proposed`: built normally; draft builds append "· PROPOSED" to the part tag.
- `open`: never built as final. The slide shows its title, claim (if any) and a dashed "Open: not agreed yet" box listing up to three lines of the sketch; no transition band.
- `--final` fails unless every slide is `agreed`, and turns warnings into errors.

Layouts:

- `title`: template's TITLE layout; heading = title, Subtitle in the accent color, then Authors and Affiliation lines centered below.
- `content`: TITLE_ONLY layout plus the fixed grid (part tag, title, claim line, content area, transition band, source line, slide number).
- `references`: title plus the `On the slide` lines, or, if absent, every entry of `## References` in number order; the font shrinks from 12 to 9 pt to fit.

## On the slide

Blocks are separated by blank lines or by a change of kind. In order of appearance they stack top to bottom in the content area:

| Line | Block |
|---|---|
| `- text`, `* text` | bullet; indent two more spaces per level |
| `1. text` | numbered item |
| any other text | plain paragraph (use for a one-line explanation, or `__Why:__ ...`) |
| `Table: caption` | bold caption of the table that follows |
| `\| a \| b \|` rows | table; first row is the header; a `\|---\|---:\|` row sets alignment (`---:` right, `:---:` center) |
| `Flow: A -> B -> **C** -> D` | row of boxes with arrows; `**C**` is the highlighted step (`→` also works) |

Inline markup, everywhere on the slide:

- `**x**`: highlight in the accent color, bold. Use for the deciding numbers only. In a table, a cell containing `**` also gets a pale accent fill, so mark only the cells that carry the claim.
- `__x__`: bold label in the text color ("__Prefix caching:__ ...").

The builder picks the largest font tier that fits (text 16 pt and tables 14 pt, down to 12 and 10 pt) and warns with the overflow in inches when nothing fits.

## Figure

```
- **Figure:** ShadowServe [3] Fig. 4          label shown in the placeholder box
  - Caption: ShadowServe [3] Fig. 4: "Quoted caption."
  - File: figures/fig4.png                   optional; relative to the spec; inserted, aspect kept
  - Position: left                           left (default), right, below or above the blocks
  - Width: 45%                               share of the content width for left or right; 25-75%
```

- One figure per slide. `Figure: none` or no field means no figure.
- Without `File`, the slide shows a dashed, labelled placeholder box with the caption under it, for a figure the user copies from a paper. Prefer saving the copied figure as an image and setting `File`, so rebuilds keep it; a figure pasted into the `.pptx` by hand is lost on rebuild.

## Validation

Errors (no deck is written): unknown or duplicate field; stray unindented text; heading not `### N. Title`; duplicate slide numbers; missing or invalid Status; missing Claim on a non-open content slide; table rows with a different cell count from the header; `Table:` caption without a table; figure file missing; invalid figure position; references slide with nothing to list.

Warnings: title over 7 words or wider than one line at 28 pt; claim over 16 words or wider than one line at 15 pt; transition or source line wider than one line; more than 3 top-level bullets; missing Part; missing Transition (except the last content slide); nothing on the slide; content overflow at the smallest font; slide numbers not 1..N; template not 16:9.

After writing the deck, the builder re-opens it and checks that every title, claim, transition, source line, text block, table cell and notes line equals the spec (round trip). `build_deck.py SPEC --verify DECK` runs the same check on an existing deck, to detect hand edits or a stale build.
