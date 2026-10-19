# Citation verification rules

These rules govern every stage and every agent. They apply to citations in
body text, captions, tables, footnotes, and appendices within the scope.

## Identity and existence

- Check identity once per cited work and support at each use. A valid entry
  does not make an attribution valid.
- Compare title, authors, year, venue, and version against an authoritative
  record: the publisher, proceedings, arXiv, Crossref, or OpenAlex.
- A DOI or arXiv id that resolves to another work is a verified mismatch.
- For a work you cannot locate, search title variants and author plus title
  combinations in at least two indexes. A broken link, a failed search, or
  absence from one index does not prove the work does not exist. Report
  `not-located` as suspected, list the searches, and never use the word
  "fabricated" without affirmative evidence.
- Account for initials, diacritics, subtitles dropped by an index, and
  legitimate differences between preprint and published versions.
- Flag a preprint when a published version exists, unless the claim depends on
  content only in the preprint.

## Claim support

- Read the cited passage, table, or figure in context. A title or a search
  snippet never establishes support.
- An abstract supports only what the abstract states explicitly. Anything
  stronger needs the relevant body text.
- Check the exact attributed clause: system and version, workload, setting,
  comparison, number, and qualifiers such as "up to" or "on average".
- Verdicts:
  - `supported`: the source states it.
  - `partial`: the source states part of it, or a narrower version.
  - `contradicted`: the source states the opposite or a different value.
  - `unrelated`: the source does not discuss it.
  - `no-access`: the needed text could not be read.
- Verify fidelity to the source, not whether the cited research is correct.
- Every verdict except `no-access` must carry a short verbatim quote and a
  locator (section, page, table, or figure). A verdict without a quote does not
  count.

## Citation role and grouped citations

- Decide what each citation does: `evidence` (backs a factual claim),
  `attribution` (credits an idea, system, or result), `background`, `example`,
  `contrast`, or `artifact` (a tool, dataset, or baseline that we use).
- A background citation need not prove a new claim of ours. An evidence or
  attribution citation must support its clause.
- For a group such as `[a,b,c]`, decide how the sources jointly support the
  sentence. Do not assume each source supports every clause, and flag clauses
  that no source in the group supports. When the sentence maps sources to
  clauses in order ("A and B use X, whereas C and D use Y"), check each source
  against its own clause.
- Flag a citation attached to the wrong clause, and a single example presented
  as general evidence.

## Prose attribution

- Check named authors, systems, and papers in the prose ("X et al. show",
  "System Y uses Z") against the cited work.
- Check that our description of prior work matches that work's own claims. An
  unfair or outdated description of a competitor is S1 even when the citation
  is correct.

## Omissions

- Anything the paper uses or builds on needs a citation at its first
  substantive use: systems, datasets, traces, baselines, algorithms, data
  structures that are not textbook material, metrics defined by others,
  figures or tables adapted from others, and quoted definitions.
- Textbook concepts need no citation (hash table, B-tree, LRU), and neither do
  our own contributions.
- At a double-blind venue, self-citation must read as third-party work ("Smith
  et al. [3] show", not "our prior work [3]").

## Metadata and formatting

- Check unresolved keys, duplicate keys, duplicate works, malformed entries,
  missing required fields, broken escaping, and lost capitalization (for
  example `{LSM}`), against the document's own citation style.
- Do not impose another style, require DOIs for works that have none, or flag
  author-list truncation that the style permits.

## Corrections

- Suggest a corrected attribution, narrower wording, or a replacement source
  only when it is verified. Otherwise write "author clarification needed".
- Never invent a substitute citation.
- Never edit the manuscript or the bibliography unless the user asks for fixes
  explicitly. The report is the deliverable.
