"""Shared helpers for the paper-integrity scripts (stdlib only)."""

import difflib
import hashlib
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

SEVERITY_ORDER = {"S0": 0, "S1": 1, "S2": 2}

# ---------------------------------------------------------------- findings


def finding(stage, severity, confidence, category, anchor, location, evidence,
            suggestion, key=None):
    """One tracker row. The ID hashes stage, category, and a line-free anchor
    so it stays stable when the manuscript shifts."""
    assert severity in SEVERITY_ORDER, severity
    assert confidence in ("verified", "suspected", "no-access"), confidence
    digest = hashlib.sha1(f"{stage}|{category}|{anchor}".encode()).hexdigest()[:8]
    return {
        "id": f"{stage}-{digest}",
        "stage": stage,
        "severity": severity,
        "confidence": confidence,
        "category": category,
        "key": key,
        "location": location,
        "evidence": evidence,
        "suggestion": suggestion,
    }


def write_json(path, obj):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def read_json(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path) as f:
        return json.load(f)


def summarize(name, findings):
    counts = {s: sum(1 for f in findings if f["severity"] == s) for s in SEVERITY_ORDER}
    print(f"{name}: {len(findings)} findings "
          + " ".join(f"{s}={n}" for s, n in counts.items()))


# ------------------------------------------------------------------ BibTeX

_ACCENTS = {
    '"a': "ä", '"o': "ö", '"u': "ü", '"A': "Ä", '"O': "Ö", '"U': "Ü",
    "'e": "é", "'a": "á", "'i": "í", "'o": "ó", "'u": "ú", "'E": "É",
    "`e": "è", "`a": "à", "^e": "ê", "^o": "ô", "~n": "ñ", "c c": "ç",
    "ss": "ß", "o": "ø", "aa": "å",
}


def latex_to_text(s):
    if not s:
        return ""
    s = re.sub(r"\\url\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\([\"'`^~]|c )\{?\\?([A-Za-z])\}?",
               lambda m: _ACCENTS.get(m.group(1) + m.group(2), m.group(2)), s)
    s = re.sub(r"\\(ss|aa|o)\b", lambda m: _ACCENTS[m.group(1)], s)
    s = s.replace("\\&", "&").replace("~", " ").replace("--", "-")
    s = re.sub(r"\\[a-zA-Z]+\*?", " ", s)
    s = s.replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", s).strip()


def norm_title(s):
    s = re.sub(r"<[^>]+>", " ", s or "")  # JATS/HTML markup in record titles
    s = latex_to_text(s).lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def title_sim(a, b):
    a, b = norm_title(a), norm_title(b)
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()


def _read_braced(text, i):
    """text[i] is '{' or '"'; return (value, index after the closing char)."""
    if text[i] == '"':
        j = i + 1
        depth = 0
        while j < len(text):
            c = text[j]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
            elif c == '"' and depth == 0:
                return text[i + 1:j], j + 1
            j += 1
        raise ValueError("unterminated quoted value")
    depth = 0
    j = i
    while j < len(text):
        c = text[j]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[i + 1:j], j + 1
        j += 1
    raise ValueError("unterminated braced value")


def parse_bib(path):
    """Return (entries, occurrences). entries: key -> {type, fields, line};
    occurrences: list of (key, line) in file order, duplicates included."""
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    entries, occurrences = {}, []
    for m in re.finditer(r"@([a-zA-Z]+)\s*\{", text):
        etype = m.group(1).lower()
        if etype in ("comment", "preamble", "string"):
            continue
        line = text.count("\n", 0, m.start()) + 1
        i = m.end()
        km = re.match(r"\s*([^,\s]+)\s*,", text[i:])
        if not km:
            continue
        key = km.group(1)
        i += km.end()
        fields = {}
        while i < len(text):
            fm = re.match(r"\s*([a-zA-Z_\-]+)\s*=\s*", text[i:])
            if not fm:
                break
            name = fm.group(1).lower()
            i += fm.end()
            if text[i] in '{"':
                value, i = _read_braced(text, i)
            else:
                vm = re.match(r"[^,}\s]+", text[i:])
                value = vm.group(0) if vm else ""
                i += len(value)
            fields[name] = value.strip()
            cm = re.match(r"\s*,", text[i:])
            if cm:
                i += cm.end()
            else:
                break
        occurrences.append((key, line))
        entries.setdefault(key, {"type": etype, "fields": fields, "line": line})
    return entries, occurrences


