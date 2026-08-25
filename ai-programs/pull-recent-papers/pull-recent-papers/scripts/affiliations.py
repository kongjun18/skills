#!/usr/bin/env python3
"""Extract raw author/affiliation text for arXiv papers.

This script is deliberately *deterministic and dumb*: it fetches the paper and
returns the verbatim author block plus any email domains it finds. It does NOT
clean institution names, deduplicate, or classify academia/industry -- that is
interpretation, and it is the agent's job (read the raw text, write the clean
org name and sector).

Why we read the paper at all: the arXiv Atom API carries no affiliations, and
OpenAlex has none for fresh preprints (indexed but un-enriched for days). So we
pull them from the paper itself:

  1. https://arxiv.org/html/{id}  -- the ar5iv full-text render; its author
     block (<div class="ltx_authors">) has institutions, usually with the
     corresponding-author email domain.
  2. Fallback https://arxiv.org/pdf/{id} -- the author region of the first page
     (above the abstract) via `pdftotext`, if it is on PATH.

Usage:
    # ids on the command line
    python3 affiliations.py 2607.13604 2607.13276 ...

    # or feed fetch_arxiv.py --json on stdin (reads every arxiv_id)
    python3 fetch_arxiv.py --days 7 --json | python3 affiliations.py --from-json

    # curated subset only (skip peripheral tier)
    python3 fetch_arxiv.py --json | python3 affiliations.py --from-json --curated

Output: JSON on stdout, keyed by id:
    {id: {"block": "<raw author/affiliation text>",
          "emails": ["name@ethz.ch", ...],
          "email_domains": ["ethz.ch", ...],
          "source": "html" | "pdf" | "none"}}

The agent then reads `block` (and `email_domains` as a hint) and produces the
clean institution list + academia/industry/both tag for the digest.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request

HTML_URL = "https://arxiv.org/html/{id}"
PDF_URL = "https://arxiv.org/pdf/{id}"
UA = "pull-recent-papers-affil/1.0"

EMAIL_RE = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")


def fetch(url: str, timeout: int = 30) -> bytes | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except Exception:
        return None


def author_block_html(page: bytes) -> str:
    """Return the plain-text ar5iv author block, or ''."""
    t = page.decode("utf-8", "ignore")
    # drop scripts/styles so the tag-strip doesn't slurp JS/CSS
    t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", t)
    m = re.search(r'(?is)<div class="ltx_authors".*?</div>\s*(?:</div>)?', t)
    if not m:
        return ""
    txt = re.sub(r"(?is)<[^>]+>", " ", m.group(0))
    return html.unescape(re.sub(r"\s+", " ", txt)).strip()


def pdf_author_region(raw: bytes) -> str:
    """Return the author region of the PDF first page (title..abstract).

    Institutions sit between the title and the abstract; the body below often
    name-drops companies, which would pollute the affiliation text, so we cut
    at the first section marker.
    """
    if not shutil.which("pdftotext"):
        return ""
    with tempfile.NamedTemporaryFile(suffix=".pdf") as fh:
        fh.write(raw)
        fh.flush()
        try:
            out = subprocess.run(
                ["pdftotext", "-f", "1", "-l", "1", fh.name, "-"],
                capture_output=True, timeout=30,
            )
            text = out.stdout.decode("utf-8", "ignore")
        except Exception:
            return ""
    cut = re.search(
        r"(?im)^\s*(abstract|introduction|1[.\s]+introduction|ccs concepts|keywords)\b",
        text,
    )
    region = text[:cut.start()] if cut else text[:1200]
    return re.sub(r"[ \t]+", " ", region).strip()


def emails_of(text: str) -> tuple[list[str], list[str]]:
    emails: list[str] = []
    for m in EMAIL_RE.finditer(text):
        e = m.group(0)
        if e not in emails:
            emails.append(e)
    domains: list[str] = []
    for e in emails:
        d = e.split("@", 1)[1].lower()
        if d not in domains:
            domains.append(d)
    return emails, domains


def lookup(arxiv_id: str) -> dict:
    """Resolve one id (version suffix tolerated) to raw block + emails + source."""
    bare = arxiv_id.split("v")[0]

    page = fetch(HTML_URL.format(id=bare))
    if page and len(page) > 9000:  # 404 stubs are ~8 KB
        block = author_block_html(page)
        if block:
            emails, domains = emails_of(block)
            return {"block": block, "emails": emails,
                    "email_domains": domains, "source": "html"}

    pdf = fetch(PDF_URL.format(id=bare))
    if pdf:
        block = pdf_author_region(pdf)
        if block:
            emails, domains = emails_of(block)
            return {"block": block, "emails": emails,
                    "email_domains": domains, "source": "pdf"}

    return {"block": "", "emails": [], "email_domains": [], "source": "none"}


def read_ids(args) -> list[str]:
    if args.from_json:
        data = json.load(sys.stdin)
        papers = data["papers"] if isinstance(data, dict) else data
        if args.curated:
            papers = [p for p in papers if p.get("priority") != "peripheral"]
        return [p["arxiv_id"] for p in papers]
    return args.ids


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ids", nargs="*", help="arXiv ids (e.g. 2607.13604)")
    ap.add_argument("--from-json", action="store_true",
                    help="read ids from fetch_arxiv.py --json on stdin")
    ap.add_argument("--curated", action="store_true",
                    help="with --from-json, skip peripheral-tier papers")
    ap.add_argument("--delay", type=float, default=1.5,
                    help="seconds between fetches to avoid HTTP 429 (default 1.5)")
    args = ap.parse_args()

    ids = read_ids(args)
    if not ids:
        ap.error("no ids given (pass ids or --from-json)")

    result: dict[str, dict] = {}
    for i, aid in enumerate(ids):
        result[aid] = lookup(aid)
        doms = ", ".join(result[aid]["email_domains"]) or "(no emails)"
        print(f"{aid}: {result[aid]['source']:4}  {doms}", file=sys.stderr)
        if i < len(ids) - 1:
            time.sleep(args.delay)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
