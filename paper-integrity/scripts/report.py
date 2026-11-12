#!/usr/bin/env python3
"""Stage 8: merge findings, apply verifier and author decisions, evaluate the
submission gate, and write report.md + report.json in --out.

Inputs in --out (all optional except what the level produced):
  findings-*.json   findings from scripts and agents (agents may omit "id")
  verdicts-*.json   per-use claim-support verdicts (coverage only)
  triage-*.json     reference triage results (fast and full), same format
                    as refute-*.json
  refute-*.json     stage-7 results: [{id, verdict: upheld|refuted|downgraded,
                    severity?, confirmed?, reason}]
  decisions.json    author decisions: {id: {status: cleared|fixed|dismissed, note}}
  run.json          level and script stages run (written by run.py)

Gate: FAIL if any S0 is open (verified or suspected). PASS only when the
claim-support, omission, and overlap stages all ran; otherwise NOT CERTIFIED.

Also writes summary.md, the results table shown to the user, and prints it.
"""

import argparse
import glob
import json
import os
import subprocess

from common import SEVERITY_ORDER, finding, read_json, write_json

STAGES = [
    ("1 mechanical", "findings-mechanical.json"),
    ("2 identity", "findings-identity.json"),
    ("2b triage", "triage-*.json"),
    ("3 ledger", "ledger.jsonl"),
    ("4 claim support", "verdicts-*.json"),
    ("5 omission", "findings-omission-*.json"),
    ("6 overlap", "findings-overlap.json"),
    ("7 refute", "refute-*.json"),
]
LEGEND = ("Severity: S0 blocks submission, S1 major (lowers reviewer trust), S2 minor polish. "
          "Confidence: verified = a source record or quoted passage shows the defect; "
          "suspected = a heuristic or failed search points to it, unconfirmed; "
          "no-access = the source could not be read.")
S0_CLASSES = {"4 claim support": "claim contradiction, misattribution",
              "5 omission": "uncited borrowed work",
              "6 overlap": "copied text"}


def revision(paper_dir):
    try:
        rev = subprocess.run(["git", "-C", paper_dir, "rev-parse", "--short", "HEAD"],
                             capture_output=True, text=True).stdout.strip()
        dirty = subprocess.run(["git", "-C", paper_dir, "status", "--porcelain", "--untracked-files=no"],
                               capture_output=True, text=True).stdout.strip()
        return f"{rev}{' + uncommitted changes' if dirty else ''}" if rev else "unknown"
    except FileNotFoundError:
        return "unknown"


