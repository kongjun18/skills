#!/usr/bin/env python3
"""Stage 1: mechanical citation checks (offline, seconds).

Reads the LaTeX log, BibTeX log, aux file, bibliography, rendered PDF, and the
citation ledger (run ledger.py first). Writes findings-mechanical.json and
coverage-mechanical.json in --out.
"""

import argparse
import json
import os
import re
import subprocess

from common import (die, find_build_file, finding, norm_title, parse_bib,
                    read_aux_bibdata, read_aux_citations, summarize, write_json)


def load_ledger(out):
    path = os.path.join(out, "ledger.jsonl")
    if not os.path.exists(path):
        die("ledger.jsonl missing; run ledger.py first")
    with open(path) as f:
        return [json.loads(l) for l in f if l.strip()]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--paper-dir", required=True)
    ap.add_argument("--main", default="main.tex")
    ap.add_argument("--build-dir", help="dir holding main.aux/.log/.blg/.pdf "
                    "(default: paper dir)")
    ap.add_argument("--bib", action="append", help="bibliography file(s); "
                    "default: \\bibdata from the aux file")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    stem = os.path.splitext(args.main)[0]
    aux = find_build_file(args.paper_dir, args.build_dir, stem, ".aux")
    log = find_build_file(args.paper_dir, args.build_dir, stem, ".log")
    blg = find_build_file(args.paper_dir, args.build_dir, stem, ".blg")
    pdf = find_build_file(args.paper_dir, args.build_dir, stem, ".pdf")
    ledger = load_ledger(args.out)
    findings, notes = [], []

    bibs = args.bib or [os.path.join(args.paper_dir, b if b.endswith(".bib") else b + ".bib")
                        for b in (read_aux_bibdata(aux) if aux else [])]
    if not bibs:
        die("no bibliography found; pass --bib")

    # Build freshness: an aux older than any source means the logs may be stale.
    if aux:
        aux_t = os.path.getmtime(aux)
        newer = [u["location"].split(":")[0] for u in ledger
                 if os.path.getmtime(os.path.join(args.paper_dir, u["location"].split(":")[0])) > aux_t]
        if newer:
            notes.append(f"build older than sources ({sorted(set(newer))[0]} and others); "
                         "log/PDF findings may be stale, rebuild first")
    else:
        notes.append("no aux file; build-dependent checks skipped")

    entries, occurrences = {}, []
    for b in bibs:
        e, o = parse_bib(b)
        rel = os.path.relpath(b, args.paper_dir)
        for k, v in e.items():
            v["file"] = rel
            entries.setdefault(k, v)
        occurrences += [(k, f"{rel}:{n}") for k, n in o]

    tex_keys = []
    for u in ledger:
        if u["key"] not in tex_keys:
            tex_keys.append(u["key"])
    aux_keys = read_aux_citations(aux) if aux else []
    cited = list(dict.fromkeys(tex_keys + aux_keys))

    # Duplicate keys: BibTeX keeps the first; a citation may render the wrong work.
    seen = {}
    for k, loc in occurrences:
        if k in seen:
            findings.append(finding(
                "M", "S1", "verified", "duplicate-key", k, f"{seen[k]}; {loc}",
                f"Key `{k}` is defined twice; BibTeX uses the first definition.",
                "Keep one definition and confirm it describes the intended work.", k))
        else:
            seen[k] = loc

    # Cited keys with no entry.
    for k in cited:
        if k not in entries:
            loc = next((u["location"] for u in ledger if u["key"] == k), "aux")
            findings.append(finding(
                "M", "S1", "verified", "missing-entry", k, loc,
                f"`{k}` is cited but not defined in {', '.join(os.path.relpath(b, args.paper_dir) for b in bibs)}.",
                "Add the entry from an authoritative record, or fix the key.", k))

    # Entries cited in more than one key for the same work.
    by_doi, by_title = {}, {}
    for k, e in entries.items():
        doi = e["fields"].get("doi", "").lower().strip()
        if doi:
            by_doi.setdefault(doi, []).append(k)
        t = norm_title(e["fields"].get("title", ""))
        if t:
            by_title.setdefault(t, []).append(k)
    for group, label in ((by_doi, "DOI"), (by_title, "title")):
        for value, keys in group.items():
            live = [k for k in keys if k in cited]
            if len(keys) > 1 and len(live) > 1:
                findings.append(finding(
                    "M", "S2", "verified", "duplicate-work", "|".join(sorted(keys)),
                    "; ".join(f"{entries[k]['file']}:{entries[k]['line']}" for k in keys),
                    f"Keys {', '.join(live)} share the same {label}; the bibliography lists the work twice.",
                    "Merge to one key.", live[0]))

    # Required fields on cited entries.
    for k in cited:
        e = entries.get(k)
        if not e:
            continue
        f = e["fields"]
        loc = f"{e['file']}:{e['line']}"
        missing = [x for x in ("title", "author") if not f.get(x) and not (x == "author" and f.get("editor"))]
        has_locator = bool(f.get("url") or f.get("doi")
                           or "http" in f.get("howpublished", "") + f.get("note", ""))
        if missing == ["author"] and e["type"] in ("misc", "online", "manual") and has_locator:
            # Project pages, manuals, and software often have no personal author.
            findings.append(finding(
                "M", "S2", "verified", "missing-field", f"{k}|author", loc,
                f"`{k}` ({e['type']}) has no author; acceptable for a web, software, or manual "
                "reference if the style renders the title and URL.",
                "Add an organization as author if the style needs one.", k))
        elif missing:
            findings.append(finding(
                "M", "S1", "verified", "missing-field", f"{k}|{'|'.join(missing)}", loc,
                f"`{k}` has no {' or '.join(missing)}; the rendered reference is incomplete.",
                "Fill the field from an authoritative record.", k))
        if not f.get("year") and not f.get("date"):
            findings.append(finding(
                "M", "S2", "verified", "missing-field", f"{k}|year", loc,
                f"`{k}` has no year.", "Add the year from an authoritative record.", k))
        if e["type"] in ("misc", "online", "manual", "techreport") and not (
                f.get("url") or f.get("doi") or "http" in f.get("howpublished", "") + f.get("note", "")):
            findings.append(finding(
                "M", "S2", "verified", "no-locator", k, loc,
                f"`{k}` ({e['type']}) has no URL or DOI, so readers cannot find it.",
                "Add a stable URL or DOI.", k))

    # LaTeX log: undefined citations.
    if log:
        with open(log, errors="replace") as fh:
            text = fh.read()
        undefined = sorted(set(re.findall(r"Citation `([^']+)' on page \d+ undefined", text)))
        if undefined:  # one row: these usually share a cause (failed BibTeX run, typo)
            findings.append(finding(
                "M", "S1", "verified", "undefined-citation", "log", os.path.relpath(log, args.paper_dir),
                f"LaTeX reports {len(undefined)} undefined citation(s), shown as [?] in the PDF: "
                + ", ".join(f"`{k}`" for k in undefined) + ".",
                "Check the BibTeX log for the cause, fix the keys or entries, then rebuild.",
                undefined[0] if len(undefined) == 1 else None))
    else:
        notes.append("no LaTeX log; undefined-citation check skipped")

    # BibTeX log.
    if blg:
        with open(blg, errors="replace") as fh:
            text = fh.read()
        for k in sorted(set(re.findall(r'I didn\'t find a database entry for "([^"]+)"', text))):
            findings.append(finding(
                "M", "S1", "verified", "missing-entry", k, os.path.relpath(blg, args.paper_dir),
                f"BibTeX found no entry for `{k}`.", "Fix the key or add the entry.", k))
        warns = {}
        for msg, k in re.findall(r"Warning--(.+?) in (\S+)\n", text):
            warns.setdefault(k, []).append(msg.strip())
        for k, msgs in sorted(warns.items()):
            findings.append(finding(
                "M", "S2", "verified", "bibtex-warning", k, os.path.relpath(blg, args.paper_dir),
                f"`{k}`: " + "; ".join(sorted(set(msgs))),
                "Complete or correct the fields BibTeX names.", k))
    else:
        notes.append("no BibTeX log; BibTeX warning check skipped")

    # Rendered PDF: unresolved markers.
    if pdf:
        try:
            text = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True,
                                  text=True, timeout=120).stdout
            hits = len(re.findall(r"\[\?\]|\[\?,|\(\?\)|\?\?", text))
            if hits and not any(f["category"] == "undefined-citation" for f in findings):
                findings.append(finding(
                    "M", "S1", "verified", "unresolved-marker", "pdf", os.path.relpath(pdf, args.paper_dir),
                    f"The rendered PDF contains {hits} unresolved marker(s) ([?], (?), or ??).",
                    "Search the PDF for the markers, fix the citations or references, and rebuild."))
        except (FileNotFoundError, subprocess.TimeoutExpired):
            notes.append("pdftotext unavailable; PDF marker check skipped")
    else:
        notes.append("no PDF; rendered-marker check skipped")

    uncited = sorted(k for k in entries if k not in cited)
    write_json(os.path.join(args.out, "findings-mechanical.json"), findings)
    write_json(os.path.join(args.out, "coverage-mechanical.json"), {
        "stage": "mechanical",
        "inputs": {"aux": aux, "log": log, "blg": blg, "pdf": pdf, "bib": bibs},
        "cited_keys": cited,
        "uncited_entries": uncited,
        "notes": notes,
    })
    summarize("mechanical", findings)
    print(f"  {len(cited)} cited keys, {len(uncited)} uncited entries (not rendered)")
    for n in notes:
        print(f"  note: {n}")


if __name__ == "__main__":
    main()
