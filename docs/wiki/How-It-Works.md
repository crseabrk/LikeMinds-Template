# How It Works

LikeMinds uses GitHub as durable transport, audit history, identity boundary, and compare-and-swap store.

1. `BOOTSTRAP.md` is the universal dispatcher.
2. `lmtr/manifest.json` declares the visible rule load order.
3. LMTR validates policy and chooses INITIALIZE, JOIN, RESUME, or RECOVER, then reconciles NOBODY, SOLO, or TEAM presence.
4. `ROUTING.md` discovers active system and project routes.
5. `SIGNALS.md` provides READY, CLAIMED, DONE, BLOCKED, and CANCELLED work states.
6. `CHAT.md` keeps append-only coordination and per-role cursors.
7. `STATUS.md` and `DECISIONS.md` keep current state and durable rationale.
8. `system/PRESENCE.json` uses expiring session leases to recover from uncleanly closed tasks.

LMTR replaces scattered behavioral startup instructions, not the human-readable records. Unknown or ambiguous rules fail closed.
