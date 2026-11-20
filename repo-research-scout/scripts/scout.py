#!/usr/bin/env python3
"""Cached GitHub issue/PR census, tiered selection, and analysis store.

One SQLite database per GitHub repository holds the census (metadata and
bodies of every issue and PR updated inside the window, plus every open one),
comments fetched on demand, observed state changes, study selections, and
model analyses keyed by (study, stage, item, input hash, prompt version), so
nothing is re-pulled or re-analyzed unless it changed. A registry file indexes
the databases so peer repositories are reused across studies.

Storage follows the XDG base directories under agent-skills/repo-research-scout/:
  data  (${XDG_DATA_HOME:-~/.local/share})   source of truth: registry.json, db/
  state (${XDG_STATE_HOME:-~/.local/state})  per-study batches/ and results/ (resumable)
  cache (${XDG_CACHE_HOME:-~/.cache})        per-study metrics/ and digests/ (regenerable)
The study directory in the project (_docs/explorations/<date>-<slug>/) is a
view: study.toml, hypotheses.md, the report, and data/evidence.sqlite, which
`snapshot` exports from the source of truth. Data flows one way, into the view.

Model work happens outside this script: `export` writes batch files of cache
misses, the host agent analyzes them with the brief for the stage, and
`ingest` validates and stores the results.

Requires an authenticated `gh` and Python 3.11+. Standard library only.

Commands:
  sync      --study S | REPO [--window-months N]
  select    --study S [--repo R --query "kw1,kw2" --name NAME --limit N]
  export    --study S --stage t1|t2 [--max-items N] [--max-tokens N]
  ingest    --study S --batch B.json [RESULTS.jsonl] [--model M] [--effort E]
  metrics   --study S [--out DIR] | --from-snapshot EVIDENCE.sqlite --out DIR
  digest    --study S [--out DIR]
  verify    --study S                  checks <study dir>/hypotheses.md
  snapshot  --study S [--out FILE]     default <study dir>/data/evidence.sqlite
  status    --study S
  registry
"""

import argparse
import csv
import datetime as dt
import hashlib
import json
import math
import os
import re
import sqlite3
import statistics
import subprocess
import sys
import time
import tomllib
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
SKILLS_REPO = SKILL_DIR.parent
def xdg(var: str, default: str) -> Path:
    return Path(os.environ.get(var) or default).expanduser() / "agent-skills" / "repo-research-scout"


DATA = xdg("XDG_DATA_HOME", "~/.local/share")
STATE = xdg("XDG_STATE_HOME", "~/.local/state")
CACHE = xdg("XDG_CACHE_HOME", "~/.cache")
REGISTRY = DATA / "registry.json"
BRIEFS = {"t1": SKILL_DIR / "references" / "t1-triage.md",
          "t2": SKILL_DIR / "references" / "t2-analysis.md"}
MAINTAINER = {"OWNER", "MEMBER", "COLLABORATOR"}
MIN_QUOTE = 20

SCHEMA = """
CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY, v TEXT);
CREATE TABLE IF NOT EXISTS items(
  key TEXT PRIMARY KEY, repo TEXT, number INT, kind TEXT, title TEXT, body TEXT,
  url TEXT, state TEXT, state_reason TEXT, author TEXT, author_assoc TEXT,
  created_at TEXT, updated_at TEXT, closed_at TEXT, labels TEXT,
  n_comments INT, n_reactions INT, additions INT, deletions INT,
  files TEXT, links TEXT, first_seen TEXT, last_seen TEXT, comments_synced_at TEXT);
CREATE TABLE IF NOT EXISTS comments(
  id INTEGER PRIMARY KEY, item_key TEXT, author TEXT, author_assoc TEXT,
  created_at TEXT, body TEXT);
CREATE INDEX IF NOT EXISTS comments_item ON comments(item_key);
CREATE TABLE IF NOT EXISTS state_changes(
  item_key TEXT, observed_at TEXT, old_state TEXT, new_state TEXT);
CREATE TABLE IF NOT EXISTS syncs(
  id INTEGER PRIMARY KEY, repo TEXT, pass TEXT, started_at TEXT, finished_at TEXT,
  window_start TEXT, stop_at TEXT, fetched INT, gh_version TEXT);
CREATE VIRTUAL TABLE IF NOT EXISTS items_fts USING fts5(key UNINDEXED, title, body);
CREATE TABLE IF NOT EXISTS selections(
  study TEXT, item_key TEXT, direction TEXT, score REAL, selected_at TEXT,
  PRIMARY KEY(study, item_key, direction));
CREATE TABLE IF NOT EXISTS analyses(
  study TEXT, stage TEXT, item_key TEXT, input_hash TEXT, prompt_version TEXT,
  result TEXT, model TEXT, effort TEXT, ingested_at TEXT,
  PRIMARY KEY(study, stage, item_key, input_hash, prompt_version));
CREATE TABLE IF NOT EXISTS batches(
  id TEXT PRIMARY KEY, study TEXT, stage TEXT, created_at TEXT, n_items INT,
  est_tokens INT, prompt_version TEXT, path TEXT);
"""

ENUMS = {
    "t1": {"type": {"bug", "performance", "feature", "design", "question", "docs", "build", "other"}},
    "t2": {"root_cause": {"implementation-bug", "design-limit", "tradeoff", "missing-abstraction",
                          "usage-error", "unclear"},
           "resolution": {"fixed", "workaround", "wontfix", "open", "duplicate", "unclear"},
           "generality": {"implementation-specific", "system-class", "general", "unclear"}},
}
FIELDS = {
    "t1": {"directions": list, "component": str, "type": str, "escalate": bool, "reason": str},
    "t2": {"directions": list, "component": str, "symptom": str, "root_cause": str,
           "resolution": str, "workload": str, "maintainer_position": str, "generality": str,
           "generality_reason": str, "quotes": list, "summary": str},
}


