""" local Ollama-based chat model implementation """
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import httpx

from .llm_base import ChatModel, ChatMessage


@dataclass(frozen=True)
class OllamaConfig:
    """ Configuration settings for Ollama """
    base_url: str = "http://localhost:11434"
    model: str = "llama3.2:3b"
    timeout_seconds: int = 120


class OllamaChatModel(ChatModel):
    """
    ChatModel implementation backed by Ollama's /api/generate endpoint.

    We map:
    - system ChatMessages -> Ollama's `system` field
    - user/assistant ChatMessages -> Ollama's `prompt` field (plain text)
    """

    def __init__(self, config: Optional[OllamaConfig] = None):
        self._config = config or OllamaConfig()

    async def chat(self, messages: List[ChatMessage]) -> str:
        system_parts: List[str] = []
        prompt_parts: List[str] = []

        for msg in messages:
            if msg.role == "system":
                system_parts.append(msg.content)
            else:
                prefix = "User" if msg.role == "user" else "Assistant"
                prompt_parts.append(f"{prefix}: {msg.content}")

        system_text = "\n\n".join(system_parts) if system_parts else ""
        prompt_text = "\n\n".join(prompt_parts) if prompt_parts else ""

        payload: Dict[str, Any] = {
            "model": self._config.model,
            "prompt": prompt_text,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_predict": 512,
            },
        }

        if system_text:
            payload["system"] = system_text

        async with httpx.AsyncClient(
            timeout=self._config.timeout_seconds
        ) as client:
            resp = await client.post(
                f"{self._config.base_url}/api/generate",
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()

        # Prefer /api/generate shape: {"response": "..."}
        content = data.get("response")

        # Fall back to /api/chat-style shape: {"message": {"content": "..."}}
        if not content:
            message = data.get("message") or {}
            content = message.get("content")

        content = (content or "").strip()

        if not content:
            # Safe fallback instead of silently returning ""
            return (
                "I’m sorry, I could not generate a response just now. "
                "Please try rephrasing your question, "
                "or speak to your GP or cancer team for advice."
            )

        return content
