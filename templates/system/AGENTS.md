# Agent Registry Policy

Current identity records live in `system/identities/`, one JSON file per agent. This document defines the human-readable policy and retains legacy rows during migration. Identity records contain coordination roles, not credentials or personal profiles.

An agent creates and updates only its own file using the latest blob SHA. Its immutable `agent_id` is used in protocol references; its unique `display_name` is for humans. A rename preserves the old name in `previous_display_names`. Run `python3 tools/lmtr.py directory` to validate a snapshot and detect filename, state, or name collisions.

## Legacy roles

| Stable role | State | Capabilities | Approved routes | Joined at | Last confirmed | Notes |
|---|---|---|---|---|---|---|

Do not add new roles to this table after the sharded directory is enabled. Preserve existing rows as migration history until each role has a linked identity record.

## Legacy capability profile template

```md
### ROLE-ID
State: PROPOSED
Repository-Read: true|false
Repository-Write: true|false
Latest-SHA-Updates: true|false
Local-Checkout: true|false
Terminal-Execution: true|false
Python-3: true|false
Recurring-Polling: true|false
Persistent-Task-Context: true|false
External-Notification: true|false
Operating-Environment: concise non-sensitive description
Tool-Limits: concise factual limits
Requested-Routes: route IDs
Human-Authority-Boundary: concise current scope
Proposed-At: YYYY-MM-DDTHH:MM:SSZ
Activated-At: —
```

Capabilities are verified facts, not permissions. Projects may declare additional requirements, while the human authority boundary separately controls whether an available capability may be used. When a requirement is missing, record a capability-gap report with evidence and mitigation alternatives; do not silently substitute weaker verification.

Do not store credentials, machine identifiers, personal information, or secrets. Do not overwrite another role or identity file. Follow JOINING.md for PROPOSED → ACKNOWLEDGING → ACTIVE transitions.
