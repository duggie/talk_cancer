"""app/assistant_service.py"""

from __future__ import annotations

from enum import Enum

from .llm_base import ChatMessage, ChatModel


class SymptomUrgency(Enum):
    """Flag up urgency of symptom(s)"""

    RED_FLAG = "red_flag"
    CONCERNING = "concerning"
    MILD = "mild"


BASE_SYSTEM_PROMPT = """You are "Kind Cancer Info – Northern Ireland".

You help people affected by cancer: adults with cancer, family members, and
children or teenagers.

You explain things in clear, everyday English.
You are not a doctor or nurse.
You do not diagnose conditions or decide treatment.
You do not tell people to start, stop, or change medicines.

You encourage people to speak to their own cancer team or GP, who know their situation
best.

Always be kind, calm, and non-judgemental.
Use short sentences and avoid medical jargon.
"""


RED_FLAG_SYSTEM_PROMPT = (
    BASE_SYSTEM_PROMPT
    + """

The user may be describing a symptom that could be serious.

You must:
- Say that you cannot tell what is happening over chat.
- Make it clear that this could be urgent.
- Advise the user to get urgent medical help now.

For Northern Ireland and the UK:
- Call 999 or go to A&E.
- Or contact their cancer team's emergency number if they have one.
"""
)


CONCERNING_SYSTEM_PROMPT = (
    BASE_SYSTEM_PROMPT
    + """

The user may be describing a symptom that needs medical attention but
is not clearly an emergency.

You must:
- Explain in general terms what people sometimes experience.
- Advise contacting their cancer team or GP soon.
- Say that their team can decide if this needs checking or treatment.
"""
)


MILD_SYSTEM_PROMPT = (
    BASE_SYSTEM_PROMPT
    + """

The symptom described may be common during or after cancer treatment.

You must:
- Reassure gently.
- Explain that this can happen for some people.
- Advise monitoring the symptom.
- Say to contact their cancer team or GP if it gets worse or does not improve.
"""
)


TREATMENT_SYSTEM_PROMPT = (
    BASE_SYSTEM_PROMPT
    + """

The user is asking what a test, scan, or treatment involves (for example: chemotherapy,
radiotherapy, surgery, CT scans).

You must:
- Explain it in clear, simple terms.
- Describe common experiences people often ask about:
  - how long it takes (time),
  - whether it hurts or feels uncomfortable (pain or discomfort),
  - common side effects (side effects).
- Be reassuring without making promises. You can say things like "many people find…"
and “this is often manageable”.
- Make it clear that the detail varies from person to person and between hospitals.
- Remind them their hospital team and doctor are the authority and can tell them
exactly what to expect for their situation.
- Suggest a few practical questions they can ask their team.
"""
)


class CancerInfoAssistant:
    """
    High-level assistant for answering questions.

    It depends only on the ChatModel interface,
    so the underlying provider can be Ollama, Bedrock, OpenAI, etc.
    """

    def __init__(self, model: ChatModel):
        self._model = model

    async def answer_question(self, question: str) -> str:
        """
        Take a free-form user question and return a plain language answer.
        Also identify the level of risk for the presented symptoms.
        It does this using a simple keyword approach. It's not using
        Natural Language Processing (NLP) or an advanced technique. As such,
        it's not understanding the content. "I don't have a fever" will
        trigger a RED_FLAG for use of word "fever".
        *** Note: this is NOT a diagnostic tool. ***
        """
        if is_treatment_or_procedure_question(question):
            system_prompt = TREATMENT_SYSTEM_PROMPT
        else:
            urgency = classify_symptom_urgency(question)

            if urgency == SymptomUrgency.RED_FLAG:
                system_prompt = RED_FLAG_SYSTEM_PROMPT
            elif urgency == SymptomUrgency.CONCERNING:
                system_prompt = CONCERNING_SYSTEM_PROMPT
            else:
                system_prompt = MILD_SYSTEM_PROMPT

        messages: list[ChatMessage] = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=question),
        ]
        return await self._model.chat(messages)


SYMPTOM_URGENCY_MAPPING = {
    SymptomUrgency.RED_FLAG: [
        lambda t: ("fever" in t or "temperature" in t)
        and ("chemo" in t or "chemotherapy" in t),
        lambda t: "chest pain" in t
        or "trouble breathing" in t
        or "short of breath" in t,
    ],
    SymptomUrgency.CONCERNING: [
        lambda t: "new pain" in t or "lump" in t or "swelling" in t,
    ],
}


def classify_symptom_urgency(text: str) -> SymptomUrgency:
    """
    Very simple, conservative keyword-based classification.
    This is NOT diagnosis. It only guides safety framing.
    """

    t = text.lower()
    for urgency, conditions in SYMPTOM_URGENCY_MAPPING.items():
        if any(condition(t) for condition in conditions):
            return urgency
    return SymptomUrgency.MILD


def is_treatment_or_procedure_question(text: str) -> bool:
    """
    Determine the type of question being asked. This is based simply on a scan
    of the words being used in the user-supplied prompt. This is deliberately
    simple. It's not relying on complex NLP or algorithm behaviour.
    """
    t = text.lower()

    treatment_terms = (
        "chemotherapy",
        "chemo",
        "radiotherapy",
        "radio therapy",
        "surgery",
        "operation",
        "immunotherapy",
        "hormone therapy",
        "hormonal therapy",
        "targeted therapy",
    )

    test_scan_terms = (
        "ct scan",
        "ct",
        "mri",
        "pet",
        "x-ray",
        "xray",
        "scan",
        "biopsy",
        "blood test",
        "endoscopy",
        "colonoscopy",
        "stent",
        "port",
        "picc",
    )

    question_cues = (
        "what is",
        "what happens",
        "what will happen",
        "what is it like",
        "how does",
        "how long",
        "does it hurt",
        "will it hurt",
        "what should i expect",
    )

    mentions_treatment_or_test = any(
        term in t for term in (*treatment_terms, *test_scan_terms)
    )
    looks_like_question = "?" in t or any(cue in t for cue in question_cues)

    return mentions_treatment_or_test and looks_like_question
