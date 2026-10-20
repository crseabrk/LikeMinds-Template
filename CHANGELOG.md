# Changelog

## 0.1.6-alpha.1 — 2026-10-20

- Add evidence-based stale-project and idle-agent reports with configurable 30/7-day defaults, unknown-evidence handling, polling exclusion and explicit reactivation.
- Filter bootstrap availability through effective activity without changing durable membership, route declarations, cursors, claims or other agents' automations.
- Add fingerprint-checked reconciliation snapshots, append-only activity recording, tests and migration/rollback documentation. Run CI on Linux, macOS and Windows.
- Include the previously upstream identity-discovery changes below; legacy installation data remains protected until separately migrated.
- Update installation validation to run inactivity and structural checks; include existing Origins/AI-disclosure docs in the managed manifest so installed links resolve.
- Implemented with OpenAI Codex assistance. This source version is not a claim that a GitHub release or tag was published.

### Previously unreleased identity work

- Add one-file-per-agent identity discovery with immutable IDs, unique display names, preserved aliases, and dependency-free validation.
- Replace peer-to-peer introductions and all-participant join acknowledgements with commit-pinned directory snapshots and bounded admission roles for requested routes.
- Add explicit migration and rollback rules so existing installations never silently mix quorum models.

## 0.1.5-alpha.2

- Add a human-approved connector-only initialization path for agents without an authenticated executable checkout.
- Require static inspection, latest-SHA writes, remote commit verification, deferred-validation records, and later validation by a checkout-capable agent.

## 0.1.5-alpha.1

- Publish the first experimental LikeMinds alpha under Apache-2.0.
- Include LMTR startup and presence policy, managed installation updates, human-first installation documentation, capability audits, sequential coordination, and disconnected recovery behavior.

## 0.1.5-draft

- Isolate updater integration fixtures from live installation projects, system records, routing, and installation metadata.

## 0.1.4-draft

- Allow installations to acknowledge specific preserved historical duplicate message IDs without weakening checks for new duplicates.
- Protect installation-specific `.likeminds/` metadata from upstream managed files.

## 0.1.3-draft

- Require the managed-file manifest to contain every structurally required framework file.
- Include `tools/validate.py` so installed workflows can execute structural validation.

## 0.1.2-draft

- Add explicit managed-file updates for independent template installations.
- Protect operational records and installation policy from framework updates.
- Add adoption, planning, conflict detection, backups, validation, rollback, and installed-source tracking.
- Document a human-approved connector-only update path with static-validation limits.

## Earlier unreleased work

- Added a formal multi-agent joining handshake.
- Added stable-role membership states and capability registration.
- Added acknowledgement, role-collision, cursor initialization, replacement, and blocked-join rules.
- Added an empty operational agent registry template.
- Added a human-authorized solo-continuation path for late specialists working from completed project history.

## 0.1.0-draft — 2026-08-24

- Initial sanitized technical scaffold.
- Core routing, signals, cursors, recovery, and acknowledged-move protocol.
- Name-independent installation metadata.
- Extension and capability declaration groundwork.
- Empty operational templates and validation foundation.

No public release has been published.

Inactivity-aware admission now excludes stale approvers in both legacy and directory mode, with audited owner-invited recovery when no current approver remains.
