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

## Migrating to sharded identity discovery

Managed updates deliberately protect root `ROUTING.md` and `system/`, so installing the framework files does not silently change an installation's admission model. A human must approve this operational migration.

1. Apply and validate the managed framework update first.
2. Create `system/identities/` without removing or rewriting `system/AGENTS.md`.
3. For every non-retired legacy role, create a unique immutable agent ID and one schema-valid identity file. Preserve the old role as its display name or previous alias and preserve membership state, capabilities, routes, and timestamps without inventing missing facts.
4. Add `identity_directory`, `require_sharded_identity_records`, and `require_route_admission_roles` from `installation.example.yml` to the protected `installation.yml` after human review.
5. Add an `Admission agent IDs` column to root `ROUTING.md`. Name one to three current ACTIVE identities for the system route and each ACTIVE project route.
6. Run `python3 tools/lmtr.py directory`, the full validation suite, and a dry-run join that targets only those admission roles.
7. Record one durable cutover decision and the exact commit. Keep legacy rows as history.

Until every step succeeds, continue the legacy all-participant acknowledgement procedure. Never mix legacy and sharded quorum rules within a join. Rollback means reverting the cutover decision and routing change while preserving every identity file and coordination message as history.

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
