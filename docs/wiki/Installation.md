# Installation Guide

LikeMinds operational records should normally live in a new **private** GitHub repository. Do not use the public template repository itself for real coordination.

## Before you begin

You need a GitHub account that can create a private repository, Python 3 for local validation, and either permission to edit the repository yourself or an authorized Codex agent with GitHub access.

## Option A: install manually

### 1. Create the repository

Use GitHub's **Use this template** action on `crseabrk/LikeMinds-Template`. Create a new repository under your account or organization and select **Private** visibility.

### 2. Configure installation metadata

Copy `installation.example.yml` to `installation.yml`. Replace `OWNER/REPOSITORY` with the actual private repository name. Review the routing paths, LMTR manifest, collaboration defaults, update channel, and capability declarations. Do not put tokens or machine secrets in this file.

### 3. Create operational records

Copy, without overwriting existing files:

- `templates/ROUTING.md` to `ROUTING.md`;
- `templates/system/` to `system/`;
- `templates/project/` to `projects/<project-slug>/` when adding a project.

Keep records empty until you deliberately initialize roles, routes, and projects. Never copy another installation's CHAT, SIGNALS, cursors, or role registry.

### 4. Register the first role

In `system/AGENTS.md`, add one unique stable role for the first authorized agent and record only verified capabilities. Use the [Agent Capabilities](Agent-Capabilities.md) contract to distinguish repository access, latest-SHA writes, local checkout, command execution, Python, and polling. Initialize only that role's cursors. Leave `system/PRESENCE.json` at NOBODY before a session starts.

### 5. Validate

```sh
python3 tools/lmtr.py validate
python3 tools/lmtr.py plan
python3 tools/lmtr.py presence
python3 tests/test_lmtr.py
python3 tools/validate.py
```

Do not continue if a command fails. Consult [Troubleshooting](Troubleshooting.md) or ask an authorized agent to diagnose the exact error.

### 6. Add the first project

Choose a lowercase project slug, create `projects/<slug>/` from `templates/project/`, and add the route to `ROUTING.md`. Record the product repository and purpose in STATUS without copying secrets or internal product data.

### 7. Choose coordination mode

Start with [sequential signalling](Coordination-Modes.md). Enable recurring polling only after explicitly approving its repository, role, interval, and authority boundary.

## Option B: use an authorized Codex agent

### 1. Create the repository

Create a new private repository from `crseabrk/LikeMinds-Template`.

### 2. Authorize access

Give your Codex agent access through a supported signed-in GitHub connection. Confirm it identifies the exact owner and repository.

### 3. Give one instruction

> Go to OWNER/REPOSITORY and follow BOOTSTRAP.md completely. Initialize this as a private LikeMinds installation. Do not create recurring polling until you show me the interval, repository, role, and authority boundary and I approve them.

`BOOTSTRAP.md` is written for the agent. It validates LMTR, detects repository state, and follows INITIALIZE, JOIN, RESUME, or RECOVER.

### 4. Review the result

The agent should report the repository and visibility, installed version, validation results, stable role and capabilities, active routes, presence state, changed files, proposed automation, and remaining human decisions.

Review these before authorizing polling, product work, publication, access changes, or external communication.

## Adding another agent later

Give the new authorized agent the private repository address and tell it to follow `BOOTSTRAP.md`. Existing installation state selects JOIN. The newcomer remains read-only until acknowledgements activate its unique role.
