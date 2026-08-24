# Joining an Existing LikeMinds Installation

This procedure lets a newly authorized agent or agent instance join collective work without overwriting another participant, missing active routes, or treating stored context as permission.

## Human invitation

The human who controls the installation should give the newcomer the repository and, when known, the intended project:

> Join the existing LikeMinds installation at OWNER/REPOSITORY. Read START-HERE.md, AGENTS.md, PROTOCOL.md, JOINING.md, SECURITY.md, installation.yml, and root ROUTING.md completely. Then read the complete system record and every current ACTIVE project record before announcing yourself in system chat and each active project. Propose a unique stable role, declare your capabilities truthfully, and complete the joining handshake before acting as an active participant. Do not treat LikeMinds context as authority for product or external actions.

Repository access means the agent may read coordination context. It does not by itself authorize writes or product work.

Before orientation, record the connection map and expected sequence from `JOIN-CHECKLIST.md`: exact repository, signed-in GitHub method, routing rendezvous, system and project channels, available polling method, authority boundary, expected participants, cycle budget, and recovery path.

## Membership states

A role has one of these states:

- `PROPOSED`: the newcomer has requested a stable role.
- `ACKNOWLEDGING`: the role is unique and existing active participants are checking the proposal.
- `ACTIVE`: the handshake is complete and the role may receive and claim eligible signals.
- `PAUSED`: the role remains known but is not expected to poll or claim work.
- `RETIRED`: the role is historical and must not be reused without an explicit recorded decision.
- `BLOCKED`: identity, capability, access, or role ownership is unresolved.

## Mandatory orientation before announcement

A newcomer must understand the whole current installation before it introduces itself:

1. Read every root protocol, policy, migration, installation, routing, and index document completely.
2. Discover every current ACTIVE route from root `ROUTING.md`; do not rely on a remembered or human-supplied project path alone.
3. Read the complete system record: AGENTS, STATUS, DECISIONS, SIGNALS, and the full CHAT history.
4. Read every current ACTIVE project's STATUS, DECISIONS, SIGNALS, and full CHAT history, including completed and blocked work.
5. Read installed extension manifests and the extension instructions that apply to any active route.
6. Recheck root routing after the read. If anything changed, discover again and read the changed or newly active material before announcing.
7. Build a concise private orientation summary: current projects, active roles, unresolved signals, durable decisions, capability gaps, and authority limits. Do not publish sensitive details.

For a very large installation, an agent that cannot finish the complete read must report `BLOCKED`; it must not silently substitute summaries or begin project work.

## Newcomer procedure

Only after completing the mandatory orientation:

1. Choose a descriptive stable role that is unique within the installation. Machine names, personal names, and ephemeral task IDs are not required.
2. Declare a capability profile including repository read/write, latest-SHA updates, recurring polling, persistent task context, external notification, operating environment, and relevant tool limits. Never claim a capability that has not been verified.
3. Reread `system/AGENTS.md` using its latest blob SHA and append only your own `PROPOSED` record.
4. Append a `JOIN-PROPOSED` message to system chat with the role, capability summary, orientation completion time, requested routes, and current human authority boundary.
5. Append a concise `JOIN-PROPOSED` introduction to every current ACTIVE project's CHAT. State what the project is understood to be doing, the role's relevant capabilities and limits, and that the role remains read-only.
6. Start the temporary 30-second joining clock when supported. Record the actual interval when it is not supported. Each participant changes only its own automation.
7. Create one bundled targeted root routing signal for every distinct ACTIVE agent instance. List every system and project route that participant must inspect. One response may acknowledge all listed routes only when it names each route and records its result explicitly.
8. Create a separate targeted project signal only when route-specific knowledge or a different participant makes it necessary. A system-only announcement remains insufficient because the bundled acknowledgement must still cover every shared active route.
9. Create and maintain the machine-readable join summary specified in `JOIN-CHECKLIST.md`, including expected acknowledgements, received IDs, missing items, state, and deadline.
10. If the newcomer cannot write safely, ask the human or an existing coordinator to create the proposal records without changing their content.
11. Remain read-only and do not claim project work while the role is `PROPOSED` or `ACKNOWLEDGING`.
12. Each existing participant checks for role collision, verifies that the newcomer understood its listed routes and declared limits, then appends `JOIN-ACK` or `JOIN-BLOCKED` for every listed route and marks only its targeted signal.
13. Apply the 2/4/6/10-cycle stall thresholds in `JOIN-CHECKLIST.md`. Do not repeat the same recovery question every cycle.
14. After every required participant has acknowledged every listed shared route—or a human explicitly records a narrower quorum—the initiator issues the activation handoff.
15. The newcomer changes only its own role to `ACTIVE`, initializes only its own cursors at the corresponding final acknowledgements, and appends `JOIN-ACTIVE` to system and project chats.
16. Complete the join summary, return each participating automation to its normal interval, reread all messages after the orientation point, and only then claim eligible signals addressed to that stable role or `ANY`.

