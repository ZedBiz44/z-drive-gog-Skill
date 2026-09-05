#!/usr/bin/env python3
"""Verify Drive item ancestry and shortcut targets against one approved client root."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ID_RE = re.compile(r"^[A-Za-z0-9_-]{10,}$")


def fail(message: str) -> None:
    print(json.dumps({"ok": False, "error": message}, indent=2))
    raise SystemExit(1)


def check_id(value: str, label: str) -> str:
    if not ID_RE.fullmatch(value):
        fail(f"{label} must be a Drive ID")
    return value


def extract_items(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        for key in ("files", "items", "results"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        data = payload.get("data")
        if isinstance(data, dict) and isinstance(data.get("files"), list):
            return [item for item in data["files"] if isinstance(item, dict)]
        if payload.get("id"):
            return [payload]
    fail("metadata JSON must be an item object, a list, or an object containing files/items/results")


def target_id(item: dict[str, Any]) -> str | None:
    details = item.get("shortcutDetails") or item.get("shortcut_details") or {}
    if not isinstance(details, dict):
        return None
    return details.get("targetId") or details.get("target_id")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata-json", required=True, type=Path)
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--client-root-id", required=True)
    parser.add_argument("--shared-drive-id")
    args = parser.parse_args()

    candidate_id = check_id(args.candidate_id, "candidate ID")
    root_id = check_id(args.client_root_id, "client root ID")
    if args.shared_drive_id:
        check_id(args.shared_drive_id, "Shared Drive ID")

    try:
        payload = json.loads(args.metadata_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read metadata JSON: {exc}")

    items = extract_items(payload)
    by_id = {str(item.get("id")): item for item in items if item.get("id")}
    if candidate_id not in by_id:
        fail("candidate is missing from metadata JSON")

    candidate = by_id[candidate_id]
    resolved_id = target_id(candidate) or candidate_id
    if resolved_id not in by_id:
        fail("shortcut target metadata is required before it can be trusted")

    resolved = by_id[resolved_id]
    if resolved.get("trashed") is True:
        fail("resolved item is trashed")
    if args.shared_drive_id and resolved.get("driveId") not in {None, args.shared_drive_id}:
        fail("resolved item belongs to a different Shared Drive")

    chain: list[str] = [resolved_id]
    current_id = resolved_id
    visited = {current_id}
    while current_id != root_id:
        current = by_id.get(current_id)
        if not current:
            fail(f"metadata is missing parent details for {current_id}")
        parents = current.get("parents")
        if not isinstance(parents, list) or not parents:
            fail("ancestry did not reach the approved client root")
        if len(parents) != 1:
            fail("multiple parents require explicit human review")
        parent_id = str(parents[0])
        if parent_id in visited:
            fail("folder ancestry contains a loop")
        if parent_id != root_id and parent_id not in by_id:
            fail(f"metadata is missing parent details for {parent_id}")
        chain.append(parent_id)
        visited.add(parent_id)
        current_id = parent_id

    print(json.dumps({
        "ok": True,
        "candidate_id": candidate_id,
        "resolved_id": resolved_id,
        "is_shortcut": resolved_id != candidate_id,
        "client_root_id": root_id,
        "ancestry": chain,
        "name": resolved.get("name"),
        "mime_type": resolved.get("mimeType"),
        "modified_time": resolved.get("modifiedTime"),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
