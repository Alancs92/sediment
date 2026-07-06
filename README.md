# sediment

A personal, local-first ambient-capture pipeline: it captures meetings,
continuous desktop/audio context, and coding-agent sessions; normalizes them
into a daily record; syncs the useful bits into Notion; and archives raw
media cheaply.

**Status: early implementation.** The aggregator (phase 3, `aggregator/`) is
scaffolded, tested, and containerized, but still runs against sample data —
Meetily and Screenpipe (phases 1-2) haven't been set up on a real machine
yet, so there's no real capture data to feed it. See
[`docs/implementation/README.md`](docs/implementation/README.md) for status.

## Components (planned)

| Component | Captures | Output |
|---|---|---|
| Meetily | Meeting audio (calendar/manual-triggered) | Markdown/SQLite transcript + summary per meeting |
| Screenpipe | Screen + system audio + mic, 24/7 | Local SQLite: frames, transcripts, app/window context |
| Coding-agent session log | Final output of every agent session | Existing structured DB |
| Ollama (local) | — | Summarization/embedding, daily digest generation |
| Notion (via MCP) | — | Daily Log, Meeting Notes, Tasks, Dev Sessions |

See [`docs/architecture/ambient-capture-architecture.md`](docs/architecture/ambient-capture-architecture.md)
for the full design, including why these tools don't overlap and how they're
wired together.

## Documentation

Start at [`docs/README.md`](docs/README.md) — it maps every doc in this repo.

If you're an AI coding agent, start at [`AGENTS.md`](AGENTS.md) instead.

## Build order

See [`docs/implementation/README.md`](docs/implementation/README.md) for the
phased build plan and current status of each phase.

## Getting started

- Setting up Meetily/Screenpipe/Ollama on your own machine:
  [`docs/setup/`](docs/setup/)
- Running the aggregator (Docker or local Python):
  [`aggregator/README.md`](aggregator/README.md)

## Contributing

Every change — human or agent — follows the standards in
[`docs/standards/`](docs/standards/) (TDD, security, code review) and records
non-trivial decisions in [`docs/decisions/`](docs/decisions/).
