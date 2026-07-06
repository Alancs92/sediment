# Standards

Baseline engineering practices that apply to **every** change in this repo,
regardless of which component or language is involved. These are not
aspirational — treat them as gating criteria before anything merges.

| Doc | Covers |
|---|---|
| [`testing.md`](testing.md) | TDD expectations, what must have tests, how to handle things that touch real external services (Notion, Ollama, Screenpipe). |
| [`security.md`](security.md) | Data sensitivity, secrets handling, the deny-list requirement for capture, license/commercial-use compliance. |
| [`code-review.md`](code-review.md) | What a reviewer (human or agent) must check before approving a change. |

These apply on top of, not instead of, whatever standards a specific
component's own docs describe once implementation starts.
