# pylint: disable=redefined-outer-name
""" tests/test_cli.py """

from __future__ import annotations

import builtins
from typing import Iterable, Iterator, List

import pytest

from app import cli


class DummyModel:
    """Lightweight stand-in for OllamaChatModel."""


class DummyAssistant:
    """Async stand-in for CancerInfoAssistant that records calls."""

    def __init__(self, model: DummyModel) -> None:
        self.model = model
        self.received_questions: List[str] = []

    async def answer_question(self, question: str) -> str:
        """Mimic answering the question."""
        self.received_questions.append(question)
        return f"dummy answer for: {question}"


@pytest.fixture(autouse=True)
def dummy_assistant(monkeypatch: pytest.MonkeyPatch) -> DummyAssistant:
    """
    Automatically replace CancerInfoAssistant and OllamaChatModel in the cli
    module with dummy versions for all tests.
    """
    dummy = DummyAssistant(model=DummyModel())

    def assistant_factory(
        model: DummyModel
    ) -> DummyAssistant:  # type: ignore[override]
        # Ensure the model passed in is our DummyModel instance type
        assert isinstance(model, DummyModel)
        return dummy

    monkeypatch.setattr(cli, "OllamaChatModel", DummyModel)
    monkeypatch.setattr(cli, "CancerInfoAssistant", assistant_factory)

    return dummy


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
        print(prompt, end="")
        try:
            return next(iterator)
        except StopIteration as exc:
            raise EOFError from exc

    return fake_input  # type: ignore[return-value]


@pytest.mark.asyncio
async def test_main_greets_user_and_exits_on_quit(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
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
    assert "> " in captured
    assert "Bye." in captured


@pytest.mark.asyncio
async def test_main_ignores_empty_input_and_answers_question_then_quits(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    dummy_assistant: DummyAssistant,
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

    assert dummy_assistant.received_questions == ["What is cancer?"]
    assert "dummy answer for: What is cancer?" in captured
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
    # No responses -> first call to fake_input triggers StopIteration,
    # which _make_input_function converts into EOFError.
    fake_input = _make_input_function([])
    monkeypatch.setattr(builtins, "input", fake_input)

    await cli.main()

    captured = capsys.readouterr().out
    assert "\nBye." in captured


@pytest.mark.asyncio
async def test_main_handles_keyboardinterrupt_gracefully(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """
    If input() raises KeyboardInterrupt, main() should print '\\nBye.'
    and return.
    """

    def raise_keyboard_interrupt(prompt: str = "") -> str:
        raise KeyboardInterrupt

    monkeypatch.setattr(builtins, "input", raise_keyboard_interrupt)

    await cli.main()

    captured = capsys.readouterr().out
    assert "\nBye." in captured
