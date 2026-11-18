# Profiles and project overrides

The skill has three layers. Later layers override earlier ones; the user's instruction in the conversation overrides all of them.

| Layer | Where | Holds |
|---|---|---|
| Core | `SKILL.md`, [principles.md](principles.md) | pipeline, principles, checklists, builder |
| Case profile | `references/profiles/<case>.md` | what differs by kind of talk: structure, what to show, length habits |
| Project override | the project's `slide-profile.md`, or a project skill | authors, template, units, vocabulary, banned names, house style, feedback log |
| Deck spec | the `## Deck` section and free sections of the spec | settings for this one deck |

Precedence: user instruction > deck spec > project override > case profile > core.

## Case profiles

Pick one at the start and name it in the spec (`- **Profile:** research-group-talk`). Bundled profiles:

- [research-group-talk](profiles/research-group-talk.md): ongoing project that will become a paper; paper structure; directions, not results.
- [project-sync-meeting](profiles/project-sync-meeting.md): regular project sync; results since last time; what changed, what's next.

To add a case, copy the shape of an existing profile: purpose, audience, structure, content rules, defaults, extra checks. Keep project facts out of case profiles.

## Project override

A project overrides or extends a profile with a `slide-profile.md` file. Start from [assets/slide-profile-template.md](../assets/slide-profile-template.md).

How the skill finds it, first match wins:

1. The spec's `- **Project profile:** <path>` field.
2. `slide-profile.md` in the spec's directory or any parent directory up to the repository root.
3. A project skill for slides (for example `.claude/skills/<project>-slides/SKILL.md`). The agent reads it as prose; if it should also feed the builder, it points to a `slide-profile.md`.

What the builder reads from `slide-profile.md` (field lines, same syntax as the spec):

| Field | Effect |
|---|---|
| Extends | the case profile used when the spec names none |
| Template | default template, relative to the profile file |
| Font, Accent | default font family and accent color |
| Banned terms | merged with the spec's; checked by `qa_deck.py --spec` |
| Authors, Affiliation | defaults for the title slide |

Everything else in the file is prose for the agent: audience, vocabulary file, units, rules that tighten or relax a principle (say which), and the feedback log. Unknown fields are ignored by the builder.

Example of a project override: the KVFlow project keeps a project skill, `kvflow-slides`, with its own numbered rules, glossary, authors and banned internal names; it also asks for outline slides, which this skill omits by default. That is the kind of difference a project override records.

## Recording feedback

When the user corrects style, wording or structure:

1. Apply the correction to the spec and rebuild.
2. Add a dated line to the project override's feedback log: what the user asked, and the rule that follows from it.
3. If the rule holds for every deck of that kind, propose adding it to the case profile; if for every deck, to [principles.md](principles.md). Edit the shared skill only when the user agrees.
