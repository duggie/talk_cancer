"""tests/test_story_1_3_treatments.py"""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from app.assistant_service import CancerInfoAssistant
from app.llm_base import ChatMessage, ChatModel


@dataclass
class RecordingChatModel(ChatModel):
    reply: str = "dummy reply"
    recorded_messages: list[ChatMessage] | None = None

    async def chat(self, messages: list[ChatMessage]) -> str:
        self.recorded_messages = list(messages)
        return self.reply


def recorded(model: RecordingChatModel) -> list[ChatMessage]:
    assert model.recorded_messages is not None
    return model.recorded_messages


@pytest.mark.asyncio
async def test_story_1_3_explains_treatment_in_simple_terms():
    """
    Story 1.3:
    Treatments should be explained in simple terms,
    with common experiences and clear limits.
    """

    fake_model = RecordingChatModel()
    assistant = CancerInfoAssistant(model=fake_model)

    question = "What is chemotherapy and what happens when you have it?"

    await assistant.answer_question(question)

    system_text = recorded(fake_model)[0].content.lower()

    # Simple language requirement
    assert "simple" in system_text or "clear" in system_text

    # Common experiences
    assert "side effects" in system_text
    assert "pain" in system_text or "discomfort" in system_text or "feel" in system_text
    assert "time" in system_text or "takes" in system_text

    # Variability and authority
    assert "varies" in system_text or "different for everyone" in system_text
    assert "doctor" in system_text or "cancer team" in system_text


@pytest.mark.asyncio
async def test_story_1_3_explains_tests_and_scans_without_giving_advice():
    """
    Tests and scans should be explained calmly,
    without medical advice or guarantees.
    """

    fake_model = RecordingChatModel()
    assistant = CancerInfoAssistant(model=fake_model)

    question = "What happens during a CT scan?"

    await assistant.answer_question(question)

    system_text = recorded(fake_model)[0].content.lower()

    # Plain explanation
    assert "explain" in system_text or "what happens" in system_text

    # Experience-related info
    assert "time" in system_text or "takes" in system_text
    assert (
        "pain" in system_text or "uncomfortable" in system_text or "feel" in system_text
    )

    # Safety / authority
    assert "cannot say exactly" in system_text or "varies" in system_text
    assert "hospital" in system_text or "doctor" in system_text


@pytest.mark.asyncio
async def test_story_1_3_uses_reassuring_and_non_scary_tone():
    """
    Explanations should aim to reduce anxiety.
    """

    fake_model = RecordingChatModel()
    assistant = CancerInfoAssistant(model=fake_model)

    question = "I'm worried about radiotherapy. What is it like?"

    await assistant.answer_question(question)

    system_text = recorded(fake_model)[0].content.lower()

    assert "reassure" in system_text or "many people find" in system_text
    assert "not everyone" in system_text or "can be different"
    assert "questions" in system_text or "talk to" in system_text
