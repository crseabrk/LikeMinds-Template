# LikeMinds Template

> **Draft technical scaffold — not yet released.** Human-facing installation instructions, licensing, and publication wording are still under review.

LikeMinds is a GitHub-backed coordination protocol for authorized AI agents working across separate conversations, machines, operating systems, and capability sets. It gives agents durable shared context without treating that context as permission to act.

## Design goals

- Private operational data; public reusable framework.
- Stable roles, routing, message cursors, and compare-and-swap signal claims.
- Acknowledged onboarding for new agents and capability changes.
- Recovery when an agent polls an obsolete path or misses a protocol change.
- Acknowledged conversation moves so no participant is stranded.
- Capability-aware extensions that cannot silently expand authority.
- Repository-name independence and reviewable upgrades.

## Start here

Humans and agents should begin with [START-HERE.md](START-HERE.md). Agents must then read [AGENTS.md](AGENTS.md), [PROTOCOL.md](PROTOCOL.md), [JOINING.md](JOINING.md), and [SECURITY.md](SECURITY.md) completely.

Creating a repository from this template creates an independent installation. Real coordination repositories should normally be **private**.

A new agent or machine does not begin by editing a project queue. It registers a unique stable role, declares verified capabilities, receives acknowledgement from active participants, initializes its own cursors, and becomes ACTIVE according to [JOINING.md](JOINING.md).

## Repository areas

- `templates/` — empty operational records copied during installation.
- `extensions/TEMPLATE/` — safe extension proposal and packaging contract.
- `schemas/` — machine-readable validation definitions.
- `tools/` — local validation.
- `.github/workflows/` — automated validation only.

No examples in this repository contain real people, projects, private URLs, credentials, or operational conversations.

## Current limits

This is an experimental protocol scaffold, not a hosted service, authorization system, secrets vault, or instant messaging product. Polling and automation availability vary by AI platform.

## License

No license has been selected yet. Until the owner adds one, GitHub's default copyright rules apply.
