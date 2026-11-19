# Knowledge Lifecycle and Conflicts

Read when knowledge has become stale, when sources or notes disagree, when a specification and the code disagree, or when parallel edits to one topic need reconciling. Every outcome here is recorded by editing the note that already owns the topic ([SKILL.md](../SKILL.md#one-current-view)), never by adding a note that comments on it.

## States

A note, or a single claim in it, is one of:

- `active`: usable now, within its stated scope;
- `disputed`: credible claims or evidence conflict, and resolution is pending;
- `superseded`: replaced by newer knowledge or a newer decision;
- `expired`: was valid, but only for an older revision, version, or context;
- `invalid`: disproved, mistaken, or unsupported from the start.

## Handling Stale Knowledge

1. Classify it with one of the states above.
2. Remove the inactive claim from `Current View`.
3. Add a `Semantic History` line with why it changed and the evidence.
4. Write the replacement claim into the same note. Link a separate note only when the replacement is a different topic.
5. Update active files that depended on the claim: indexes, `status.md`, specifications, other notes.
6. Archive only when the material is no longer needed for active navigation.

Do not silently delete important context. Do not keep contradictory old and new claims together in `Current View` unless they are explicitly marked `disputed`.

## Conflict Resolution

Do not resolve semantic conflicts by last write wins.

| Situation | Outcome |
|---|---|
| Same claim, same scope, written twice | Consolidate into one |
| Overlapping claims | Merge into one clearer `Current View` |
| Different scopes or versions | State each scope explicitly |
| Old claim was wrong | Mark it `invalid` |
| Old claim was once true | Mark it `expired` |
| New knowledge or a new decision replaced it | Mark it `superseded` |
| Evidence is inconclusive | Mark it `disputed`, with both sides' evidence |
| Specification differs from implementation | Record a conformance conflict ([SKILL.md](../SKILL.md#authority)) |

When resolution needs user or maintainer authority, keep the conflict explicit in the note and list it in the closeout summary under conflicts and open questions. Do not invent a decision.
