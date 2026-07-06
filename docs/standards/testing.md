# Testing (TDD)

Applies to all application code (aggregator, any future service). Does not
apply to docs-only changes.

## Rules

1. **Write the failing test before the implementation.** For a bug fix, the
   test must reproduce the bug and fail on the old code before you touch the
   fix.
2. **A task/PR is not done if tests are failing, skipped, or missing for the
   logic it introduces.** Don't mark implementation-plan phases (see
   [`../implementation/README.md`](../implementation/README.md)) complete
   with red or absent tests.
3. **Prioritize coverage on the riskiest logic first**, in order of actual
   risk in this project:
   - Dedupe logic (Screenpipe vs. Meetily overlap) — silent data loss or
     duplication here is the most likely real bug.
   - Timestamp-overlap joins (coding-agent session ↔ Screenpipe context).
   - Aggregator idempotency — re-running the daily job must not create
     duplicate Notion pages or corrupt already-written output.
   - Any parsing of Meetily/Screenpipe's on-disk formats — these are
     external tools whose schemas can change under us.
4. **Draw a clear boundary between unit and integration tests** for anything
   that touches a real external service (Notion API, Ollama, Screenpipe's
   local REST API):
   - Unit tests mock the boundary and run in CI with no network/local daemon
     dependency.
   - Integration tests that require a live Screenpipe/Ollama/Notion are
     explicitly marked as such and are allowed to be run manually/locally
     rather than gating every commit — but they must exist for anything that
     writes to Notion or deletes local data (archival).
5. **No test deleted or weakened just to make a change pass.** If a test is
   wrong, fix the test in its own reviewable step with a reason, not folded
   silently into an unrelated change.

## What doesn't need a test

Docs, config-only changes, and pure formatting/renames.
