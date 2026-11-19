#!/usr/bin/env python3
"""Check an exploration report for the mechanically checkable rules in SKILL.md.

Usage:
    lint_report.py REPORT.md [REPORT.md ...]

Exit status is 1 when any error is reported, 0 otherwise (warnings alone
do not fail), and 2 on usage error.

Errors:
  status          missing or invalid `Status: active|concluded` line
  sections        required section missing, out of order, or empty
  tldr            TL;DR has no bullets or more than five
  scorecard       scorecard has no rows, no Status column, or an invalid status
  link            relative link or in-report anchor that does not resolve
  placeholder     template placeholder left (`TODO`, `YYYY-MM-DD`), in any status;
                  an unfinished item belongs in the Scorecard as `not run` or `blocked`

Errors in a concluded report, warnings in an active one:
  tldr-trace      TL;DR quantity that does not appear outside TL;DR and Scorecard;
                  a number with a unit (`42 GB/s`, `3.1x`, `12%`) must reappear with
                  the same unit, a bare number must reappear as a number
  tldr-tag        TL;DR bullet with a number but no evidence tag
  tldr-confidence TL;DR bullet without "Confidence:"

It cannot judge whether evidence supports a claim. Treat a clean run as the
absence of structural defects, not as proof that the report is sound.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "Scope",
    "TL;DR",
    "Scorecard",
    "Findings",
    "Caveats",
    "Anomalies",
    "Analysis",
    "Reproduce",
    "Open Questions",
    "Data Index",
    "Changelog",
]
STATUSES = {"answered", "partial", "not run", "blocked"}
MAX_TLDR_BULLETS = 5

COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
FENCE_RE = re.compile(r"^```.*?^```", re.DOTALL | re.MULTILINE)
INLINE_CODE_RE = re.compile(r"`[^`]*`")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)[^)]*\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$", re.MULTILINE)
STATUS_RE = re.compile(r"^Status:\s*(\S+)\s*$", re.MULTILINE)
NUMBER_RE = re.compile(r"(?<![\w.])\d{1,3}(?:,\d{3})+(?:\.\d+)?|(?<![\w.,])\d+(?:\.\d+)?")
# Units recognized after a number. Matching is case-sensitive (GB is not Gb).
_UNITS = (
    r"%|x|×|"
    r"[npµμum]?s|sec|min|h|hr|days?|"
    r"[KMGTP]i?B|B|[KMGT]?bit|[KMGT]b|bits?|"
    r"[KMG]?IOPS|[KMG]?ops|[KMG]?op|req|reqs|"
    r"[kKMG]?Hz|[kM]?W|[mk]?J|°C|"
    r"cores?|threads?|nodes?|GPUs?|CPUs?|servers?|clients?"
)
QUANTITY_RE = re.compile(
    r"(?<![\w.])(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)"
    r"\s?(" + _UNITS + r")(?:/(\w+))?(?![\w/])"
)
PLACEHOLDER_RE = re.compile(r"\bTODO\b|YYYY-MM-DD")
TAG_RE = re.compile(r"\[(measured|derived|estimated|(?:cited|discussion):[^\]]+)\]")


def slugify(heading: str) -> str:
    """GitHub-style heading anchor."""
    text = re.sub(r"[`*_]|\[([^\]]*)\]\([^)]*\)", r"\1", heading).strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def anchors(text: str) -> set[str]:
    seen: dict[str, int] = {}
    result = set()
    for match in HEADING_RE.finditer(text):
        slug = slugify(match.group(2))
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        result.add(slug if count == 0 else f"{slug}-{count}")
    return result


def split_sections(text: str) -> list[tuple[str, str]]:
    """Return (title, body) for each level-2 section, in order."""
    matches = [m for m in HEADING_RE.finditer(text) if len(m.group(1)) == 2]
    sections = []
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections.append((match.group(2), text[match.end():end]))
    return sections


def bullets(body: str) -> list[str]:
    return [line[2:].strip() for line in body.splitlines() if line.startswith("- ")]


def table_rows(body: str) -> list[list[str]]:
    rows = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if all(re.fullmatch(r":?-+:?", cell) for cell in cells if cell):
            continue
        rows.append(cells)
    return rows


def _number(text: str) -> float:
    return float(text.replace(",", ""))


def _quantity(match: re.Match) -> tuple[float, str, str]:
    unit = "x" if match.group(2) == "×" else match.group(2).replace("μ", "µ")
    return (_number(match.group(1)), unit, match.group(3) or "")


def lint(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    raw = path.read_text(encoding="utf-8")
    text = COMMENT_RE.sub("", raw)

    status_match = STATUS_RE.search(text)
    status = status_match.group(1) if status_match else None
    if status not in {"active", "concluded"}:
        errors.append("status: expected a line `Status: active` or `Status: concluded`")

    sections = split_sections(text)
    by_title = {title: body for title, body in sections}
    present = [title for title, _ in sections if title in REQUIRED_SECTIONS]
    for name in REQUIRED_SECTIONS:
        if name not in by_title:
            errors.append(f"sections: missing `## {name}`")
        elif not by_title[name].strip():
            errors.append(f"sections: `## {name}` is empty")
    expected_order = [name for name in REQUIRED_SECTIONS if name in present]
    if present != expected_order:
        errors.append(f"sections: out of order; expected {' → '.join(expected_order)}")

    tldr = bullets(by_title.get("TL;DR", ""))
    if "TL;DR" in by_title and not tldr:
        errors.append("tldr: no bullets")
    if len(tldr) > MAX_TLDR_BULLETS:
        errors.append(f"tldr: {len(tldr)} bullets; at most {MAX_TLDR_BULLETS}")

    if "Scorecard" in by_title:
        rows = table_rows(by_title["Scorecard"])
        header = [cell.lower() for cell in rows[0]] if rows else []
        if len(rows) < 2:
            errors.append("scorecard: table has no rows")
        elif "status" not in header:
            errors.append("scorecard: table has no Status column")
        else:
            col = header.index("status")
            for row in rows[1:]:
                value = row[col].lower() if col < len(row) else ""
                if value not in STATUSES:
                    errors.append(
                        f"scorecard: invalid status `{value}` in row `{' | '.join(row[:2])}`; "
                        f"use one of {', '.join(sorted(STATUSES))}"
                    )

    traced_body = "\n".join(
        body for title, body in sections if title not in {"TL;DR", "Scorecard"}
    )
    traced_body = TAG_RE.sub("", INLINE_CODE_RE.sub(lambda m: m.group(0).strip("`"), traced_body))
    body_quantities = {_quantity(m) for m in QUANTITY_RE.finditer(traced_body)}
    body_numbers = {_number(n) for n in NUMBER_RE.findall(traced_body)}
    tldr_issues = errors if status == "concluded" else warnings
    for bullet in tldr:
        stripped = TAG_RE.sub("", INLINE_CODE_RE.sub("", bullet))
        with_unit = {m.start(1): m for m in QUANTITY_RE.finditer(stripped)}
        reported = set()
        for match in NUMBER_RE.finditer(stripped):
            quantity = with_unit.get(match.start())
            if quantity is not None:
                key, ok = _quantity(quantity), _quantity(quantity) in body_quantities
                label = quantity.group(0)
            else:
                key, ok = _number(match.group(0)), _number(match.group(0)) in body_numbers
                label = match.group(0)
            if not ok and key not in reported:
                reported.add(key)
                tldr_issues.append(f"tldr-trace: `{label}` in TL;DR appears nowhere in the body")
        if NUMBER_RE.search(stripped) and not TAG_RE.search(bullet):
            tldr_issues.append(f"tldr-tag: no evidence tag in `{bullet[:60]}`")
        if "confidence:" not in bullet.lower():
            tldr_issues.append(f"tldr-confidence: no confidence in `{bullet[:60]}`")

    placeholder_text = INLINE_CODE_RE.sub("", FENCE_RE.sub("", text))
    placeholders = PLACEHOLDER_RE.findall(placeholder_text)
    if placeholders:
        errors.append(
            f"placeholder: {len(placeholders)} template placeholder(s) left "
            "(TODO or YYYY-MM-DD); fill them, or record unfinished items as `not run` or `blocked`"
        )

    link_text = INLINE_CODE_RE.sub("", FENCE_RE.sub("", text))
    report_anchors = anchors(text)
    for match in LINK_RE.finditer(link_text):
        target = match.group(1)
        if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
            continue
        file_part, _, anchor = target.partition("#")
        if not file_part:
            if anchor not in report_anchors:
                errors.append(f"link: anchor `#{anchor}` matches no heading")
        elif not (path.parent / file_part).exists():
            errors.append(f"link: `{file_part}` does not exist")

    return errors, warnings


def main(argv: list[str]) -> int:
    if not argv or argv[0] in {"-h", "--help"}:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    failed = False
    for arg in argv:
        path = Path(arg)
        if not path.is_file():
            print(f"{arg}: not a file", file=sys.stderr)
            return 2
        errors, warnings = lint(path)
        for message in errors:
            print(f"{arg}: error: {message}")
        for message in warnings:
            print(f"{arg}: warning: {message}")
        if not errors and not warnings:
            print(f"{arg}: clean")
        failed = failed or bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
