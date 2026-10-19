#!/usr/bin/env python3
"""Split agent work into balanced batches so all agents of a stage can be
launched at once.

  triage   open suspected S0/S1 reference findings from identity.py
           (fast and full); one batch = finding ids
  claims   cited keys, co-cited keys kept together, balanced by use count
  omission manuscript files grouped by top-level section, balanced by sentences
  refute   open S0/S1 findings still needing an independent check

Prints JSON: [{"batch": "<name>", "items": [...], "weight": n}, ...].
Run report.py first for triage and refute (they read report.json).
"""

import argparse
import json
import os

from common import die, read_json

TRIAGE_CATEGORIES = {"not-located", "identifier-unresolved", "dead-link", "venue-mismatch",
                     "author-mismatch", "year-mismatch", "preprint-has-published-version"}


def pack(weighted, n):
    """Greedy balance of (item, weight) into at most n bins."""
    bins = [[] for _ in range(max(1, min(n, len(weighted))))]
    load = [0] * len(bins)
    for item, w in sorted(weighted, key=lambda x: -x[1]):
        i = load.index(min(load))
        bins[i].append(item)
        load[i] += w
    return [(b, l) for b, l in zip(bins, load) if b]


def load_jsonl(path):
    if not os.path.exists(path):
        die(f"{os.path.basename(path)} missing; run ledger.py first")
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("stage", choices=("triage", "claims", "omission", "refute"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-agents", type=int)
    ap.add_argument("--keys", help="limit claims to these keys")
    args = ap.parse_args()
    n = args.max_agents or {"triage": 4, "claims": 8, "omission": 4, "refute": 4}[args.stage]

    if args.stage in ("triage", "refute"):
        report = read_json(os.path.join(args.out, "report.json"))
        if report is None:
            die("report.json missing; run report.py first")
        open_ = [f for f in report["findings"] if f["status"] == "open"
                 and f["severity"] in ("S0", "S1")]
        if args.stage == "triage":
            todo = [f for f in open_ if f["stage"] == "I" and f["confidence"] == "suspected"
                    and f["category"] in TRIAGE_CATEGORIES]
        else:
            triaged = {r["id"] for p in os.listdir(args.out) if p.startswith("triage-")
                       for r in read_json(os.path.join(args.out, p), [])}
            todo = [f for f in open_ if f["stage"] not in ("M",)
                    and not (f["stage"] == "I" and f["confidence"] == "verified")
                    and f["id"] not in triaged]
        batches = pack([(f["id"], 1) for f in todo], n)
    elif args.stage == "claims":
        uses = load_jsonl(os.path.join(args.out, "ledger.jsonl"))
        if args.keys:
            uses = [u for u in uses if u["key"] in set(args.keys.split(","))]
        parent = {}

        def find(k):
            parent.setdefault(k, k)
            while parent[k] != k:
                parent[k] = parent[parent[k]]
                k = parent[k]
            return k
        count = {}
        for u in uses:
            count[u["key"]] = count.get(u["key"], 0) + 1
            for c in u["co_cited"]:
                if c in count or not args.keys or c in args.keys.split(","):
                    parent[find(u["key"])] = find(c)
        groups = {}
        for k in count:
            groups.setdefault(find(k), []).append(k)
        # A co-citation cluster larger than a fair share is split by key.
        share = max(1, sum(count.values()) // n)
        units = []
        for ks in groups.values():
            w = sum(count[k] for k in ks)
            units += [(ks, w)] if w <= share else [([k], count[k]) for k in ks]
        batches = [([k for ks in b for k in ks], w) for b, w in pack(units, n)]
    else:
        sents = load_jsonl(os.path.join(args.out, "sentences.jsonl"))
        by_part = {}
        for s in sents:
            f = s["location"].split(":")[0]
            parts = f.split("/")
            part = parts[1] if len(parts) > 2 else os.path.splitext(parts[-1])[0]
            by_part.setdefault(part, {}).setdefault(f, 0)
            by_part[part][f] += 1
        units = [(sorted(files), sum(files.values())) for files in by_part.values()]
        batches = [([f for fs in b for f in fs], w) for b, w in pack(units, n)]

    print(json.dumps([{"batch": f"{args.stage}{i}", "items": items, "weight": w}
                      for i, (items, w) in enumerate(batches, 1)], indent=1))


if __name__ == "__main__":
    main()
