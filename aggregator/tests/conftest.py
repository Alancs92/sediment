from __future__ import annotations

from datetime import datetime

import pytest

from sediment_aggregator.models import Meeting, ScreenSegment


def dt(hour: int, minute: int = 0, day: int = 6) -> datetime:
    return datetime(2026, 7, day, hour, minute)


@pytest.fixture
def make_meeting():
    def _make(id="m1", title="Standup", start=dt(9), end=dt(9, 30)):
        return Meeting(id=id, title=title, start=start, end=end, transcript="hi", summary="s")

    return _make


@pytest.fixture
def make_segment():
    def _make(start=dt(9), end=dt(9, 15), audio="some audio"):
        return ScreenSegment(
            start=start,
            end=end,
            app="Chrome",
            window_title="Docs",
            ocr_text="some text",
            audio_transcript=audio,
        )

    return _make
