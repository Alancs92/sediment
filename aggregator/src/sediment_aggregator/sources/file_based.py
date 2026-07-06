"""File-based v0 adapters: read a normalized JSON export, one file per day.

Expected layout: ``{export_dir}/{YYYY-MM-DD}.json`` containing a JSON list.

Meetily record shape::

    {"id": "...", "title": "...", "start": "2026-07-06T09:00:00+10:00",
     "end": "2026-07-06T09:45:00+10:00", "transcript": "...", "summary": "..."}

Screenpipe record shape::

    {"start": "...", "end": "...", "app": "...", "window_title": "...",
     "ocr_text": "...", "audio_transcript": "..." | null}

Nothing produces this format yet — it's the v0 integration point. Until a
real Meetily/Screenpipe adapter exists, export their data into this shape
(by hand, or a small script) to feed the aggregator.
"""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path

from ..models import Meeting, ScreenSegment


def _load_day_file(export_dir: Path, day: date) -> list[dict]:
    path = export_dir / f"{day.isoformat()}.json"
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return json.load(f)


class JsonFileMeetilySource:
    def __init__(self, export_dir: Path | str):
        self.export_dir = Path(export_dir)

    def for_date(self, day: date) -> list[Meeting]:
        return [
            Meeting(
                id=record["id"],
                title=record["title"],
                start=datetime.fromisoformat(record["start"]),
                end=datetime.fromisoformat(record["end"]),
                transcript=record.get("transcript", ""),
                summary=record.get("summary", ""),
            )
            for record in _load_day_file(self.export_dir, day)
        ]


class JsonFileScreenpipeSource:
    def __init__(self, export_dir: Path | str):
        self.export_dir = Path(export_dir)

    def for_date(self, day: date) -> list[ScreenSegment]:
        return [
            ScreenSegment(
                start=datetime.fromisoformat(record["start"]),
                end=datetime.fromisoformat(record["end"]),
                app=record.get("app", ""),
                window_title=record.get("window_title", ""),
                ocr_text=record.get("ocr_text", ""),
                audio_transcript=record.get("audio_transcript"),
            )
            for record in _load_day_file(self.export_dir, day)
        ]
