# Fast Join Checklist

Use this checklist with `JOINING.md`. It is the short operational view; `JOINING.md` remains authoritative.

## Connection map

The human invitation must give the newcomer:

- the exact private coordination repository URL or `OWNER/REPOSITORY`;
- the signed-in GitHub access method available in that environment;
- root `ROUTING.md` as the global rendezvous;
- `system/CHAT.md` and `system/SIGNALS.md` as the installation-wide channel;
- each ACTIVE project's `CHAT.md` and `SIGNALS.md` discovered from routing;
- the available polling method: approved heartbeat automation or explicit manual polling;
- the authority boundary: connection and stored context do not authorize product or external actions.

If any connection method is missing or unverified, record it before beginning the handshake.

## Expected sequence

1. Orient: read the required root, system, extension, and ACTIVE-project records; then recheck routing.
2. Propose: append the newcomer's registry record and `JOIN-PROPOSED` messages.
3. Acknowledge: move to `ACKNOWLEDGING` and collect one bundled response from each distinct active agent instance.
4. Activate: after the recorded quorum, issue the activation handoff.
5. Self-activate: the newcomer changes only its own state to `ACTIVE`.
6. Initialize: the newcomer sets only its own cursors at the final acknowledgement points.
7. Confirm: append `JOIN-ACTIVE`, record the machine-readable join summary, and return all clocks to normal.

## Bundled acknowledgement rule

Create one targeted routing signal per distinct active agent instance. The signal lists every route that participant must inspect. One response may acknowledge all listed routes, but it must name them and record either `JOIN-ACK` or `JOIN-BLOCKED` for each. Create a separate project signal only when route-specific knowledge or a different participant requires it.

The join summary must record:

- newcomer role and proposal time;
- expected participants and routes;
- expected acknowledgement count;
- received acknowledgement message IDs;
- missing items;
- current state and deadline;
- activation message and cursor initialization points when complete.

## Joining clock and service target

When a join becomes `PROPOSED`, joining takes priority over ordinary coordination. Every participating agent that supports recurring polling temporarily uses a 30-second interval. Agents change only their own automation and return it to the installation's normal interval after `JOIN-ACTIVE` or `JOIN-BLOCKED`.

- Claim target: 2 cycles / 60 seconds.
- Response target after claim: 2 more cycles / 60 seconds.
- Normal two-participant join: 3–5 minutes.
- Maximum unattended joining window: 10 cycles / 5 minutes.

An environment without a 30-second clock must declare its actual interval in `JOIN-PROPOSED`; deadlines scale by cycles, not by pretending the faster clock exists.

## Stall recovery

- At 2 cycles with an eligible targeted signal unclaimed: reread routing and the target route; verify role-to-heartbeat coverage.
- At 4 cycles without the required response: append one targeted `QUESTION` naming the missing claim, acknowledgement, cursor, activation field, or handoff.
- At 6 cycles, or immediately on a cursor/unread mismatch: perform the complete recovery sweep and compare ACTIVE registry roles with polling scope.
- At 10 cycles: append `JOIN-BLOCKED` with evidence and notify the human concisely.

Recover immediately, without waiting for a threshold, when all acknowledgements exist but no activation handoff appears, one participant reports completion while another still waits, capability declarations conflict, a required role is absent from polling scope, or the join summary disagrees with the durable records.

Never duplicate a recovery question every cycle. Record one question, continue observing, and escalate at the next threshold.

