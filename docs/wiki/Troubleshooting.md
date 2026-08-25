# Troubleshooting

## The agent can read GitHub but cannot run LMTR

A GitHub connector may expose individual repository files without creating a local checkout. In that environment, the agent cannot truthfully claim to have run the filesystem-based validator or conformance tests.

The agent should report connector-only access, state whether any command was attempted, and label any per-file or in-memory review as **static inspection only**. It must remain read-only until it obtains an executable checkout or the human explicitly approves narrowly scoped connector-only coordination writes. Connector read/write access does not imply terminal execution, Python availability, or a local repository tree.

- **LMTR-E001/E002:** manifest missing, invalid, or unsupported.
- **LMTR-E003/E004:** module list is empty, duplicated, or out of visible order.
- **LMTR-E005/E006:** unsafe or missing module path.
- **LMTR-E007:** unknown token; LMTR fails closed.
- **LMTR-E008/E011:** unmatched or unclosed block.
- **LMTR-E009:** invalid block arity.
- **LMTR-E010:** statement outside a valid top-level block.
- **LMTR-E012:** protected safety rule is missing.

If `plan` returns RECOVER, inspect installation metadata, root routing, and `system/AGENTS.md`. Do not force INITIALIZE or reuse another role's cursor.
