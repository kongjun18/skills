# Deck spec: <talk title>

<!-- The single source of truth for the deck. Format: references/spec-format.md.
     Edit wording here first, then rebuild; never hand-edit generated text in the .pptx.
     HTML comments like this one are ignored by the builder. -->

Status: slides 1-3 agreed <date>; 4 proposed; 5 open.

## Deck

- **Profile:** research-group-talk
- **Banned terms:** TODO, TBD, /\bv\d+_final\b/

<!-- Optional: Output (default: this file's name without _spec, .pptx), Template, Project profile, Font,
     Accent, Length. See references/spec-format.md. -->

## Goal and audience

- Audience: <who>; what they already know; what they should leave with.
- Length: <about N min, or "not strict">. Ask whether length matters before optimizing for it.

## Storyline

<!-- The logic chain, one clause per slide, each step answering the question the previous one raised. -->
Fact the audience accepts (2) → the case existing work makes (3) → the gap it leaves (4) → our question (5).

## Vocabulary and units

- <term>: <definition at first use>; replaces <internal name>.
- Units: <unit per quantity>, stated once; never converted silently.

## References

- [1] A. Author et al., "Title of the cited paper," Venue Year.
- [2] B. Author et al., "Title of another cited paper," Venue Year.

## Slides

### 1. Group Meeting

- **Layout:** title
- **Status:** agreed
- **Subtitle:** One line that names the topic
- **Authors:** First Author · Second Author · Third Author
- **Affiliation:**
  - Lab name · Department
  - University
- **Minutes:** 0.5
- **Notes:** One sentence that frames the talk.

### 2. Short claim as the title

- **Part:** Background
- **Status:** agreed
- **Minutes:** 1.5
- **Claim:** One plain sentence with its scope, about twelve to sixteen words, on one line.
- **Full claim:** The longer sentence with every qualifier; it goes to the speaker notes.
- **On the slide:**
  - __Label:__ one fact the audience needs, with its **key number** highlighted.
  - A second fact; keep at most three bullets.

  Flow: Input -> Stage A -> **Stage that matters** -> Output
- **Transition:** One sentence that raises the question the next slide answers.
- **Notes:**
  - Scope, caveats and extra data go here, not on the slide.
  - Say how every derived number was derived.
- **Sources:** Author et al. [1], Table 2.

### 3. Tables carry the evidence

- **Part:** Background
- **Status:** agreed
- **Minutes:** 1.5
- **Claim:** A small table with one row per option and the deciding cells highlighted.
- **On the slide:**
  Table: What the table shows, with its unit and scope
  | Option | Metric A (unit) | Metric B (unit) |
  |---|---:|---:|
  | Baseline | 1.0 | 10 s |
  | Option one | **2.0** | 12 s |
  | Option two | 1.1 | **5 s** |

  Estimate = how the derived column was computed [2].
- **Transition:** Why the highlighted cells matter for the next step.
- **Sources:** Author et al. [2], Table 1; derived as stated.

### 4. Copied figures stay placeholders

- **Part:** Motivation
- **Status:** proposed
- **Minutes:** 2
- **Claim:** A figure copied from a paper sits in a labelled box until the user inserts it.
- **On the slide:**
  | Work | What it studies | What it leaves open |
  |---|---|---|
  | Author et al. [1] | a related problem | the case we study |
  | Author et al. [2] | a related system | **the gap this talk is about** |
- **Figure:** Author et al. [1] Fig. 3
  - Caption: Author et al. [1] Fig. 3: "Quoted figure title."
  - Position: left
  - Width: 45%
- **Transition:** So we ask the research question.
- **Notes:** Insert the figure by setting File: to an image path, so rebuilds keep it.
- **Sources:** Author et al. [1], Fig. 3; Author et al. [2].

### 5. Research question as a question?

- **Part:** Research question
- **Status:** open
- **Claim:** To be agreed with the user.
- **On the slide:**
  - Candidate framing A.
  - Candidate framing B.

### 6. References

- **Layout:** references
- **Part:** Backup
- **Status:** agreed
