# `_docs/` Layout

Every document a skill or agent generates inside a project goes under one
top-level `_docs/` directory. This file owns the layout; other skills link to
their section here.

The underscore keeps agent documents apart from a project's own `docs/`, which
often holds human documentation and may be published by a documentation-site
tool.

```
_docs/
├── README.md        what this directory is, and an index of its sections
├── knowledge/       repo-memory: knowledge useful across epics, with index.md
├── specs/           repo-memory: accepted specifications
├── epics/           repo-memory: index.md and one directory per epic
├── explorations/    exploration-report: <YYYY-MM-DD>-<slug>/report.md with its scripts, data, figures
├── tutorials/       teachme: <slug>.html
└── scratch/         never committed
    ├── pr-reviews/  address-pr-comments: PR_<id>_REVIEW.md and per-thread docs
    ├── restack/     git: RESTACK-RESTORE-<YYYYMMDD>.md
    └── integrity/   paper-integrity: one <YYYYMMDD_HHMM>/ directory per run
```

## Rules

- **Create only what the work needs.** Create `_docs/README.md` with the first
  section; keep it to a few lines that say agents and skills write here and
  link each section that exists.
- **Commit policy.** `scratch/` is never committed: on first use add
  `/_docs/scratch/` to `.git/info/exclude`, which every worktree of the
  repository shares, and leave the project's `.gitignore` alone. Other
  sections follow their owner skill's commit policy.
- **Repositories you do not own.** When working in someone else's repository,
  exclude all of `/_docs/` in `.git/info/exclude` and commit nothing there.
- **Existing layouts stay.** A repository whose `AGENTS.md` names other
  locations for these documents keeps them until the user migrates it.
- **Out of scope.** Files that are inputs to a deliverable stay with it, such
  as a paper's glossary, an evaluation plan, a deck's spec and sources, and
  the data and figures of the paper itself. `README`, `AGENTS.md`, and
  `CLAUDE.md` stay at the repository root. Skills that work across projects
  write to a directory the user chooses.
