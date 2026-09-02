# Quick Start

## Human setup

Begin with the [Installation Guide](Installation.md). You may configure the new private repository manually or delegate initialization to an authorized Codex agent.

For agent-assisted setup, send the agent:

> Go to OWNER/REPOSITORY and follow BOOTSTRAP.md completely.

This is an agent instruction, not the human installation procedure. The same command works for a fresh installation and an existing one. The LMTR planner selects one state:

- **INITIALIZE** creates only missing installation records.
- **JOIN** registers one sharded identity and obtains bounded route-admission acknowledgements.
- **RESUME** continues an existing ACTIVE role from its own cursors.
- **RECOVER** stops ambiguous or incomplete state from being treated as valid.

Active presence has three states: **NOBODY** (zero sessions), **SOLO** (one session, work directly with the human without coordination polling), and **TEAM** (two or more sessions, polling and signals active).

## Verify locally

```sh
python3 tools/lmtr.py validate
python3 tools/lmtr.py plan
python3 tools/lmtr.py presence
python3 tools/lmtr.py directory
python3 tools/validate.py
```

If Python 3 is unavailable, the agent must report that prerequisite instead of claiming validation passed.

## First project

Ask an ACTIVE agent: `Start LikeMinds for <project>`. It creates or joins the matching project route, records its stable role, and proposes a narrowly scoped heartbeat. Product changes remain separately authorized.
