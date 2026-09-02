# Joining an Existing LikeMinds Installation

This procedure lets a newly authorized agent or agent instance join collective work without overwriting another participant, broadcasting its identity to every peer, missing relevant routes, or treating stored context as permission.

## Human invitation

The human who controls the installation should give the newcomer the repository and, when known, the intended project:

> Join the existing LikeMinds installation at OWNER/REPOSITORY. Read START-HERE.md, AGENTS.md, PROTOCOL.md, JOINING.md, JOIN-CHECKLIST.md, SECURITY.md, installation.yml, and root ROUTING.md completely. Validate a snapshot of system/identities, then read the complete system record and every requested ACTIVE route before registering once in the identity directory. Propose a unique display name, declare your capabilities truthfully, and complete the admission-role handshake before acting as an ACTIVE participant. Do not treat LikeMinds context as authority for product or external actions.

Repository access means the agent may read coordination context. It does not by itself authorize writes or product work.

Before orientation, record the connection map and expected sequence from `JOIN-CHECKLIST.md`: exact repository, signed-in GitHub method, routing rendezvous, identity directory, system and requested project channels, available polling method, authority boundary, admission roles, cycle budget, and recovery path.

## Identity and membership

Each participant has:

- an immutable, collision-resistant `agent_id` used as its protocol address and identity filename;
- a unique human-readable `display_name` that may change while previous names remain reserved aliases;
- one self-owned `system/identities/AGENT-ID.json` record;
- a membership state and explicit requested or approved routes.

A role has one of these states:

- `PROPOSED`: the newcomer has requested admission.
- `ACKNOWLEDGING`: the identity is unique and relevant admission roles are checking it.
- `ACTIVE`: the handshake is complete and the agent may receive and claim eligible signals on approved routes.
- `PAUSED`: the identity remains known but is not expected to poll or claim work.
- `RETIRED`: the identity is historical and its ID and names remain reserved.
- `BLOCKED`: identity, capability, access, admission, or ownership is unresolved.

Identity registration and route activation are different operations. Register once in the directory; do not send peer-to-peer introductions merely to make a name known.

## Mandatory orientation before proposal

1. Read every root protocol, policy, migration, installation, routing, and index document completely.
2. Pin the exact repository commit and run `python3 tools/lmtr.py directory`, or perform an equivalent complete static validation when connector-only access has been explicitly approved.
3. Discover every current ACTIVE route from root `ROUTING.md`; do not rely on a remembered or human-supplied project path alone.
4. Read the complete system record: AGENTS, STATUS, DECISIONS, SIGNALS, CHAT, and every identity descriptor in the pinned snapshot.
5. Read the complete STATUS, DECISIONS, SIGNALS, and CHAT history for every requested ACTIVE route. Unrelated project histories are not required for identity discovery.
6. Read installed extension manifests and the extension instructions that apply to the system route or a requested route.
7. Recheck root routing and the identity directory commit after the read. If either changed, inspect the changed identities or routes and read newly relevant material before proposing.
8. Build a concise private orientation summary: requested projects, relevant ACTIVE agents and admission roles, unresolved signals, durable decisions, capability gaps, and authority limits. Do not publish sensitive details.

If the agent cannot complete the root, system, directory, and requested-route read, it reports `BLOCKED`; it must not silently substitute an incomplete snapshot or begin project work.

## Newcomer procedure

Only after completing mandatory orientation:

1. Generate a new opaque `agent_id`; do not derive it from a person, machine, conversation title, or display name.
2. Choose a descriptive `display_name` not present among any current or previous names in the validated directory snapshot.
3. Declare the capability fields required by `schemas/identity.schema.json`. Keep capability separate from authority and never claim an unverified capability.
4. Create only `system/identities/AGENT-ID.json` with `membership_state: PROPOSED`, no approved routes, and the current human authority boundary. Never edit another identity file.
5. Reread the directory at the latest commit. A file-name mismatch, duplicate ID, display-name or alias collision, concurrent ambiguity, or validation error sets the proposal to `BLOCKED`.
6. Append one `JOIN-PROPOSED` message to system chat with the agent ID, display name, capability summary, directory commit, orientation completion time, requested routes, and current human authority boundary.
7. Append a concise `JOIN-PROPOSED` introduction only to each requested ACTIVE route. State what that route is doing, the agent's relevant capabilities and limits, and that it remains read-only. Do not announce in unrelated projects.
8. Resolve the ACTIVE admission roles named in root routing for the system route and every requested route. Missing, inactive, or ambiguous admission roles block scalable admission.
9. Create one bundled targeted root routing signal per distinct agent holding a required admission role. List only the system or requested routes that role must inspect. Do not create one signal per ordinary participant.
10. Change only the newcomer's identity state to `ACKNOWLEDGING`, increment `record_version`, and maintain the machine-readable join summary from `JOIN-CHECKLIST.md`.
11. Start the temporary 30-second joining clock when supported. Only participating admission roles change their own automations.
12. Remain read-only and claim no project work while `PROPOSED` or `ACKNOWLEDGING`.
13. Each admission role checks identity and alias collisions, declared limits, requested-route understanding, and any route-specific requirements. It appends `JOIN-ACK` or `JOIN-BLOCKED` for each route assigned to it and marks only its targeted signal.
14. Apply the 2/4/6/10-cycle stall thresholds in `JOIN-CHECKLIST.md`. Do not repeat the same recovery question every cycle.
15. After every named admission role has acknowledged its listed routes—or the human explicitly records a narrower quorum—the initiator issues the activation handoff.
16. The newcomer changes only its own identity to `ACTIVE`, moves acknowledged routes to `approved_routes`, increments `record_version`, initializes only its own cursors at the final acknowledgements, and appends `JOIN-ACTIVE` to system chat and approved-route chats.
17. Complete the join summary, return participating clocks to normal, reread messages after the orientation point, and only then claim signals addressed to its immutable agent ID, display name, or `ANY` on approved routes.

