"""Tests for user story 1.1 Ask free-form questions"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

import pytest

from app.llm_base import ChatModel, ChatMessage
from app.assistant_service import CancerInfoAssistant


@dataclass
class FakeChatModel(ChatModel):
    """
    Fake model used for TDD.
    Records messages and returns a canned response.
    """

    response_text: str
    recorded_messages: List[ChatMessage] | None = None

    async def chat(self, messages: List[ChatMessage]) -> str:
        """Chat function to help with tests"""
        self.recorded_messages = list(messages)
        return self.response_text


@pytest.mark.asyncio
async def test_story_1_1_free_form_question_gets_answer():
    """
    Story 1.1:
    As a person affected by cancer,
    I want to ask free-form questions in my own words
    so that I can get an understandable answer.
    """

    fake_model = FakeChatModel(
        response_text="This is a simple answer in plain language."
    )
    assistant = CancerInfoAssistant(model=fake_model)

    question = "My mum has just started chemo in Belfast. Does it hurt?"
    answer = await assistant.answer_question(question)

    # We get some answer text back
    assert isinstance(answer, str)
    assert "simple answer" in answer

    # The assistant has passed a system + user message to the model
    assert fake_model.recorded_messages is not None
    messages = fake_model.recorded_messages
    assert len(messages) == 2

    system_msg, user_msg = messages

    # System prompt sets the persona (Kind Cancer Info – NI)
    assert system_msg.role == "system"
    assert "Kind Cancer Info – Northern Ireland" in system_msg.content
    assert "not a doctor" in system_msg.content.lower()
    assert "Northern Ireland" in system_msg.content

    # User question is passed through unchanged
    assert user_msg.role == "user"
    assert user_msg.content == question
