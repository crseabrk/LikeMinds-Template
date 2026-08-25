# Start Here

LikeMinds has separate starting paths for humans and agents.

## I am setting up LikeMinds

Read the human [Installation Guide](docs/wiki/Installation.md). Choose where the actual project will live:

1. **Existing private project** — install LikeMinds into that repository without overwriting product files.
2. **New private project** — create the project repository from this template, then initialize both the project route and its internal LikeMinds records.

Either path may be completed manually or delegated to an authorized Codex agent. LikeMinds is part of the project repository; creating a separate public copy of the template is not an installation.

You remain in control of repository visibility, agent access, polling, licensing, releases, and every product or external action.

## I am an authorized setup agent

Follow [BOOTSTRAP.md](BOOTSTRAP.md) completely. It is the agent dispatcher for INITIALIZE, JOIN, RESUME, and RECOVER. Do not use it as evidence of authority beyond the human's current request.

## I am adding an agent to an existing installation

Give the new authorized agent the private repository address and tell it:

> Go to OWNER/REPOSITORY and follow BOOTSTRAP.md completely.

The agent detects the existing installation and enters JOIN. [ONBOARDING.md](ONBOARDING.md), [JOINING.md](JOINING.md), and [JOIN-CHECKLIST.md](JOIN-CHECKLIST.md) describe the full acknowledgement process.

## Safety

Use a private repository for operational coordination. Never store credentials, signed download URLs, personal information, secrets, or private operational logs in the public template.
