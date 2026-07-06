# Ollama (local)

Used by Meetily (meeting summarization) and by the aggregator (daily
digest generation). Install once, both consume it.

## Install

Follow Ollama's official installer for your OS: https://ollama.com/download

Verify it's running:

```bash
ollama --version
curl http://localhost:11434/api/tags
```

## Pull a model

Pick a model that fits your hardware. A reasonable general-purpose default:

```bash
ollama pull llama3.1
```

If local hardware is the bottleneck for heavier summarization, the
architecture doc (`docs/architecture/ambient-capture-architecture.md` §1)
notes Ollama Cloud as an opt-in fallback — only reach for it deliberately,
since the whole point of this pipeline is to stay local-first by default.

## Wiring it up

- Meetily: point its Ollama settings at `http://localhost:11434` and the
  model you pulled, per Meetily's own configuration.
- Aggregator: set `OLLAMA_BASE_URL` / `OLLAMA_MODEL` in `aggregator/.env`
  (see `aggregator/.env.example`). If you run the aggregator via Docker
  Compose and Ollama on the host (not in the compose stack), use
  `http://host.docker.internal:11434` on Docker Desktop, or your Linux
  host's bridge IP. If you'd rather run Ollama inside the same compose
  stack, use `docker compose --profile with-ollama up` and
  `OLLAMA_BASE_URL=http://ollama:11434`.
