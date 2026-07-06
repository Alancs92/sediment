from __future__ import annotations

import responses

from sediment_aggregator.ollama_client import OllamaClient


@responses.activate
def test_summarize_posts_prompt_and_returns_trimmed_response():
    responses.add(
        responses.POST,
        "http://localhost:11434/api/generate",
        json={"response": "  a short summary  "},
        status=200,
    )

    client = OllamaClient()
    result = client.summarize("summarize this")

    assert result == "a short summary"
    request_body = responses.calls[0].request.body
    assert b"summarize this" in request_body
