#!/usr/bin/env python3
"""Check repo-memory notes for scattered knowledge.

Enforces the mechanically checkable part of Non-Negotiable Rule 11:
one topic has exactly one current note.

Usage:
    lint_notes.py [PATH ...]

PATH defaults to docs/. Exit status is 1 when any finding is reported,
0 when the notes are clean, and 2 on usage error.

Detects:
  pointer-note   a note whose body is mostly a reference to another note
  duplicate-stem two or more notes in one directory sharing a title stem
  flat-pile      many sibling notes in one directory with no index

It cannot tell whether two differently named notes cover the same topic.
Treat a clean run as the absence of obvious scatter, not as proof of good
structure.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

# A note filename is <ID>-<short-kebab-title>.md per SKILL.md.
NOTE_RE = re.compile(r"^(\d{3})-(.+)\.md$")

# Wikilinks, markdown links to .md files, and bare note filenames.
LINK_RE = re.compile(r"\[\[[^\]]+\]\]|\[[^\]]*\]\([^)]*\.md[^)]*\)|\b\d{3}-[a-z0-9-]+\.md\b")

# Language suggesting the note exists only to correct another one.
SUPERSEDE_RE = re.compile(
    r"\b(supersed(es|ed|ing)|replaces\s+note|corrects?\s+note|"
    r"invalidates?\s+note|obsoletes?\s+note|see\s+instead)\b",
    re.IGNORECASE,
)

# A directory with more notes than this and no index is a flat pile.
FLAT_PILE_THRESHOLD = 3

# Below this many non-link words, a note is mostly a pointer.
POINTER_MAX_WORDS = 60


def strip_noise(text: str) -> str:
    """Remove fenced code and headings so prose checks see prose only."""
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"^#{1,6} .*$", " ", text, flags=re.MULTILINE)
    return text


def title_stem(title: str) -> str:
    """Normalize a kebab title for near-duplicate comparison."""
    words = [w for w in title.split("-") if w not in {"and", "the", "for", "of", "in", "to"}]
    return "-".join(sorted(words))


def check_pointer_note(body: str) -> list[str]:
    prose = strip_noise(body)
    links = LINK_RE.findall(prose)
    without_links = LINK_RE.sub(" ", prose)
    words = len(without_links.split())

    findings = []
    supersede = SUPERSEDE_RE.search(prose)
    if links and words < POINTER_MAX_WORDS:
        findings.append(
            f"pointer-note: {words} words of prose around {len(links)} note "
            f"reference(s). A correction belongs inside the note it corrects "
            f"(SKILL.md: Correcting a note)."
        )
    elif supersede and words < POINTER_MAX_WORDS * 3:
        findings.append(
            f"pointer-note: short note using supersession language "
            f"({supersede.group(0)!r}). Edit the original note in place instead."
        )
    return findings


def check_directory(directory: Path, notes: list[Path]) -> list[tuple[Path, str]]:
    findings: list[tuple[Path, str]] = []

    by_stem: dict[str, list[Path]] = defaultdict(list)
    for note in notes:
        match = NOTE_RE.match(note.name)
        if match:
            by_stem[title_stem(match.group(2))].append(note)

    for stem, paths in sorted(by_stem.items()):
        if len(paths) > 1:
            names = ", ".join(p.name for p in sorted(paths))
            findings.append(
                (
                    directory,
                    f"duplicate-stem: {names} share the title stem {stem!r}. "
                    f"Merge them into one note (SKILL.md: Prefer merging over "
                    f"fragmenting).",
                )
            )

    has_index = any(p.name.lower() == "index.md" for p in directory.iterdir() if p.is_file())
    if len(notes) > FLAT_PILE_THRESHOLD and not has_index:
        findings.append(
            (
                directory,
                f"flat-pile: {len(notes)} sibling notes with no index.md. Merge "
                f"them, or move them under an epic with an index (SKILL.md: "
                f"Prefer merging over fragmenting).",
            )
        )

    return findings


def lint(roots: list[Path]) -> int:
    findings: list[tuple[Path, str]] = []
    by_directory: dict[Path, list[Path]] = defaultdict(list)
    scanned = 0

    for root in roots:
        if not root.exists():
            print(f"note: {root} does not exist, skipping", file=sys.stderr)
            continue
        for path in sorted(root.rglob("*.md")):
            if "archive" in path.parts or ".git" in path.parts:
                continue
            if not NOTE_RE.match(path.name):
                continue
            scanned += 1
            by_directory[path.parent].append(path)
            try:
                body = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                print(f"note: cannot read {path}: {exc}", file=sys.stderr)
                continue
            findings.extend((path, f) for f in check_pointer_note(body))

    for directory, notes in sorted(by_directory.items()):
        findings.extend(check_directory(directory, notes))

    if not scanned:
        print("No notes found. Nothing to check.")
        return 0

    for location, message in findings:
        print(f"{location}: {message}")

    noun = "note" if scanned == 1 else "notes"
    if findings:
        print(f"\n{len(findings)} finding(s) across {scanned} {noun}.")
        return 1

    print(f"{scanned} {noun} checked, no obvious scatter found.")
    return 0


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("-")]
    if len(args) != len(argv[1:]):
        print(__doc__, file=sys.stderr)
        return 2
    roots = [Path(a) for a in args] or [Path("docs")]
    return lint(roots)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
