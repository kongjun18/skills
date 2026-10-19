#!/usr/bin/env python3
"""Run the script stages for a level.

  offline: ledger, mechanical, report (no network, no agents)
  fast:    offline + identity, then stop for the triage agents;
           afterwards `run.py --finish`
  full:    fast + fetch_sources + overlap, then stop for the agent stages
           (triage, claim support, omission, refute); afterwards `run.py --finish`

`--finish` reruns overlap when sources were fetched, then the report.
"""

import argparse
import os
import subprocess
import sys

from common import read_json, write_json

HERE = os.path.dirname(os.path.abspath(__file__))
LEVELS = ("offline", "fast", "full")


def step(name, *argv):
    print(f"== {name}", flush=True)
    res = subprocess.run([sys.executable, os.path.join(HERE, name + ".py"), *argv])
    if res.returncode:
        sys.exit(f"{name} failed with exit code {res.returncode}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--level", choices=LEVELS)
    ap.add_argument("--finish", action="store_true", help="after the agent stages of fast or full")
    ap.add_argument("--paper-dir", required=True)
    ap.add_argument("--main", default="main.tex")
    ap.add_argument("--build-dir")
    ap.add_argument("--out", required=True)
    ap.add_argument("--cache", help="shared HTTP cache file")
    ap.add_argument("--local-pdfs")
    ap.add_argument("--keys", help="limit identity/fetch to these keys")
    ap.add_argument("--mailto")
    ap.add_argument("--previous", help="earlier run dir to carry statuses from")
    args = ap.parse_args()
    if not args.finish and not args.level:
        ap.error("--level is required unless --finish")

    os.makedirs(args.out, exist_ok=True)
    report = ["--out", args.out, "--paper-dir", args.paper_dir]
    if args.previous:
        report += ["--previous", args.previous]

    if args.finish:
        if os.path.isdir(os.path.join(args.out, "sources")):
            step("overlap", "--out", args.out)
        step("report", *report)
        return

    write_json(os.path.join(args.out, "run.json"), {"level": args.level})
    paper = ["--paper-dir", args.paper_dir]
    step("ledger", *paper, "--main", args.main, "--out", args.out)
    mech = [*paper, "--main", args.main, "--out", args.out]
    if args.build_dir:
        mech += ["--build-dir", args.build_dir]
    step("mechanical", *mech)
    if args.level in ("fast", "full"):
        ident = [*paper, "--out", args.out]
        for flag in ("cache", "keys", "mailto"):
            if getattr(args, flag):
                ident += [f"--{flag}", getattr(args, flag)]
        step("identity", *ident)
    if args.level == "full":
        fetch = ["--out", args.out]
        for flag in ("local_pdfs", "keys"):
            if getattr(args, flag):
                fetch += [f"--{flag.replace('_', '-')}", getattr(args, flag)]
        step("fetch_sources", *fetch)
        step("overlap", "--out", args.out)
    notes = (read_json(os.path.join(args.out, "coverage-mechanical.json"), {}) or {}).get("notes", [])
    write_json(os.path.join(args.out, "run.json"), {"level": args.level, "notes": notes})
    step("report", *report)
    if args.level != "offline":
        print(f"\nScript stages done. Run the {args.level} agent stages per SKILL.md, "
              "then: run.py --finish with the same --out.")


if __name__ == "__main__":
    main()
