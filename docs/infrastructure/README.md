# Infrastructure

CI/CD, environments, secrets management, and deployment/runtime concerns.

**Status: placeholder.** This repo currently has no application code, so
there is no CI pipeline, deployment target, or runtime environment to
document yet. Do not fabricate infrastructure that doesn't exist — fill in
the sections below as each piece is actually built, and link the PR that
introduced it.

## What needs to be documented here once implementation starts

- **CI pipeline**: what runs on every PR (lint, tests per
  `docs/standards/testing.md`, any security scanning), which platform
  (e.g. GitHub Actions), and what blocks a merge.
- **Runtime environment(s)**: this is a local-first, single-user system per
  the architecture doc — document which machine(s) it's expected to run on
  (personal vs. work machine, per the licensing note in
  `docs/architecture/ambient-capture-architecture.md` §4), OS assumptions,
  and how the aggregator is scheduled (cron/launchd).
- **Secrets management**: how Notion API tokens, Ollama Cloud keys, and
  Backblaze B2 credentials are supplied to the aggregator at runtime (env
  vars via `.env`, OS keychain, etc.) — see `docs/standards/security.md`.
- **Scheduled jobs**: the daily aggregator run and the (deferred) weekly
  archival job — where they're defined, how failures are surfaced.
- **Dependency/version management**: how the aggregator's dependencies
  (Python, per ADR 0002) are pinned and updated.

## Current status

| Area | Status |
|---|---|
| CI pipeline | Not set up |
| Deployment/runtime | Not set up |
| Secrets management | Not set up |
| Scheduled jobs | Not set up |
