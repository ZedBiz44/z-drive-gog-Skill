#!/usr/bin/env python3
"""Build or execute constrained z-drive-gog commands from private runtime configuration."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ID_RE = re.compile(r"^[A-Za-z0-9_-]{10,}$")
ROLES = {"reader", "writer", "commenter"}
ROUTINE = {"upload", "mkdir", "copy", "rename", "move", "archive", "download", "get", "search"}
PREVIEW = {"replace", "trash", "external-share", "remove-access"}
JACK_ONLY = {"public-share", "domain-share", "permanent-delete"}


def fail(message: str) -> None:
    print(json.dumps({"ok": False, "error": message}))
    raise SystemExit(2)


def load_registry(path: Path, account_label: str, client_code: str) -> tuple[str, dict[str, Any], dict[str, Any]]:
    try:
        registry = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read private registry: {exc}")
    account = registry.get("accounts", {}).get(account_label, {})
    client = registry.get("clients", {}).get(client_code, {})
    gog_account = account.get("gog_account")
    if not gog_account or gog_account == "auto":
        fail("registry must supply explicit non-auto gog_account")
    if not client.get("client_root_folder_id"):
        fail("registry must supply client_root_folder_id")
    return gog_account, client, registry.get("runtime", {})


def check_id(value: str | None, label: str) -> str:
    if not value or not ID_RE.fullmatch(value):
        fail(f"{label} must be a valid Drive ID")
    return value


def check_local_path(value: str | None, workspace: Path) -> str:
    if not value:
        fail("local path is required for upload or replace")
    path = Path(value).expanduser().resolve()
    workspace = workspace.expanduser().resolve()
    if not path.is_file():
        fail("local path must identify an existing regular file")
    if workspace not in path.parents:
        fail("local file must be inside the approved task workspace")
    return str(path)


def require_approval(action: str, approval: str) -> None:
    if action in JACK_ONLY and approval != "jack":
        fail(f"{action} requires Jack’s explicit approval")
    if action in PREVIEW and approval not in {"preview", "jack"}:
        fail(f"{action} requires a reviewed preview approval")
    if action in ROUTINE and approval not in {"assignment", "preview", "jack"}:
        fail(f"{action} requires current-assignment authorization")


def add_common(command: list[str], account: str) -> list[str]:
    return command + ["--account", account, "--json", "--no-input", "--wrap-untrusted"]


def build_command(args: argparse.Namespace, account: str, client: dict[str, Any]) -> tuple[list[str], str]:
    action = args.action
    root = check_id(client.get("client_root_folder_id"), "configured client root folder ID")
    archive = client.get("archive_folder_id")
    destination = args.destination_folder_id or args.parent_folder_id

    if action in {"upload", "mkdir", "copy", "move", "archive"}:
        if action == "archive":
            destination = archive
        destination = check_id(destination, "destination folder ID")
        if destination not in {root, archive} and not args.boundary_proof:
            fail("nested destination needs a successful boundary proof from drive_resolve_target.py")
        if action == "upload":
            local_path = check_local_path(args.local_path, Path(args.task_workspace))
            if not args.name:
                fail("upload requires --name")
            return add_common([args.gog_bin, "drive", "upload", local_path, "--parent", destination, "--name", args.name], account), action
        if action == "mkdir":
            if not args.name:
                fail("mkdir requires --name")
            return add_common([args.gog_bin, "drive", "mkdir", args.name, "--parent", destination], account), action
        if action == "copy":
            source = check_id(args.file_id, "source file ID")
            if not args.name:
                fail("copy requires --name")
            return add_common([args.gog_bin, "drive", "copy", source, args.name, "--parent", destination], account), action
        source = check_id(args.file_id, "file ID")
        return add_common([args.gog_bin, "drive", "move", source, "--parent", destination], account), action

    if action == "rename":
        source = check_id(args.file_id, "file ID")
        if not args.name:
            fail("rename requires --name")
        return add_common([args.gog_bin, "drive", "rename", source, args.name], account), action

    if action == "remove-access":
        source = check_id(args.file_id, "file ID")
        permission = check_id(args.permission_id, "permission ID")
        return add_common([args.gog_bin, "drive", "unshare", source, permission], account), action

    if action == "replace":
        source = check_id(args.file_id, "existing file ID")
        local_path = check_local_path(args.local_path, Path(args.task_workspace))
        command = [args.gog_bin, "drive", "upload", local_path, "--replace", source]
        if args.if_version:
            command += ["--if-version", args.if_version]
        return add_common(command, account), action

    if action == "trash":
        source = check_id(args.file_id, "file ID")
        return add_common([args.gog_bin, "drive", "delete", source], account), action

    if action == "permanent-delete":
        source = check_id(args.file_id, "file ID")
        return add_common([args.gog_bin, "drive", "delete", source, "--permanent"], account), action

    if action in {"external-share", "public-share", "domain-share"}:
        source = check_id(args.file_id, "file ID")
        role = args.role or "reader"
        if role not in ROLES:
            fail("role must be reader, writer, or commenter")
        if action == "external-share":
            if not args.email:
                fail("external-share requires --email")
            command = [args.gog_bin, "drive", "share", source, "--to", "user", "--email", args.email, "--role", role]
        elif action == "domain-share":
            if not args.domain:
                fail("domain-share requires --domain")
            command = [args.gog_bin, "drive", "share", source, "--to", "domain", "--domain", args.domain, "--role", role]
        else:
            command = [args.gog_bin, "drive", "share", source, "--to", "anyone", "--role", role]
        if args.notify:
            command.append("--notify")
        return add_common(command, account), action

    if action == "get":
        return add_common([args.gog_bin, "drive", "get", check_id(args.file_id, "file ID")], account), action
    if action == "download":
        source = check_id(args.file_id, "file ID")
        if not args.output_path:
            fail("download requires --output-path")
        return add_common([args.gog_bin, "drive", "download", source, "--format", args.export_format, "--out", args.output_path], account), action
    if action == "search":
        if not args.query:
            fail("search requires --query")
        command = [args.gog_bin, "drive", "search", args.query, "--parent", root, "--max", str(args.max_results)]
        if client.get("shared_drive_id"):
            command += ["--drive", client["shared_drive_id"]]
        else:
            command.append("--no-all-drives")
        return add_common(command, account), action

    fail(f"unsupported action: {action}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", required=True, type=Path)
    parser.add_argument("--account-label", required=True)
    parser.add_argument("--client-code", required=True)
    parser.add_argument("--action", required=True, choices=sorted(ROUTINE | PREVIEW | JACK_ONLY))
    parser.add_argument("--approval", required=True, choices=("assignment", "preview", "jack"))
    parser.add_argument("--gog-bin", default="gog")
    parser.add_argument("--file-id")
    parser.add_argument("--parent-folder-id")
    parser.add_argument("--destination-folder-id")
    parser.add_argument("--local-path")
    parser.add_argument("--task-workspace", default="/tmp")
    parser.add_argument("--name")
    parser.add_argument("--email")
    parser.add_argument("--domain")
    parser.add_argument("--role")
    parser.add_argument("--permission-id")
    parser.add_argument("--cross-client", action="store_true")
    parser.add_argument("--notify", action="store_true")
    parser.add_argument("--if-version")
    parser.add_argument("--query")
    parser.add_argument("--max-results", type=int, default=20)
    parser.add_argument("--export-format", default="md")
    parser.add_argument("--output-path")
    parser.add_argument("--boundary-proof", action="store_true")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    require_approval(args.action, args.approval)
    if args.cross_client and args.action in {"move", "copy"} and args.approval not in {"preview", "jack"}:
        fail("cross-client move or copy requires a reviewed preview approval")
    account, client, _runtime = load_registry(args.registry, args.account_label, args.client_code)
    command, action = build_command(args, account, client)
    output: dict[str, Any] = {"ok": True, "action": action, "command": command, "executed": False}

    if args.execute:
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=120, check=False)
        except (OSError, subprocess.TimeoutExpired) as exc:
            fail(f"GOG execution failed: {exc}")
        output.update({"executed": True, "returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
        if result.returncode != 0:
            output["ok"] = False
            print(json.dumps(output, indent=2))
            return result.returncode

    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
