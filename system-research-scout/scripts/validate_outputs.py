#!/usr/bin/env python3
"""Pre-flight validator for system-research-scout outputs.

Enforces gates A-J listed in SKILL.md ("Pre-flight gates"). The skill is not
complete until this script exits with status 0. Empty or unfilled outputs fail
(gate J): a run with no sparks, no curated tags, no venue reads, or no ideas is
not a passing run.

Each check runs independently so partial failures still produce a useful
report. Exit code is the number of failed gates (capped at 1 for non-zero
shell semantics; use --strict to exit with the actual failure count).

Usage:
  python3 <skill-dir>/scripts/validate_outputs.py --out DIR
  (reads DIR/papers, DIR/thinking, DIR/sparking; --papers/--thinking/--sparking
  override individual directories)
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path


# ---------- Helpers ----------

FORBIDDEN_SUBSTRINGS = [
    "TODO",
    "TBD",
    "refine after",
    "infer from",
    "look for",
    "Title TBA",
    "to be filled",
    "placeholder",
    "TO_BE_REPLACED",
]

LENS_PATTERN = re.compile(r"\bL(?:1[01]|[1-9])\b")
LENS_LINE = re.compile(r"^\s*-\s*Lens applied\s*:", re.M)
BASELINE_LINE = re.compile(r"^\s*-\s*Baseline that breaks\s*:", re.M)
PRIOR_ART_LINE = re.compile(r"^\s*-\s*Closest prior art\s*:", re.M)
ONE_SENTENCE_IDEA_LINE = re.compile(r"^\s*-\s*One-sentence idea\s*:", re.M)
OBSERVED_MISMATCH = re.compile(
    r"^\s*-\s*Observed mismatch\s*:\s*[\"“](.+?)[\"”]",
    re.M | re.S,
)
ROLE_TAGS = {"motivating", "corroborating", "solves-one-piece",
             "competing-approach", "disconfirming"}

FORBIDDEN_CURATED_TAG = "general-systems"


def strip_code_fences(text: str) -> str:
    """Remove ``` fenced blocks so the TODO-scaffold gate ignores legitimate
    code-fence examples."""
    return re.sub(r"```.*?```", "", text, flags=re.S)


def normalize_quote(text: str) -> str:
    """Normalize text for verbatim-quote matching: NFKC (ligatures), straight
    quotes, lowercase, and line-break hyphenation removed ("sys- tem" and
    "system" match), whitespace collapsed. Applied to both quote and corpus."""
    text = unicodedata.normalize("NFKC", text or "")
    text = text.translate(str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'",
                                         "\u00ad": "", "–": "-", "—": "-"}))
    text = re.sub(r"-\s*", "", text)
    return re.sub(r"\s+", " ", text).strip().lower()


_PDF_TEXT_CACHE: dict[str, str] = {}


def local_pdf_text(paper: dict) -> str:
    """Full pdftotext output of the paper's local PDF, normalized; "" if none."""
    path = paper.get("local_pdf") or ""
    if not path:
        return ""
    if path not in _PDF_TEXT_CACHE:
        text = ""
        if shutil.which("pdftotext") and Path(path).is_file():
            try:
                out = subprocess.run(["pdftotext", "-q", path, "-"], capture_output=True,
                                     timeout=120, check=False)
                text = out.stdout.decode("utf-8", errors="replace")
            except (OSError, subprocess.TimeoutExpired):
                text = ""
        _PDF_TEXT_CACHE[path] = normalize_quote(text)
    return _PDF_TEXT_CACHE[path]


@dataclass
class GateResult:
    name: str
    passed: bool
    failures: list[str]

    def render(self) -> str:
        head = f"[{'PASS' if self.passed else 'FAIL'}] {self.name}"
        if self.passed or not self.failures:
            return head
        body = "\n".join(f"    - {f}" for f in self.failures[:20])
        if len(self.failures) > 20:
            body += f"\n    - ... ({len(self.failures) - 20} more)"
        return head + "\n" + body


# ---------- Load inputs ----------

def load_papers(papers_dir: Path) -> list[dict]:
    path = papers_dir / "metadata.jsonl"
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if "title" in d:  # skip status-only rows
            rows.append(d)
    return rows


def load_sparks(sparking_dir: Path) -> dict[Path, str]:
    if not sparking_dir.exists():
        return {}
    return {p: p.read_text(encoding="utf-8") for p in sorted(sparking_dir.glob("*.md"))}


def load_thinking_files(thinking_dir: Path) -> dict[Path, str]:
    """Load every .md file under thinking/ recursively."""
    if not thinking_dir.exists():
        return {}
    out: dict[Path, str] = {}
    for p in sorted(thinking_dir.rglob("*.md")):
        out[p] = p.read_text(encoding="utf-8")
    return out


# ---------- Gates ----------

def gate_a_no_scaffolding(thinking_files: dict[Path, str],
                          spark_files: dict[Path, str]) -> GateResult:
    failures: list[str] = []
    for path, text in {**thinking_files, **spark_files}.items():
        stripped = strip_code_fences(text)
        for needle in FORBIDDEN_SUBSTRINGS:
            for m in re.finditer(re.escape(needle), stripped):
                line_no = stripped.count("\n", 0, m.start()) + 1
                failures.append(f"{path}:{line_no}: forbidden substring {needle!r}")
    return GateResult("A. No TODO scaffolding", not failures, failures)


def gate_b_coverage_gated_trend(thinking_files: dict[Path, str]) -> GateResult:
    failures: list[str] = []
    trend_path = next((p for p in thinking_files if p.name == "topic_trend.md"), None)
    ledger_path = next((p for p in thinking_files if p.name == "coverage_ledger.md"), None)
    if trend_path is None:
        return GateResult("B. Coverage-gated trend", False,
                          ["thinking/topic_trend.md is missing"])
    if ledger_path is None:
        failures.append("thinking/coverage_ledger.md is missing — required by gate B")
    trend_text = thinking_files[trend_path]
    if "coverage_ledger.md" not in trend_text:
        failures.append(f"{trend_path}: does not reference coverage_ledger.md")
    # Each topic row must include Completeness:
    rows = re.split(r"^##\s+", trend_text, flags=re.M)[1:]
    for row in rows:
        head = row.splitlines()[0].strip() if row.splitlines() else "<empty>"
        if "Completeness" not in row:
            failures.append(f"{trend_path}: row '{head}' missing 'Completeness:' line")
        direction_m = re.search(r"Direction\s*:\s*([^\n]+)", row)
        if direction_m:
            direction = direction_m.group(1).strip().lower()
            if direction.split()[0] in {"rising", "fading", "stable", "emerging"}:
                # Must have completeness >= 0.9 evidence written out.
                completeness_m = re.search(
                    r"Completeness\s*:\s*([^\n]+)", row)
                completeness_text = completeness_m.group(1) if completeness_m else ""
                # Heuristic: look for a number >= 0.9 in the Completeness line,
                # OR explicit "complete" wording. The validator does not try
                # to re-derive completeness from the ledger; that's the
                # author's job.
                nums = [float(x) for x in re.findall(r"0?\.\d+|1\.0+", completeness_text)]
                # Every numeric completeness value present must be >= 0.9.
                # Rationale: a row that says "A=1.00, B=0.42" cannot support a
                # rising/fading claim because year B is too sparse to compare.
                if nums and min(nums) < 0.9 and "complete" not in completeness_text.lower():
                    failures.append(
                        f"{trend_path}: row '{head}' labels Direction={direction} but "
                        f"Completeness min={min(nums):.2f} < 0.9 — use "
                        "'unknown — partial coverage' instead.")
    return GateResult("B. Coverage-gated trend", not failures, failures)


def gate_c_evidence_chain(spark_files: dict[Path, str],
                          papers: list[dict]) -> GateResult:
    """Every spark has an Observed-mismatch quote, and each quote appears
    verbatim (after normalize_quote) in a paper's abstract or
    introduction_excerpt, or in the local PDF text of a paper the spark cites.
    This is the single checkable-corpus rule stated in SKILL.md."""
    failures: list[str] = []
    corpus = " ".join(normalize_quote(p.get("abstract", "")) + " " +
                      normalize_quote(p.get("introduction_excerpt", "")) for p in papers)
    titles = {p.get("title", ""): p for p in papers}
    for path, text in spark_files.items():
        quotes = list(OBSERVED_MISMATCH.finditer(text))
        if not quotes:
            failures.append(f"{path}: no 'Observed mismatch: \"...\"' quote — every spark needs one")
            continue
        cited = [titles[t] for t in _cited_paper_titles(text, set(titles))]
        for m in quotes:
            quote = normalize_quote(m.group(1))
            if len(quote) < 8:
                failures.append(f"{path}: Observed-mismatch quote too short to verify")
                continue
            if quote in corpus:
                continue
            if any(quote in local_pdf_text(p) for p in cited):
                continue
            failures.append(
                f"{path}: Observed-mismatch quote not found in any abstract, "
                "introduction_excerpt, or the local PDF of a cited paper — possible "
                f"fabrication. Quote starts: {quote[:80]!r}")
    return GateResult("C. Evidence chain", not failures, failures)


def _cited_paper_titles(spark_text: str, paper_titles: set[str]) -> set[str]:
    cited: set[str] = set()
    for title in paper_titles:
        if not title:
            continue
        # Match the title literally (case-insensitive). Titles tend to be
        # long enough that false positives are rare.
        if title.lower() in spark_text.lower():
            cited.add(title)
    return cited


def gate_d_spark_diversity(spark_files: dict[Path, str],
                           papers: list[dict]) -> GateResult:
    failures: list[str] = []
    titles = {p.get("title", "") for p in papers}
    paper_sets: dict[Path, set[str]] = {
        path: _cited_paper_titles(text, titles)
        for path, text in spark_files.items()
    }
    keys = list(paper_sets.keys())
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            a, b = paper_sets[keys[i]], paper_sets[keys[j]]
            if not a or not b:
                continue
            overlap = len(a & b) / max(len(a | b), 1)
            if overlap > 0.5:
                failures.append(
                    f"{keys[i].name} and {keys[j].name} share {overlap:.0%} "
                    f"of cited papers ({len(a & b)}/{len(a | b)}) — "
                    "exceeds 50% diversity gate.")
    return GateResult("D. Spark diversity", not failures, failures)


def gate_e_tag_justification(papers: list[dict]) -> GateResult:
    failures: list[str] = []
    for p in papers:
        curated = p.get("topic_tags_curated") or []
        if not curated:
            continue
        evidence = p.get("topic_tag_evidence") or {}
        abstract = normalize_quote(p.get("abstract", ""))
        for tag in curated:
            if tag not in evidence:
                failures.append(
                    f"{p.get('title','<no title>')[:80]}: curated tag {tag!r} "
                    "has no topic_tag_evidence entry.")
                continue
            quote = normalize_quote(evidence[tag])
            if len(quote) < 8 or quote not in abstract:
                failures.append(
                    f"{p.get('title','<no title>')[:80]}: evidence for tag "
                    f"{tag!r} not found in abstract.")
    return GateResult("E. Tag justification", not failures, failures)


def gate_f_lens_applied(spark_files: dict[Path, str],
                        thinking_files: dict[Path, str]) -> GateResult:
    failures: list[str] = []
    # Sparks: each file must have a Lens applied line
    for path, text in spark_files.items():
        if not LENS_LINE.search(text):
            failures.append(f"{path}: missing 'Lens applied:' line")
            continue
        # Each Lens applied line must name at least one L1-L11
        for m in LENS_LINE.finditer(text):
            line_end = text.find("\n", m.end())
            line = text[m.end():line_end if line_end != -1 else len(text)]
            if not LENS_PATTERN.search(line):
                failures.append(f"{path}: 'Lens applied:' line does not name L1-L11")
    # Detailed ideas: each H2 block in research_ideas.md must have a Lens line
    ideas_path = next((p for p in thinking_files if p.name == "research_ideas.md"), None)
    if ideas_path is not None:
        blocks = re.split(r"^##\s+", thinking_files[ideas_path], flags=re.M)[1:]
        for block in blocks:
            head = block.splitlines()[0].strip() if block.splitlines() else "<empty>"
            if not LENS_LINE.search("##" + block):  # restore the marker for the regex
                failures.append(f"{ideas_path}: idea '{head}' missing 'Lens applied:' line")
    return GateResult("F. Lens applied", not failures, failures)


def gate_g_no_forbidden_tag(papers: list[dict]) -> GateResult:
    failures: list[str] = []
    for p in papers:
        curated = p.get("topic_tags_curated") or []
        if FORBIDDEN_CURATED_TAG in curated:
            failures.append(
                f"{p.get('title','<no title>')[:80]}: uses forbidden curated "
                f"tag {FORBIDDEN_CURATED_TAG!r}")
    return GateResult("G. No forbidden tag", not failures, failures)


def gate_h_awards_parsed(papers: list[dict]) -> GateResult:
    """We don't re-fetch USENIX pages here; instead we check internal
    consistency: any paper whose `note` or `authors` field still contains
    an award marker must have an `awards` entry. This catches papers where
    BibTeX-stripping ran but award detection failed."""
    failures: list[str] = []
    for p in papers:
        blob = (p.get("authors", "") + " " + p.get("note", "")).lower()
        flagged = ("best paper" in blob or "distinguished artifact" in blob)
        if flagged and not p.get("awards"):
            failures.append(
                f"{p.get('title','<no title>')[:80]}: authors/note mentions an "
                "award but `awards` list is empty.")
    return GateResult("H. Awards parsed", not failures, failures)


def gate_i_idea_grammar(thinking_files: dict[Path, str]) -> GateResult:
    failures: list[str] = []
    ideas_path = next((p for p in thinking_files if p.name == "research_ideas.md"), None)
    if ideas_path is None:
        return GateResult("I. Idea grammar", False,
                          ["thinking/research_ideas.md is missing"])
    text = thinking_files[ideas_path]
    blocks = re.split(r"^##\s+", text, flags=re.M)[1:]
    for block in blocks:
        head = block.splitlines()[0].strip() if block.splitlines() else "<empty>"
        block_text = "##" + block
        if not ONE_SENTENCE_IDEA_LINE.search(block_text):
            failures.append(f"idea '{head}': missing 'One-sentence idea:' line")
        if not BASELINE_LINE.search(block_text):
            failures.append(f"idea '{head}': missing 'Baseline that breaks:' line")
        if not PRIOR_ART_LINE.search(block_text):
            failures.append(
                f"idea '{head}': missing 'Closest prior art:' line — "
                "the Step 6a novelty check populates this; without it the idea "
                "cannot enter the ranked output.")
        role_count = sum(
            1 for tag in ROLE_TAGS
            if re.search(rf"\b{re.escape(tag)}\b", block)
        )
        if role_count < 1:
            failures.append(
                f"idea '{head}': no per-paper role tags found "
                f"(expected at least 3 papers with roles in "
                f"{sorted(ROLE_TAGS)})")
        # Count how many paper entries actually carry a role marker.
        # Heuristic: count occurrences of "— motivating", "— corroborating", etc.
        role_marker_count = sum(
            len(re.findall(rf"[—-]\s*{re.escape(tag)}\b", block))
            for tag in ROLE_TAGS
        )
        if role_marker_count < 3:
            failures.append(
                f"idea '{head}': only {role_marker_count} papers tagged with a role; "
                "need at least 3 per references/final_deliverables.md.")
    return GateResult("I. Idea grammar", not failures, failures)


def gate_j_non_empty(papers: list[dict], spark_files: dict[Path, str],
                     thinking_files: dict[Path, str], papers_dir: Path) -> GateResult:
    """A run with nothing to check is not a passing run."""
    failures: list[str] = []
    if not papers:
        failures.append(f"{papers_dir / 'metadata.jsonl'}: missing or has no paper rows — "
                        "run survey_top_systems.py --out DIR first")
    elif not any(p.get("topic_tags_curated") for p in papers):
        failures.append("no paper has topic_tags_curated — reader agents (Step 4) must curate tags "
                        "with quoted topic_tag_evidence")
    if not spark_files:
        failures.append("sparking/ has no spark files — Step 7 must write at least one spark")
    if not any(p.parent.name == "venue_reads" for p in thinking_files):
        failures.append("thinking/venue_reads/ is empty — Step 4 reader output is missing")
    if not any(p.name == "coverage_ledger.md" for p in thinking_files):
        failures.append("thinking/coverage_ledger.md is missing — Step 1 output")
    ideas = next((t for p, t in thinking_files.items() if p.name == "research_ideas.md"), "")
    if not re.search(r"^##\s+\S", ideas, re.M):
        failures.append("thinking/research_ideas.md has no '## ' idea blocks")
    return GateResult("J. Non-empty outputs", not failures, failures)


# ---------- Driver ----------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", help="Workspace passed to survey_top_systems.py --out.")
    parser.add_argument("--thinking", help="Override OUT/thinking.")
    parser.add_argument("--sparking", help="Override OUT/sparking.")
    parser.add_argument("--papers", help="Override OUT/papers.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with the actual count of failed gates (otherwise capped at 1).",
    )
    args = parser.parse_args()

    if not args.out and not (args.thinking and args.sparking and args.papers):
        parser.error("pass --out DIR (or all of --papers, --thinking, --sparking)")
    out = Path(args.out).expanduser() if args.out else None
    thinking_dir = Path(args.thinking) if args.thinking else out / "thinking"
    sparking_dir = Path(args.sparking) if args.sparking else out / "sparking"
    papers_dir = Path(args.papers) if args.papers else out / "papers"

    papers = load_papers(papers_dir)
    spark_files = load_sparks(sparking_dir)
    thinking_files = load_thinking_files(thinking_dir)

    results = [
        gate_j_non_empty(papers, spark_files, thinking_files, papers_dir),
        gate_a_no_scaffolding(thinking_files, spark_files),
        gate_b_coverage_gated_trend(thinking_files),
        gate_c_evidence_chain(spark_files, papers),
        gate_d_spark_diversity(spark_files, papers),
        gate_e_tag_justification(papers),
        gate_f_lens_applied(spark_files, thinking_files),
        gate_g_no_forbidden_tag(papers),
        gate_h_awards_parsed(papers),
        gate_i_idea_grammar(thinking_files),
    ]

    print(f"system-research-scout pre-flight validator")
    print(f"papers={len(papers)}, sparks={len(spark_files)}, "
          f"thinking_files={len(thinking_files)}")
    print("-" * 60)
    for r in results:
        print(r.render())
    print("-" * 60)
    failed = sum(1 for r in results if not r.passed)
    if failed == 0:
        print("All gates passed.")
        return 0
    print(f"{failed} gate(s) failed.")
    return failed if args.strict else 1


if __name__ == "__main__":
    sys.exit(main())
