# GitHub project backup — 2026-10-23

Task: push the full ATP project, including the Margins website, to the user's GitHub account.

Base commit: `2c40e40c0f3ac51cc11eabe6c7c25932234e83e0`.
Destination: private standalone `zvonimir-rezo/tennis_atp`, preserving upstream commit history. A GitHub fork of the public source would have to be public. Keep JeffSackmann/tennis_atp as the upstream remote.

Acceptance checks:

- Commit the project source, notebooks, documentation, assets and static release builder.
- Preserve the pre-existing upstream file deletions as unstaged local changes.
- Exclude ignored models, processed data, release archives, caches and reports.
- Verify the Margins release build and compare the pushed commit with local HEAD.

Results before push: scanned 198 project files; no credential pattern matches or files above 25 MiB. Margins builder passed: 33 release files, 49 local references, ZIP SHA256 `1c5ac5c38d4d1eefdd3797f04a4b371227fffadfd2e89c740a2a67044a3429bb`.

Current commit: the commit containing this handoff record (resolve with `git log -1 -- docs/github-handoff.md`).
Status: prepared for initial push; final remote verification is reported in the chat.
Next action: create the private destination, push the import commit as `main`, and verify its SHA and visibility. Website hosting remains separate.
