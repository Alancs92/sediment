---
name: bootstrap-repo-docs
description: "Use when starting a brand-new repository (or a new project inside one) that needs a baseline documentation structure before any code is written — architecture docs, decision records (ADRs), engineering standards (TDD/security/code review), and infrastructure placeholders. Triggers on requests like 'set up docs for a new repo', 'bootstrap this repo', 'scaffold architecture/decision docs', 'I have a design doc, turn it into a repo', or 'prepare a docs-only branch/PR'. Produces an AI-agnostic doc structure (AGENTS.md entry point, not tied to any one vendor) readable by any coding agent or human contributor."
---

# Bootstrap repo docs

Scaffolds a minimal, durable documentation architecture for a new repository
or project, before any application code exists. The goal: any agent (or
human) that opens this repo cold — in this session or a future one — can
find what's being built, why key choices were made, what rules gate a merge,
and what infrastructure exists, without re-asking the project owner.

This produces **docs only**. Do not write application code as part of this
skill unless the user explicitly asks for it in the same request.

## When NOT to use this

- The repo already has this structure (check for `AGENTS.md` + `docs/` with
  `architecture/`, `decisions/`, `standards/` first — if present, extend it,
  don't duplicate it).
- The user wants actual feature code, not docs scaffolding.

## Inputs to gather before writing anything

1. **Project identity**: name, one-line purpose. Ask if not obvious from
   context.
2. **Source design material**, if any (an uploaded/pasted architecture doc,
   a design conversation). If present, this becomes the seed for
   `docs/architecture/` and for the first real ADR(s) — don't invent
   architecture from scratch if the user already gave you one.
3. **Target stack/language(s)**, if known — used only to tailor
   `.gitignore` and the infrastructure placeholder; skip if genuinely
   unknown this early (docs-only repos often don't know yet).
4. **Branch/PR conventions already imposed on you** (e.g. a designated
   feature branch) — follow those; this skill doesn't dictate git workflow,
   only file contents.

## Structure to produce

```
<repo-root>/
├── .gitignore                     # tailored to stated/likely stack; always
│                                   # cover secrets (.env), local DBs, OS/editor cruft
├── README.md                      # human-facing: what this is, status, links into docs/
├── AGENTS.md                      # AI-agnostic agent entry point (see below)
└── docs/
    ├── README.md                  # index/map of every doc below, one line each
    ├── architecture/
    │   ├── README.md              # how to add new architecture docs; living-doc rule
    │   └── <name>.md              # the design doc itself (verbatim if user supplied one)
    ├── implementation/
    │   └── README.md              # phased build plan + status table, derived from the
    │                               # architecture doc's build order if it has one
    ├── decisions/
    │   ├── README.md              # ADR rules + template + index table
    │   ├── 0001-record-architecture-decisions.md   # bootstrap ADR, always first
    │   └── 0002-...               # one ADR per decision already embedded in the
    │                               # supplied design doc (see "Mining ADRs" below)
    ├── standards/
    │   ├── README.md
    │   ├── testing.md             # TDD rules, tailored to the project's actual risk areas
    │   ├── security.md            # tailored to actual sensitive-data/secrets surface
    │   └── code-review.md         # correctness/reuse/security/process checklist
    └── infrastructure/
        └── README.md              # CI/CD, environments, secrets — placeholder with a
                                   # "current status" table, filled in as it's built
```

## Key content rules (apply across every file)

- **AGENTS.md is the single agent-facing entry point**, at repo root, vendor-
  neutral in name and content. If the harness you're running in also reads a
  vendor-specific file (`CLAUDE.md`, `.cursorrules`, etc.), make that file a
  short pointer to `AGENTS.md`, not a duplicate.
- **`docs/README.md` is the map** — every other doc gets one line here
  explaining its purpose and how it relates to the others.
- **ADRs are append-only.** Never edit an accepted decision's content;
  supersede it with a new numbered file instead. Always seed ADR 0001 as the
  bootstrap "we use ADRs" record (Nygard-style: Context / Decision /
  Consequences).
- **Mining ADRs from a supplied design doc**: read through it for sentences
  that pick one option over another with a stated reason ("recommended to
  start", "chosen over X because...", "the right default for..."). Each
  cluster of related choices becomes one ADR (don't create one ADR per
  sentence — group by theme) with Status: Accepted, referencing the
  architecture doc section it came from.
- **`docs/implementation/README.md`** should be a status table, not prose —
  phase, dependencies, status (`Not started` until code lands), notes. If
  the design doc has a build-order section, use it directly as the phases.
- **`docs/standards/*`** must be tailored to the actual project, not generic
  boilerplate — pull real risk areas out of the architecture doc (e.g. "this
  project touches screen/audio capture" → security.md calls out deny-lists
  and raw-media handling by name; "this has a dedupe/join step" → testing.md
  names it as the top testing priority). Generic filler that doesn't
  reference the actual system reads as unread — avoid it.
- **`docs/infrastructure/README.md`** must be honest about having nothing
  yet if that's true. Don't fabricate a CI pipeline or deployment story that
  doesn't exist; list what needs to be documented once it does, as a status
  table.
- **Root `README.md`** is for humans: what this is, current status (docs-
  only vs. has-code), a components/architecture summary table if useful,
  and links into `docs/`. Keep it short — detail lives in `docs/`.
- **`.gitignore`** always covers: secrets/env files, local databases
  (`*.db`, `*.sqlite*`) if the project touches local data capture/storage,
  common language artifacts for the stated/likely stack, OS/editor cruft.
  Don't add sections for stacks that are pure speculation.

## Process

1. Confirm current repo state first (`git status`, check for an existing
   `AGENTS.md`/`docs/` structure) — don't overwrite unrelated existing work.
2. If a source design doc was supplied, read it fully before drafting
   anything else — the implementation plan, ADRs, and tailored standards all
   derive from it.
3. Write files in this order: `.gitignore` → `README.md` → `AGENTS.md` →
   `docs/architecture/*` → `docs/implementation/README.md` →
   `docs/decisions/*` → `docs/standards/*` → `docs/infrastructure/README.md`.
   Architecture and decisions come before standards/infrastructure because
   the latter should reference concrete risk areas from the former.
4. Follow whatever git workflow constraints are already in effect (designated
   branch, no unsolicited PRs, etc.) — this skill only defines file content.
5. Do not add application code, CI config, or dependency manifests in this
   pass unless explicitly asked — that belongs to a later, separate piece of
   work per `docs/implementation/README.md`.

## Reusing this skill in another repo

This skill folder is self-contained. To reuse it elsewhere: copy
`.claude/skills/bootstrap-repo-docs/` into the target repo's (or your
personal) `.claude/skills/` directory, then invoke it there. It doesn't
depend on anything specific to the repo it was written in.
