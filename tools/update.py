#!/usr/bin/env python3
"""Plan and apply fail-closed LikeMinds framework updates from a local source checkout."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / ".likeminds" / "update-state.json"
MANIFEST_REL = Path("updates/managed-files.json")


class UpdateFailure(Exception):
    pass


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_relative(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise UpdateFailure(f"unsafe managed path: {value}")
    return path


def load_manifest(source: Path) -> dict:
    try:
        data = json.loads((source / MANIFEST_REL).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise UpdateFailure(f"update manifest unreadable: {exc}") from exc
    if data.get("format") != "likeminds-managed-files-1":
        raise UpdateFailure("unsupported update manifest")
    files = data.get("files")
    if not isinstance(files, list) or not files or files != sorted(set(files)):
        raise UpdateFailure("managed file list must be non-empty, unique, and sorted")
    protected = tuple(data.get("protected_paths", []))
    for value in files:
        rel = safe_relative(value)
        text = rel.as_posix()
        if any(text == item.rstrip("/") or text.startswith(item) for item in protected):
            raise UpdateFailure(f"manifest attempts to manage protected path: {text}")
        if not (source / rel).is_file():
            raise UpdateFailure(f"source is missing managed file: {text}")
    return data


def load_state() -> dict:
    if not STATE.exists():
        return {"format": "likeminds-update-state-1", "files": {}}
    try:
        data = json.loads(STATE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise UpdateFailure(f"update state unreadable: {exc}") from exc
    if data.get("format") != "likeminds-update-state-1" or not isinstance(data.get("files"), dict):
        raise UpdateFailure("unsupported update state")
    return data


def source_revision(source: Path, supplied: str | None) -> str:
    if supplied:
        return supplied
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=source, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else "UNVERIFIED"


def build_plan(source: Path, manifest: dict, state: dict) -> list[dict]:
    plan = []
    installed = state["files"]
    for value in manifest["files"]:
        rel = safe_relative(value)
        src = source / rel
        dst = ROOT / rel
        source_hash = digest(src)
        current_hash = digest(dst) if dst.is_file() else None
        installed_hash = installed.get(value)
        if current_hash == source_hash:
            action = "UNCHANGED"
        elif current_hash is None:
            action = "ADD"
        elif installed_hash is None:
            action = "CONFLICT-UNTRACKED"
        elif current_hash != installed_hash:
            action = "CONFLICT-LOCAL-MODIFICATION"
        else:
            action = "UPDATE"
        plan.append({
            "path": value, "action": action, "installed_sha256": installed_hash,
            "current_sha256": current_hash, "source_sha256": source_hash,
        })
    return plan


def write_state(source: Path, manifest: dict, revision: str) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "format": "likeminds-update-state-1",
        "source": "crseabrk/LikeMinds-Template",
        "source_revision": revision,
        "source_version": manifest["version"],
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "files": {value: digest(ROOT / safe_relative(value)) for value in manifest["files"] if (ROOT / safe_relative(value)).is_file()},
    }
    temporary = STATE.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(STATE)


def adopt(source: Path, manifest: dict, revision: str) -> None:
    if STATE.exists():
        raise UpdateFailure("update state already exists; adopt is only for an unmanaged installation")
    STATE.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "format": "likeminds-update-state-1",
        "source": "crseabrk/LikeMinds-Template",
        "source_revision": "ADOPTED-BASELINE",
        "source_version": "UNVERIFIED",
        "target_source_revision": revision,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "files": {value: digest(ROOT / safe_relative(value)) for value in manifest["files"] if (ROOT / safe_relative(value)).is_file()},
    }
    STATE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Adopted current installation as an unverified baseline; reviewed update target is {revision}")


def validate_installation() -> None:
    commands = ([sys.executable, "tools/lmtr.py", "validate"], [sys.executable, "tests/test_lmtr.py"])
    for command in commands:
        result = subprocess.run(command, cwd=ROOT, text=True)
        if result.returncode:
            raise UpdateFailure(f"post-update validation failed: {' '.join(command)}")


def apply(source: Path, manifest: dict, state: dict, plan: list[dict], revision: str) -> None:
    conflicts = [item for item in plan if item["action"].startswith("CONFLICT")]
    if conflicts:
        raise UpdateFailure("conflicts block update: " + ", ".join(item["path"] for item in conflicts))
    changes = [item for item in plan if item["action"] in {"ADD", "UPDATE"}]
    if not changes:
        write_state(source, manifest, revision)
        print("Already current; update state refreshed")
        return
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = ROOT / ".likeminds" / "backups" / stamp
    copied = []
    try:
        for item in changes:
            rel = safe_relative(item["path"])
            dst = ROOT / rel
            if dst.exists():
                saved = backup / rel
                saved.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(dst, saved)
            dst.parent.mkdir(parents=True, exist_ok=True)
            temporary = dst.with_suffix(dst.suffix + ".update-tmp")
            shutil.copy2(source / rel, temporary)
            temporary.replace(dst)
            copied.append((dst, (backup / rel) if (backup / rel).exists() else None))
        validate_installation()
        write_state(source, manifest, revision)
    except Exception:
        for dst, saved in reversed(copied):
            if saved:
                shutil.copy2(saved, dst)
            elif dst.exists():
                dst.unlink()
        raise
    print(f"Updated {len(changes)} managed files to {manifest['version']} from {revision}")
    print(f"Backup: {backup}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage LikeMinds framework updates")
    parser.add_argument("command", choices=("adopt", "plan", "apply"))
    parser.add_argument("--source", required=True, help="local checkout of LikeMinds-Template")
    parser.add_argument("--source-revision", help="verified upstream commit SHA")
    args = parser.parse_args()
    try:
        source = Path(args.source).resolve()
        if source == ROOT:
            raise UpdateFailure("source and installation must be different directories")
        manifest = load_manifest(source)
        revision = source_revision(source, args.source_revision)
        if args.command == "adopt":
            adopt(source, manifest, revision)
            return 0
        state = load_state()
        plan = build_plan(source, manifest, state)
        print(json.dumps({"source_version": manifest["version"], "source_revision": revision, "changes": plan}, indent=2))
        if args.command == "apply":
            if not STATE.exists():
                raise UpdateFailure("installation is unmanaged; run adopt, review the plan, then apply")
            apply(source, manifest, state, plan, revision)
        return 0
    except UpdateFailure as exc:
        print(f"UPDATE-E001 {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