# ---------- utilities ----------

def now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha(text: str, n: int = 16) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:n]


def norm(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).casefold()
    text = text.translate(str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"'}))
    return re.sub(r"\s+", " ", text).strip()


def days_between(a: str, b: str) -> float:
    fa = dt.datetime.fromisoformat(a.replace("Z", "+00:00"))
    fb = dt.datetime.fromisoformat(b.replace("Z", "+00:00"))
    return (fb - fa).total_seconds() / 86400


def quarter(ts: str) -> str:
    return f"{ts[:4]}Q{(int(ts[5:7]) - 1) // 3 + 1}"


def months_ago(months: int) -> str:
    today = dt.date.today()
    y, m = divmod(today.year * 12 + today.month - 1 - months, 12)
    return f"{y:04d}-{m + 1:02d}-01T00:00:00Z"


def gh_graphql(query: str, **variables) -> dict:
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    for k, v in variables.items():
        if v is not None:
            cmd += ["-f", f"{k}={v}"]
    for attempt in range(4):
        p = subprocess.run(cmd, capture_output=True, text=True)
        if p.returncode == 0:
            data = json.loads(p.stdout)
            if "errors" not in data:
                return data["data"]
            err = json.dumps(data["errors"])[:500]
        else:
            err = p.stderr.strip()[:500]
        time.sleep(5 * 2 ** attempt)
    raise SystemExit(f"gh graphql failed after retries: {err}")


def gh_version() -> str:
    return subprocess.check_output(["gh", "--version"], text=True).splitlines()[0]


# ---------- registry and databases ----------

def load_registry() -> dict:
    return json.loads(REGISTRY.read_text()) if REGISTRY.exists() else {}


def save_registry(reg: dict) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text(json.dumps(reg, indent=2, sort_keys=True) + "\n")


def db_path(repo: str, create: bool = False) -> Path:
    path = DATA / "db" / (repo.replace("/", "__") + ".sqlite")
    if path.exists():
        return path
    if not create:
        raise SystemExit(f"{repo} has no database; run: scout.py sync {repo}")
    if path.resolve().is_relative_to(SKILLS_REPO.resolve()):
        raise SystemExit("refusing to write a database inside the skills repository")
    path.parent.mkdir(parents=True, exist_ok=True)
    reg = load_registry()
    reg[repo] = {"db": str(path), "registered_at": now()}
    save_registry(reg)
    return path


def connect(repo: str, create: bool = False) -> sqlite3.Connection:
    con = sqlite3.connect(db_path(repo, create))
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA)
    return con


def meta_get(con, k):
    row = con.execute("SELECT v FROM meta WHERE k=?", (k,)).fetchone()
    return row[0] if row else None


def meta_set(con, k, v):
    con.execute("INSERT INTO meta(k, v) VALUES(?, ?) ON CONFLICT(k) DO UPDATE SET v=excluded.v", (k, v))


# ---------- study config ----------

def load_study(path: str) -> dict:
    p = Path(path).resolve()
    raw = p.read_bytes()
    cfg = tomllib.loads(raw.decode())
    for key in ("id", "targets", "directions"):
        if not cfg.get(key):
            raise SystemExit(f"{p}: missing required key '{key}'")
    for d in cfg["directions"]:
        if not d.get("id") or not d.get("keywords"):
            raise SystemExit(f"{p}: every [[directions]] entry needs id and keywords")
    cfg.setdefault("peers", [])
    cfg.setdefault("components", {})
    cfg.setdefault("label_components", {})
    b = cfg.setdefault("budget", {})
    for k, v in {"t1_per_direction": 150, "t2_per_direction": 25, "t1_body_chars": 600,
                 "t2_max_chars": 12000, "t1_batch": 50, "t2_batch": 8, "half_life_days": 365}.items():
        b.setdefault(k, v)
    cfg["window_start"] = cfg.get("window_start") or months_ago(int(cfg.get("window_months", 24)))
    if len(cfg["window_start"]) == 10:
        cfg["window_start"] += "T00:00:00Z"
    cfg["_path"], cfg["_dir"], cfg["_hash"] = p, p.parent, sha(raw.decode())
    cfg["_state"], cfg["_cache"] = STATE / cfg["id"], CACHE / cfg["id"]
    return cfg


def prompt_version(stage: str) -> str:
    return sha(BRIEFS[stage].read_text(), 12)


def context_for(cfg: dict) -> dict:
    return {"directions": [{k: d.get(k, "") for k in ("id", "title", "question")} for d in cfg["directions"]],
            "components": sorted(cfg["components"]) + ["other", "unknown"]}


# ---------- sync ----------

ITEM_FIELDS = ("number title state stateReason createdAt updatedAt closedAt url authorAssociation "
               "author{login} labels(first:20){nodes{name}} comments{totalCount} reactions{totalCount} bodyText")
ISSUES_Q = ("query($owner:String!,$name:String!,$cursor:String){repository(owner:$owner,name:$name){"
            "issues(first:100,after:$cursor,orderBy:{field:UPDATED_AT,direction:DESC}%s){pageInfo{hasNextPage endCursor} "
            "nodes{" + ITEM_FIELDS + " closedByPullRequestsReferences(first:5,includeClosedPrs:false){nodes{number}}}}}}")
