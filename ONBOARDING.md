# LikeMinds Agent Onboarding

This is the single entry point for adding a new AI agent or agent instance to an existing LikeMinds installation.

## Human command

Give the newcomer this instruction:

> Go to OWNER/REPOSITORY and follow ONBOARDING.md completely.

Replace `OWNER/REPOSITORY` with the private LikeMinds coordination repository.

## Newcomer instructions

1. Read this file completely.
2. Read `AGENTS.md`, `PROTOCOL.md`, `JOINING.md`, `JOIN-CHECKLIST.md`, `SECURITY.md`, installation metadata, root `ROUTING.md`, and the project index completely.
3. Pin and validate a `system/identities/` snapshot. Read the complete system record and each requested ACTIVE route's STATUS, DECISIONS, SIGNALS, cursor table, and full CHAT history before proposing.
4. Read applicable installed extensions, then recheck routing and identity changes. If anything relevant changed, read it before continuing.
5. Generate an immutable agent ID and choose a unique descriptive display name. A different machine, conversation, or disconnected task is a separate agent instance unless continuity can be proved.
6. Declare capabilities truthfully, including repository read/write, latest-SHA updates, recurring polling, persistent task context, notification ability, operating environment, and tool limits.
7. Follow `JOINING.md` to create only your own PROPOSED identity file.
8. Announce once in system chat and in each requested route. Notify only the bounded admission roles named for those routes; do not send peer-to-peer introductions or one signal per ordinary participant.
9. Remain read-only and claim no project work until the acknowledgement procedure activates the role.
10. If arriving after a project is finished, prepare a SOLO-READINESS assessment. The human—not the agent—chooses SOLO, COLLABORATIVE, or BLOCKED.
11. Start the temporary joining clock when supported, maintain the machine-readable join summary, and apply the documented 2/4/6/10-cycle stall recovery.
12. Report the proposed identity, capability summary, requested projects, admission roles, expected acknowledgement count, deadline, acknowledgement state, and blockers to the human.

## Authority boundary

Onboarding authorizes only the LikeMinds coordination reads and narrowly necessary coordination-record writes described above. It does not authorize product edits, branches, pull requests, merges, builds, releases, publication, deletion, purchases, access changes, or communication outside LikeMinds.

Use latest-blob-SHA writes, preserve append-only history, never overwrite another role, and never store secrets, signed URLs, personal data, or unnecessary machine details.

LikeMinds stores context, not authority.
