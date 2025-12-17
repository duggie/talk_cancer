"""
nox is a command-line tool that automates testing in multiple Python environments
See: https://nox.thea.codes/en/stable/
"""

import os
import nox  # type: ignore[import-not-found]


PYTHON = "3.14"


def _set_pythonpath(session: nox.Session) -> None:
    """ Mirrors: echo "PYTHONPATH=$PWD" """
    session.env["PYTHONPATH"] = os.getcwd()


def _require_venv(session: nox.Session) -> None:
    """check to ensure we are running inside a virtual environment rather than system"""
    if session.virtualenv is None and os.environ.get("VIRTUAL_ENV") is None:
        session.error("No active virtualenv; activate one or drop -R")


@nox.session(python=PYTHON)
def quality(session: nox.Session) -> None:
    """Check with ruff, pyright, bandit & pip-audit"""
    _require_venv(session)
    session.install("--upgrade", "pip")
    session.install("-r", "requirements.txt", "-r", "requirements-dev.txt")

    _set_pythonpath(session)

    session.run("ruff", "format", "--check", ".", external=True)
    session.run("ruff", "check", ".", external=True)
    session.run("pyright", external=True)
    session.run("bandit", "-q", "-r", "app", external=True)
    session.run("pip-audit", external=True)


@nox.session(python=PYTHON)
def tests(session: nox.Session) -> None:
    """Run tests using pytest & ensure at least 80% code coverage"""
    _require_venv(session)
    session.install("--upgrade", "pip")
    session.install("-r", "requirements.txt", "-r", "requirements-dev.txt")

    _set_pythonpath(session)

    session.run("coverage", "run", "-m", "pytest", external=True)
    session.run("coverage", "report", "--fail-under=80", external=True)


@nox.session(python=PYTHON)
def types(session: nox.Session) -> None:
    """Run pyright analysis"""
    _require_venv(session)
    session.install("--upgrade", "pip")
    session.install("-r", "requirements.txt", "-r", "requirements-dev.txt")

    _set_pythonpath(session)

    session.run("pyright", external=True)
