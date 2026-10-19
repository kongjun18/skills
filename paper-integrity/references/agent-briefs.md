# Agent briefs

Paste the matching brief into each subagent prompt and fill in `<OUT>`,
`<PAPER_DIR>`, `<SKILL_DIR>`, `<BATCH>` (the batch name from
`plan_agents.py`, such as `claims3`), and `<ITEMS>` (that batch's items).
Every agent reads [citation-rules.md](citation-rules.md) and
[severity.md](severity.md), writes only its own files in the run directory,
and never edits the manuscript or the bibliography.

## Shared formats

**Finding** (claim, omission, and new findings from triage or refute). Agents
write a JSON list. `report.py` derives the stable `id` from `stage`,
`category`, and `anchor`, so agents must not invent ids.

```json
{
  "stage": "C",
  "severity": "S0",
  "confidence": "verified",
  "category": "contradicted",
  "anchor": "U-1a2b3c4d",
  "location": "sections/intro.tex:12",
  "key": "smith2020",
  "evidence": "Paper: \"...\". Source (Sec. 5.2, Table 3): \"...\". Explain the gap.",
  "suggestion": "Narrow to \"...\" or cite the source that states it."
}
```

- `stage` is `C` (claim support), `A` (omission), or `R` (new finding raised
  during triage or refute).
- `anchor` is the ledger `use_id` for claim findings, `section|term` for
  omission findings, and `key|category` for reference findings. Keep it the
  same across runs so the ID stays stable.

**Decision** (triage and refute) on an existing finding id:

```json
{"id": "I-4685edc5", "verdict": "upheld|refuted|downgraded", "severity": "S2",
 "confirmed": true, "reason": "Evidence with URL or quote."}
```

`severity` applies only to `downgraded`. Set `confirmed` to true only when an
upheld finding now has direct evidence.

## Stage 2b: triage of suspected references (fast and full)

```
You confirm or clear reference problems that scripts could only suspect.
Run dir: <OUT>. Finding ids: <ITEMS> (details in <OUT>/report.json; script
records in <OUT>/identity.json; bibliography entries are at each finding's
location under <PAPER_DIR>).
Read <SKILL_DIR>/references/citation-rules.md (Identity and existence) and
<SKILL_DIR>/references/severity.md first.

For each finding:
1. Search for the work with web search and publisher, proceedings, DBLP, arXiv,
   and vendor pages: title variants, author plus title, and the venue. Search
   only with reference metadata; never paste manuscript text.
2. Decide:
   - refuted: the reference is fine (the work exists and the entry matches it,
     or the link works in a browser). Give the URL.
   - upheld: the problem is real. Set confirmed=true when you have direct
     evidence, such as the publisher page showing a different year or venue.
   - downgraded: real but minor. Give the tier from severity.md.
3. When you find the correct metadata or a stable URL, put it in the reason so
   the author can fix the entry. Never invent metadata.

Write <OUT>/triage-<BATCH>.json: a list of decisions. Write any new problem you
find to <OUT>/findings-triage-<BATCH>.json with stage "R".
Return one line per finding: id, verdict, and the key evidence.
```

## Stage 4: claim support (full)

```
You verify citations for one batch of cited works in a paper.
Run dir: <OUT>. Keys: <ITEMS>. Paper sources: <PAPER_DIR>.
Read <SKILL_DIR>/references/citation-rules.md and severity.md first.

For each key:
1. Read its uses in <OUT>/ledger.jsonl (key, sentence, previous_sentence,
   co_cited, location). Open the .tex file at the location when the sentence
   needs more context.
2. Read the source text <OUT>/sources/<key>.txt, its access level in
   <OUT>/sources/index.json, and the record in <OUT>/identity.json. If the
   access level is abstract or none, try to fetch the full text (publisher
   open-access page, arXiv, author page). Save it as <OUT>/sources/<key>.txt,
   and record the new access level and origin in
   <OUT>/sources/agent-<BATCH>.json as {key: {access, origin}}.
   Do not send manuscript text to external services.
3. For each use, decide its role and verdict per citation-rules.md. Quote the
   source verbatim, with a locator, for every verdict except no-access.
4. Check the prose attribution (named authors and systems), and whether we
   describe the work fairly.

Write <OUT>/verdicts-<BATCH>.json: a list of
  {use_id, key, role, verdict, quote, locator, access, note}
and <OUT>/findings-claims-<BATCH>.json: a finding for every verdict other than
supported, plus prose-attribution defects. A no-access use becomes an S1
finding with confidence "no-access" and the suggestion "supply <key>.pdf in
the local PDF dir".
Return: uses checked, counts by verdict, and the S0 list.
```

## Stage 5: omission and anonymity (full)

```
You look for borrowed work that the paper uses without citing it.
Run dir: <OUT>. Files: <ITEMS> (relative to <PAPER_DIR>).
Venue review mode: <double-blind|single-blind|unknown>.
Read <SKILL_DIR>/references/citation-rules.md (Omissions) and severity.md.

1. Read the files in full.
2. List every named system, dataset, trace, baseline, algorithm, nonstandard
   data structure, external metric, adapted figure or table, and quoted
   definition. For each, check whether a citation appears at or before its
   first substantive use anywhere in the paper (search <OUT>/ledger.jsonl and
   the .tex files).
3. Report uncited items as category uncited-borrowed-work, S0 suspected, with
   anchor "<section>|<term>". Name the work that should probably be cited only
   when you have verified it; otherwise write "author to supply".
4. For a double-blind venue, report first-person self-citations as
   anonymity-breach.
Skip textbook concepts and the paper's own contributions.

Write <OUT>/findings-omission-<BATCH>.json. Return the list of items.
```

## Stage 7: refute (full, wave B)

Use fresh agents, never the ones that produced the findings.
`plan_agents.py refute` already skips mechanical findings, verified identity
findings, and findings that triage decided.

```
You try to disprove integrity findings. Be adversarial: a false S0 wastes the
author's time, and a missed S0 can damage a reputation.
Run dir: <OUT>. Finding ids: <ITEMS> (details in <OUT>/report.json).
Read <SKILL_DIR>/references/citation-rules.md and severity.md.

For each finding, re-read the manuscript location and the source independently,
and fetch more of the source if needed. Decide upheld, refuted, or downgraded,
with a quote or URL as the reason. If you find a new S0 while checking, add it
to <OUT>/findings-refute-<BATCH>.json with stage "R".

Write <OUT>/refute-<BATCH>.json: a list of decisions.
Return counts by verdict and every upheld S0.
```