PRS_Q = ("query($owner:String!,$name:String!,$cursor:String){repository(owner:$owner,name:$name){"
         "pullRequests(first:50,after:$cursor,orderBy:{field:UPDATED_AT,direction:DESC}%s){pageInfo{hasNextPage endCursor} "
         "nodes{" + ITEM_FIELDS.replace("stateReason ", "") + " merged additions deletions "
         "closingIssuesReferences(first:5){nodes{number}} files(first:100){nodes{path}}}}}}")


def upsert(con, repo: str, kind: str, n: dict, ts: str) -> None:
    key = f"{repo}#{n['number']}"
    state = "MERGED" if n.get("merged") else n["state"]
    old = con.execute("SELECT state FROM items WHERE key=?", (key,)).fetchone()
    if old and old[0] != state:
        con.execute("INSERT INTO state_changes VALUES(?,?,?,?)", (key, ts, old[0], state))
    refs = n.get("closedByPullRequestsReferences") or n.get("closingIssuesReferences") or {"nodes": []}
    row = {
        "key": key, "repo": repo, "number": n["number"], "kind": kind, "title": n["title"],
        "body": n.get("bodyText") or "", "url": n["url"], "state": state,
        "state_reason": n.get("stateReason"), "author": (n.get("author") or {}).get("login"),
        "author_assoc": n.get("authorAssociation"), "created_at": n["createdAt"],
        "updated_at": n["updatedAt"], "closed_at": n.get("closedAt"),
        "labels": json.dumps([x["name"] for x in n["labels"]["nodes"]]),
        "n_comments": n["comments"]["totalCount"], "n_reactions": n["reactions"]["totalCount"],
        "additions": n.get("additions"), "deletions": n.get("deletions"),
        "files": json.dumps([f["path"] for f in (n.get("files") or {"nodes": []})["nodes"]]),
        "links": json.dumps([r["number"] for r in refs["nodes"]]), "first_seen": ts, "last_seen": ts,
    }
    cols = ",".join(row)
    updates = ",".join(f"{c}=excluded.{c}" for c in row if c not in ("key", "first_seen"))
    con.execute(f"INSERT INTO items({cols}) VALUES({','.join('?' * len(row))}) "
                f"ON CONFLICT(key) DO UPDATE SET {updates}", list(row.values()))
    con.execute("DELETE FROM items_fts WHERE key=?", (key,))
    con.execute("INSERT INTO items_fts(key, title, body) VALUES(?,?,?)", (key, row["title"], row["body"]))


def sync_pass(con, repo, kind, window_start, open_only, ghv) -> int:
    owner, name = repo.split("/")
    conn_name = "issues" if kind == "issue" else "pullRequests"
    query = (ISSUES_Q if kind == "issue" else PRS_Q) % (",states:[OPEN]" if open_only else "")
    pass_name = f"{kind}{'-open' if open_only else ''}"
    covered, synced_to = meta_get(con, f"{kind}.covered_from"), meta_get(con, f"{kind}.synced_to")
    if open_only:
        stop_at = None  # walk every open item once per window extension
    else:
        stop_at = synced_to if covered and covered <= window_start else window_start
    started, cursor, fetched, newest = now(), None, 0, synced_to or ""
    while True:
        page = gh_graphql(query, owner=owner, name=name, cursor=cursor)["repository"][conn_name]
        done = False
        for n in page["nodes"]:
            if stop_at and n["updatedAt"] < stop_at:
                done = True
                break
            upsert(con, repo, kind, n, started)
            fetched += 1
            newest = max(newest, n["updatedAt"])
        con.commit()
        print(f"  {repo} {pass_name}: {fetched} items", end="\r", flush=True)
        if done or not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]
    print()
    if open_only:
        meta_set(con, f"{kind}.open_backfill", window_start)
    else:
        meta_set(con, f"{kind}.synced_to", newest)
        meta_set(con, f"{kind}.covered_from", min(filter(None, [covered, window_start])))
    con.execute("INSERT INTO syncs(repo, pass, started_at, finished_at, window_start, stop_at, fetched, gh_version) "
                "VALUES(?,?,?,?,?,?,?,?)", (repo, pass_name, started, now(), window_start, stop_at, fetched, ghv))
    con.commit()
    return fetched


def sync_repo(repo: str, window_start: str) -> None:
    con = connect(repo, create=True)
    ghv = gh_version()
    for kind in ("issue", "pr"):
        sync_pass(con, repo, kind, window_start, False, ghv)
        backfill = meta_get(con, f"{kind}.open_backfill")
        if not backfill or backfill > window_start:
            sync_pass(con, repo, kind, window_start, True, ghv)
    reg = load_registry()
    reg[repo]["last_sync"] = now()
    save_registry(reg)


def fetch_comments(con, repo: str, keys: list[str]) -> None:
    stale = [k for k in keys if (r := con.execute("SELECT updated_at, comments_synced_at, n_comments FROM items WHERE key=?", (k,)).fetchone())
             and r["n_comments"] and (r["comments_synced_at"] or "") < r["updated_at"]]
    owner, name = repo.split("/")
    sel = "comments(first:100){nodes{databaseId author{login} authorAssociation createdAt bodyText}}"
    for i in range(0, len(stale), 20):
        chunk = stale[i:i + 20]
        parts = " ".join(f"i{k.split('#')[1]}:issueOrPullRequest(number:{k.split('#')[1]}){{... on Issue{{{sel}}} ... on PullRequest{{{sel}}}}}"
                         for k in chunk)
        data = gh_graphql(f"query{{repository(owner:\"{owner}\",name:\"{name}\"){{{parts}}}}}")["repository"]
        ts = now()
        for k in chunk:
            node = data.get(f"i{k.split('#')[1]}")
            if node is None:
                continue
            con.execute("DELETE FROM comments WHERE item_key=?", (k,))
            for c in node["comments"]["nodes"]:
                con.execute("INSERT OR REPLACE INTO comments VALUES(?,?,?,?,?,?)",
                            (c["databaseId"], k, (c.get("author") or {}).get("login"), c["authorAssociation"],
                             c["createdAt"], c["bodyText"] or ""))
            con.execute("UPDATE items SET comments_synced_at=? WHERE key=?", (ts, k))
        con.commit()


