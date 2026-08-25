# Onboarding and Recovery

A new conversation, machine, or disconnected task is a new agent instance unless continuity is unambiguous.

JOIN requires complete orientation, a unique stable role, truthful capabilities, acknowledgements from active participants, and initialization of only the new role's cursors. A joining role remains read-only until ACTIVE.

The coordination minimum and route-specific expansion rules are defined in [Agent Capabilities](Agent-Capabilities.md). A missing capability blocks only the affected operation. The agent reports the gap, evidence, safe remaining scope, mitigation alternatives, and required human decision instead of silently substituting a weaker procedure.

RECOVER is selected when operational state is partial, contradictory, or ambiguous. Recovery verifies required documents, rediscovers routing, compares the role's cursors, and inspects stale claims. It blocks rather than guessing.

During an active join, participants may temporarily shorten their own polling clocks. No agent changes another agent's automation.

## Presence after a crash or closed session

Every participating session has a lease with a non-secret session ID, last-seen timestamp, normal poll interval, and clean-exit state. A missed lease is SUSPECT during the grace window and STALE afterward. STALE sessions do not count toward NOBODY, SOLO, or TEAM, but their durable roles remain untouched.

NOBODY means zero effective sessions. SOLO means one; it stops its own coordination polling and works with the human. TEAM means two or more; polling and signals run. An invalid timestamp or incomplete lease is UNKNOWN and blocks in RECOVER.

Silence is never enough. Reconciliation uses the shared presence record and latest-SHA updates. Re-entering sessions renew their own lease and recompute the state. No session closes another session or changes another agent's automation.
