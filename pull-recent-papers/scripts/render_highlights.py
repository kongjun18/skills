#!/usr/bin/env python3
"""Render the highlighted papers of a curated digest (JSON) as Markdown.

Deterministic like render_html.py: it reads the digest JSON the agent wrote and
joins each `highlights.items` entry (matched by URL) with its paper card in
`rings` for authors, affiliation, sector, date, category, topic, and takeaway.
The first highlight is the "if you read one thing" pick.

Usage:
    python3 render_highlights.py DIR/digest-YYYY-Www.json --out-dir DIR   # -> DIR/digest-YYYY-Www-highlights.md
    python3 render_highlights.py digest.json -o out.md
    cat digest.json | python3 render_highlights.py                       # -> stdout

Outputs belong in the user's digest directory, never inside the skills
repository; the script refuses such an output path.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

LEAD_PREFIX = re.compile(r"^\s*if you read one thing[.:\s-]*", re.IGNORECASE)
TAGS = re.compile(r"<[^>]+>")


def plain(text: str) -> str:
    """Strip inline HTML the review prose may carry."""
    return TAGS.sub("", text or "").strip()


def paper_index(d: dict) -> dict[str, tuple[dict, str]]:
    index = {}
    for ring in d.get("rings", []):
        for topic in ring.get("topics", []):
            for paper in topic.get("papers", []):
                index[paper.get("url", "")] = (paper, topic.get("title", ""))
    return index


def render_item(item: dict, index: dict, heading: str) -> list[str]:
    paper, topic = index.get(item.get("url", ""), ({}, ""))
    why = LEAD_PREFIX.sub("", plain(item.get("why", "")))
    out = [f"### {heading}[{item.get('title', '')}]({item.get('url', '')})", ""]
    if why:
        out += [f"**Why:** {why}", ""]
    meta = []
    if paper.get("authors"):
        meta.append(f"- **Authors:** {paper['authors']}")
    if paper.get("affiliation"):
        sector = f" ({paper['sector']})" if paper.get("sector") else ""
        meta.append(f"- **Affiliation:** {paper['affiliation']}{sector}")
    ident = " · ".join(x for x in [
        f"arXiv:{paper['arxiv_id']}" if paper.get("arxiv_id") else "",
        paper.get("primary_category", ""), paper.get("date", ""), topic] if x)
    if ident:
        meta.append(f"- **Paper:** {ident}")
    if paper.get("takeaway"):
        meta.append(f"- **Takeaway:** {plain(paper['takeaway'])}")
    return out + meta + [""]


def render(d: dict) -> str:
    items = d.get("highlights", {}).get("items", [])
    index = paper_index(d)
    title = d.get("title", "arXiv Digest")
    out = [f"# {title} — highlights", ""]
    if d.get("subtitle"):
        out += [f"_{d['subtitle']}_", ""]
    if not items:
        return "\n".join(out + ["No highlights this window.", ""])
    out += ["## If you read one thing", ""]
    out += render_item(items[0], index, "")
    if len(items) > 1:
        out += ["## More highlights", ""]
        for n, item in enumerate(items[1:], start=2):
            out += render_item(item, index, f"{n}. ")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", nargs="?", help="digest JSON path (default: stdin)")
    ap.add_argument("-o", "--output", help="write Markdown here (default: stdout)")
    ap.add_argument("--out-dir", help="write <input-stem>-highlights.md into this directory")
    args = ap.parse_args()
    if args.out_dir:
        if not args.input:
            ap.error("--out-dir needs an input path to name the output")
        args.output = str(Path(args.out_dir).expanduser() / (Path(args.input).stem + "-highlights.md"))
    if args.output:
        repo = Path(__file__).resolve().parents[2]
        target = Path(args.output).expanduser().resolve()
        if repo in target.parents:
            ap.error(f"refusing to write inside the skills repository ({repo}); "
                     "write to the digest directory instead")

    data = json.load(open(args.input) if args.input else sys.stdin)
    out = render(data)
    if args.output:
        with open(args.output, "w") as f:
            f.write(out)
        print(f"wrote {args.output}: {len(out)} bytes", file=sys.stderr)
    else:
        sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