# ---------- selection (T0, no model) ----------

def fts_query(keywords: list[str]) -> str:
    return " OR ".join('"' + kw.replace('"', '""') + '"' for kw in keywords)


def score_rows(rows, half_life: float, ref: str) -> list[tuple[str, float]]:
    out = []
    for rank, r in enumerate(rows):
        relevance = 1 - rank / max(len(rows), 1)
        activity = 1 + math.log1p(r["n_comments"]) + math.log1p(r["n_reactions"]) \
            + 0.5 * len(json.loads(r["links"])) + (0.5 if r["author_assoc"] in MAINTAINER else 0)
        recency = 0.5 ** (max(days_between(r["updated_at"], ref), 0) / half_life)
        out.append((r["key"], relevance * activity * recency))
    return sorted(out, key=lambda x: -x[1])


def select(cfg: dict, repo: str | None, query: str | None, name: str | None, limit: int | None) -> None:
    ref, ts = now(), now()
    if query:
        if not (repo and name):
            raise SystemExit("--query needs --repo and --name")
        if repo not in cfg["targets"] + cfg["peers"]:
            raise SystemExit(f"{repo} is not in the study's targets or peers")
        jobs = [(repo, {"id": name, "keywords": [q.strip() for q in query.split(",") if q.strip()]}, limit or 30)]
    else:
        jobs = [(r, d, cfg["budget"]["t1_per_direction"]) for r in cfg["targets"] for d in cfg["directions"]]
    for repo_name, d, n in jobs:
        con = connect(repo_name)
        rows = con.execute(
            "SELECT i.* FROM items_fts f JOIN items i ON i.key=f.key WHERE items_fts MATCH ? "
            "AND (i.updated_at>=? OR i.state='OPEN') ORDER BY bm25(items_fts)",
            (fts_query(d["keywords"]), cfg["window_start"])).fetchall()
        picked = score_rows(rows, cfg["budget"]["half_life_days"], ref)[:n]
        con.execute("DELETE FROM selections WHERE study=? AND direction=?", (cfg["id"], d["id"]))
        con.executemany("INSERT INTO selections VALUES(?,?,?,?,?)",
                        [(cfg["id"], k, d["id"], s, ts) for k, s in picked])
        con.commit()
        print(f"{repo_name} {d['id']}: {len(rows)} keyword matches in window, selected {len(picked)}")


# ---------- export / ingest (T1, T2) ----------

def latest_analysis(con, study: str, stage: str, key: str):
    row = con.execute("SELECT result FROM analyses WHERE study=? AND stage=? AND item_key=? "
                      "ORDER BY ingested_at DESC LIMIT 1", (study, stage, key)).fetchone()
    return json.loads(row[0]) if row else None


