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
