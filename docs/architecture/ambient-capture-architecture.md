# Personal Ambient Capture Architecture
### Meetily + Screenpipe + Claude Code + Notion MCP

**Goal:** one local-first pipeline that captures meetings, continuous desktop/audio context, and Claude Code sessions; normalizes them into a daily record; syncs the useful bits into Notion; archives raw media cheaply.

---

## 1. Component roles (don't let them overlap)

| Component | Captures | Runs | Output |
|---|---|---|---|
| **Meetily** | Meeting audio only (calendar/manual-triggered sessions) | Local app, Whisper.cpp/Parakeet + Ollama | Markdown/SQLite: transcript + AI summary per meeting |
| **Screenpipe** | Screen (OCR/accessibility tree) + all system audio + mic, 24/7 | Background daemon | Local SQLite: timestamped frames, transcripts, app/window context |
| **Claude Code DB (yours)** | Final output of every CC session | Your existing app | Whatever schema you already built (assume Postgres/SQLite) |
| **Ollama (local)** | — | Local GPU/CPU | Summarization/embedding for all of the above |
| **Ollama Cloud** | — | Opt-in only | Fallback for heavier summarization when local hardware is the bottleneck |

**Key decision: don't run both Meetily and Screenpipe as separate audio capture pipelines for the same meeting.** Screenpipe already captures all system audio continuously, including meetings. Options:

- **A (recommended to start):** Keep Meetily for meetings — better structured summaries, speaker-aware, purpose-built templates. Configure Screenpipe to **skip audio capture during Meetily-active windows** (or just accept the redundancy at first since disk is cheap and dedupe later) but keep Screenpipe's *screen* capture running always, since that's the thing Meetily doesn't do.
- **B (later optimization):** Drop Meetily entirely once you trust Screenpipe's `meeting-summary` pipe enough, and use Screenpipe as the single capture layer for both meetings and ambient context.

Start with A. It's less clever but nothing breaks.

---

## 2. Data flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                            YOUR MACHINE                              │
│                                                                       │
│  ┌───────────┐      ┌──────────────┐      ┌─────────────────────┐  │
│  │  Meetily  │      │  Screenpipe  │      │  Claude Code DB      │  │
│  │  (meeting │      │  (24/7 screen│      │  (your existing      │  │
│  │  sessions)│      │  + audio)    │      │  session capture)    │  │
│  └─────┬─────┘      └──────┬───────┘      └──────────┬───────────┘  │
│        │                   │                          │              │
│        │ .md/SQLite        │ SQLite + pipes           │ Postgres/    │
│        │                   │ (day-recap,              │ SQLite       │
│        │                   │  ai-prompt-journal,      │              │
│        │                   │  standup-update)         │              │
│        └───────────┬───────┴──────────────┬───────────┘              │
│                     ▼                      ▼                         │
│              ┌─────────────────────────────────────┐                 │
│              │   Ollama (local)                     │                 │
│              │   summarization / embedding /        │                 │
│              │   daily digest generation             │                 │
│              └──────────────────┬────────────────────┘                │
│                                  ▼                                     │
│              ┌─────────────────────────────────────┐                 │
│              │  Aggregator script (cron, daily)      │                 │
│              │  - pulls from all 3 sources           │                 │
│              │  - normalizes to one JSON/MD schema   │                 │
│              │  - dedupes meeting audio vs screenpipe│                 │
│              └──────────────────┬────────────────────┘                │
│                                  │                                     │
└──────────────────────────────────┼─────────────────────────────────────┘
                                   ▼
                    ┌───────────────────────────┐
                    │   Notion (via Notion MCP)  │
                    │   - Meeting Notes DB       │
                    │   - Tasks Tracker          │
                    │   - Academic DB            │
                    │   - new: Daily Log DB       │
                    └───────────────────────────┘

                    [later, deferred]
                    ┌───────────────────────────┐
                    │  Archival job (weekly cron) │
                    │  raw audio/screenshots      │
                    │  older than N days           │
                    │  → Backblaze B2 (cold)       │
                    └───────────────────────────┘
