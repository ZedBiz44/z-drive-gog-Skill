# Bounded correction verification

Owner: Cody. Reviewer and merge/install decision: Jack. Status: implemented candidate; not installed or deployed.

Scope excludes production WordPress writes, deployment, new providers, consolidation, storage migration and skill retirement. Rollback before merge is closing the PR; existing installations remain unchanged. After a future authorized installation, restore the previous approved package if the pilot fails.

Base: 830cf6d0e1d58c65b0ee161566bc1d0a7e7bf8a0. Branch: cody/align-file-governance; target: main.

Naming and placement now explicitly defer to z-files-folders and its current authorities. Removed the competing spaced/date filename from the main skill, operations reference and human SOP. Clarified migration precedence in README, operations, approval rules and command recipes: copy, verify, then archive the retained original. Do not delete migration sources or substitute a direct move. Ordinary authorized operations outside migration remain available. Account, ancestry, access, private receipts and sharing/deletion permissions remain in force. No helper behavior changed.

Validation: reviewed a routine save, explicit routine move, migration with successful verification, failed verification, missing archive and cross-owner case against the unchanged governing skill. Migration failures retain originals and hold the affected item; normal work retains its existing authorization. This is an instruction review, not a live Drive experiment. ZedBiz repository and native package validators passed. Built package has 14 source-matching files (see manifest); checked tracked distribution updated with source. No Drive files were moved, copied or renamed. Live runtime loading and workflow execution remain untested.

