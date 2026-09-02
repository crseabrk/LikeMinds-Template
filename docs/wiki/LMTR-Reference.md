# LMTR 0.1 Reference

LMTR is a small declarative coordination-policy language. Its Forth influence is a compact line-oriented vocabulary, not a hidden operand stack.

## Syntax

- One statement per line.
- Whitespace separates words.
- `#` starts a comment.
- Named blocks end with `end`.
- The manifest fixes module order.
- Unknown tokens, missing modules, unsafe paths, and unclosed blocks fail closed.

Top-level forms are `ruleset`, `authority`, `policy`, `procedure`, `default`, `unknown`, and `ambiguous`. LMTR has no variables, recursion, macros, arbitrary includes, shell, HTTP, credential access, or product mutation.

## Protected baseline

LMTR 0.1 requires default deny, unknown deny, ambiguous block, human approval for product writes, latest-SHA signal claims, own-cursor-only updates, and history-deletion denial.

## Commands

```sh
python3 tools/lmtr.py validate
python3 tools/lmtr.py plan
python3 tools/lmtr.py presence
python3 tools/lmtr.py directory
```

`plan` emits machine-readable startup, presence, and identity-directory state. `presence` reports PRESENT, SUSPECT, STALE, or UNKNOWN per session and derives NOBODY, SOLO, TEAM, or RECOVER. `directory` validates every sharded identity file, detects ID and display-name collisions, and emits a compact roster. These commands do not perform writes.
