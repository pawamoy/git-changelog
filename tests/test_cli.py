"""Tests for the `cli` module."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from git_changelog import cli

if TYPE_CHECKING:
    from pathlib import Path


def test_main() -> None:
    """Basic CLI test."""
    assert cli.main([]) == 0


def test_show_help(capsys: pytest.CaptureFixture) -> None:
    """Show help.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    with pytest.raises(SystemExit):
        cli.main(["-h"])
    captured = capsys.readouterr()
    assert "git-changelog" in captured.out


def test_get_version() -> None:
    """Get self version."""
    assert cli.get_version()


@pytest.mark.parametrize(
    "args",
    [
        (".", "-s", "feat,fix"),
        ("-s", "feat,fix", "."),
    ],
)
def test_passing_repository_and_sections(tmp_path: Path, args: tuple[str]) -> None:
    """Render the changelog of given repository, choosing sections.

    Parameters:
        tmp_path: A temporary path to write the changelog into.
        args: Command line arguments.
    """
    ch = tmp_path.joinpath("ch.md")
    assert cli.main([*args, "-o", ch.as_posix(), "-c", "angular"]) == 0
