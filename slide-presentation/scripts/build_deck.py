#!/usr/bin/env python3
"""Build a .pptx deck from a Markdown deck spec, the single source of truth.

The spec format is defined in references/spec-format.md; assets/deck-spec-template.md is a buildable example.
Wording changes go into the spec first, then rebuild; never hand-edit the generated text in the .pptx.

Run (from anywhere):
  uv run --no-project --with python-pptx python <skill>/scripts/build_deck.py SPEC.md \
      [--out DECK.pptx] [--template T.pptx] [--check] [--final] [--strict] [--outline]

  --check    parse, validate and estimate layout only; write nothing
  --final    every slide must be agreed and every warning becomes an error
  --strict   warnings become errors
  --outline  print the slide table (number, part, title, status, minutes)
  --verify D compare an existing deck D with the spec (detects hand edits or a stale build); no build

Exit status: 0 = built (warnings may be printed), 1 = errors.
"""
from __future__ import annotations

import argparse
import copy
import functools
import re
import subprocess
import sys
import warnings
from dataclasses import dataclass, field
from pathlib import Path

warnings.filterwarnings("ignore", message=".*global interpreter lock.*")  # lxml on free-threaded Python

SKILL = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = SKILL / "assets" / "templates" / "google-slides-default.pptx"
PROFILE_NAME = "slide-profile.md"

SLIDE_FIELDS = {"part", "status", "layout", "minutes", "claim", "full claim", "on the slide", "figure",
                "transition", "notes", "sources", "subtitle", "authors", "affiliation"}
DECK_FIELDS = {"profile", "project profile", "template", "output", "banned terms", "font", "accent", "length"}
LAYOUTS = {"title", "content", "references"}
STATUSES = {"agreed", "proposed", "open"}
FIGURE_KEYS = {"caption", "file", "position", "width"}
POSITIONS = {"left", "right", "below", "above"}

# Design grid in inches on a 10 x 5.625 in (16:9) slide; scaled uniformly for other 16:9 sizes.
LEFT, WIDTH = 0.34, 9.32
RIGHT = LEFT + WIDTH
TITLE_Y, TITLE_H = 0.40, 0.60
CLAIM_Y, CLAIM_H = 1.02, 0.38
TOP = 1.60                      # first content row
BOTTOM_BAND, BOTTOM_FREE = 4.42, 4.95
BAND_Y, BAND_H = 4.55, 0.45     # transition band
SRC_Y, SRC_H, SRC_W = 5.12, 0.28, 8.70
TITLE_PT, CLAIM_PT, BAND_PT, SRC_PT, PART_PT, CAPTION_PT = 28, 15, 14, 9, 10, 10
TIERS = [(16, 14), (15, 13), (14, 12), (13, 11), (12, 10)]   # (text pt, table pt), tried in order until it fits
LINE = 1.2                      # line height / font size
BLOCK_GAP = 0.18
TITLE_MAX_WORDS, CLAIM_MAX_WORDS, MAX_TOP_BULLETS = 7, 16, 3

INK, MUTED, GRAY = "212121", "5F6368", "80868B"
HEAD, RULE, NEUTRAL, EDGE, WHITE, PAPER = "E8EAED", "C4C7CC", "F1F3F4", "9AA0A6", "FFFFFF", "F8F9FA"

MARKUP = re.compile(r"(\*\*.+?\*\*|__.+?__)")


def strip_markup(text: str) -> str:
    return re.sub(r"\*\*(.+?)\*\*|__(.+?)__", lambda m: m.group(1) or m.group(2), text)


# ------------------------------------------------------------------------------------------------ issues

class Issues:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def err(self, where: str, msg: str):
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str):
        self.warnings.append(f"{where}: {msg}")


# ------------------------------------------------------------------------------------------------ parsing

FIELD_RE = re.compile(r"^- \*\*([^*]+?)(?::\*\*|\*\*:)\s*(.*)$")
H1_RE = re.compile(r"^#\s")
H2_RE = re.compile(r"^##\s+(.+?)\s*$")
H3_RE = re.compile(r"^###\s+(.+?)\s*$")
SLIDE_H_RE = re.compile(r"^(\d+)\.\s+(.+)$")
REF_RE = re.compile(r"^\s*(?:[-*]\s+)?\[(\d+)\]\s+(.+)$")


@dataclass
class Field:
    name: str
    first: str
    line: int
    body: list[str] = field(default_factory=list)

    def text(self) -> str:
        """The field as one paragraph: first line plus continuation lines joined by spaces."""
        parts = [self.first.strip()] + [b.strip() for b in self.body]
        return " ".join(p for p in parts if p)

    def lines(self) -> list[str]:
        """First line (if any) and the dedented continuation lines; blank lines kept as block separators."""
        return ([self.first] if self.first.strip() else []) + self.body

    def items(self) -> list[str]:
        """Comma-separated items on the first line plus one item per '- ' continuation line."""
        out = [x.strip() for x in self.first.split(",") if x.strip()]
        for b in self.body:
            b = b.strip()
            if b.startswith("- "):
                out.append(b[2:].strip())
            elif b:
                out += [x.strip() for x in b.split(",") if x.strip()]
        return out


@dataclass
class Slide:
    num: int
    title: str
    line: int
    fields: dict = field(default_factory=dict)

    def get(self, name: str, default: str = "") -> str:
        f = self.fields.get(name)
        return f.text() if f else default

    @property
    def where(self) -> str:
        return f"line {self.line}, slide {self.num} '{self.title}'"

    @property
    def status(self) -> str:
        return (self.get("status").split() or [""])[0].lower().strip(".,;:")

    @property
    def layout(self) -> str:
        return (self.get("layout", "content").split() or ["content"])[0].lower()


@dataclass
class Spec:
    path: Path
    deck: dict
    slides: list
    refs: dict


