# Migrations

Installations are independent copies and do not silently track this template. LikeMinds uses an explicit managed-file updater so humans can review framework changes without overwriting operational records.

## Managed update workflow

The upstream manifest is `updates/managed-files.json`. Installed state is recorded in `.likeminds/update-state.json`. Only manifest-listed framework files are updated; `installation.yml`, root routing, `system/`, and `projects/` are protected.

For a local installation and a separately pulled template checkout:

```sh
python3 tools/update.py adopt --source /path/to/LikeMinds-Template --source-revision COMMIT_SHA
python3 tools/update.py plan --source /path/to/LikeMinds-Template --source-revision COMMIT_SHA
python3 tools/update.py apply --source /path/to/LikeMinds-Template --source-revision COMMIT_SHA
```

`adopt` is a one-time baseline for an existing unmanaged installation. Review and commit its state before applying an update. `plan` reports ADD, UPDATE, UNCHANGED, and blocking conflicts. `apply` refuses locally modified managed files, backs up replaced files, updates atomically, runs LMTR validation and conformance tests, and records the installed upstream revision.

If preserved operational history already contains duplicate message IDs, record only the known path and IDs in `.likeminds/validation-baseline.json` using format `likeminds-validation-baseline-1`. This installation-specific exception preserves history while allowing every unlisted future duplicate to fail validation. Never add an ID merely to make a new validation failure disappear; investigate it first.

Never use the template checkout itself as the destination. Pull or fetch the source separately and pin a reviewed commit SHA.

## Connector-only update workflow

An authorized connector-only agent follows the same manifest and state semantics:

1. pin and report the exact public template commit;
2. read `updates/managed-files.json` at that commit;
3. compare every destination file against `.likeminds/update-state.json`;
4. block on an untracked or locally modified managed file;
5. create one latest-SHA commit containing only eligible managed files and the refreshed update state;
6. leave protected operational paths untouched;
7. label validation as static inspection unless an executable checkout runs the supplied commands.

Connector-only application requires explicit human approval because executable validation is unavailable. A connector agent must never treat a successful file copy as runtime validation.

Future versions must document:

- supported source and destination versions;
- framework files changed;
- operational records affected;
- backup and rollback steps;
- extension compatibility;
- required human approvals.

Updaters should propose reviewable pull requests and must never overwrite CHAT history, completed signals, installation policy, or private operational data without explicit human approval.
