from __future__ import annotations

from sediment_aggregator.models import DaySummary
from sediment_aggregator.writer import render_markdown, write_day_summary


def test_render_markdown_no_data():
    summary = DaySummary(date="2026-07-06")
    text = render_markdown(summary)
    assert "No meetings today" in text
    assert "No Screenpipe data" in text


def test_render_markdown_with_data(make_meeting):
    summary = DaySummary(
        date="2026-07-06",
        meetings=[make_meeting()],
        meetings_summary="Talked about the sprint.",
        dropped_duplicate_audio_count=2,
    )
    text = render_markdown(summary)
    assert "Talked about the sprint." in text
    assert "Standup" in text
    assert "Deduped 2 Screenpipe audio" in text


def test_write_day_summary_creates_file_and_dir(tmp_path):
    summary = DaySummary(date="2026-07-06")
    output_dir = tmp_path / "nested" / "output"

    path = write_day_summary(summary, output_dir)

    assert path == output_dir / "2026-07-06.md"
    assert path.exists()


def test_write_day_summary_is_idempotent(make_meeting, tmp_path):
    summary = DaySummary(date="2026-07-06", meetings=[make_meeting()], meetings_summary="v1")
    path1 = write_day_summary(summary, tmp_path)

    summary.meetings_summary = "v2"
    path2 = write_day_summary(summary, tmp_path)

    assert path1 == path2
    assert "v2" in path2.read_text()
    assert list(tmp_path.glob("*.md")) == [path2]