def _read_fields(lines, start, target, known, issues, where_prefix, strict_unknown=True):
    """Parse '- **Field:** value' lines with indented continuations into target; returns nothing."""
    cur = None
    for i, ln in lines:
        m = FIELD_RE.match(ln)
        if m:
            name = m.group(1).strip().lower()
            if known is not None and name not in known:
                if strict_unknown:
                    issues.err(f"{where_prefix} line {i}", f"unknown field '{m.group(1).strip()}' "
                               f"(known: {', '.join(sorted(known))})")
                cur = None
                continue
            if name in target:
                issues.err(f"{where_prefix} line {i}", f"duplicate field '{m.group(1).strip()}'")
            cur = Field(name, m.group(2), i)
            target[name] = cur
            continue
        if not ln.strip():
            if cur is not None:
                cur.body.append("")
            continue
        if ln.startswith("  ") and cur is not None:
            cur.body.append(ln[2:])
            continue
        if strict_unknown:
            issues.err(f"{where_prefix} line {i}", "expected '- **Field:** value' or an indented continuation, "
                       f"got: {ln.strip()[:70]}")
        cur = None
    for f in target.values():
        while f.body and not f.body[-1].strip():
            f.body.pop()


def parse_spec(path: Path, issues: Issues) -> Spec:
    raw = path.read_text(encoding="utf-8")
    raw = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), raw, flags=re.S)
    section, deck_lines, refs = None, [], {}
    slides: list[Slide] = []
    slide_lines: dict[int, list] = {}
    in_code = False
    for i, ln in enumerate(raw.split("\n"), 1):
        if ln.lstrip().startswith("```"):
            in_code = not in_code
            if section in ("deck", "slides"):
                issues.err(f"line {i}", "code fences are not allowed in the Deck or Slides sections")
            continue
        if in_code:
            continue
        if H1_RE.match(ln):
            section = None
            continue
        m2 = H2_RE.match(ln)
        if m2 and not ln.startswith("###"):
            section = m2.group(1).strip().lower()
            continue
        if section == "deck":
            deck_lines.append((i, ln))
        elif section == "references":
            m = REF_RE.match(ln)
            if m:
                refs[int(m.group(1))] = m.group(2).strip()
            elif ln.startswith("|"):
                cells = [c.strip() for c in ln.strip().strip("|").split("|")]
                mm = re.match(r"^\[(\d+)\]$", cells[0]) if cells else None
                if mm and len(cells) >= 2:
                    refs[int(mm.group(1))] = cells[-1]
        elif section == "slides":
            m3 = H3_RE.match(ln)
            if m3:
                ms = SLIDE_H_RE.match(m3.group(1))
                if not ms:
                    issues.err(f"line {i}", f"slide heading must be '### N. Title', got: {ln.strip()}")
                    continue
                slides.append(Slide(int(ms.group(1)), ms.group(2).strip(), i))
                slide_lines[len(slides) - 1] = []
                continue
            if slides:
                slide_lines[len(slides) - 1].append((i, ln))
    deck: dict = {}
    _read_fields(deck_lines, 0, deck, DECK_FIELDS, issues, "Deck")
    for k, s in enumerate(slides):
        _read_fields(slide_lines[k], 0, s.fields, SLIDE_FIELDS, issues, f"slide {s.num}")
    if not slides:
        issues.err(str(path), "no slides found: put '### N. Title' headings under a '## Slides' section")
    return Spec(path, deck, slides, refs)


# ------------------------------------------------------------------------------------------------ settings

def _git_root(start: Path) -> Path:
    for d in [start, *start.parents]:
        if (d / ".git").exists():
            return d
    return Path(start.anchor)


def find_project_profile(spec: Spec, issues: Issues):
    f = spec.deck.get("project profile")
    if f:
        p = (spec.path.parent / f.text()).expanduser().resolve()
        if not p.is_file():
            issues.err(f"Deck line {f.line}", f"project profile not found: {p}")
            return None
        return p
    start = spec.path.parent.resolve()
    stop = _git_root(start)
    for d in [start, *start.parents]:
        if (d / PROFILE_NAME).is_file():
            return d / PROFILE_NAME
        if d == stop:
            break
    return None


def load_settings(spec: Spec, issues: Issues, cli_template=None) -> dict:
    """Defaults <- project profile (slide-profile.md) <- spec Deck section <- command line.
    Banned terms are merged across levels, not overridden."""
    s = {"font": "Arial", "accent": "1967D2", "template": DEFAULT_TEMPLATE, "banned": [], "authors": "",
         "affiliation": [], "project_profile": None, "profile": spec.deck["profile"].text()
         if "profile" in spec.deck else ""}
    pp = find_project_profile(spec, issues)
    if pp:
        s["project_profile"] = pp
        pf: dict = {}
        lines = list(enumerate(pp.read_text(encoding="utf-8").split("\n"), 1))
        _read_fields(lines, 0, pf, None, issues, str(pp), strict_unknown=False)
        if "template" in pf:
            s["template"] = (pp.parent / pf["template"].text()).expanduser()
        for k in ("font", "accent"):
            if k in pf:
                s[k] = pf[k].text()
        if "banned terms" in pf:
            s["banned"] += pf["banned terms"].items()
        if "authors" in pf:
            s["authors"] = pf["authors"].text()
        if "affiliation" in pf:
            s["affiliation"] = [x.strip().lstrip("- ").strip() for x in pf["affiliation"].lines() if x.strip()]
        if not s["profile"] and "extends" in pf:
            s["profile"] = pf["extends"].text()
    d = spec.deck
    if "template" in d:
        s["template"] = (spec.path.parent / d["template"].text()).expanduser()
    for k in ("font", "accent"):
        if k in d:
            s[k] = d[k].text()
    if "banned terms" in d:
        s["banned"] += d["banned terms"].items()
    if cli_template:
        s["template"] = Path(cli_template).expanduser()
    s["accent"] = s["accent"].lstrip("#").upper()
    if not re.fullmatch(r"[0-9A-F]{6}", s["accent"]):
        issues.err("Deck", f"accent must be a hex color like 1967D2, got {s['accent']}")
        s["accent"] = "1967D2"
    s["template"] = Path(s["template"]).resolve()
    if not s["template"].is_file():
        issues.err("Deck", f"template not found: {s['template']}")
    return s


# ------------------------------------------------------------------------------------------------ measurement

@functools.lru_cache(maxsize=None)
def _font(family: str, bold: bool):
    try:
        from PIL import ImageFont
        q = f"{family}:bold" if bold else family
        path = subprocess.run(["fc-match", "-f", "%{file}", q], capture_output=True, text=True,
                              timeout=5).stdout.strip()
        return ImageFont.truetype(path, 100) if path else None
    except Exception:
        return None


FONT_FAMILY = ["Arial"]


