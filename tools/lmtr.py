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
AGENT_ID_RE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
ROUTE_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._/-]*$")
IDENTITY_STATES = {"PROPOSED", "ACKNOWLEDGING", "ACTIVE", "PAUSED", "RETIRED", "BLOCKED"}
IDENTITY_FIELDS = {
    "version", "agent_id", "display_name", "previous_display_names", "membership_state",
    "capabilities", "requested_routes", "approved_routes", "authority_boundary",
    "record_version", "proposed_at", "activated_at", "updated_at",
}
CAPABILITY_BOOLEAN_FIELDS = {
    "repository_read", "repository_write", "latest_sha_updates", "local_checkout",
    "terminal_execution", "python_3", "recurring_polling", "persistent_task_context",
    "external_notification",
}
CAPABILITY_TEXT_FIELDS = {"operating_environment", "tool_limits"}


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
        ("identity-directory", "snapshot", "require"),
        ("other-identity", "mutation", "deny"),
        ("display-name", "collision", "block"),
        ("peer-introduction", "broadcast", "deny"),
        ("admission-roles", "three-maximum", "require"),
    }
    missing = sorted(required - corpus)
    if missing:
        raise LMTRFailure(f"LMTR-E012 protected rules missing: {missing}")
    return statements


def _validate_timestamp(value: object, field: str, agent_id: str) -> datetime:
    if not isinstance(value, str):
        raise LMTRFailure(f"LMTR-E033 {agent_id}: {field} must be a date-time string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise LMTRFailure(f"LMTR-E033 {agent_id}: invalid {field}") from exc
    if parsed.tzinfo is None:
        raise LMTRFailure(f"LMTR-E033 {agent_id}: {field} requires a timezone")
    return parsed


def _validate_routes(value: object, field: str, agent_id: str) -> list[str]:
    if not isinstance(value, list) or any(
        not isinstance(route, str) or len(route) > 128 or not ROUTE_ID_RE.fullmatch(route)
        for route in value
    ):
        raise LMTRFailure(f"LMTR-E034 {agent_id}: invalid {field}")
    if len(value) != len(set(value)):
        raise LMTRFailure(f"LMTR-E034 {agent_id}: duplicate {field}")
    return value


def load_identity_directory(root: Path | None = None) -> dict:
    """Validate and return the sharded identity directory without mutating it."""
    root = root or ROOT
    directory = root / "system" / "identities"
    if not directory.exists():
        return {"source": "absent", "count": 0, "states": {}, "records": {}}
    if not directory.is_dir():
        raise LMTRFailure("LMTR-E030 system/identities is not a directory")
    nested = sorted(path.relative_to(directory).as_posix() for path in directory.rglob("*.json") if path.parent != directory)
    if nested:
        raise LMTRFailure(f"LMTR-E031 nested identity records are not allowed: {nested}")

    records = {}
    reserved_names: dict[str, str] = {}
    states: dict[str, int] = {}
    for path in sorted(directory.glob("*.json")):
        if path.is_symlink() or not path.is_file():
            raise LMTRFailure(f"LMTR-E031 unsafe identity record: {path.name}")
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise LMTRFailure(f"LMTR-E031 unreadable identity record {path.name}: {exc}") from exc
        if not isinstance(data, dict) or set(data) != IDENTITY_FIELDS or data.get("version") != 1:
            raise LMTRFailure(f"LMTR-E032 unsupported identity record: {path.name}")

        agent_id = data.get("agent_id")
        if not isinstance(agent_id, str) or not 3 <= len(agent_id) <= 64 or not AGENT_ID_RE.fullmatch(agent_id):
            raise LMTRFailure(f"LMTR-E032 invalid agent_id: {path.name}")
        if path.name != f"{agent_id}.json" or agent_id in records:
            raise LMTRFailure(f"LMTR-E032 identity filename mismatch or duplicate: {path.name}")

        display_name = data.get("display_name")
        if (
            not isinstance(display_name, str) or not 2 <= len(display_name) <= 64
            or display_name != display_name.strip() or "\n" in display_name or "\r" in display_name
        ):
            raise LMTRFailure(f"LMTR-E032 invalid display_name: {agent_id}")
        previous_names = data.get("previous_display_names")
        if not isinstance(previous_names, list) or any(
            not isinstance(name, str) or not 2 <= len(name) <= 64 or name != name.strip()
            or "\n" in name or "\r" in name
            for name in previous_names
        ):
            raise LMTRFailure(f"LMTR-E032 invalid previous_display_names: {agent_id}")
        local_names = [display_name, *previous_names]
        normalized = [name.casefold() for name in local_names]
        if len(normalized) != len(set(normalized)):
            raise LMTRFailure(f"LMTR-E035 repeated display name or alias: {agent_id}")
        for name, key in zip(local_names, normalized):
            if key in reserved_names:
                raise LMTRFailure(
                    f"LMTR-E035 display name collision: {name!r} is reserved by {reserved_names[key]} and {agent_id}"
                )
            reserved_names[key] = agent_id

        state = data.get("membership_state")
        if state not in IDENTITY_STATES:
            raise LMTRFailure(f"LMTR-E032 invalid membership_state: {agent_id}")
        states[state] = states.get(state, 0) + 1

        capabilities = data.get("capabilities")
        if not isinstance(capabilities, dict) or set(capabilities) != CAPABILITY_BOOLEAN_FIELDS | CAPABILITY_TEXT_FIELDS:
            raise LMTRFailure(f"LMTR-E036 invalid capability fields: {agent_id}")
        if any(not isinstance(capabilities[field], bool) for field in CAPABILITY_BOOLEAN_FIELDS):
            raise LMTRFailure(f"LMTR-E036 capability flags must be boolean: {agent_id}")
        text_limits = {"operating_environment": 200, "tool_limits": 500}
        if any(
            not isinstance(capabilities[field], str) or not capabilities[field].strip()
            or len(capabilities[field]) > text_limits[field]
            for field in CAPABILITY_TEXT_FIELDS
        ):
            raise LMTRFailure(f"LMTR-E036 capability descriptions must be non-empty: {agent_id}")

        requested_routes = _validate_routes(data.get("requested_routes"), "requested_routes", agent_id)
        approved_routes = _validate_routes(data.get("approved_routes"), "approved_routes", agent_id)
        if state == "PROPOSED" and approved_routes:
            raise LMTRFailure(f"LMTR-E037 PROPOSED identity has approved routes: {agent_id}")
        if not set(approved_routes).issubset(requested_routes):
            raise LMTRFailure(f"LMTR-E037 approved route was not requested: {agent_id}")
        if (
            not isinstance(data.get("authority_boundary"), str) or not data["authority_boundary"].strip()
            or len(data["authority_boundary"]) > 500
        ):
            raise LMTRFailure(f"LMTR-E032 missing authority_boundary: {agent_id}")
        if not isinstance(data.get("record_version"), int) or isinstance(data["record_version"], bool) or data["record_version"] < 1:
            raise LMTRFailure(f"LMTR-E032 invalid record_version: {agent_id}")
        proposed_at = _validate_timestamp(data.get("proposed_at"), "proposed_at", agent_id)
        updated_at = _validate_timestamp(data.get("updated_at"), "updated_at", agent_id)
        if updated_at < proposed_at:
            raise LMTRFailure(f"LMTR-E033 {agent_id}: updated_at precedes proposed_at")
        activated_at = data.get("activated_at")
        if activated_at is not None:
            activated_at = _validate_timestamp(activated_at, "activated_at", agent_id)
            if activated_at < proposed_at or activated_at > updated_at:
                raise LMTRFailure(f"LMTR-E033 {agent_id}: activated_at is outside the record lifetime")
        if state in {"ACTIVE", "PAUSED", "RETIRED"} and activated_at is None:
            raise LMTRFailure(f"LMTR-E033 {agent_id}: {state} requires activated_at")

        records[agent_id] = {
            "display_name": display_name,
            "membership_state": state,
            "approved_routes": approved_routes,
            "record_version": data["record_version"],
        }

    return {
        "source": str(directory.relative_to(root)),
        "count": len(records),
        "states": dict(sorted(states.items())),
        "records": records,
    }


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
    legacy_records = re.sub(r"```.*?```", "", agents, flags=re.DOTALL)
    presence = reconcile_presence()
    if presence["collaboration_state"] in {"SOLO", "TEAM"}:
        return presence["collaboration_state"]
    if presence["collaboration_state"] == "RECOVER":
        return "RECOVER"
    directory = load_identity_directory()
    directory_states = directory["states"]
    if directory_states.get("ACTIVE", 0):
        return "RESUME"
    if directory_states.get("PROPOSED", 0) or directory_states.get("ACKNOWLEDGING", 0):
        return "JOIN"
    if "State: ACTIVE" in legacy_records or "| ACTIVE |" in legacy_records:
        return "RESUME"
    if "State: PROPOSED" in legacy_records or "State: ACKNOWLEDGING" in legacy_records:
        return "JOIN"
    return "RECOVER"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate LMTR or print the bootstrap plan")
    parser.add_argument("command", choices=("validate", "plan", "presence", "directory"), nargs="?", default="validate")
    args = parser.parse_args()
    try:
        statements = validate()
        if args.command == "plan":
            print(json.dumps({
                "lmtr": "0.1.0",
                "state": detect_state(),
                "presence": reconcile_presence(),
                "directory": load_identity_directory(),
                "statements": len(statements),
            }, indent=2))
        elif args.command == "presence":
            print(json.dumps(reconcile_presence(), indent=2))
        elif args.command == "directory":
            print(json.dumps(load_identity_directory(), indent=2))
        else:
            print(f"LMTR validation passed: {len(statements)} statements")
        return 0
    except LMTRFailure as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
