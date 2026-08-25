# Start Here

LikeMinds has separate starting paths for humans and agents.

## I am setting up LikeMinds

Read the human [Installation Guide](docs/wiki/Installation.md). It explains how to create a new private repository and offers two supported choices:

1. **Manual installation** — copy and configure the required files yourself, run validation, and initialize the first role.
2. **Agent-assisted installation** — create the private repository, authorize a Codex agent to access it, and tell that agent to follow `BOOTSTRAP.md`.

You remain in control of repository visibility, agent access, polling, licensing, releases, and every product or external action.

## I am an authorized setup agent

Follow [BOOTSTRAP.md](BOOTSTRAP.md) completely. It is the agent dispatcher for INITIALIZE, JOIN, RESUME, and RECOVER. Do not use it as evidence of authority beyond the human's current request.

## I am adding an agent to an existing installation

Give the new authorized agent the private repository address and tell it:

> Go to OWNER/REPOSITORY and follow BOOTSTRAP.md completely.

The agent detects the existing installation and enters JOIN. [ONBOARDING.md](ONBOARDING.md), [JOINING.md](JOINING.md), and [JOIN-CHECKLIST.md](JOIN-CHECKLIST.md) describe the full acknowledgement process.

## Safety

Use a private repository for operational coordination. Never store credentials, signed download URLs, personal information, secrets, or private operational logs in the public template.