def text_w(text: str, pt: float, bold: bool = False) -> float:
    """Width in inches of one line of text (markup stripped)."""
    text = strip_markup(text)
    f = _font(FONT_FAMILY[0], bold)
    if f is None:
        return len(text) * pt * (0.56 if bold else 0.52) / 72
    return f.getlength(text) * pt / 100 / 72 * 1.03


def wrap_count(text: str, width: float, pt: float, bold: bool = False) -> int:
    n = 0
    for para in strip_markup(text).split("\n"):
        words, line, n_para = para.split(), "", 1
        for w in words:
            cand = (line + " " + w).strip()
            if line and text_w(cand, pt, bold) > width:
                n_para += 1
                line = w
            else:
                line = cand
        n += n_para
    return max(n, 1)


# ------------------------------------------------------------------------------------------------ content blocks

LIST_RE = re.compile(r"^( *)(?:([-*])\s+|(\d+)\.\s+)?(.*)$")


@dataclass
class Block:
    kind: str                     # text | table | flow
    paras: list = field(default_factory=list)      # text: (kind, level, text, num)
    rows: list = field(default_factory=list)       # table rows (header first)
    align: str = ""
    caption: str = ""
    items: list = field(default_factory=list)      # flow boxes


def parse_blocks(lines: list[str], where: str, issues: Issues) -> list[Block]:
    blocks: list[Block] = []
    cur, caption = None, ""
    for ln in lines + [""]:
        s = ln.strip()
        if not s:
            cur = None
            continue
        if s.startswith("|"):
            if cur is None or cur.kind != "table":
                cur = Block("table", caption=caption)
                caption = ""
                blocks.append(cur)
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                cur.align = "".join("c" if c.startswith(":") and c.endswith(":") else "r" if c.endswith(":")
                                    else "l" for c in cells)
                continue
            cur.rows.append(cells)
            continue
        if s.lower().startswith("table:"):
            caption, cur = s[6:].strip(), None
            continue
        if s.lower().startswith("flow:"):
            items = [x.strip() for x in re.split(r"\s*(?:->|→)\s*", s[5:].strip()) if x.strip()]
            blocks.append(Block("flow", items=items))
            cur = None
            continue
        if cur is None or cur.kind != "text":
            cur = Block("text")
            blocks.append(cur)
        m = LIST_RE.match(ln)
        kind = "num" if m.group(3) else ("bullet" if m.group(2) else "none")
        cur.paras.append((kind, len(m.group(1)) // 2, m.group(4).strip(), int(m.group(3) or 1)))
    if caption:
        issues.err(where, "'Table:' caption is not followed by a table")
    for b in blocks:
        if b.kind == "table":
            nc = len(b.rows[0])
            for r in b.rows[1:]:
                if len(r) != nc:
                    issues.err(where, f"table row has {len(r)} cells, header has {nc}: | {' | '.join(r)} |")
            b.align = (b.align or "l" * nc)[:nc].ljust(nc, "l")
    return blocks


def parse_figure(slide: Slide, spec: Spec, issues: Issues):
    f = slide.fields.get("figure")
    if not f or f.first.strip().lower() in ("", "none", "-"):
        if f and f.body and f.first.strip().lower() in ("none", "-"):
            issues.warn(slide.where, "Figure is 'none' but has sub-items")
        return None
    fig = {"label": f.first.strip(), "caption": "", "file": None, "position": "left", "width": 0.5}
    for b in f.body:
        m = re.match(r"^- ([A-Za-z]+):\s*(.*)$", b.strip())
        if not m or m.group(1).lower() not in FIGURE_KEYS:
            if b.strip():
                issues.err(slide.where, f"Figure sub-item must be '- Key: value' with key in "
                           f"{sorted(FIGURE_KEYS)}, got: {b.strip()[:60]}")
            continue
        k, v = m.group(1).lower(), m.group(2).strip()
        if k == "file":
            p = (spec.path.parent / v).expanduser()
            if not p.is_file():
                issues.err(slide.where, f"figure file not found: {p}")
            fig["file"] = p
        elif k == "position":
            if v.lower() not in POSITIONS:
                issues.err(slide.where, f"figure position must be one of {sorted(POSITIONS)}")
            else:
                fig["position"] = v.lower()
        elif k == "width":
            try:
                w = float(v.rstrip("%")) / (100 if v.endswith("%") or float(v.rstrip("%")) > 1 else 1)
                fig["width"] = min(max(w, 0.25), 0.75)
            except ValueError:
                issues.err(slide.where, f"figure width must be a percentage, got {v}")
        else:
            fig[k] = v
    return fig


# ------------------------------------------------------------------------------------------------ validation

def validate(spec: Spec, issues: Issues, final: bool):
    nums = [s.num for s in spec.slides]
    if len(set(nums)) != len(nums):
        issues.err(str(spec.path), f"duplicate slide numbers: {sorted(n for n in set(nums) if nums.count(n) > 1)}")
    elif nums != list(range(1, len(nums) + 1)):
        issues.warn(str(spec.path), "slide numbers are not 1..N in order; renumber so they match the deck")
    content = [s for s in spec.slides if s.layout == "content"]
    last_content = content[-1] if content else None
    for s in spec.slides:
        w = s.where
        if s.layout not in LAYOUTS:
            issues.err(w, f"Layout must be one of {sorted(LAYOUTS)}")
            continue
        if "status" not in s.fields:
            issues.err(w, "missing Status (agreed / proposed / open)")
        elif s.status not in STATUSES:
            issues.err(w, f"Status must start with agreed, proposed or open, got '{s.get('status')}'")
        elif final and s.status != "agreed":
            issues.err(w, f"--final: slide is '{s.status}', not agreed")
        if "minutes" in s.fields:
            try:
                float(s.get("minutes").split()[0])
            except (ValueError, IndexError):
                issues.err(w, "Minutes must be a number")
        words = len(strip_markup(s.title).split())
        if s.layout == "content":
            if words > TITLE_MAX_WORDS:
                issues.warn(w, f"title has {words} words; aim for a 3-7 word claim")
            if text_w(s.title, TITLE_PT, True) > WIDTH - 0.06:
                issues.warn(w, "title does not fit on one line; shorten it")
            if s.status == "open":
                continue
            if "part" not in s.fields:
                issues.warn(w, "missing Part")
            claim = s.get("claim")
            if not claim:
                issues.err(w, "missing Claim (one line under the title)")
            else:
                cw = len(strip_markup(claim).split())
                if cw > CLAIM_MAX_WORDS:
                    issues.warn(w, f"claim line has {cw} words; aim for 12-16, move the rest to Full claim or Notes")
                if text_w(claim, CLAIM_PT) > WIDTH - 0.06:
                    issues.warn(w, "claim line does not fit on one line; shorten it")
            if "transition" not in s.fields and s is not last_content:
                issues.warn(w, "missing Transition to the next slide")
            if "transition" in s.fields and text_w("→  " + s.get("transition"), BAND_PT) > WIDTH - 0.35:
                issues.warn(w, "transition does not fit on one line in the band; shorten it")
            if "sources" in s.fields and text_w(_source_text(s.get("sources")), SRC_PT) > SRC_W - 0.06:
                issues.warn(w, "source line does not fit on one line; shorten it or move detail to Notes")
            blocks = parse_blocks(s.fields["on the slide"].lines() if "on the slide" in s.fields else [], w, issues)
            fig = parse_figure(s, spec, issues)
            if not blocks and not fig:
                issues.warn(w, "nothing under 'On the slide' and no Figure")
            top = sum(1 for b in blocks if b.kind == "text" for p in b.paras if p[0] != "none" and p[1] == 0)
            if top > MAX_TOP_BULLETS:
                issues.warn(w, f"{top} top-level bullets; keep at most {MAX_TOP_BULLETS}, move detail to Notes")
        elif s.layout == "title":
            for k in ("claim", "transition", "on the slide", "figure"):
                if k in s.fields:
                    issues.warn(w, f"'{k}' is ignored on a title slide")
        elif s.layout == "references":
            if "on the slide" not in s.fields and not spec.refs:
                issues.err(w, "references slide without 'On the slide' needs a '## References' section")


# ------------------------------------------------------------------------------------------------ pptx helpers

class Ctx:
    """Rendering context: scale from design inches to the template's slide size, colors and font."""

    def __init__(self, prs, settings):
        from pptx.util import Emu
        self.prs, self.Emu = prs, Emu
        self.k = prs.slide_width / 914400 / 10.0
        self.font = settings["font"]
        self.accent = settings["accent"]
        self.pale = _blend(self.accent, 0.13)
        self.band = _blend(self.accent, 0.09)

    def e(self, inches: float):
        return self.Emu(int(round(inches * self.k * 914400)))

    def pt(self, size: float):
        from pptx.util import Pt
        return Pt(size * self.k)


def _blend(hex_color: str, a: float) -> str:
    c = [int(hex_color[i:i + 2], 16) for i in (0, 2, 4)]
    return "".join(f"{round(255 - (255 - v) * a):02X}" for v in c)


def _rgb(h: str):
    from pptx.dml.color import RGBColor
    return RGBColor.from_string(h)


def _sub(parent, tag, **attrs):
    from lxml import etree
    from pptx.oxml.ns import qn
    el = etree.SubElement(parent, qn(tag))
    for k, v in attrs.items():
        el.set(k, str(v))
    return el


def _runs(cx, p, text, size, color=INK, italic=False, bold_all=False):
    """**x** = highlight (bold, accent color, key numbers only); __x__ = bold label in the text color."""
    for part in MARKUP.split(text):
        if not part:
            continue
        hl, lab = part.startswith("**") and len(part) > 4, part.startswith("__") and len(part) > 4
        r = p.add_run()
        r.text = part[2:-2] if (hl or lab) else part
        f = r.font
        f.name, f.size, f.italic = cx.font, cx.pt(size), italic
        f.bold = hl or lab or bold_all
        f.color.rgb = _rgb(cx.accent if hl else color)


def _para(cx, p, kind, level, before, num=1):
    pPr = p._p.get_or_add_pPr()
    for c in list(pPr):
        pPr.remove(c)
    hang = 0.3 if kind == "num" else 0.2
    mar = 0.25 * level if kind == "none" else hang + 0.02 + 0.25 * level
    pPr.set("marL", str(int(cx.e(mar))))
    pPr.set("indent", "0" if kind == "none" else str(-int(cx.e(hang))))
    _sub(_sub(pPr, "a:lnSpc"), "a:spcPct", val=100000)
    _sub(_sub(pPr, "a:spcBef"), "a:spcPts", val=int(before * cx.k * 100))
    if kind == "none":
        _sub(pPr, "a:buNone")
        return
    _sub(_sub(pPr, "a:buClr"), "a:srgbClr", val=MUTED)
    _sub(pPr, "a:buSzPct", val=100000)
    _sub(pPr, "a:buFont", typeface=cx.font)
    if kind == "bullet":
        _sub(pPr, "a:buChar", char="•")
    else:
        _sub(pPr, "a:buAutoNum", type="arabicPeriod", startAt=num)


def _plain(shape):
    from pptx.oxml.ns import qn
    st = shape._element.find(qn("p:style"))
    if st is not None:
        shape._element.remove(st)


def add_paras(cx, slide, x, y, w, h, paras, size, color=INK, gap=None, align=None, italic=False, anchor="top",
              name=None):
    from pptx.enum.text import MSO_ANCHOR
    tb = slide.shapes.add_textbox(cx.e(x), cx.e(y), cx.e(w), cx.e(h))
    if name:
        tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = cx.e(0.03)
    tf.margin_top = tf.margin_bottom = cx.e(0.02)
    tf.vertical_anchor = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE, "bottom": MSO_ANCHOR.BOTTOM}[anchor]
    gap = size * 0.6 if gap is None else gap
    for k, (kind, level, text, num) in enumerate(paras):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        _para(cx, p, kind, level, 0 if k == 0 else gap, num)
        if align is not None:
            p.alignment = align
        _runs(cx, p, text, size - 1.5 * level, color=color, italic=italic)
    return tb


def add_line(cx, slide, x, y, w, h, text, size, **kw):
    return add_paras(cx, slide, x, y, w, h, [("none", 0, text, 1)], size, **kw)


def add_box(cx, slide, x, y, w, h, text, fill=NEUTRAL, line=EDGE, size=12, color=INK, bold=False,
            rounded=True, dash=False, name=None):
    from pptx.enum.dml import MSO_LINE_DASH_STYLE
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
    from pptx.util import Pt
    s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
                               cx.e(x), cx.e(y), cx.e(w), cx.e(h))
    if name:
        s.name = name
    if rounded:
        s.adjustments[0] = 0.12
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = _rgb(fill)
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = _rgb(line)
        s.line.width = Pt(1.0 * cx.k)
        if dash:
            s.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    _plain(s)
    tf = s.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = cx.e(0.05)
    tf.margin_top = tf.margin_bottom = cx.e(0.03)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    for k, part in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.CENTER
        _runs(cx, p, part, size, color=color, bold_all=bold)
    return s