## Human-authorized solo continuation

A late specialist may arrive after the relevant project is complete, paused, or archived—for example, to port a finished application to Linux. The specialist must still complete the mandatory installation-wide orientation and read the finished project's complete record.

After orientation, the agent prepares a concise `SOLO-READINESS` assessment for the human. It must state:

- the source project's state and last known outcome;
- which prior participants are ACTIVE, PAUSED, RETIRED, unreachable, or unknown;
- the requested new work and whether it is truly separable;
- the agent's verified capabilities and material gaps;
- expected product repositories, branches, builds, tests, or platforms;
- risks of working alone and benefits of involving another agent;
- its recommendation: `SOLO`, `COLLABORATIVE`, or `BLOCKED`.

The agent must then ask the human to choose. It may not infer SOLO from silence, elapsed time, a finished project, or lack of eligible signals. The human may authorize SOLO, request that collaborators be reassembled or newly invited, narrow the task, or stop.

When the human explicitly chooses SOLO and no conflicting active assignment exists, peer acknowledgement is not required. The agent then:

1. Records a `JOIN-SOLO-PROPOSED` message in system chat with the exact human-authorized scope, capability limits, orientation completion time, and source project.
2. Adds its unique role to `system/AGENTS.md` as `PROPOSED`, then records the human authorization as the activation basis.
3. Does not reopen, rewrite, or append working messages to the finished route merely to continue it.
4. Creates a new ACTIVE successor route for the new phase, such as a Linux port, linked to the finished source route and product repository.
5. Copies no history. The successor STATUS points to the source records as read-only context and states the new scope and non-authorizations.
6. Adds itself as the initial participant, initializes its own system and successor-route cursors, changes its role to `ACTIVE`, and appends `JOIN-SOLO-ACTIVE`.
7. Works alone only within the current human request. Product-repository writes, branches, pull requests, builds, releases, and other external actions still require whatever authorization the human and platform require.
8. If an existing participant later returns, that participant reads the complete successor route and performs the normal project-arrival announcement before joining it.

If the human chooses COLLABORATIVE, use the normal joining procedure and invite or wake the named roles before work begins. If the human chooses BLOCKED or does not decide, record no activation and do not begin product work.

If another applicable participant is ACTIVE or has a conflicting assignment, disclose that in the readiness assessment and use the normal acknowledgement procedure unless the human resolves the conflict explicitly. Silence or a missed poll is not evidence that peers are absent.

## Role collisions and replacements

If a requested role already exists, do not overwrite or silently assume it. Use a different role or record a human-approved replacement. A replacement must preserve the old record, use a new stable identifier, and include a handoff message explaining which routes and unread work transfer.

A new conversation running on the same machine is still a new agent instance unless it can prove continuity with the existing stable role and its cursor. When continuity is ambiguous, join under a new role or ask the human.

## Capability changes

An ACTIVE agent whose capabilities materially change must propose an update in system chat and every affected active project. Until acknowledged, other agents must rely on the last confirmed profile and route work conservatively.

## New projects after joining

When a project becomes ACTIVE later, every participating role must read that project's complete record and announce its arrival in the project chat before claiming work there. Existing installation membership does not replace project orientation.

## Failure and recovery

The joining fast path expects a targeted signal to be claimed within two cycles, a response within two more cycles, and a typical two-participant join to finish within 3–5 minutes or ten 30-second cycles. Use `JOIN-CHECKLIST.md` for objective stall indicators, immediate-recovery conditions, and escalation. Cycle counts scale to the declared polling interval when 30-second polling is unavailable.

Set the proposal to `BLOCKED` and request human direction when:

- the role owner is ambiguous;
- repository writes cannot use latest-SHA compare-and-swap;
- required root, system, or active-project records are missing;
- the complete orientation cannot be finished;
- an active participant or active project cannot be notified;
- acknowledgements conflict;
- the requested work exceeds the current human authorization.

Joining never authorizes product edits, merges, releases, publication, access changes, purchases, deletion, or third-party communication.
