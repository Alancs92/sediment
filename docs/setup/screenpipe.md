# Screenpipe (continuous screen + audio capture)

Phase 2 of `docs/implementation/README.md`. Runs 24/7 in the background,
capturing screen (OCR/accessibility tree) and system audio/mic — this is
the thing Meetily doesn't do, per
`docs/architecture/ambient-capture-architecture.md` §1.

As with Meetily, install from wherever you sourced Screenpipe originally;
this doc focuses on the configuration that matters for this project, not
install mechanics.

## Before you turn on 24/7 capture: the deny-list

Per `docs/standards/security.md` and the architecture doc §4: configure
Screenpipe's `deny-apps`/`allow-apps` filtering **at the daemon/global config
level**, not only per-pipe, so a new pipe can't accidentally capture
identifiable/clinical data just because someone forgot to filter it there
too. The exact config key names depend on your installed version — check
Screenpipe's own config reference — but the shape is typically something
like:

```toml
# example only — confirm exact keys/format against your installed version
[capture]
deny-apps = ["Epic", "<your EHR app name>", "<internal tools showing patient data>"]
```

Do this **before** the daemon starts running continuously, not after.

## License / commercial-use check

Screenpipe's license (at the time the architecture doc was written) is
source-available: free for personal/non-commercial use, paid for commercial
use. If this machine is work-owned, confirm with your employer's device/data
policy and the license terms before running 24/7 capture on it — see
`docs/standards/security.md`. Prefer a personal machine to sidestep the
question entirely.

## Verify before adding pipes

Let it run untouched for a few days first to gauge storage growth and CPU
load (this is the acceptance bar for phase 2 in
`docs/implementation/README.md` — update that table once done) before
enabling pipes like `day-recap` or `ai-prompt-journal`.

## What the aggregator needs from it

Same as Meetily: the aggregator's v0 adapter reads a normalized JSON export,
not Screenpipe's native SQLite/REST API directly (see
`docs/decisions/0003-aggregator-v0-container-and-adapters.md`). Export each
day's segments into the shape documented in
`aggregator/src/sediment_aggregator/sources/file_based.py`
(`{start, end, app, window_title, ocr_text, audio_transcript}` per segment)
under `aggregator/data/screenpipe/<YYYY-MM-DD>.json`, until a real adapter
against Screenpipe's local REST API (`localhost:3030` per the architecture
doc) replaces this step.
