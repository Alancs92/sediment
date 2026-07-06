"""Writes a DaySummary to a local markdown file. No Notion sync yet (phase 4)."""

from __future__ import annotations

from pathlib import Path

from .models import DaySummary


def render_markdown(summary: DaySummary) -> str:
    lines = [f"# Daily log — {summary.date}", ""]

    lines += ["## Meetings", ""]
    if summary.meetings:
        lines.append(summary.meetings_summary or "_(no summary generated)_")
        lines.append("")
        for meeting in summary.meetings:
            lines.append(f"- **{meeting.title}** ({meeting.start:%H:%M}–{meeting.end:%H:%M})")
    else:
        lines.append("_No meetings today._")
    lines.append("")

    lines += ["## Desktop activity", ""]
    if summary.screen_segments:
        lines.append(summary.desktop_activity_summary or "_(no summary generated)_")
    else:
        lines.append("_No Screenpipe data for today._")
    lines.append("")

    if summary.dropped_duplicate_audio_count:
        lines.append(
            f"_(Deduped {summary.dropped_duplicate_audio_count} Screenpipe audio "
            "segment(s) that overlapped a Meetily meeting.)_"
        )
        lines.append("")

    return "\n".join(lines)


def write_day_summary(summary: DaySummary, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{summary.date}.md"
    path.write_text(render_markdown(summary), encoding="utf-8")
    return path
