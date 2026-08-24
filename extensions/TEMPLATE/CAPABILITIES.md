# Capability Contract

Use explicit booleans or enumerated values. Never infer that all agents support the same tools.

Common capabilities:

- repository_read
- repository_write
- compare_and_swap_updates
- scheduled_tasks
- persistent_task_context
- external_notifications
- pull_request_creation
- structured_validation

A required missing capability blocks installation unless this extension documents a safe human-operated fallback.
