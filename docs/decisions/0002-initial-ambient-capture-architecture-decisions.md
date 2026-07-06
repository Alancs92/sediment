# 0002. Initial ambient-capture architecture decisions

Status: Accepted

## Context

The initial system design
([`docs/architecture/ambient-capture-architecture.md`](../architecture/ambient-capture-architecture.md))
bundles several distinct decisions made up front, before any code exists.
Recording them here so they're not lost or silently re-litigated later.

## Decisions

1. **Meetily and Screenpipe both run, roles kept separate (architecture §1,
   Option A).** Meetily stays the source of truth for meeting audio
   (structured, speaker-aware summaries); Screenpipe runs 24/7 for screen
   capture plus supplementary/redundant audio. We accept audio capture
   redundancy at first rather than trying to suppress Screenpipe's audio
   during meetings, and dedupe in the aggregator instead. Dropping Meetily
   in favor of Screenpipe's `meeting-summary` pipe (Option B) is deferred
   until that pipe is trusted.
2. **The aggregator is the only new code in the initial build**, implemented
   in **Python** (architecture §3) — chosen over Go/Rust for iteration speed,
   given Ollama's and Notion's Python client maturity, despite the author's
   comfort with Go/Rust from prior work.
3. **The coding-agent session DB is never replaced by Screenpipe capture**
   (architecture §5). The session DB is structured and intentional;
   Screenpipe is unstructured supplementary context, joined by timestamp
   overlap, not a replacement data source. Start with the minimal
   (read-only) integration; add the `ai-prompt-journal` timestamp join later.
4. **Backblaze B2 is the default cold-archive tier** (architecture §6), over
   Cloudflare R2, because the workload is write-once/rarely-read and B2 is
   the cheaper raw-storage option for that pattern (~$6/TB/month). Paired
   with the Cloudflare Bandwidth Alliance for free egress if bulk retrieval
   is ever needed.
5. **Retention shape (deferred but planned): local for 30-90 days, then
   `rclone sync` to B2 weekly, deleting local raw media but keeping the
   extracted text/transcript index locally forever.** Exact window is
   deferred until real Screenpipe storage-growth data exists (see
   implementation plan, phase 6).

## Consequences

- These are treated as the current baseline, not open questions — reopening
  any of them (e.g. dropping Meetily, switching languages, changing cold
  storage provider) should produce a new ADR that supersedes the relevant
  point above, not a silent change to the architecture doc.
- Because dedupe logic is a policy choice (§1) rather than a hard technical
  constraint, it's expected to need real-world tuning once phase 3 of the
  implementation plan lands.
