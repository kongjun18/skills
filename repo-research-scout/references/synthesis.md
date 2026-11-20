# T3 Synthesis: Landscape, Clusters, Generality, Cards

Read this when running Step 6 of the workflow. T3 reads only derived files (`work/metrics/`, `work/digests/`) and, for a specific claim, single items from the database; it never reads raw batches in bulk.

## 1. Component landscape

From `component_quarter.csv`, place each component on two axes over the window:

- **Demand:** issues opened per quarter and its trend; distinct authors (breadth of users).
- **Resolution:** `closed_within_90d_frac`, median and p90 days to close, open backlog.

| Label | Pattern | Alternative explanations to rule out before using the label |
|---|---|---|
| active-healthy | high demand, high resolution | — |
| gap | high or rising demand, low or falling resolution | triage backlog after a release; a new feature still settling; issues filed by a bot |
| mature-quiet | low demand, high resolution, low churn | the component is little used; issues routed to another repository |
| stale | low demand, large old open backlog | maintainers never close; feature deprecated |
| churning | many PRs, reverts, or config additions relative to issues | refactor in progress |

Also read `direction_root_causes.csv`: a component whose analyzed items are mostly `design-limit` or `tradeoff` is a stronger research signal than one with many `implementation-bug` items. State counts with their denominator and say that analyzed items are a selected sample, while the census counts are complete for items created inside the window.

## 2. Pain clusters

Read `work/digests/digest-<direction>.md`. Group items by **mechanism**, not keyword: two items belong together when the same cause produces them (for example "manifest rewrite cost grows with fragment count"). Keep a cluster only if it has at least two independent reporters, or one maintainer statement of a design limit or tradeoff. For each cluster record: items, components, root-cause mix, resolution mix, first and last dates, and whether it recurred after a fix.

## 3. Generality test

For each cluster whose root cause is `design-limit`, `tradeoff`, or `missing-abstraction`:

1. Name the mechanism in system-neutral terms.
2. Pick peers that implement the same function differently (listed in the study's `peers`; sync each with `scout.py sync <repo>` if absent).
3. Search them without model cost: `scout.py select --study S --repo <peer> --query "kw1,kw2" --name cluster-<id> --limit 30`, then run T1 and T2 on the hits like any other batch.
4. Verdict:
   - `implementation-specific`: peers with a different design do not show it, or show it fixed by a known technique (name it).
   - `system-class`: peers of the same class show the same mechanism.
   - `general`: systems of different classes show it.
   - `unclear`: peers not searched or searches empty for reasons other than absence (vocabulary, tracker elsewhere).

Absence of issues in a peer is weak evidence; prefer a peer maintainer statement or a design document.

## 4. Prior art

For each cluster that survives as `system-class` or `general`, search for the closest published work and design documents (papers, RFCs, blog posts by system authors). Record up to three closest works with one sentence each on what they do and do not cover. If you could not search, write "prior art unchecked"; never imply novelty without a search.

## 5. Hypothesis cards

Write one card per surviving cluster to `cards/<slug>.md` in the study directory, using exactly these sections:

```markdown
# <one-line claim>

## Research question
<question a paper could answer>

## Mismatch
<what the system assumes versus what the workload does, in two or three sentences>

## Evidence
- https://github.com/<owner>/<repo>/issues/<n> — "<verbatim quote>"
- (two or more lines; each quote verbatim from that item's body or comments)

## Generality
<verdict from step 3, peers searched, what they showed>

## Prior art
<closest works, or "prior art unchecked">

## Falsification
<observations that would show this is not a real or general problem>

## Cheapest experiment
<minimal reproduction or measurement, its inputs, and its expected cost; not run unless the user asks>

## Verdict
<promising | needs evidence | implementation-only | drop>, with confidence and the one fact that would change it
```
```

Then run `scout.py verify-cards --study S cards/*.md` and fix every failure. It checks the sections, that each evidence quote is verbatim in an item stored in a registered database, and that no placeholder remains.

## 6. Hand to the report

Write the exploration report with the `exploration-report` skill. Map each study direction to a scorecard row and each card to a finding or open question. Cite the snapshot (`scout.py snapshot`) as raw data, and put every number the reader needs into the report as a table rather than pointing at the snapshot; tag issue-derived claims `[cited: <url>]` and census counts `[measured]` with the snapshot path. Issue reports are third-party evidence, not reproduction.