def item_text(con, item, stage: str, cfg: dict) -> str:
    labels = ", ".join(json.loads(item["labels"]))
    head = f"[{item['kind']} {item['state']}] {item['title']}\nlabels: {labels}\n"
    if stage == "t1":
        return head + item["body"][:cfg["budget"]["t1_body_chars"]]
    limit = cfg["budget"]["t2_max_chars"]
    head += f"created {item['created_at'][:10]}, closed {(item['closed_at'] or '-')[:10]}, author {item['author_assoc']}\n"
    linked = json.loads(item["links"])
    if linked:
        head += f"linked: {', '.join('#' + str(x) for x in linked)}\n"
    files = json.loads(item["files"])
    if files:
        head += f"files: {', '.join(files[:15])}{' ...' if len(files) > 15 else ''}\n"
    text = head + "\nBODY:\n" + item["body"][:limit // 2]
    comments = con.execute("SELECT * FROM comments WHERE item_key=? ORDER BY created_at", (item["key"],)).fetchall()
    ordered = [c for c in comments if c["author_assoc"] in MAINTAINER] + [c for c in comments if c["author_assoc"] not in MAINTAINER]
    kept, omitted = [], 0
    for c in ordered:
        chunk = f"\nCOMMENT {c['id']} ({'maintainer' if c['author_assoc'] in MAINTAINER else 'other'}, {c['created_at'][:10]}):\n{c['body']}"
        if len(text) + sum(map(len, kept)) + len(chunk) > limit:
            omitted += 1
            continue
        kept.append(chunk)
    return text + "".join(kept) + (f"\n[{omitted} comments omitted for length]" if omitted else "")


def candidates(cfg: dict, stage: str):
    """Yield (repo, con, key) in priority order for a stage."""
    for repo in cfg["targets"] + cfg["peers"]:
        try:
            con = connect(repo)
        except SystemExit:
            continue
        rows = con.execute("SELECT item_key, direction, score FROM selections WHERE study=? ORDER BY score DESC",
                           (cfg["id"],)).fetchall()
        if stage == "t1":
            seen = set()
            for r in rows:
                if r["item_key"] not in seen:
                    seen.add(r["item_key"])
                    yield repo, con, r["item_key"]
            continue
        per_dir = Counter()
        seen = set()
        for r in rows:
            t1 = latest_analysis(con, cfg["id"], "t1", r["item_key"])
            if not t1 or not t1["escalate"] or not t1["directions"] or r["item_key"] in seen:
                continue
            dirs = t1["directions"]
            if all(per_dir[d] >= cfg["budget"]["t2_per_direction"] for d in dirs):
                continue
            for d in dirs:
                per_dir[d] += 1
            seen.add(r["item_key"])
            yield repo, con, r["item_key"]


def export(cfg: dict, stage: str, max_items: int | None, max_tokens: int | None) -> None:
    pv, ctx = prompt_version(stage), context_for(cfg)
    ctx_json = json.dumps(ctx, sort_keys=True)
    brief_tokens = len(BRIEFS[stage].read_text()) // 4
    out_dir = cfg["_state"] / "batches"
    out_dir.mkdir(parents=True, exist_ok=True)
    picked, hits, tokens = [], 0, 0
    pending_comments = defaultdict(list)
    cands = list(candidates(cfg, stage))
    if stage == "t2":
        for repo, con, key in cands:
            pending_comments[repo].append(key)
        for repo, keys in pending_comments.items():
            fetch_comments(connect(repo), repo, keys)
    for repo, con, key in cands:
        item = con.execute("SELECT * FROM items WHERE key=?", (key,)).fetchone()
        text = item_text(con, item, stage, cfg)
        h = sha(text + ctx_json)
        if con.execute("SELECT 1 FROM analyses WHERE study=? AND stage=? AND item_key=? AND input_hash=? AND prompt_version=?",
                       (cfg["id"], stage, key, h, pv)).fetchone():
            hits += 1
            continue
        if (max_items and len(picked) >= max_items) or (max_tokens and tokens + len(text) // 4 > max_tokens):
            break
        picked.append({"key": key, "input_hash": h, "url": item["url"], "text": text})
        tokens += len(text) // 4
    size = cfg["budget"][f"{stage}_batch"]
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for i in range(0, len(picked), size):
        chunk = picked[i:i + size]
        bid = f"{stage}-{stamp}-{i // size:03d}"
        path = out_dir / f"{bid}.json"
        est = sum(len(x["text"]) // 4 for x in chunk) + brief_tokens
        results = cfg["_state"] / "results" / f"{bid}.jsonl"
        results.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"batch_id": bid, "study": cfg["id"], "stage": stage, "prompt_version": pv,
                                    "brief": str(BRIEFS[stage]), "results": str(results), "context": ctx,
                                    "items": chunk}, indent=1))
        for repo in {x["key"].split("#")[0] for x in chunk}:
            con = connect(repo)
            con.execute("INSERT OR REPLACE INTO batches VALUES(?,?,?,?,?,?,?,?)",
                        (bid, cfg["id"], stage, now(), len(chunk), est, pv, str(path)))
            con.commit()
        print(path)
    n_batches = math.ceil(len(picked) / size) if picked else 0
    print(f"{stage}: {len(cands)} candidates, {hits} cached, {len(picked)} exported in {n_batches} batches, "
          f"~{tokens + brief_tokens * n_batches} input tokens estimated (chars/4)")


def validate(stage: str, rec: dict, item: dict, ctx: dict) -> list[str]:
    errs = []
    for f, t in FIELDS[stage].items():
        if not isinstance(rec.get(f), t):
            errs.append(f"{f}: expected {t.__name__}")
    if errs:
        return errs
    for f, allowed in ENUMS[stage].items():
        if rec[f] not in allowed:
            errs.append(f"{f}: {rec[f]!r} not in {sorted(allowed)}")
    dir_ids = {d["id"] for d in ctx["directions"]}
    if bad := [d for d in rec["directions"] if d not in dir_ids]:
        errs.append(f"unknown directions {bad}")
    if rec["component"] not in ctx["components"]:
        errs.append(f"component {rec['component']!r} not in {ctx['components']}")
    if stage == "t2":
        if not rec["quotes"]:
            errs.append("quotes: at least one verbatim quote required")
        hay = norm(item["text"])
        for q in rec["quotes"]:
            t = q.get("text", "") if isinstance(q, dict) else ""
            if len(norm(t)) < MIN_QUOTE or norm(t) not in hay:
                errs.append(f"quote not verbatim in item text (or < {MIN_QUOTE} chars): {t[:80]!r}")
    return errs


def ingest(cfg: dict, batch_path: str, results: str | None, model: str, effort: str) -> None:
    batch = json.loads(Path(batch_path).read_text())
    results = results or batch["results"]
    if batch["study"] != cfg["id"]:
        raise SystemExit("batch belongs to a different study")
    stage, items = batch["stage"], {x["key"]: x for x in batch["items"]}
    ok, bad, seen = 0, 0, set()
    for ln, line in enumerate(Path(results).read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"line {ln}: invalid JSON: {e}")
            bad += 1
            continue
        item = items.get(rec.get("key"))
        errs = ["key not in batch"] if not item else (["input_hash mismatch"] if rec.get("input_hash") != item["input_hash"]
                                                     else validate(stage, rec, item, batch["context"]))
        if errs:
            print(f"line {ln} {rec.get('key')}: " + "; ".join(errs))
            bad += 1
            continue
        con = connect(rec["key"].split("#")[0])
        con.execute("INSERT OR REPLACE INTO analyses VALUES(?,?,?,?,?,?,?,?,?)",
                    (cfg["id"], stage, rec["key"], rec["input_hash"], batch["prompt_version"],
                     json.dumps(rec), model, effort, now()))
        con.commit()
        seen.add(rec["key"])
        ok += 1
    missing = sorted(set(items) - seen)
    print(f"{batch['batch_id']}: stored {ok}, rejected {bad}, missing {len(missing)}")
    for k in missing:
        print(f"  missing {k}")
    if bad or missing:
        sys.exit(1)


