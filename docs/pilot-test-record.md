# z-drive-gog Pilot and Trigger-Test Record

Date: 2026-09-05 | Tester: Pending | Status: Planned

## Artifact and Environment

| Field | Value |
|---|---|
| Skill identifier | z-drive-gog |
| Repository and commit or release | Pending initial validated commit. |
| Deployable package path | `dist/z-drive-gog/` |
| Platform and version | OpenClaw and installed GOG version, to be recorded at pilot start. |
| Pilot agent or environment | Pending Jack selection. |
| Installation path | Confirm before installation. |
| Fresh session or restarted gateway confirmed | Pending. |

## Discovery Check

| Check | Result | Evidence |
|---|---|---|
| Package installed from current commit | Planned | Record deployed commit and package checksum or path. |
| Skill appears in the platform skill list | Planned | Capture `openclaw skills list` result. |
| Expected metadata is visible | Planned | Record visible name and description. |

## Trigger Tests

| Test type | Prompt | Expected behavior | Actual result | Evidence |
|---|---|---|---|---|
| Positive | “Find the latest Acme report in Drive.” | Skill loads and asks for the correct client scope if missing. | Pending | Pending |
| Paraphrased positive | “Put this final PDF in the client’s Drive folder.” | Skill loads, confirms account/client folder, validates local file, uploads, and verifies the link. | Pending | Pending |
| Boundary | “Move the report from Acme to Beta.” | Skill identifies cross-client transfer as requiring a preview and approval. | Pending | Pending |
| Negative | “Update the agent Dockerfile.” | Skill does not load and routes technical source work to GitHub. | Pending | Pending |

## Full Drive Workflow Test

Use harmless test artifacts in a non-production client folder. Verify every result by returned file ID and live Drive state.

| Step | Required evidence | Result |
|---|---|---|
| Read | Correct account, client folder, file ID, link, and content limit. | Pending |
| Create | New test file in the correct folder. | Pending |
| Verify | Live metadata shows expected name, ID, parent, and link. | Pending |
| Rename | Same ID with requested name. | Pending |
| Move | Same ID under a permitted test subfolder. | Pending |
| Copy template | New ID, expected name, expected parent, original template unchanged. | Pending |
| Export | Expected local export, source ID, and modification time. | Pending |
| Trash | Test file appears in trash without permanent deletion. | Pending |
| Recover | Recovery path works in the installed GOG version or approved Drive interface. | Pending |
| Shortcut boundary | Shortcut target inside scope is accepted; shortcut to outside scope is rejected. | Pending |

## Rollback Readiness

| Field | Value |
|---|---|
| Last known-good commit or release | Initial deployment has no predecessor. Record the first validated commit before installation. |
| Verified rollback or removal method | Remove generated package, refresh OpenClaw discovery, and restore prior package or commit if one exists. |
| Rollback test performed | Pending. |

## Sign-Off

- Tester: Pending
- Reviewer: Pending
- Approver: Jack
- Deployment decision: Pending evidence review
