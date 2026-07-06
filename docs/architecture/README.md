# Architecture docs

Living documents describing what `sediment` is and how its parts fit
together. Update these in place as the design evolves — don't fork a new
file for a design change, and don't rewrite history here; if a change is
significant enough to need a rationale trail, record it as an ADR in
[`../decisions/`](../decisions/) and update this doc to reflect the new
current state.

## Contents

- [`ambient-capture-architecture.md`](ambient-capture-architecture.md) — the
  baseline design: component roles (Meetily, Screenpipe, coding-agent session
  DB, Ollama, Notion), data flow, the aggregator, storage/archival, and build
  order.

## Adding a new architecture doc

Add one file per major subsystem once this repo has more than one (e.g. a
separate doc for the aggregator's internals once it's built, or for the
Notion schema). Keep this README's contents list current when you do.
