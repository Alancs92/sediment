# Security

This project captures screen content, audio, and coding-agent session data,
and per the architecture doc may run on a work machine. Treat these as real
risks, not boilerplate.

## Data sensitivity

- **Deny-list clinical/work-identifiable apps at the capture layer, not just
  at sync time.** Screenpipe's `deny-apps`/`allow-apps` must be configured at
  the daemon level (global) as well as per-pipe, so an app can't leak into
  local capture just because one pipe forgot to filter it — see architecture
  doc §4. If you add a new pipe or capture source, it inherits this
  requirement; don't assume the global deny-list alone covers it if the new
  source can capture outside Screenpipe's daemon.
- Never sync raw screen/audio capture to Notion — only derived summaries and
  extracted text should leave the local machine. Treat any code path that
  would upload raw media as a bug.
- Default to least retention: local raw media has a retention window (see
  `docs/architecture/ambient-capture-architecture.md` §6); don't add code
  paths that keep raw capture "just in case" past that window without an ADR
  justifying it.

## Secrets

- No API keys, tokens, or credentials (Notion, Ollama Cloud, Backblaze B2,
  rclone config) committed to this repo, ever — including in test fixtures,
  example configs, or debug logs.
- `.env` and equivalents are gitignored; commit `.env.example` with variable
  names only, no values.
- If a secret is ever committed, treat it as compromised: rotate it, don't
  just remove it from a later commit (history retains it).

## Licensing / commercial-use compliance

- Screenpipe's license is source-available: free for personal/non-commercial
  use, paid for commercial use (architecture doc §4). Before running any
  capture component on a work-owned machine, confirm it complies with both
  the tool's license terms and the employer's device/data policy. When in
  doubt, run ambient capture only on a personal machine.

## Review checklist before merging capture/storage/sync code

- Does this touch Screenpipe capture config? Confirm the global deny-list is
  still in effect and covers the new surface.
- Does this write to Notion or any external service? Confirm it can't be
  triggered against unfiltered/raw data.
- Does this change what's retained locally or archived? Confirm it matches
  the retention policy or comes with an ADR explaining the change.
- Does this introduce a new secret/credential? Confirm it's read from env/
  config, never hardcoded, and `.env.example` is updated.
