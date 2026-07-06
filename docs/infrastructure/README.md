# Infrastructure

CI/CD, environments, secrets management, and deployment/runtime concerns.

## CI pipeline

`.github/workflows/aggregator-ci.yml` runs on every push/PR touching
`aggregator/`:
- `ruff check` (lint)
- `pytest` with coverage
- `docker build` of `aggregator/Dockerfile`, to catch packaging breakage
  separately from test breakage

Nothing merges to `main` with a red run. As new components are added
alongside `aggregator/`, give each its own workflow file scoped by `paths:`
rather than growing one monolithic pipeline.

## Runtime environment

Local-first, single-user, per the architecture doc. The aggregator
(`aggregator/`) runs as a single Docker container via
`aggregator/docker-compose.yml`:
- `serve` mode (the default `CMD`) runs the pipeline on a daily schedule
  and exposes `/status` + `/healthz` for monitoring.
- An optional `ollama` service can run in the same compose stack
  (`--profile with-ollama`), or you can point `OLLAMA_BASE_URL` at Ollama
  running on the host instead.
- Meetily and Screenpipe themselves are **not** containerized — they need
  direct mic/screen access and run natively on whichever machine per
  `docs/setup/meetily.md` / `docs/setup/screenpipe.md` and the
  license/work-machine note in `docs/standards/security.md`.

## Secrets management

Supplied via `aggregator/.env` (gitignored; `aggregator/.env.example`
documents the variable names, no values). Today that's just Ollama
connection settings — no Notion/B2 credentials yet, since phases 4 and 6
haven't landed. When they do, add the new variables to `.env.example` and
this doc, never hardcode them, per `docs/standards/security.md`.

## Scheduled jobs

- **Daily aggregation**: handled in-process by `aggregator`'s `serve` mode
  (`DAILY_RUN_TIME` in `.env`) — no external cron needed when running via
  Docker Compose.
- **Weekly archival to B2**: not built yet (implementation phase 6).

## Dependency management

`aggregator/pyproject.toml` pins direct dependencies with lower bounds
(`>=`); no lockfile yet given the small dependency set. Revisit (e.g. add
`pip-compile` output) if the dependency surface grows.

## Current status

| Area | Status |
|---|---|
| CI pipeline | `aggregator-ci.yml` — lint, test, docker build |
| Deployment/runtime | Docker Compose, single container (`aggregator/`) |
| Secrets management | `.env` file, gitignored, no secrets in use yet |
| Scheduled jobs | In-process daily scheduler in `aggregator`; weekly archival not built |
