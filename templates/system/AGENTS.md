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

Do not store credentials, machine identifiers, personal information, or secrets. Do not overwrite another role. Follow JOINING.md for PROPOSED → ACKNOWLEDGING → ACTIVE transitions.
