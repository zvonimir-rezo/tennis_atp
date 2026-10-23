# Security boundaries

The deployable Margins website is a static release built with `python3 scripts/build_study_release.py`. Publish only the contents of `reports/releases/margins-static/`. It requires no credentials, environment variables, database or prediction API. The historical match evidence included in that release is intentionally public.

`gui_server.py` is a localhost development tool for the separate prediction prototype. It serves the repository root through Python's simple HTTP handler. Do not expose it to the public internet or deploy the full repository as a static directory: that could disclose project files and generated artifacts. Public prediction hosting requires a separate server and deployment review.

The prediction prototype loads local pickle artifacts. Only load artifacts produced by a trusted source; pickle files can execute code when loaded. Generated models, processed player states and reports are excluded from Git.

Keep API tokens, passwords, private keys and account configuration out of source files, notebooks, screenshots, commit messages and Git history. Public source availability does not establish that the prediction service is ready for production.
