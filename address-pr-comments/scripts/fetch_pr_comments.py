#!/usr/bin/env python3
"""Fetch every review comment on a GitHub pull request into one Markdown file.

Uses the GitHub GraphQL API through `gh api graphql` (read-only) and paginates
every connection: PR metadata, PR-level comments, review summaries, review
threads, and every reply in each thread. GitHub-resolved threads are hidden by
default; the header reports how many were hidden.

Usage:
  fetch_pr_comments.py [PR] [--repo OWNER/NAME] [--out FILE] [--json FILE]
                       [--include-resolved]
  fetch_pr_comments.py --from-json FILE [--out FILE] [--include-resolved]

  PR                  PR number or URL; default: the PR of the current branch
  --repo OWNER/NAME   repository; default: from the URL, else the current repo
  --out FILE          Markdown output (default: <repo root>/_docs/scratch/pr-reviews/PR_REVIEW_COMMENTS.md)
  --json FILE         also save the raw fetched data as JSON
  --from-json FILE    format a previously saved JSON instead of fetching
  --include-resolved  keep GitHub-resolved threads, marked as resolved

Requires an authenticated `gh` (`gh auth status`). Exit status: 0 on success,
1 on a fetch or input error (the error is printed verbatim), 2 on usage error.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PR_QUERY = """
query($owner: String!, $name: String!, $number: Int!) {
  repository(owner: $owner, name: $name) {
    pullRequest(number: $number) {
      number title url state isDraft createdAt
      author { __typename login }
      baseRefName headRefName headRefOid
    }
  }
}
"""

CONNECTION_QUERIES = {
    "comments": """
query($owner: String!, $name: String!, $number: Int!, $cursor: String) {
  repository(owner: $owner, name: $name) { pullRequest(number: $number) {
    comments(first: 100, after: $cursor) {
      pageInfo { hasNextPage endCursor }
      nodes { author { __typename login } createdAt body url }
    }
  } }
}
""",
    "reviews": """
query($owner: String!, $name: String!, $number: Int!, $cursor: String) {
  repository(owner: $owner, name: $name) { pullRequest(number: $number) {
    reviews(first: 100, after: $cursor) {
      pageInfo { hasNextPage endCursor }
      nodes { author { __typename login } state submittedAt body url }
    }
  } }
}
""",
    "reviewThreads": """