# ---------- metrics and digest ----------

def component_of(con, cfg: dict, item) -> str:
    files = json.loads(item["files"])
    if item["kind"] == "issue":
        for n in json.loads(item["links"]):
            pr = con.execute("SELECT files FROM items WHERE key=?", (f"{item['repo']}#{n}",)).fetchone()
            if pr:
                files += json.loads(pr[0])
    votes = Counter()
    for f in files:
        best = max(((c, p) for c, ps in cfg["components"].items() for p in ps if f.startswith(p)),
                   key=lambda x: len(x[1]), default=None)
        if best:
            votes[best[0]] += 1
    if votes:
        return votes.most_common(1)[0][0]
    for label in json.loads(item["labels"]):
        if label in cfg["label_components"]:
            return cfg["label_components"][label]
    for stage in ("t2", "t1"):
        a = latest_analysis(con, cfg["id"], stage, item["key"])
        if a and a["component"] not in ("other", "unknown"):
            return a["component"]
    return "unassigned"


def pct(values, p):
    if not values:
        return ""
    s = sorted(values)
    return round(s[min(len(s) - 1, int(p * len(s)))], 1)


CQ_COLS = ["repo", "component", "quarter", "kind", "opened", "open_now", "closed_or_merged",
           "closed_within_90d_frac", "median_days_to_close", "p90_days_to_close",
           "distinct_authors", "maintainer_authored", "reverts", "bug_labeled"]
RC_COLS = ["repo", "direction", "component", "root_cause", "resolution", "generality", "items"]


def gather_live(cfg: dict) -> tuple[list[dict], list[tuple[str, dict]]]:
    """Census items created in the window (with component) and the latest T2 analysis per item."""
    items, t2 = [], []
    for repo in cfg["targets"] + cfg["peers"]:
        try:
            con = connect(repo)
        except SystemExit:
            continue
        if repo in cfg["targets"]:
            for r in con.execute("SELECT * FROM items WHERE created_at>=?", (cfg["window_start"],)).fetchall():
                items.append({**dict(r), "component": component_of(con, cfg, r)})
        for (key,) in con.execute("SELECT DISTINCT item_key FROM analyses WHERE study=? AND stage='t2'", (cfg["id"],)):
            t2.append((repo, latest_analysis(con, cfg["id"], "t2", key)))
    return items, t2


def gather_snapshot(path: Path) -> tuple[list[dict], list[tuple[str, dict]], str]:
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    computed_at = con.execute("SELECT v FROM manifest WHERE k='computed_at'").fetchone()[0]
    items = [dict(r) for r in con.execute("SELECT * FROM items WHERE in_census=1")]
    t2 = [(r["item_key"].split("#")[0], json.loads(r["result"])) for r in con.execute(
        "SELECT item_key, result FROM analyses a WHERE stage='t2' AND ingested_at="
        "(SELECT MAX(ingested_at) FROM analyses b WHERE b.stage='t2' AND b.item_key=a.item_key)")]
    return items, t2, computed_at


def metric_tables(items: list[dict], t2: list[tuple[str, dict]], ref: str) -> tuple[list[list], list[list]]:
    groups = defaultdict(list)
    for r in items:
        groups[(r["repo"], r["component"], quarter(r["created_at"]), r["kind"])].append(r)
    cq = []
    for (repo, comp, q, kind), rs in sorted(groups.items()):
        closed = [days_between(r["created_at"], r["closed_at"]) for r in rs if r["closed_at"]]
        mature = [r for r in rs if days_between(r["created_at"], ref) >= 90]
        within = sum(1 for r in mature if r["closed_at"] and days_between(r["created_at"], r["closed_at"]) <= 90)
        cq.append([repo, comp, q, kind, len(rs), sum(r["state"] == "OPEN" for r in rs), len(closed),
                   round(within / len(mature), 3) if mature else "", pct(closed, 0.5), pct(closed, 0.9),
                   len({r["author"] for r in rs}), sum(r["author_assoc"] in MAINTAINER for r in rs),
                   sum(r["title"].lower().startswith("revert") for r in rs),
                   sum(any("bug" in lb.lower() for lb in json.loads(r["labels"])) for r in rs)])
    counts = Counter((repo, d, a["component"], a["root_cause"], a["resolution"], a["generality"])
                     for repo, a in t2 for d in a["directions"])
    return cq, [[*k, v] for k, v in sorted(counts.items())]


def metrics(cfg: dict | None, out: Path, from_snapshot: Path | None = None) -> None:
    if from_snapshot:
        items, t2, ref = gather_snapshot(from_snapshot)
    else:
        (items, t2), ref = gather_live(cfg), now()
    cq, rc = metric_tables(items, t2, ref)
    out.mkdir(parents=True, exist_ok=True)
    for name, cols, rows in (("component_quarter.csv", CQ_COLS, cq), ("direction_root_causes.csv", RC_COLS, rc)):
        with (out / name).open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(cols)
            w.writerows(rows)
    print(f"wrote {out}/component_quarter.csv, direction_root_causes.csv (reference time {ref})")