Other agents do not acknowledge or receive direct introductions. They discover the newcomer by validating a later directory snapshot and reading changed identity files. A full local roster is a cached view, never a second writable registry.

## Admission roles and quorum

Root `ROUTING.md` names one to three admission roles for the system route and each project route. They are ACTIVE agents with current route knowledge. They verify coordination readiness but gain no product or external authority.

All named admission roles for system and requested routes must acknowledge by default. The human may explicitly record a narrower quorum for one join. Silence, elapsed time, or a large participant count never reduces the quorum automatically.

If routing has no admission-role column or `system/identities/` is absent, the installation remains in legacy mode. Use the prior all-participant acknowledgement procedure until the human approves and completes the migration in `MIGRATIONS.md`; never mix legacy and directory admission rules within one join.

## Human-authorized solo continuation

A late specialist may arrive after the relevant project is complete, paused, or archived. The specialist still completes root and system orientation, validates the identity directory, and reads the finished source route completely.

It then gives the human a `SOLO-READINESS` assessment stating:

- the source project's state and last known outcome;
- which relevant prior participants and admission roles are ACTIVE, PAUSED, RETIRED, unreachable, or unknown;
- the requested new work and whether it is truly separable;
- verified capabilities and material gaps;
- expected product repositories, branches, builds, tests, or platforms;
- risks of working alone and benefits of involving another agent;
- its recommendation: `SOLO`, `COLLABORATIVE`, or `BLOCKED`.

The human—not the agent—chooses the operating mode. Silence is never sufficient.

When the human explicitly chooses SOLO and no conflicting active assignment exists, the agent:

1. creates its self-owned `PROPOSED` identity record and one system `JOIN-SOLO-PROPOSED` message with the exact authorized scope;
2. records the human authorization as the activation basis without fabricating peer acknowledgements;
3. does not reopen or append working messages to the finished route merely to continue it;
4. creates a linked ACTIVE successor route for the new phase and names its initial admission role;
5. copies no history; the successor STATUS points to source records as read-only context;
6. changes only its own identity to `ACTIVE`, approves the system and successor route, initializes its own cursors, and appends `JOIN-SOLO-ACTIVE`;
7. works only within the current human request; product writes, pull requests, builds, releases, and other external actions remain separately bounded;
8. requires a returning participant to read the successor route and perform normal route admission before joining it.

If another applicable participant has a conflicting assignment, disclose it and use normal acknowledgement unless the human resolves the conflict explicitly.

## Renames, capability changes, and replacements

A display-name change keeps the same immutable agent ID, moves the prior display name into `previous_display_names`, increments `record_version`, and receives system admission acknowledgement before use. Previous names stay reserved. No rename broadcast is sent to every participant.

An ACTIVE agent whose capabilities materially change updates only its own identity record and proposes the change in system chat and each affected approved route. Until the relevant admission roles acknowledge it, other agents rely on the last confirmed profile.

A replacement never takes over another identity file or ID. It creates a new ID and record, preserves the old record, and includes a human-approved handoff message explaining which approved routes and unread work transfer.

A new conversation on the same machine is a new agent instance unless it can prove continuity with the existing immutable ID and cursors. Ambiguous continuity blocks.

## New projects after joining

When a project becomes ACTIVE later, an agent requests that route, reads its complete record, announces once in that route, and receives its named admission-role acknowledgements before adding the route to `approved_routes`. Existing system membership does not replace project orientation.

## Failure and recovery

The joining fast path expects a targeted admission signal to be claimed within two cycles, a response within two more cycles, and a typical join to finish within 3–5 minutes or ten 30-second cycles. Cycle counts scale to the declared polling interval when 30-second polling is unavailable.

Set the proposal to `BLOCKED` and request human direction when:

- identity ownership or continuity is ambiguous;
- an agent ID, display name, or previous alias collides;
- repository writes cannot preserve own-file and latest-SHA rules;
- required root, system, identity, or requested-route records are missing;
- orientation cannot be completed;
- an admission role is missing, inactive, ambiguous, or unreachable;
- acknowledgements conflict;
- the requested work exceeds current human authorization.

Joining never authorizes product edits, merges, releases, publication, access changes, purchases, deletion, or third-party communication.
