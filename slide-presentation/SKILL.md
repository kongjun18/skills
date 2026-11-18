---
name: slide-presentation
description: Plan, specify, build and check slide decks (.pptx) through one Markdown deck spec that the user reviews and the builder turns into slides. Use for any request to make, outline, restructure, polish or review slides, a deck, a talk or a presentation, such as a group meeting talk, a research talk, a project sync meeting or a progress update, and for building a pptx from agreed content with a template. Core pipeline and principles are general; case profiles (research group talk, project sync meeting) and project overrides (authors, template, units, vocabulary, banned internal names) customize it.
---

# Slide Presentation

A deck is an argument: each slide makes one point and hands over to the next. Agree on that argument in a Markdown spec first; the deck is generated from the spec and never edited separately.

```
goal and audience → storyline → deck spec (per slide) + sources index → build → render → visual QA → user review
                                  ↑__________________ every change goes here first ___________________|
```

## Setup

1. **Pick the case profile** and read it: [research-group-talk](references/profiles/research-group-talk.md) (ongoing work on its way to a paper) or [project-sync-meeting](references/profiles/project-sync-meeting.md) (progress since last time). If neither fits, say so and agree on the structure with the user.
2. **Find the project override**: the spec's `Project profile` field, else a `slide-profile.md` in the spec's directory or a parent up to the repository root, else a project skill for slides. It supplies authors, template, units, vocabulary, banned internal names and recorded feedback; create one from [assets/slide-profile-template.md](assets/slide-profile-template.md) when a project has none. Precedence: user > deck spec > project override > case profile > this skill. Details: [customization.md](references/customization.md).
3. **Ask what is not known**: audience, whether length matters (do not optimize for it unprompted), what must not appear, which figures the user will copy in from papers, the template.

## Pipeline

1. **Goal and storyline.** Write the audience, the goal, and the logic chain (one clause per slide, each answering the question the previous slide raised) into the spec's free sections. Check every consecutive pair for a missing step. Agree on it before writing slides.
2. **Deck spec.** Copy [assets/deck-spec-template.md](assets/deck-spec-template.md) to `<deck>_spec.md`. Per slide: Part, Status, Title (the heading), Claim, On the slide, Figure, Transition, Notes, Sources. Format: [spec-format.md](references/spec-format.md). Start lean.
3. **Review in batches.** Discuss a few slides at a time. Mark each `agreed`, `proposed` or `open` with the date and the reason for changes. Never build an `open` slide as final.
4. **Sources index.** Trace every number and quoted claim to its origin in `<deck>_sources.md` ([template](assets/sources-template.md)); verify against the source itself, not memory.
5. **Build** with [scripts/build_deck.py](scripts/build_deck.py): it validates the spec, lays out the fixed grid on the template, writes the deck, and re-reads it to confirm every field landed unchanged.
6. **Render and lint** with [scripts/qa_deck.py](scripts/qa_deck.py), then open every PNG. Commands and the visual checklist: [build-and-qa.md](references/build-and-qa.md).
7. **User review.** Hand over the deck, the open/proposed slides, the lint hits you kept and why. Feedback goes into the spec, then rebuild. Record style feedback in the project override (see [customization.md](references/customization.md#recording-feedback)).

## Principles

Full rules with the mistakes behind them: [principles.md](references/principles.md).

- **Content before format.** The spec is the source of truth; wording changes go there first.
- **One point per slide.** Title = short claim (3-7 words). Claim line = one line, about 12-16 words, with scope. Body = minimal evidence: one figure, one small table, 1-3 numbers, or a one-sentence cause; at most three bullets. A visible transition at the bottom. Everything else to the notes.
- **Lean.** Merge slides that make the same point. No outline or agenda slides unless asked.
- **Calibrated.** No "must", "never", "always", "cannot", "no one", "exactly", absolute "only". Check novelty and gap claims against related work; prefer "unexplored", "partly explained".
- **Directions, not early results**, when presenting research questions of ongoing work, unless asked.
- **Evidence.** Prefer other papers' data in background and motivation; cite on the slide; label estimates and derived numbers with how they were derived; scope every number; quote a paper's rates when its percentage disagrees with them; one source per table column.
- **Words and units.** A small vocabulary up front; define terms at first use (figure labels count); avoid clashing terms; units per domain stated once, never converted silently; no step IDs, host names or paths on slides or in notes.
- **Figures.** A figure copied from a paper is a labelled placeholder with caption and citation until the user supplies it; show only what the user asked for.
- **Layout.** The user's template, else the bundled [Google Slides default](assets/templates/google-slides-default.pptx); a fixed grid; one accent color for key numbers only; readable tables.

## Pre-handover checklist

- [ ] Storyline agreed; no gap between consecutive slides; background and motivation do not overlap.
- [ ] Every content slide: claim title, one-line claim, minimal evidence, transition; detail in notes.
- [ ] No over-stated or unchecked novelty claims; no results where the profile asks for directions.
- [ ] Every number scoped, sourced on the slide, and traced in the sources index.
- [ ] Terms defined at first use; units consistent; no internal names (lint clean).
- [ ] `build_deck.py` reports no errors; warnings resolved or explained; `--final` passes when the user wants the final deck.
- [ ] Every rendered slide inspected; render outputs deleted or kept outside the repository.
- [ ] Only the deck's files staged, by path.
