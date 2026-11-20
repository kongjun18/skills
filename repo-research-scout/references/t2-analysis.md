# T2 Analysis Brief

You analyze full GitHub issue or PR threads for a systems research study. Read one batch file and write one JSON object per item, one per line (JSONL), to the results path you were given. Judge only from the item text; do not browse.

The batch file has `context.directions`, `context.components`, and `items` (key, input_hash, url, text). The text holds metadata, linked PRs, changed files, the body, and comments; maintainer comments come first and are labeled `maintainer`.

## Fields

| Field | Type | Meaning |
|---|---|---|
| `key`, `input_hash` | string | copied from the item |
| `directions` | list of ids | directions whose question this item bears on (may be `[]`) |
| `component` | string | one of `context.components` |
| `symptom` | string | what the user observed, one sentence, concrete (operation, scale, effect) |
| `root_cause` | string | see the table below |
| `resolution` | string | `fixed`, `workaround`, `wontfix`, `open`, `duplicate`, or `unclear` |
| `workload` | string | the workload that exposed it, in a few words (for example "streaming ingest of small batches"); `unclear` if not stated |
| `maintainer_position` | string | what maintainers said about cause or fix, one sentence; `""` if they did not comment |
| `generality` | string | see the table below |
| `generality_reason` | string | one sentence: the mechanism that makes it specific or general |
| `quotes` | list | 1–3 objects `{"text": ..., "who": "reporter" | "maintainer" | "other"}`; each `text` is copied verbatim from the item text, at least 20 characters |
| `summary` | string | at most 400 characters: symptom, cause, and resolution |

`root_cause`:

| Value | Use when |
|---|---|
| `implementation-bug` | a defect fixable without changing the design |
| `design-limit` | the current design cannot do it without a format, protocol, or architecture change |
| `tradeoff` | two goals conflict (for example write amplification versus read latency) and any setting hurts one; signals: knobs added, reverted fixes, "it depends on workload" |
| `missing-abstraction` | users build the same thing outside the system because no mechanism exists |
| `usage-error` | the system worked as designed and the user misused it |
| `unclear` | the thread does not establish a cause |

`generality`:

| Value | Use when |
|---|---|
| `implementation-specific` | caused by this codebase's choices; another implementation of the same idea would not have it |
| `system-class` | inherent to this class of system (for example any log-structured table format on object storage) |
| `general` | a tradeoff that appears across system classes |
| `unclear` | not enough information |

## Rules

- Quotes are verbatim: copy characters exactly; do not fix, trim inside, or join passages. Prefer maintainer quotes that state a cause, constraint, or decision. `ingest` rejects any quote it cannot find in the item text.
- Separate what the thread shows from what you infer. `generality` is a hypothesis for the synthesis tier, not a conclusion; keep `generality_reason` to the mechanism.
- A closed state is not a fix: check whether a merged PR or a maintainer comment shows the fix.
- Output one line per item, every item, no prose before or after.
