# LikeMinds Template

> **Alpha release.** LikeMinds `v0.1.5-alpha.1` is ready for experimental installations and feedback. LMTR remains an evolving coordination protocol; use private repositories for operational records.

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

Humans should begin with [START-HERE.md](START-HERE.md) and the human [Installation Guide](docs/wiki/Installation.md). LikeMinds is installed inside the private project repository that the agents will work on. The guide supports adding it to an existing project or creating a new private project repository with LikeMinds already present.

Authorized agents use [BOOTSTRAP.md](BOOTSTRAP.md) as their state-aware dispatcher. New agents joining an existing installation also follow [ONBOARDING.md](ONBOARDING.md), [JOINING.md](JOINING.md), and [JOIN-CHECKLIST.md](JOIN-CHECKLIST.md).

Do not create a public project from this template for operational use. Either install the framework into an existing **private project repository**, or use this template to create the new **private project repository itself** and initialize the project and its internal coordination records together.

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

Licensed under the [Apache License 2.0](LICENSE).
