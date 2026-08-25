#!/usr/bin/env python3
"""Fail-closed LMTR 0.1 parser and bootstrap planner."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "lmtr" / "manifest.json"
TOP_LEVEL = {"ruleset", "authority", "policy", "procedure", "default", "unknown", "ambiguous"}
BLOCKS = {"authority", "policy", "procedure", "each"}
WORDS = {
    "ruleset", "authority", "policy", "procedure", "default", "unknown", "ambiguous",
    "allow", "deny", "block", "human", "read", "require", "identify", "unique", "state",
    "mutation", "routes", "discover", "each", "route", "records", "append-only", "living",
    "stored", "find", "latest-sha", "claim", "one", "maximum", "context", "authorized",
    "action", "result", "append", "signal", "terminal", "update", "own-cursor", "other-cursor",
    "unread", "after-read", "advance", "complete", "orientation", "stable-role", "propose",
    "capabilities", "declare", "participants", "acknowledge", "own-role", "own-cursors",
    "initialize", "fresh-template", "create", "missing", "bootstrap-role", "record", "validator",
    "pass", "repository", "inspect", "required", "documents", "verify", "routing", "rediscover",
    "compare", "stale-claims", "ambiguity", "call", "conversation-move", "acknowledged", "history",
    "deletion", "role", "replacement", "installation.yml", "manifest", "order", "modules", "platform",
    "preserve", "later-rule", "narrowing", "coordination", "product-write", "merge", "release",
    "publish", "delete", "access-change", "external-contact", "secrets", "signed-urls", "CHAT",
    "STATUS", "DECISIONS", "SIGNALS", "ROUTING.md", "projects/INDEX.md", "ACTIVE", "JOIN",
    "INITIALIZE", "RECOVER", "RESUME", "fresh-template", "end",
    "TEAM", "SOLO", "NOBODY", "solo", "other-participants", "inactive", "own-heartbeat", "stop",
    "collaboration", "collaboration-state", "direct", "silence", "other-heartbeat", "presence", "leases",
    "expired", "stale", "mark", "unknown", "recompute", "present-agents", "two-minimum", "one", "zero",
    "running", "polling", "expired-lease", "role-retire", "reentry", "lease-renew",
}
PATH_RE = re.compile(r"^[A-Za-z0-9._/-]+$")


@dataclass
class Statement:
    path: str
    line: int
    words: list[str]


class LMTRFailure(Exception):
    pass


def load_manifest() -> dict:
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LMTRFailure(f"LMTR-E001 manifest unreadable: {exc}") from exc
    if data.get("format") != "lmtr-manifest-0.1" or data.get("version") != "0.1.0":
        raise LMTRFailure("LMTR-E002 unsupported manifest format or version")
    modules = data.get("modules")
    if not isinstance(modules, list) or len(modules) != len(set(modules)) or not modules:
        raise LMTRFailure("LMTR-E003 modules must be a non-empty unique ordered list")
    if modules != sorted(modules):
        raise LMTRFailure("LMTR-E004 modules are not visibly ordered")
    return data


def parse_module(path: Path) -> list[Statement]:
    if path.parent.resolve() != (ROOT / "lmtr").resolve() or not PATH_RE.match(path.name):
        raise LMTRFailure(f"LMTR-E005 unsafe module path: {path}")
    if not path.is_file():
        raise LMTRFailure(f"LMTR-E006 missing module: {path.name}")
    statements: list[Statement] = []
    stack: list[str] = []
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        words = line.split()
        if any(word not in WORDS and not PATH_RE.match(word) and not re.match(r"^\d+(\.\d+)*$", word) for word in words):
            raise LMTRFailure(f"LMTR-E007 {path.name}:{number}: unknown token")
        if words[0] == "end":
            if len(words) != 1 or not stack:
                raise LMTRFailure(f"LMTR-E008 {path.name}:{number}: unmatched end")
            stack.pop()
        elif words[0] in BLOCKS:
            if words[0] != "authority" and len(words) != 2:
                raise LMTRFailure(f"LMTR-E009 {path.name}:{number}: block arity")
            if words[0] == "authority" and len(words) != 1:
                raise LMTRFailure(f"LMTR-E009 {path.name}:{number}: block arity")
            stack.append(words[0])
        elif not stack and words[0] not in TOP_LEVEL:
            raise LMTRFailure(f"LMTR-E010 {path.name}:{number}: statement outside top-level block")
        statements.append(Statement(path.name, number, words))
    if stack:
        raise LMTRFailure(f"LMTR-E011 {path.name}: unclosed block {stack[-1]}")
    return statements


def validate() -> list[Statement]:
    manifest = load_manifest()
    statements: list[Statement] = []
    for module in manifest["modules"]:
        statements.extend(parse_module(ROOT / "lmtr" / module))
    corpus = {tuple(item.words) for item in statements}
    required = {
        ("default", "deny"), ("unknown", "deny"), ("ambiguous", "block"),
        ("product-write", "human"), ("other-cursor", "update", "deny"),
        ("latest-sha", "claim", "require"), ("history", "deletion", "deny"),
    }
    missing = sorted(required - corpus)
    if missing:
        raise LMTRFailure(f"LMTR-E012 protected rules missing: {missing}")
    return statements


def reconcile_presence(now: datetime | None = None) -> dict:
    path = ROOT / "system" / "PRESENCE.json"
    if not path.exists():
        return {"collaboration_state": "NOBODY", "sessions": {}, "source": "absent"}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LMTRFailure(f"LMTR-E020 presence unreadable: {exc}") from exc
    if data.get("version") != 1 or not isinstance(data.get("sessions"), dict):
        raise LMTRFailure("LMTR-E021 unsupported presence record")
    grace = data.get("grace_multiplier", 5)
    if not isinstance(grace, int) or not 3 <= grace <= 20:
        raise LMTRFailure("LMTR-E022 invalid presence grace multiplier")
    now = now or datetime.now(timezone.utc)
    effective = {}
    live = 0
    unknown = 0
    for role, session in data["sessions"].items():
        try:
            seen = datetime.fromisoformat(session["last_seen"].replace("Z", "+00:00"))
            interval = int(session["interval_seconds"])
            if seen.tzinfo is None or interval < 30:
                raise ValueError
            age = max(0.0, (now - seen.astimezone(timezone.utc)).total_seconds())
            if session.get("exit_state") == "CLOSED":
                status = "STALE"
            elif age <= interval * 2:
                status = "PRESENT"
                live += 1
            elif age <= interval * grace:
                status = "SUSPECT"
                live += 1
            else:
                status = "STALE"
            effective[role] = {"status": status, "age_seconds": int(age)}
        except (KeyError, TypeError, ValueError):
            effective[role] = {"status": "UNKNOWN"}
            unknown += 1
    if unknown:
        state = "RECOVER"
    else:
        state = "NOBODY" if live == 0 else "SOLO" if live == 1 else "TEAM"
    return {"collaboration_state": state, "sessions": effective, "source": str(path.relative_to(ROOT))}


def detect_state() -> str:
    installation = ROOT / "installation.yml"
    routing = ROOT / "ROUTING.md"
    system_agents = ROOT / "system" / "AGENTS.md"
    operational = [installation.exists(), routing.exists(), system_agents.exists()]
    if not any(operational):
        return "INITIALIZE"
    if not all(operational):
        return "RECOVER"
    agents = system_agents.read_text(encoding="utf-8")
    presence = reconcile_presence()
    if presence["collaboration_state"] in {"SOLO", "TEAM"}:
        return presence["collaboration_state"]
    if presence["collaboration_state"] == "RECOVER":
        return "RECOVER"
    if "State: ACTIVE" in agents or "| ACTIVE |" in agents:
        return "RESUME"
    if "State: PROPOSED" in agents or "State: ACKNOWLEDGING" in agents:
        return "JOIN"
    return "RECOVER"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate LMTR or print the bootstrap plan")
    parser.add_argument("command", choices=("validate", "plan", "presence"), nargs="?", default="validate")
    args = parser.parse_args()
    try:
        statements = validate()
        if args.command == "plan":
            print(json.dumps({"lmtr": "0.1.0", "state": detect_state(), "presence": reconcile_presence(), "statements": len(statements)}, indent=2))
        elif args.command == "presence":
            print(json.dumps(reconcile_presence(), indent=2))
        else:
            print(f"LMTR validation passed: {len(statements)} statements")
        return 0
    except LMTRFailure as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
