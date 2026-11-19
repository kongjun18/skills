#!/usr/bin/env python3
"""Check the skills repository against the rules in AGENTS.md.

Errors (exit 1):
  - SKILL.md frontmatter missing, unparsable, or `name` != directory name
  - empty or over-long `description`
  - relative Markdown link that does not resolve
  - AGENTS.md "Maintained Skills" out of sync with the skill directories
  - an installed symlink that points into this repository at a directory
    without SKILL.md

Warnings:
  - SKILL.md longer than the line budget (default 300)
  - a maintained skill not installed in a harness skills directory
  - an installed third-party skill whose clone is not pinned in
    third-party/SOURCES.md

Usage: python3 tools/check.py [--max-lines N] [--no-installs]
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HARNESS_DIRS = [Path.home() / ".claude" / "skills", Path.home() / ".codex" / "skills"]
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def main_checkout() -> Path:
    """The main worktree root; install symlinks point there, not at linked worktrees."""
    try:
        out = subprocess.run(
            ["git", "-C", str(REPO), "worktree", "list", "--porcelain"],
            capture_output=True, text=True, check=True,
        ).stdout
        return Path(out.splitlines()[0].removeprefix("worktree ")).resolve()
    except (subprocess.CalledProcessError, IndexError, FileNotFoundError):
        return REPO


def skill_dirs() -> list[Path]:
    return sorted(p.parent for p in REPO.glob("*/SKILL.md"))


def frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        return None
    fields: dict[str, str] = {}
    key = None
    for line in text[4:end].splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            key, value = m.group(1), m.group(2).strip()
            if re.fullmatch(r"[>|][+-]?", value):  # YAML block scalar: value on indented lines
                fields[key] = ""
            else:
                fields[key] = value.strip('"').strip("'")
                key = None
        elif key and line.startswith((" ", "\t")):
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields


def strip_code(text: str) -> str:
    """Drop fenced code blocks and inline code so example links are not checked."""
    text = re.sub(r"^```.*?^```", "", text, flags=re.S | re.M)
    return re.sub(r"`[^`\n]*`", "", text)


def check_links(md: Path, errors: list[str]) -> None:
    for target in LINK_RE.findall(strip_code(md.read_text(encoding="utf-8"))):
        if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
            continue
        path = target.split("#", 1)[0]
        if path and not (md.parent / path).exists():
            errors.append(f"{md.relative_to(REPO)}: broken link -> {target}")


def maintained_in_agents() -> set[str]:
    text = (REPO / "AGENTS.md").read_text(encoding="utf-8")
    m = re.search(r"^## Maintained Skills\n(.*?)^## ", text, flags=re.S | re.M)
    return set(re.findall(r"^- `([a-z0-9-]+)`", m.group(1), flags=re.M)) if m else set()


def check_installs(skills: list[str], errors: list[str], warnings: list[str]) -> None:
    root = main_checkout()
    sources = REPO / "third-party" / "SOURCES.md"
    pinned = sources.read_text(encoding="utf-8") if sources.exists() else ""
    for hdir in HARNESS_DIRS:
        if not hdir.is_dir():
            continue
        installed = set()
        for entry in sorted(hdir.iterdir()):
            if not entry.is_symlink():
                continue
            target = Path(os.path.realpath(entry))
            if root not in target.parents:
                continue
            installed.add(entry.name)
            if not (target / "SKILL.md").is_file():
                errors.append(f"{entry}: points at {target}, which has no SKILL.md")
                continue
            rel = target.relative_to(root)
            if rel.parts[0] == "third-party" and f"`{rel.parts[1]}`" not in pinned:
                warnings.append(f"{entry}: third-party clone {rel.parts[1]} not pinned in third-party/SOURCES.md")
        for name in skills:
            if name not in installed:
                warnings.append(f"{hdir}: {name} not installed (run tools/install.sh)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--max-lines", type=int, default=300)
    ap.add_argument("--no-installs", action="store_true", help="skip harness symlink checks")
    args = ap.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    dirs = skill_dirs()
    names = [d.name for d in dirs]

    for d in dirs:
        skill_md = d / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8")
        fm = frontmatter(text)
        if fm is None:
            errors.append(f"{d.name}/SKILL.md: missing or unterminated frontmatter")
        else:
            if fm.get("name") != d.name:
                errors.append(f"{d.name}/SKILL.md: name {fm.get('name')!r} != directory {d.name!r}")
            if not NAME_RE.match(d.name) or len(d.name) > 64:
                errors.append(f"{d.name}: directory name is not short kebab-case")
            desc = fm.get("description", "")
            if not desc:
                errors.append(f"{d.name}/SKILL.md: empty description")
            elif len(desc) > 1024:
                errors.append(f"{d.name}/SKILL.md: description is {len(desc)} chars (max 1024)")
        lines = text.count("\n") + 1
        if lines > args.max_lines:
            warnings.append(f"{d.name}/SKILL.md: {lines} lines (budget {args.max_lines})")
        for md in d.rglob("*.md"):
            check_links(md, errors)

    check_links(REPO / "AGENTS.md", errors)
    listed = maintained_in_agents()
    for name in sorted(set(names) - listed):
        errors.append(f"AGENTS.md: skill {name} missing from Maintained Skills")
    for name in sorted(listed - set(names)):
        errors.append(f"AGENTS.md: lists {name}, which has no SKILL.md")

    if not args.no_installs:
        check_installs(names, errors, warnings)

    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    print(f"{len(dirs)} skills, {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