def add_arrow(cx, slide, x1, y1, x2, y2):
    from pptx.enum.shapes import MSO_CONNECTOR
    from pptx.util import Pt
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, cx.e(x1), cx.e(y1), cx.e(x2), cx.e(y2))
    c.line.color.rgb = _rgb(EDGE)
    c.line.width = Pt(1.5 * cx.k)
    _sub(c.line._get_or_add_ln(), "a:tailEnd", type="triangle", w="med", len="med")
    return c


def _cell_borders(cell):
    from lxml import etree
    from pptx.oxml.ns import qn
    tcPr = cell._tc.get_or_add_tcPr()
    for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        old = tcPr.find(qn(tag))
        if old is not None:
            tcPr.remove(old)
    fill = [c for c in tcPr if c.tag in (qn("a:solidFill"), qn("a:noFill"))]
    for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        ln = etree.Element(qn(tag), w=str(9525), cap="flat", cmpd="sng", algn="ctr")
        _sub(_sub(ln, "a:solidFill"), "a:srgbClr", val=RULE)
        _sub(ln, "a:prstDash", val="solid")
        if fill:
            fill[0].addprevious(ln)
        else:
            tcPr.append(ln)


# ------------------------------------------------------------------------------------------------ block layout

PAD_X, PAD_Y = 0.08, 0.05


