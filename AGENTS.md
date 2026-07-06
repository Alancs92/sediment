# AGENTS.md

This file is the entry point for any AI coding agent (Claude, GPT, Gemini,
Copilot, or otherwise) working in this repository. It is intentionally
tool-agnostic — do not assume a specific vendor or CLI. If your tool reads a
vendor-specific file (`CLAUDE.md`, `.cursorrules`, etc.), that file should
simply point back here rather than duplicating content.

## What this repo is

`sediment` is the implementation of a personal, local-first ambient-capture
pipeline (meetings, desktop/audio context, coding sessions) normalized into a
daily record and synced to Notion. The full design is in
[`docs/architecture/ambient-capture-architecture.md`](docs/architecture/ambient-capture-architecture.md).

**Current state: documentation only.** No application code has been written
yet. Code lands on separate branches/PRs, built in the order defined in
[`docs/implementation/README.md`](docs/implementation/README.md). Do not add
implementation code against this baseline without checking that file first.

## Read this before doing anything else

1. [`docs/README.md`](docs/README.md) — map of all documentation, start here.
2. [`docs/architecture/`](docs/architecture/) — what we're building and why.
3. [`docs/decisions/`](docs/decisions/) — the ADR log. Check it before
   re-deciding something that was already decided; add to it when you make a
   new non-trivial decision.
4. [`docs/standards/`](docs/standards/) — TDD, security, and code-review
   rules that apply to every change, regardless of language or component.
5. [`docs/infrastructure/`](docs/infrastructure/) — CI/CD, environments, and
   secrets handling (placeholder until code exists; fill in as it lands).

## Ground rules for agents

- **Record decisions, don't just make them.** Any choice with lasting
  consequence (data flow, storage, library/service choice, schema, security
  posture) gets a new file in `docs/decisions/` following the existing ADR
  template — not just a mention in a commit message or chat.
- **TDD is not optional** for application code — see
  `docs/standards/testing.md`. Docs-only changes don't need tests.
- **Treat capture data as sensitive by default.** This project touches
  screen/audio capture and, per the architecture doc, may run on a work
  machine — see `docs/standards/security.md` before writing anything that
  touches capture, storage, or sync.
- **Keep docs in sync with reality.** If an implementation decision
  contradicts something written in `docs/architecture/`, update the
  architecture doc and add an ADR explaining the change — don't let the
  two silently diverge.
- **Don't invent infrastructure that doesn't exist yet.** `docs/infrastructure/`
  is a placeholder; fill it in when CI/deployment actually exists, not before.
