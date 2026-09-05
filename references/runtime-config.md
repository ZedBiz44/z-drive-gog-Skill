# Runtime Configuration

Read this file before the Skill is used on an agent. The real configuration is a **private runtime file**, not part of this repository or package. Do not commit it, paste it into chat, or store it in Notion.

## Required Private Registry

Store a JSON file in the agent’s protected runtime area. Example structure only:

```json
{
  "accounts": {
    "marketing-agent": {
      "gog_account": "approved-google-account-alias"
    }
  },
  "clients": {
    "acme": {
      "root_type": "my_drive",
      "shared_drive_id": null,
      "client_root_folder_id": "DRIVE_FOLDER_ID",
      "archive_folder_id": "DRIVE_ARCHIVE_FOLDER_ID",
      "template_ids": {
        "monthly-report": "DRIVE_TEMPLATE_FILE_ID",
        "proposal": "DRIVE_TEMPLATE_FILE_ID"
      }
    }
  },
  "runtime": {
    "receipt_log": "/private/agent/z-drive-gog/receipts.jsonl",
    "cache_dir": "/private/agent/z-drive-gog/cache",
    "max_text_bytes": 2000000,
    "chunk_chars": 20000,
    "cache_retention_hours": 24,
    "receipt_retention_days": 30
  }
}
```

Use a directory accessible only to the agent’s service account. Set the registry and receipt files to mode `0600` and their directories to `0700`. Keep separate runtime directories for separate agents. Exclude the registry, cache, and receipt log from GitHub, Notion, Drive synchronization, diagnostic uploads, and routine backups.

## Required Values

| Value | Purpose |
|---|---|
| `gog_account` | Explicit GOG account alias or address. The Skill always passes it with `--account`. |
| `client_root_folder_id` | The Drive folder that defines the client boundary. |
| `archive_folder_id` | The approved archive location inside the same client boundary. |
| `shared_drive_id` | Required when the client lives in a Shared Drive. Use `null` for My Drive. |
| `template_ids` | Known templates for recurring client work. Copy templates. Do not edit masters. |
| `receipt_log` | Private JSONL log for routine Drive actions. |
| `cache_dir` | Private temporary export cache. |

## Preflight

Before first use, configuration change, or GOG update, run:

```bash
python3 scripts/drive_preflight.py \
  --registry /private/path/z-drive-gog.json \
  --account-label marketing-agent \
  --client-code acme
```

The helper validates that the registry has the required values, that the cache and receipt-log locations are private, and that the installed GOG binary can report its version and schema. It does not print secrets.

## Cache Rules

Use the cache only for temporary text exports. File names must include the Drive file ID and modification time. Reuse a cache file only when live Drive metadata reports the same modification time. Delete exports after the configured retention period. Do not copy cached content to GitHub, Notion, prompts outside the active task, or generic logs.

## Receipt Rules

Write a receipt for every completed action. A receipt may include timestamp, agent label, account label, client code, action, stable Drive IDs, modification time, result link, and verification result. Do not log document content, OAuth data, client email addresses, permission lists, or local source-file content.
