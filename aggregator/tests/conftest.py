from __future__ import annotations

from datetime import UTC, datetime

import pytest

from sediment_aggregator.models import Meeting, ScreenSegment


def dt(hour: int, minute: int = 0, day: int = 6) -> datetime:
    return datetime(2026, 7, day, hour, minute, tzinfo=UTC)


@pytest.fixture
def make_meeting():
    def _make(id="m1", title="Standup", start=None, end=None):
        start = dt(9) if start is None else start
        end = dt(9, 30) if end is None else end
        return Meeting(id=id, title=title, start=start, end=end, transcript="hi", summary="s")

    return _make


@pytest.fixture
def make_segment():
    def _make(start=None, end=None, audio="some audio"):
        start = dt(9) if start is None else start
        end = dt(9, 15) if end is None else end
        return ScreenSegment(
            start=start,
            end=end,
            app="Chrome",
            window_title="Docs",
            ocr_text="some text",
            audio_transcript=audio,
        )

    return _make
