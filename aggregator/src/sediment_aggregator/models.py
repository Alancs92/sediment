"""Normalized data shapes the pipeline operates on.

These are deliberately independent of Meetily's or Screenpipe's actual
on-disk/API schema, which isn't confirmed yet (see
docs/decisions/0003-aggregator-v0-container-and-adapters.md). Adapters in
``sources/`` are responsible for translating real tool output into these
shapes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class Meeting:
    """One meeting, as produced by Meetily."""

    id: str
    title: str
    start: datetime
    end: datetime
    transcript: str
    summary: str

    def overlaps(self, start: datetime, end: datetime) -> bool:
        return self.start < end and start < self.end


@dataclass
class ScreenSegment:
    """One Screenpipe capture window: screen context plus optional audio."""

    start: datetime
    end: datetime
    app: str
    window_title: str
    ocr_text: str
    audio_transcript: str | None = None

    def overlaps(self, start: datetime, end: datetime) -> bool:
        return self.start < end and start < self.end


@dataclass
class DaySummary:
    """The normalized output of one day's aggregation run, pre-Notion."""

    date: str  # YYYY-MM-DD
    meetings: list[Meeting] = field(default_factory=list)
    screen_segments: list[ScreenSegment] = field(default_factory=list)
    meetings_summary: str = ""
    desktop_activity_summary: str = ""
    dropped_duplicate_audio_count: int = 0
