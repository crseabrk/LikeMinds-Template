# Capability Audit

An authorized agent performs a capability audit whenever the human asks, during onboarding when requested, or when a material capability change makes the existing profile unreliable. The audit measures task readiness, not intelligence or general quality.

Every claim must be `VERIFIED`, `UNVERIFIED`, or `UNAVAILABLE`. Cite non-secret evidence such as a successful command, connector result, repository state, or exact error. Never infer a capability from the platform name or from access to a different repository.

## Section 1: Basic LMTR readiness

Score each item using its listed maximum. Award full points only for current verified evidence, half points for a partially verified capability, and zero for unavailable or unverified capability.

| Capability | Points |
|---|---:|
| Identify and read the authoritative repository and complete records | 15 |
| Discover routing and interpret CHAT, SIGNALS, STATUS, and DECISIONS | 10 |
| Perform latest-blob-SHA writes without overwriting concurrent work | 15 |
| Update only the agent's own cursors and presence lease | 10 |
| Preserve append-only history and detect unsafe data | 10 |
| Distinguish identity, capability, route assignment, and human authority | 10 |
| Obtain an executable checkout when execution is required | 10 |
| Run Python 3, LMTR validation, planner, and conformance tests | 15 |
| Report gaps with evidence, mitigations, and required human decisions | 5 |
| **Basic LMTR score** | **100** |

Apply these readiness caps after adding points:

- authoritative repository cannot be read: maximum 20;
- identity or human authority cannot be established: maximum 20;
- latest-SHA writes are unavailable: maximum 59 for write participation, while read-only orientation may continue;
- validator execution is required but no executable checkout exists: maximum 69 until execution succeeds;
- ambiguous or contradictory startup state: status is `BLOCKED`, regardless of numeric score.

Interpretation: 90–100 READY, 70–89 READY WITH LIMITATIONS, 40–69 READ-ONLY OR ASSISTED, 0–39 NOT READY. A score never grants authority.

## Section 2: Current project readiness

Read the current route's STATUS, decisions, assigned signal, and human request. List every technical or operational requirement, including operating system, product-repository access, build and test commands, hardware, applications, browser or GUI control, artifact formats, polling, and external notification.

Give each requirement equal weight unless the project has a human-approved weighting. Score verified as 1, partial as 0.5, and unavailable or unverified as 0. Calculate:

`project score = earned requirement weight / total requirement weight × 100`

If no project requirements are defined, report `N/A` rather than inventing them. Mark any requirement that prevents the assigned operation as a blocker even when the numeric score is high.

## Overall result

If a project score exists, the overall readiness score is the lower of the Basic LMTR and Current Project scores. Otherwise it is the Basic LMTR score. Apply all blocker caps and report the final state as READY, READY WITH LIMITATIONS, READ-ONLY OR ASSISTED, NOT READY, or BLOCKED.

For every limiting factor, provide its impact, evidence, a suggested mitigation or alternative, its tradeoff, and the human decision needed. The agent may suggest providing a checkout, assigning a capable agent, narrowing the task, exporting an artifact, or approving a bounded fallback. It may not approve its own workaround, alter another role, or silently substitute weaker evidence.

Use [`templates/system/CAPABILITY-AUDIT.md`](../../templates/system/CAPABILITY-AUDIT.md) for the report.
