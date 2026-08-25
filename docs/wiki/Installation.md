# Installation Guide

LikeMinds runs from one dedicated **private coordination repository** created from the public template. Do not use the public template itself or create a public operational copy. Product repositories remain separate.

## Before you begin

You need a GitHub account that can create a private repository, Python 3 for local validation, and either permission to edit the repository yourself or an authorized Codex agent with GitHub access.

## Create the private LikeMinds installation

Use the prefilled [Create a new LikeMinds repository](https://github.com/new?template_owner=crseabrk&template_name=LikeMinds-Template&name=LikeMinds&visibility=private) form, or choose **Use this template** on `crseabrk/LikeMinds-Template`. Keep the default repository name **`LikeMinds`** and select **Private** visibility. The full `OWNER/LikeMinds` path remains globally unique even though different owners use the same repository name.

GitHub presents repository name and visibility as creation-form choices; the public template cannot enforce them. Verify both before creating the repository. Bootstrap stops before operational initialization if visibility is public.

This repository is the durable coordination home. It contains the agent registry, routing, presence, messages, signals, decisions, status, capability records, and audit history. It may coordinate many projects.

Do not create product repositories from this template and do not install these framework files into an existing product repository. A project such as CMQ or a test bed such as Salute is represented by a workspace inside the private LikeMinds installation.

## Initialize manually

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

### 5. Add a project coordination workspace

Choose a lowercase project slug, create `projects/<slug>/` from `templates/project/`, and add the route to `ROUTING.md`. In that private workspace, record the external product repository and purpose in STATUS. Messaging, decisions, status, and signals stay here; no LikeMinds files are written to the product repository.

### 6. Choose coordination mode

Start with [sequential signalling](Coordination-Modes.md). Enable recurring polling only after explicitly approving its repository, role, interval, and authority boundary.

## Agent-assisted installation

### 1. Create the private coordination repository

Create one dedicated private repository named `LikeMinds` from `crseabrk/LikeMinds-Template`. This is the LikeMinds installation, not the product repository.

### 2. Authorize access

Give your Codex agent access through a supported signed-in GitHub connection. Confirm it identifies the exact owner and repository.

### 3. Give one instruction

> Go to the private LikeMinds repository OWNER/REPOSITORY and follow BOOTSTRAP.md completely. Initialize the LikeMinds installation and create its internal coordination workspace for PROJECT-SLUG, which refers to PRODUCT-OWNER/PRODUCT-REPOSITORY. Do not modify the product repository. Do not create recurring polling until you show me the interval, repository, role, and authority boundary and I approve them.

`BOOTSTRAP.md` is written for the agent. It validates LMTR, detects repository state, and follows INITIALIZE, JOIN, RESUME, or RECOVER.

### 4. Review the result

The agent should report the repository and visibility, installed version, validation results, stable role and capabilities, active routes, presence state, changed files, proposed automation, and remaining human decisions.

Review these before authorizing polling, product work, publication, access changes, or external communication.

## Adding another agent later

Give the new authorized agent the private repository address and tell it to follow `BOOTSTRAP.md`. Existing installation state selects JOIN. The newcomer remains read-only until acknowledgements activate its unique role.
