# Migrating to LMTR

LMTR 0.1 begins in shadow mode: Markdown remains the human-readable authority while LMTR decisions are compared against existing behavior.

1. Inventory normative Markdown rules.
2. Validate the ordered LMTR ruleset.
3. Run INITIALIZE, JOIN, RESUME, RECOVER, NOBODY, SOLO, TEAM, and stale-session fixtures.
4. Compare normalized decisions and resolve every difference.
5. Test a clean macOS bootstrap and disconnected Windows onboarding.
6. Preserve a rollback to Markdown-only operation.

Never overwrite operational CHAT, STATUS, DECISIONS, SIGNALS, roles, or cursors during migration.