def text_height(paras, width, size, gap=None):
    gap = size * 0.6 if gap is None else gap
    h = 0.04
    for k, (kind, level, text, _num) in enumerate(paras):
        s = size - 1.5 * level
        indent = 0.25 * level + (0.32 if kind == "num" else 0.22 if kind == "bullet" else 0)
        h += wrap_count(text, width - 0.06 - indent, s) * s * LINE / 72 + (gap / 72 if k else 0)
    return h


def table_geometry(b: Block, width, size):
    """Column widths (natural widths, water-filled into the available width) and row heights."""
    nc = len(b.rows[0])
    nat = [max(text_w(r[j] if j < len(r) else "", size, i == 0) for i, r in enumerate(b.rows)) + 2 * PAD_X + 0.06
           for j in range(nc)]
    total = sum(nat)
    if total <= width:
        target = min(width, total * 1.3)
        cols = [n * target / total for n in nat]
    else:
        cols, left, free = [0.0] * nc, list(range(nc)), width
        while left:
            share = free / len(left)
            small = [j for j in left if nat[j] <= share]
            if not small:
                for j in left:
                    cols[j] = max(share, 0.8)
                break
            for j in small:
                cols[j] = nat[j]
                free -= nat[j]
                left.remove(j)
    rows_h = []
    for i, r in enumerate(b.rows):
        n = max(wrap_count(r[j] if j < len(r) else "", cols[j] - 2 * PAD_X - 0.02, size, i == 0)
                for j in range(nc))
        rows_h.append(n * size * LINE / 72 + 2 * PAD_Y + 0.04)
    return cols, rows_h


def block_height(b: Block, width, tier):
    tsize, bsize = tier
    if b.kind == "text":
        return text_height(b.paras, width, tsize)
    if b.kind == "table":
        cap = (wrap_count(b.caption, width, bsize, True) * bsize * LINE / 72 + 0.06) if b.caption else 0
        return cap + sum(table_geometry(b, width, bsize)[1])
    if b.kind == "flow":
        return flow_geometry(b, width)[1]
    return 0


def flow_geometry(b: Block, width, size=12, gap=0.4):
    nat = [text_w(t, size, t.startswith("**")) + 0.3 for t in b.items]
    avail = width - gap * (len(b.items) - 1)
    total = sum(nat)
    ws = [n * avail / total for n in nat] if total > avail else [n + (avail - total) / len(nat) * 0.5 for n in nat]
    lines = max(wrap_count(t, w - 0.12, size) for t, w in zip(b.items, ws))
    return ws, 0.32 + lines * size * LINE / 72


def stack_height(blocks, width, tier):
    return sum(block_height(b, width, tier) for b in blocks) + BLOCK_GAP * max(len(blocks) - 1, 0)


def place_blocks(cx, slide, blocks, x, y, width, tier):
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
    tsize, bsize = tier
    amap = {"l": PP_ALIGN.LEFT, "r": PP_ALIGN.RIGHT, "c": PP_ALIGN.CENTER}
    for n, b in enumerate(blocks, 1):
        h = block_height(b, width, tier)
        if b.kind == "text":
            add_paras(cx, slide, x, y, width, h, b.paras, tsize, name=f"Text {n}")
        elif b.kind == "flow":
            ws, fh = flow_geometry(b, width)
            bx = x
            for k, (t, w) in enumerate(zip(b.items, ws)):
                hl = t.startswith("**") and t.endswith("**")
                add_box(cx, slide, bx, y, w, fh, t.strip("*") if hl else t, fill=cx.pale if hl else NEUTRAL,
                        line=cx.accent if hl else EDGE, bold=hl, size=12, name=f"Flow {n}.{k + 1}")
                if k < len(ws) - 1:
                    add_arrow(cx, slide, bx + w + 0.06, y + fh / 2, bx + w + 0.34, y + fh / 2)
                bx += w + 0.4
        elif b.kind == "table":
            ty = y
            if b.caption:
                ch = wrap_count(b.caption, width, bsize, True) * bsize * LINE / 72 + 0.04
                add_line(cx, slide, x, y, width, ch, f"__{b.caption}__", bsize, name=f"Table caption {n}")
                ty += ch + 0.02
            cols, rows_h = table_geometry(b, width, bsize)
            nr, nc = len(b.rows), len(cols)
            shp = slide.shapes.add_table(nr, nc, cx.e(x), cx.e(ty), cx.e(sum(cols)), cx.e(sum(rows_h)))
            shp.name = f"Table {n}"
            tbl = shp.table
            tblPr = tbl._tbl.tblPr
            for a in ("firstRow", "bandRow"):
                tblPr.set(a, "0")
            from pptx.oxml.ns import qn
            style = tblPr.find(qn("a:tableStyleId"))
            if style is not None:
                style.text = "{5940675A-B579-460E-94D1-54222C63F5DA}"   # "No Style, Table Grid"
            for j, w in enumerate(cols):
                tbl.columns[j].width = cx.e(w)
            for i in range(nr):
                tbl.rows[i].height = cx.e(rows_h[i])
                for j in range(nc):
                    txt = b.rows[i][j] if j < len(b.rows[i]) else ""
                    c = tbl.cell(i, j)
                    c.margin_left = c.margin_right = cx.e(PAD_X)
                    c.margin_top = c.margin_bottom = cx.e(PAD_Y)
                    c.vertical_anchor = MSO_ANCHOR.MIDDLE
                    c.fill.solid()
                    c.fill.fore_color.rgb = _rgb(HEAD if i == 0 else (cx.pale if "**" in txt else WHITE))
                    tf = c.text_frame
                    tf.word_wrap = True
                    p = tf.paragraphs[0]
                    p.alignment = amap[b.align[j]]
                    _runs(cx, p, txt, bsize, bold_all=(i == 0))
                    _cell_borders(c)
        y += h + BLOCK_GAP
    return y


