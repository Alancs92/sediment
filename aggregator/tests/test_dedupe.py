from __future__ import annotations

from datetime import UTC, datetime

from sediment_aggregator.dedupe import dedupe_screenpipe_against_meetily


def dt(hour, minute=0):
    return datetime(2026, 7, 6, hour, minute, tzinfo=UTC)


def test_no_meetings_leaves_segments_untouched(make_segment):
    segment = make_segment()
    result, dropped = dedupe_screenpipe_against_meetily([], [segment])
    assert result == [segment]
    assert dropped == 0


def test_fully_overlapping_segment_loses_audio(make_meeting, make_segment):
    meeting = make_meeting(start=dt(9), end=dt(10))
    segment = make_segment(start=dt(9, 15), end=dt(9, 45), audio="meeting chatter")

    result, dropped = dedupe_screenpipe_against_meetily([meeting], [segment])

    assert dropped == 1
    assert result[0].audio_transcript is None
    assert result[0].ocr_text == segment.ocr_text  # screen context preserved


def test_partially_overlapping_segment_loses_audio(make_meeting, make_segment):
    meeting = make_meeting(start=dt(9), end=dt(9, 30))
    segment = make_segment(start=dt(9, 20), end=dt(9, 40), audio="tail end")

    result, dropped = dedupe_screenpipe_against_meetily([meeting], [segment])

    assert dropped == 1
    assert result[0].audio_transcript is None


def test_adjacent_non_overlapping_segment_is_untouched(make_meeting, make_segment):
    meeting = make_meeting(start=dt(9), end=dt(9, 30))
    segment = make_segment(start=dt(9, 30), end=dt(10), audio="after meeting")

    result, dropped = dedupe_screenpipe_against_meetily([meeting], [segment])

    assert dropped == 0
    assert result[0].audio_transcript == "after meeting"


def test_segment_with_no_audio_is_passed_through_and_not_counted(make_meeting, make_segment):
    meeting = make_meeting(start=dt(9), end=dt(10))
    segment = make_segment(start=dt(9), end=dt(9, 30), audio=None)

    result, dropped = dedupe_screenpipe_against_meetily([meeting], [segment])

    assert dropped == 0
    assert result[0].audio_transcript is None


def test_multiple_meetings_only_overlapping_one_drops_audio(make_meeting, make_segment):
    morning = make_meeting(id="m1", start=dt(9), end=dt(9, 30))
    afternoon = make_meeting(id="m2", start=dt(14), end=dt(14, 30))
    morning_segment = make_segment(start=dt(9, 5), end=dt(9, 10), audio="morning")
    evening_segment = make_segment(start=dt(18), end=dt(18, 10), audio="evening")

    result, dropped = dedupe_screenpipe_against_meetily(
        [morning, afternoon], [morning_segment, evening_segment]
    )

    assert dropped == 1
    assert result[0].audio_transcript is None
    assert result[1].audio_transcript == "evening"


def test_order_is_preserved(make_meeting, make_segment):
    segments = [
        make_segment(start=dt(1), end=dt(2), audio="a"),
        make_segment(start=dt(3), end=dt(4), audio="b"),
        make_segment(start=dt(5), end=dt(6), audio="c"),
    ]
    result, _ = dedupe_screenpipe_against_meetily([], segments)
    assert [s.audio_transcript for s in result] == ["a", "b", "c"]
