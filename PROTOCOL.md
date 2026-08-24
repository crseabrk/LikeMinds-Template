# LikeMinds Core Protocol

Protocol version: 0.1.0-draft

## Records

Every active route has:

- `STATUS.md`: concise living state and next action.
- `DECISIONS.md`: durable choices and rationale.
- `CHAT.md`: append-only messages plus per-role read cursors.
- `SIGNALS.md`: wake, claim, completion, and blocking queue.

Root `ROUTING.md` is the stable rendezvous point. `system/AGENTS.md` is the stable-role and capability registry.

## Membership and joining

New agents follow `JOINING.md` and move through `PROPOSED → ACKNOWLEDGING → ACTIVE`, or `BLOCKED`. Only ACTIVE roles may claim project work.

Before announcing, a newcomer reads the complete framework, system record, and every current ACTIVE project's full record, then rechecks routing for changes. It announces its proposed role in system chat and every active project. A system-only announcement is insufficient. Acknowledgements are bundled per distinct active agent instance: one targeted routing signal lists every route that participant must inspect, and one response may explicitly cover all listed routes. Separate project signals are required only where route-specific knowledge or different participants make them necessary.

A join proposal must declare truthful capabilities, orientation completion, requested routes, and the current human authority boundary. Existing active participants acknowledge in each shared context before activation. Role collisions, incomplete orientation, missing notification paths, or ambiguous continuity block activation. Joining does not expand authority.

A late specialist first completes the full orientation and gives the human a SOLO-READINESS assessment covering project state, participant availability, scope, capabilities, risks, and a SOLO, COLLABORATIVE, or BLOCKED recommendation. The human—not the agent—chooses the operating mode. Only explicit human authorization permits solo continuation. That path records the authorization, preserves the finished route, and creates a linked ACTIVE successor route for the new work phase. Silence is never sufficient evidence that peers are absent.

## Signal lifecycle

`READY → CLAIMED → DONE` or `BLOCKED`. A human may set `CANCELLED`.

Claim with the latest file blob SHA. A stale update means the claim did not succeed; reread before acting. Never delete a signal to consume it.

## Messages and cursors

Messages use unique IDs, ISO-8601 timestamps, stable From/To roles, an allowed type, related stable identifiers, and concise factual content. History is append-only; corrections are new messages.

Advance only your own cursor after reading every earlier message. A new role receives cursors only after activation; each initialization point must follow the final acknowledgement so required context cannot be skipped silently.

## Recovery

While any join is `PROPOSED` or `ACKNOWLEDGING`, joining takes priority over ordinary coordination. Participating agents that support recurring polling temporarily use a 30-second interval and change only their own automations. The join records its expected participants, routes, acknowledgement count, received IDs, missing items, deadline, and state. Apply the 2/4/6/10-cycle recovery thresholds in `JOIN-CHECKLIST.md`; return clocks to normal after `JOIN-ACTIVE` or `JOIN-BLOCKED`.

After three consecutive polls with no eligible signal and no coordination change:

1. Reread required root documents completely.
2. Reread installation metadata, `system/AGENTS.md`, and root routing.
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

Shared living files require latest-SHA replacement. On conflict, preserve the winning update, reread, and reapply only still-valid changes. Never force or silently overwrite another agent's state.

## Extensions

Load order: core → official extensions → installation policy → project extensions → current human authorization. Later layers may narrow but never expand authority beyond the current human request.
