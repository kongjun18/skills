#!/usr/bin/env python3
"""Print an HTML code citation and excerpt, copied from a file at a pinned commit.

Usage:
    excerpt.py --repo DIR --commit HASH --tutorial OUT.html PATH:START-END [--lang LANG]

Prints `<a class="src" ...>` followed by `<pre><code class="language-LANG">`
with the lines HTML-escaped, ready to paste into a tutorial. Trim lines by
hand afterwards if needed, leaving a comment marker where you cut.

The link is a GitHub permalink when the commit is on a remote branch of a
github.com remote; otherwise a relative path from the tutorial's directory to
the file in the working tree, with a warning on stderr when the working-tree
file differs from the pinned commit (the link would show other content).
"""

from __future__ import annotations

import argparse
import html
import os
import re
import subprocess
import sys
from pathlib import Path


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)


def permalink(repo: Path, commit: str, path: str, start: int, end: int) -> str | None:
    if not git(repo, "branch", "-r", "--contains", commit).stdout.strip():
        return None
    for remote in git(repo, "remote").stdout.split():
        url = git(repo, "remote", "get-url", remote).stdout.strip()
        m = re.match(r"^(?:https://github\.com/|git@github\.com:)([^/]+/[^/]+?)(?:\.git)?$", url)
        if m:
            return f"https://github.com/{m[1]}/blob/{commit}/{path}#L{start}-L{end}"
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("loc", help="path:START-END relative to the repository root")
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--commit", required=True)
    ap.add_argument("--tutorial", type=Path, required=True, help="the tutorial file, for relative links")
    ap.add_argument("--lang", default="")
    args = ap.parse_args()

    m = re.fullmatch(r"([^:]+):(\d+)(?:-(\d+))?", args.loc)
    if not m:
        print(f"error: {args.loc!r} is not path:START-END", file=sys.stderr)
        return 2
    path, start = m[1], int(m[2])
    end = int(m[3] or start)
    shown = git(args.repo, "show", f"{args.commit}:{path}")
    if shown.returncode != 0:
        print(f"error: {path} not found at {args.commit}: {shown.stderr.strip()}", file=sys.stderr)
        return 1
    lines = shown.stdout.splitlines()
    if not 1 <= start <= end <= len(lines):
        print(f"error: {args.loc} out of range ({path} has {len(lines)} lines)", file=sys.stderr)
        return 1

    href = permalink(args.repo, args.commit, path, start, end)
    if href is None:
        target = (args.repo / path).resolve()
        href = os.path.relpath(target, args.tutorial.resolve().parent)
        if not target.is_file() or target.read_text(encoding="utf-8", errors="replace") != shown.stdout:
            print(f"warning: working-tree {path} differs from {args.commit[:12]}; the link shows other content",
                  file=sys.stderr)

    label = f"{path}:{start}" + (f"–{end}" if end != start else "")
    code = html.escape("\n".join(lines[start - 1:end]), quote=False)
    lang = f' class="language-{args.lang}"' if args.lang else ""
    print(f'<a class="src" data-loc="{html.escape(args.loc)}" href="{html.escape(href)}">{html.escape(label)}</a>')
    print(f"<pre><code{lang}>{code}</code></pre>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
