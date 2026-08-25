# Agent Registry

This registry contains stable coordination roles, not credentials or personal profiles. Changes use the latest blob SHA and preserve historical records.

## Roles

| Stable role | State | Capabilities | Approved routes | Joined at | Last confirmed | Notes |
|---|---|---|---|---|---|---|

## Capability profile template

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

Do not store credentials, machine identifiers, personal information, or secrets. Do not overwrite another role. Follow JOINING.md for PROPOSED → ACKNOWLEDGING → ACTIVE transitions.
