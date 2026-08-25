# Troubleshooting

## The agent can read GitHub but cannot run LMTR

A GitHub connector may expose individual repository files without creating a local checkout. In that environment, the agent cannot truthfully claim to have run the filesystem-based validator or conformance tests.

The agent should report connector-only access, state whether any command was attempted, and label any per-file or in-memory review as **static inspection only**. It must remain read-only until it obtains an executable checkout or the human explicitly approves narrowly scoped connector-only coordination writes. Connector read/write access does not imply terminal execution, Python availability, or a local repository tree.

For a fresh private template, the human may respond with an approval such as:

> I explicitly approve connector-only initialization of OWNER/REPOSITORY. Record the missing authenticated checkout and unexecuted validation as capability limitations. Verify every remote change and commit, and do not claim that local tests passed.

The agent then follows **Connector-only initialization** in root `BOOTSTRAP.md`. It records the installation as **initialized, validation deferred** and leaves an executable-checkout validation as a named follow-up. Approval for this fallback applies only to LikeMinds coordination records in the named repository; it grants no product or external authority.

- **LMTR-E001/E002:** manifest missing, invalid, or unsupported.
- **LMTR-E003/E004:** module list is empty, duplicated, or out of visible order.
- **LMTR-E005/E006:** unsafe or missing module path.
- **LMTR-E007:** unknown token; LMTR fails closed.
- **LMTR-E008/E011:** unmatched or unclosed block.
- **LMTR-E009:** invalid block arity.
- **LMTR-E010:** statement outside a valid top-level block.
- **LMTR-E012:** protected safety rule is missing.

If `plan` returns RECOVER, inspect installation metadata, root routing, and `system/AGENTS.md`. Do not force INITIALIZE or reuse another role's cursor.

## Update conflicts

- `CONFLICT-UNTRACKED` means an existing installation has not recorded a baseline for that managed file. Run `adopt` once and review the resulting state before applying.
- `CONFLICT-LOCAL-MODIFICATION` means the installed managed file changed after its recorded version. Preserve it, compare with upstream, and resolve deliberately; the updater will not overwrite it.
- A post-update validator failure automatically restores copied files from `.likeminds/backups/`. Inspect the exact command failure before retrying.
