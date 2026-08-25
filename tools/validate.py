#!/usr/bin/env python3
"""Structural validation for a LikeMinds template or installation."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md", "BOOTSTRAP.md", "ONBOARDING.md", "START-HERE.md", "AGENTS.md", "PROTOCOL.md", "JOINING.md", "JOIN-CHECKLIST.md",
    "SECURITY.md", "VERSION", "installation.example.yml", "templates/ROUTING.md",
    "templates/system/STATUS.md", "templates/system/DECISIONS.md",
    "templates/system/AGENTS.md", "templates/system/CHAT.md",
    "templates/system/SIGNALS.md", "templates/project/STATUS.md",
    "templates/system/PRESENCE.json", "schemas/presence.schema.json",
    "templates/project/DECISIONS.md", "templates/project/CHAT.md",
    "templates/project/SIGNALS.md", "extensions/TEMPLATE/manifest.yml",
    "extensions/TEMPLATE/EXTENSION.md", "extensions/TEMPLATE/INSTALL.md",
    "extensions/TEMPLATE/UNINSTALL.md",
    "lmtr/manifest.json", "tools/lmtr.py", "docs/wiki/Home.md",
    "docs/wiki/Quick-Start.md", "docs/wiki/LMTR-Reference.md",
    "docs/wiki/Installation.md",
    "docs/wiki/Agent-Capabilities.md",
    "docs/wiki/Coordination-Modes.md",
    "docs/wiki/Security-and-Authority.md", "docs/wiki/Launch-Checklist.md",
    "tests/test_lmtr.py",
]
PROTECTED_PHRASES = [
    "context, not authority",
    "latest blob sha",
    "update only your own cursor",
    "never move a conversation unilaterally",
]
JOINING_PHRASES = [
    "proposed → acknowledging → active",
    "only active roles may claim project work",
    "every current active project's full record",
    "system-only announcement remains insufficient",
    "human-authorized solo continuation",
    "creates a new active successor route",
    "solo-readiness",
    "the human—not the agent—chooses the operating mode",
    "bundled targeted root routing signal",
    "30-second",
    "2/4/6/10-cycle",
    "machine-readable join summary",
]
ALLOWED_SIGNAL_STATES = {"READY", "CLAIMED", "DONE", "BLOCKED", "CANCELLED"}
ALLOWED_MEMBER_STATES = {"PROPOSED", "ACKNOWLEDGING", "ACTIVE", "PAUSED", "RETIRED", "BLOCKED"}
MESSAGE_HEADER = re.compile(r"^### ([A-Z0-9-]+) — ", re.MULTILINE)
SIGNAL_HEADER = re.compile(r"^### ([A-Z0-9-]+)$", re.MULTILINE)


def markdown_files():
    return [p for p in ROOT.rglob("*.md") if ".git" not in p.parts]


def validate_required(errors):
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")


def validate_core_phrases(errors):
    corpus = "\n".join((ROOT / p).read_text(encoding="utf-8").lower()
                        for p in ("AGENTS.md", "PROTOCOL.md", "SECURITY.md"))
    for phrase in PROTECTED_PHRASES:
        if phrase not in corpus:
            errors.append(f"protected core phrase missing: {phrase}")


def validate_joining_protocol(errors):
    joining = (ROOT / "JOINING.md").read_text(encoding="utf-8").lower()
    protocol = (ROOT / "PROTOCOL.md").read_text(encoding="utf-8").lower()
    corpus = joining + "\n" + protocol
    for phrase in JOINING_PHRASES:
        if phrase not in corpus:
            errors.append(f"joining protocol phrase missing: {phrase}")

    registry = (ROOT / "templates/system/AGENTS.md").read_text(encoding="utf-8")
    for state in re.findall(r"^State:\s*(\S+)", registry, re.MULTILINE):
        if state not in ALLOWED_MEMBER_STATES:
            errors.append(f"templates/system/AGENTS.md: invalid member state {state}")


def validate_ids(errors):
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        ids = MESSAGE_HEADER.findall(text)
        duplicates = sorted({item for item in ids if ids.count(item) > 1})
        for item in duplicates:
            errors.append(f"{path.relative_to(ROOT)}: duplicate message id {item}")


def validate_signal_states(errors):
    for path in ROOT.rglob("SIGNALS.md"):
        text = path.read_text(encoding="utf-8")
        for state in re.findall(r"^State:\s*(\S+)", text, re.MULTILINE):
            if state not in ALLOWED_SIGNAL_STATES:
                errors.append(f"{path.relative_to(ROOT)}: invalid signal state {state}")


def validate_public_safety(errors):
    # Add installation-specific forbidden markers locally. The public template
    # deliberately avoids collecting or guessing personal identifiers.
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        if re.search(r"https://[^\s)]+[?&](sig|token|jwt)=", text, re.I):
            errors.append(f"{path.relative_to(ROOT)}: possible signed URL")


def main():
    errors = []
    validate_required(errors)
    validate_core_phrases(errors)
    validate_joining_protocol(errors)
    validate_ids(errors)
    validate_signal_states(errors)
    validate_public_safety(errors)
    try:
        from lmtr import validate as validate_lmtr
        validate_lmtr()
    except Exception as exc:
        errors.append(f"LMTR validation failed: {exc}")
    if errors:
        print("LikeMinds validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("LikeMinds structural validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
