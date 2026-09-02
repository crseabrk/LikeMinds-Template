#!/usr/bin/env python3
"""Dependency-free LMTR conformance checks."""

import importlib.util
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("lmtr", ROOT / "tools" / "lmtr.py")
lmtr = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = lmtr
SPEC.loader.exec_module(lmtr)


def identity(number: int, state: str = "PROPOSED") -> dict:
    stamp = "2026-01-01T00:00:00Z"
    active = state in {"ACTIVE", "PAUSED", "RETIRED"}
    return {
        "version": 1,
        "agent_id": f"agt-scale-{number:03d}",
        "display_name": f"Scale Agent {number:03d}",
        "previous_display_names": [],
        "membership_state": state,
        "capabilities": {
            "repository_read": True,
            "repository_write": True,
            "latest_sha_updates": True,
            "local_checkout": True,
            "terminal_execution": True,
            "python_3": True,
            "recurring_polling": False,
            "persistent_task_context": True,
            "external_notification": False,
            "operating_environment": "Test fixture",
            "tool_limits": "No external actions",
        },
        "requested_routes": ["system", "project-scale"],
        "approved_routes": ["system", "project-scale"] if active else [],
        "authority_boundary": "Test coordination only",
        "record_version": 2 if active else 1,
        "proposed_at": stamp,
        "activated_at": stamp if active else None,
        "updated_at": stamp,
    }


def main() -> None:
    statements = lmtr.validate()
    assert statements
    manifest = json.loads((ROOT / "lmtr" / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["modules"] == sorted(manifest["modules"])
    corpus = "\n".join(" ".join(item.words) for item in statements)
    for rule in (
        "default deny", "unknown deny", "ambiguous block", "silence solo deny",
        "other-heartbeat mutation deny", "expired-lease role-retire deny",
        "reentry lease-renew require", "identity-directory snapshot require",
        "other-identity mutation deny", "display-name collision block",
        "peer-introduction broadcast deny", "admission-roles acknowledge",
        "admission-roles three-maximum require",
        "identity-directory absent legacy-quorum require", "quorum-model mix deny",
    ):
        assert rule in corpus, rule

    bootstrap = (ROOT / "BOOTSTRAP.md").read_text(encoding="utf-8")
    for safeguard in (
        "Connector-only access",
        "Connector-only initialization",
        "static inspection",
        "remain read-only",
        "if no command was attempted, say so",
        "validation and tests as **DEFERRED**",
        "first checkout-capable authorized agent",
    ):
        assert safeguard in bootstrap, safeguard

    with tempfile.TemporaryDirectory() as directory:
        test_root = Path(directory)
        (test_root / "system").mkdir()
        now = datetime.now(timezone.utc).isoformat()
        presence = {
            "version": 1,
            "collaboration_state": "TEAM",
            "grace_multiplier": 5,
            "sessions": {
                "agent-a": {"session_id": "a", "last_seen": now, "interval_seconds": 180, "exit_state": "OPEN"},
                "agent-b": {"session_id": "b", "last_seen": now, "interval_seconds": 180, "exit_state": "OPEN"},
            },
        }
        (test_root / "system" / "PRESENCE.json").write_text(json.dumps(presence), encoding="utf-8")
        original_root = lmtr.ROOT
        try:
            lmtr.ROOT = test_root
            assert lmtr.reconcile_presence()["collaboration_state"] == "TEAM"
            presence["sessions"]["agent-b"]["exit_state"] = "CLOSED"
            (test_root / "system" / "PRESENCE.json").write_text(json.dumps(presence), encoding="utf-8")
            assert lmtr.reconcile_presence()["collaboration_state"] == "SOLO"
            presence["sessions"]["agent-a"]["exit_state"] = "CLOSED"
            (test_root / "system" / "PRESENCE.json").write_text(json.dumps(presence), encoding="utf-8")
            assert lmtr.reconcile_presence()["collaboration_state"] == "NOBODY"
        finally:
            lmtr.ROOT = original_root

    with tempfile.TemporaryDirectory() as directory:
        test_root = Path(directory)
        identities = test_root / "system" / "identities"
        identities.mkdir(parents=True)
        for number in range(100):
            record = identity(number, "ACTIVE" if number == 0 else "PROPOSED")
            (identities / f"{record['agent_id']}.json").write_text(
                json.dumps(record), encoding="utf-8"
            )
        snapshot = lmtr.load_identity_directory(test_root)
        assert snapshot["count"] == 100
        assert snapshot["states"] == {"ACTIVE": 1, "PROPOSED": 99}
        assert snapshot["records"]["agt-scale-000"]["display_name"] == "Scale Agent 000"

        collision = identity(99)
        collision["display_name"] = "scale agent 000"
        (identities / "agt-scale-099.json").write_text(json.dumps(collision), encoding="utf-8")
        try:
            lmtr.load_identity_directory(test_root)
            raise AssertionError("display-name collision was accepted")
        except lmtr.LMTRFailure as exc:
            assert "LMTR-E035" in str(exc)

        collision["display_name"] = "Scale Agent 099"
        collision["agent_id"] = "agt-wrong-name"
        (identities / "agt-scale-099.json").write_text(json.dumps(collision), encoding="utf-8")
        try:
            lmtr.load_identity_directory(test_root)
            raise AssertionError("identity filename mismatch was accepted")
        except lmtr.LMTRFailure as exc:
            assert "LMTR-E032" in str(exc)
    print("LMTR conformance checks passed.")


if __name__ == "__main__":
    main()
