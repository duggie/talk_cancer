"""tests/test_story_1_2_symptoms.py"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

import pytest

from app.llm_base import ChatModel, ChatMessage
from app.assistant_service import CancerInfoAssistant


@dataclass
class RecordingChatModel(ChatModel):
    """
    Fake model that records the messages passed to it.
    """

    reply: str = "dummy reply"
    recorded_messages: List[ChatMessage] | None = None

    async def chat(self, messages: List[ChatMessage]) -> str:
        self.recorded_messages = list(messages)
        return self.reply


@pytest.mark.asyncio
async def test_story_1_2_red_flag_symptom_triggers_urgent_guidance():
    """
    Story 1.2:
    If a user describes a red-flag symptom (e.g. fever during chemo),
    the assistant must frame the response as urgent and direct the user
    to emergency or cancer team support.
    """

    fake_model = RecordingChatModel()
    assistant = CancerInfoAssistant(model=fake_model)

    question = "I am on chemotherapy and I have had a high fever all night."

    await assistant.answer_question(question)

    assert fake_model.recorded_messages is not None

    system_msg = fake_model.recorded_messages[0]
    user_msg = fake_model.recorded_messages[1]

    # User message is passed through unchanged
    assert user_msg.content == question

    # System prompt must include urgency guidance
    system_text = system_msg.content.lower()

    assert "urgent" in system_text
    assert "999" in system_text or "a&e" in system_text
    assert "cancer team" in system_text

    # Explicitly NOT diagnosing
    assert "diagnose" in system_text
    assert "not a doctor" in system_text


@pytest.mark.asyncio
async def test_story_1_2_concerning_symptom_prompts_contact_with_team():
    """
    If a symptom is concerning but not clearly an emergency,
    the assistant should advise contacting the cancer team or GP.
    """

    fake_model = RecordingChatModel()
    assistant = CancerInfoAssistant(model=fake_model)

    question = "I have new pain in my back that started this week."

    await assistant.answer_question(question)

    assert fake_model.recorded_messages is not None
    system_msg = fake_model.recorded_messages[0]
    system_text = system_msg.content.lower()

    assert "cancer team" in system_text or "gp" in system_text
    assert "urgent" not in system_text or "999" not in system_text


@pytest.mark.asyncio
async def test_story_1_2_mild_symptom_allows_monitoring():
    """
    For mild or common symptoms, the assistant should allow monitoring
    while still encouraging the user to speak to their team if it worsens.
    """

    fake_model = RecordingChatModel()
    assistant = CancerInfoAssistant(model=fake_model)

    question = "I feel more tired than usual after treatment."

    await assistant.answer_question(question)

    assert fake_model.recorded_messages is not None
    system_text = fake_model.recorded_messages[0].content.lower()

    assert "common" in system_text or "can happen" in system_text
    assert "if it gets worse" in system_text or "if it does not improve" in system_text
    assert "cancer team" in system_text


@pytest.mark.asyncio
async def test_story_1_2_red_flag_chest_pain_triggers_urgent_guidance():
    """
    For high risk symptoms, the assistant should trigger the need for
    urgent follow-up with medical professionals.
    """
    fake_model = RecordingChatModel()
    assistant = CancerInfoAssistant(model=fake_model)

    question = "I have chest pain and I feel short of breath."

    await assistant.answer_question(question)

    assert fake_model.recorded_messages is not None
    system_text = fake_model.recorded_messages[0].content.lower()

    assert "urgent" in system_text
    assert "999" in system_text or "a&e" in system_text
    assert "cancer team" in system_text
