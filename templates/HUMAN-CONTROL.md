# LikeMinds Human Control

This append-only ledger records human requests made through the GitHub Actions **LikeMinds control panel**. The newest valid request for a stable role supersedes its earlier requests.

A control request may narrow an agent's authority immediately. It cannot grant capabilities the agent does not possess, override platform safety rules, or substitute for current human authorization where an external action requires confirmation.

## Allowed values

- Agent state: `ACTIVE`, `READ_ONLY`, `PAUSED`, or `REVOKED`
- Poll interval: `30 seconds`, `3 minutes`, `10 minutes`, or `MANUAL`
- Permission: `ALLOW`, `ASK`, or `DENY`

Agents read this file on every heartbeat, apply changes only to their own task or automation, and record the outcome in `HUMAN-STATUS.md`. Permission reductions apply immediately. Permission increases become effective only after the affected agent confirms that the request is valid, supported, and within its governing instructions.

## Requests

No control requests have been submitted.
