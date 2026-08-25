# Installation Guide

LikeMinds is an internal coordination system installed in the **private repository of the project being coordinated**. Do not use the public template repository itself, or a separate public copy of it, for real coordination.

## Before you begin

You need a GitHub account that can create a private repository, Python 3 for local validation, and either permission to edit the repository yourself or an authorized Codex agent with GitHub access.

## Choose the project repository

### Path 1: add LikeMinds to an existing private project

Keep the existing project repository as the authority. Copy the framework-managed files listed in `updates/managed-files.json` into it without overwriting product files or any existing LikeMinds operational records. Then continue with configuration below. An authorized agent may perform this installation after confirming the exact repository, visibility, collisions, and proposed changes.

### Path 2: create a new private project with LikeMinds installed

Use GitHub's **Use this template** action on `crseabrk/LikeMinds-Template`. Create the new project repository under your account or organization and select **Private** visibility. This repository is the project repository, not a separate coordination-only copy. Add the project's code and assets alongside the framework after initialization.

Creating a public repository from the template is suitable only for a deliberately sanitized demonstration, not an operational project.

## Manual initialization

### 1. Configure installation metadata

Copy `installation.example.yml` to `installation.yml`. Replace `OWNER/REPOSITORY` with the actual private repository name. Review the routing paths, LMTR manifest, collaboration defaults, update channel, and capability declarations. Do not put tokens or machine secrets in this file.

### 2. Create operational records

Copy, without overwriting existing files:

- `templates/ROUTING.md` to `ROUTING.md`;
- `templates/system/` to `system/`;
- `templates/project/` to `projects/<project-slug>/` when adding a project.

Keep records empty until you deliberately initialize roles, routes, and projects. Never copy another installation's CHAT, SIGNALS, cursors, or role registry.

### 3. Register the first role

In `system/AGENTS.md`, add one unique stable role for the first authorized agent and record only verified capabilities. Use the [Agent Capabilities](Agent-Capabilities.md) contract to distinguish repository access, latest-SHA writes, local checkout, command execution, Python, and polling. Initialize only that role's cursors. Leave `system/PRESENCE.json` at NOBODY before a session starts.

### 4. Validate

```sh
python3 tools/lmtr.py validate
python3 tools/lmtr.py plan
python3 tools/lmtr.py presence
python3 tests/test_lmtr.py
python3 tools/validate.py
```

Do not continue if a command fails. Consult [Troubleshooting](Troubleshooting.md) or ask an authorized agent to diagnose the exact error.

### 5. Add the project route

Choose a lowercase project slug, create `projects/<slug>/` from `templates/project/`, and add the route to `ROUTING.md`. Record this repository and the project's purpose in STATUS without copying secrets or unnecessary product data.

### 6. Choose coordination mode

Start with [sequential signalling](Coordination-Modes.md). Enable recurring polling only after explicitly approving its repository, role, interval, and authority boundary.

## Agent-assisted installation

### 1. Select the target

Choose either an existing private project repository or a new private project repository created from `crseabrk/LikeMinds-Template`. Do not create a separate public coordination repository.

### 2. Authorize access

Give your Codex agent access through a supported signed-in GitHub connection. Confirm it identifies the exact owner and repository.

### 3. Give one instruction

> Install or initialize LikeMinds inside the private project repository OWNER/REPOSITORY and follow BOOTSTRAP.md completely. Preserve existing product files. Create the project route for PROJECT-SLUG. Do not create recurring polling until you show me the interval, repository, role, and authority boundary and I approve them.

`BOOTSTRAP.md` is written for the agent. It validates LMTR, detects repository state, and follows INITIALIZE, JOIN, RESUME, or RECOVER.

### 4. Review the result

The agent should report the repository and visibility, installed version, validation results, stable role and capabilities, active routes, presence state, changed files, proposed automation, and remaining human decisions.

Review these before authorizing polling, product work, publication, access changes, or external communication.

## Adding another agent later

Give the new authorized agent the private repository address and tell it to follow `BOOTSTRAP.md`. Existing installation state selects JOIN. The newcomer remains read-only until acknowledgements activate its unique role.
