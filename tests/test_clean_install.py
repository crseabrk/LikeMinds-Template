#!/usr/bin/env python3
"""Clean-room smoke test for documented manual installation."""

from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def run(root: Path, *command: str) -> str:
    result = subprocess.run(command, cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert result.returncode == 0, result.stdout
    return result.stdout


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        installation = Path(directory) / "clean-private-installation"
        installation.mkdir()
        manifest = json.loads((ROOT / "updates" / "managed-files.json").read_text(encoding="utf-8"))
        for relative in manifest["files"]:
            source = ROOT / relative
            target = installation / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)

        initial = json.loads(run(installation, sys.executable, "tools/lmtr.py", "plan"))
        assert initial["state"] == "INITIALIZE"
        assert initial["presence"]["collaboration_state"] == "NOBODY"

        metadata = (installation / "installation.example.yml").read_text(encoding="utf-8")
        (installation / "installation.yml").write_text(
            metadata.replace("OWNER/REPOSITORY", "example/private-likeminds"), encoding="utf-8"
        )
        shutil.copy2(installation / "templates" / "ROUTING.md", installation / "ROUTING.md")
        shutil.copytree(installation / "templates" / "system", installation / "system")
        shutil.copytree(installation / "templates" / "project", installation / "projects" / "example")

        unregistered = json.loads(run(installation, sys.executable, "tools/lmtr.py", "plan"))
        assert unregistered["state"] == "RECOVER"
        assert unregistered["directory"]["count"] == 0

        identity = {
            "version": 1,
            "agent_id": "agt-clean-room-001",
            "display_name": "Clean Room Coordinator",
            "previous_display_names": [],
            "membership_state": "ACTIVE",
            "capabilities": {
                "repository_read": True,
                "repository_write": True,
                "latest_sha_updates": True,
                "local_checkout": True,
                "terminal_execution": True,
                "python_3": True,
                "recurring_polling": False,
                "persistent_task_context": False,
                "external_notification": False,
                "operating_environment": "Clean-room test fixture",
                "tool_limits": "Local validation only",
            },
            "requested_routes": ["system", "example"],
            "approved_routes": ["system", "example"],
            "authority_boundary": "Smoke-test coordination only",
            "record_version": 2,
            "proposed_at": "2026-01-01T00:00:00Z",
            "activated_at": "2026-01-01T00:00:01Z",
            "updated_at": "2026-01-01T00:00:01Z",
        }
        identity_path = installation / "system" / "identities" / "agt-clean-room-001.json"
        identity_path.write_text(json.dumps(identity, indent=2) + "\n", encoding="utf-8")

        resumed = json.loads(run(installation, sys.executable, "tools/lmtr.py", "plan"))
        assert resumed["state"] == "RESUME"
        assert resumed["presence"]["collaboration_state"] == "NOBODY"
        assert resumed["directory"]["count"] == 1
        run(installation, sys.executable, "tools/lmtr.py", "validate")
        run(installation, sys.executable, "tools/lmtr.py", "directory")
        run(installation, sys.executable, "tests/test_lmtr.py")
        run(installation, sys.executable, "tools/validate.py")

    print("Clean-room installation checks passed.")


if __name__ == "__main__":
    main()
