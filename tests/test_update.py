#!/usr/bin/env python3
"""Integration checks for managed LikeMinds updates."""

from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def run(destination: Path, *args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, "tools/update.py", *args], cwd=destination,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    assert result.returncode == expected, result.stdout + result.stderr
    return result


def copy_repo(source: Path, destination: Path) -> None:
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns(".git", ".likeminds", "__pycache__"))


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        base = Path(directory)
        source = base / "source"
        destination = base / "installation"
        copy_repo(ROOT, source)
        copy_repo(ROOT, destination)

        run(destination, "adopt", "--source", str(source), "--source-revision", "baseline")
        state_path = destination / ".likeminds" / "update-state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        assert state["source_revision"] == "ADOPTED-BASELINE"
        assert state["target_source_revision"] == "baseline"

        (source / "VERSION").write_text("test-update\n", encoding="utf-8")
        plan = run(destination, "plan", "--source", str(source), "--source-revision", "update-1")
        assert '"path": "VERSION"' in plan.stdout and '"action": "UPDATE"' in plan.stdout
        run(destination, "apply", "--source", str(source), "--source-revision", "update-1")
        assert (destination / "VERSION").read_text(encoding="utf-8") == "test-update\n"

        (destination / "AGENTS.md").write_text(
            (destination / "AGENTS.md").read_text(encoding="utf-8") + "\nlocal change\n",
            encoding="utf-8",
        )
        (source / "AGENTS.md").write_text(
            (source / "AGENTS.md").read_text(encoding="utf-8") + "\nupstream change\n",
            encoding="utf-8",
        )
        conflict = run(destination, "plan", "--source", str(source), "--source-revision", "update-2")
        assert "CONFLICT-LOCAL-MODIFICATION" in conflict.stdout
        run(destination, "apply", "--source", str(source), "--source-revision", "update-2", expected=1)

    print("LikeMinds updater checks passed.")


if __name__ == "__main__":
    main()
