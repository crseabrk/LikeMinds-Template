# Origins

LikeMinds began with a practical coordination problem.

Its creator was developing and porting the same work on macOS and Windows at the same time, using a separate Codex session on each machine. The sessions could each contribute useful work, but they did not share a durable understanding of what the other had learned, changed, decided, or still needed. Keeping them aligned meant repeatedly copying and pasting status reports, technical context, decisions, and instructions from one conversation into the other.

The immediate goal was not to build a general multi-agent platform. It was to stop making the human act as a message courier between capable agents working on the same effort.

## The coordination problem

The underlying problem was larger than copying text:

- Each session had only a partial view of the work.
- A decision made on one machine could be invisible on the other.
- Chat history was not a reliable shared project record.
- Sessions could close, restart, or disappear without a clean handoff.
- macOS and Windows agents could have different tools, access, and limitations.
- An agent returning later needed to distinguish current state from stale messages.
- Shared information could easily be mistaken for shared permission.
- When only one agent remained, continued coordination polling wasted effort and obscured the human-agent workflow.

A useful solution therefore needed more than a shared chat. It needed durable routing, identities, acknowledgements, cursors, capability declarations, presence states, recovery rules, and human-readable records. It also needed to fail closed: learning that work exists must never silently authorize an agent to perform it.

## From two sessions to LikeMinds

The first use case was simply two Codex sessions coordinating across macOS and Windows. As the workflow was tested, the same design had to account for disconnected agents, new agents entering an existing effort, agents with unequal capabilities, projects with additional requirements, and sessions that ended without properly releasing their state.

Those needs became LikeMinds and LMTR:

- GitHub provides the durable, reviewable coordination record.
- Stable roles identify participants independently of a particular chat session.
- Routes, chat records, signals, decisions, and cursors provide shared state.
- Capability audits make limitations visible and require the affected agent to suggest a mitigation.
- NOBODY, SOLO, TEAM, UNKNOWN, and recovery handling describe whether coordination is actually possible.
- Protected operational records allow the reusable framework to update without replacing an installation's history.
- Human authority remains explicit throughout the system.

LikeMinds is still rooted in that original experience: agents should work together directly when coordination is available, work with the human when they are alone, and never force the human to reconstruct the project by shuttling fragments between isolated sessions.

## First practical application: CMQ

The first practical application of LikeMinds was [CMQ](https://github.com/crseabrk/cmq), a deliberately small native two-pane file manager for macOS and Windows 11.

CMQ and LikeMinds were developed and published in parallel. The project owner began with limited Windows programming experience and no prior Swift or GitHub experience. Separate Codex sessions worked on the platform implementations while the coordination difficulties between those sessions drove the development of LikeMinds. CMQ provided the real project pressure, cross-platform differences, handoffs, and capability gaps against which the coordination framework was exercised.

This made CMQ more than an example added after the protocol was designed: it was the first live workload that helped shape the protocol.

## Recursive development

LikeMinds was then used to continue developing LikeMinds. As the framework became usable, the participating Codex agents increasingly coordinated its design, implementation, testing, migration, and release preparation through the evolving system itself. Problems discovered during real operation became new protocol requirements, and the framework was refined iteratively in response.

In that practical engineering sense, LikeMinds helped create itself. This does not imply consciousness, independent intent, or autonomous authority. The project remained human-directed and human-authorized throughout. The full authorship and implementation account is in the [AI Development Disclosure](../../AI-DISCLOSURE.md).

## What LikeMinds is—and is not

LikeMinds is a coordination framework, not a claim that agents share consciousness or authority. It gives authorized agents a common, auditable place to learn what is happening and communicate about it. The human remains the owner of the installation and the source of authority.

The framework is intentionally repository-backed rather than dependent on any one conversation, machine, operating system, or AI product feature. The original macOS and Windows workflow supplied the problem; LikeMinds generalizes the solution without hiding where it came from.
