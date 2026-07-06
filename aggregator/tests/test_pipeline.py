from __future__ import annotations

from datetime import date
from pathlib import Path

import responses

from sediment_aggregator.ollama_client import OllamaClient
from sediment_aggregator.pipeline import run_for_date
from sediment_aggregator.sources.file_based import (
    JsonFileMeetilySource,
    JsonFileScreenpipeSource,
)

FIXTURES = Path(__file__).parent / "fixtures"


@responses.activate
def test_run_for_date_writes_deduped_summary(tmp_path):
    responses.add(
        responses.POST,
        "http://localhost:11434/api/generate",
        json={"response": "a summary"},
        status=200,
    )

    output_path = run_for_date(
        date(2026, 7, 6),
        meetily=JsonFileMeetilySource(FIXTURES / "meetily"),
        screenpipe=JsonFileScreenpipeSource(FIXTURES / "screenpipe"),
        ollama=OllamaClient(),
        output_dir=tmp_path,
    )

    text = output_path.read_text()
    assert "a summary" in text
    # the fixture's overlapping screenpipe segment should be deduped, so only
    # one summarization call is made per non-empty section (meetings, desktop)
    assert len(responses.calls) == 2


@responses.activate
def test_run_for_date_with_no_data_skips_ollama_calls(tmp_path):
    output_path = run_for_date(
        date(1999, 1, 1),
        meetily=JsonFileMeetilySource(FIXTURES / "meetily"),
        screenpipe=JsonFileScreenpipeSource(FIXTURES / "screenpipe"),
        ollama=OllamaClient(),
        output_dir=tmp_path,
    )

    assert len(responses.calls) == 0
    assert "No meetings today" in output_path.read_text()
