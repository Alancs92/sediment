# sediment

A personal, local-first ambient-capture pipeline: it captures meetings,
continuous desktop/audio context, and coding-agent sessions; normalizes them
into a daily record; syncs the useful bits into Notion; and archives raw
media cheaply.

**Status: documentation only.** This repository currently contains only
architecture and process docs — no application code has been written yet.
Implementation will land on separate branches once the docs here are settled.

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

## Contributing

Every change — human or agent — follows the standards in
[`docs/standards/`](docs/standards/) (TDD, security, code review) and records
non-trivial decisions in [`docs/decisions/`](docs/decisions/).
