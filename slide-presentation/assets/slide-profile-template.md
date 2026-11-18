# Slide profile: <project>

<!-- Copy to the project as slide-profile.md (repository root or the slides directory).
     Field lines are read by build_deck.py and qa_deck.py; the rest is guidance for the agent.
     See references/customization.md in the slide-presentation skill. -->

- **Extends:** research-group-talk
- **Template:** ../templates/project-template.pptx
- **Font:** Arial
- **Accent:** 1967D2
- **Authors:** First Author · Second Author · Third Author
- **Affiliation:**
  - Lab name · Department
  - University
- **Banned terms:** TODO, TBD
  - /\bS\d{2}\.\d{2}(\.\d+)?\b/
  - internal-host-name

## Audience and occasions

- Who attends, what they know, how often the project presents.

## Vocabulary and units

- Glossary: `<path to the glossary>`; slide term → definition → internal name it replaces.
- Units: <quantity → unit>, stated once per deck.
- Words to avoid: <word> (say <replacement>), with the reason.

## Overrides of the case profile or core principles

- <rule> (tightens | relaxes | adds) <principle>, because <user's reason>, <date>.

## Evidence locations

- Where numbers come from (reports, result directories); they go in the sources index, never on slides.

## Feedback log

- <YYYY-MM-DD>: <what the user asked> → <rule>.
