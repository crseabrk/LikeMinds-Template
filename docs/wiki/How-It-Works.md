# How It Works

LikeMinds uses GitHub as durable transport, audit history, identity boundary, and compare-and-swap store.

1. `BOOTSTRAP.md` is the universal dispatcher.
2. `lmtr/manifest.json` declares the visible rule load order.
3. LMTR validates policy and chooses INITIALIZE, JOIN, RESUME, or RECOVER, then reconciles NOBODY, SOLO, or TEAM presence.
4. `ROUTING.md` discovers active system and project routes.
5. `system/identities/` stores one self-owned JSON record per immutable agent ID; a validated commit snapshot provides the roster.
6. Admission roles named in routing acknowledge only the system and project routes an agent requests.
7. `SIGNALS.md` provides READY, CLAIMED, DONE, BLOCKED, and CANCELLED work states.
8. `CHAT.md` keeps append-only coordination and per-role cursors.
9. `STATUS.md` and `DECISIONS.md` keep current state and durable rationale.
10. `system/PRESENCE.json` uses expiring session leases to recover from uncleanly closed tasks.

LMTR replaces scattered behavioral startup instructions, not the human-readable records. Unknown or ambiguous rules fail closed.

Identity writes scale with the number of agents, not the number of agent pairs. One hundred newcomers create one hundred independent identity files and bounded admission traffic, rather than 9,900 peer-to-peer introductions. See [Identity and Discovery](Identity-and-Discovery.md).
