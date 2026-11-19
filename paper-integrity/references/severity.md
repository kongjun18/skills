# Severity, confidence, and the gate

Every finding has three independent fields.

- **Severity** says how much damage the defect can do.
- **Confidence** says how sure we are that the defect is real.
- **Status** says what the author decided.

Never lower a severity because confidence is low. A suspected S0 stays S0
until the triage or refute stage, or the author, resolves it.

## Severity

| Tier | Meaning | Submit with it open? |
| --- | --- | --- |
| **S0 Blocker** | A reader could reasonably read it as dishonesty or fabrication. | No. |
| **S1 Major** | A reviewer who notices it trusts the paper less. | Allowed, but fix it if you can. |
| **S2 Minor** | Formatting or metadata polish only. | Yes. |

## Check-to-tier map

The tier for each category. Scripts and agents use this table; when a case is
not listed, choose the tier by the meaning above and say why in the evidence.

| Category | Stage | Tier | Notes |
| --- | --- | --- | --- |
| `identifier-mismatch`: DOI or arXiv id resolves to a different work | 2 | S0 | Verified when the record title clearly differs. |
| `identifier-unresolved`: DOI or arXiv id resolves nowhere | 2 | S0 | Suspected; usually a typo, but it may also be an invented identifier. |
| `not-located`: a scholarly entry with no matching record anywhere | 2 | S0 | Suspected. Never call it fabricated without affirmative evidence. |
| `not-located`: a web, manual, or misc entry with no locator | 2 | S1 | |
| `retracted` | 2 | S0 | Allowed only when the text cites it explicitly as retracted. |
| `contradicted`: the source says the opposite, or a different number | 4 | S0 | |
| `misattributed`: wrong author, system, or paper credited in the prose | 4 | S0 | For example "X et al. proposed Y" when Z proposed Y. |
| `unrelated`: the source does not discuss the claim | 4 | S0 when the citation's role is evidence or attribution; S1 when it is background | |
| `partial` or `overgeneralized` support | 4 | S1 | One source behind "all systems", missing qualifiers, or a different setting. |
| `unfair-characterization`: prior work described as weaker than its own text shows | 4 | S1 | |
| `no-access`: support could not be checked | 4 | S1 | Confidence is `no-access`; supply the PDF to resolve it. |
| `uncited-borrowed-work`: a system, dataset, baseline, method, figure, or definition used without a citation | 5 | S0 | Suspected until the refute stage confirms it. |
| `anonymity-breach`: self-citation in the first person at a double-blind venue | 5 | S0 | Check only when the venue is double-blind. |
| `verbatim-overlap` of 12 or more consecutive words without quotation | 6 | S0 | Suspected; dismiss standard names and definitions. |
| `preprint-has-published-version` | 2 | S1 | Suspected; the claim may depend on preprint-only content. |
| `author-mismatch` in metadata | 2 | S1 | |
| `year-mismatch` | 2 | S1 when the gap is more than one year; S2 when it is one year or the record is preprint-only | |
| `venue-mismatch` | 2 | S1 | Suspected; venue names vary. |
| `dead-link` | 2 | S1 | Suspected; some sites block scripts. |
| `undefined-citation`, `missing-entry`, `unresolved-marker`, `duplicate-key` | 1 | S1 | Visible in the PDF, or it may render the wrong work. |
| `missing-field` (title or author) | 1 | S1 | S2 for a `misc`, `online`, or `manual` entry that has a URL or DOI and lacks only the author. |
| `missing-field` (year), `no-locator`, `bibtex-warning`, `duplicate-work`, `title-differs` | 1–2 | S2 | |

## Confidence

- `verified`: an authoritative record or a quoted source passage shows the
  defect.
- `suspected`: a heuristic or a failed search points to it, but there is no
  direct evidence yet.
- `no-access`: the needed source could not be read.

The triage stage (reference findings) and the refute stage (all other S0 and
S1 findings) may upgrade `suspected` to `verified`, downgrade the severity
with a reason, or refute the finding.

## Status

- `open`: the default.
- `fixed`: the author changed the paper. The next run must not detect it again;
  if it does, the finding reopens.
- `cleared`: the author confirmed that there is no defect, for example by
  finding the publisher page for a `not-located` entry.
- `dismissed`: the finding is not a defect, for example a standard term in
  `verbatim-overlap`.
- `refuted`: the triage or refute stage disproved it.

Authors record decisions in `decisions.json` with a note. A cleared S0 must
name the evidence in its note.

## Gate

- **FAIL**: at least one S0 is `open`, whatever its confidence.
- **NOT CERTIFIED**: no open S0, but claim support (4), omission (5), or
  overlap (6) did not run. The offline and fast levels always end here, since they cannot
  check those S0 classes.
- **PASS**: no open S0, and stages 4–6 ran over the whole scope.

PASS is a statement about the checked scope and the fetched sources only. It is
not proof that the paper has no integrity problem.
