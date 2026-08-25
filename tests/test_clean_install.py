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
        shutil.copytree(ROOT, installation, ignore=shutil.ignore_patterns(".git", ".likeminds", "__pycache__"))

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

        registry = installation / "system" / "AGENTS.md"
        text = registry.read_text(encoding="utf-8")
        marker = "|---|---|---|---|---|---|---|"
        row = "| Clean Room Coordinator | ACTIVE | local validation only | system, example | test | test | smoke-test role |"
        registry.write_text(text.replace(marker, marker + "\n" + row, 1), encoding="utf-8")

        resumed = json.loads(run(installation, sys.executable, "tools/lmtr.py", "plan"))
        assert resumed["state"] == "RESUME"
        assert resumed["presence"]["collaboration_state"] == "NOBODY"
        run(installation, sys.executable, "tools/lmtr.py", "validate")
        run(installation, sys.executable, "tests/test_lmtr.py")
        run(installation, sys.executable, "tools/validate.py")

    print("Clean-room installation checks passed.")


if __name__ == "__main__":
    main()
