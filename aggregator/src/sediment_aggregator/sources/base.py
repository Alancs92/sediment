"""Source interfaces. Concrete adapters live alongside this file.

Only a file-based adapter (``file_based.py``) ships today. It reads a
normalized JSON export rather than Meetily's/Screenpipe's real on-disk or API
schema, because that schema isn't confirmed yet — see
docs/decisions/0003-aggregator-v0-container-and-adapters.md. Swap in a real
SQLite/REST adapter behind these same interfaces once phases 1-2 of
docs/implementation/README.md are running and the real schema is known;
don't change ``dedupe.py`` or ``pipeline.py`` to do it.
"""

from __future__ import annotations

from datetime import date
from typing import Protocol

from ..models import Meeting, ScreenSegment


class MeetilySource(Protocol):
    def for_date(self, day: date) -> list[Meeting]: ...


class ScreenpipeSource(Protocol):
    def for_date(self, day: date) -> list[ScreenSegment]: ...
