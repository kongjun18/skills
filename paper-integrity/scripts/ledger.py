#!/usr/bin/env python3
"""Stage 3: citation-use ledger.

Expands the manuscript from its main file, then records every citation use
(key, sentence, section, file:line) with a stable ID, plus every sentence of
the paper for the overlap stage.

Outputs in --out: ledger.jsonl, sentences.jsonl, ledger.md.
"""

import argparse
import hashlib
import json
import os
import re

from common import latex_to_text

CITE_RE = re.compile(r"\\(no)?cite[a-zA-Z]*\*?\s*(?:\[[^\]]*\]\s*){0,2}\{([^}]*)\}")
INPUT_RE = re.compile(r"\\(?:input|include|subfile)\{([^}]*)\}")
SECTION_RE = re.compile(r"\\(section|subsection|subsubsection|paragraph)\*?\{([^}]*)\}")
ABBREV = ("e.g", "i.e", "et al", "etc", "vs", "cf", "fig", "figs", "sec", "secs",
          "eq", "tab", "no", "resp", "approx", "al")


def strip_comment(line):
    out, i = [], 0
    while i < len(line):
        c = line[i]
        if c == "\\" and i + 1 < len(line):
            out.append(line[i:i + 2])
            i += 2
            continue
        if c == "%":
            break
        out.append(c)
        i += 1
    return "".join(out)


def expand(path, paper_dir, lines, seen):
    """Append (file, lineno, text) for the document, following \\input."""
    if path in seen or not os.path.exists(path):
        return
    seen.add(path)
    rel = os.path.relpath(path, paper_dir)
    with open(path, errors="replace") as f:
        for n, raw in enumerate(f, 1):
            text = strip_comment(raw.rstrip("\n"))
            if "\\end{document}" in text:
                lines.append((rel, n, text.split("\\end{document}")[0]))
                return
            m = INPUT_RE.search(text)
            if m:
                lines.append((rel, n, text[:m.start()]))
                target = m.group(1).strip()
                if not target.endswith(".tex"):
                    target += ".tex"
                expand(os.path.join(paper_dir, target), paper_dir, lines, seen)
                lines.append((rel, n, text[m.end():]))
            else:
                lines.append((rel, n, text))


def split_sentences(text):
    """Return list of (start, end) offsets. Approximate on purpose: it only has
    to give each citation a readable clause."""
    spans, start = [], 0
    for m in re.finditer(r"[.!?](?:''|\")?\s+(?=[A-Z\\(`])", text):
        before = text[start:m.start()].split()
        last = before[-1].lower().rstrip(".") if before else ""
        if last in ABBREV or re.fullmatch(r"[a-z]", last):
            continue
        spans.append((start, m.end()))
        start = m.end()
    if text[start:].strip():
        spans.append((start, len(text)))
    return spans


def readable(s):
    s = CITE_RE.sub(lambda m: "[" + m.group(2).replace(" ", "") + "]", s)
    s = re.sub(r"\\(?:ref|cref|Cref|autoref|label)\{[^}]*\}", "#", s)
    return latex_to_text(s)


def build(paper_dir, main):
    lines = []
    expand(os.path.join(paper_dir, main), paper_dir, lines, set())

    # Body only; preamble lines carry no claims.
    for i, (_, _, t) in enumerate(lines):
        if "\\begin{document}" in t:
            lines = lines[i:]
            break

    # Paragraphs: runs of non-blank lines, keeping a char -> (file, line) map.
    paragraphs, cur, cur_map = [], [], []
    section = "(front matter)"
    for f, n, t in lines:
        sm = SECTION_RE.search(t)
        if sm:
            if cur:
                paragraphs.append(("".join(cur), cur_map, section))
                cur, cur_map = [], []
            section = latex_to_text(sm.group(2))
        if not t.strip():
            if cur:
                paragraphs.append(("".join(cur), cur_map, section))
                cur, cur_map = [], []
            continue
        cur_map.append((sum(len(x) for x in cur), f, n))
        cur.append(t.strip() + " ")
    if cur:
        paragraphs.append(("".join(cur), cur_map, section))

    def locate(cmap, offset):
        loc = cmap[0]
        for entry in cmap:
            if entry[0] <= offset:
                loc = entry
        return f"{loc[1]}:{loc[2]}"

    uses, sentences = [], []
    for text, cmap, section in paragraphs:
        spans = split_sentences(text)
        for idx, (a, b) in enumerate(spans):
            raw = text[a:b].strip()
            plain = readable(raw)
            loc = locate(cmap, a)
            sid = hashlib.sha1(plain.lower().encode()).hexdigest()[:8]
            sentences.append({"sid": sid, "location": loc, "section": section,
                              "text": plain})
            prev = readable(text[spans[idx - 1][0]:spans[idx - 1][1]]) if idx else ""
            for m in CITE_RE.finditer(raw):
                if m.group(1):  # \nocite
                    continue
                keys = [k.strip() for k in m.group(2).split(",") if k.strip()]
                for k in keys:
                    uid = hashlib.sha1(f"{k}|{plain.lower()}".encode()).hexdigest()[:8]
                    uses.append({
                        "use_id": f"U-{uid}",
                        "key": k,
                        "co_cited": [x for x in keys if x != k],
                        "location": locate(cmap, a + m.start()),
                        "section": section,
                        "sentence": plain,
                        "previous_sentence": prev,
                        "command": raw[m.start():m.end()],
                    })
    # Same key cited twice in one sentence -> one use.
    dedup = {}
    for u in uses:
        dedup.setdefault(u["use_id"], u)
    return list(dedup.values()), sentences


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--paper-dir", required=True)
    ap.add_argument("--main", default="main.tex")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    uses, sentences = build(args.paper_dir, args.main)
    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "ledger.jsonl"), "w") as f:
        for u in uses:
            f.write(json.dumps(u, ensure_ascii=False) + "\n")
    with open(os.path.join(args.out, "sentences.jsonl"), "w") as f:
        for s in sentences:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    by_key = {}
    for u in uses:
        by_key.setdefault(u["key"], []).append(u)
    with open(os.path.join(args.out, "ledger.md"), "w") as f:
        f.write(f"# Citation-use ledger\n\n{len(uses)} uses of {len(by_key)} keys.\n")
        for k in sorted(by_key):
            f.write(f"\n## {k} ({len(by_key[k])} uses)\n\n")
            for u in by_key[k]:
                co = f" (with {', '.join(u['co_cited'])})" if u["co_cited"] else ""
                f.write(f"- `{u['use_id']}` {u['location']}, {u['section']}{co}: "
                        f"{u['sentence']}\n")
    print(f"ledger: {len(uses)} citation uses of {len(by_key)} keys; "
          f"{len(sentences)} sentences")


if __name__ == "__main__":
    main()
