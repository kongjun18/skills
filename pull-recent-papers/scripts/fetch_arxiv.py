#!/usr/bin/env python3
"""Fetch recent arXiv papers and group them by a configurable topic taxonomy.

Queries the arXiv Atom API for the configured categories, filters to a recent
time window, tags each paper with the first matching topic, and prints a
Markdown digest ordered by tier, then topic.

Categories, tiers, topics, and window defaults come from a TOML config:
`--config PATH`, else the user config at
`${XDG_CONFIG_HOME:-~/.config}/agent-skills/pull-recent-papers/config.toml`,
else the bundled `assets/default-config.toml` (a storage-systems taxonomy).

The reader context file is resolved as `[reader] context_file` (default
`context.md`, relative to the config directory) if it exists, else the
user-profile skill's `agent-skills/user-profile/profile.md` if it exists, else
none.

Usage:
    python3 fetch_arxiv.py [--config PATH] [--days N | --since TIME] [--max-per-cat N] [--json]

Notes:
    * Uses only the Python standard library (urllib, xml, tomllib; 3.11+).
    * arXiv's API requires HTTPS; http:// returns a 301 redirect.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import tomllib
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from itertools import groupby
from pathlib import Path

API = "https://export.arxiv.org/api/query"
NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

AGENT_SKILLS = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config") / "agent-skills"
USER_CONFIG = AGENT_SKILLS / "pull-recent-papers" / "config.toml"
# Optional personal profile owned by the separate user-profile skill; read only
# if present, never required.
USER_PROFILE = AGENT_SKILLS / "user-profile" / "profile.md"
DEFAULT_CONFIG = Path(__file__).resolve().parent.parent / "assets" / "default-config.toml"


def resolve_config_path(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit)
    return USER_CONFIG if USER_CONFIG.exists() else DEFAULT_CONFIG


def load_config(path: Path) -> dict:
    """Load and validate the config; exit with a clear message if malformed."""
    with open(path, "rb") as f:
        cfg = tomllib.load(f)
    digest = cfg.get("digest", {})
    tiers = cfg.get("tiers", [])
    topics = cfg.get("topics", [])
    if not digest.get("categories"):
        raise SystemExit(f"{path}: [digest] categories must be a non-empty list")
    strict = digest.get("strict_categories", {})
    labels = {t.get("label") for t in topics}
    for cat, allowed in strict.items():
        if cat not in digest["categories"]:
            raise SystemExit(f"{path}: strict category {cat!r} is not in categories")
        if unknown := set(allowed) - labels:
            raise SystemExit(f"{path}: strict category {cat!r} names unknown topics {sorted(unknown)}")
    tier_ids = [t["id"] for t in tiers]
    catch_all = [t["id"] for t in tiers if t.get("catch_all")]
    if len(catch_all) != 1:
        raise SystemExit(f"{path}: exactly one [[tiers]] entry must set catch_all = true")
    for t in topics:
        if t.get("tier") not in tier_ids:
            raise SystemExit(f"{path}: topic {t.get('label')!r} has unknown tier {t.get('tier')!r}")
        if t.get("tier") == catch_all[0]:
            raise SystemExit(f"{path}: topic {t.get('label')!r} is in the catch-all tier; "
                             "unmatched papers land there automatically")
        for pat in t.get("patterns", []) + t.get("exclude", []):
            try:
                re.compile(pat)
            except re.error as exc:
                raise SystemExit(f"{path}: topic {t.get('label')!r} has bad pattern {pat!r}: {exc}")
    cfg["_catch_all"] = next(t for t in tiers if t.get("catch_all"))
    # context_file is relative to the config file's directory, so the user's
    # context sits next to their config regardless of the working directory.
    # The bundled default points into the user config directory instead.
    base = USER_CONFIG.parent if path.resolve() == DEFAULT_CONFIG else path.resolve().parent
    own = base / cfg.get("reader", {}).get("context_file", "context.md")
    cfg["_own_context"] = own
    cfg["_context_path"] = own if own.exists() else USER_PROFILE if USER_PROFILE.exists() else None
    return cfg


def show_config(path: Path, cfg: dict) -> None:
    """Print a short human-readable summary of the resolved config."""
    digest, reader = cfg["digest"], cfg.get("reader", {})
    print(f"config:     {path}" + ("  (bundled default)" if path == DEFAULT_CONFIG else ""))
    print(f"user path:  {USER_CONFIG}" + ("" if USER_CONFIG.exists() else "  (missing: first launch)"))
    print(f"title:      {digest.get('title', 'arXiv Digest')}")
    print(f"field:      {digest.get('field', '(unset)')}")
    print(f"categories: {', '.join(digest['categories'])}")
    for cat, allowed in digest.get("strict_categories", {}).items():
        print(f"strict:     {cat} kept only for: {', '.join(allowed)}")
    print(f"window:     {digest.get('days', 7)} days, max {digest.get('max_results', 200)} results")
    ctx, own = cfg["_context_path"], cfg["_own_context"]
    if ctx == USER_PROFILE:
        print(f"context:    {ctx}  (user profile; {own} missing)")
    elif ctx:
        print(f"context:    {ctx}")
    else:
        print(f"context:    (none; {own} and {USER_PROFILE} missing)")
    interests = '; '.join(reader.get('interests', [])) or '(none)'
    if ctx and reader.get('interests'):
        interests = f"(ignored: the reader context is the source of interests) {interests}"
    print(f"interests:  {interests}")
    print(f"authors:    {'; '.join(reader.get('author_names', [])) or '(none)'}")
    prefs = cfg.get("ranking", {}).get("preferences", [])
    print(f"ranking:    {'; '.join(prefs) or '(none)'}")
    print("tiers (priority order):")
    for t in cfg["tiers"]:
        labels = [x["label"] for x in cfg.get("topics", []) if x["tier"] == t["id"]]
        tail = "catch-all for unmatched papers" if t.get("catch_all") else ", ".join(labels)
        print(f"  {t['id']}: {t['title']} -- {tail}")


PAGE_SIZE = 1000   # arXiv caps a single response at 2000; smaller pages are more reliable
PAGE_DELAY = 3.0   # seconds between pages, per arXiv API etiquette


def build_query(categories: list[str], max_per_cat: int, start: int = 0) -> str:
    cat_expr = "+OR+".join(f"cat:{c}" for c in categories)
    params = (
        f"search_query=({cat_expr})"
        f"&start={start}&max_results={max_per_cat}"
        f"&sortBy=submittedDate&sortOrder=descending"
    )
    return f"{API}?{params}"


def fetch_window(categories: list[str], max_results: int, since: datetime) -> list[dict]:
    """Page through results (newest first) until `max_results` or past `since`."""
    entries: list[dict] = []
    while len(entries) < max_results:
        size = min(PAGE_SIZE, max_results - len(entries))
        page = parse_entries(fetch(build_query(categories, size, start=len(entries))))
        entries.extend(page)
        dates = [d for d in map(published_at, page) if d]
        if len(page) < size or (dates and min(dates) < since):
            break
        time.sleep(PAGE_DELAY)
    return entries


def fetch(url: str, retries: int = 3) -> bytes:
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "pull-recent-papers/1.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read()
        except Exception as exc:  # noqa: BLE001 - surface after retries
            last = exc
            time.sleep(2 * (attempt + 1))
    raise SystemExit(f"arXiv API request failed after {retries} tries: {last}")


def parse_entries(xml_bytes: bytes) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    out = []
    for e in root.findall("a:entry", NS):
        def text(tag):
            node = e.find(f"a:{tag}", NS)
            return (node.text or "").strip() if node is not None else ""

        entry_id = text("id")
        prim = e.find("arxiv:primary_category", NS)
        authors = []
        for a in e.findall("a:author", NS):
            name = a.find("a:name", NS)
            if name is not None and name.text:
                authors.append(name.text)
        out.append({
            "id": entry_id,
            "arxiv_id": entry_id.rsplit("/", 1)[-1],
            "title": re.sub(r"\s+", " ", text("title")),
            "summary": re.sub(r"\s+", " ", text("summary")),
            "published": text("published"),
            "updated": text("updated"),
            "authors": authors,
            "primary_category": prim.get("term") if prim is not None else "",
            "categories": [c.get("term") for c in e.findall("a:category", NS)],
        })
    return out


def classify(entry: dict, cfg: dict) -> tuple[str, str]:
    """Return (topic_label, tier_id) for the first matching topic.

    A topic's `exclude` patterns veto it (the paper falls through to later
    topics). Papers that match no topic fall into the catch-all tier, labeled
    with that tier's title, so nothing in-category is silently dropped.
    """
    hay = f"{entry['title']} {entry['summary']}"

    def hit(patterns: list[str]) -> bool:
        return any(re.search(p, hay, flags=re.IGNORECASE) for p in patterns)

    for topic in cfg.get("topics", []):
        if hit(topic.get("patterns", [])) and not hit(topic.get("exclude", [])):
            return topic["label"], topic["tier"]
    fallback = cfg["_catch_all"]
    return fallback["title"], fallback["id"]


def published_at(entry: dict) -> datetime | None:
    try:
        return datetime.strptime(entry["published"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def within_window(entry: dict, start: datetime, end: datetime) -> bool:
    pub = published_at(entry)
    return pub is not None and start <= pub < end


def parse_since(text: str) -> datetime:
    """Parse an ISO date or datetime; naive values are taken as UTC."""
    try:
        when = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        raise SystemExit(f"--since: not an ISO date/datetime: {text!r}")
    return when if when.tzinfo else when.replace(tzinfo=timezone.utc)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", help=f"TOML config (default: {USER_CONFIG}, "
                                     "else the bundled default)")
    ap.add_argument("--show-config", action="store_true",
                    help="validate and summarize the resolved config, then exit (no fetch)")
    window = ap.add_mutually_exclusive_group()
    window.add_argument("--days", type=int, help="look-back window in days (default: config, 7)")
    window.add_argument("--since", help="window start as an ISO date/datetime (UTC if no "
                                        "offset), e.g. the previous digest's window end")
    ap.add_argument("--max-per-cat", type=int,
                    help="max results to pull from the combined query (default: config, 200)")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of Markdown")
    ap.add_argument("--curated-json", action="store_true",
                    help="like --json, but strip catch-all-tier papers' abstracts "
                         "(keeps their title/id/topic) so evaluation ingests full "
                         "abstracts only for papers it will judge — a token saver")
    args = ap.parse_args()

    config_path = resolve_config_path(args.config)
    cfg = load_config(config_path)
    if args.show_config:
        show_config(config_path, cfg)
        return 0
    print(f"config: {config_path}", file=sys.stderr)
    digest = cfg["digest"]
    categories = digest["categories"]
    strict = digest.get("strict_categories", {})
    max_results = args.max_per_cat or digest.get("max_results", 200)

    end = datetime.now(timezone.utc).replace(microsecond=0)
    if args.since:
        start = parse_since(args.since)
        if start >= end:
            raise SystemExit(f"--since {args.since} is not in the past")
    else:
        start = end - timedelta(days=args.days or digest.get("days", 7))
    entries = fetch_window(categories, max_results, start)

    # Truncation check: results come newest first, so if the query returned its
    # full quota and even the oldest raw entry is inside the window, older
    # in-window papers were cut off.
    dates = [d for d in map(published_at, entries) if d]
    oldest_raw = min(dates) if dates else None
    truncated = len(entries) >= max_results and oldest_raw is not None and oldest_raw >= start
    print(f"raw: {len(entries)} entries (cap {max_results}), oldest "
          f"{oldest_raw.isoformat() if oldest_raw else 'n/a'}; window {start.isoformat()} -> "
          f"{end.isoformat()}", file=sys.stderr)
    if truncated:
        print("WARNING: window truncated; raise max_results / --max-per-cat", file=sys.stderr)

    # Dedup by arxiv_id, filter to window, classify.
    seen: set[str] = set()
    matched: list[dict] = []
    for e in entries:
        if e["arxiv_id"] in seen:
            continue
        seen.add(e["arxiv_id"])
        if not within_window(e, start, end):
            continue
        # Gate: the paper must be *primarily* in a configured category, not a
        # paper from another field that merely cross-lists here.
        if e["primary_category"] not in categories:
            continue
        e["topic"], e["priority"] = classify(e, cfg)
        e["skim"] = e["priority"] == cfg["_catch_all"]["id"]
        # Strict categories are high-volume neighbors pulled only for a few
        # topics; anything else from them would flood the digest.
        if e["primary_category"] in strict and e["topic"] not in strict[e["primary_category"]]:
            continue
        matched.append(e)

    # Order by priority tier, then topic order from the config, then newest first.
    # (Stable sorts applied inner-key first: date desc, then group key.)
    tier_index = {t["id"]: i for i, t in enumerate(cfg["tiers"])}
    topic_index = {t["label"]: i for i, t in enumerate(cfg.get("topics", []))}
    matched.sort(key=lambda e: e["published"], reverse=True)
    matched.sort(key=lambda e: (tier_index[e["priority"]], topic_index.get(e["topic"], len(topic_index))))

    if args.json or args.curated_json:
        papers = matched
        if args.curated_json:
            # Catch-all papers render terse (no abstract) downstream, so their
            # full summary is dead weight in the agent's context. Drop it while
            # keeping the fields the terse skim list still needs.
            papers = [
                {k: v for k, v in p.items() if not (p["skim"] and k == "summary")}
                for p in matched
            ]
        print(json.dumps({"config": str(config_path),
                          "context_file": str(cfg["_context_path"] or ""),
                          "window": {"start": start.isoformat(), "end": end.isoformat()},
                          "cutoff": start.isoformat(),
                          "raw_count": len(entries),
                          "oldest_raw": oldest_raw.isoformat() if oldest_raw else None,
                          "truncated": truncated,
                          "count": len(matched), "papers": papers},
                         indent=2, ensure_ascii=False))
        return 0

    render_markdown(matched, start, end, truncated, cfg)
    return 0


def render_markdown(matched: list[dict], start: datetime, end: datetime,
                    truncated: bool, cfg: dict) -> None:
    digest = cfg["digest"]
    tier_titles = {t["id"]: t["title"] for t in cfg["tiers"]}
    print(f"# {digest.get('title', 'arXiv Digest')} — {start:%Y-%m-%d} to {end:%Y-%m-%d}")
    print(f"_Window: {start:%Y-%m-%dT%H:%MZ} → {end:%Y-%m-%dT%H:%MZ} · {len(matched)} papers · "
          f"categories: {', '.join(digest['categories'])}_\n")
    if truncated:
        print("**Warning: window truncated — raise `max_results`.**\n")

    if not matched:
        print("No matching papers in this window.")
        return

    # `matched` is already ordered by (tier, topic, newest-first), so groupby
    # over topic yields contiguous, correctly-ordered sections. The catch-all
    # tier renders terse (title + one-line meta, no abstract) so it stays
    # skimmable without crowding the relevant sections above it.
    last_tier = None
    for topic, group in groupby(matched, key=lambda e: e["topic"]):
        papers = list(group)
        tier = papers[0]["priority"]
        skim = papers[0]["skim"]
        if tier != last_tier:
            print(f"\n## {tier_titles[tier]}\n")
            last_tier = tier
        print(f"### {topic}  ({len(papers)})\n")
        for p in papers:
            authors = ", ".join(p["authors"][:4]) + (" et al." if len(p["authors"]) > 4 else "")
            date = p["published"][:10]
            cats = ", ".join(p["categories"][:3])
            if skim:
                print(f"- [{p['title']}]({p['id']}) · {date} · `{cats}` · arXiv:{p['arxiv_id']}")
                continue
            abstract = p["summary"]
            if len(abstract) > 500:
                abstract = abstract[:500].rsplit(" ", 1)[0] + "…"
            print(f"- **[{p['title']}]({p['id']})**  ")
            print(f"  {authors} · {date} · `{cats}` · arXiv:{p['arxiv_id']}  ")
            print(f"  {abstract}\n")
        if skim:
            print()


if __name__ == "__main__":
    sys.exit(main())
