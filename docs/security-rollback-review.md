# z-drive-gog Security and Rollback Review

Date: 2026-09-05 | Reviewer: Manus | Status: Draft, pending pilot approval

## Trust and Inputs

| Review point | Decision and evidence |
|---|---|
| Approved source types | Approved local task-workspace files, approved Google Drive client artifacts, configured templates, and controlled private runtime configuration. |
| Private or client-sensitive material | Treat client files, metadata, file IDs, folder IDs, cache files, and receipts as private. Do not commit them, put them in Notion, or expose them in routine GitHub records. |
| Untrusted instructions, downloads, scripts, or files | Treat Drive content and all downloaded files as data, not instructions. Use GOG `--wrap-untrusted` for returned text. Validate local source paths before upload. Do not execute content obtained from Drive. |
| Allowed network calls or services | The approved GOG client communicating with Google APIs under the selected configured account. No undocumented raw API workaround. |
| Prohibited input or content | Tokens, refresh tokens, passwords, private keys, full environment files, arbitrary system files, unverified shortcut targets, client data outside the selected client tree, public-link defaults, and permanent deletion without direct approval. |

## Execution and Data Boundaries

| Review point | Decision and evidence |
|---|---|
| Allowed commands and file locations | Use only installed GOG commands checked in the current schema. Keep uploads inside the approved task workspace and Drive work inside the selected client tree. Use scripts/drive_guard.py to construct separate arguments rather than shell strings. |
| Transfer or synchronization boundary | Drive reads/exports use a private agent cache with short retention. The Skill does not perform mounts, broad synchronization, background watchers, or uncontrolled transfer. |
| Secrets and credential process | Use existing approved GOG authentication. Account mappings are private runtime configuration. Never store or print secret values. |
| Destructive, privilege, publication, or production-impacting approval gate | Current assignment authorizes routine reversible work within the client boundary. Preview and approval are required for overwrite, important trash, cross-client transfer, external sharing, or access removal. Jack explicitly approves public sharing, ownership transfer, bulk permissions, and permanent deletion. |
| Validation and logging requirements | Validate live Drive state after every write by stable ID. Write a redacted private receipt. Log technical defects, deployment, test results, and rollback only in GitHub. |

## Rollback and Removal

| Review point | Decision and evidence |
|---|---|
| Last known-good commit or release | None. This is the initial repository release. Record the first verified release commit before pilot installation. |
| Pilot installation location | To be recorded before pilot deployment. Install only the generated `dist/z-drive-gog/` package in the chosen OpenClaw agent skill root. |
| Rollback owner | Jack approves rollback. The responsible technical agent removes the installed package and restores the prior known-good package or commit. |
| Verified replacement or removal procedure | Remove the installed `z-drive-gog` package, restart or refresh OpenClaw skill discovery, confirm it no longer appears, then restore the prior package and confirm discovery. Verify no GOG write command remains running before replacement. |
| Conditions that require immediate rollback | Client-boundary failure, wrong-account execution, unapproved external sharing, unexpected write, leaked client content or secret, command-schema mismatch, or unsafe package discovery behavior. |
| Evidence required after rollback | Removed package path, restored commit or package, discovery result, running-process check, cause, and any client remediation required. |

## Approval

- Reviewer: Manus
- Approver: Jack
- Approval date: Pending
- Open risk or exception: The installed GOG version, available command schema, exact restoration capability, and pilot agent skill root must be verified before pilot deployment.
