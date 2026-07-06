# sediment-aggregator

Phase 3 of `docs/implementation/README.md`: merges Meetily + Screenpipe
capture for a day, dedupes overlapping audio, summarizes via local Ollama,
and writes a local markdown file. No Notion sync yet — that's phase 4.

See `docs/decisions/0003-aggregator-v0-container-and-adapters.md` for why
this reads a normalized JSON export rather than Meetily/Screenpipe's real
on-disk schema (not confirmed yet), and why it ships as a single container.

## Local development

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/ruff check src tests
.venv/bin/pytest
```

Run against the test fixtures (no real Ollama needed if you just want to see
dedupe/parsing work — summarization calls will fail without a running
Ollama):

```bash
MEETILY_EXPORT_DIR=tests/fixtures/meetily \
SCREENPIPE_EXPORT_DIR=tests/fixtures/screenpipe \
OUTPUT_DIR=/tmp/sediment-output \
.venv/bin/python -m sediment_aggregator run --date 2026-07-06
```

## Running via Docker

```bash
cp .env.example .env        # then edit it
mkdir -p data/meetily data/screenpipe data/output
docker compose up --build   # add --profile with-ollama to run Ollama in this stack too
```

This starts the scheduler (`serve`), which runs the pipeline daily at
`DAILY_RUN_TIME` and exposes:

- `GET http://localhost:8420/healthz` — liveness
- `GET http://localhost:8420/status` — last run time/result, next scheduled run

For a one-off run instead of the scheduler:

```bash
docker compose run --rm aggregator python -m sediment_aggregator run --date 2026-07-06
```

## Feeding it real data

Nothing produces the expected JSON export format yet (see `src/sediment_aggregator/sources/file_based.py`
for the exact shape) — Meetily and Screenpipe need to be running first
(phases 1-2). Until a real adapter exists, export their data into that
shape by hand or with a small script, drop it under
`data/meetily/<YYYY-MM-DD>.json` / `data/screenpipe/<YYYY-MM-DD>.json`, and
the aggregator will pick it up on its next run.

## Testing

Follows `docs/standards/testing.md`: `dedupe.py` (the highest-risk logic) has
the most thorough coverage, external boundaries (`ollama_client.py`, the
file-based sources) are tested against mocks/fixtures rather than live
services, and `pipeline.py`/`writer.py` are tested for idempotency.