def fit_tier(blocks, width, avail):
    for tier in TIERS:
        if stack_height(blocks, width, tier) <= avail + 1e-6:
            return tier, 0.0
    return TIERS[-1], stack_height(blocks, width, TIERS[-1]) - avail


def add_figure(cx, slide, fig, x, y, w, h):
    """Image file fitted into the box, or a labelled dashed placeholder; caption flush under it."""
    cap = fig["caption"]
    cap_h = (wrap_count(cap, w - 0.06, CAPTION_PT) * CAPTION_PT * LINE / 72 + 0.06) if cap else 0
    bh = h - cap_h - (0.04 if cap else 0)
    if bh < 0.8:
        return False
    if fig["file"] is not None and fig["file"].is_file():
        from pptx.parts.image import Image
        iw, ih = Image.from_file(str(fig["file"])).size
        scale = min(w / iw, bh / ih)
        pw, ph = iw * scale, ih * scale
        pic = slide.shapes.add_picture(str(fig["file"]), cx.e(x + (w - pw) / 2), cx.e(y), cx.e(pw), cx.e(ph))
        pic.name = "Figure"
        bh = ph
    else:
        add_box(cx, slide, x, y, w, bh, f"[Figure placeholder]\n{fig['label']}\n(insert manually)", fill=PAPER,
                line=EDGE, size=12, color=GRAY, rounded=False, dash=True, name="Figure")
    if cap:
        add_line(cx, slide, x, y + bh + 0.04, w, cap_h, cap, CAPTION_PT, color=MUTED, name="Figure caption")
    return True


# ------------------------------------------------------------------------------------------------ slides

def pick_layout(prs, kind):
    names = {"title": ["TITLE", "Title Slide"], "content": ["TITLE_ONLY", "Title Only"]}[kind]
    for n in names:
        for lay in prs.slide_layouts:
            if lay.name == n:
                return lay
    if kind == "title":
        return prs.slide_layouts[0]
    for lay in prs.slide_layouts:
        types = [p.placeholder_format.type for p in lay.placeholders]
        if any("TITLE" in str(t) for t in types) and not any("BODY" in str(t) or "SUBTITLE" in str(t) for t in types):
            return lay
    return prs.slide_layouts[0]


def add_slide_number(slide):
    """Copy the layout's slide-number placeholder so the number shows on every slide."""
    from pptx.oxml.ns import qn
    ph = next((p for p in slide.slide_layout.placeholders if "SLIDE_NUMBER" in str(p.placeholder_format.type)), None)
    if ph is None:
        return
    sp = copy.deepcopy(ph._element)
    sp.find(".//" + qn("p:cNvPr")).set("id", str(max(s.shape_id for s in slide.shapes) + 1))
    body = sp.find(qn("p:txBody"))
    for p in body.findall(qn("a:p")):
        body.remove(p)
    p = _sub(body, "a:p")
    fld = _sub(p, "a:fld", id="{B6F15528-21DE-4FAA-801E-634DDDAF4B2B}", type="slidenum")
    _sub(fld, "a:rPr", lang="en-US")
    _sub(fld, "a:t").text = "‹#›"
    slide.shapes._spTree.append(sp)


def _source_text(t: str) -> str:
    return t if re.match(r"^sources?\b", t, re.I) else f"Sources: {t}"


def notes_text(s: Slide, clock: list) -> str:
    out = []
    if "minutes" in s.fields:
        m = float(s.get("minutes").split()[0])
        clock[0] += m
        mm, ss = divmod(round(clock[0] * 60), 60)
        out.append(f"Time: {m:g} min (ends {mm}:{ss:02d}).")
    if s.status == "open":
        out.append("OPEN: content not agreed yet; this slide is a placeholder.")
    if "full claim" in s.fields:
        out.append("Claim in full: " + strip_markup(s.get("full claim")))
    if "notes" in s.fields:
        out += [strip_markup(ln.rstrip()) for ln in s.fields["notes"].lines() if ln.strip()]
    if "transition" in s.fields:
        out.append("Transition: " + strip_markup(s.get("transition")))
    return "\n".join(out)


def new_content_slide(cx, s: Slide, draft_tags: bool):
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
    slide = cx.prs.slides.add_slide(pick_layout(cx.prs, "content"))
    t = slide.shapes.title
    if t is None:
        t = slide.shapes.add_textbox(cx.e(LEFT), cx.e(TITLE_Y), cx.e(WIDTH), cx.e(TITLE_H))
    t.name = "Title"
    t.left, t.top, t.width, t.height = cx.e(LEFT), cx.e(TITLE_Y), cx.e(WIDTH), cx.e(TITLE_H)
    tf = t.text_frame
    tf.text = strip_markup(s.title)
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = cx.e(0.03)
    tf.margin_top = tf.margin_bottom = cx.e(0)
    tf.vertical_anchor = MSO_ANCHOR.BOTTOM
    tf.paragraphs[0].alignment = PP_ALIGN.LEFT      # aligned with the body margin, whatever the template says
    for r in tf.paragraphs[0].runs:
        r.font.name, r.font.size, r.font.bold = cx.font, cx.pt(TITLE_PT), True
        r.font.color.rgb = _rgb(INK)
    tag = s.get("part")
    if draft_tags and s.status in ("proposed", "open"):
        tag = f"{tag} · {s.status.upper()}" if tag else s.status.upper()
    if tag:
        add_line(cx, slide, 6.2, 0.14, RIGHT - 6.2, 0.25, tag, PART_PT, color=GRAY, align=PP_ALIGN.RIGHT,
                 name="Part")
    add_slide_number(slide)
    return slide


