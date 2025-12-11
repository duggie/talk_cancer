# tests/test_cli.py

from __future__ import annotations

import builtins
from typing import Iterable, Iterator, List

import pytest

from app import cli


class DummyModel:
    """Lightweight stand-in for OllamaChatModel."""
    pass


class DummyAssistant:
    """Async stand-in for CancerInfoAssistant that records calls."""

    def __init__(self, model: DummyModel) -> None:
        self.model = model
        self.received_questions: List[str] = []

    async def answer_question(self, question: str) -> str:
        self.received_questions.append(question)
        return f"dummy answer for: {question}"


@pytest.fixture(autouse=True)
def patch_assistant_and_model(monkeypatch: pytest.MonkeyPatch) -> DummyAssistant:
    """
    Automatically replace CancerInfoAssistant and OllamaChatModel in the cli
    module with dummy versions for all tests.
    """

    dummy_assistant = DummyAssistant(model=DummyModel())

    # When cli.CancerInfoAssistant(model=...) is called, return our instance.
    def assistant_factory(model: DummyModel) -> DummyAssistant:  # type: ignore[override]
        # Ensure the model passed in is our DummyModel instance type
        assert isinstance(model, DummyModel)
        return dummy_assistant

    monkeypatch.setattr(cli, "OllamaChatModel", DummyModel)
    monkeypatch.setattr(cli, "CancerInfoAssistant", assistant_factory)

    return dummy_assistant


def _make_input_function(responses: Iterable[str]) -> builtins.input:
    """
    Create a fake input() that sequentially returns the given responses.
    If it is called more times than there are responses, it raises EOFError
    (just like the real input can at end of file).
    """
    iterator: Iterator[str] = iter(responses)

    def fake_input(prompt: str = "") -> str:
        # Emulate real input() behaviour: print the prompt to stdout
        assert isinstance(prompt, str)
        print(prompt, end="")  # <-- this line is the key change
        try:
            return next(iterator)
        except StopIteration as exc:
            raise EOFError from exc

    return fake_input  # type: ignore[return-value]


@pytest.mark.asyncio
async def test_main_greets_user_and_exits_on_quit(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """
    main() should print the banner, accept a single 'quit' command and exit
    cleanly with 'Bye.'.
    """
    fake_input = _make_input_function(["quit"])
    monkeypatch.setattr(builtins, "input", fake_input)

    await cli.main()

    captured = capsys.readouterr().out

    assert "Kind Cancer Info – NI (local, Ollama-backed)" in captured
    # Ensure it prompts the user
    assert "> " in captured
    # Ensure it exits politely
    assert "Bye." in captured


@pytest.mark.asyncio
async def test_main_ignores_empty_input_and_answers_question_then_quits(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    patch_assistant_and_model: DummyAssistant,
) -> None:
    """
    main() should:
    - ignore empty input
    - call the assistant for a non-empty question
    - then exit when the user types 'quit'
    """
    fake_input = _make_input_function(["", "What is cancer?", "quit"])
    monkeypatch.setattr(builtins, "input", fake_input)

    await cli.main()

    captured = capsys.readouterr().out

    # The dummy assistant should have been called exactly once with the question
    assert patch_assistant_and_model.received_questions == ["What is cancer?"]

    # Its answer should be printed
    assert "dummy answer for: What is cancer?" in captured

    # And we should eventually see the exit message
    assert "Bye." in captured


@pytest.mark.asyncio
async def test_main_exits_on_exit_keyword_case_insensitive(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    'exit' (in any case) should behave like 'quit' and terminate the loop.
    """
    fake_input = _make_input_function(["EXIT"])
    monkeypatch.setattr(builtins, "input", fake_input)

    await cli.main()

    captured = capsys.readouterr().out
    assert "Bye." in captured


@pytest.mark.asyncio
async def test_main_handles_eoferror_gracefully(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    If input() raises EOFError, main() should print '\\nBye.' and return.
    """

    def raise_eof(prompt: str = "") -> str:
        raise EOFError

    monkeypatch.setattr(builtins, "input", raise_eof)

    await cli.main()

    captured = capsys.readouterr().out

    # The exact behaviour in the file is: print("\nBye.")
    assert "\nBye." in captured


@pytest.mark.asyncio
async def test_main_handles_keyboardinterrupt_gracefully(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    If input() raises KeyboardInterrupt, main() should print '\\nBye.' and return.
    """

    def raise_keyboard_interrupt(prompt: str = "") -> str:
        raise KeyboardInterrupt

    monkeypatch.setattr(builtins, "input", raise_keyboard_interrupt)

    await cli.main()

    captured = capsys.readouterr().out
    assert "\nBye." in captured
