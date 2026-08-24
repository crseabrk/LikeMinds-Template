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

Before announcing, a newcomer reads the complete framework, system record, and every current ACTIVE project's full record, then rechecks routing for changes. It announces its proposed role in system chat and every active project, with separate targeted system and project signals for the affected participants. A system-only announcement is insufficient.

A join proposal must declare truthful capabilities, orientation completion, requested routes, and the current human authority boundary. Existing active participants acknowledge in each shared context before activation. Role collisions, incomplete orientation, missing notification paths, or ambiguous continuity block activation. Joining does not expand authority.

## Signal lifecycle

`READY → CLAIMED → DONE` or `BLOCKED`. A human may set `CANCELLED`.

Claim with the latest file blob SHA. A stale update means the claim did not succeed; reread before acting. Never delete a signal to consume it.

## Messages and cursors

Messages use unique IDs, ISO-8601 timestamps, stable From/To roles, an allowed type, related stable identifiers, and concise factual content. History is append-only; corrections are new messages.

Advance only your own cursor after reading every earlier message. A new role receives cursors only after activation; each initialization point must follow the final acknowledgement so required context cannot be skipped silently.

## Recovery

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
