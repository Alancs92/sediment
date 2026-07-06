"""Dedupe Screenpipe audio against Meetily meeting windows.

Policy (docs/architecture/ambient-capture-architecture.md §1, and
docs/decisions/0002-initial-ambient-capture-architecture-decisions.md):
Meetily is the source of truth for meeting audio. Where a Screenpipe segment
overlaps a Meetily meeting window, we drop that segment's audio transcript
(Meetily's is better structured) but always keep the segment itself, since
Screenpipe's *screen* context has no Meetily equivalent.

Fails safe: on any ambiguity we keep data rather than drop it. A segment's
audio is only dropped if it genuinely overlaps a meeting window; partial
overlap is enough to drop that segment's audio (it's within a meeting), but
segments merely adjacent to (not overlapping) a meeting are left untouched.
"""

from __future__ import annotations

from dataclasses import replace

from .models import Meeting, ScreenSegment


def dedupe_screenpipe_against_meetily(
    meetings: list[Meeting], segments: list[ScreenSegment]
) -> tuple[list[ScreenSegment], int]:
    """Return (segments with overlapping audio stripped, count of segments changed).

    Segments are returned in the same order they were given. Segments with no
    audio_transcript to begin with are passed through unchanged and not
    counted.
    """
    deduped: list[ScreenSegment] = []
    dropped_count = 0

    for segment in segments:
        if segment.audio_transcript is None:
            deduped.append(segment)
            continue

        overlaps_a_meeting = any(
            meeting.overlaps(segment.start, segment.end) for meeting in meetings
        )
        if overlaps_a_meeting:
            deduped.append(replace(segment, audio_transcript=None))
            dropped_count += 1
        else:
            deduped.append(segment)

    return deduped, dropped_count
