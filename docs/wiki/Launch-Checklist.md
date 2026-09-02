# Launch Checklist

- LMTR parser and structural validator pass.
- INITIALIZE, JOIN, RESUME, and RECOVER behavior is documented.
- NOBODY, SOLO, and TEAM are derived from crash-safe leases rather than silence.
- UNKNOWN presence fails into RECOVER; stale sessions never retire durable roles.
- A 100-record identity snapshot validates, and duplicate IDs, filenames, display names, or aliases fail closed.
- Every ACTIVE route names one to three ACTIVE admission agent IDs; identity introduction does not fan out peer to peer.
- Wiki quick start works from one repository link.
- Public repository contains no private operational history or secrets.
- macOS validation passes.
- Disconnected Windows review passes.
- Migration preserves operational records and cursors and never mixes legacy and sharded quorum rules.
- License choice is explicit.
- Release and publication receive current human approval.
- Rollback to Markdown-only behavior is documented.
