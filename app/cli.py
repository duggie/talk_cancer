from __future__ import annotations

import asyncio

from .assistant_service import CancerInfoAssistant
from .llm_ollama import OllamaChatModel


async def main() -> None:
    assistant = CancerInfoAssistant(model=OllamaChatModel())

    print("Kind Cancer Info – NI (local, Ollama-backed)")
    print("Type your question and press Enter. Type 'quit' to exit.\n")

    while True:
        try:
            question = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            return

        if not question:
            continue
        if question.lower() in {"quit", "exit"}:
            print("Bye.")
            return

        answer = await assistant.answer_question(question)
        print(f"\n{answer}\n")


if __name__ == "__main__":
    asyncio.run(main())