def cell(s):
    return str(s or "").replace("|", "\\|").replace("\n", " ")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True)
    ap.add_argument("--paper-dir", required=True)
    ap.add_argument("--previous", help="earlier run dir; carries statuses forward")
    ap.add_argument("--decisions", help="author decisions file (default: <out>/decisions.json)")
    args = ap.parse_args()

    run = read_json(os.path.join(args.out, "run.json"), {}) or {}
    ran = {name: bool(glob.glob(os.path.join(args.out, pat))) for name, pat in STAGES}

    findings = []
    for path in sorted(glob.glob(os.path.join(args.out, "findings-*.json"))):
        for f in read_json(path, []):
            if "id" not in f:  # agent output: derive the stable ID here
                f = dict(finding(f["stage"], f["severity"], f["confidence"], f["category"],
                                 f["anchor"], f["location"], f["evidence"], f["suggestion"],
                                 f.get("key")), **{k: v for k, v in f.items() if k == "use_id"})
            f["status"] = "open"
            f["notes"] = []
            findings.append(f)
    by_id = {}
    for f in findings:  # one row per ID; repeated detections merge
        by_id.setdefault(f["id"], f)
    findings = list(by_id.values())

    for path in sorted(glob.glob(os.path.join(args.out, "triage-*.json"))) + \
            sorted(glob.glob(os.path.join(args.out, "refute-*.json"))):
        for r in read_json(path, []):
            f = by_id.get(r.get("id"))
            if not f:
                continue
            who = "triage" if os.path.basename(path).startswith("triage") else "verifier"
            f["notes"].append(f"{who}: {r['verdict']}: {r.get('reason', '')}")
            if r["verdict"] == "refuted":
                f["status"] = "refuted"
            elif r["verdict"] == "downgraded" and r.get("severity") in SEVERITY_ORDER:
                f["severity"] = r["severity"]
            elif r["verdict"] == "upheld" and f["confidence"] == "suspected" and r.get("confirmed"):
                f["confidence"] = "verified"

    if args.previous:
        prev = {f["id"]: f for f in (read_json(os.path.join(args.previous, "report.json"), {}) or {}).get("findings", [])}
        for f in findings:
            p = prev.get(f["id"])
            if p and p["status"] in ("cleared", "dismissed", "refuted"):
                f["status"] = p["status"]
                f["notes"] += [n for n in p.get("notes", []) if n.startswith(("author", "verifier", "triage"))]
            elif p and p["status"] == "fixed":
                f["notes"].append("reopened: marked fixed in the previous run but detected again")
    decisions = read_json(args.decisions or os.path.join(args.out, "decisions.json"), {}) or {}
    for fid, d in decisions.items():
        if fid in by_id:
            by_id[fid]["status"] = d["status"]
            by_id[fid]["notes"].append(f"author: {d.get('note', '')}")

    open_ = [f for f in findings if f["status"] == "open"]
    open_s0 = [f for f in open_ if f["severity"] == "S0"]
    unchecked = [f"{s} ({c})" for s, c in S0_CLASSES.items() if not ran[s]]
    if open_s0:
        gate = f"FAIL: {len(open_s0)} open S0 finding(s)."
    elif unchecked:
        gate = ("NOT CERTIFIED: no open S0 in the checked classes, but these stages did not "
                "run: " + "; ".join(unchecked) + ".")
    else:
        gate = "PASS: no open S0, and every S0 class was checked."

    verdicts = []
    for path in glob.glob(os.path.join(args.out, "verdicts-*.json")):
        verdicts += read_json(path, [])
    vcount = {}
    for v in verdicts:
        vcount[v.get("verdict")] = vcount.get(v.get("verdict"), 0) + 1
    uses = 0
    if os.path.exists(os.path.join(args.out, "ledger.jsonl")):
        with open(os.path.join(args.out, "ledger.jsonl")) as fh:
            uses = sum(1 for l in fh if l.strip())
    sources = read_json(os.path.join(args.out, "sources", "index.json"), {}) or {}
    for path in sorted(glob.glob(os.path.join(args.out, "sources", "agent-*.json"))):
        sources.update(read_json(path, {}) or {})  # sources the claim agents fetched
    access = {}
    for s in sources.values():
        access[s["access"]] = access.get(s["access"], 0) + 1

    key = lambda f: (SEVERITY_ORDER[f["severity"]], f["confidence"] != "verified", f["category"], f["location"])
    lines = [
        "# Citation integrity report", "",
        f"- Paper: `{args.paper_dir}` at revision {revision(args.paper_dir)}",
        f"- Level: {run.get('level', 'unknown')}",
        f"- **Gate: {gate}**", "",
        "## Coverage", "",
        "| Stage | Ran |", "| --- | --- |",
    ] + [f"| {name} | {'yes' if ran[name] else 'no'} |" for name, _ in STAGES] + [
        "",
        f"- Citation uses: {uses}; claim-support verdicts: {len(verdicts)}"
        + (f" ({', '.join(f'{k}={n}' for k, n in sorted(vcount.items()))})" if vcount else ""),
        "- Source access: " + (", ".join(f"{k}={n}" for k, n in sorted(access.items())) or "not fetched"),
    ] + [f"- Note: {n}" for n in run.get("notes", [])] + ["", "## Open findings", ""]
    header = [LEGEND, "",
              "| ID | Severity | Confidence | Category | Location | Evidence | Suggested action |",
              "| --- | --- | --- | --- | --- | --- | --- |"]
    if open_:
        lines += header + [
            f"| {f['id']} | {f['severity']} | {f['confidence']} | {f['category']} | "
            f"{cell(f['location'])} | {cell(f['evidence'])} | {cell(f['suggestion'])} |"
            for f in sorted(open_, key=key)]
    else:
        lines.append("None.")
    closed = [f for f in findings if f["status"] != "open"]
    if closed:
        lines += ["", "## Closed findings", "",
                  "| ID | Severity | Status | Category | Location | Notes |", "| --- | --- | --- | --- | --- | --- |"]
        lines += [f"| {f['id']} | {f['severity']} | {f['status']} | {f['category']} | "
                  f"{cell(f['location'])} | {cell('; '.join(f['notes']))} |" for f in sorted(closed, key=key)]
    counts = {s: sum(1 for f in open_ if f["severity"] == s) for s in SEVERITY_ORDER}
    lines += ["", "## Summary", "",
              "Open: " + ", ".join(f"{s}={n}" for s, n in counts.items())
              + f"; closed: {len(closed)}.",
              "", "To clear a finding, add `{\"<id>\": {\"status\": \"cleared|fixed|dismissed\", "
              "\"note\": \"...\"}}` to decisions.json and rerun report.py."]
    with open(os.path.join(args.out, "report.md"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    write_json(os.path.join(args.out, "report.json"), {"gate": gate, "ran": ran, "findings": findings})
    summary = render_summary(args.out, run, gate, findings, open_, ran, uses, verdicts, access, key)
    with open(os.path.join(args.out, "summary.md"), "w") as fh:
        fh.write(summary)
    print(summary)


def short(s, n=180):
    s = cell(s)
    return s if len(s) <= n else s[:n - 1].rstrip() + "…"


def render_summary(out, run, gate, findings, open_, ran, uses, verdicts, access, key):
    """The results table for the user: gate, counts, every open S0/S1, S2 by
    category, and what only the author can do."""
    closed = [f for f in findings if f["status"] != "open"]
    lines = [f"**Citation check ({run.get('level', '?')}): {gate}**", "",
             "| Severity | Open | Closed |", "| --- | --- | --- |"]
    for s, label in (("S0", "S0 blocker"), ("S1", "S1 major"), ("S2", "S2 minor")):
        lines.append(f"| {label} | {sum(f['severity'] == s for f in open_)} | "
                     f"{sum(f['severity'] == s for f in closed)} |")
    major = sorted([f for f in open_ if f["severity"] in ("S0", "S1")], key=key)
    lines += ["", "**Open S0 and S1**", ""]
    if major:
        lines += [LEGEND, "",
                  "| # | Severity | Confidence | Citation key | Location | Problem | Action |",
                  "| --- | --- | --- | --- | --- | --- | --- |"]
        lines += [f"| {i} | {f['severity']} | {f['confidence']} | `{f.get('key') or '-'}` | "
                  f"{cell(f['location'])} | {short(f['evidence'])} | {short(f['suggestion'], 100)} |"
                  for i, f in enumerate(major, 1)]
    else:
        lines.append("None.")
    minor = [f for f in open_ if f["severity"] == "S2"]
    if minor:
        cats = {}
        for f in minor:
            cats.setdefault(f["category"], []).append(f.get("key") or "-")
        lines += ["", "**Open S2 by category**", "", "| Category | Count | Citations |",
                  "| --- | --- | --- |"]
        lines += [f"| {c} | {len(ks)} | {short(', '.join(sorted(set(ks))), 160)} |"
                  for c, ks in sorted(cats.items(), key=lambda x: -len(x[1]))]
    pdfs = sorted({f.get("key") for f in open_ if f["confidence"] == "no-access" and f.get("key")})
    confirm = sorted({f.get("key") for f in open_ if f["category"] in
                      ("not-located", "identifier-unresolved", "dead-link")
                      and f["severity"] in ("S0", "S1") and f.get("key")})
    if pdfs or confirm:
        lines += ["", "**Needs you**", ""]
        if pdfs:
            lines.append(f"- Supply PDFs (`<key>.pdf` in the local PDF dir): {', '.join(pdfs)}")
        if confirm:
            lines.append(f"- Confirm these references exist or fix their locator: {', '.join(confirm)}")
    skipped = [n for n, r in ran.items() if not r]
    lines += ["", f"Coverage: {uses} citation uses; claim verdicts {len(verdicts)}; sources "
              + (", ".join(f"{k}={n}" for k, n in sorted(access.items())) or "not fetched")
              + (f"; not run: {', '.join(skipped)}" if skipped else "; all stages ran")
              + f". Full report: `{os.path.join(out, 'report.md')}`.", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    main()
