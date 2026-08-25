# Changelog

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

## Unreleased

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
