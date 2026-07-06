# 0003. Aggregator v0: container packaging and file-based adapters

Status: Accepted

## Context

Phase 3 of the implementation plan ("Aggregator v0") is the first real code
in this repo. Two open questions needed answers before writing it:

1. Meetily's and Screenpipe's actual on-disk/API schemas aren't confirmed —
   phases 1-2 (installing and running those tools) haven't happened yet.
   Building adapters against a guessed schema risks baking in wrong
   assumptions that are expensive to unwind later.
2. The user wants something easy to run and monitor without managing a
   Python environment by hand, given this runs unattended on a personal
   machine.

## Decision

- **The aggregator's core (dedupe, summarization, orchestration, output)
  is built against a normalized internal data model** (`models.py`), with
  Meetily/Screenpipe access behind a `Protocol` interface (`sources/base.py`).
- **The only concrete adapter shipped in v0 reads a normalized JSON export**
  (`sources/file_based.py`) rather than a real SQLite/REST integration.
  Real adapters get written once phases 1-2 are running and the actual
  schema is known — this avoids guessing Meetily's SQLite schema or
  Screenpipe's REST API shape and hardcoding something wrong.
- **The aggregator ships as a single Docker container**, run via
  `docker compose up`, with:
  - a `run` mode for one-shot invocation (useful for testing/manual runs),
  - a `serve` mode that schedules the daily run and exposes `/status` and
    `/healthz` over plain HTTP (stdlib `http.server`, no framework
    dependency) so it can be checked with `curl` without extra tooling.
  - an optional `ollama` service in the same compose file (profile-gated)
    for users who don't already run Ollama on the host.

## Consequences

- The aggregator is directly testable and already has full unit/integration
  coverage (dedupe edge cases, idempotent writes, mocked Ollama/HTTP) without
  needing Meetily or Screenpipe actually installed anywhere.
- Real data can't flow through it yet. Whoever wires up phases 1-2 must
  either add an export step that emits the normalized JSON shape, or write a
  new adapter behind the same `MeetilySource`/`ScreenpipeSource` interfaces
  and update `docs/implementation/README.md` — this ADR does not need to be
  superseded for that, since the interfaces were designed for exactly this
  swap, but a new ADR should record whatever the real schema turns out to be
  if it surprises the assumptions above (e.g. if Meetily can't reasonably
  export per-day files).
- `dedupe.py` fails safe (keeps data on ambiguous overlap) per
  `docs/standards/security.md`'s least-surprise principle and
  `docs/standards/testing.md`'s risk ranking.
