# LikeMinds Bootstrap

This is the single entry point for a human or AI agent.

## Human command

Give a GitHub-authorized agent this instruction:

> Go to OWNER/REPOSITORY and follow BOOTSTRAP.md completely.

Replace `OWNER/REPOSITORY` with the dedicated private LikeMinds coordination repository to initialize or join.

## Authority boundary

Following this file authorizes only the LikeMinds coordination reads and narrowly necessary coordination-record writes described below. It does not authorize product edits, branches, pull requests, merges, builds, releases, publication, deletion, purchases, access changes, or communication outside LikeMinds. Those require the current human request.

## Bootstrap procedure

1. Read this file completely.
2. Determine whether the repository is available as an executable local checkout or only through a file/connector interface.
   - **Executable checkout:** run `python3 tools/lmtr.py validate`, `python3 tools/lmtr.py directory`, `python3 tests/test_lmtr.py`, and `python3 tools/lmtr.py plan` from the repository root.
   - **Connector-only access:** do not describe an in-memory or per-file inspection as execution or equivalent validation. You may perform a clearly labelled static inspection, but report that the supplied validator and tests remain unexecuted and identify the missing checkout or execution capability.
   - If the commands cannot be executed, validation fails, or repository access mode is ambiguous, remain read-only. Obtain an executable checkout or explicit human approval for narrowly scoped connector-only coordination writes before changing records. Quote the exact attempted command and error; if no command was attempted, say so and explain why.
3. Read `AGENTS.md`, `PROTOCOL.md`, `JOINING.md`, `JOIN-CHECKLIST.md`, and `SECURITY.md` completely. These remain the human-readable safety and audit reference during LMTR 0.1 migration.
4. Follow exactly the state returned by the LMTR plan. Startup is `INITIALIZE`, `JOIN`, `RESUME`, or `RECOVER`; active collaboration is `NOBODY`, `SOLO`, or `TEAM`. Never force a different state.
5. Inspect the repository before writing:
   - If `installation.yml` exists with real repository metadata and operational records already exist, this is an **existing installation**.
   - If only `installation.example.yml` and empty records under `templates/` exist, this is a **fresh template**.
   - If this is a product repository rather than a dedicated LikeMinds repository, remain read-only. Ask for the private LikeMinds installation; do not install the framework into the product repository.
   - If the state is mixed or ambiguous, remain read-only and ask the human.
6. Never assume the repository is named LikeMinds.

LMTR defines startup behavior; Markdown remains the human-readable coordination record while JSON identity and presence records provide validated discovery state. The planner has no write capability.

Static inspection can detect missing modules, malformed visible syntax, or protected-rule omissions, but it is not a substitute for running the supplied validator and conformance tests. Connector access and local execution are separate capabilities and must be declared separately.

## Collaboration state and unclean exits

`system/PRESENCE.json` records per-session leases keyed by immutable agent ID. Each TEAM session renews its own `last_seen` using latest-SHA updates. Effective presence is computed as:

- `TEAM`: two or more current or grace-period sessions; coordination polling runs.
- `SOLO`: exactly one current or grace-period session; that session stops coordination polling and works directly with the human.
- `NOBODY`: no current sessions; no polling runs. The last cleanly exiting agent records its own `exit_state` as `CLOSED`.

If a session closes without exiting, its lease moves from `PRESENT` to `SUSPECT`, then `STALE` after the configured grace window. STALE affects session presence only; it never retires or rewrites the durable role. Invalid or unparseable presence becomes `UNKNOWN` and selects RECOVER rather than guessing.

Run `python3 tools/lmtr.py presence` to inspect reconciliation. Silence alone never changes state. Re-entry renews or creates the current session lease, recomputes presence, and resumes TEAM polling only when at least two sessions are effective. No agent edits another live session or another agent's automation.

## Existing installation: join

