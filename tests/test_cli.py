"""Tests for the `cli` module."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pytest
import toml

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


@pytest.mark.parametrize("is_pyproject", [True, False, None])
@pytest.mark.parametrize(("sections", "sections_value"), [
    (None, None),
    ("", None),
    (",,", None),
    ("force-null", None),
    ("a, b, ", ["a", "b"]),
    ("a,  , ", ["a"]),
    ("a, b, c", ["a", "b", "c"]),
    (["a", "b", "c"], ["a", "b", "c"]),
    # Uncomment if None/null is once allowed as a value
    # ("none", None),
    # ("none, none, none", None),
])
@pytest.mark.parametrize("parse_refs", [None, False, True])
def test_config_reading(
    tmp_path: Path,
    is_pyproject: bool | None,
    sections: str | list[str] | None,
    sections_value: list | None,
    parse_refs: bool | None,
) -> None:
    """Check settings files are correctly interpreted.

    Parameters:
        tmp_path: A temporary path to write the settings file into.
        is_pyproject: controls whether a ``pyproject.toml`` (``True``),
        a ``.git-changelog.toml`` (``False``) or a custom file (``None``) is being tested.
        sections: A ``sections`` config to override defaults.
        sections_falue: The expectation for ``sections`` after reading the config file.
        parse_refs: A explicit override of the ``parse_refs`` of the config (if boolean)
        or skip writing the override into the test config file (``None``).
    """
    os.chdir(tmp_path)

    config_content = {}

    if sections is not None:
        config_content["sections"] = None if sections == "force-null" else sections

    if parse_refs is not None:
        config_content["parse_refs"] = parse_refs

    config_fname = "custom-file.toml" if is_pyproject is None else ".git-changelog.toml"
    config_fname = "pyproject.toml" if is_pyproject else config_fname
    (tmp_path / config_fname).write_text(
        toml.dumps(
            config_content if not is_pyproject
            else {"tool": {"git-changelog": config_content}},
        ),
    )

    settings = (
        cli.read_config(tmp_path / config_fname) if config_fname == "custom-file.toml"
        else cli.read_config()
    )

    ground_truth = cli.DEFAULT_SETTINGS.copy()
    ground_truth["sections"] = sections_value
    ground_truth["parse_refs"] = bool(parse_refs)

    assert settings == ground_truth
