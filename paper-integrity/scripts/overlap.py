#!/usr/bin/env python3
"""Stage 6: verbatim text overlap between the manuscript and fetched sources.

Compares every manuscript sentence (sentences.jsonl from ledger.py) with every
text in sources/ using word 8-gram shingles. A run of --min-words or more
shared consecutive words outside quotation marks is a suspected S0
(copied text without quotation). This only covers sources that were fetched;
it does not replace a plagiarism service.

Writes findings-overlap.json in --out.
"""

import argparse
import json
import os
import re

from common import die, finding, summarize, write_json

N = 8


def words(s):
    return re.findall(r"[a-z0-9]+", s.lower())


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True)
    ap.add_argument("--min-words", type=int, default=12)
    args = ap.parse_args()

    sent_path = os.path.join(args.out, "sentences.jsonl")
    src_dir = os.path.join(args.out, "sources")
    if not os.path.exists(sent_path) or not os.path.isdir(src_dir):
        die("run ledger.py and fetch_sources.py first")
    with open(sent_path) as f:
        sentences = [json.loads(l) for l in f if l.strip()]

    shingles = {}  # 8-gram -> set of source keys
    for name in sorted(os.listdir(src_dir)):
        if not name.endswith(".txt"):
            continue
        key = name[:-4]
        w = words(open(os.path.join(src_dir, name), errors="replace").read())
        for i in range(len(w) - N + 1):
            shingles.setdefault(" ".join(w[i:i + N]), set()).add(key)

    findings = []
    for s in sentences:
        text = re.sub(r"``.*?''|\".*?\"", " ", s["text"])  # quoted text is fine
        w = words(text)
        if len(w) < args.min_words:
            continue
        best = {}  # key -> (run length, start)
        run = {}
        for i in range(len(w) - N + 1):
            hit = shingles.get(" ".join(w[i:i + N]), set())
            for k in hit:
                run[k] = run.get(k, 0) + 1
                length = run[k] + N - 1
                if length > best.get(k, (0, 0))[0]:
                    best[k] = (length, i - run[k] + 1)
            for k in list(run):
                if k not in hit:
                    del run[k]
        for k, (length, start) in best.items():
            if length >= args.min_words:
                span = " ".join(w[start:start + length])
                findings.append(finding(
                    "O", "S0", "suspected", "verbatim-overlap", f"{s['sid']}|{k}", s["location"],
                    f"{length} consecutive words match source `{k}`: \"{span}\". "
                    f"Sentence: {s['text']}",
                    "Rewrite in our own words, or quote and cite the source. Dismiss if the "
                    "phrase is a standard name or definition.", k))
    write_json(os.path.join(args.out, "findings-overlap.json"), findings)
    summarize("overlap", findings)


if __name__ == "__main__":
    main()
