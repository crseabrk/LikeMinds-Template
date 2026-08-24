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
2. Read `AGENTS.md`, `PROTOCOL.md`, `JOINING.md`, `JOIN-CHECKLIST.md`, and `SECURITY.md` completely.
3. Inspect the repository before writing:
   - If `installation.yml` exists with real repository metadata and operational records already exist, this is an **existing installation**.
   - If only `installation.example.yml` and empty records under `templates/` exist, this is a **fresh template**.
   - If the state is mixed or ambiguous, remain read-only and ask the human.
4. Never assume the repository is named LikeMinds.

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