def digest(cfg: dict, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    by_dir = defaultdict(list)
    for repo in cfg["targets"] + cfg["peers"]:
        try:
            con = connect(repo)
        except SystemExit:
            continue
        for (key,) in con.execute("SELECT DISTINCT item_key FROM analyses WHERE study=? AND stage='t2'", (cfg["id"],)):
            a = latest_analysis(con, cfg["id"], "t2", key)
            item = con.execute("SELECT url, state, created_at FROM items WHERE key=?", (key,)).fetchone()
            for d in a["directions"] or ["(none)"]:
                by_dir[d].append((repo, key, item, a))
    for d, entries in sorted(by_dir.items()):
        lines = [f"# Digest: {d}", "", f"study {cfg['id']}, {len(entries)} analyzed items", ""]
        for repo, key, item, a in sorted(entries, key=lambda e: (e[3]["component"], e[0], e[1])):
            q = a["quotes"][0]["text"].replace("\n", " ")[:240]
            lines.append(f"- [{key}]({item['url']}) {item['state']} {item['created_at'][:7]} | comp={a['component']} "
                         f"root={a['root_cause']} res={a['resolution']} gen={a['generality']} | {a['summary']} | \"{q}\"")
        (out / f"digest-{d}.md").write_text("\n".join(lines) + "\n")
        print(out / f"digest-{d}.md")


# ---------- hypotheses, snapshot, status ----------

CARD_SECTIONS = ["Research question", "Mismatch", "Evidence", "Generality",
                 "Prior art", "Falsification", "Cheapest experiment", "Verdict"]
EVIDENCE_RE = re.compile(r'^- (https://github\.com/\S+) — "(.+)"\s*$')


def find_item(url: str):
    m = re.match(r"https://github\.com/([^/]+/[^/]+)/(?:issues|pull)/(\d+)", url)
    if not m:
        return None, None
    try:
        con = connect(m.group(1))
    except SystemExit:
        return None, None
    return con, con.execute("SELECT * FROM items WHERE key=?", (f"{m.group(1)}#{m.group(2)}",)).fetchone()


def verify_hypotheses(path: Path) -> None:
    """Each `## ` heading is one card; it needs every `### ` section and verbatim evidence lines."""
    text = path.read_text()
    cards = re.split(r"^## ", text, flags=re.M)[1:]
    if not cards:
        raise SystemExit(f"FAIL {path}: no cards (each card starts with a '## ' heading)")
    failures = 0
    for card in cards:
        title, errs, n = card.splitlines()[0], [], 0
        heads = set(re.findall(r"^### (.+?)\s*$", card, flags=re.M))
        errs += [f"missing section ### {s}" for s in CARD_SECTIONS if s not in heads]
        for line in card.splitlines():
            m = EVIDENCE_RE.match(line)
            if not m:
                continue
            n += 1
            con, item = find_item(m.group(1))
            if not item:
                errs.append(f"item not in any database: {m.group(1)}")
                continue
            hay = norm(item["title"] + " " + item["body"] + " " + " ".join(
                c[0] for c in con.execute("SELECT body FROM comments WHERE item_key=?", (item["key"],))))
            if len(norm(m.group(2))) < MIN_QUOTE or norm(m.group(2)) not in hay:
                errs.append(f"quote not verbatim in {m.group(1)}: {m.group(2)[:80]!r}")
        if n == 0:
            errs.append('no evidence lines of the form: - <github url> — "verbatim quote"')
        if "TODO" in card:
            errs.append("unfilled placeholder")
        print(f"{'OK  ' if not errs else 'FAIL'} {title[:70]} ({n} evidence lines)")
        for e in errs:
            print(f"     {e}")
        failures += bool(errs)
    sys.exit(1 if failures else 0)


SNAP_ITEM_COLS = ["key", "repo", "number", "kind", "title", "url", "state", "state_reason", "author",
                  "author_assoc", "created_at", "updated_at", "closed_at", "labels", "n_comments",
                  "n_reactions", "links", "component", "in_census"]


def snapshot(cfg: dict, out: Path) -> None:
    """Freeze the study's evidence into one SQLite file that `metrics --from-snapshot` reproduces from."""
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".tmp")
    tmp.unlink(missing_ok=True)
    ref = now()
    items, t2 = gather_live(cfg)
    snap = sqlite3.connect(tmp)
    snap.executescript(f"""
        CREATE TABLE manifest(k TEXT PRIMARY KEY, v TEXT);
        CREATE TABLE items({", ".join(SNAP_ITEM_COLS)}, PRIMARY KEY(key));
        CREATE TABLE selections(item_key, direction, score);
        CREATE TABLE analyses(stage, item_key, input_hash, prompt_version, result, model, effort, ingested_at);
        CREATE TABLE syncs(repo, pass, started_at, finished_at, window_start, stop_at, fetched, gh_version);
        CREATE TABLE component_quarter({", ".join(CQ_COLS)});
        CREATE TABLE direction_root_causes({", ".join(RC_COLS)});""")
    put = lambda table, rows, n: snap.executemany(f"INSERT OR IGNORE INTO {table} VALUES({','.join('?' * n)})", rows)
    put("items", [[r[c] for c in SNAP_ITEM_COLS[:-1]] + [1] for r in items], len(SNAP_ITEM_COLS))
    for repo in cfg["targets"] + cfg["peers"]:
        try:
            con = connect(repo)
        except SystemExit:
            continue
        sel = con.execute("SELECT item_key, direction, score FROM selections WHERE study=?", (cfg["id"],)).fetchall()
        put("selections", sel, 3)
        extra = con.execute(f"SELECT * FROM items WHERE key IN (SELECT item_key FROM selections WHERE study=?) "
                            f"AND NOT (created_at>=? AND repo IN ({','.join('?' * len(cfg['targets']))}))",
                            (cfg["id"], cfg["window_start"], *cfg["targets"])).fetchall()
        put("items", [[r[c] for c in SNAP_ITEM_COLS[:-2]] + [component_of(con, cfg, r), 0] for r in extra],
            len(SNAP_ITEM_COLS))
        put("analyses", con.execute("SELECT stage, item_key, input_hash, prompt_version, result, model, effort, "
                                    "ingested_at FROM analyses WHERE study=?", (cfg["id"],)).fetchall(), 8)
        put("syncs", con.execute("SELECT repo, pass, started_at, finished_at, window_start, stop_at, fetched, "
                                 "gh_version FROM syncs").fetchall(), 8)
    cq, rc = metric_tables(items, t2, ref)
    put("component_quarter", cq, len(CQ_COLS))
    put("direction_root_causes", rc, len(RC_COLS))
    manifest = {"created_at": now(), "computed_at": ref, "study": cfg["id"], "study_file_hash": cfg["_hash"],
                "study_file": cfg["_path"].read_text(), "window_start": cfg["window_start"],
                "targets": json.dumps(cfg["targets"]), "peers": json.dumps(cfg["peers"]),
                "prompt_versions": json.dumps({s: prompt_version(s) for s in BRIEFS}),
                "databases": json.dumps({r: load_registry().get(r, {}).get("db") for r in cfg["targets"] + cfg["peers"]})}
    put("manifest", list(manifest.items()), 2)
    snap.commit()
    snap.close()
    os.replace(tmp, out)
    print(f"snapshot {out}: {len(items)} census items, {len(t2)} T2 analyses, {out.stat().st_size // 1024} KiB")


