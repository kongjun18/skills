#!/usr/bin/env python3
"""Write a copy of a tutorial with check-yourself answers removed, for the learner reviewer.

Usage:
    strip_answers.py TUTORIAL.html OUT.html

Removes every `<div class="answer">...</div>`. Answers must not contain a
nested <div>; the script fails if the count of removed answers does not
match the count of check-yourself questions.
"""

import re
import sys
from pathlib import Path

ANSWER_RE = re.compile(r'<div class="answer">.*?</div>', re.S)


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    text = src.read_text(encoding="utf-8")
    checks = len(re.findall(r'<details class="check"', text))
    stripped, n = ANSWER_RE.subn("", text)
    if n != checks or re.search(r'class="answer"', stripped):
        print(f"error: removed {n} answers for {checks} checks; is a <div> nested in an answer?", file=sys.stderr)
        return 1
    out.write_text(stripped, encoding="utf-8")
    print(f"{out}: {n} answers removed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
