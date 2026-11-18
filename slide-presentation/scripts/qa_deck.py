#!/usr/bin/env python3
"""Render a .pptx to PDF and per-slide PNGs, and lint its text (slides, tables, notes).

Run:
  uv run --no-project --with python-pptx python <skill>/scripts/qa_deck.py DECK.pptx \
      [--spec SPEC.md] [--ban TERM ...] [--render OUTDIR] [--dpi 110]

Lint:
  - banned terms (errors): from the spec's Deck section, the project profile (slide-profile.md) and --ban;
    a term written /regex/ is a regular expression; plain terms match whole words, case-sensitively;
  - over-stating words (warnings): absolutes such as must, never, always, cannot, only, exactly;
    review each hit and rewrite or keep it deliberately;
  - internal-looking strings (warnings): file paths and file names.
Render: LibreOffice headless -> OUTDIR/<deck>.pdf -> OUTDIR/slide-NN.png (pdftoppm). Look at every PNG.

Exit status: 1 if a banned term is found or rendering fails, else 0.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import warnings
import tempfile
from pathlib import Path

warnings.filterwarnings("ignore", message=".*global interpreter lock.*")  # lxml on free-threaded Python

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_deck  # noqa: E402

OVERSTATE = [r"must", r"never", r"always", r"cannot", r"can't", r"can ?not", r"no one", r"nobody", r"none",
             r"impossible", r"guarantee[sd]?", r"prove[sdn]?", r"proof", r"exactly", r"only", r"completely",
             r"entirely", r"solve[sd]?", r"eliminate[sd]?", r"the first", r"first to", r"unique(?:ly)?",
             r"clearly", r"obviously"]
OVER_RE = re.compile(r"(?<![\w-])(" + "|".join(OVERSTATE) + r")(?![\w-])", re.I)
INTERNAL_RE = re.compile(r"(?<![\w/])(?:[\w.-]+/){2,}[\w.-]+|(?<![\w/])[\w-]+(?:/[\w.-]+)*\.(?:py|md|json|csv|ya?ml|"
                         r"log|sh|txt|ipynb|pptx)\b")


def slide_texts(pptx: Path):
    from pptx import Presentation
    for i, s in enumerate(Presentation(str(pptx)).slides, 1):
        for sh in s.shapes:
            if sh.has_text_frame and sh.text_frame.text.strip():
                yield i, sh.name, sh.text_frame.text
            if getattr(sh, "has_table", False) and sh.has_table:
                for r in sh.table.rows:
                    for c in r.cells:
                        if c.text.strip():
                            yield i, sh.name, c.text
        if s.has_notes_slide:   # the builder copies the transition into the notes; lint it once, in the band
            notes = s.notes_slide.notes_text_frame.text.split("\n")
            yield i, "notes", "\n".join(ln for ln in notes if not ln.startswith("Transition: "))


def banned_patterns(spec: Path | None, extra: list[str]):
    terms = list(extra)
    if spec:
        issues = build_deck.Issues()
        sp = build_deck.parse_spec(spec.resolve(), issues)
        terms += build_deck.load_settings(sp, issues)["banned"]
    pats = []
    for t in dict.fromkeys(terms):
        if len(t) > 2 and t.startswith("/") and t.endswith("/"):
            pats.append((t, re.compile(t[1:-1])))
        else:
            pats.append((t, re.compile(r"(?<![\w-])" + re.escape(t) + r"(?![\w-])")))
    return pats


def ctx(text, m, width=40):
    a, b = max(m.start() - width, 0), min(m.end() + width, len(text))
    return ("…" if a else "") + text[a:b].replace("\n", " ") + ("…" if b < len(text) else "")


def lint(pptx: Path, spec: Path | None, extra: list[str]) -> int:
    pats = banned_patterns(spec, extra)
    n_err = n_warn = 0
    for i, where, text in slide_texts(pptx):
        for term, rx in pats:
            for m in rx.finditer(text):
                print(f"ERROR   slide {i} [{where}] banned term '{term}': {ctx(text, m)}")
                n_err += 1
        for m in OVER_RE.finditer(text):
            print(f"WARNING slide {i} [{where}] over-stating? '{m.group(0)}': {ctx(text, m)}")
            n_warn += 1
        for m in INTERNAL_RE.finditer(text):
            print(f"WARNING slide {i} [{where}] internal name or path? '{m.group(0)}'")
            n_warn += 1
    print(f"lint: {n_err} banned-term hits, {n_warn} warnings to review ({len(pats)} banned terms checked)")
    return n_err


def render(pptx: Path, outdir: Path, dpi: int) -> int:
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice or not shutil.which("pdftoppm"):
        print("ERROR render needs LibreOffice (soffice) and pdftoppm (poppler)")
        return 1
    outdir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="lo-profile-") as prof:
        r = subprocess.run([soffice, f"-env:UserInstallation=file://{prof}", "--headless", "--convert-to", "pdf",
                            "--outdir", str(outdir), str(pptx)], capture_output=True, text=True, timeout=300)
    pdf = outdir / (pptx.stem + ".pdf")
    if r.returncode or not pdf.is_file():
        print(f"ERROR LibreOffice conversion failed: {r.stderr.strip() or r.stdout.strip()}")
        return 1
    for old in outdir.glob("slide-*.png"):
        old.unlink()
    subprocess.run(["pdftoppm", "-png", "-r", str(dpi), str(pdf), str(outdir / "slide")], check=True)
    pngs = sorted(outdir.glob("slide-*.png"))
    print(f"rendered {pdf} and {len(pngs)} PNGs in {outdir}; inspect every one")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pptx", type=Path)
    ap.add_argument("--spec", type=Path, help="deck spec; supplies banned terms (Deck + project profile)")
    ap.add_argument("--ban", nargs="*", default=[], help="extra banned terms; /regex/ allowed")
    ap.add_argument("--render", type=Path, metavar="OUTDIR", help="render PDF and PNGs into OUTDIR")
    ap.add_argument("--dpi", type=int, default=110)
    a = ap.parse_args(argv)
    if not a.pptx.is_file():
        print(f"ERROR not found: {a.pptx}")
        return 1
    rc = 1 if lint(a.pptx, a.spec, a.ban) else 0
    if a.render:
        rc |= render(a.pptx.resolve(), a.render.resolve(), a.dpi)
    return rc


if __name__ == "__main__":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    sys.exit(main())
