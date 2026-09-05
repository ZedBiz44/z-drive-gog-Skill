# Drive Operations

Read this file before creating, uploading, copying, renaming, moving, archiving, sharing, or trashing a Drive item. Use the installed GOG schema as the final command contract.

## Preflight

Before the first operation on an agent, after a GOG update, or when authentication fails:

```bash
gog --version
gog schema --json
gog auth doctor --account "$ACCOUNT" --check --json --no-input
```

Confirm the account label, selected client code, source ID, destination folder ID, client-boundary checks, and required approval status. Use `--dry-run` for unfamiliar commands.

## Routine Work Authorized by the Assignment

When the current assignment clearly calls for the following work inside an approved client folder, complete it without a second confirmation. Validate input and destination IDs, execute once, verify live Drive state, then write a private receipt.

| Task | GOG action | Required verification |
|---|---|---|
| Upload a new file | `gog drive upload <localPath> --parent <folderId> --name <name>` | Returned file ID, name, parent, and web link. |
| Create a folder | `gog drive mkdir <name> --parent <folderId>` | Returned folder ID and parent. |
| Copy a template | `gog drive copy <templateId> <newName> --parent <folderId>` | Source ID, new ID, name, and parent. |
| Rename | `gog drive rename <fileId> <newName>` | Same file ID and new name. |
| Move within one client | `gog drive move <fileId> --parent <folderId>` | Same file ID and destination parent. |
| Archive | `gog drive move <fileId> --parent <archiveFolderId>` | Same file ID and archive parent. |
| Export | `gog drive download <fileId> --format <format> --out <path>` | Export file exists locally and source modification time is recorded. |

Always use `--account "$ACCOUNT" --json --no-input --wrap-untrusted` unless an installed schema documents a required alternative. Do not use shell string concatenation with user-provided names or paths. Pass values as separate structured arguments.

## Create and Upload Rules

- Verify that a local upload file exists, is a regular file, and is inside the approved task workspace. Do not upload arbitrary system files, secret files, runtime registries, cache files, or logs.
- Prefer a new file or a template copy. Name the new deliverable clearly, normally `Client - Deliverable - YYYY-MM-DD`.
- Do not alter a master template. Copy it first and work on the copy.
- Use `--convert` or `--convert-to doc|sheet|slides` only when the current assignment explicitly asks for a Google-native file and the installed GOG schema supports the conversion.
- Do not pass `--replace` unless overwrite approval has been obtained. If replacement is approved, use `--if-version <known-version>` when the installed schema supports it, then re-read the result. Stop on a version conflict.

## Rename, Move, Copy, and Archive Rules

- Resolve the source by file ID. Do not rename or move the first result of a fuzzy search.
- Verify both source and destination ancestry before a move or copy.
- Treat an item moving to a different client as high risk even if both client folders are configured. Show a preview and ask first.
- Before copying, search the destination for an equivalent recent copy. Avoid duplicate clutter. If a duplicate is not clearly equivalent, create the requested copy and record both IDs.
- Archive only to the configured archive folder inside the same client boundary.

## Risky Operations

Before any operation in this table, show a concise preview with the account, client code, source ID, destination or recipient, visibility effect, recovery path, and expected result. Wait for explicit approval.

| Risky task | Required approval |
|---|---|
| Replace file contents | Explicit approval for the exact existing file ID. |
| Trash important file or folder | Explicit approval for the exact item. Prefer archive when appropriate. |
| Move or copy across client boundaries | Explicit approval after source and destination checks. |
| Share outside the normal client group | Explicit approval that names the recipient/group and role. |
| Remove access | Explicit approval that names the recipient/group being removed. |

## Actions Requiring Jack’s Direct Approval

Do not treat the following as routine, even if a broad assignment says “clean up Drive” or “share this.” Require a direct Jack approval in the current request:

- `--to anyone`, `--to domain`, or `--discoverable` sharing.
- Ownership transfer.
- Bulk permission changes.
- Permanent deletion with `gog drive delete --permanent`.
- Large moves or copies across clients.

## Trash and Recovery

`gog drive delete <fileId>` moves an item to trash by default. Do not use `--permanent` without Jack’s direct approval for the exact target. Before promising a restore, verify the recovery command available in the **installed** GOG schema or use the authorized Drive user interface. Never invent an undeclared raw API workaround.