def split_names(author_field):
    """Return author family names; corporate {{...}} names stay whole."""
    names = []
    for raw in re.split(r"\s+and\s+", author_field or ""):
        raw = raw.strip()
        if not raw or raw.lower() == "others":
            continue
        if raw.startswith("{") and raw.endswith("}") and raw.count("{") == 1:
            names.append(latex_to_text(raw))
            continue
        if raw.startswith("{{") or (raw.startswith("{") and "," not in raw):
            names.append(latex_to_text(raw))
            continue
        if "," in raw:
            names.append(latex_to_text(raw.split(",")[0]))
        else:
            names.append(latex_to_text(raw.split()[-1]))
    return names


def norm_name(s):
    s = latex_to_text(s).lower()
    for a, b in (("ä", "a"), ("ö", "o"), ("ü", "u"), ("é", "e"), ("è", "e"),
                 ("á", "a"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("ñ", "n"),
                 ("ç", "c"), ("ø", "o"), ("å", "a"), ("ß", "ss")):
        s = s.replace(a, b)
    return re.sub(r"[^a-z]", "", s)


def entry_url(fields):
    for name in ("url", "howpublished", "note"):
        m = re.search(r"https?://[^\s}]+", fields.get(name, ""))
        if m:
            return m.group(0).rstrip(".,")
    return None


def entry_arxiv_id(fields):
    for name in ("eprint", "url", "journal", "note", "howpublished", "doi"):
        m = re.search(r"(\d{4}\.\d{4,5})(v\d+)?", fields.get(name, ""))
        if m and (name == "eprint" or "arxiv" in fields.get(name, "").lower()):
            return m.group(1)
    return None


# ------------------------------------------------------------------- LaTeX


def read_aux_citations(aux_path):
    """Cited keys from \\citation lines, following \\@input aux files."""
    keys, seen = [], set()

    def visit(path):
        if not os.path.exists(path) or path in seen:
            return
        seen.add(path)
        with open(path, errors="replace") as f:
            for line in f:
                m = re.match(r"\\citation\{([^}]*)\}", line)
                if m:
                    for k in m.group(1).split(","):
                        k = k.strip()
                        if k and k != "*" and k not in keys:
                            keys.append(k)
                m = re.match(r"\\@input\{([^}]*)\}", line)
                if m:
                    visit(os.path.join(os.path.dirname(path), m.group(1)))

    visit(aux_path)
    return keys


def read_aux_bibdata(aux_path):
    if not os.path.exists(aux_path):
        return []
    with open(aux_path, errors="replace") as f:
        m = re.search(r"\\bibdata\{([^}]*)\}", f.read())
    return [b.strip() for b in m.group(1).split(",")] if m else []


def find_build_file(paper_dir, build_dir, stem, ext):
    """Prefer the build dir; fall back to the paper dir. Return None if absent."""
    for d in (build_dir, paper_dir):
        if d:
            p = os.path.join(d, stem + ext)
            if os.path.exists(p):
                return p
    return None


# -------------------------------------------------------------------- HTTP


class Http:
    """Cached, throttled GET. The cache maps URL -> {status, body} so reruns
    and other stages do not repeat network calls."""

    def __init__(self, cache_path, mailto=None, delay=1.0):
        self.cache_path = cache_path
        self.cache = read_json(cache_path, {}) or {}
        self.mailto = mailto
        self.delay = delay
        self.last = {}
        self.lock = threading.Lock()
        ua = "paper-integrity/0.1"
        if mailto:
            ua += f" (mailto:{mailto})"
        self.headers = {"User-Agent": ua}

    def get(self, url, accept_json=True, max_bytes=5_000_000):
        if url in self.cache:
            return self.cache[url]["status"], self.cache[url]["body"]
        host = urllib.parse.urlparse(url).netloc
        with self.lock:
            wait = self.last.get(host, 0) + self.delay - time.time()
            if wait > 0:
                time.sleep(wait)
            self.last[host] = time.time()
        status, body = None, None
        for attempt in range(3):
            try:
                req = urllib.request.Request(url, headers=self.headers)
                with urllib.request.urlopen(req, timeout=30) as r:
                    status = r.status
                    body = r.read(max_bytes).decode("utf-8", errors="replace")
                break
            except urllib.error.HTTPError as e:
                status, body = e.code, ""
                if e.code not in (429, 500, 502, 503, 504):
                    break
            except Exception as e:  # timeouts, DNS, TLS
                status, body = None, f"error: {e}"
            time.sleep(2 * (attempt + 1))
        if accept_json and status == 200:
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                pass
        # Do not cache transient failures.
        if status is not None and status not in (429, 500, 502, 503, 504):
            self.cache[url] = {"status": status, "body": body}
        return status, body

    def save(self):
        write_json(self.cache_path, self.cache)


def die(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(2)
