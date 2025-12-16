"""app/llm_base.py"""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol, Literal, List


Role = Literal["system", "user", "assistant"]


@dataclass(frozen=True)
class ChatMessage:
    """ChatMessage"""

    role: Role
    content: str


class ChatModel(Protocol):
    """
    Interface for any chat model (Ollama, Bedrock, OpenAI, etc.).
    """

    @abstractmethod
    async def chat(self, messages: List[ChatMessage]) -> str:
        """
        Send a list of messages to the model and return the assistant's reply.
        """