def status(cfg: dict) -> None:
    pvs = {s: prompt_version(s) for s in BRIEFS}
    for repo in cfg["targets"] + cfg["peers"]:
        try:
            con = connect(repo)
        except SystemExit:
            print(f"{repo}: not synced")
            continue
        n = con.execute("SELECT kind, COUNT(*) FROM items GROUP BY kind").fetchall()
        sel = con.execute("SELECT COUNT(DISTINCT item_key) FROM selections WHERE study=?", (cfg["id"],)).fetchone()[0]
        line = [f"{repo}: db={db_path(repo)}", "items " + ", ".join(f"{k}={c}" for k, c in n),
                f"synced_to issue={meta_get(con, 'issue.synced_to')} pr={meta_get(con, 'pr.synced_to')}",
                f"selected={sel}"]
        for s, pv in pvs.items():
            cur = con.execute("SELECT COUNT(DISTINCT item_key) FROM analyses WHERE study=? AND stage=? AND prompt_version=?",
                              (cfg["id"], s, pv)).fetchone()[0]
            tok = con.execute("SELECT COALESCE(SUM(est_tokens),0) FROM batches WHERE study=? AND stage=?", (cfg["id"], s)).fetchone()[0]
            line.append(f"{s}: analyzed={cur} (prompt {pv}), exported_est_tokens={tok}")
        print("\n  ".join(line))


# ---------- CLI ----------

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sync"); s.add_argument("repo", nargs="?"); s.add_argument("--study")
    s.add_argument("--window-months", type=int, default=24)
    s = sub.add_parser("select"); s.add_argument("--study", required=True); s.add_argument("--repo")
    s.add_argument("--query"); s.add_argument("--name"); s.add_argument("--limit", type=int)
    s = sub.add_parser("export"); s.add_argument("--study", required=True)
    s.add_argument("--stage", choices=["t1", "t2"], required=True)
    s.add_argument("--max-items", type=int); s.add_argument("--max-tokens", type=int)
    s = sub.add_parser("ingest"); s.add_argument("--study", required=True); s.add_argument("--batch", required=True)
    s.add_argument("results", nargs="?"); s.add_argument("--model", default="unspecified"); s.add_argument("--effort", default="unspecified")
    s = sub.add_parser("digest"); s.add_argument("--study", required=True); s.add_argument("--out")
    s = sub.add_parser("snapshot"); s.add_argument("--study", required=True); s.add_argument("--out")
    s = sub.add_parser("metrics"); s.add_argument("--study"); s.add_argument("--from-snapshot")
    s.add_argument("--out")
    s = sub.add_parser("verify"); s.add_argument("--study", required=True)
    s = sub.add_parser("status"); s.add_argument("--study", required=True)
    sub.add_parser("registry")
    a = ap.parse_args()

    if a.cmd == "registry":
        print(json.dumps(load_registry(), indent=2))
        return
    if a.cmd == "sync":
        if a.study:
            cfg = load_study(a.study)
            for repo in cfg["targets"]:
                sync_repo(repo, cfg["window_start"])
        elif a.repo:
            sync_repo(a.repo, months_ago(a.window_months))
        else:
            ap.error("sync needs REPO or --study")
        return
    if a.cmd == "metrics" and a.from_snapshot:
        if not a.out:
            ap.error("--from-snapshot needs --out")
        metrics(None, Path(a.out), Path(a.from_snapshot))
        return
    if not a.study:
        ap.error("--study is required")
    cfg = load_study(a.study)
    if a.cmd == "select":
        select(cfg, a.repo, a.query, a.name, a.limit)
    elif a.cmd == "export":
        export(cfg, a.stage, a.max_items, a.max_tokens)
    elif a.cmd == "ingest":
        ingest(cfg, a.batch, a.results, a.model, a.effort)
    elif a.cmd == "metrics":
        metrics(cfg, Path(a.out) if a.out else cfg["_cache"] / "metrics")
    elif a.cmd == "digest":
        digest(cfg, Path(a.out) if a.out else cfg["_cache"] / "digests")
    elif a.cmd == "snapshot":
        snapshot(cfg, Path(a.out) if a.out else cfg["_dir"] / "data" / "evidence.sqlite")
    elif a.cmd == "verify":
        verify_hypotheses(cfg["_dir"] / "hypotheses.md")
    elif a.cmd == "status":
        status(cfg)


if __name__ == "__main__":
    main()
