"""Runtime configuration, sourced from environment variables (see .env.example).

No secrets have hardcoded defaults; see docs/standards/security.md.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    meetily_export_dir: Path
    screenpipe_export_dir: Path
    output_dir: Path
    ollama_base_url: str
    ollama_model: str
    daily_run_time: str  # "HH:MM", local time
    status_port: int

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            meetily_export_dir=Path(os.environ.get("MEETILY_EXPORT_DIR", "/data/meetily")),
            screenpipe_export_dir=Path(
                os.environ.get("SCREENPIPE_EXPORT_DIR", "/data/screenpipe")
            ),
            output_dir=Path(os.environ.get("OUTPUT_DIR", "/data/output")),
            ollama_base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"),
            ollama_model=os.environ.get("OLLAMA_MODEL", "llama3.1"),
            daily_run_time=os.environ.get("DAILY_RUN_TIME", "23:00"),
            status_port=int(os.environ.get("STATUS_PORT", "8420")),
        )
