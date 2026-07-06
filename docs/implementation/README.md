# Implementation plan & status

Phased build order, mirroring
[`docs/architecture/ambient-capture-architecture.md` §7](../architecture/ambient-capture-architecture.md#7-build-order).
Each phase should land on its own branch/PR — this repo has no application
code yet, so every phase below is `Not started`.

Update the status column as work lands. When a phase completes, link its PR
here and note any deviation from the original plan as a new ADR in
[`../decisions/`](../decisions/) rather than silently changing this table.

| # | Phase | Depends on | Status | Notes |
|---|---|---|---|---|
| 1 | Meetily running, Ollama summarization verified on real meetings | — | Not started | |
| 2 | Screenpipe installed, run untouched for a few days to measure storage/CPU | — | Not started | |
| 3 | Aggregator v0: Meetily + Screenpipe merge → local markdown, dedupe logic verified | 1, 2 | Not started | No Notion yet — verify dedupe before adding a destination |
| 4 | Notion MCP sync from aggregator output | 3 | Not started | |
| 5 | Coding-agent session join (timestamp-overlap) | 4 | Not started | |
| 6 | Archival to Backblaze B2 | 3 (needs real storage growth data) | Not started | Revisit sizing once a few months of real Screenpipe data exists |

## Definition of done, per phase

A phase is `Done` only when:
- Code + tests merged (per [`docs/standards/testing.md`](../standards/testing.md))
- Security checklist reviewed (per [`docs/standards/security.md`](../standards/security.md))
- Any new decision recorded as an ADR
- This table updated in the same PR
