# Decisions (ADRs)

An append-only log of Architecture Decision Records. Each ADR captures one
decision, the context that led to it, and its consequences — so future
contributors (human or agent) understand *why*, not just *what*.

## Rules

- **Never edit or delete an accepted ADR's decision/context.** If a decision
  changes, write a new ADR that supersedes the old one, and mark the old
  one's status as `Superseded by NNNN`.
- **One decision per file.**
- **Number sequentially**, zero-padded to 4 digits: `NNNN-short-title.md`.
- Write one **before or immediately after** making any decision with lasting
  consequence: architecture/data-flow choices, storage/service/library
  selection, schema changes, security posture, or deviations from the plan
  in [`../implementation/README.md`](../implementation/README.md).
- Trivial/reversible choices (variable names, formatting) don't need one.

## Template

```markdown
# NNNN. Title

Status: Proposed | Accepted | Superseded by NNNN

## Context

What problem or question forced this decision. What constraints applied.

## Decision

What was decided, stated plainly.

## Consequences

What this makes easier, harder, or forecloses. Include trade-offs
accepted, not just benefits.
```

## Index

| ADR | Title | Status |
|---|---|---|
| [0001](0001-record-architecture-decisions.md) | Record architecture decisions | Accepted |
| [0002](0002-initial-ambient-capture-architecture-decisions.md) | Initial ambient-capture architecture decisions | Accepted |
| [0003](0003-aggregator-v0-container-and-adapters.md) | Aggregator v0: container packaging and file-based adapters | Accepted |
