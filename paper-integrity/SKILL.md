---
name: paper-integrity
description: Report-only pre-submission integrity gate for academic papers, currently covering citations. Checks that cited works exist and match their entries (DOI, arXiv, metadata, retraction, preprint vs published), that each citation supports its sentence, that borrowed systems, datasets, or methods are cited, and that text is not copied from sources. Ranks issues S0 (blocker), S1 (major), S2 (minor), reports a PASS / NOT CERTIFIED / FAIL gate with a results table, and asks at launch for the level (offline, fast, full; fast and full fan out concurrent subagents). Use for "check citations", "citation audit", "integrity check", "is this safe to submit", "find fabricated or wrong references". Does not edit the manuscript. For placeholders, typos, cross-references, layout, and number consistency, use paper-hygiene; for argument and presentation, use paper-presentation-review.
---

# Paper Integrity

Find the defects that can look like academic dishonesty or damage the
authors' reputation before reviewers find them. The current scope is
citations. The deliverable is a results table and a report with a gate. This
skill never edits the manuscript or the bibliography unless the user asks for
fixes explicitly.

**The gate rule.** No open S0, and every S0 class checked. Read
[references/severity.md](references/severity.md) for the tiers, the
check-to-tier map, confidence, statuses, and the gate. Read
[references/citation-rules.md](references/citation-rules.md) before judging
any citation.

## 1. Launch: ask for the level

Always ask before running anything, unless the launch request already names a
level. In Claude Code, call `AskUserQuestion` with these options in this
order. Elsewhere, ask the same question in plain text and wait for the answer.

- **Question:** "Which citation check level should I run?" (header: `Level`)
- **Fast:** "Scripts check every reference against Crossref, OpenAlex, and
  arXiv; parallel agents confirm or clear what the scripts can only suspect.
  A few minutes. Does not check whether sources support our sentences."
- **Full:** "Fast, plus parallel agents read every cited source and check each
  citation's sentence, look for uncited borrowed work, and check for copied
  text; fresh agents then try to disprove every finding. Tens of minutes and
  many tokens. The only level that can PASS the gate."
- **Offline:** "Build logs and the bibliography only. Seconds, no network, no
  agents."

For **full**, ask in the same `AskUserQuestion` call for the scope: the whole
paper, or named sections or citation keys.

| Level | Script stages | Agent stages (concurrent) | Best gate |
| --- | --- | --- | --- |
| offline | 1 mechanical, 3 ledger | none | NOT CERTIFIED |
| fast | + 2 identity | 2b triage | NOT CERTIFIED |
| full | + source fetch, 6 overlap | 2b triage, 4 claim support, 5 omission, then 7 refute | PASS |

## 2. Setup

Resolve these from project instructions (a project skill or `AGENTS.md`), or
ask the user:

- `PAPER_DIR`: the manuscript root containing the main `.tex` file.
- `BUILD_DIR`: where the latest build left `main.aux`, `.log`, `.blg`, and
  `.pdf`. Rebuild first if the sources are newer; `mechanical.py` warns when
  the build is stale.
- `OUT`: a new run directory, `_docs/scratch/integrity/<YYYYMMDD_HHMM>` in the
  manuscript repository, never committed (the shared
  [`_docs/` layout](../repo-memory/references/docs-layout.md)).
- `CACHE`: an optional shared HTTP cache file, so reruns do not repeat lookups.
- `LOCAL_PDFS`: an optional directory of author-supplied `<key>.pdf` files for
  paywalled sources.
- `PREVIOUS`: the last run's `OUT`, if any, so earlier decisions carry forward.

**Data handling.** Scripts and agents send only public reference metadata
(titles, authors, DOIs, URLs) to external services: Crossref, OpenAlex,
arXiv, cited sites, the Wayback Machine, and web search. Manuscript text never
goes to an external service. Agents read it only inside the session.

## 3. Run

Scripts are stdlib Python 3 in `scripts/` and need `pdftotext` for PDFs.
`SKILL_DIR` is this skill's directory. `S=$SKILL_DIR/scripts`.

```bash
python3 $S/run.py --level <offline|fast|full> --paper-dir $PAPER_DIR \
  --build-dir $BUILD_DIR --out $OUT [--cache $CACHE] [--local-pdfs $LOCAL_PDFS] \
  [--keys k1,k2] [--previous $PREVIOUS]
```

**offline** ends here; go to section 4. **fast** and **full** stop after the
script stages so you can run the agents below.

### Agent stages

