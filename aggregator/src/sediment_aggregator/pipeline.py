"""Orchestrates one day's aggregation run: load -> dedupe -> summarize -> write.

Idempotent by construction: re-running for the same date re-derives the
summary from source data and overwrites the same output file, rather than
appending or creating a new one.
"""

from __future__ import annotations

import logging
from datetime import date
from pathlib import Path

from .dedupe import dedupe_screenpipe_against_meetily
from .models import DaySummary
from .ollama_client import OllamaClient
from .sources.base import MeetilySource, ScreenpipeSource
from .writer import write_day_summary

logger = logging.getLogger(__name__)

MEETINGS_PROMPT_TEMPLATE = (
    "Summarize these meetings from {date} in a few sentences, "
    "focused on decisions and action items:\n\n{transcripts}"
)
DESKTOP_PROMPT_TEMPLATE = (
    "Summarize this desktop activity log from {date} in a few sentences, "
    "focused on what was worked on:\n\n{context}"
)


def run_for_date(
    day: date,
    *,
    meetily: MeetilySource,
    screenpipe: ScreenpipeSource,
    ollama: OllamaClient,
    output_dir: Path,
) -> Path:
    meetings = meetily.for_date(day)
    segments = screenpipe.for_date(day)

    deduped_segments, dropped_count = dedupe_screenpipe_against_meetily(meetings, segments)
    logger.info(
        "day=%s meetings=%d segments=%d deduped_audio=%d",
        day,
        len(meetings),
        len(segments),
        dropped_count,
    )

    meetings_summary = ""
    if meetings:
        transcripts = "\n\n".join(f"## {m.title}\n{m.transcript}" for m in meetings)
        meetings_summary = ollama.summarize(
            MEETINGS_PROMPT_TEMPLATE.format(date=day.isoformat(), transcripts=transcripts)
        )

    desktop_summary = ""
    if deduped_segments:
        context = "\n".join(
            f"[{s.start:%H:%M}-{s.end:%H:%M}] {s.app} — {s.window_title}: {s.ocr_text}"
            for s in deduped_segments
        )
        desktop_summary = ollama.summarize(
            DESKTOP_PROMPT_TEMPLATE.format(date=day.isoformat(), context=context)
        )

    summary = DaySummary(
        date=day.isoformat(),
        meetings=meetings,
        screen_segments=deduped_segments,
        meetings_summary=meetings_summary,
        desktop_activity_summary=desktop_summary,
        dropped_duplicate_audio_count=dropped_count,
    )
    return write_day_summary(summary, output_dir)
