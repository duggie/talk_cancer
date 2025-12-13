"""tests/test_llm_base.py"""
import pytest

from app.llm_base import ChatModel, ChatMessage


@pytest.mark.asyncio
async def test_chatmodel_protocol_method_raises_not_implemented() -> None:
    """Call the protocol method directly; it should raise by design."""
    with pytest.raises(NotImplementedError):
        await ChatModel.chat(object(), [ChatMessage(role="user", content="hi")])
