# Skills Repository Guide

## Layout

- `skills/`: maintained skills, one directory per skill.
- `third-party/`: upstream source repositories and their original skill layouts.
- Each maintained skill starts at `skills/<name>/SKILL.md`.
- Keep optional skill resources in `agents/`, `assets/`, `references/`, or `scripts/` inside that skill.

## Maintained Skills

- `address-pr-comments`: fetch and triage GitHub PR review feedback.
- `good-agent`: general engineering and research work discipline.
- `high-signal-writing`: concise, reader-first agent responses.
- `paper-presentation`: orchestrator for paper presentation review, guided paragraph generation, structural revision, and verification; delegates to the review and revise skills.
- `paper-presentation-review`: read-only presentation review (argument structure, terminology, section responsibility, figures) with located findings.
- `paper-presentation-revise`: presentation-preserving prose and structure revision that addresses review findings.
- `paper-integrity`: pre-submission integrity gate, starting with citations (existence, metadata, claim support, omissions, copied text); S0/S1/S2 tiers, offline/fast/full levels chosen at launch, stdlib scripts plus concurrent subagents, results table.
- `paper-review`: staged systems/database paper-review framework; editorial and citation checks implemented, deeper review stages reserved.
- `paper-hygiene`: source and rendered-PDF cleanup for mechanical defects, terminology drift, accidental duplication, float whitespace, and short paragraph tails.
- `paper-writer`: paper prose refinement (refine -> rethink -> refine, logic chain) and outline-first drafting with reviewer subagents.
- `rebase-restack`: recoverable Git rebase and Graphite restack workflow.
- `repo-memory`: repository-local knowledge and closeout protocol.
- `systems-evaluation-planner`: systems-paper claim and evaluation planning.
- `systems-paper-plotting`: auditable systems-paper figure production.

## Conventions

- Match each skill directory name to the `name` in its frontmatter.
- Use valid YAML frontmatter and keep trigger guidance in `description`.
- Link every bundled reference directly from `SKILL.md` using relative paths.
- Do not commit UUID-suffixed export names, duplicate export trees, or wrapper index pages.
- Preserve third-party layouts and provenance; make only minimal compatibility fixes unless a broader update is requested.

## Validation

- Run the skill-creator `quick_validate.py` validator against every directory containing `SKILL.md`.
- Check that relative Markdown links resolve and that maintained skills have no references to missing bundled files.
- Inspect `git diff` and `git status` before handoff; preserve unrelated user changes.

## Repository Memory

- Keep this file as the short root index.
- Create an epic under `docs/epics/` only for work that will span multiple tasks or sessions.
- Route temporary investigation output outside the repository or to ignored scratch space.
