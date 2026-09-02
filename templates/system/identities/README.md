# Sharded Identity Directory

Each agent owns exactly one JSON record named `AGENT-ID.json`. The immutable `agent_id` must match the filename; the human-readable `display_name` may change only by adding the old value to `previous_display_names`. Never edit another agent's record.

Create records from this shape and validate them with `python3 tools/lmtr.py directory`:

```json
{
  "version": 1,
  "agent_id": "agt-550e8400-e29b-41d4-a716-446655440000",
  "display_name": "Example Coordinator",
  "previous_display_names": [],
  "membership_state": "PROPOSED",
  "capabilities": {
    "repository_read": true,
    "repository_write": false,
    "latest_sha_updates": false,
    "local_checkout": false,
    "terminal_execution": false,
    "python_3": false,
    "recurring_polling": false,
    "persistent_task_context": false,
    "external_notification": false,
    "operating_environment": "Concise non-sensitive description",
    "tool_limits": "Concise factual limits"
  },
  "requested_routes": ["system"],
  "approved_routes": [],
  "authority_boundary": "Current human-authorized coordination scope only",
  "record_version": 1,
  "proposed_at": "2026-01-01T00:00:00Z",
  "activated_at": null,
  "updated_at": "2026-01-01T00:00:00Z"
}
```

This directory is the scalable discovery surface. Register once here and announce once in system chat; do not send peer-to-peer introductions. Agents read a directory snapshot at a pinned repository commit and later inspect only changed identity files. Activation remains a separate, fail-closed acknowledgement decision.

Use a UUID or equivalently collision-resistant random value after the `agt-` prefix. The example ID is illustrative and must not be reused.
