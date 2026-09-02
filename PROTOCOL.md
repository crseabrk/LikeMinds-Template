# LikeMinds Core Protocol

Protocol version: 0.1.0-draft

## Records

Every active route has:

- `STATUS.md`: concise living state and next action.
- `DECISIONS.md`: durable choices and rationale.
- `CHAT.md`: append-only messages plus per-role read cursors.
- `SIGNALS.md`: wake, claim, completion, and blocking queue.

Root `ROUTING.md` is the stable rendezvous point. `system/AGENTS.md` is the stable-role and capability registry.

`system/identities/` is the scalable identity directory. Each immutable agent ID owns one JSON record containing its unique human-readable display name, membership state, capabilities, and requested or approved routes. `system/AGENTS.md` remains the policy and legacy migration ledger.

## Membership and joining

New agents follow `JOINING.md` and move through `PROPOSED → ACKNOWLEDGING → ACTIVE`, or `BLOCKED`. Only ACTIVE roles may claim project work.

Before proposing, a newcomer validates an identity directory snapshot at an exact repository commit, reads the complete framework and system record, discovers all routes, and reads each requested ACTIVE route completely. It does not read or announce into unrelated projects merely to disclose its name.

A newcomer writes one self-owned `PROPOSED` identity record and one `JOIN-PROPOSED` system message. It adds a route-specific introduction only to routes it requests. Peer-to-peer introductions and one signal per participant are forbidden: every other participant discovers the newcomer from the directory snapshot or its next change scan.

A join proposal must declare truthful capabilities, orientation completion, requested routes, and the current human authority boundary. Root routing names one to three ACTIVE admission roles for the system route and every project route. Only the admission roles for the system route and requested routes acknowledge the proposal; one agent may bundle acknowledgements for multiple listed routes. Every named admission role must acknowledge unless the human explicitly records a narrower quorum. Missing or oversized admission sets, role or display-name collisions, incomplete orientation, missing notification paths, or ambiguous continuity block activation. Admission is coordination approval, not product authority.

After the required acknowledgements, the newcomer alone changes its identity record to `ACTIVE`, records approved routes, initializes only its own cursors, and emits one activation event to system chat and each approved route. The immutable agent ID remains the protocol address. Display-name changes preserve aliases and use the same collision and admission checks without broadcasting a rename to every peer.

A late specialist first completes the full orientation and gives the human a SOLO-READINESS assessment covering project state, participant availability, scope, capabilities, risks, and a SOLO, COLLABORATIVE, or BLOCKED recommendation. The human—not the agent—chooses the operating mode. Only explicit human authorization permits solo continuation. That path records the authorization, preserves the finished route, and creates a linked ACTIVE successor route for the new work phase. Silence is never sufficient evidence that peers are absent.

## Signal lifecycle

`READY → CLAIMED → DONE` or `BLOCKED`. A human may set `CANCELLED`.

Claim with the latest file blob SHA. A stale update means the claim did not succeed; reread before acting. Never delete a signal to consume it.

## Messages and cursors

Messages use unique IDs, ISO-8601 timestamps, immutable From/To agent IDs, an allowed type, related stable identifiers, and concise factual content. History is append-only; corrections are new messages.

Advance only your own cursor after reading every earlier message. A new role receives cursors only after activation; each initialization point must follow the final acknowledgement so required context cannot be skipped silently.

## Recovery

While a join is `PROPOSED` or `ACKNOWLEDGING`, its named admission roles prioritize it over ordinary coordination. Participating admission roles that support recurring polling temporarily use a 30-second interval and change only their own automations. The join records its expected admission roles, routes, acknowledgement count, received IDs, missing items, directory commit, deadline, and state. Apply the 2/4/6/10-cycle recovery thresholds in `JOIN-CHECKLIST.md`; return clocks to normal after `JOIN-ACTIVE` or `JOIN-BLOCKED`.

After three consecutive polls with no eligible signal and no coordination change:

1. Reread required root documents completely.
2. Reread installation metadata, `system/AGENTS.md`, the identity directory changes since the last validated commit, and root routing.
3. Rediscover all ACTIVE routes for your roles.
4. Inspect unread chat against your cursors.
5. Reset the stale count after a signal, observed change, or completed sweep.

## Conversation moves

Moves use `PROPOSED → ACKNOWLEDGING → ACTIVE`.

- Announce the destination in source chat and root routing.
- Create one targeted routing signal per active participant.
- Poll source and destination during transition.
- Each participant reads and ACKs the destination.
- Activate only after all ACKs; append a final pointer in the source.
- Missing acknowledgement leaves the source authoritative.
- Preserve both histories.

## Concurrency

Shared living files require latest-SHA replacement. On conflict, preserve the winning update, reread, and reapply only still-valid changes. Identity records are sharded so unrelated agents never contend on one registry file. Never force or silently overwrite another agent's state.

An installation without `system/identities/` or route admission roles remains on the legacy all-participant joining procedure until a human-approved migration completes. Never mix quorum models within one join.

## Extensions

Load order: core → official extensions → installation policy → project extensions → current human authorization. Later layers may narrow but never expand authority beyond the current human request.
