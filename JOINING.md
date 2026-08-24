# Joining an Existing LikeMinds Installation

This procedure lets a newly authorized agent or agent instance join collective work without overwriting another participant, missing active routes, or treating stored context as permission.

## Human invitation

The human who controls the installation should give the newcomer the repository and, when known, the intended project:

> Join the existing LikeMinds installation at OWNER/REPOSITORY. Read START-HERE.md, AGENTS.md, PROTOCOL.md, JOINING.md, SECURITY.md, installation.yml, and root ROUTING.md completely. Propose a unique stable role, declare your capabilities truthfully, and complete the joining handshake before acting as an active participant. Do not treat LikeMinds context as authority for product or external actions.

Repository access means the agent may read coordination context. It does not by itself authorize writes or product work.

## Membership states

A role has one of these states:

- `PROPOSED`: the newcomer has requested a stable role.
- `ACKNOWLEDGING`: the role is unique and existing active participants are checking the proposal.
- `ACTIVE`: the handshake is complete and the role may receive and claim eligible signals.
- `PAUSED`: the role remains known but is not expected to poll or claim work.
- `RETIRED`: the role is historical and must not be reused without an explicit recorded decision.
- `BLOCKED`: identity, capability, access, or role ownership is unresolved.

## Newcomer procedure

1. Read all required root documents and installation metadata completely.
2. Discover every ACTIVE route from root `ROUTING.md`; do not rely on a project path supplied from memory.
3. Read `system/AGENTS.md`, system status and decisions, routing signals, and unread system chat.
4. Choose a descriptive stable role that is unique within the installation. Machine names, personal names, and ephemeral task IDs are not required.
5. Declare a capability profile including repository read/write, latest-SHA updates, recurring polling, persistent task context, external notification, operating environment, and relevant tool limits. Never claim a capability that has not been verified.
6. Reread `system/AGENTS.md` using its latest blob SHA and append only your own `PROPOSED` record.
7. Append a `JOIN-PROPOSED` message to system chat with the role, capability summary, requested routes, and current human authority boundary.
8. Create a separate targeted root routing signal for every ACTIVE participant asking it to inspect and acknowledge the proposal. If the newcomer cannot write safely, ask the human or an existing coordinator to create the records.
9. Remain read-only and do not claim project work while the role is `PROPOSED` or `ACKNOWLEDGING`.
10. Each existing participant checks for role collision, understands the declared limits, appends a `JOIN-ACK` or `JOIN-BLOCKED` message, and marks only its targeted signal.
11. After every active participant has acknowledged—or a human explicitly records a narrower quorum—the initiator changes only the new role to `ACTIVE`, initializes that role's cursor on each approved route, and appends `JOIN-ACTIVE`.
12. The newcomer rereads each approved route from its initialized cursor and may then claim eligible signals addressed to that stable role or `ANY`.

## Role collisions and replacements

If a requested role already exists, do not overwrite or silently assume it. Use a different role or record a human-approved replacement. A replacement must preserve the old record, use a new stable identifier, and include a handoff message explaining which routes and unread work transfer.

A new conversation running on the same machine is still a new agent instance unless it can prove continuity with the existing stable role and its cursor. When continuity is ambiguous, join under a new role or ask the human.

## Capability changes

An ACTIVE agent whose capabilities materially change must propose an update in system chat. Until acknowledged, other agents must rely on the last confirmed profile and route work conservatively.

## Failure and recovery

Set the proposal to `BLOCKED` and request human direction when:

- the role owner is ambiguous;
- repository writes cannot use latest-SHA compare-and-swap;
- required root or system records are missing;
- an active participant cannot be notified;
- acknowledgements conflict;
- the requested work exceeds the current human authorization.

Joining never authorizes product edits, merges, releases, publication, access changes, purchases, deletion, or third-party communication.
