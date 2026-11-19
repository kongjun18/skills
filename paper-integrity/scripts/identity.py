#!/usr/bin/env python3
"""Stage 2: reference identity, version, link, and retraction checks.

For each cited entry, resolve it against Crossref, OpenAlex, and arXiv (DBLP
blocks scripted clients), compare title, first author, year, and venue, check
URLs of web references, and flag retractions and preprints that have a
published version. Only public reference metadata leaves the machine.

Writes identity.json (resolved records, used by fetch_sources.py) and
findings-identity.json in --out. Run mechanical.py first (it lists cited keys).
"""

import argparse
import os
import re
import urllib.parse
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

from common import (Http, die, entry_arxiv_id, entry_url, finding, latex_to_text,
                    norm_name, norm_title, parse_bib, read_json, split_names,
                    summarize, title_sim, write_json)

PREPRINT_HOSTS = ("arxiv", "biorxiv", "medrxiv", "ssrn", "research square",
                  "openreview", "techrxiv", "preprints")
WEB_TYPES = ("misc", "online", "manual", "electronic", "www", "software")


def oa_record(w):
    if not isinstance(w, dict) or not w.get("display_name"):
        return None
    locs = []
    for loc in w.get("locations") or []:
        src = loc.get("source") or {}
        if src.get("display_name"):
            locs.append({"venue": src["display_name"], "type": src.get("type"),
                         "pdf": loc.get("pdf_url"), "landing": loc.get("landing_page_url")})
    abstract = None
    inv = w.get("abstract_inverted_index")
    if inv:
        pos = sorted((p, word) for word, ps in inv.items() for p in ps)
        abstract = " ".join(word for _, word in pos)
    best = w.get("best_oa_location") or {}
    return {
        "source": "openalex",
        "id": w.get("id"),
        "title": w["display_name"],
        "authors": [a["author"]["display_name"] for a in w.get("authorships") or []
                    if a.get("author", {}).get("display_name")],
        "year": w.get("publication_year"),
        "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
        "venues": locs,
        "is_retracted": bool(w.get("is_retracted")),
        "oa_pdf": best.get("pdf_url") or (w.get("open_access") or {}).get("oa_url"),
        "abstract": abstract,
    }


def cr_record(m):
    if not isinstance(m, dict) or not m.get("title"):
        return None
    year = None
    for k in ("published-print", "published-online", "issued"):
        parts = (m.get(k) or {}).get("date-parts") or [[None]]
        if parts[0][0]:
            year = parts[0][0]
            break
    return {
        "source": "crossref",
        "title": m["title"][0] + (": " + m["subtitle"][0] if m.get("subtitle") else ""),
        "authors": [" ".join(x for x in (a.get("given"), a.get("family")) if x)
                    for a in m.get("author") or []],
        "year": year,
        "doi": m.get("DOI"),
        "venues": [{"venue": v, "type": m.get("type")} for v in m.get("container-title") or []],
        "is_retracted": any(u.get("type") in ("retraction", "withdrawal")
                            for u in m.get("updated-by") or []),
        "oa_pdf": None,
        "abstract": None,
    }


def arxiv_record(http, aid):
    status, body = http.get(f"https://export.arxiv.org/api/query?id_list={aid}",
                            accept_json=False)
    if status != 200 or not body:
        return None
    ns = {"a": "http://www.w3.org/2005/Atom"}
    try:
        e = ET.fromstring(body).find("a:entry", ns)
    except ET.ParseError:
        return None
    if e is None or e.find("a:title", ns) is None:
        return None
    published = e.findtext("a:published", default="", namespaces=ns)
    return {
        "source": "arxiv",
        "title": re.sub(r"\s+", " ", e.findtext("a:title", namespaces=ns)).strip(),
        "authors": [a.findtext("a:name", namespaces=ns) for a in e.findall("a:author", ns)],
        "year": int(published[:4]) if published[:4].isdigit() else None,
        "doi": None,
        "venues": [{"venue": "arXiv", "type": "repository"}],
        "is_retracted": False,
        "oa_pdf": f"https://arxiv.org/pdf/{aid}",
        "abstract": re.sub(r"\s+", " ", e.findtext("a:summary", default="", namespaces=ns)).strip(),
    }