Briefs are in [references/agent-briefs.md](references/agent-briefs.md).
`plan_agents.py <stage> --out $OUT` prints balanced batches. Launch **every
agent of a wave in one message** so they run concurrently, and give each agent
exactly one batch.

| Wave | Levels | Stage | Batches | Agent effort |
| --- | --- | --- | --- | --- |
| A | fast, full | 2b triage | `plan_agents.py triage` (≤4) | medium (`worker-medium`) |
| A | full | 4 claim support | `plan_agents.py claims` (≤8) | high (`worker-high`) |
| A | full | 5 omission | `plan_agents.py omission` (≤4) | medium (`worker-medium`) |
| B | full | 7 refute | `plan_agents.py refute` (≤4), after wave A and `run.py --finish` | high, fresh agents |

Steps:

1. Run the wave-A planners and launch all wave-A agents together. Skip a stage
   whose plan is empty.
2. When they finish, run `python3 $S/run.py --finish --paper-dir $PAPER_DIR
   --out $OUT [--previous $PREVIOUS]`.
3. **full only:** run `plan_agents.py refute`, launch wave B, then run
   `run.py --finish` again. Refute skips findings the triage agents already
   decided.
4. **full only:** spot-check two `supported` verdicts and every upheld S0 against
   its quote yourself.

## 4. Show the results

Every run ends with `summary.md`, which `report.py` also prints. Show it to the
user as it is, in this order:

1. **Gate line**: FAIL, NOT CERTIFIED, or PASS, with the reason.
2. **Count table**: open and closed findings per tier.
3. **Open S0 and S1 table**: one row each, with tier, confidence, citation key,
   location, problem, and action.
4. **Open S2 table**: grouped by category, with counts and keys.
5. **Needs you**: PDFs to supply and references to confirm.
6. **Coverage line**: what ran and where the full report is.

After the table, add at most three sentences: what triage or refute changed,
anything you doubt in the table, and the next step. For example: fix the S0
rows, supply the listed PDFs, or run full before submission. Explain that
decisions go in `$OUT/decisions.json` as `{"<id>": {"status":
"cleared|fixed|dismissed", "note": "..."}}`, and that the next run picks them
up with `--previous $OUT`. Do not restate rows the table already shows.

## Toolbox

Other skills may call these directly; `run.py --level offline` is the cheap citation sanity check.

| Script | Stage | Does | Writes in `OUT` |
| --- | --- | --- | --- |
| `run.py` | all | Runs the script stages of a level; `--finish` closes a run after agents | `run.json` |
| `ledger.py` | 3 | Expands `\input`, records every citation use with sentence, section, `file:line`, co-cited keys, and a stable `use_id`; records all sentences | `ledger.jsonl`, `ledger.md`, `sentences.jsonl` |
| `mechanical.py` | 1 | Undefined citations, missing entries, duplicate keys and works, missing fields, BibTeX warnings, `[?]` in the PDF, stale build | `findings-mechanical.json`, `coverage-mechanical.json` |
| `identity.py` | 2 | Crossref, OpenAlex, and arXiv lookup per cited key: identifier mismatch, not located, retraction, author, year, venue, preprint with a published version, dead links with archive hints | `identity.json`, `findings-identity.json` |
| `fetch_sources.py` | 4 prep | Full text from local PDFs, arXiv, open-access PDFs, or web pages; abstract as a fallback | `sources/<key>.txt`, `sources/index.json` |
| `overlap.py` | 6 | 12+ word verbatim runs between our sentences and any fetched source | `findings-overlap.json` |
| `plan_agents.py` | 2b, 4, 5, 7 | Balanced agent batches: suspected references, co-cited key groups, section groups, findings to refute | stdout JSON |
| `report.py` | 8 | Merges findings, applies triage, refute, and author decisions, carries statuses, evaluates the gate | `report.md`, `report.json`, `summary.md` |

Script order matters: `ledger` before `mechanical`, `mechanical` before
`identity`, `identity` before `fetch_sources`, and `fetch_sources` before
`overlap`.

## Limits

- `identity.py` cannot query DBLP (it blocks scripted clients) or Semantic
  Scholar (it rate-limits without a key). Triage agents cover the gap with web
  search.
- `overlap.py` covers only fetched sources. It does not replace a plagiarism
  service such as iThenticate.
- Claim support depends on source access. `no-access` uses stay open as S1
  until a PDF is supplied.
- Venue matching accepts an acronym that spells word prefixes of the record
  venue's name, but not one built otherwise (for example from a sponsoring
  group's name); triage agents clear those `venue-mismatch` findings.
- The sentence splitter is approximate. Agents must open the `.tex` location
  when the clause in the ledger is unclear.
