# Failure Handling

Stop safely. Do not solve an uncertain Drive state by guessing, repeating a write, widening a search, changing permissions, or creating a replacement file.

## Retry Rules

Retry only safe reads, metadata checks, lists, searches, and exports that failed with a temporary timeout, service error, or rate limit. Retry no more than three times with increasing delay.

For a write that times out or returns an unknown outcome, do **not** retry immediately. Inspect the target folder and file by stable IDs, expected name, parent folder, and recent modification time. Continue only after you can determine whether the first attempt succeeded.

## Stop Conditions

| Situation | Required response |
|---|---|
| Wrong or no approved account | Stop and ask for the correct approved account. |
| Authentication check fails | Report the account label and auth failure. Do not print tokens or edit GOG authentication. |
| Missing client or folder mapping | Stop and ask for the correct client code or registry update. |
| Several plausible files | Show the candidates and ask the user to choose. |
| File or folder ancestry cannot be proven | Stop. Do not read, write, or move the item. |
| Shortcut target is out of scope | Reject it and explain that the target is outside the approved client area. |
| Existing file would be replaced | Show a preview and obtain approval for the exact file ID. |
| Version conflict during replacement | Re-read the file and ask for direction. Do not overwrite a newer version. |
| Local source is outside task workspace | Stop. Do not upload it. |
| Content is too large or binary | Return metadata and the Drive link. Ask for a narrower request or use a dedicated capability. |
| Unapproved external sharing or deletion | Stop and request the required approval. |

## Escalate and Record

Write a private failure receipt with the safe error category, action, stable IDs where allowed, and next required decision. Do not include client content, token values, secret paths, or raw error dumps.

Create a GitHub issue only for a technical Skill defect, GOG incompatibility, failed deployment, security concern, test failure, or rollback event. Do not create a GitHub issue for an ordinary client-file access denial or routine Drive action.
