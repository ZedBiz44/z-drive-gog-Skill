#!/usr/bin/env python3
"""Validate z-drive-gog private configuration and non-mutating GOG readiness."""

from __future__ import annotations

import argparse
import json
import os
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any


def fail(message: str) -> None:
    print(json.dumps({"ok": False, "error": message}, indent=2))
    raise SystemExit(1)


def private_path(path: Path, label: str, is_file: bool = False) -> None:
    target = path if not is_file else path.parent
    if not target.exists():
        fail(f"{label} path does not exist: {target}")
    mode = stat.S_IMODE(target.stat().st_mode)
    if mode & (stat.S_IRWXG | stat.S_IRWXO):
        fail(f"{label} path must not be group/world accessible: {target}")


def run(command: list[str]) -> dict[str, Any]:
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=30, check=False)
    except FileNotFoundError:
        fail(f"GOG binary was not found: {command[0]}")
    except subprocess.TimeoutExpired:
        fail(f"GOG command timed out: {' '.join(command[:3])}")

    return {
        "command": command[:3] + ["…"] if len(command) > 3 else command,
        "returncode": result.returncode,
        "stdout": result.stdout[:500],
        "stderr": result.stderr[:500],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", required=True, type=Path)
    parser.add_argument("--account-label", required=True)
    parser.add_argument("--client-code", required=True)
    parser.add_argument("--gog-bin", default="gog")
    parser.add_argument("--skip-auth-check", action="store_true")
    args = parser.parse_args()

    if not args.registry.is_file():
        fail(f"registry does not exist: {args.registry}")
    private_path(args.registry, "registry", is_file=True)

    try:
        registry = json.loads(args.registry.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"registry is not readable JSON: {exc}")

    account = registry.get("accounts", {}).get(args.account_label, {})
    client = registry.get("clients", {}).get(args.client_code, {})
    runtime = registry.get("runtime", {})
    gog_account = account.get("gog_account")
    root_id = client.get("client_root_folder_id")

    if not gog_account or gog_account == "auto":
        fail("registry must provide an explicit non-auto gog_account")
    if not root_id:
        fail("registry must provide client_root_folder_id")
    if not runtime.get("receipt_log") or not runtime.get("cache_dir"):
        fail("registry must provide receipt_log and cache_dir")

    cache_dir = Path(runtime["cache_dir"]).expanduser()
    receipt_log = Path(runtime["receipt_log"]).expanduser()
    private_path(cache_dir, "cache")
    private_path(receipt_log, "receipt log", is_file=True)
    if receipt_log.exists():
        mode = stat.S_IMODE(receipt_log.stat().st_mode)
        if mode & (stat.S_IRWXG | stat.S_IRWXO):
            fail(f"receipt log must not be group/world accessible: {receipt_log}")

    version = run([args.gog_bin, "--version"])
    schema = run([args.gog_bin, "schema", "--json"])
    if version["returncode"] != 0 or schema["returncode"] != 0:
        fail("GOG version or schema check failed; inspect the selected GOG installation")

    auth: dict[str, Any] = {"skipped": True}
    if not args.skip_auth_check:
        auth = run([
            args.gog_bin,
            "auth",
            "doctor",
            "--account",
            gog_account,
            "--check",
            "--json",
            "--no-input",
        ])
        if auth["returncode"] != 0:
            fail("GOG authentication check failed for the selected account")

    print(json.dumps({
        "ok": True,
        "account_label": args.account_label,
        "client_code": args.client_code,
        "client_root_folder_id": root_id,
        "shared_drive": bool(client.get("shared_drive_id")),
        "gog_version": version,
        "gog_schema": schema,
        "auth": auth,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
