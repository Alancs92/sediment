# 0001. Record architecture decisions

Status: Accepted

## Context

This repo will accumulate non-trivial technical decisions over time (which
tools to run, how to dedupe overlapping capture, storage/retention choices,
security posture). Without a durable record, that reasoning ends up scattered
across commit messages, PR descriptions, and chat history — none of which is
easy for a future contributor (or agent starting a fresh session) to find or
trust.

## Decision

Use lightweight Architecture Decision Records (ADRs), stored in
`docs/decisions/`, one file per decision, following the template in
`docs/decisions/README.md`. Numbered sequentially, immutable once accepted,
superseded rather than edited when a decision changes.

## Consequences

- Every future agent/contributor session can reconstruct *why* the system
  looks the way it does without asking the project owner to re-explain it.
- Adds a small amount of process overhead per non-trivial decision.
- Requires discipline to actually write one instead of just making the
  change — this is called out explicitly in `AGENTS.md`.
