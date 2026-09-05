# Drive Search Cheat Sheet

Start inside the approved client folder. Keep searches small and specific. Use `--max 20` or fewer results. Then inspect candidate metadata and prove the folder boundary before using a result.

## Search Patterns

| Request | First search approach | What to verify next |
|---|---|---|
| Exact known file | Search the full file name in the client folder. | File ID, parent, modification time, and trashed state. |
| Latest report | Search `report` in the client folder. | Sort candidates by `modifiedTime` descending and show the recent options. |
| PDF proposal | Search `proposal` in the client folder. | MIME type, active state, and client ancestry. |
| File made this month | Search a narrow phrase, then use a raw Drive query only if needed. | Date, client tree, and matching deliverable type. |
| Folder | Search the known folder name. | Confirm it is a folder and trace parents to client root. |
| Template | Use the configured template ID whenever possible. | Confirm the master template is not being edited. |

## Basic Commands

```bash
# Narrow full-text search in the client root.
gog drive search "proposal" --parent "$CLIENT_ROOT_ID" --no-all-drives --max 20 --account "$ACCOUNT" --json --no-input --wrap-untrusted

# Drive query language after the query has been checked.
gog drive search "name contains 'report' and trashed = false" --raw-query --parent "$CLIENT_ROOT_ID" --no-all-drives --max 20 --account "$ACCOUNT" --json --no-input --wrap-untrusted

# Inspect the final candidate.
gog drive get "$FILE_ID" --account "$ACCOUNT" --json --no-input --wrap-untrusted
```

For a configured Shared Drive, replace `--no-all-drives` with `--drive "$SHARED_DRIVE_ID"`.

## Never Do This

Do not search all of Drive for a generic term such as `invoice`, `report`, or `proposal`. Do not pick the first result without checking its client folder, modification date, and file ID. Do not use a file name as a later write target when an ID is available.
