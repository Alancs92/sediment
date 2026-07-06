# Documentation map

This folder is the source of truth for why and how `sediment` is built. It's
written to be read by humans and AI agents alike — see the root
[`AGENTS.md`](../AGENTS.md) for the agent-facing entry point.

| Folder | Purpose |
|---|---|
| [`architecture/`](architecture/) | What we're building: system design, component roles, data flow. Living documents — updated in place as the design evolves. |
| [`implementation/`](implementation/) | The build plan: phased order of work, current status of each phase. |
| [`decisions/`](decisions/) | Architecture Decision Records (ADRs) — an append-only log of choices made and why. Never edit or delete a past ADR; supersede it with a new one instead. |
| [`standards/`](standards/) | Baseline engineering practices that apply to every change regardless of language or component: TDD, security, code review. |
| [`infrastructure/`](infrastructure/) | CI/CD, environments, secrets, deployment/runtime concerns. Placeholder until code exists. |

## How these relate

- **architecture** describes the *current intended design*.
- **decisions** explains *why* the design is what it is, and records changes
  to it over time — architecture docs describe the "what", ADRs preserve the
  "why" and the history.
- **implementation** tracks *progress* against the architecture.
- **standards** and **infrastructure** are cross-cutting: they apply no
  matter which part of the architecture you're implementing.

## Conventions

- All docs are Markdown, no build step, readable directly on GitHub.
- Keep architecture docs living/current; keep decision records historical
  and immutable once accepted.
- Prefer editing the relevant doc over leaving decisions in commit messages,
  PR descriptions, or chat — anything a future agent or contributor would
  need belongs here.