query($owner: String!, $name: String!, $number: Int!, $cursor: String) {
  repository(owner: $owner, name: $name) { pullRequest(number: $number) {
    reviewThreads(first: 50, after: $cursor) {
      pageInfo { hasNextPage endCursor }
      nodes {
        id isResolved isOutdated path line originalLine startLine originalStartLine
        resolvedBy { login }
        comments(first: 100) {
          pageInfo { hasNextPage endCursor }
          nodes { %s }
        }
      }
    }
  } }
}
""",
}

THREAD_COMMENT_FIELDS = (
    "author { __typename login } createdAt body url diffHunk "
    "originalCommit { oid } commit { oid }"
)
CONNECTION_QUERIES["reviewThreads"] %= THREAD_COMMENT_FIELDS

THREAD_COMMENTS_QUERY = """
query($id: ID!, $cursor: String) {
  node(id: $id) { ... on PullRequestReviewThread {
    comments(first: 100, after: $cursor) {
      pageInfo { hasNextPage endCursor }
      nodes { %s }
    }
  } }
}
""" % THREAD_COMMENT_FIELDS


class FetchError(RuntimeError):
    pass


def run(cmd: list[str]) -> str:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise FetchError(f"`{' '.join(cmd[:3])} …` failed: {proc.stderr.strip() or proc.stdout.strip()}")
    return proc.stdout


def graphql(query: str, **variables) -> dict:
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        if value is None:
            continue
        cmd += ["-F" if isinstance(value, int) else "-f", f"{key}={value}"]
    data = json.loads(run(cmd))
    if data.get("errors"):
        raise FetchError("GraphQL errors: " + "; ".join(e.get("message", str(e)) for e in data["errors"]))
    return data["data"]


def resolve_target(pr: str | None, repo: str | None) -> tuple[str, str, int]:
    number = None
    if pr:
        match = re.match(r"https?://[^/]+/([^/]+)/([^/]+)/pull/(\d+)", pr)
        if match:
            repo = repo or f"{match.group(1)}/{match.group(2)}"
            number = int(match.group(3))
        elif pr.lstrip("#").isdigit():
            number = int(pr.lstrip("#"))
        else:
            raise FetchError(f"not a PR number or URL: {pr}")
    if number is None:
        number = json.loads(run(["gh", "pr", "view", "--json", "number"]))["number"]
    if not repo:
        repo = run(["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"]).strip()
    owner, _, name = repo.partition("/")
    if not owner or not name:
        raise FetchError(f"--repo must be OWNER/NAME, got: {repo}")
    return owner, name, number


def fetch_connection(field: str, owner: str, name: str, number: int) -> list[dict]:
    nodes, cursor = [], None
    while True:
        data = graphql(CONNECTION_QUERIES[field], owner=owner, name=name, number=number, cursor=cursor)
        conn = data["repository"]["pullRequest"][field]
        nodes += conn["nodes"]
        if not conn["pageInfo"]["hasNextPage"]:
            return nodes
        cursor = conn["pageInfo"]["endCursor"]


def complete_thread(thread: dict) -> dict:
    conn = thread["comments"]
    comments = list(conn["nodes"])
    cursor = conn["pageInfo"]["endCursor"] if conn["pageInfo"]["hasNextPage"] else None
    while cursor:
        page = graphql(THREAD_COMMENTS_QUERY, id=thread["id"], cursor=cursor)["node"]["comments"]
        comments += page["nodes"]
        cursor = page["pageInfo"]["endCursor"] if page["pageInfo"]["hasNextPage"] else None
    thread = dict(thread)
    thread["comments"] = comments
    return thread


def fetch(owner: str, name: str, number: int) -> dict:
    pr = graphql(PR_QUERY, owner=owner, name=name, number=number)["repository"]["pullRequest"]
    if pr is None:
        raise FetchError(f"PR {owner}/{name}#{number} not found")
    return {
        "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repository": f"{owner}/{name}",
        "pr": pr,
        "comments": fetch_connection("comments", owner, name, number),
        "reviews": fetch_connection("reviews", owner, name, number),
        "threads": [complete_thread(t) for t in fetch_connection("reviewThreads", owner, name, number)],
    }


# ------------------------------------------------------------------ formatting

def who(author: dict | None) -> str:
    if not author:
        return "@ghost"
    login = author.get("login") or "ghost"
    is_bot = author.get("__typename") == "Bot" or login.endswith("[bot]")
    return f"@{login}" + (" (bot)" if is_bot else "")


def quote(body: str) -> str:
    body = (body or "").strip() or "(empty)"
    return "\n".join(f"> {line}" if line else ">" for line in body.splitlines())


def fence(text: str, lang: str = "") -> str:
    longest = max((len(m) for m in re.findall(r"`+", text)), default=0)
    ticks = "`" * max(3, longest + 1)
    return f"{ticks}{lang}\n{text.rstrip()}\n{ticks}"


def thread_line(thread: dict) -> int:
    for key in ("line", "originalLine", "startLine", "originalStartLine"):
        if thread.get(key):
            return thread[key]
    return 0


def render(data: dict, include_resolved: bool) -> str:
    pr = data["pr"]
    threads = sorted(data["threads"], key=lambda t: (t.get("path") or "", thread_line(t)))
    resolved = [t for t in threads if t.get("isResolved")]
    shown = threads if include_resolved else [t for t in threads if not t.get("isResolved")]

    pr_level = [("comment", c.get("createdAt") or "", c) for c in data["comments"]]
    pr_level += [("review", r.get("submittedAt") or "", r) for r in data["reviews"] if (r.get("body") or "").strip()]
    pr_level.sort(key=lambda item: item[1])

    hidden_note = (f"{len(resolved)} resolved thread(s) included and marked" if include_resolved
                   else f"{len(resolved)} resolved thread(s) hidden")
    out = [
        f"# PR {pr['number']} review comments — {pr['title']}",
        "",
        f"- **PR:** {pr['url']}",
        f"- **Repository:** {data.get('repository', '')}",
        f"- **State:** {pr['state'].lower()}{' (draft)' if pr.get('isDraft') else ''}",
        f"- **Author:** {who(pr.get('author'))}",
        f"- **Branch:** `{pr['headRefName']}` → `{pr['baseRefName']}`",
        f"- **Head commit:** `{pr['headRefOid']}`",
        f"- **Fetched:** {data['fetched_at']}",
        f"- **Counts:** {len(pr_level)} PR-level comment(s) and review summaries · "
        f"{len(shown)} review thread(s) shown · {hidden_note}",
        "",
        "## PR-level comments",
        "",
    ]
    if not pr_level:
        out += ["None.", ""]
    for kind, when, item in pr_level:
        label = "comment" if kind == "comment" else f"review summary ({item.get('state', '').lower()})"
        out += [f"### {who(item.get('author'))} — {label}, {when}", "", f"[link]({item.get('url', '')})", "",
                quote(item.get("body", "")), ""]

    out += ["## Review threads", "", "Sorted by file and line. Each thread shows the diff hunk the reviewer "
            "saw, then every comment in order.", ""]
    if not shown:
        out += ["None.", ""]
    for thread in shown:
        comments = thread["comments"]
        first = comments[0] if comments else {}
        flags = ["resolved" if thread.get("isResolved") else "unresolved"]
        if thread.get("isOutdated"):
            flags.append("outdated")
        line = thread.get("line") or f"{thread_line(thread)} (original)"
        out += [f"### `{thread.get('path')}:{line}` — {who(first.get('author'))}", "",
                f"- **State:** {', '.join(flags)}"
                + (f" (resolved by @{thread['resolvedBy']['login']})" if thread.get("resolvedBy") else ""),
                f"- **original_commit_id:** `{(first.get('originalCommit') or {}).get('oid', '')}`",
                f"- **Thread link:** [link]({first.get('url', '')})", ""]
        if first.get("diffHunk"):
            out += [fence(first["diffHunk"], "diff"), ""]
        for i, comment in enumerate(comments):
            role = "comment" if i == 0 else "reply"
            out += [f"**{who(comment.get('author'))}** — {role}, {comment.get('createdAt', '')} "
                    f"([link]({comment.get('url', '')}))", "", quote(comment.get("body", "")), ""]
    return "\n".join(out).rstrip() + "\n"


def default_out() -> Path:
    try:
        root = Path(run(["git", "rev-parse", "--show-toplevel"]).strip())
    except (FetchError, FileNotFoundError):
        root = Path.cwd()
    return root / "_docs" / "scratch" / "pr-reviews" / "PR_REVIEW_COMMENTS.md"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pr", nargs="?")
    ap.add_argument("--repo")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--json", type=Path, dest="json_out")
    ap.add_argument("--from-json", type=Path)
    ap.add_argument("--include-resolved", action="store_true")
    args = ap.parse_args(argv)
    try:
        if args.from_json:
            data = json.loads(args.from_json.read_text(encoding="utf-8"))
        else:
            data = fetch(*resolve_target(args.pr, args.repo))
            if args.json_out:
                args.json_out.parent.mkdir(parents=True, exist_ok=True)
                args.json_out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        text = render(data, args.include_resolved)
    except (FetchError, FileNotFoundError, json.JSONDecodeError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    out = args.out or default_out()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    resolved = sum(1 for t in data["threads"] if t.get("isResolved"))
    shown = len(data["threads"]) - (0 if args.include_resolved else resolved)
    print(f"wrote {out}: PR {data['pr']['number']}, {len(data['comments'])} PR-level comment(s), "
          f"{len(data['reviews'])} review(s), {shown} thread(s) shown, "
          f"{0 if args.include_resolved else resolved} resolved hidden")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
