# LikeMinds Template

> **Release candidate.** LMTR 0.1 and the human wiki are ready for cross-platform launch validation. Licensing and the final release action remain owner decisions.

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

To create an installation, begin with [BOOTSTRAP.md](BOOTSTRAP.md). To add an agent to an existing installation, point it to [ONBOARDING.md](ONBOARDING.md). Humans and agents may also consult [START-HERE.md](START-HERE.md). Agents must then read [AGENTS.md](AGENTS.md), [PROTOCOL.md](PROTOCOL.md), [JOINING.md](JOINING.md), [JOIN-CHECKLIST.md](JOIN-CHECKLIST.md), and [SECURITY.md](SECURITY.md) completely.

Creating a repository from this template creates an independent installation. Real coordination repositories should normally be **private**.

A new agent or machine does not begin by editing a project queue. It registers a unique stable role, declares verified capabilities, receives acknowledgement from active participants, initializes its own cursors, and becomes ACTIVE according to [JOINING.md](JOINING.md).

LMTR is the fail-closed startup policy layer. Validate it with `python3 tools/lmtr.py validate` and inspect the selected startup state with `python3 tools/lmtr.py plan`. Human documentation starts at [docs/wiki/Home.md](docs/wiki/Home.md).

## Repository areas

- `templates/` — empty operational records copied during installation.
- `extensions/TEMPLATE/` — safe extension proposal and packaging contract.
- `schemas/` — machine-readable validation definitions.
- `tools/` — local validation.
- `.github/workflows/` — automated validation only.
- `lmtr/` — ordered declarative startup and coordination policy.
- `docs/wiki/` — human quick start, coordination modes, LMTR reference, security, migration, troubleshooting, and launch guidance.

No examples in this repository contain real people, projects, private URLs, credentials, or operational conversations.

## Current limits

This is an experimental protocol scaffold, not a hosted service, authorization system, secrets vault, or instant messaging product. Polling and automation availability vary by AI platform.

## License

No license has been selected yet. Until the owner adds one, GitHub's default copyright rules apply.
