# Project staleness and agent inactivity

## Design and state model

LikeMinds distinguishes **membership** (admitted identity), **presence** (a short session lease), and **activity** (dated work or coordination evidence). An old ACTIVE registry row must not make a disconnected agent appear available forever. Polling must not keep an otherwise idle agent alive.

`tools/activity.py` computes a reversible effective state. Defaults are seven days for agents and thirty days for projects; the boundary is inclusive. Configure integer values from 1 to 3650 days in `system/ACTIVITY.json`'s `policy`. These are conservative defaults, not a claim that every project needs daily activity.

| Declared state | Evidence | Effective result |
|---|---|---|
| Agent ACTIVE | Valid activity younger than threshold | ACTIVE |
| Agent ACTIVE | At or beyond idle threshold | INACTIVE |
| Project ACTIVE | At or beyond stale threshold | STALE |
| Either ACTIVE | No timestamp, malformed or future timestamp | UNKNOWN; recover, do not guess |
| PAUSED, FINISHED, RETIRED, BLOCKED, joining states | Any age | Preserve declared state; never auto-reopen or auto-admit |

**INACTIVE is not RETIRED.** Identity ownership, membership, roles, cursors, project history, existing signal claims, and scheduled tasks are never changed by this tool. Projects are not archived or deleted. No peer's identity record is rewritten. The computed availability is authoritative for claim eligibility: an inactive agent cannot claim new work, and a stale project needs explicit renewed attention before new work is claimed. Existing claims need a documented recovery handoff, never silent reassignment.

## Evidence and limitations

- Sharded installations use immutable identity IDs and their `updated_at` as a conservative lower bound; dated authored CHAT messages and explicit activity events can advance it. An identity update can postpone inactivity even if it is maintenance rather than product work.
- Legacy installations use exact role names from registry tables/sections, the last-confirmed/join dates, and matching CHAT authors. A trailing parenthesized nickname is accepted; ambiguous role mappings are not invented. Unmapped legacy authors do not renew an agent.
- Projects use dated CHAT entries for their routed project slug plus explicit project events. A newly prepared route without activity is UNKNOWN if ACTIVE; non-ACTIVE routes remain as declared.
- `Type: POLL`, `Type: HEARTBEAT`, or `Activity: POLL` messages are ignored. Presence heartbeats, file modification times, cursor edits and repeated report generation do not renew activity. Older unlabeled STATUS messages cannot reliably be distinguished from progress; label future polling explicitly or avoid logging idle polls.
- Dates include timezone offsets. Historical date-only registry entries are interpreted conservatively through the end of the UTC day. Future timestamps or malformed evidence make an ACTIVE subject UNKNOWN, even if another timestamp looks plausible. Correct the evidence through a documented correction/migration, not by guessing.
- Running a job outside LikeMinds is invisible unless it records work. Before an expected long absence, leave a handoff and appropriate route/role state or adjust the policy explicitly. Activity is not a measurement of model thinking time or a surveillance system.

## Commands

From the private installation root:

```sh
python3 tools/activity.py report
python3 tools/lmtr.py activity
python3 tools/lmtr.py plan
```

These commands write nothing. The planner includes effective activity and filters session presence through it. An installation with only stale ACTIVE agents returns RECOVER, not RESUME. This does not grant the next arriving session ownership of an old identity. A live polling lease alone cannot bypass inactivity.

To save an auditable snapshot, copy `input_sha256` from the latest report:

```sh
python3 tools/activity.py reconcile --expect INPUT_SHA256
```

This writes only `system/INACTIVITY.json`, including the thresholds, evaluation time, evidence paths, source fingerprint, declared states and effective states. It is a cache/evidence snapshot: reports and bootstrap recompute current state rather than trusting an old saved result. Preserve prior snapshots in Git history. No automatic scheduler is installed; evaluation occurs on demand and at bootstrap/claim checks. A separately human-authorized heartbeat can run the read-only report.

## Returning to work

After the human requests renewed work, an admitted returning agent proves identity continuity and reads its unread routes. It can append its own dated RESUME event (or a substantive CHAT message), then recheck eligibility:

```sh
python3 tools/activity.py record --expect INPUT_SHA256 \
  --subject-type agent --subject YOUR_AGENT_ID --kind RESUME \
  --summary 'Human requested continuation; unread handoff reviewed'
```

For an ACTIVE but stale project, the authorized assignee can separately record a project RESUME using the route slug. This does not reactivate PAUSED/FINISHED routes, change admission, or authorize a product action. A new agent must join normally. Do not record on behalf of another identity unless the human explicitly directs a documented correction. Allowed event kinds are WORK, HANDOFF, ACK and RESUME; they require a nonempty explanation. Events append to `system/ACTIVITY.json`; they never overwrite prior events.

Example empty ledger (optional; absence uses these defaults):

```json
{"version":1,"policy":{"agent_idle_days":7,"project_stale_days":30},"events":[]}
```

## Concurrency, deployment and recovery

Writes require a fresh fingerprint over registry, routing, identity, presence, CHAT and activity inputs. A changed input rejects the write. A local exclusive lock serializes activity writers; normal Git/connector operations still require a clean synchronized checkout or latest-blob-SHA compare-and-swap. This local lock does not protect against an unrelated process changing files or a remote writer: refetch/recheck before committing, and retry on remote conflicts. Never use a saved fingerprint to force an old decision through.

If a process is interrupted and leaves `.likeminds/activity.lock`, verify no activity command is running before removing that lock; rerun the report. Invalid ledgers, unsafe paths and unknown subjects fail closed. The CLI does not authenticate humans: the current user request and governing instructions remain the authority boundary.

## Installation and verification

The managed updater installs only code, schemas, tests and docs. It never writes protected operational data. Running report requires no identity-directory migration and works with legacy registries. Reconcile is a separate operational step after update review; its only write is the derived snapshot. Tests cover exact boundaries, missing/malformed/future evidence, heartbeat exclusion, conservative legacy and sharded identity handling, history preservation, stale-input rejection, reactivation and startup eligibility.

Implementation was produced with OpenAI Codex assistance. Automated fixtures are not proof of every host's native permissions or scheduling behavior. The CI matrix runs the Python checks on Linux, macOS and Windows.

## Admission must survive absent agents

The same inactivity classification removes stale agents from mandatory joining acknowledgements. Run `python3 tools/activity.py admission --route example` against the current installation. Legacy mode starts with all declared ACTIVE participants; directory mode starts with named system/requested-route admission IDs. Only effective ACTIVE candidates require ACKs; INACTIVE/PAUSED/RETIRED candidates are audited exclusions, while UNKNOWN/missing/ambiguous evidence blocks recovery rather than being silently discarded.

When every candidate is excluded, a current direct owner invitation permits documented owner-invited membership recovery under JOINING.md. No second per-join waiver and no responses from abandoned agents are required. The report itself does not authorize activation. Preserve the invitation reference, orientation/validation, revision/hash, exact exclusions and conflict checks in the join summary, then recompute before a latest-SHA activation write. Returning agents must catch up; they cannot retroactively veto an audited admission. Project STALE/PAUSED/FINISHED and product authorization remain separate.
