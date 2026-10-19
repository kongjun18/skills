#!/usr/bin/env python3
"""Stage 4 prep: collect the text of each cited source.

Order per key: a local PDF supplied by the author (<local-pdfs>/<key>.pdf),
an arXiv or open-access PDF from identity.json, the entry URL for web
references, then the record abstract. Writes sources/<key>.txt and
sources/index.json (access = full | web | abstract | none) in --out.
Claim-support agents read these first and may add sources they fetch.
"""

import argparse
import html
import os
import re
import subprocess
import tempfile
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from common import die, read_json, write_json

UA = {"User-Agent": "paper-integrity/0.1"}


def download(url, limit=60_000_000):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.headers.get("Content-Type", ""), r.read(limit)


def pdf_text(data):
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(data)
        f.flush()
        res = subprocess.run(["pdftotext", "-layout", f.name, "-"], capture_output=True,
                             text=True, timeout=180)
    return res.stdout


def html_text(raw):
    raw = re.sub(r"(?is)<(script|style|nav|header|footer)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</p>|</h\d>|</li>|</div>", "\n", raw)
    raw = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n\n", raw)).strip()


def candidates(key, info, local_dir):
    if local_dir:
        p = os.path.join(local_dir, f"{key}.pdf")
        if os.path.exists(p):
            yield "full", "local", p
    seen = set()
    for r in info.get("records", []):
        for url in [r.get("oa_pdf")] + [v.get("pdf") for v in r.get("venues", [])]:
            if url and url not in seen:
                seen.add(url)
                yield "full", "pdf", url
    if info.get("url"):
        yield "web", "url", info["url"]


def fetch(key, info, local_dir, src_dir):
    tried = []
    for access, kind, where in candidates(key, info, local_dir):
        try:
            if kind == "local":
                with open(where, "rb") as f:
                    text = pdf_text(f.read())
            else:
                ctype, data = download(where)
                if data[:5] == b"%PDF-" or "pdf" in ctype:
                    text, access = pdf_text(data), "full"
                else:
                    text = html_text(data.decode("utf-8", errors="replace"))
            if len(text) > 2000:
                with open(os.path.join(src_dir, f"{key}.txt"), "w") as f:
                    f.write(text)
                return key, {"access": access, "origin": where, "chars": len(text), "tried": tried}
            tried.append(f"{where}: too little text ({len(text)} chars)")
        except Exception as e:  # network or conversion failure; try the next source
            tried.append(f"{where}: {type(e).__name__}")
    abstract = next((r["abstract"] for r in info.get("records", []) if r.get("abstract")), None)
    if abstract:
        with open(os.path.join(src_dir, f"{key}.txt"), "w") as f:
            f.write(abstract)
        return key, {"access": "abstract", "origin": "record abstract", "chars": len(abstract),
                     "tried": tried}
    return key, {"access": "none", "origin": None, "chars": 0, "tried": tried}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True)
    ap.add_argument("--local-pdfs", help="dir of author-supplied <key>.pdf files")
    ap.add_argument("--keys", help="comma-separated subset")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()

    identity = read_json(os.path.join(args.out, "identity.json"))
    if identity is None:
        die("identity.json missing; run identity.py first")
    keys = list(identity)
    if args.keys:
        keys = [k for k in keys if k in set(args.keys.split(","))]
    src_dir = os.path.join(args.out, "sources")
    os.makedirs(src_dir, exist_ok=True)
    index = read_json(os.path.join(src_dir, "index.json"), {}) or {}
    todo = [k for k in keys if index.get(k, {}).get("access") not in ("full", "web")]
    with ThreadPoolExecutor(args.workers) as pool:
        for k, meta in pool.map(lambda k: fetch(k, identity[k], args.local_pdfs, src_dir), todo):
            index[k] = meta
    write_json(os.path.join(src_dir, "index.json"), index)
    counts = {}
    for k in keys:
        counts[index[k]["access"]] = counts.get(index[k]["access"], 0) + 1
    print("sources: " + " ".join(f"{a}={n}" for a, n in sorted(counts.items())))
    missing = [k for k in keys if index[k]["access"] in ("abstract", "none")]
    if missing:
        print("  no full text (supply <key>.pdf in --local-pdfs): " + ", ".join(missing))


if __name__ == "__main__":
    main()
