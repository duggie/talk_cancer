# tests/test_ollama_chat_model.py
from __future__ import annotations

from typing import Any, Dict, List

import pytest

from app.llm_base import ChatMessage
from app.llm_ollama import OllamaChatModel, OllamaConfig


class DummyResponse:
    def __init__(self, json_data: Dict[str, Any], status_code: int = 200):
        self._json_data = json_data
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if not (200 <= self.status_code < 300):
            raise RuntimeError(f"HTTP {self.status_code}")

    def json(self) -> Dict[str, Any]:
        return self._json_data


@pytest.mark.asyncio
async def test_ollama_chat_model_uses_generate_with_system_and_prompt(monkeypatch):
    config = OllamaConfig(base_url="http://dummy", model="dummy-model")
    model = OllamaChatModel(config=config)

    captured_payload: Dict[str, Any] = {}
    captured_url: str | None = None

    async def fake_post(url: str, json: Dict[str, Any]):  # type: ignore[override]
        nonlocal captured_payload, captured_url
        captured_url = url
        captured_payload = json
        return DummyResponse(
            {
                "model": "dummy-model",
                "response": "Hello from fake Ollama.",
                "done": True,
            }
        )

    import httpx

    class DummyAsyncClient:
        def __init__(self, *args: Any, **kwargs: Any):
            pass

        async def __aenter__(self) -> "DummyAsyncClient":
            return self

        async def __aexit__(self, exc_type, exc, tb) -> None:  # type: ignore[override]
            return None

        async def post(self, url: str, json: Dict[str, Any]):  # type: ignore[override]
            return await fake_post(url, json)

    monkeypatch.setattr(httpx, "AsyncClient", DummyAsyncClient)

    messages: List[ChatMessage] = [
        ChatMessage(role="system", content="system text"),
        ChatMessage(role="user", content="user question"),
    ]

    reply = await model.chat(messages)

    # 1) We actually return the LLM's response string
    assert reply == "Hello from fake Ollama."

    # 2) We hit the correct endpoint
    assert captured_url == "http://dummy/api/generate"

    # 3) Model name and stream flag are set
    assert captured_payload["model"] == "dummy-model"
    assert captured_payload["stream"] is False

    # 4) System and prompt content are wired correctly
    assert "system text" in captured_payload["system"]
    assert "user question" in captured_payload["prompt"]
