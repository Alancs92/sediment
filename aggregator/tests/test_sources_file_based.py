from __future__ import annotations

from datetime import date
from pathlib import Path

from sediment_aggregator.sources.file_based import (
    JsonFileMeetilySource,
    JsonFileScreenpipeSource,
)

FIXTURES = Path(__file__).parent / "fixtures"


def test_meetily_source_reads_fixture():
    source = JsonFileMeetilySource(FIXTURES / "meetily")
    meetings = source.for_date(date(2026, 7, 6))
    assert len(meetings) == 1
    assert meetings[0].title == "Team standup"


def test_screenpipe_source_reads_fixture():
    source = JsonFileScreenpipeSource(FIXTURES / "screenpipe")
    segments = source.for_date(date(2026, 7, 6))
    assert len(segments) == 2
    assert segments[1].audio_transcript is None


def test_missing_day_file_returns_empty_list():
    source = JsonFileMeetilySource(FIXTURES / "meetily")
    assert source.for_date(date(1999, 1, 1)) == []
