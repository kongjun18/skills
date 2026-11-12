#!/usr/bin/env python3
"""Survey top systems proceedings and produce machine metadata + scaffolding.

This script is the collection and scaffolding step, NOT the researcher. It:
  - downloads official conference pages and PDFs where available,
  - records blocked/future venue-years,
  - strips BibTeX boilerplate from USENIX author fields and normalizes UTF-8,
  - assigns a first-pass `topic_tags_keyword_seed` (renamed from `topic_tags`
    in earlier versions to signal that it is a scaffold, not curated truth),
  - parses USENIX award markers ("Best Paper", "Distinguished Artifact") into
    an `awards` list,
  - assigns a `priority_seed` (must-read | should-read | skim) using deployment
    and award signals,
  - writes per-venue catalog files under thinking/catalog/{venue}-{year}.md
    using the 5-line digest schema from references/final_deliverables.md,
  - removes the legacy monolithic thinking/paper_catalog.md and stale
    thinking/per_paper/ if present.

Curated tags, sparks, ideas, and trends are produced by agents in Steps 3-7 of
the workflow described in SKILL.md, not by this script.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import time
import unicodedata
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable
from urllib.parse import parse_qs, unquote, urljoin, urlparse

import requests
from bs4 import BeautifulSoup


USER_AGENT = "system-research-scout/1.0 (+research metadata; respectful crawler)"
TIMEOUT = 30


USENIX_SOURCES = {
    ("OSDI", 2025): "https://www.usenix.org/conference/osdi25/technical-sessions",
    ("OSDI", 2026): "https://www.usenix.org/conference/osdi26/technical-sessions",
    ("FAST", 2025): "https://www.usenix.org/conference/fast25/technical-sessions",
    ("FAST", 2026): "https://www.usenix.org/conference/fast26/technical-sessions",
    ("ATC", 2025): "https://www.usenix.org/conference/atc25/technical-sessions",
    ("NSDI", 2025): "https://www.usenix.org/conference/nsdi25/technical-sessions",
    ("NSDI", 2026): "https://www.usenix.org/conference/nsdi26/technical-sessions",
}

SIGCOMM_SOURCES = {
    ("SIGCOMM", 2025): "https://conferences.sigcomm.org/sigcomm/2025/program/papers-info/",
}

SOSP_ACCEPTED_SOURCES = {
    ("SOSP", 2025): "https://sigops.org/s/conferences/sosp/2025/accepted.html",
}

SIGMOD_OPENTOC_SOURCES = {
    ("SIGMOD", 2025): [
        "https://2025.sigmod.org/toc-3-1.html",
        "https://2025.sigmod.org/toc-2-6.html",
        "https://2025.sigmod.org/toc-3-3.html",
    ],
}

STATIC_STATUS = [
    {
        "venue": "ATC",
        "year": 2026,
        "status": "not-yet-published",
        "source_url": "https://www.usenix.org/conferences/byname/131",
        "note": "USENIX ATC archive listed 2025 as latest; atc26 technical sessions returned 404 as of 2026-06-09.",
    },
    {
        "venue": "SOSP",
        "year": 2026,
        "status": "not-yet-published",
        "source_url": "https://sigops.org/s/conferences/sosp/2026/accepted.html",
        "note": "Accepted page was TBD as of 2026-06-09.",
    },
    {
        "venue": "SIGCOMM",
        "year": 2026,
        "status": "not-yet-published",
        "source_url": "https://conferences.sigcomm.org/sigcomm/2026/",
        "note": "Conference/camera-ready dates were after 2026-06-09; proceedings unavailable.",
    },
    {
        "venue": "VLDB",
        "year": 2025,
        "status": "source-blocked",
        "source_url": "https://www.vldb.org/pvldb/volumes/18/",
        "note": "PVLDB Vol. 18 is the official 2025 source, but vldb.org timed out from this environment during validation.",
    },
    {
        "venue": "VLDB",
        "year": 2026,
        "status": "partial",
        "source_url": "https://www.vldb.org/pvldb/volumes/19/",
        "note": "PVLDB Vol. 19 was in progress; VLDB 2026 research-track cutoff is June 15, 2026.",
    },
    {
        "venue": "OSDI",
        "year": 2026,
        "status": "accepted-list-only",
        "source_url": "https://www.usenix.org/conference/osdi26/technical-sessions",
        "note": "Technical-session page had titles/authors but no public abstracts/PDFs as of 2026-06-09.",
    },
    {
        "venue": "ASPLOS",
        "year": 2025,
        "status": "source-gated",
        "source_url": "https://www.asplos-conference.org/asplos2025/main-program/",
        "note": "ACM DL gates PDFs; this script does not auto-scrape ACM DL. Reader agents should populate manually from author pages, arXiv, or DOI-link PDFs.",
    },
    {
        "venue": "ASPLOS",
        "year": 2026,
        "status": "source-gated",
        "source_url": "https://www.asplos-conference.org/asplos2026/",
        "note": "Re-check availability per conference cadence; ACM DL auto-scrape not implemented.",
    },
    {
        "venue": "EuroSys",
        "year": 2025,
        "status": "source-gated",
        "source_url": "https://2025.eurosys.org/program.html",
        "note": "ACM DL gates PDFs; reader agents populate manually from author pages, arXiv, or DOI-link PDFs.",
    },
    {
        "venue": "EuroSys",
        "year": 2026,
        "status": "not-yet-published",
        "source_url": "https://2026.eurosys.org/",
        "note": "Re-check; EuroSys 2026 program typically published in spring '26.",
    },
]


# Keyword-seed tagging is a SCAFFOLD. Reader agents replace these with curated
# tags from the 16-leaf taxonomy in SKILL.md §5. Do not derive trend or taste
# claims from this list; the field name is deliberately verbose to discourage
# mistaking it for ground truth.
KEYWORD_SEED_RULES = [
    ("llm-serving-engine", ["inference", "serving", "vllm", "sglang", "decoding", "request batching", "prefill", "decode"]),
    ("llm-training-substrate", ["training", "pretrain", "fine-tun", "fault tolerant training", "parallelism", "pipeline parallel", "tensor parallel", "collective communication"]),
    ("kv-cache-mgmt", ["kv cache", "kv-cache", "kvcache", "attention cache", "prefix cache"]),
    ("vector-retrieval", ["vector search", "ann index", "approximate nearest neighbor", "graph index", "vector index"]),
    ("rag-data-plane", ["retrieval-augmented", "rag pipeline", "embedding refresh", "feature store"]),
    ("cxl-disagg-memory", ["cxl", "disaggregated memory", "remote memory", "tiered memory", "memory pool"]),
    ("cloud-object-storage", ["object storage", "blob store", "erasure cod", "geo-distributed", "tape", "archive"]),
    ("local-flash-storage", ["ssd", "nvm", "flash", "file system", "filesystem", "write-ahead log", "kv store"]),
    ("learned-index-or-optimizer", ["learned index", "learned optimizer", "learned cache", "auto-tuning", "tuner"]),
    ("verification-and-checkers", ["formal verif", "invariant", "fuzz", "semantic checker", "deterministic replay", "model checking"]),
    ("gpu-network-and-collectives", ["nccl", "rdma", "collective", "optical", "congestion control", "in-network aggregation"]),
    ("agentic-data-workflows", ["llm agent", "tool use", "agentic workflow", "agent orchestration"]),
]

DEPLOYMENT_PHRASES = [
    "in production",
    "deployed",
    "we observed",
    "at scale",
    "production deployment",
    "production cluster",
]

INDUSTRY_AT_SCALE = [
    "alibaba", "bytedance", "tencent", "meituan", "microsoft", "google",
    "anthropic", "nvidia", "meta", "amazon", "apple", "huawei",
    "baidu", "ant group", "kuaishou", "xiaohongshu",
]


@dataclass
class Paper:
    venue: str
    year: int
    title: str
    authors: str = ""
    abstract: str = ""
    doi: str = ""
    pdf_url: str = ""
    source_url: str = ""
    local_pdf: str = ""
    status: str = "metadata-only"
    note: str = ""
    download_source: str = ""
    download_error: str = ""
    source_status: str = "published"
    awards: list[str] = field(default_factory=list)
    priority_seed: str = "skim"
    topic_tags_keyword_seed: list[str] = field(default_factory=list)
    topic_tags_curated: list[str] = field(default_factory=list)
    topic_tag_evidence: dict[str, str] = field(default_factory=dict)


def normalize_text(text: str) -> str:
    """Strip mojibake produced by misdecoded UTF-8 (e.g. "Î»-Tune" -> "λ-Tune")
    and collapse whitespace."""
    if not text:
        return ""
    # Best-effort mojibake repair: many USENIX/ACM scrapes arrived as UTF-8
    # bytes mis-decoded as latin-1. Round-trip if it looks like that.
    if any(ch in text for ch in ("Î", "Ã", "Â")):
        try:
            repaired = text.encode("latin-1").decode("utf-8")
            text = repaired
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
    text = unicodedata.normalize("NFKC", text)
    return re.sub(r"\s+", " ", text).strip()


def clean(text: str) -> str:
    return normalize_text(text)


def strip_bibtex(authors: str) -> str:
    """Remove BibTeX/copyright boilerplate that USENIX pages append to author
    blocks (e.g. "Awarded Best Paper! ... BibTeX @inproceedings {...} ...")."""
    if not authors:
        return ""
    text = authors
    # Cut everything from the first "BibTeX @" or "Open Access" or "Download X PDF" onward.
    for marker in ("BibTeX @", "Open Access", "Download Paper", "Download PDF", "Presentation Video", "Open Access Sponsored"):
        idx = text.find(marker)
        if idx > 0:
            text = text[:idx]
    # Drop "Awarded ..." trailing phrases; they go into `awards` instead.
    text = re.sub(r"\s*Awarded[^.;]*[.;]?\s*", " ", text)
    return clean(text)


def detect_awards(raw_authors_block: str, page_html: str) -> list[str]:
    """USENIX flags awards inline on the presentation page. We check both the
    raw author block (before stripping) and the full page HTML to catch
    "Best Paper", "Best Paper Runner-Up", and "Distinguished Artifact"."""
    awards: list[str] = []
    haystack = (raw_authors_block + " " + page_html).lower()
    if "best paper runner" in haystack:
        awards.append("best-paper-runner-up")
    elif "awarded best paper" in haystack or "best paper award" in haystack:
        awards.append("best-paper")
    if "distinguished artifact" in haystack:
        awards.append("distinguished-artifact")
    return awards


def infer_keyword_seed_tags(paper: Paper) -> list[str]:
    """First-pass scaffold tagging from title + abstract keywords. NOT a
    ground-truth taxonomy; readers replace these with curated tags."""
    blob = (paper.title + " " + paper.abstract).lower()
    tags: list[str] = []
    for tag, keywords in KEYWORD_SEED_RULES:
        if any(kw in blob for kw in keywords):
            tags.append(tag)
    return tags


def assign_priority_seed(paper: Paper) -> str:
    """Coarse read priority — readers may override and record a reason.

    Rules (from SKILL.md §6):
      - any award                                  -> must-read
      - industry-at-scale author + deployment      -> must-read
      - abstract mentions deployment/scale         -> should-read
      - clustering signal (>=3 papers on same kwd) -> should-read (added post-hoc)
      - else                                       -> skim
    """
    if paper.awards:
        return "must-read"
    authors_l = paper.authors.lower()
    abstract_l = paper.abstract.lower()
    has_deployment = any(p in abstract_l for p in DEPLOYMENT_PHRASES)
    has_industry = any(name in authors_l for name in INDUSTRY_AT_SCALE)
    if has_deployment and has_industry:
        return "must-read"
    if has_deployment or has_industry:
        return "should-read"
    return "skim"


def boost_priority_by_clustering(rows: list[Paper]) -> None:
    """If >=3 papers in the same (year, keyword-seed-tag) bucket are still
    `skim`, promote them to `should-read` per SKILL.md §6."""
    bucket: dict[tuple[int, str], list[Paper]] = {}
    for row in rows:
        for tag in row.topic_tags_keyword_seed:
            bucket.setdefault((row.year, tag), []).append(row)
    for (_, _), papers in bucket.items():
        if len(papers) >= 3:
            for p in papers:
                if p.priority_seed == "skim":
                    p.priority_seed = "should-read"


def slugify(text: str, limit: int = 140) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return (text[:limit].rstrip("-") or "untitled")


def unwrap_url(url: str) -> str:
    if "urldefense.proofpoint.com" not in url:
        return url
    parsed = urlparse(url)
    target = parse_qs(parsed.query).get("u", [""])[0]
    if not target:
        return url
    target = target.replace("-3A", ":").replace("-2F", "/").replace("-3F", "?").replace("-3D", "=")
    target = target.replace("-26", "&")
    return unquote(target)


class Client:
    def __init__(self, cache_dir: Path, delay: float = 0.25):
        self.cache_dir = cache_dir
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get(self, url: str) -> requests.Response:
        time.sleep(self.delay)
        return self.session.get(url, timeout=TIMEOUT)

    def html(self, url: str) -> str:
        key = hashlib.sha256(url.encode()).hexdigest()[:16] + ".html"
        path = self.cache_dir / key
        if path.exists():
            return path.read_text(encoding="utf-8", errors="replace")
        response = self.get(url)
        response.raise_for_status()
        path.write_text(response.text, encoding="utf-8")
        return response.text

    def download_pdf(self, url: str, path: Path) -> bool:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and path.stat().st_size > 1024:
            return True
        response = self.get(url)
        if response.status_code != 200 or b"%PDF" not in response.content[:2048]:
            return False
        path.write_bytes(response.content)
        return True


def parse_usenix(client: Client, venue: str, year: int, url: str) -> list[Paper]:
    html_text = client.html(url)
    soup = BeautifulSoup(html_text, "html.parser")
    slug = url.rstrip("/").split("/")[-2]
    links: dict[str, str] = {}
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"]
        if f"/conference/{slug}/presentation/" in href:
            full = urljoin(url, href)
            text = clean(anchor.get_text(" ", strip=True))
            if text and full not in links:
                links[full] = text

    rows: list[Paper] = []
    for page_url, title_hint in links.items():
        try:
            raw_page = client.html(page_url)
            page = BeautifulSoup(raw_page, "html.parser")
        except Exception as exc:  # noqa: BLE001
            rows.append(Paper(venue, year, title_hint, source_url=page_url, status="blocked", note=str(exc)))
            continue

        title = clean(page.find("h1").get_text(" ", strip=True)) if page.find("h1") else title_hint
        abstract_el = page.select_one(".field-name-field-paper-description")
        abstract = clean(abstract_el.get_text(" ", strip=True)) if abstract_el else ""
        pdf_url = ""
        for anchor in page.find_all("a", href=True):
            href = anchor["href"]
            label = clean(anchor.get_text(" ", strip=True)).lower()
            if href.lower().endswith(".pdf") and ("pdf" in label or f"/{slug}-" in href):
                if "slides" not in href.lower():
                    pdf_url = urljoin(page_url, href)
                    break

        raw_authors = ""
        node = page.select_one(".node-paper")
        if node:
            node_text = clean(node.get_text(" ", strip=True))
            if abstract:
                node_text = node_text.replace(abstract, "")
            if title:
                node_text = node_text.replace(title, "")
            raw_authors = clean(node_text.split("Abstract")[0])

        awards = detect_awards(raw_authors, raw_page)
        authors = strip_bibtex(raw_authors)

        paper = Paper(
            venue=venue,
            year=year,
            title=title,
            authors=authors,
            abstract=abstract,
            pdf_url=pdf_url,
            source_url=page_url,
            status="metadata-only",
            awards=awards,
        )
        if pdf_url:
            paper.status = "pdf-available"
        rows.append(paper)
    return dedupe(rows)


def parse_sigcomm_2025(client: Client, url: str) -> list[Paper]:
    soup = BeautifulSoup(client.html(url), "html.parser")
    rows: list[Paper] = []
    for tr in soup.find_all("tr"):
        doi_anchor = tr.find("a", href=lambda href: href and "dl.acm.org/doi/10.1145/3718958." in href)
        if not doi_anchor:
            continue
        href = doi_anchor["href"]
        first_cell = tr.find("td")
        title = ""
        authors = ""
        if first_cell:
            title_el = first_cell.select_one(".text-color-primary") or first_cell.find("p")
            authors_el = first_cell.select_one(".style_italic")
            title = clean(title_el.get_text(" ", strip=True)) if title_el else ""
            authors = clean(authors_el.get_text(" ", strip=True)) if authors_el else ""
        if not title:
            continue
        abstract = ""
        next_row = tr.find_next_sibling("tr")
        if next_row and "abstract-row" in (next_row.get("class") or []):
            abstract = clean(next_row.get_text(" ", strip=True))
            abstract = re.sub(r"^Abstract:\s*", "", abstract, flags=re.I)
        doi = href.split("/doi/", 1)[-1]
        rows.append(
            Paper(
                "SIGCOMM",
                2025,
                title,
                authors=authors,
                abstract=abstract,
                doi=doi,
                source_url=url,
                pdf_url=f"https://dl.acm.org/doi/pdf/{doi}",
                status="metadata-only",
            )
        )
    return dedupe(rows)


def parse_sigmod_opentoc(client: Client, year: int, urls: Iterable[str]) -> list[Paper]:
    rows: list[Paper] = []
    seen_titles: set[str] = set()
    for url in urls:
        soup = BeautifulSoup(client.html(url), "html.parser")
        headings = soup.find_all("h3")
        for index, heading in enumerate(headings):
            title = clean(heading.get_text(" ", strip=True))
            if not title or "editorial" in title.lower() or title in seen_titles:
                continue
            seen_titles.add(title)
            start = heading
            stop = headings[index + 1] if index + 1 < len(headings) else None
            parts = []
            doi = ""
            for sib in start.next_siblings:
                if sib is stop:
                    break
                if getattr(sib, "name", None) == "h3":
                    break
                if getattr(sib, "get_text", None):
                    parts.append(clean(sib.get_text(" ", strip=True)))
                    for anchor in sib.find_all("a", href=True) if getattr(sib, "find_all", None) else []:
                        href = unwrap_url(anchor["href"])
                        if "dl.acm.org/doi/" in href and not doi:
                            doi = href.split("/doi/", 1)[-1].split("?")[0]
            text = clean(" ".join(p for p in parts if p))
            abstract = ""
            match = re.search(r"Abstract\s*[:.]?\s*(.*?)(?:Full Citation|DOI:|$)", text, flags=re.I)
            if match:
                abstract = clean(match.group(1))
            rows.append(
                Paper(
                    "SIGMOD",
                    year,
                    title,
                    abstract=abstract,
                    doi=doi,
                    source_url=url,
                    pdf_url=f"https://dl.acm.org/doi/pdf/{doi}" if doi else "",
                    status="metadata-only",
                )
            )
    return rows


def parse_sosp_accepted(client: Client, year: int, url: str) -> list[Paper]:
    soup = BeautifulSoup(client.html(url), "html.parser")
    rows: list[Paper] = []
    heading = soup.find("h2", string=lambda text: text and "Accepted Papers" in text)
    search_root = heading.find_parent("main") if heading else soup
    for li in search_root.find_all("li"):
        title_el = li.find("b")
        if not title_el:
            continue
        title = clean(title_el.get_text(" ", strip=True))
        authors_el = li.find("em")
        authors = clean(authors_el.get_text(" ", strip=True)) if authors_el else ""
        rows.append(
            Paper(
                "SOSP",
                year,
                title=title,
                authors=authors,
                source_url=url,
                status="accepted-list-only",
                note="Official accepted page lists titles/authors only; use ACM DL proceedings 10.1145/3731569 for abstracts and PDFs.",
            )
        )
    return dedupe(rows)


def dedupe(rows: Iterable[Paper]) -> list[Paper]:
    out: list[Paper] = []
    seen: set[tuple[str, int, str]] = set()
    for row in rows:
        if clean(row.title).lower() in {"title tba", "tba"}:
            continue
        key = (row.venue, row.year, clean(row.title).lower())
        if row.title and key not in seen:
            seen.add(key)
            out.append(row)
    return out


def unique_pdf_path(papers_dir: Path, row: Paper, used: set[Path]) -> Path:
    base = papers_dir / row.venue.lower() / str(row.year) / f"{slugify(row.title)}.pdf"
    path = base
    if path in used:
        suffix = hashlib.sha256(f"{row.venue}-{row.year}-{row.title}".encode()).hexdigest()[:8]
        path = base.with_name(f"{base.stem}--{suffix}.pdf")
    used.add(path)
    return path


def _looks_like_valid_pdf(path: Path, min_bytes: int = 4096) -> bool:
    """A previously-downloaded file counts as reusable only if it starts with
    the %PDF magic and is large enough to be plausible content (not an HTML
    paywall stub saved by an earlier broken run)."""
    try:
        if not path.is_file() or path.stat().st_size < min_bytes:
            return False
        with path.open("rb") as fh:
            return fh.read(4) == b"%PDF"
    except OSError:
        return False


def finalize_paper_downloads(rows: list[Paper], papers_dir: Path, client: Client, download: bool) -> None:
    used: set[Path] = set()
    for row in rows:
        if not row.pdf_url:
            row.download_error = row.download_error or "No direct PDF URL discovered from official source."
            continue
        if not download:
            row.status = "pdf-available"
            continue
        pdf_path = unique_pdf_path(papers_dir, row, used)
        # Skip re-download if the destination already holds a valid PDF.
        # This makes re-runs idempotent and protects expensive USENIX/VLDB
        # corpora from being re-fetched after a coverage_ledger refresh.
        if _looks_like_valid_pdf(pdf_path):
            row.local_pdf = str(pdf_path)
            row.download_source = row.pdf_url
            row.status = "downloaded-cached"
            continue
        try:
            if client.download_pdf(row.pdf_url, pdf_path):
                row.local_pdf = str(pdf_path)
                row.download_source = row.pdf_url
                row.status = "downloaded"
            else:
                row.status = "pdf-download-failed"
                row.download_error = f"PDF URL did not return a PDF: {row.pdf_url}"
        except Exception as exc:  # noqa: BLE001
            row.status = "pdf-download-failed"
            row.download_error = str(exc)


def write_jsonl(rows: list[Paper], status_rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(asdict(row), ensure_ascii=False) + "\n")
        for row in status_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def grouped(rows: list[Paper], key_fn):
    groups: dict = {}
    for row in rows:
        groups.setdefault(key_fn(row), []).append(row)
    return groups


def first_author_last_name(authors: str) -> str:
    if not authors:
        return "Unknown"
    first = authors.split(",")[0].strip()
    parts = first.split()
    return parts[-1] if parts else "Unknown"


def claim_sentence(abstract: str) -> str:
    """Pick the first abstract sentence that names what the paper did.
    Heuristic: prefer the sentence containing "we present|propose|design|build"
    when one exists; otherwise the first sentence."""
    if not abstract:
        return ""
    sentences = re.split(r"(?<=[.!?])\s+", abstract)
    for s in sentences:
        if re.search(r"\bwe (present|propose|design|build|introduce|develop)\b", s, re.I):
            return s.strip()
    return sentences[0].strip() if sentences else ""


def pain_sentence(abstract: str) -> str:
    """Pick a sentence that names an unsolved pain. Heuristic: phrases like
    'in practice', 'we assume', 'remains', 'future work', 'challenging',
    'hard to'. Returns '—' if none found."""
    if not abstract:
        return "—"
    sentences = re.split(r"(?<=[.!?])\s+", abstract)
    triggers = ("in practice", "we assume", "remains", "future work",
                "challenging", "hard to", "however,", "not considered",
                "hard to deploy")
    for s in sentences:
        s_l = s.lower()
        if any(t in s_l for t in triggers):
            return s.strip()
    return "—"


def write_catalog_per_venue_year(rows: list[Paper], thinking_dir: Path) -> None:
    """Write thinking/catalog/{venue}-{year}.md per the 5-line digest schema
    in references/final_deliverables.md. Replaces the legacy monolithic
    thinking/paper_catalog.md."""
    catalog_dir = thinking_dir / "catalog"
    catalog_dir.mkdir(parents=True, exist_ok=True)
    for (venue, year), group in sorted(grouped(rows, lambda r: (r.venue, r.year)).items()):
        path = catalog_dir / f"{venue}-{year}.md"
        with path.open("w", encoding="utf-8") as f:
            f.write(f"# Catalog — {venue} {year}\n\n")
            f.write(
                "Source: see `papers/metadata.jsonl` for per-paper source URLs. "
                "Completeness: see `coverage_ledger.md`. "
                "This file is the 5-line digest scaffold; reader agents fill in "
                "curated tags and may rewrite the Pain line with a verbatim "
                "quote from the paper introduction.\n\n"
            )
            for row in sorted(group, key=lambda r: r.title):
                lead = first_author_last_name(row.authors) or "Unknown"
                seed_tags = ", ".join(row.topic_tags_keyword_seed) or "—"
                claim = claim_sentence(row.abstract) or "—"
                pain = pain_sentence(row.abstract)
                pdf_field = row.local_pdf if row.local_pdf else f"metadata-only: {row.status}"
                f.write(f"- **{row.title}** — {lead} et al. ({row.venue} {row.year})\n")
                f.write(f"  - Curated tags: other (seed: {seed_tags})\n")
                f.write(f"  - Claim: {claim}\n")
                f.write(f"  - Pain: {pain}\n")
                f.write(f"  - PDF: {pdf_field}\n")
                if row.awards:
                    f.write(f"  - Awards: {', '.join(row.awards)}\n")
                f.write(f"  - Priority seed: {row.priority_seed}\n")


def cleanup_legacy_outputs(thinking_dir: Path) -> None:
    legacy_catalog = thinking_dir / "paper_catalog.md"
    if legacy_catalog.exists():
        legacy_catalog.unlink()
    legacy_per_paper = thinking_dir / "per_paper"
    if legacy_per_paper.exists() and legacy_per_paper.is_dir():
        shutil.rmtree(legacy_per_paper)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--years", nargs="+", type=int, default=[2025, 2026])
    parser.add_argument("--out-papers", default="papers")
    parser.add_argument("--out-thinking", default="thinking")
    parser.add_argument(
        "--out-sparking",
        default="sparking",
        help="Directory where reader/synthesis/critic agents will write spark files. "
        "Created if missing; the script does not write spark content (agents do).",
    )
    parser.add_argument("--no-download", action="store_true", help="Collect metadata without downloading PDFs.")
    args = parser.parse_args()

    papers_dir = Path(args.out_papers)
    thinking_dir = Path(args.out_thinking)
    sparking_dir = Path(args.out_sparking)
    sparking_dir.mkdir(parents=True, exist_ok=True)
    client = Client(papers_dir / "_cache")
    rows: list[Paper] = []

    for (venue, year), url in USENIX_SOURCES.items():
        if year in args.years:
            rows.extend(parse_usenix(client, venue, year, url))

    for (venue, year), url in SIGCOMM_SOURCES.items():
        if year in args.years:
            rows.extend(parse_sigcomm_2025(client, url))

    for (venue, year), url in SOSP_ACCEPTED_SOURCES.items():
        if year in args.years:
            rows.extend(parse_sosp_accepted(client, year, url))

    for (venue, year), urls in SIGMOD_OPENTOC_SOURCES.items():
        if year in args.years:
            rows.extend(parse_sigmod_opentoc(client, year, urls))

    status_rows = [row for row in STATIC_STATUS if row["year"] in args.years]
    rows = dedupe(rows)
    finalize_paper_downloads(rows, papers_dir, client, not args.no_download)

    # Tagging + priority seed must happen AFTER abstracts are populated.
    for row in rows:
        row.topic_tags_keyword_seed = infer_keyword_seed_tags(row)
        row.priority_seed = assign_priority_seed(row)
    boost_priority_by_clustering(rows)

    write_jsonl(rows, status_rows, papers_dir / "metadata.jsonl")
    thinking_dir.mkdir(parents=True, exist_ok=True)
    cleanup_legacy_outputs(thinking_dir)
    write_catalog_per_venue_year(rows, thinking_dir)

    print(f"Collected {len(rows)} paper metadata rows")
    print(f"Wrote {papers_dir / 'metadata.jsonl'}")
    print(f"Wrote {thinking_dir / 'catalog'}/<venue>-<year>.md (one per venue-year)")
    print(f"Ensured {sparking_dir} exists for agent-authored sparks")
    print(
        "Next steps for the agent: build thinking/coverage_ledger.md, fan out "
        "reader agents, run synthesis and critic, then validate with "
        "scripts/validate_outputs.py."
    )


if __name__ == "__main__":
    main()
