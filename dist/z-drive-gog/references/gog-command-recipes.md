# GOG Command Recipes

Follow `z-files-folders` for naming, placement and copy-first migrations. Direct move/archive/delete examples below do not authorize skipping copy verification or deleting migration sources. For migration: copy, verify, then archive the retained original; hold that item if verification or archive access is missing. Preserve the approved account, project boundary, permissions and receipts.

Use these as patterns. Before executing a command, check `gog schema --json` on the target agent because installed GOG versions may differ. Set `ACCOUNT` from the private runtime registry. Use `--json --no-input --wrap-untrusted` for agent execution.

## Inspect and Search

```bash
# Inspect file or folder metadata.
gog drive get "$FILE_ID" --account "$ACCOUNT" --json --no-input --wrap-untrusted

# Search direct children of a known My Drive folder.
gog drive search "monthly report" --parent "$FOLDER_ID" --no-all-drives --max 20 --account "$ACCOUNT" --json --no-input --wrap-untrusted

# Pass through an exact Drive query after checking syntax.
gog drive search "name contains 'report' and trashed = false" --raw-query --parent "$FOLDER_ID" --no-all-drives --max 20 --account "$ACCOUNT" --json --no-input --wrap-untrusted

# Search a configured Shared Drive.
gog drive search "proposal" --parent "$FOLDER_ID" --drive "$SHARED_DRIVE_ID" --max 20 --account "$ACCOUNT" --json --no-input --wrap-untrusted

# Print a browser-ready Drive link for a resolved file ID.
gog drive url "$FILE_ID" --account "$ACCOUNT" --json --no-input
```

A `--parent` search is a direct-child scope. Use the folder-boundary procedure to prove nested ancestry before acting on a deep result.

## Download and Export

```bash
# Export a Google Doc to Markdown.
gog drive download "$FILE_ID" --format md --out "$OUTPUT_PATH" --account "$ACCOUNT" --json --no-input --wrap-untrusted

# Export a Google-native item to PDF.
gog drive download "$FILE_ID" --format pdf --out "$OUTPUT_PATH" --account "$ACCOUNT" --json --no-input --wrap-untrusted

# Export a Sheet first tab as CSV only when that meets the request.
gog drive download "$FILE_ID" --format csv --out "$OUTPUT_PATH" --account "$ACCOUNT" --json --no-input --wrap-untrusted
```

Google Docs support Markdown export. CSV or TSV export from Google Sheets covers only the first tab, so use the Sheets Skill for multi-tab work.

## Routine Create and Organize Work

```bash
# Upload a new local file into the approved folder.
gog drive upload "$LOCAL_PATH" --parent "$FOLDER_ID" --name "$FILE_NAME" --account "$ACCOUNT" --json --no-input --wrap-untrusted

# Create a folder inside the approved client tree.
gog drive mkdir "$FOLDER_NAME" --parent "$FOLDER_ID" --account "$ACCOUNT" --json --no-input --wrap-untrusted

# Copy a template. Never edit a master template.
gog drive copy "$TEMPLATE_ID" "$NEW_NAME" --parent "$FOLDER_ID" --account "$ACCOUNT" --json --no-input --wrap-untrusted

# Rename an identified file.
gog drive rename "$FILE_ID" "$NEW_NAME" --account "$ACCOUNT" --json --no-input --wrap-untrusted

# Move an identified file after validating source and destination boundaries.
gog drive move "$FILE_ID" --parent "$DESTINATION_FOLDER_ID" --account "$ACCOUNT" --json --no-input --wrap-untrusted
```

## Guarded Replace, Share, and Trash

Run `--dry-run` first, show a preview, and wait for explicit approval before these commands.

```bash
# Replace only the exact approved file. Prefer --if-version when available.
gog drive upload "$LOCAL_PATH" --replace "$FILE_ID" --if-version "$KNOWN_VERSION" --account "$ACCOUNT" --json --no-input --wrap-untrusted

# Share with an approved named person. Do not add --notify unless the assignment requires it.
gog drive share "$FILE_ID" --to user --email "$RECIPIENT_EMAIL" --role reader --account "$ACCOUNT" --json --no-input --wrap-untrusted

# Move to trash. Never add --permanent without direct Jack approval.
gog drive delete "$FILE_ID" --account "$ACCOUNT" --json --no-input --wrap-untrusted
```

`--to anyone`, `--to domain`, `--discoverable`, and `--permanent` require Jack’s direct approval. Do not put user-provided strings into a shell command. Build commands as argument arrays in `scripts/drive_guard.py`.
