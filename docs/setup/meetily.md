# Meetily (meeting audio capture)

Phase 1 of `docs/implementation/README.md`. Meetily is the source of truth
for meeting audio per `docs/decisions/0002-initial-ambient-capture-architecture-decisions.md`
— structured, speaker-aware summaries, purpose-built for meetings.

This project doesn't vendor or link a specific Meetily download — install
it from wherever you sourced it originally, and fill in the exact steps
your version needs below once you've done it once. What matters for the
rest of this pipeline is the output shape, not the install mechanics.

## Install & configure (fill in as you go)

1. Install the app for your OS.
2. Point its transcription backend at Whisper.cpp/Parakeet as documented by
   the tool itself.
3. Point its summarization backend at your local Ollama (see
   [`ollama.md`](ollama.md)) — same model you're already running.
4. Run it against a few real meetings and sanity-check summary quality
   before moving on (this is the acceptance bar for phase 1 in
   `docs/implementation/README.md` — update that table once done).

## What the aggregator needs from it

The aggregator (`aggregator/`) doesn't read Meetily's native storage yet —
see `docs/decisions/0003-aggregator-v0-container-and-adapters.md`. For now,
export each day's meetings into the JSON shape documented in
`aggregator/src/sediment_aggregator/sources/file_based.py`
(`{title, start, end, transcript, summary}` per meeting) under
`aggregator/data/meetily/<YYYY-MM-DD>.json`. Once Meetily's real on-disk
schema is confirmed, replace this manual export step with a proper adapter
behind the same `MeetilySource` interface.

## Note on overlap with Screenpipe

Per the architecture doc, Screenpipe also captures all system audio,
including meetings — that's intentional redundancy at this stage (see
`docs/setup/screenpipe.md` and ADR 0002). Don't try to suppress Screenpipe's
audio during meetings yet; the aggregator's dedupe logic handles the overlap.