```

---

## 3. Aggregator: the piece you actually need to build

This is the only genuinely new code. Everything else is existing tools. It's a scheduled script (daily, e.g. 11pm cron/launchd job) that:

1. **Pulls Meetily output** — read its SQLite DB or the markdown files it writes, filter for today's meetings.
2. **Pulls Screenpipe output** — query its local REST API (`localhost:3030`) or SQLite directly, filter for today, run the `day-recap` and `ai-prompt-journal` pipes if not already scheduled natively.
3. **Pulls Claude Code sessions** — query your existing DB for today's session outputs.
4. **Dedupe pass** — if a Screenpipe audio segment overlaps a Meetily meeting window, drop the Screenpipe transcript for that window (keep Meetily's version, it's better structured) but keep Screenpipe's *screen* context for that window.
5. **Summarize with local Ollama** — one call per section (meetings / dev work / other desktop activity) rather than one giant prompt, to keep it inside your context/VRAM budget.
6. **Write to Notion via Notion MCP** — create/update a page in a new "Daily Log" database, with sub-blocks or relations linking to:
   - Meeting notes (their own DB, one page per meeting, matches what Notion's own AI Meeting Notes would produce)
   - Claude Code sessions relevant to that day (relation field pointing at a new lightweight "Dev Sessions" DB, or just embed a summary + link back to your own app if you don't want a full duplicate DB)
   - Tasks extracted (push into your existing Tasks Tracker DB, `2f7b0f13dc11808f9f75d0ec95094936`)

Language choice: since you're comfortable in Rust/Go from the OpenSearch/Chronicle work, a small Go or Python script is enough — this doesn't need a service, just a scheduled batch job. Python is probably faster to iterate on given Ollama's Python client and the Notion API's Python SDK maturity.

---

## 4. Screenpipe configuration specifics

Given your clinical work, configure `deny-apps` in Screenpipe's pipe frontmatter / config to exclude anything touching patient data (EHR windows, Annalise internal tools if they show identifiable data) from screen capture entirely — not just from the Notion sync, but from local capture in the first place. Screenpipe supports `allow-apps`/`deny-apps` filtering at the OS level per pipe; set a global deny-list at the daemon config level too, not just per-pipe, so it can't be forgotten.

License note (repeat from earlier, because it matters for a work machine): Screenpipe's GitHub license is source-available, free for personal/non-commercial use, paid license for commercial use. If this runs on your Harrison.ai laptop, check whether your usage counts as "commercial" under their terms, and separately whether it fits Harrison.ai's device/data policies at all before running 24/7 capture on a work machine. Might be worth running it only on a personal machine to sidestep that entirely.

---

## 5. Claude Code integration

Two options, not mutually exclusive:

- **Minimal (do this first):** leave your existing Claude Code → DB pipeline exactly as-is. Aggregator just reads from it. Zero new integration risk.
- **Richer (later):** enable Screenpipe's `ai-prompt-journal` pipe so screen context around each Claude Code session (what error was on screen, what doc you had open) gets captured alongside your session DB's final-output records. Join them in the aggregator by timestamp overlap.

Don't try to have Screenpipe *replace* your session DB — your DB is structured and intentional, Screenpipe's capture is unstructured and noisy. Treat Screenpipe purely as supplementary context.

---

## 6. Storage & archival (deferred, but the shape to plan for)

Local, fast-access tier (SQLite/local disk):
- Meetily transcripts + summaries — small, keep forever locally
- Screenpipe DB — grows ~5-10GB/month per their own numbers; this is the one that needs a retention policy
- Claude Code session DB — small, keep forever locally

Cold archive tier (when you get to it): **Backblaze B2** is the right default for this specific workload — you're write-once, rarely-read, and it's the cheapest raw storage available (~$6/TB/month), cheaper than R2 for a pattern where you're not serving this data to anyone, just cold-storing it. Pair it with the Cloudflare Bandwidth Alliance if you ever do need to pull large batches back out, since B2↔Cloudflare egress is free.

Suggested (future) retention policy: keep Screenpipe raw screenshots/audio locally for 30-90 days for fast search, then a weekly job (`rclone sync` is the standard tool here) pushes anything older to B2 and deletes the local copy, keeping only the extracted text/transcript index locally forever (that's the searchable, useful part — the raw screenshots are just an audit trail you'll rarely open).

---

## 7. Build order

1. **Meetily** — get it running, verify Ollama summarization quality on a few real meetings
2. **Screenpipe** — install, let it run a few days untouched to gauge storage growth and CPU load before adding pipes
3. **Aggregator v0** — just the Meetily + Screenpipe merge, dumped to a local markdown file (no Notion yet) — verify the dedupe logic works before adding a destination
4. **Notion MCP sync** — point the aggregator's output at Notion once v0 is trustworthy
5. **Claude Code join** — add the timestamp-overlap join with your session DB
6. **Archival** — revisit once you have a few months of real Screenpipe storage growth data to size the retention window correctly
