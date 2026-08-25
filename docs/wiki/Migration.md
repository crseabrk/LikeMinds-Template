# Migrating to LMTR

LMTR 0.1 begins in shadow mode: Markdown remains the human-readable authority while LMTR decisions are compared against existing behavior.

1. Inventory normative Markdown rules.
2. Validate the ordered LMTR ruleset.
3. Run INITIALIZE, JOIN, RESUME, RECOVER, NOBODY, SOLO, TEAM, and stale-session fixtures.
4. Compare normalized decisions and resolve every difference.
5. Test a clean macOS bootstrap and disconnected Windows onboarding.
6. Preserve a rollback to Markdown-only operation.

Never overwrite operational CHAT, STATUS, DECISIONS, SIGNALS, roles, or cursors during migration.

## Updating an installed copy

Repositories created from a GitHub template do not receive upstream changes automatically. Use the managed update procedure in root [`MIGRATIONS.md`](../../MIGRATIONS.md). It provides a reviewable plan, detects local modifications, protects operational paths, creates backups, validates after application, and records the exact installed upstream revision.

An installation with only connector access uses the documented connector workflow and requires explicit human approval. Its result remains statically inspected until the installed repository is validated from an executable checkout.
