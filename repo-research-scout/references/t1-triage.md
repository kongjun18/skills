# T1 Triage Brief

You triage GitHub issues and PRs for a research study. Read one batch file and write one JSON object per item, one per line (JSONL), to the results path you were given. Judge only from the item text; do not browse.

The batch file has `context.directions` (id, title, question), `context.components` (allowed component names), and `items` (key, input_hash, url, text). The text is the title, labels, and the start of the body.

For every item, output exactly these fields:

| Field | Type | Meaning |
|---|---|---|
| `key` | string | copied from the item |
| `input_hash` | string | copied from the item |
| `directions` | list of direction ids | directions whose question this item bears on; `[]` if none (keyword false positive) |
| `component` | string | one of `context.components`; `unknown` if the text does not say |
| `type` | string | `bug`, `performance`, `feature`, `design`, `question`, `docs`, `build`, or `other` |
| `escalate` | boolean | true if a full read could reveal a design limit, tradeoff, recurring problem, or maintainer reasoning relevant to a direction; false for typos, packaging, one-off usage help, and duplicates with nothing new |
| `reason` | string | at most 200 characters: why it bears on the directions, or why not |

Rules:

- Be strict on `directions`: matching a keyword is not relevance. The item must bear on the direction's question.
- Escalate sparingly; the next tier reads full threads at much higher cost. When unsure between two similar items, escalate the one with more discussion or maintainer involvement.
- Output one line per item, every item, no prose before or after.
