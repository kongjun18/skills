# Source Manifest

This manifest lists preferred sources and the availability observed when it was last verified (2026-06-09). Dates below are observations, not current facts: re-check every official page before a new run, update this file and the source tables in `scripts/survey_top_systems.py` for new years. If a venue-year has not happened or proceedings are not public, skip it from analysis and record it in the coverage ledger.

## USENIX

USENIX technical-session pages usually expose titles, authors, abstracts, presentation pages, and PDF links in stable HTML.

- OSDI 2025: `https://www.usenix.org/conference/osdi25/technical-sessions`
- OSDI 2026: `https://www.usenix.org/conference/osdi26/technical-sessions`
- FAST 2025: `https://www.usenix.org/conference/fast25/technical-sessions`
- FAST 2026: `https://www.usenix.org/conference/fast26/technical-sessions`
- USENIX ATC 2025: `https://www.usenix.org/conference/atc25/technical-sessions`
- USENIX ATC 2026: not published as of 2026-06-09; `https://www.usenix.org/conference/atc26/technical-sessions` returned a 404 page.
- NSDI 2025: `https://www.usenix.org/conference/nsdi25/technical-sessions`
- NSDI 2026: `https://www.usenix.org/conference/nsdi26/technical-sessions` — re-check availability; spring '26 typically published by April.

Extraction hints:

- Scrape links containing `/conference/{conf}/presentation/`.
- On presentation pages, collect `a[href$=".pdf"]` or links whose text contains `Paper`.
- Abstracts often appear near headings/classes containing `Abstract`.

## SOSP

- SOSP 2025 site: `https://sigops.org/s/conferences/sosp/2025/`
- SOSP 2025 accepted papers: `https://sigops.org/s/conferences/sosp/2025/accepted.html`
- SOSP 2025 ACM DL proceedings: `https://dl.acm.org/doi/proceedings/10.1145/3731569`
- SOSP 2026 accepted page: `https://sigops.org/s/conferences/sosp/2026/accepted.html`

Availability:

- SOSP 2025 is published. The accepted page lists titles/authors; ACM DL article pages are needed for abstracts/PDFs. Try ACM DOI PDFs and record blockers explicitly.
- SOSP 2026 is not yet published as of 2026-06-09; accepted page was TBD.

ACM DOI patterns:

- Article: `https://dl.acm.org/doi/{article_doi}`
- PDF: `https://dl.acm.org/doi/pdf/{article_doi}`

## SIGMOD / PACMMOD

- SIGMOD 2025 accepted papers: `https://2025.sigmod.org/sigmod_papers.shtml`
- SIGMOD 2025 OpenTOCs:
  - `https://2025.sigmod.org/toc-3-1.html`
  - `https://2025.sigmod.org/toc-2-6.html`
  - `https://2025.sigmod.org/toc-3-3.html`
- SIGMOD 2026 accepted papers: `https://2026.sigmod.org/sigmod_papers.shtml`
- SIGMOD 2026 detailed program: `https://sigmodconf.hosting.acm.org/2026/sigmod_program_detailed.shtml`
- SIGMOD 2026 PACMMOD TOCs:
  - `https://dl.acm.org/toc/PACMMOD/2025/3/4`
  - `https://dl.acm.org/toc/PACMMOD/2025/3/6`
  - `https://dl.acm.org/toc/PACMMOD/2026/4/1`
  - `https://dl.acm.org/toc/PACMMOD/2026/4/3`

Availability:

- SIGMOD 2025 and 2026 paper lists are available as of 2026-06-09.
- 2025 local OpenTOC pages include abstracts and DOI links.
- 2026 may require ACM DL article pages for abstracts. Try ACM DOI PDFs and record blockers explicitly.

## VLDB / PVLDB

Use PVLDB volume pages and the conference program.

- PVLDB volumes landing: `https://www.vldb.org/pvldb/`
- PVLDB Volume 18: normally corresponds to the 2025 conference cycle.
- PVLDB Volume 19: normally corresponds to the 2026 conference cycle.
- VLDB 2025 site: `https://www.vldb.org/2025/`
- VLDB 2026 site: `https://www.vldb.org/2026/`

Availability can be sensitive to site downtime. If `vldb.org` times out, retry later. Treat the timeout as an operational blocker, not evidence that VLDB is missing.

PVLDB extraction hints:

- Crawl volume pages for issue links and paper links.
- Prefer exact PDF links from the page over synthesized filenames.
- When only page ranges are available, use DOI/OpenAlex/Semantic Scholar metadata only as a fallback and record the fallback.

## SIGCOMM

- SIGCOMM 2025 site: `https://conferences.sigcomm.org/sigcomm/2025/`
- SIGCOMM 2025 program details: `https://conferences.sigcomm.org/sigcomm/2025/program/program-details/`
- SIGCOMM 2025 papers: `https://conferences.sigcomm.org/sigcomm/2025/program/papers-info/`
- SIGCOMM 2025 ACM DL proceedings DOI: `10.1145/3718958`
- SIGCOMM 2026 site: `https://conferences.sigcomm.org/sigcomm/2026/`
- SIGCOMM 2026 CFP: `https://conferences.sigcomm.org/sigcomm/2026/cfp/`

Availability:

- SIGCOMM 2025 is published and the papers page embeds abstracts and DOI links.
- SIGCOMM 2026 is not yet published as of 2026-06-09; camera-ready deadline is after this date.

## ASPLOS

ACM venue; proceedings live on ACM DL. ASPLOS '25 program: spring 2025; ASPLOS '26 program: spring 2026.

- ASPLOS 2025 site: `https://www.asplos-conference.org/asplos2025/`
- ASPLOS 2025 program: `https://www.asplos-conference.org/asplos2025/main-program/`
- ASPLOS 2026 site: `https://www.asplos-conference.org/asplos2026/`
- ACM DL proceedings root: `https://dl.acm.org/conference/asplos`

Availability:

- ASPLOS papers usually appear on ACM DL behind DOI URLs (`https://dl.acm.org/doi/{doi}`). Prefer authors' personal/institutional pages or arXiv preprints when ACM DL gates the PDF.

## EuroSys

ACM venue; proceedings on ACM DL.

- EuroSys 2025 site: `https://2025.eurosys.org/`
- EuroSys 2025 accepted papers: `https://2025.eurosys.org/program.html`
- EuroSys 2026 site: `https://2026.eurosys.org/`
- ACM DL proceedings root: `https://dl.acm.org/conference/eurosys`

Availability:

- EuroSys 2025 is published as of 2026-06-09; 2026 is typically published in spring '26 (re-check).
- ACM DL DOI patterns match SOSP and ASPLOS.

## General Fallbacks

- DOI metadata: Crossref, ACM DL article pages, OpenAlex, Semantic Scholar.
- PDF search order: official conference PDF, ACM PDF, author website, institutional repository.
- Record fallback source in metadata and never overwrite official DOI/source fields.

## Output Rule

Do not create per-paper Markdown notes. The catalog is split per `(venue, year)` under `thinking/catalog/`, with a 5-line digest per paper — *not* a pasted abstract. Curated analysis lives in aggregate Markdown outputs and `sparking/*.md`. See `final_deliverables.md` for schemas and the validator in `scripts/validate_outputs.py` for the enforced gates.

## Coverage Ledger Required

Before writing any cross-year analysis, populate `thinking/coverage_ledger.md` per `final_deliverables.md`. The trend file (`topic_trend.md`) is gated on it: a venue/year with `completeness < 0.9` cannot contribute to a `direction:` label.
