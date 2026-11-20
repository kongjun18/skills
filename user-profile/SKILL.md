---
name: user-profile
description: >-
  Maintain the user's personal profile at ~/.config/agent-skills/user-profile: a short profile.md (background, interests,
  current work, resources) plus an append-only signals.md that agents add to when the user states a
  lasting interest or preference. Use for "set up my profile", "update my profile", "what do you know
  about my interests", "fold my signals into the profile", "review my profile". Skills that read the
  profile only need its path; they do not need this skill.
---

# User Profile

A small, evolving description of the user that any skill or harness can read
when a task depends on who the user is: what they work on, what they already
know, and what they can run. It is context, not a constraint.

## Location

`${XDG_CONFIG_HOME:-~/.config}/agent-skills/user-profile/` is the fixed path
every harness uses (`PROFILE_DIR` below). It holds two plain files and is
never put under version control, because it is personal:

- `profile.md`: the profile. Short, free-form Markdown, about a page.
- `signals.md`: append-only evidence that may change the profile.

The profile lives outside the skills repository and holds only what is useful
for the user's work. Never copy it into a repository. Leave out IDs, grades, contact details, and anyone else's
unpublished work.

## Reading

- Read `profile.md` when a task depends on the user's interests, expertise, or
  resources. Do not load it for unrelated tasks.
- Use it to rank, frame, and connect, never to exclude. Work outside the
  profile can be the most important result, so keep room for it and say when
  something outside the profile looks strong.
- If the profile and the user's current request disagree, the request wins.

## Capturing signals

Append one line to `signals.md` when the user states or clearly shows a lasting
interest, disinterest, or change: a new project, a direction they want to
follow, a topic they call noise, a new resource.

```
- 2026-11-19 · user said FPGA accelerator papers are noise for them · digest review
```

- Record what the user said or did, not your inference about them.
- Skip one-off task preferences; those belong to the task.
- Never edit `profile.md` while capturing.

## Updating the profile

Run when the user asks, or suggest it when `signals.md` has about ten lines
since the last update.

1. Read `profile.md` and the signals added since its `Last updated:` date.
2. Propose a diff to `profile.md`: add, reword, or drop entries. Also flag
   entries no signal has touched in about six months and ask whether they still
   hold.
3. Apply only what the user approves and set `Last updated:` to today. Keep
   the signals; they are the profile's history.

## Setup

If `PROFILE_DIR` does not exist, create it, copy
[assets/profile.md](assets/profile.md) into it, and add an empty `signals.md`.
If the user already keeps a briefing about themselves elsewhere, such as a
digest's context file, start from it instead of the template. Fill the gaps
from the user's answers, then add this pointer to each harness's global instructions
(`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`):

```
- Personal profile: `~/.config/agent-skills/user-profile/profile.md` describes my background, interests, current work, and resources. Read it when a task depends on them; it is context, not a constraint, so never use it to exclude work. When I state a lasting interest or preference, append a dated line to `~/.config/agent-skills/user-profile/signals.md` (format in the `user-profile` skill).
```
