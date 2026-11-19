#!/usr/bin/env python3
"""Fetch recent arXiv system papers and group them by topic priority.

Queries the arXiv Atom API for the relevant CS categories, filters to a
recent time window, tags each paper against a storage-proximity taxonomy, and
prints a Markdown digest ordered by ring: core storage -> storage-facing
adjacent -> peripheral.

Usage:
    python3 fetch_arxiv.py [--days N] [--max-per-cat N] [--json]

Notes:
    * Uses only the Python standard library (urllib, xml) -- no deps.
    * arXiv's API requires HTTPS; http:// returns a 301 redirect.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from itertools import groupby

API = "https://export.arxiv.org/api/query"
NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

# arXiv categories that carry storage/systems work.
CATEGORIES = ["cs.DB", "cs.OS", "cs.DC", "cs.AR", "cs.PF"]

# Topic taxonomy, organized as three "rings" of storage-proximity for a
# storage researcher (the primary field is storage; adjacent fields matter to
# the degree they touch storage / data / memory movement):
#
#   core       (Ring 1) -- the primary field: core storage
#   adjacent   (Ring 2) -- adjacent fields, storage-facing slice
#   peripheral (Ring 3) -- in-category systems papers with no storage angle
#
# Order matters: the first matching topic wins, so more specific / more
# storage-central topics are listed first. Each topic has a tier (for section
# ordering) and keyword patterns matched against title+abstract
# (case-insensitive, word-ish boundaries where useful). Ring 3 is a catch-all
# so nothing in the target categories vanishes silently -- the agent then
# curates the peripheral list down.
TOPICS = [
    # ==== Ring 1: Core storage ====
    ("I/O layer & OS storage stack", "core", [
        r"io_uring", r"block (device|layer)", r"page cache",
        r"file ?system", r"\bNVMe\b", r"\bSSD\b", r"\bflash\b", r"\bFTL\b",
        r"\bZNS\b", r"\bSMR\b", r"\bext4\b", r"\bXFS\b", r"\bF2FS\b",
        r"\bI/?O (stack|path|scheduler|layer)", r"direct I/?O",
    ]),
    ("Memory & disaggregation", "core", [
        r"\bCXL\b", r"persistent memory", r"\bPMEM\b", r"\bNVM\b",
        r"memory disaggregat", r"disaggregated memory", r"far memory",
        r"tiered memory", r"memory tiering", r"byte[\s-]?addressable",
    ]),
    ("Storage systems", "core", [
        r"\bstorage\b", r"object storage", r"key[\s-]?value store", r"\bKV store\b",
        r"\bRDMA\b", r"deduplicat", r"erasure cod", r"\bRAID\b",
        r"disaggregat", r"tiered storage", r"distributed storage",
        r"caching", r"cache (system|hierarchy|coherence)",
        r"storage (encryption|security)", r"storage energy", r"storage carbon",
    ]),
    ("Distributed storage & consistency", "core", [
        r"replicat", r"consensus", r"\bRaft\b", r"\bPaxos\b", r"quorum",
        r"linearizab", r"distributed transaction", r"atomic commit", r"\b2PC\b",
        r"sharding", r"partition(ing|ed) (data|store|table)",
        r"consistency (model|protocol)",
    ]),
    ("DB storage engine", "core", [
        r"storage engine", r"buffer (pool|manager|management)",
        r"\bB[\+\-]?tree", r"LSM[\s-]?tree", r"\bWAL\b", r"write[\s-]?ahead log",
        r"on[\s-]?disk index", r"columnar", r"data warehouse",
        r"\bParquet\b", r"\bIceberg\b", r"lakehouse", r"data (lake|format)",
        r"checkpoint", r"recovery (log|manager)",
    ]),
    ("Storage for AI", "core", [
        r"kv[\s-]?cache", r"kvcache", r"key[\s-]?value cache", r"attention cache",
        r"cache offload", r"prefix cach", r"paged attention",
        r"model (checkpoint|loading)", r"checkpoint(ing)? .*(train|LLM|model)",
        r"\bRAG\b", r"vector (store|storage|database|index)",
        r"llm (memory|storage)",
    ]),

    # ==== Ring 2: Storage-facing adjacent ====
    ("Databases (query/txn)", "adjacent", [
        r"\bdatabase", r"\bdbms\b", r"\bOLAP\b", r"\bOLTP\b",
        r"\bquery (optimiz|processing|engine|plan|execution)", r"\bSQL\b",
        r"transaction", r"\bindex(ing|es)?\b", r"vector search",
        r"join (order|algorithm)", r"cardinality estimat",
    ]),
    ("Distributed data processing", "adjacent", [
        r"map[\s-]?reduce", r"\bSpark\b", r"dataflow", r"stream processing",
        r"batch processing", r"data (pipeline|processing) (system|framework)",
        r"coordination service", r"\bZooKeeper\b", r"distributed (query|join|compute)",
    ]),
    ("LLM inference systems", "adjacent", [
        r"llm (serving|inference)", r"\bvLLM\b", r"continuous batching",
        r"(request|inference|token) schedul", r"speculative decod",
        r"disaggregated (prefill|inference)", r"serving (system|engine)",
        r"quantiz", r"model parallel",
    ]),
    ("Cloud, storage-facing", "adjacent", [
        r"cloud storage", r"\bS3\b", r"serverless.*(state|storage|data)",
        r"stateful (serverless|function)", r"datacenter (storage|memory)",
        r"multi[\s-]?tenant (storage|database)", r"\bFaaS\b.*(state|storage)",
    ]),
    ("OS, storage-facing", "adjacent", [
        r"memory management", r"paging", r"page (fault|table|migration)",
        r"swap", r"virtual memory", r"memory virtualization",
        r"storage virtualization", r"\bNUMA\b",
    ]),

    # ==== Ring 3: Peripheral (catch-all; see classify()) ====
    ("Peripheral", "peripheral", [r".*"]),
]

PRIORITY_ORDER = {"core": 0, "adjacent": 1, "peripheral": 2}
SECTION_TITLES = {
    "core": "Core storage",
    "adjacent": "Storage-facing adjacent",
    "peripheral": "Peripheral (skim only)",
}


def build_query(max_per_cat: int) -> str:
    cat_expr = "+OR+".join(f"cat:{c}" for c in CATEGORIES)
    params = (
        f"search_query=({cat_expr})"
        f"&start=0&max_results={max_per_cat}"
        f"&sortBy=submittedDate&sortOrder=descending"
    )
    return f"{API}?{params}"


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


def classify(entry: dict) -> tuple[str, str]:
    """Return (topic_label, tier) for the first matching topic.

    The final "Peripheral" topic is a catch-all (pattern ".*"), so every
    in-category paper is classified -- nothing is silently dropped. Storage
    signals are checked against title+abstract; keywords that need visible
    context (e.g. bare "storage") stay word-bounded in TOPICS.
    """
    hay = f"{entry['title']} {entry['summary']}".lower()
    for label, tier, patterns in TOPICS:
        for pat in patterns:
            if re.search(pat, hay, flags=re.IGNORECASE):
                return label, tier
    return "Peripheral", "peripheral"


def within_window(entry: dict, cutoff: datetime) -> bool:
    try:
        pub = datetime.strptime(entry["published"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return False
    return pub >= cutoff


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--days", type=int, default=7, help="look-back window in days (default 7)")
    ap.add_argument("--max-per-cat", type=int, default=200,
                    help="max results to pull from the combined query (default 200)")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of Markdown")
    ap.add_argument("--curated-json", action="store_true",
                    help="like --json, but strip peripheral papers' abstracts "
                         "(keeps their title/id/topic) so evaluation ingests full "
                         "abstracts only for papers it will judge — a token saver")
    args = ap.parse_args()

    cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
    url = build_query(args.max_per_cat)
    entries = parse_entries(fetch(url))

    # Dedup by arxiv_id, filter to window, classify.
    seen: set[str] = set()
    matched: list[dict] = []
    for e in entries:
        if e["arxiv_id"] in seen:
            continue
        seen.add(e["arxiv_id"])
        if not within_window(e, cutoff):
            continue
        # Gate: the paper must be *primarily* a systems/storage paper, not an
        # ML/domain paper that merely cross-lists here or mentions a keyword.
        if e["primary_category"] not in CATEGORIES:
            continue
        e["topic"], e["priority"] = classify(e)
        matched.append(e)

    # Order by priority tier, then topic order within TOPICS, then newest first.
    # (Stable sorts applied inner-key first: date desc, then group key.)
    topic_index = {label: i for i, (label, _, _) in enumerate(TOPICS)}
    matched.sort(key=lambda e: e["published"], reverse=True)
    matched.sort(key=lambda e: (PRIORITY_ORDER[e["priority"]], topic_index[e["topic"]]))

    if args.json or args.curated_json:
        papers = matched
        if args.curated_json:
            # Peripheral papers render terse (no abstract) downstream, so their
            # full summary is dead weight in the agent's context. Drop it while
            # keeping the fields the terse peripheral list still needs.
            papers = [
                {k: v for k, v in p.items() if not (p["priority"] == "peripheral" and k == "summary")}
                for p in matched
            ]
        print(json.dumps({"cutoff": cutoff.isoformat(), "count": len(matched),
                          "papers": papers}, indent=2, ensure_ascii=False))
        return 0

    render_markdown(matched, cutoff, args.days)
    return 0


def render_markdown(matched: list[dict], cutoff: datetime, days: int) -> None:
    now = datetime.now(timezone.utc)
    print(f"# arXiv storage-systems digest — last {days} days")
    print(f"_Window: {cutoff:%Y-%m-%d} → {now:%Y-%m-%d} · {len(matched)} papers · "
          f"categories: {', '.join(CATEGORIES)}_\n")

    if not matched:
        print("No matching papers in this window.")
        return

    # `matched` is already ordered by (tier, topic, newest-first), so groupby
    # over topic yields contiguous, correctly-ordered sections. The peripheral
    # tier renders terse (title + one-line meta, no abstract) so it stays
    # skimmable without crowding the storage-relevant sections above it.
    last_tier = None
    for topic, group in groupby(matched, key=lambda e: e["topic"]):
        papers = list(group)
        tier = papers[0]["priority"]
        if tier != last_tier:
            print(f"\n## {SECTION_TITLES[tier]}\n")
            last_tier = tier
        print(f"### {topic}  ({len(papers)})\n")
        for p in papers:
            authors = ", ".join(p["authors"][:4]) + (" et al." if len(p["authors"]) > 4 else "")
            date = p["published"][:10]
            cats = ", ".join(p["categories"][:3])
            if tier == "peripheral":
                print(f"- [{p['title']}]({p['id']}) · {date} · `{cats}` · arXiv:{p['arxiv_id']}")
                continue
            abstract = p["summary"]
            if len(abstract) > 500:
                abstract = abstract[:500].rsplit(" ", 1)[0] + "…"
            print(f"- **[{p['title']}]({p['id']})**  ")
            print(f"  {authors} · {date} · `{cats}` · arXiv:{p['arxiv_id']}  ")
            print(f"  {abstract}\n")
        if tier == "peripheral":
            print()


if __name__ == "__main__":
    sys.exit(main())