def build_content(cx, s: Slide, spec: Spec, issues: Issues, draft_tags: bool):
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    slide = new_content_slide(cx, s, draft_tags)
    if s.get("claim"):
        add_line(cx, slide, LEFT, CLAIM_Y, WIDTH, CLAIM_H, s.get("claim"), CLAIM_PT, color=MUTED, name="Claim")
    has_band = "transition" in s.fields and s.status != "open"
    bottom = BOTTOM_BAND if has_band else BOTTOM_FREE
    avail = bottom - TOP
    if s.status == "open":
        sketch = [strip_markup(x.strip().lstrip("-").strip()) for x in
                  (s.fields["on the slide"].lines() if "on the slide" in s.fields else []) if x.strip()][:3]
        txt = "[Open: not agreed yet]\n" + ("\n".join(sketch) if sketch else "Content to be agreed.")
        add_box(cx, slide, LEFT, TOP, WIDTH, avail, txt, fill=PAPER, line=EDGE, size=13, color=GRAY,
                rounded=False, dash=True, name="Open placeholder")
    else:
        blocks = parse_blocks(s.fields["on the slide"].lines() if "on the slide" in s.fields else [], s.where,
                              Issues())
        fig = parse_figure(s, spec, Issues())
        over = 0.0
        if fig and fig["position"] in ("left", "right"):
            fw = WIDTH * fig["width"] - 0.15
            cw = WIDTH - fw - 0.3
            fx = LEFT if fig["position"] == "left" else RIGHT - fw
            bx = LEFT + fw + 0.3 if fig["position"] == "left" else LEFT
            if not blocks:
                fw, fx = WIDTH * fig["width"], LEFT + (WIDTH - WIDTH * fig["width"]) / 2
            add_figure(cx, slide, fig, fx, TOP, fw, avail)
            if blocks:
                tier, over = fit_tier(blocks, cw, avail)
                place_blocks(cx, slide, blocks, bx, TOP, cw, tier)
        else:
            min_fig = 1.6 if fig else 0
            tier, over = fit_tier(blocks, WIDTH, avail - min_fig - (BLOCK_GAP if fig and blocks else 0))
            used = stack_height(blocks, WIDTH, tier) if blocks else 0
            if fig:
                fig_h = avail - used - (BLOCK_GAP if blocks else 0)
                if fig["position"] == "above":
                    add_figure(cx, slide, fig, LEFT, TOP, WIDTH, fig_h)
                    place_blocks(cx, slide, blocks, LEFT, TOP + fig_h + BLOCK_GAP, WIDTH, tier)
                else:
                    end = place_blocks(cx, slide, blocks, LEFT, TOP, WIDTH, tier) if blocks else TOP
                    add_figure(cx, slide, fig, LEFT, end, WIDTH, fig_h)
            else:
                place_blocks(cx, slide, blocks, LEFT, TOP, WIDTH, tier)
        if over > 0.01:
            issues.warn(s.where, f"content overflows its area by about {over:.2f} in at the smallest font; "
                        "cut text or move detail to Notes")
    if has_band:
        band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx.e(LEFT), cx.e(BAND_Y), cx.e(WIDTH), cx.e(BAND_H))
        band.name = "Transition"
        band.fill.solid()
        band.fill.fore_color.rgb = _rgb(cx.band)
        band.line.fill.background()
        _plain(band)
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx.e(LEFT), cx.e(BAND_Y), cx.e(0.06), cx.e(BAND_H))
        bar.name = "Transition bar"
        bar.fill.solid()
        bar.fill.fore_color.rgb = _rgb(cx.accent)
        bar.line.fill.background()
        _plain(bar)
        tf = band.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left, tf.margin_right = cx.e(0.2), cx.e(0.1)
        tf.margin_top = tf.margin_bottom = cx.e(0.02)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        r = p.add_run()
        r.text = "→  "
        r.font.name, r.font.size, r.font.bold = cx.font, cx.pt(BAND_PT + 1), True
        r.font.color.rgb = _rgb(cx.accent)
        _runs(cx, p, s.get("transition"), BAND_PT)
    if "sources" in s.fields:
        add_line(cx, slide, LEFT, SRC_Y, SRC_W, SRC_H, _source_text(s.get("sources")), SRC_PT, color=GRAY,
                 anchor="middle", name="Source")
    return slide


def build_title(cx, s: Slide, settings):
    from pptx.enum.text import PP_ALIGN
    slide = cx.prs.slides.add_slide(pick_layout(cx.prs, "title"))
    t = slide.shapes.title
    t.name = "Title"
    t.text_frame.text = strip_markup(s.title)
    for r in t.text_frame.paragraphs[0].runs:
        r.font.size, r.font.bold, r.font.name = cx.pt(40), True, cx.font
    sub = next((p for p in slide.placeholders if p.placeholder_format.idx == 1), None)
    if sub is not None:
        if s.get("subtitle"):
            sub.name = "Subtitle"
            sub.text_frame.text = strip_markup(s.get("subtitle"))
            for r in sub.text_frame.paragraphs[0].runs:
                r.font.size, r.font.name = cx.pt(22), cx.font
                r.font.color.rgb = _rgb(cx.accent)
        else:
            sub._element.getparent().remove(sub._element)
    authors = s.get("authors") or settings["authors"]
    aff = ([x.strip().lstrip("- ").strip() for x in s.fields["affiliation"].lines() if x.strip()]
           if "affiliation" in s.fields else settings["affiliation"])
    lines = ([authors] if authors else []) + aff
    if lines:
        add_paras(cx, slide, LEFT, 4.0, WIDTH, 1.2, [("none", 0, ln, 1) for ln in lines], 12, color=MUTED, gap=3,
                  align=PP_ALIGN.CENTER, name="Authors")
    return slide


