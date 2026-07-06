# Setup guides

These cover phases 1-2 of `docs/implementation/README.md` — getting Meetily
and Screenpipe running on your own machine. None of this runs in a cloud/CI
environment: both tools need local mic/screen access, so you run these
yourself, not an agent.

| Guide | Covers |
|---|---|
| [`ollama.md`](ollama.md) | Local Ollama, needed by both Meetily and the aggregator. |
| [`meetily.md`](meetily.md) | Meeting audio capture (phase 1). |
| [`screenpipe.md`](screenpipe.md) | Continuous screen/audio capture (phase 2), including the deny-list required by `docs/standards/security.md`. |

After both are running, see `aggregator/README.md` for wiring their output
into the aggregator (phase 3).
