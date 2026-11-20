# Affiliations procedure

Read this during evaluation (stage 4), when adding the who's-behind-it signal
to curated papers.

For every curated paper, show who is behind it at a glance. The script does the
deterministic extraction; the agent interprets.

## Extract

Run the helper after the filter stage, on the ids of the papers you kept (not
the raw keyword hits, which still include misfires):

```bash
python3 $SKILL/scripts/affiliations.py 2607.13604 2607.13276 ...
```

`--from-json --curated` reads every non-catch-all paper from a saved fetch JSON
on stdin; that is the pre-curation set, so prefer explicit ids.

It emits `{id: {"block": "<raw author/affiliation text>", "emails": [...],
"email_domains": [...], "source": "html|pdf|none"}}` and prints the source and
email domains per paper to stderr. It reads `https://arxiv.org/html/{id}` (the
author block of the HTML render), falling back to the PDF author region via
`pdftotext`. It does no name cleanup or classification.

- `--delay` (default 1.5 s) spaces fetches to avoid arXiv HTTP 429; raise it for
  large batches.
- `source: "none"` or an empty `block` means neither the HTML render nor the
  PDF resolved: leave the affiliation blank, never guess.

## Interpret

Read each `block`, with `email_domains` as a hint, and produce for the digest:

- the distinct institution name(s), cleaned to a recognizable short form (for
  example "ETH Zürich", "AWS", "MIT CSAIL"); the raw block is often messy, with
  author names running into institutions and trailing city or country;
- an `academia` / `industry` / `both` tag: `.edu`, `.ac.*`, or a university
  means academia; a company domain or company name means industry.

Why a script for extraction but not parsing: the arXiv Atom API carries no
affiliations, and OpenAlex has none for fresh preprints, so the text must come
from the paper; turning that text into a clean name is judgment.

## Use

The number of distinct groups on a thread separates an emerging opening (one or
two papers, no incumbent) from a crowded thread (several groups racing). Feed
that into the opportunity read.