def same_work(bib_title, rec_title):
    """Title similarity that tolerates a record that drops the subtitle."""
    a, b = norm_title(bib_title), norm_title(rec_title)
    if a and b and (a.startswith(b + " ") or b.startswith(a + " ")):
        return 0.95
    return title_sim(bib_title, rec_title)


def first_author_matches(first, record):
    if not first or not record or not record["authors"]:
        return False
    return norm_name(first) in norm_name(record["authors"][0])


def search_title(http, title, first_author, year=None):
    """Best title match across OpenAlex and Crossref; returns (record, sim, tried)."""
    q = re.sub(r"[^\w\s]", " ", latex_to_text(title))
    q = re.sub(r"\s+", " ", q).strip()
    tried, cands = [], []
    url = ("https://api.openalex.org/works?per-page=5&filter=title.search:"
           + urllib.parse.quote(q))
    tried.append("OpenAlex title search")
    status, body = http.get(url)
    if status == 200 and isinstance(body, dict):
        cands += [oa_record(w) for w in body.get("results") or []]
    url = ("https://api.crossref.org/works?rows=5&query.bibliographic="
           + urllib.parse.quote(f"{q} {first_author or ''}".strip()))
    tried.append("Crossref bibliographic search")
    status, body = http.get(url)
    if status == 200 and isinstance(body, dict):
        cands += [cr_record(m) for m in body.get("message", {}).get("items") or []]
    # Common titles match several works; prefer the same first author and year.
    best, best_sim, best_score = None, 0.0, -1.0
    for c in cands:
        if c:
            sim = same_work(title, c["title"])
            score = sim + 0.2 * first_author_matches(first_author, c) + \
                0.1 * (year is not None and c.get("year") == year)
            if score > best_score:
                best, best_sim, best_score = c, sim, score
    return best, best_sim, tried


VENUE_FILLER = {"proc", "proceedings", "conference", "conf", "symposium", "symp", "workshop",
                "international", "annual", "usenix", "acm", "ieee", "the", "of", "on", "in"}


def abbrev_of(abbr, words):
    """True if abbr spells word prefixes of words in order, skipping words:
    "fast" ~ "file and storage technologies", "eurosys" ~ "european ...
    computer systems", "vldb" ~ "very large data bases"."""
    def go(i, j):
        if i == len(abbr):
            return True
        for k in range(j, len(words)):
            w = words[k]
            for p in range(min(len(w), len(abbr) - i), 0, -1):
                if w[:p] == abbr[i:i + p] and go(i + p, k + 1):
                    return True
        return False
    return go(0, 0)


def acronym_matches(a, b):
    """A short all-letter token of either venue abbreviates the other venue."""
    for x, y in ((a, b), (b, a)):
        words = y.split()
        for t in x.split():
            if t.isalpha() and 3 <= len(t) <= 10 and t not in VENUE_FILLER and t not in words \
                    and len(words) >= 2 and abbrev_of(t, words):
                return True
    return False


