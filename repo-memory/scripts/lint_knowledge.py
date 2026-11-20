#!/usr/bin/env python3
"""Check repo-memory knowledge notes for mechanically detectable problems.

Usage:
    lint_knowledge.py [PATH ...]

PATH defaults to _docs/ (docs/ in a repository that still uses it). Scans
numbered notes (NNN-<topic>.md, exactly three digits) wherever they sit: epic `knowledge/` directories, the legacy
epic `notes/` layout, `_docs/knowledge/`, and stray piles elsewhere. Files
under `archive/` count only for ID reuse. ADR folders (adr/, adrs/,
decisions/) are skipped, since superseded-by links are their convention.
Relative links are checked in every non-archived Markdown file scanned.

Exit status:
  0  notes found and no findings
  1  one or more findings
  2  usage error, a PATH that does not exist, or no Markdown files
     under PATH (an empty scan is never reported as clean)

Findings:
  pointer-note    a note that is mostly a reference to another note, or a
                  short note written to supersede or correct another one
  empty-note      a note with almost no prose
  duplicate-stem  notes in one directory sharing a title stem
  duplicate-id    one ID used twice in an epic, including archived notes
  mixed-layout    one epic keeps notes in both knowledge/ and notes/
  flat-pile       many sibling notes with no index.md beside or above them
  broken-link     a relative Markdown link that does not resolve

A clean run means no obvious problem, not good structure: the script
cannot tell whether two differently named notes cover the same topic.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

NOTE_RE = re.compile(r"^(\d{3})-(?!\d)(.+)\.md$")
SKIP_DIRS = {"adr", "adrs", "decisions", ".git"}
NOTE_DIRS = {"knowledge", "notes"}

# Wikilinks, Markdown links to .md files, and bare note filenames.
NOTE_LINK_RE = re.compile(r"\[\[[^\]]+\]\]|\[[^\]]*\]\([^)]*\.md[^)]*\)|\b\d{3}-[a-z0-9-]+\.md\b")
# Any inline Markdown link target, for the broken-link check.
MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")

# Language suggesting the note exists only to correct another one.
SUPERSEDE_RE = re.compile(
    r"\b(supersed(es|ed|ing)|replaces\s+note|corrects?\s+note|"
    r"invalidates?\s+note|obsoletes?\s+note|see\s+instead)\b",
    re.IGNORECASE,
)

FLAT_PILE_THRESHOLD = 3  # more sibling notes than this need an index
POINTER_MAX_WORDS = 60   # below this many non-link words, a linking note is a pointer
EMPTY_MAX_WORDS = 10     # below this many words, a note is empty


FENCE_RE = re.compile(r"^[ \t]*(```|~~~).*?^[ \t]*\1", re.DOTALL | re.MULTILINE)


def strip_code(text: str) -> str:
    """Drop fenced blocks (indented ones too) and inline code."""
    return re.sub(r"`[^`\n]*`", " ", FENCE_RE.sub(" ", text))


def prose_of(text: str) -> str:
    """Drop fenced blocks and headings; keep inline code text, since a
    backticked note filename is still a reference to that note."""
    text = FENCE_RE.sub(" ", text).replace("`", " ")
    return re.sub(r"^#{1,6} .*$", " ", text, flags=re.MULTILINE)


def title_stem(title: str) -> str:
    words = [w for w in title.split("-") if w not in {"and", "the", "for", "of", "in", "to", "a"}]
    return "-".join(sorted(words))


def is_archived(path: Path, root: Path) -> bool:
    return "archive" in path.relative_to(root).parts[:-1]


def sequence_owner(path: Path) -> Path:
    """The directory whose notes share one ID sequence (normally the epic):
    the nearest ancestor that is not a knowledge/, notes/, or archive/ dir."""
    owner = path.parent
    while owner.name in NOTE_DIRS | {"archive"} and owner.parent != owner:
        owner = owner.parent
    return owner


def check_note_body(body: str) -> list[str]:
    prose = prose_of(body)
    links = NOTE_LINK_RE.findall(prose)
    words = len(NOTE_LINK_RE.sub(" ", prose).split())
    if not links and words < EMPTY_MAX_WORDS:
        return [f"empty-note: {words} words of prose. Fill it or delete it."]
    if links and words < POINTER_MAX_WORDS:
        return [
            f"pointer-note: {words} words of prose around {len(links)} note "
            f"reference(s). Put the content in the note that owns the topic."
        ]
    supersede = SUPERSEDE_RE.search(prose)
    if supersede and words < POINTER_MAX_WORDS * 3:
        return [
            f"pointer-note: short note using supersession language "
            f"({supersede.group(0)!r}). Edit the original note in place instead."
        ]
    return []


def check_links(md: Path, body: str) -> list[str]:
    findings = []
    for target in MD_LINK_RE.findall(strip_code(body)):
        if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
            continue
        rel = target.split("#", 1)[0]
        if rel and not (md.parent / rel).exists():
            findings.append(f"broken-link: {target}")
    return findings


def has_index(directory: Path) -> bool:
    candidates = [directory]
    if directory.name in NOTE_DIRS:
        candidates.append(directory.parent)
    return any((d / "index.md").is_file() for d in candidates)


def lint(roots: list[Path]) -> int:
    findings: list[tuple[Path, str]] = []
    active_by_dir: dict[Path, list[Path]] = defaultdict(list)
    ids_by_owner: dict[Path, dict[str, list[Path]]] = defaultdict(lambda: defaultdict(list))
    layouts_by_owner: dict[Path, set[str]] = defaultdict(set)
    scanned = 0
    md_files = 0

    for root in roots:
        if not root.exists():
            print(f"error: {root} does not exist", file=sys.stderr)
            return 2
        files = [root] if root.is_file() else sorted(root.rglob("*.md"))
        base = root.parent if root.is_file() else root
        for path in files:
            if SKIP_DIRS.intersection(path.relative_to(base).parts[:-1]):
                continue
            md_files += 1
            try:
                body = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                findings.append((path, f"unreadable: {exc}"))
                continue
            archived = is_archived(path, base)
            if not archived:
                findings.extend((path, f) for f in check_links(path, body))
            match = NOTE_RE.match(path.name)
            if not match:
                continue
            owner = sequence_owner(path)
            ids_by_owner[owner][match.group(1)].append(path)
            if archived:
                continue
            scanned += 1
            if path.parent.name in NOTE_DIRS:
                layouts_by_owner[owner].add(path.parent.name)
            active_by_dir[path.parent].append(path)
            findings.extend((path, f) for f in check_note_body(body))

    if not md_files:
        print(
            "error: no Markdown files under " + ", ".join(str(r) for r in roots) + ". Check the path.",
            file=sys.stderr,
        )
        return 2

    for owner, ids in sorted(ids_by_owner.items()):
        for note_id, paths in sorted(ids.items()):
            if len(paths) > 1:
                names = ", ".join(str(p.relative_to(owner)) for p in sorted(paths))
                findings.append((owner, f"duplicate-id: {note_id} used by {names}. IDs are never reused; renumber the newer note."))
    for owner, layouts in sorted(layouts_by_owner.items()):
        if len(layouts) > 1:
            findings.append((owner, "mixed-layout: notes in both knowledge/ and notes/. Keep the epic's established directory and move the rest into it."))
    for directory, notes in sorted(active_by_dir.items()):
        by_stem: dict[str, list[Path]] = defaultdict(list)
        for note in notes:
            by_stem[title_stem(NOTE_RE.match(note.name).group(2))].append(note)
        for stem, paths in sorted(by_stem.items()):
            if len(paths) > 1:
                names = ", ".join(p.name for p in sorted(paths))
                findings.append((directory, f"duplicate-stem: {names} share the title stem {stem!r}. Merge them into one note."))
        if len(notes) > FLAT_PILE_THRESHOLD and not has_index(directory):
            findings.append((directory, f"flat-pile: {len(notes)} sibling notes with no index.md. Merge them, or put them under an epic with an index."))

    for location, message in findings:
        print(f"{location}: {message}")
    noun = "note" if scanned == 1 else "notes"
    summary = f"{scanned} active {noun} and {md_files} Markdown file(s) checked"
    if findings:
        print(f"\n{len(findings)} finding(s); {summary}.")
        return 1
    print(f"{summary}, no findings.")
    return 0


def main(argv: list[str]) -> int:
    args = argv[1:]
    if any(a.startswith("-") for a in args):
        print(__doc__, file=sys.stderr)
        return 2
    default = Path("_docs") if Path("_docs").exists() or not Path("docs").exists() else Path("docs")
    return lint([Path(a) for a in args] or [default])


if __name__ == "__main__":
    sys.exit(main(sys.argv))