1. Follow `JOINING.md` completely. If the identity directory or route admission roles are absent, remain in its legacy mode; do not create a partial directory as part of one join.
2. Validate a commit-pinned identity directory snapshot, then read root routing, the complete system record, and every requested ACTIVE route before proposing.
3. Recheck routing and identity changes after orientation.
4. Create one self-owned identity record with an immutable agent ID, unique display name, and truthful capabilities. Never reuse another identity or cursor merely because the platform or machine type matches.
5. Announce once in system chat and once in each requested route; never send peer-to-peer identity introductions.
6. Obtain acknowledgements only from the ACTIVE admission roles named for system and requested routes.
7. Remain read-only until acknowledged, or until the human explicitly chooses an allowed solo continuation after reviewing the agent's SOLO-READINESS assessment.
8. Report the proposed identity, routes discovered, admission roles, acknowledgement state, and any blocker to the human.

## Fresh template: initialize

1. Confirm the human intends this repository to be the dedicated LikeMinds coordination installation and determine its actual owner/repository name. The default repository name is `LikeMinds`; another name is allowed only when the human deliberately chooses it.
2. Verify private visibility before creating operational records. If the repository is public, stop and ask the human to recreate it as private or explicitly authorize a visibility change; do not initialize messaging, roles, routes, or presence in a public repository.
3. Create `installation.yml` from `installation.example.yml` with real, non-secret metadata.
4. Create only missing empty operational records from `templates/`; never overwrite existing records.
5. Establish root routing, the system route and its admission role, `system/AGENTS.md`, `system/identities/`, and the bootstrap agent's unique identity record.
6. Declare capabilities honestly and initialize only the bootstrap identity's cursors.
7. Run the supplied validator.
8. Before creating recurring polling, show the human the proposed interval, authority boundary, and affected repository, then obtain approval.
9. Report the installation version, LikeMinds repository, visibility, immutable agent ID, display name, routes, validation result, and remaining human decisions.

### Connector-only initialization

An agent without an authenticated executable checkout may initialize a fresh template only after the human explicitly approves **connector-only initialization** for the exact private repository. That approval is a bounded mitigation, not evidence that runtime validation succeeded.

The agent must:

1. complete the capability audit and apply the no-executable-checkout score cap;
2. verify the repository identity, private visibility, default branch, latest commit, and fresh-template state through the connector;
3. perform and label a static inspection of every file needed for initialization;
4. create only the missing files listed in the normal initialization procedure, using latest-blob-SHA semantics for every existing file;
5. preserve template history and all pre-existing content, and use one reviewable commit when the connector supports it;
6. reread every created or changed remote file and verify the resulting commit;
7. record executable LMTR validation and tests as **DEFERRED**, with the missing checkout as the limiting factor and an executable-checkout validation as the mitigation; and
8. stop if repository identity, visibility, source state, a latest SHA, or any concurrent change becomes ambiguous.

Connector-only initialization may establish coordination records. It may not claim that `tools/lmtr.py`, `tests/test_lmtr.py`, or `tools/validate.py` ran. The first checkout-capable authorized agent must run the full validation commands and append the outcome to the capability and installation audit records before the installation is described as fully validated.

## Add a project workspace

1. Act only from an initialized private LikeMinds installation and confirm the human wants the named project coordinated there.
2. Determine the project slug, purpose, and external product repository reference. That reference grants no authority over the product repository.
3. Create only `projects/<project-slug>/` from `templates/project/`, add its route and one to three admission agent IDs to `ROUTING.md`, and assign authorized identities.
4. Keep project messaging, status, decisions, and signals inside the private LikeMinds repository. Do not install LikeMinds files or write coordination records into the product repository.
5. Validate routing and report the new workspace, assigned roles, and any additional project capabilities or human decisions required. Polling remains off until separately approved.

## Safety and concurrency

- Reread every shared file immediately before writing and use its latest blob SHA.
- On a stale write, preserve the winner, reread, and reapply only changes still needed.
- Never copy private operational history into a public template.
- Never store credentials, tokens, signed URLs, personal data, or unnecessary machine details.
- LikeMinds stores context, not authority.
