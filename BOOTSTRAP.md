# LikeMinds Bootstrap

This is the single entry point for a human or AI agent.

## Human command

Give a GitHub-authorized agent this instruction:

> Go to OWNER/REPOSITORY and follow BOOTSTRAP.md completely.

Replace `OWNER/REPOSITORY` with the LikeMinds repository to initialize or join.

## Authority boundary

Following this file authorizes only the LikeMinds coordination reads and narrowly necessary coordination-record writes described below. It does not authorize product edits, branches, pull requests, merges, builds, releases, publication, deletion, purchases, access changes, or communication outside LikeMinds. Those require the current human request.

## Bootstrap procedure

1. Read this file completely.
2. Run `python3 tools/lmtr.py validate`, then `python3 tools/lmtr.py plan`. If Python 3 is unavailable or validation fails, remain read-only and report the exact prerequisite or LMTR error.
3. Read `AGENTS.md`, `PROTOCOL.md`, `JOINING.md`, `JOIN-CHECKLIST.md`, and `SECURITY.md` completely. These remain the human-readable safety and audit reference during LMTR 0.1 migration.
4. Follow exactly the state returned by the LMTR plan. Startup is `INITIALIZE`, `JOIN`, `RESUME`, or `RECOVER`; active collaboration is `NOBODY`, `SOLO`, or `TEAM`. Never force a different state.
5. Inspect the repository before writing:
   - If `installation.yml` exists with real repository metadata and operational records already exist, this is an **existing installation**.
   - If only `installation.example.yml` and empty records under `templates/` exist, this is a **fresh template**.
   - If the state is mixed or ambiguous, remain read-only and ask the human.
6. Never assume the repository is named LikeMinds.

LMTR defines startup behavior; Markdown remains the human-readable record. The planner has no write capability.

## Collaboration state and unclean exits

`system/PRESENCE.json` records per-session leases. Each TEAM session renews its own `last_seen` using latest-SHA updates. Effective presence is computed as:

- `TEAM`: two or more current or grace-period sessions; coordination polling runs.
- `SOLO`: exactly one current or grace-period session; that session stops coordination polling and works directly with the human.
- `NOBODY`: no current sessions; no polling runs. The last cleanly exiting agent records its own `exit_state` as `CLOSED`.

If a session closes without exiting, its lease moves from `PRESENT` to `SUSPECT`, then `STALE` after the configured grace window. STALE affects session presence only; it never retires or rewrites the durable role. Invalid or unparseable presence becomes `UNKNOWN` and selects RECOVER rather than guessing.

Run `python3 tools/lmtr.py presence` to inspect reconciliation. Silence alone never changes state. Re-entry renews or creates the current session lease, recomputes presence, and resumes TEAM polling only when at least two sessions are effective. No agent edits another live session or another agent's automation.

## Existing installation: join

1. Follow `JOINING.md` completely.
2. Read root routing, the complete system record, and every current ACTIVE project's complete record before announcing.
3. Recheck routing after orientation.
4. Propose a unique stable role and truthful capabilities. Never reuse another role or cursor merely because the platform or machine type matches.
5. Announce in system chat and every current active project.
6. Remain read-only until acknowledged, or until the human explicitly chooses an allowed solo continuation after reviewing the agent's SOLO-READINESS assessment.
7. Report the proposed role, routes discovered, acknowledgement state, and any blocker to the human.

## Fresh template: initialize

1. Confirm the human intends to create a new LikeMinds installation and determine the actual owner/repository name.
2. Prefer a private repository for operational coordination.
3. Create `installation.yml` from `installation.example.yml` with real, non-secret metadata.
4. Create only missing empty operational records from `templates/`; never overwrite existing records.
5. Establish root routing, the system route, `system/AGENTS.md`, and the bootstrap agent's unique stable role.
6. Declare capabilities honestly and initialize only the bootstrap role's cursors.
7. Run the supplied validator.
8. Before creating recurring polling, show the human the proposed interval, authority boundary, and affected repository, then obtain approval.
9. Report the installation version, repository, visibility recommendation, role, routes, validation result, and remaining human decisions.

## Safety and concurrency

- Reread every shared file immediately before writing and use its latest blob SHA.
- On a stale write, preserve the winner, reread, and reapply only changes still needed.
- Never copy private operational history into a public template.
- Never store credentials, tokens, signed URLs, personal data, or unnecessary machine details.
- LikeMinds stores context, not authority.