def build_references(cx, s: Slide, spec: Spec, issues: Issues, draft_tags: bool):
    slide = new_content_slide(cx, s, draft_tags)
    if "on the slide" in s.fields:
        lines = [x.strip() for x in s.fields["on the slide"].lines() if x.strip()]
    else:
        lines = [f"[{k}] {v}" for k, v in sorted(spec.refs.items())]
    paras = [("none", 0, ln.lstrip("- ").strip(), 1) for ln in lines]
    y0, avail = 1.15, BOTTOM_FREE - 1.15
    size = next((z for z in (12, 11, 10, 9) if text_height(paras, WIDTH, z, gap=4) <= avail), 9)
    if text_height(paras, WIDTH, size, gap=4) > avail:
        issues.warn(s.where, "references overflow the slide; split them over two slides")
    add_paras(cx, slide, LEFT, y0, WIDTH, avail, paras, size, gap=4, name="References")
    return slide


# ------------------------------------------------------------------------------------------------ verification

def _shape_text(slide, name):
    for sh in slide.shapes:
        if sh.name == name and sh.has_text_frame:
            return sh.text_frame.text
    return None


def verify(out: Path, spec: Spec, issues: Issues):
    """Round trip: re-open the saved deck and check that every spec field landed on its slide unchanged."""
    from pptx import Presentation
    prs = Presentation(str(out))
    if len(prs.slides) != len(spec.slides):
        issues.err(str(out), f"deck has {len(prs.slides)} slides, spec has {len(spec.slides)}")
        return
    for slide, s in zip(prs.slides, spec.slides):
        def check(name, want):
            got = _shape_text(slide, name)
            if got is None or got.replace("\x0b", "\n").strip() != want.strip():
                issues.err(s.where, f"round trip: {name} is {got!r}, spec says {want!r}")
        check("Title", strip_markup(s.title))
        if s.layout == "title":
            continue
        if s.layout == "content" and s.status != "open":
            if s.get("claim"):
                check("Claim", strip_markup(s.get("claim")))
            if "transition" in s.fields:
                check("Transition", "→  " + strip_markup(s.get("transition")))
            if "sources" in s.fields:
                check("Source", strip_markup(_source_text(s.get("sources"))))
            blocks = parse_blocks(s.fields["on the slide"].lines() if "on the slide" in s.fields else [], "", Issues())
            for n, b in enumerate(blocks, 1):
                if b.kind == "text":
                    check(f"Text {n}", "\n".join(strip_markup(p[2]) for p in b.paras))
                elif b.kind == "table":
                    sh = next((x for x in slide.shapes if x.name == f"Table {n}"), None)
                    got = [[c.text for c in r.cells] for r in sh.table.rows] if sh is not None else None
                    want = [[strip_markup(c) for c in r] + [""] * (len(b.rows[0]) - len(r)) for r in b.rows]
                    if got != want:
                        issues.err(s.where, f"round trip: Table {n} cells differ from the spec")
        notes = slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ""
        for ln in (s.fields["notes"].lines() if "notes" in s.fields else []):
            if ln.strip() and strip_markup(ln.rstrip()) not in notes:
                issues.err(s.where, f"round trip: notes line missing: {ln.strip()[:60]}")


# ------------------------------------------------------------------------------------------------ main

def drop_template_slides(prs):
    ids = prs.slides._sldIdLst
    for sid in list(ids):
        prs.part.drop_rel(sid.rId)
        ids.remove(sid)


def outline(spec: Spec) -> str:
    rows = ["| # | Part | Title | Status | Min |", "|---|---|---|---|---:|"]
    total = 0.0
    for s in spec.slides:
        m = s.get("minutes")
        try:
            total += float(m.split()[0]) if m else 0
        except ValueError:
            pass
        rows.append(f"| {s.num} | {s.get('part') or '-'} | {s.title} | {s.status or '?'} | {m or ''} |")
    rows.append(f"\nTotal: {total:g} min")
    return "\n".join(rows)


def default_out(spec: Spec) -> Path:
    if "output" in spec.deck:
        return (spec.path.parent / spec.deck["output"].text()).expanduser()
    stem = re.sub(r"[_-]spec$", "", spec.path.stem)
    return spec.path.with_name(stem + ".pptx")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--template")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--final", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--outline", action="store_true")
    ap.add_argument("--verify", type=Path, metavar="DECK")
    a = ap.parse_args(argv)
    issues = Issues()
    spec = parse_spec(a.spec.resolve(), issues)
    settings = load_settings(spec, issues, a.template)
    FONT_FAMILY[0] = settings["font"]
    validate(spec, issues, a.final)
    if a.outline:
        print(outline(spec))
    out = (a.out or default_out(spec)).resolve()
    if a.verify and not issues.errors:
        verify(a.verify.resolve(), spec, issues)
    elif not issues.errors:
        from pptx import Presentation
        prs = Presentation(str(settings["template"]))
        ratio = prs.slide_width / prs.slide_height
        if abs(ratio - 16 / 9) > 0.02:
            issues.warn(str(settings["template"]), "the layout grid is designed for 16:9; check the render")
        drop_template_slides(prs)
        cx = Ctx(prs, settings)
        clock = [0.0]
        for s in spec.slides:
            if s.layout == "title":
                sl = build_title(cx, s, settings)
            elif s.layout == "references":
                sl = build_references(cx, s, spec, issues, not a.final)
            else:
                sl = build_content(cx, s, spec, issues, not a.final)
            sl.notes_slide.notes_text_frame.text = notes_text(s, clock)
        if not a.check:
            out.parent.mkdir(parents=True, exist_ok=True)
            prs.save(str(out))
            verify(out, spec, issues)
    for w in issues.warnings:
        print(f"WARNING {w}", file=sys.stderr)
    for e in issues.errors:
        print(f"ERROR {e}", file=sys.stderr)
    counts = {k: sum(1 for s in spec.slides if s.status == k) for k in STATUSES}
    summary = (f"{len(spec.slides)} slides (agreed {counts['agreed']}, proposed {counts['proposed']}, "
               f"open {counts['open']}); {len(issues.errors)} errors, {len(issues.warnings)} warnings")
    failed = bool(issues.errors) or ((a.strict or a.final) and bool(issues.warnings))
    if failed:
        wrote = " (deck written; fix before handing over)" if out.exists() and not (a.check or a.verify) else ""
        print(f"FAILED: {summary}{wrote}", file=sys.stderr)
        return 1
    done = f"{a.verify} matches the spec" if a.verify else ("checked" if a.check else f"wrote {out}")
    print(f"{done}: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
