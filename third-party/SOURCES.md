# Third-Party Skill Sources

`third-party/` holds gitignored clones of upstream skill repositories. This file is the tracked record of what each clone is, so an install can be reproduced on another machine.

| Directory | Upstream | Pinned commit | Commit date | Installed skill |
| --- | --- | --- | --- | --- |
| `andrej-karpathy-skills` | https://github.com/multica-ai/andrej-karpathy-skills | `2c606141936f1eeef17fa3043a72095b4765b9c2` | 2026-04-20 | none (folded into `good-agent`) |

Reproduce:

```bash
git clone https://github.com/multica-ai/andrej-karpathy-skills third-party/andrej-karpathy-skills
git -C third-party/andrej-karpathy-skills checkout 2c606141936f1eeef17fa3043a72095b4765b9c2
```

When updating a clone, update its pinned commit and date here in the same change.
