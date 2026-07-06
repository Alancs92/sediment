# Code review / bug-check checklist

Applies to every PR touching application code, whether reviewed by a human
or an agent. Purpose: catch correctness and reuse issues before merge, not
after.

## Correctness

- Are edge cases handled: empty input (no meetings today, no Screenpipe
  data for the day), overlapping/adjacent time windows, clock/timezone
  boundaries (a day boundary at local midnight vs. UTC), partial failures
  (Notion write succeeds but local state update doesn't)?
- Is the aggregator idempotent — does re-running it for the same day produce
  the same result rather than duplicate Notion pages or double-counted data?
- Does dedupe logic (Screenpipe vs. Meetily overlap) fail safe — i.e., on
  ambiguous overlap, does it prefer keeping data over silently dropping it?
- Are external formats (Meetily/Screenpipe on-disk schema, Notion API
  responses) validated rather than assumed, given they're maintained outside
  this repo and can change?

## Reuse / simplification

- Does this duplicate logic that already exists elsewhere in the aggregator
  or a prior phase?
- Is the change scoped to what the current implementation-plan phase
  actually requires (see `docs/implementation/README.md`), or does it
  reach ahead into a later phase's concerns?

## Security (see `security.md` for the full checklist)

- No secrets in the diff.
- No raw capture data (screen/audio) written to a synced destination.
- Capture-layer changes preserve the deny-list.

## Process

- Tests exist and pass for new/changed logic (see `testing.md`).
- Any non-trivial decision made in this PR has a corresponding ADR in
  `docs/decisions/`.
- If this PR changes or completes an implementation phase, `docs/implementation/README.md`
  is updated in the same PR.