def venue_matches(bib_venue, record_venues):
    a = norm_title(bib_venue)
    if not a:
        return True
    acr = lambda s: "".join(w[0] for w in s.split() if w not in ("of", "on", "the", "and", "for", "in"))
    for v in record_venues:
        b = norm_title(v["venue"])
        if not b:
            continue
        if a in b or b in a or title_sim(a, b) >= 0.6:
            return True
        if acr(b) and (acr(b) in a.replace(" ", "") or a.replace(" ", "") in acr(b)):
            return True
        if acronym_matches(a, b):
            return True
        # "Proceedings of the 29th Symposium on ..." vs. "Symposium on ..."
        sig = lambda s: {w for w in s.split() if len(w) > 3 and not w.isdigit()}
        if len(sig(a) & sig(b)) >= max(2, min(len(sig(a)), len(sig(b))) // 2):
            return True
    return False


def check_entry(http, key, e, loc):
    f = e["fields"]
    title = f.get("title", "")
    names = split_names(f.get("author", ""))
    first = names[0] if names else None
    year = int(f["year"][:4]) if f.get("year", "")[:4].isdigit() else None
    bib_venue = latex_to_text(f.get("booktitle") or f.get("journal") or "")
    doi = f.get("doi", "").strip().replace("https://doi.org/", "") or None
    aid = entry_arxiv_id(f)
    url = entry_url(f)
    out = {"key": key, "type": e["type"], "title": latex_to_text(title), "location": loc,
           "records": [], "url": url, "url_status": None}
    fs = []

    def add(sev, conf, cat, evidence, suggestion, anchor=None):
        fs.append(finding("I", sev, conf, cat, anchor or f"{key}|{cat}", loc, evidence,
                          suggestion, key))

    record, how = None, None
    if doi:
        status, body = http.get(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}")
        record = cr_record(body.get("message")) if status == 200 and isinstance(body, dict) else None
        oa_status, oa_body = http.get(f"https://api.openalex.org/works/doi:{urllib.parse.quote(doi)}")
        oa = oa_record(oa_body) if oa_status == 200 else None
        if oa:
            out["records"].append(oa)
        if record:
            out["records"].insert(0, record)
        record = record or oa
        how = "DOI"
        if not record:
            add("S0", "suspected", "identifier-unresolved",
                f"DOI `{doi}` resolves in neither Crossref (HTTP {status}) nor OpenAlex (HTTP {oa_status}).",
                "Check the DOI against the publisher page; correct or remove it.")
        elif title and same_work(title, record["title"]) < 0.75:
            add("S0", "verified", "identifier-mismatch",
                f"DOI `{doi}` resolves to a different work: \"{record['title']}\" "
                f"({record['year']}); the entry says \"{latex_to_text(title)}\".",
                "Correct the DOI or the entry so both describe the cited work.")
            return out, fs
    elif aid:
        record = arxiv_record(http, aid)
        how = "arXiv id"
        if record:
            out["records"].append(record)
            if title and same_work(title, record["title"]) < 0.75:
                add("S0", "verified", "identifier-mismatch",
                    f"arXiv `{aid}` is \"{record['title']}\"; the entry says \"{latex_to_text(title)}\".",
                    "Correct the arXiv id or the entry.")
                return out, fs
        else:
            add("S0", "suspected", "identifier-unresolved",
                f"arXiv id `{aid}` did not resolve.", "Check the id on arxiv.org.")

    if e["type"] in WEB_TYPES and url:
        status, body = http.get(url, accept_json=False, max_bytes=300_000)
        out["url_status"] = status
        if status is None or status >= 400:
            wb_status, wb = http.get("https://archive.org/wayback/available?url="
                                     + urllib.parse.quote(url))
            snap = ((wb or {}).get("archived_snapshots") or {}).get("closest", {}) if wb_status == 200 and isinstance(wb, dict) else {}
            hint = f" An archived copy exists: {snap['url']}." if snap.get("url") else " No archived copy found."
            add("S1", "suspected", "dead-link",
                f"URL {url} returned {status if status else 'no response'} (some sites block scripts; confirm in a browser).{hint}",
                "Replace with a live or archived URL, or a published source.")
        else:
            m = re.search(r"<title[^>]*>(.*?)</title>", body or "", re.S | re.I)
            out["page_title"] = re.sub(r"\s+", " ", m.group(1)).strip() if m else None
        if not record:
            return out, fs

    if not record and title:
        record, sim, tried = search_title(http, title, first, year)
        how = "title search"
        if record and sim >= 0.9:
            out["records"].append(record)
        else:
            near = (f" Closest record (similarity {sim:.2f}): \"{record['title']}\"."
                    if record else "")
            record = None
            if e["type"] in WEB_TYPES:
                add("S1", "suspected", "not-located",
                    f"No URL, DOI, or matching record for this {e['type']} entry "
                    f"({', '.join(tried)}).{near}",
                    "Add a stable URL or DOI, or replace with a locatable source.")
            else:
                add("S0", "suspected", "not-located",
                    f"No record with a matching title ({', '.join(tried)}).{near} "
                    "This does not prove the work does not exist.",
                    "Confirm the work exists (publisher or proceedings page) and add its DOI or URL.")
            return out, fs
    if not record:
        return out, fs

    # Retraction.
    if any(r.get("is_retracted") for r in out["records"]):
        add("S0", "verified", "retracted",
            f"The resolved record ({record.get('doi') or record['title']}) is marked retracted.",
            "Remove the citation or cite it explicitly as retracted.")

    # Title (when resolved by identifier, a close but different title).
    if title and how != "title search":
        s = same_work(title, record["title"])
        if 0.75 <= s < 0.9:
            add("S2", "verified", "title-differs",
                f"Entry title \"{latex_to_text(title)}\" differs from the record \"{record['title']}\".",
                "Use the title as published.")

    # First author.
    if first and record["authors"] and not f.get("author", "").startswith("{{"):
        rec_first = norm_name(record["authors"][0].split()[-1])
        if norm_name(first) and rec_first and norm_name(first) != rec_first and \
                norm_name(first) not in norm_name(record["authors"][0]):
            add("S1", "verified" if how != "title search" else "suspected", "author-mismatch",
                f"First author in the entry is {first}; {record['source']} lists "
                f"{', '.join(record['authors'][:3])}{' et al.' if len(record['authors']) > 3 else ''}.",
                "Correct the author list from the publisher record.")

    venues = [v for r in out["records"] for v in r["venues"]]
    published = [v for v in venues if v.get("type") in ("journal", "conference",
                 "journal-article", "proceedings-article", "proceedings")
                 and not any(h in v["venue"].lower() for h in PREPRINT_HOSTS)]

    # Year. A preprint-only record often carries its latest version's date.
    years = {r["year"] for r in out["records"] if r.get("year")}
    if year and years and year not in years:
        gap = min(abs(year - y) for y in years)
        preprint_only = not published
        add("S1" if gap > 1 and not preprint_only else "S2",
            "verified" if how != "title search" else "suspected", "year-mismatch",
            f"Entry year {year}; records give {', '.join(map(str, sorted(years)))}"
            + (" (preprint-only record; its year may be a later version)." if preprint_only else "."),
            "Use the year of the version you cite.")

    # Preprint cited although a published version exists.
    cites_preprint = bool(aid) or any(h in bib_venue.lower() for h in PREPRINT_HOSTS)
    if cites_preprint:
        if how != "title search":
            r2, sim, _ = search_title(http, title, first, year)
            if r2 and sim >= 0.95:
                out["records"].append(r2)
                published += [v for v in r2["venues"] if v.get("type") in ("journal", "conference",
                              "journal-article", "proceedings-article")
                              and not any(h in v["venue"].lower() for h in PREPRINT_HOSTS)]
        if published:
            add("S1", "suspected", "preprint-has-published-version",
                f"The entry cites a preprint, but records list a published version: "
                f"{', '.join(sorted({v['venue'] for v in published}))}.",
                "Cite the published version unless the claim depends on preprint-only content.")
    elif bib_venue and published and not venue_matches(bib_venue, published):
        add("S1", "suspected", "venue-mismatch",
            f"Entry venue \"{bib_venue}\"{f' ({year})' if year else ''} is not among the record venues: "
            f"{', '.join(sorted({v['venue'] for v in published}))}.",
            "Confirm where and when the cited version appeared and fix the entry.")
    return out, fs


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--paper-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--keys", help="comma-separated subset of cited keys")
    ap.add_argument("--cache", help="HTTP cache file shared across runs (default: <out>/http-cache.json)")
    ap.add_argument("--mailto", help="contact address for the Crossref/OpenAlex polite pool")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()

    cov = read_json(os.path.join(args.out, "coverage-mechanical.json"))
    if not cov:
        die("coverage-mechanical.json missing; run mechanical.py first")
    entries = {}
    for b in cov["inputs"]["bib"]:
        e, _ = parse_bib(b)
        rel = os.path.relpath(b, args.paper_dir)
        for k, v in e.items():
            entries.setdefault(k, dict(v, loc=f"{rel}:{v['line']}"))
    keys = [k for k in cov["cited_keys"] if k in entries]
    if args.keys:
        wanted = set(args.keys.split(","))
        keys = [k for k in keys if k in wanted]

    cache = args.cache or os.path.join(args.out, "http-cache.json")
    http = Http(cache, mailto=args.mailto, delay=0.5)
    results, findings = {}, []
    try:
        with ThreadPoolExecutor(args.workers) as pool:
            for out, fs in pool.map(lambda k: check_entry(http, k, entries[k], entries[k]["loc"]), keys):
                results[out["key"]] = out
                findings += fs
    finally:
        http.save()

    write_json(os.path.join(args.out, "identity.json"), results)
    write_json(os.path.join(args.out, "findings-identity.json"), findings)
    located = sum(1 for r in results.values() if r["records"])
    summarize("identity", findings)
    print(f"  {located}/{len(results)} entries matched a record; cache {cache}")


if __name__ == "__main__":
    main()
