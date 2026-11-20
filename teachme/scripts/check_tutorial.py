#!/usr/bin/env python3
"""Check a generated tutorial HTML file for the mechanically checkable rules.

Usage:
    check_tutorial.py TUTORIAL.html [--repo DIR] [--check-urls]

--repo DIR    repository the tutorial cites. Every code citation
              (`a.src[data-loc="path:12-30"]`) is checked against the file as
              it is at `source-commit` (not the working tree): the path stays
              inside the repository, the file exists, the lines are in range.
              Required for repo tutorials.
--check-urls  fetch every http(s) link and report the ones that fail.

Exit status is 1 when any error is reported, 0 otherwise (warnings alone do
not fail), and 2 on usage error.

Errors:
  empty        file missing, empty, or without a <main>
  meta         <html data-kind> not repo/concept/research; tutorial-subject
               missing; tutorial-generated not YYYY-MM-DD
  placeholder  template placeholder left ({{...}}, TODO, TBD, lorem ipsum)
               outside code (<code>) and, for {{...}} only, Mermaid blocks
  section      required section id missing (objectives, prerequisites,
               big-picture, summary, glossary, further-reading; walkthrough
               for repo tutorials); no section.lesson; a lesson without
               exactly one <h2>
  check        a lesson without a details.check, or a check without a
               summary question or a non-empty .answer
  anchor       in-page #link with no matching id
  link         relative or file:// link that does not resolve on disk
  url          (--check-urls) http(s) link that does not load
  reading      further-reading has no link
  commit       repo tutorial whose source-commit is missing, not a full hash,
               or (with --repo) not a commit in the repository
  citation     bad data-loc syntax, a path outside the repository, or (with
               --repo) a file missing at source-commit or a range past its end
  glossary     glossary has no entries, or a <dfn id="d-x"> without a
               glossary entry <dt id="g-x">

Warnings:
  lessons      fewer than 3 or more than 7 lessons
  term-unused  glossary entry with no <dfn> and no link to it
  citations    repo tutorial with no code citations at all

It cannot judge whether the teaching is correct or clear. A clean run means
no structural defects, not a sound tutorial.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

REQUIRED = ["objectives", "prerequisites", "big-picture", "summary", "glossary", "further-reading"]
KINDS = {"repo", "concept", "research"}
TODO_RE = re.compile(r"\bTODO\b|\bTBD\b|lorem ipsum", re.I)
BRACE_RE = re.compile(r"\{\{[^}]*\}\}")
LOC_RE = re.compile(r"^(?P<path>[^:]+):(?P<start>\d+)(?:-(?P<end>\d+))?$")
HASH_RE = re.compile(r"^[0-9a-f]{40}([0-9a-f]{24})?$")
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Node:
    def __init__(self, tag: str, attrs: dict[str, str], parent: "Node | None"):
        self.tag, self.attrs, self.parent = tag, attrs, parent
        self.children: list[Node] = []
        self.text: list[str] = []

    def classes(self) -> set[str]:
        return set(self.attrs.get("class", "").split())

    def iter(self):
        yield self
        for c in self.children:
            yield from c.iter()

    def all_text(self) -> str:
        return " ".join(t for n in self.iter() for t in n.text).strip()


class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", {}, None)
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        node = Node(tag, {k: v or "" for k, v in attrs}, self.cur)
        self.cur.children.append(node)
        if tag not in VOID:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, {k: v or "" for k, v in attrs}, self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent

    def handle_data(self, data):
        if self.cur.tag not in ("script", "style"):
            self.cur.text.append(data)


def blank(pattern: str, text: str, keep_groups: bool = False) -> str:
    """Blank out matches but keep their newlines, so reported line numbers stay right."""
    def repl(m: re.Match) -> str:
        if keep_groups:
            inner = m.group(2)
            return m.group(1) + re.sub(r"[^\n]", " ", inner) + m.group(3)
        return re.sub(r"[^\n]", " ", m.group(0))
    return re.sub(pattern, repl, text, flags=re.S | re.I)


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)


def check_placeholders(raw: str, errors: list[str]) -> None:
    text = blank(r"<!--.*?-->", raw)
    text = blank(r"<script\b.*?</script>", text)
    text = blank(r"(<code\b[^>]*>)(.*?)(</code>)", text, keep_groups=True)
    no_mermaid = blank(r"(<pre\b[^>]*class=\"[^\"]*\bmermaid\b[^\"]*\"[^>]*>)(.*?)(</pre>)", text, keep_groups=True)
    hits = [(m.start(), m.group(0)) for m in TODO_RE.finditer(text)]
    hits += [(m.start(), m.group(0)) for m in BRACE_RE.finditer(no_mermaid)]
    for pos, s in sorted(hits):
        errors.append(f"placeholder: {s!r} at line {text.count(chr(10), 0, pos) + 1}")


def check(path: Path, repo: Path | None, check_urls: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not path.is_file() or not path.read_text(encoding="utf-8").strip():
        return [f"empty: {path} is missing or empty"], warnings
    raw = path.read_text(encoding="utf-8")
    tb = TreeBuilder()
    tb.feed(raw)
    nodes = list(tb.root.iter())
    main = next((n for n in nodes if n.tag == "main"), None)
    if main is None:
        return ["empty: no <main> element"], warnings
    metas = {n.attrs.get("name"): n.attrs.get("content", "").strip() for n in nodes if n.tag == "meta"}

    html = next((n for n in nodes if n.tag == "html"), None)
    kind = html.attrs.get("data-kind", "") if html else ""
    if kind not in KINDS:
        errors.append(f"meta: <html data-kind> is {kind!r}, expected one of {sorted(KINDS)}")
    if not metas.get("tutorial-subject"):
        errors.append("meta: <meta name=\"tutorial-subject\"> missing or empty")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", metas.get("tutorial-generated") or ""):
        errors.append("meta: <meta name=\"tutorial-generated\"> missing or not YYYY-MM-DD")

    check_placeholders(raw, errors)

    ids = {n.attrs["id"] for n in nodes if "id" in n.attrs}
    for sid in REQUIRED + (["walkthrough"] if kind == "repo" else []):
        if sid not in ids:
            errors.append(f"section: required section id {sid!r} missing")

    lessons = [n for n in main.iter() if n.tag == "section" and "lesson" in n.classes()]
    if not lessons:
        errors.append("section: no <section class=\"lesson\">")
    elif not 3 <= len(lessons) <= 7:
        warnings.append(f"lessons: {len(lessons)} lessons; the skill expects 3-7 unless the user agreed otherwise")
    for lesson in lessons:
        name = lesson.attrs.get("id", "(no id)")
        h2s = [n for n in lesson.iter() if n.tag == "h2"]
        if len(h2s) != 1:
            errors.append(f"section: lesson {name!r} has {len(h2s)} <h2>, expected 1")
        checks = [n for n in lesson.iter() if n.tag == "details" and "check" in n.classes()]
        if not checks:
            errors.append(f"check: lesson {name!r} has no details.check")
        for i, c in enumerate(checks, 1):
            summary = next((n for n in c.iter() if n.tag == "summary"), None)
            answer = next((n for n in c.iter() if "answer" in n.classes()), None)
            if summary is None or not summary.all_text():
                errors.append(f"check: lesson {name!r} check {i} has no question in <summary>")
            if answer is None or not answer.all_text():
                errors.append(f"check: lesson {name!r} check {i} has no non-empty .answer")

    hrefs = [n.attrs["href"] for n in main.iter() if n.tag == "a" and n.attrs.get("href")]
    urls = set()
    for href in hrefs:
        scheme = urlparse(href).scheme
        if href.startswith("#"):
            if href[1:] not in ids:
                errors.append(f"anchor: {href} has no matching id")
        elif scheme == "file":
            if not Path(unquote(urlparse(href).path)).exists():
                errors.append(f"link: {href} does not exist")
        elif scheme in ("http", "https"):
            urls.add(href)
        elif not scheme:
            target = (path.parent / unquote(href.split("#")[0].split("?")[0])).resolve()
            if not target.exists():
                errors.append(f"link: {href} does not resolve from {path.parent}")
    if check_urls:
        for url in sorted(urls):
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 check_tutorial"})
            try:
                urllib.request.urlopen(req, timeout=15).close()
            except Exception as e:  # report every failure kind the same way
                errors.append(f"url: {url} failed: {e}")

    reading = next((n for n in nodes if n.attrs.get("id") == "further-reading"), None)
    if reading is not None and not any(n.tag == "a" and n.attrs.get("href") for n in reading.iter()):
        errors.append("reading: further-reading has no link")

    glossary = next((n for n in nodes if n.attrs.get("id") == "glossary"), None)
    if glossary is not None:
        terms = [n.attrs["id"] for n in glossary.iter() if n.tag == "dt" and n.attrs.get("id")]
        if not terms:
            errors.append("glossary: no <dt id=...> entries")
        dfns = {n.attrs.get("id", "") for n in main.iter() if n.tag == "dfn"}
        for d in sorted(dfns):
            if d.startswith("d-") and "g-" + d[2:] not in terms:
                errors.append(f"glossary: <dfn id={d!r}> has no glossary entry g-{d[2:]}")
        linked = {h[1:] for h in hrefs if h.startswith("#")}
        for t in terms:
            if t not in linked and "d-" + t[2:] not in dfns:
                warnings.append(f"term-unused: glossary entry {t!r} has no <dfn> and no link")

    commit = metas.get("source-commit", "")
    commit_ok = False
    if kind == "repo":
        if not HASH_RE.match(commit):
            errors.append(f"commit: source-commit {commit!r} is not a full commit hash")
        elif repo is not None:
            if git(repo, "cat-file", "-e", f"{commit}^{{commit}}").returncode != 0:
                errors.append(f"commit: {commit} is not a commit in {repo}")
            else:
                commit_ok = True

    cites = [n for n in main.iter() if n.tag == "a" and "src" in n.classes()]
    if kind == "repo" and not cites:
        warnings.append("citations: repo tutorial has no a.src code citations")
    if cites and repo is None:
        errors.append("citation: tutorial has code citations; pass --repo DIR to verify them")
    for c in cites:
        loc = c.attrs.get("data-loc", "")
        m = LOC_RE.match(loc)
        if not m:
            errors.append(f"citation: data-loc {loc!r} is not path:LINE or path:START-END")
            continue
        rel = Path(m["path"])
        if rel.is_absolute() or ".." in rel.parts:
            errors.append(f"citation: {loc} points outside the repository")
            continue
        if repo is None or (kind == "repo" and not commit_ok):
            continue
        if commit_ok:
            shown = git(repo, "show", f"{commit}:{rel.as_posix()}")
            if shown.returncode != 0:
                errors.append(f"citation: {rel} does not exist at {commit[:12]}")
                continue
            n_lines = len(shown.stdout.splitlines())
        else:
            f = repo / rel
            if not f.is_file():
                errors.append(f"citation: {rel} not found under {repo}")
                continue
            n_lines = len(f.read_text(encoding="utf-8", errors="replace").splitlines())
        start, end = int(m["start"]), int(m["end"] or m["start"])
        if not 1 <= start <= end <= n_lines:
            errors.append(f"citation: {loc} out of range ({rel} has {n_lines} lines)")
    return errors, warnings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("tutorial", type=Path)
    ap.add_argument("--repo", type=Path, help="repository root for verifying code citations")
    ap.add_argument("--check-urls", action="store_true", help="fetch every http(s) link")
    args = ap.parse_args()
    if args.repo is not None and not args.repo.is_dir():
        print(f"usage: --repo {args.repo} is not a directory", file=sys.stderr)
        return 2
    errors, warnings = check(args.tutorial, args.repo, args.check_urls)
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    print(f"{args.tutorial}: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
