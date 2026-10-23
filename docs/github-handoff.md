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

Import commit: `2de7bf5bce33e24c98177c1d0e858a3084d08244`; local and GitHub `main` SHAs matched after the initial push. This completion record follows in a documentation-only commit.
Status: complete. GitHub confirms private visibility, standalone repository, and default branch `main`. `origin` points to the user's repository; `upstream` points to Sackmann's source. The local `codex/github-project-import` branch tracks `origin/main`. All 169 pre-existing upstream deletions remain unstaged; the remote retains those original files. No generated models or processed state were uploaded. The import preserves existing source formatting, including pre-existing whitespace warnings.
Next action: deploy the Margins static release to the chosen host. No GitHub backup blocker remains; website hosting remains separate.

## Public visibility — 2026-10-23

User authorized public visibility conditional on checking credentials and related security concerns. GitHub now confirms `isPrivate=false`; the repository remains standalone with the original upstream history preserved.

Gitleaks 8.30.1 scanned all local refs: 488 commits containing changes, approximately 1.14 GB, in 2m8s. The two findings are false positives: public Match Charting Project identifiers assigned to variables named `KEY`/`key` in `docs/research/wimbledon_case_probe.py` and `docs/research/2026-10-21-external-discovery.md`. Separate documentation and GUI directory scans reproduced these identifiers and additionally flagged a local design-questionnaire cache key under `.impeccable/questions/seeds/`; its surrounding object contains design selection IDs, not authentication configuration. No actual credentials were identified. The static release directory scan found no leaks. Redacted raw reports remain ignored under `reports/security/`.

Tracked filenames were checked for environment files, credential files, private keys and database files; none were found. Normal Git author details and workstation paths in historical development notes remain visible. A pattern-based credential scan is not an exhaustive application security audit. `SECURITY.md` records the local-only prediction-server and trusted-pickle boundaries; public source availability does not authorize exposing that server.

Acceptance: public visibility verified by GitHub API; finish by pushing the security-boundary document and this record, then compare local and remote commit SHAs. Next action remains static website hosting.
