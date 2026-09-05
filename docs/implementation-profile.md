# z-drive-gog Implementation Profile

Date: 2026-09-05 | Prepared by: Manus | Status: Release Candidate, pilot pending

## Identity and Ownership

| Field | Value |
|---|---|
| Skill display name | z-drive-gog |
| Canonical identifier | z-drive-gog |
| Owner or publisher | ZedBiz / Jack |
| Repository | https://github.com/ZedBiz44/z-drive-gog-Skill |
| Authoritative branch | main |
| License or attribution decision | Original ZedBiz skill guidance. GOG command names and behavior are referenced from OpenClaw gogcli documentation. |
| Naming exception | None. |

## Purpose and Scope

| Field | Value |
|---|---|
| Primary job | Use GOG to find, read, export, save, organize, share, trash, and recover approved Google Drive client files and folders. |
| Intended users | ZedBiz AI agents working with approved Google accounts and client folders. |
| Positive triggers | Requests to locate, read, export, upload, create, copy, rename, move, archive, share, or remove Drive artifacts and folders. |
| Requests that must not trigger | GitHub source work, code, Skills, infrastructure, technical issues, Notion planning, SOPs, decisions, secrets, or general unrelated research. |
| Included actions | Read, export, upload, create folder, copy template, rename, move, archive, guarded overwrite, guarded sharing, recoverable trash, and verified receipt logging. |
| Excluded actions | Credential administration, broad Drive-wide discovery, background sync/watchers, undocumented raw Drive operations, public sharing without approval, ownership transfer without approval, bulk permissions without approval, and permanent deletion without approval. |

## Platforms and Packaging

| Field | Value |
|---|---|
| Supported platform | OpenClaw using the installed GOG client. |
| Authoring source path | GitHub repository `ZedBiz44/z-drive-gog-Skill`. |
| Deployable package path | `dist/z-drive-gog/` generated from the repository. |
| Required platform adapters | None. This is an OpenClaw-only skill. |
| Target installation locations | Confirm the pilot agent’s active OpenClaw skill root before installation. |
| Platform validators | `validate_skill.py`, package validation, `openclaw skills list`, fresh-session trigger tests, and live Drive verification. |

## Controls and Approval

| Field | Value |
|---|---|
| Default operating mode | Complete Drive operation skill. Routine reversible work is authorized only where the current assignment clearly calls for it. |
| Human approver | Jack. |
| Pilot agent or environment | To be selected by Jack before deployment. Use a non-production test-client folder and an approved account. |
| Wider rollout rule | Stop after one agent completes the full evidence sequence. Jack approves any rollout beyond that agent. |
| Stop and escalation conditions | Wrong account, missing client mapping, failed boundary proof, unresolved shortcut target, unknown write outcome, unapproved risky action, leaked data, schema mismatch, or content safety issue. |
| Retry limit | Three retries for temporary read failures only. Never blindly retry an uncertain write. |

## Security and Rollback

| Field | Value |
|---|---|
| Security review record | [security-rollback-review.md](security-rollback-review.md) |
| Approved data and source boundaries | Selected account, configured client folder tree, approved task workspace, configured templates, and private runtime registry. |
| Approved execution boundaries | Installed GOG command schema, constrained argument arrays, private cache and receipt log, and explicit approval gates. |
| Last known-good commit or release | Pending initial validated commit. |
| Rollback owner | Jack authorizes; responsible technical agent executes. |
| Verified rollback or removal procedure | Defined in the security review; confirm during the first pilot. |

## Completion Evidence

| Field | Evidence |
|---|---|
| Structural validator result | Pending build validation. |
| Platform validator result | Pending target-agent installation. |
| Trigger-test record | [pilot-test-record.md](pilot-test-record.md) |
| Pilot result | Pending. |
| Deployed commit or release | Pending. |
| GitHub issue or change record | To be created at task completion. |
| Notion operational summary | Requested z-Skills SOP database entry. |
| Final approver and date | Pending Jack approval for pilot deployment and later wider rollout. |
