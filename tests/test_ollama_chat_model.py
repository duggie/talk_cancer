"""Tests for the OllamaChatModel wrapper around the Ollama HTTP API."""

from __future__ import annotations

from typing import Any

import httpx
import pytest

from app.llm_base import ChatMessage
from app.llm_ollama import OllamaChatModel, OllamaConfig


class DummyResponse:
    """Simple dummy HTTP response used to stub httpx responses."""

    def __init__(
        self,
        json_data: dict[str, Any],
        status_code: int = 200,
    ) -> None:
        """Store JSON payload and status code."""
        self._json_data = json_data
        self.status_code = status_code

    def raise_for_status(self) -> None:
        """Raise at non-2xx status codes to mimic httpx.Response."""
        if self.status_code < 200 or self.status_code >= 300:
            msg = f"HTTP {self.status_code}"
            raise RuntimeError(msg)

    def json(self) -> dict[str, Any]:
        """Return the stored JSON payload."""
        return self._json_data


class DummyAsyncClient:
    """Async client that proxies POST calls to a supplied callable."""

    def __init__(
        self,
        *args: Any,
        post_impl: Any,
        **kwargs: Any,
    ) -> None:
        """Accept and store the implementation for POST."""
        del args, kwargs
        self._post_impl = post_impl

    async def __aenter__(self) -> DummyAsyncClient:
        """Enter the async context manager."""
        return self

    async def __aexit__(
        self,
        exc_type,
        exc,
        tb,
    ) -> None:  # type: ignore[override]
        """Exit the async context manager."""
        del exc_type, exc, tb
        return None

    async def post(
        self,
        url: str,
        json: dict[str, Any],
    ) -> DummyResponse:
        """Delegate POST calls to the injected implementation."""
        return await self._post_impl(url, json)


@pytest.mark.asyncio
async def test_chat_model_uses_generate_with_system_and_prompt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Ensure chat() calls the generate endpoint with expected payload."""
    config = OllamaConfig(
        base_url="http://dummy",
        model="dummy-model",
    )
    model = OllamaChatModel(config=config)

    captured_payload: dict[str, Any] = {}
    captured_url: str | None = None

    async def fake_post(
        url: str,
        json: dict[str, Any],
    ) -> DummyResponse:
        """Capture request data and return a canned response."""
        nonlocal captured_payload, captured_url
        captured_url = url
        captured_payload = json
        return DummyResponse(
            {
                "model": "dummy-model",
                "response": "Hello from fake Ollama.",
                "done": True,
            },
        )

    def make_dummy_async_client(
        *_: Any,
        **kwargs: Any,
    ) -> DummyAsyncClient:
        """Return a dummy async client instance."""
        return DummyAsyncClient(post_impl=fake_post, **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", make_dummy_async_client)

    messages: list[ChatMessage] = [
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


@pytest.mark.asyncio
async def test_chat_model_formats_assistant_messages(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Ensure assistant-role messages use 'Assistant:' prefix in the prompt."""
    config = OllamaConfig(base_url="http://dummy", model="dummy-model")
    model = OllamaChatModel(config=config)

    captured_payload: dict[str, Any] = {}
    captured_url: str | None = None

    async def fake_post(url: str, json: dict[str, Any]) -> DummyResponse:
        nonlocal captured_payload, captured_url
        captured_url = url
        captured_payload = json
        return DummyResponse({"response": "ok"})

    def fake_client_factory(*args: Any, **kwargs: Any) -> DummyAsyncClient:
        return DummyAsyncClient(*args, post_impl=fake_post, **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", fake_client_factory)

    messages: list[ChatMessage] = [
        ChatMessage(role="user", content="hello"),
        ChatMessage(role="assistant", content="hi there"),
    ]

    reply = await model.chat(messages)

    assert reply == "ok"
    assert captured_url == "http://dummy/api/generate"
    # This is the key assertion: the assistant message should be
    # prefixed correctly.
    assert "Assistant: hi there" in captured_payload["prompt"]


@pytest.mark.asyncio
async def test_chat_model_returns_safe_fallback_on_blank_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    If Ollama returns empty/whitespace response, return the safe
    fallback string.
    """
    config = OllamaConfig(base_url="http://dummy", model="dummy-model")
    model = OllamaChatModel(config=config)

    async def fake_post(_url: str, _json: dict[str, Any]) -> DummyResponse:
        # whitespace-only should be stripped to "", triggering the fallback
        return DummyResponse({"response": "   \n\t  "})

    def fake_client_factory(*args: Any, **kwargs: Any) -> DummyAsyncClient:
        return DummyAsyncClient(*args, post_impl=fake_post, **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", fake_client_factory)

    messages: list[ChatMessage] = [ChatMessage(role="user", content="yup")]

    reply = await model.chat(messages)

    expected = "I’m sorry, I could not generate a response just now."
    assert reply.startswith(expected)


@pytest.mark.asyncio
async def test_chat_model_raises_on_non_2xx_http_status(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Non-2xx responses should raise via raise_for_status()."""
    config = OllamaConfig(base_url="http://dummy", model="dummy-model")
    model = OllamaChatModel(config=config)

    async def fake_post(_url: str, _json: dict[str, Any]) -> DummyResponse:
        return DummyResponse({"error": "boom"}, status_code=500)

    def fake_client_factory(*args: Any, **kwargs: Any) -> DummyAsyncClient:
        return DummyAsyncClient(*args, post_impl=fake_post, **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", fake_client_factory)

    messages: list[ChatMessage] = [ChatMessage(role="user", content="hello")]

    with pytest.raises(RuntimeError, match=r"HTTP 500"):
        await model.chat(messages)
