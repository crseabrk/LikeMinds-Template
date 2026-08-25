# Coordination Modes

LikeMinds does not require continuous polling. Choose the least expensive mode that meets the project's latency needs.

## Sequential signalling — default

Human-directed sequential signalling is the normal low-cost mode:

1. Agent A records a durable handoff and stops.
2. The human asks Agent B to inspect LikeMinds.
3. Agent B reads, responds, records the result, and stops.
4. The human decides who acts next.

This preserves routing, decisions, signals, and audit history without spending usage on idle wakes. Its tradeoff is higher latency and greater human involvement.

## Heartbeat synchronization — intensive mode

Recurring heartbeats wake an agent task on every interval and can consume materially more usage. Enable them only with visible human approval and only for short intensive windows such as:

- active multi-agent implementation;
- release preparation;
- merge or conflict resolution;
- time-sensitive handoffs;
- onboarding and recovery tests.

Start at three minutes for normal active coordination. Temporarily use 30–60 seconds only when rapid exchanges justify the cost. Back off after unchanged polls, and automatically slow or stop when the handoff, join, recovery, or release window completes.

Each session owns only its own heartbeat. It never edits or stops another session's automation. TEAM may poll; SOLO stops coordination polling and works with the human; NOBODY has no polling.

## Tradeoffs

| Mode | Latency | Usage | Freshness | Human involvement |
|---|---:|---:|---:|---:|
| Sequential | Higher | Lowest | On demand | Highest |
| 3-minute heartbeat | Low | Moderate | Current | Low |
| 30–60 second heartbeat | Lowest | Highest | Near-real-time | Lowest |

## Release-window example

The human approves a 60-second TEAM heartbeat for two agents. Each renews its own presence lease, processes at most one eligible signal per wake, and backs off after unchanged polls. When validation and handoff complete, both record results; the remaining agent recomputes SOLO and stops its own heartbeat.
