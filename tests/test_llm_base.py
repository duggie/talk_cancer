"""tests/test_llm_base.py"""

import pytest

from app.llm_base import ChatModel, ChatMessage


class _ConcreteModel(ChatModel):
    async def chat(self, messages: list[ChatMessage]) -> str:
        raise NotImplementedError


@pytest.mark.asyncio
async def test_chatmodel_chat_raises_not_implemented() -> None:
    with pytest.raises(NotImplementedError):
        await _ConcreteModel().chat([ChatMessage(role="user", content="hi")])
