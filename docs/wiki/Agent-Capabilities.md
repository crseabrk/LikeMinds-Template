# Agent Capabilities

LikeMinds separates an agent's immutable ID, human-readable display name, technical capabilities, route assignment, and human authority. Possessing a tool does not authorize its use, and authorization does not prove that the required tool is available.

## Basic coordination requirements

An agent must truthfully declare whether it can:

- read the authoritative repository and identify its exact owner and name;
- read complete UTF-8 coordination records;
- validate a commit-pinned identity directory snapshot and update only its own identity file;
- preserve append-only history;
- perform latest-blob-SHA compare-and-swap writes;
- update only its own cursors and, when the approved mode requires one, its own session lease;
- distinguish connector access from a local executable checkout;
- report its operating limits without exposing secrets or unnecessary machine details.

An agent lacking repository write or latest-SHA support may orient and report, but remains read-only. An agent lacking an executable checkout may perform labelled static inspection, but may not claim that the supplied validator or tests ran.

Presence is mode-dependent. When the human is working with one agent directly and coordination polling is off, preserving NOBODY without creating a lease is correct. Agents do not create leases, polling, or synthetic activity merely to prove capability.

## Project-specific expansion

Each route may require capabilities beyond the coordination minimum. Examples include a particular operating system, product-repository access, local builds, test hardware, browser automation, scheduled polling, artifact inspection, or external notification.

Record required capabilities in the project's STATUS or an explicit decision. The agent records verified capabilities and limits in its own role profile. A project requirement does not grant permission: the human authority boundary must separately authorize the affected action.

## Capability-gap report

When an assigned operation needs a missing or unverified capability, the agent stops that operation and reports:

1. the requested operation and affected route;
2. the exact missing or unverified capability;
3. evidence, including the attempted command and exact error, or a statement that no command was attempted and why;
4. what remains safely possible;
5. at least one mitigation or alternative, with its tradeoff;
6. the specific human decision or authorization needed.

Suitable alternatives may include providing a local checkout, assigning a capable agent, narrowing the task to static review, exporting an artifact for another environment, or explicitly approving a connector-only coordination write. Never describe a weaker substitute as equivalent verification.

The human chooses whether to add capability, reassign the operation, accept a narrower result, approve a bounded fallback, or stop. Agents do not expand their own permissions, alter another role's profile, or silently bypass a requirement.

## On-demand audit

When asked, the agent performs the evidence-based [Capability Audit](Capability-Audit.md). It reports a scored Basic LMTR section, a separately scored Current Project section, limiting factors, mitigation suggestions, and the human decisions required. The score measures readiness for the named route and operation; it is not authority and is not transferable to another project or environment.
