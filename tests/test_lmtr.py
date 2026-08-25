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


def main() -> None:
    statements = lmtr.validate()
    assert statements
    manifest = json.loads((ROOT / "lmtr" / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["modules"] == sorted(manifest["modules"])
    corpus = "\n".join(" ".join(item.words) for item in statements)
    for rule in (
        "default deny", "unknown deny", "ambiguous block", "silence solo deny",
        "other-heartbeat mutation deny", "expired-lease role-retire deny",
        "reentry lease-renew require",
    ):
        assert rule in corpus, rule

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
    print("LMTR conformance checks passed.")


if __name__ == "__main__":
    main()
