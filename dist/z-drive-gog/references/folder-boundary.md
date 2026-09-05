# Client Folder Boundary

The client root folder in the private registry is the boundary for both reads and writes. A result is valid only when the Skill can prove that it belongs to that root folder or a nested subfolder of that root.

## Resolve Files Safely

- Use a supplied file ID when available. Otherwise, search only in the selected client folder.
- Treat names as hints. If the search returns several plausible files, show the list and ask the user to choose.
- Inspect each candidate with `gog drive get <fileId> --json` before reading or changing it.
- Confirm the item is not trashed unless the task specifically concerns the trashed item.
- Check the item’s parent IDs and walk each parent upward until reaching the configured client root. Stop if the chain cannot be read, reaches a different root, crosses an unexpected Shared Drive, or loops.
- `gog drive search --parent <folderId>` searches direct children. Do not treat this filter alone as proof that a deeply nested item is inside the client tree.

## Shortcuts

A shortcut is not the item itself. Read shortcut metadata, identify its target ID, and run the full metadata and ancestry check again against the target.

Reject the shortcut when its target is outside the client tree, its target cannot be inspected, or the target lives in a different Shared Drive than the configured client scope. Do not copy, move, share, or trash a shortcut target just because the shortcut sits in an approved folder.

## Shared Drives

For a client in My Drive, use `--no-all-drives` for normal searches. For a client in a configured Shared Drive, use `--drive <sharedDriveId>` and verify that the result belongs to the configured Shared Drive as well as the client folder tree.

Do not search every accessible Shared Drive by default. Do not change Shared Drive membership, settings, or ownership through this Skill.

## Validate Write Destinations

Before an upload, folder creation, copy, or move, validate the destination folder ancestry to the same client root. For a move or copy, validate **both** source and destination. Cross-client movement is a high-risk action and requires a preview and approval.

## “Latest” and Similar Names

When asked for “latest,” sort candidate items by `modifiedTime` descending and show the most recent items with dates. If the top candidates are tied or materially unclear, ask for a selection. Never assume that the first ordinary search result is the newest or correct file.
