# Troubleshooting

- **LMTR-E001/E002:** manifest missing, invalid, or unsupported.
- **LMTR-E003/E004:** module list is empty, duplicated, or out of visible order.
- **LMTR-E005/E006:** unsafe or missing module path.
- **LMTR-E007:** unknown token; LMTR fails closed.
- **LMTR-E008/E011:** unmatched or unclosed block.
- **LMTR-E009:** invalid block arity.
- **LMTR-E010:** statement outside a valid top-level block.
- **LMTR-E012:** protected safety rule is missing.

If `plan` returns RECOVER, inspect installation metadata, root routing, and `system/AGENTS.md`. Do not force INITIALIZE or reuse another role's cursor.
