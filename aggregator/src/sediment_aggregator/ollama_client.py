"""Thin client for local Ollama summarization calls.

One call per section (architecture doc §3, point 5) rather than one giant
prompt, to stay inside local context/VRAM budgets.
"""

from __future__ import annotations

import requests


class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.1"):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def summarize(self, prompt: str, *, timeout: float = 120.0) -> str:
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={"model": self.model, "prompt": prompt, "stream": False},
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()["response"].strip()
