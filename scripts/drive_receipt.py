#!/usr/bin/env python3
"""Write a redacted JSONL receipt for one z-drive-gog action."""

from __future__ import annotations

import argparse
import json
import os
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ALLOWED_FIELDS = {
    "agent",
    "account_label",
    "client_code",
    "action",
    "file_id",
    "folder_id",
    "source_file_id",
    "destination_folder_id",
    "mime_type",
    "modified_time",
    "result_link",
    "verification",
    "status",
    "approval_reference",
    "cache_status",
    "error_category",
}
BANNED_PARTS = ("token", "secret", "password", "content", "body", "email", "permission")


def fail(message: str) -> None:
    print(json.dumps({"ok": False, "error": message}))
    raise SystemExit(1)


def ensure_private(path: Path) -> None:
    if not path.parent.exists():
        fail(f"receipt directory does not exist: {path.parent}")
    directory_mode = stat.S_IMODE(path.parent.stat().st_mode)
    if directory_mode & (stat.S_IRWXG | stat.S_IRWXO):
        fail("receipt directory must not be group/world accessible")
    if path.exists():
        file_mode = stat.S_IMODE(path.stat().st_mode)
        if file_mode & (stat.S_IRWXG | stat.S_IRWXO):
            fail("receipt file must not be group/world accessible")


def clean_event(event: dict[str, Any]) -> dict[str, Any]:
    clean: dict[str, Any] = {}
    for key, value in event.items():
        lowered = key.lower()
        if key not in ALLOWED_FIELDS:
            continue
        if any(part in lowered for part in BANNED_PARTS):
            continue
        if isinstance(value, (str, int, float, bool)) or value is None:
            clean[key] = value
        else:
            fail(f"receipt field '{key}' must be a simple value")
    return clean


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt-log", required=True, type=Path)
    parser.add_argument("--event-json", required=True, help="One JSON object, not a file path")
    args = parser.parse_args()

    ensure_private(args.receipt_log)
    try:
        event = json.loads(args.event_json)
    except json.JSONDecodeError as exc:
        fail(f"event-json must be valid JSON: {exc}")
    if not isinstance(event, dict):
        fail("event-json must be a JSON object")

    receipt = clean_event(event)
    required = {"agent", "account_label", "client_code", "action", "status", "verification"}
    missing = sorted(required - receipt.keys())
    if missing:
        fail(f"receipt is missing required fields: {', '.join(missing)}")
    receipt["timestamp"] = datetime.now(timezone.utc).isoformat()

    flags = os.O_APPEND | os.O_CREAT | os.O_WRONLY
    fd = os.open(args.receipt_log, flags, 0o600)
    with os.fdopen(fd, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(receipt, sort_keys=True) + "\n")
    os.chmod(args.receipt_log, 0o600)

    print(json.dumps({"ok": True, "receipt_log": str(args.receipt_log), "action": receipt["action"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
