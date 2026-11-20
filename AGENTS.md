# Skills Repository Guide

## Layout

- `<name>/SKILL.md`: one maintained skill per top-level directory; the directory name matches the frontmatter `name`.
- Optional skill resources live inside the skill in `agents/`, `assets/`, `references/`, or `scripts/`.
- `third-party/`: gitignored clones of upstream skill repositories; pinned in [third-party/SOURCES.md](third-party/SOURCES.md).
- `tools/`: repository tooling (`check.py`, `install.sh`).

## Maintained Skills

Working discipline:

- `good-agent`: general engineering and research work discipline.
- `high-signal-writing`: concise, reader-first conversational responses (not artifacts).
- `repo-memory`: repository-local knowledge and closeout protocol.

Git and code review:

- `git`: local Git conventions — worktrees under `.worktree/`, and safe rebase / Graphite restack with backups and a restore doc.
- `address-pr-comments`: fetch and triage GitHub PR review feedback into a living review doc.

Research:

- `exploration-report`: agent-run explorations recorded as reproducible in-repo reports with a structural linter.
- `systems-evaluation-planner`: systems-paper claim and evaluation planning (`evaluation_plan.yaml`).
- `systems-paper-plotting`: auditable systems-paper figure production from the plan.
- `system-research-scout`: evidence-bound survey of recent systems-conference papers into research ideas.
- `pull-recent-papers`: weekly arXiv digest and research radar.

Learning:

- `teachme`: self-contained HTML tutorials that teach a repository, concept, or research direction, with a structural checker.

Papers and talks:

- `paper-writer`: single entry point for writing paper text — outline, draft, rebuild from old material, refine, simplify; owns the shared terminology contract.
- `paper-presentation-review`: read-only presentation diagnosis and independent verification of revisions.
- `paper-hygiene`: meaning-preserving mechanical cleanup of source and rendered PDF.
- `paper-integrity`: report-only pre-submission gate, starting with citations.
- `paper-review`: reviewer-side work on someone else's paper — develop the user's review, or run an independent review.
- `slide-presentation`: spec-first slide decks (storyline → Markdown deck spec → pptx builder → render and lint).

## Skill Design Rules

Every agent that adds or edits a skill follows these rules.

1. **One owner per request type.** The `description` is a trigger contract: what the skill owns, with trigger phrases, and what it routes elsewhere ("for X, use Y"). Before adding or broadening a trigger, grep the other descriptions for collisions and resolve them.
2. **SKILL.md is the core, not the manual.** Keep it to about 300 lines or fewer: purpose, non-negotiables, workflow, routing, done criteria. Put detail in `references/`, each linked from SKILL.md with the condition for reading it. Never require loading every reference up front; a typical request should load well under 1,000 lines.
3. **State each rule once.** Other places link to it instead of restating it. A contract shared by several skills lives in one owner skill's `references/`, and the others link to `../<owner>/references/<file>.md`.
4. **Generic skills carry no project specifics.** No project vocabulary, repository paths, venues, author names, or one-paper examples. Those belong in the project's own `AGENTS.md` or project skill. Examples use neutral placeholders.
5. **Generalize episode fixes.** When a failure motivates a new rule, write the general rule once in its home section, with at most one short example. Do not append the same patch to several files.
6. **Few modes, one vocabulary.** Keep modes and stages few, give them one naming scheme, and use one schema per artifact.
7. **Everything claimed exists and works.** Referenced scripts ship with the skill and run; validators fail on empty or unfilled input; linked files resolve.
8. **Skills hold definitions only.** Run outputs, caches, corpora, personal config, and other teams' repositories live outside this repository. A skill writes its outputs to the user's working repository or a user-chosen directory, never into this one.
9. **Preserve third-party provenance.** Keep upstream layouts intact, make only minimal compatibility fixes, and pin each upstream in `third-party/SOURCES.md`.
10. **Per-user files follow the XDG Base Directory spec.** A file a skill keeps outside the user's project goes under `agent-skills/<skill-name>/` in the matching base directory, using the `XDG_*` variable when it is set:
    - config the user edits, such as settings and profiles: `${XDG_CONFIG_HOME:-~/.config}/agent-skills/<skill-name>/`
    - data the skill accumulates that the user would miss, such as corpora and history: `${XDG_DATA_HOME:-~/.local/share}/agent-skills/<skill-name>/`
    - state such as logs, last-run markers, and resumable progress: `${XDG_STATE_HOME:-~/.local/state}/agent-skills/<skill-name>/`
    - cache that is safe to delete and regenerate: `${XDG_CACHE_HOME:-~/.cache}/agent-skills/<skill-name>/`

    A file shared by several skills lives under its owner skill's name. Never create dotfiles or dot-directories directly in `~`. A missing config falls back to bundled defaults; no skill requires one to exist. Deliverables still go to the user's project or a chosen directory (rule 8).

## Validation

- Run `python3 tools/check.py` before handoff. It validates frontmatter, relative links, SKILL.md length, and the install symlinks.
- Run the skill-creator `quick_validate.py` against every changed skill directory when it is available.
- After adding, renaming, or removing a skill, run `tools/install.sh` to refresh the symlinks in `~/.claude/skills` and `~/.codex/skills`.
- Inspect `git diff` and `git status` before handoff; preserve unrelated user changes.

## Repository Memory

- Keep this file as the short root index.
- Create an epic under `docs/epics/` only for work that will span multiple tasks or sessions.
- Route temporary investigation output outside the repository or to ignored scratch space.
