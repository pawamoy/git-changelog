"""Tests for the `cli` module."""

# IMPORTANT: Do not call `git_changelog.cli.main()`
# without passing a config file path, otherwise
# it will use its own config file and possibly modify
# the CHANGELOG!

from __future__ import annotations

import os
import sys
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Iterator

import pytest
import tomli_w

from git_changelog import cli, debug

if TYPE_CHECKING:
    from pathlib import Path

    from tests.helpers import GitRepo


if sys.version_info >= (3, 11):
    from contextlib import chdir
else:
    # TODO: remove once support for Python 3.10 is dropped
    from contextlib import contextmanager

    @contextmanager
    def chdir(path: str) -> Iterator[None]:  # noqa: D103
        old_wd = os.getcwd()
        os.chdir(path)
        try:
            yield
        finally:
            os.chdir(old_wd)


# IMPORTANT: See top module comment.
def test_main(tmp_path: Path) -> None:
    """Basic CLI test.

    Parameters:
        tmp_path: A temporary path to write an empty config to.
    """
    assert cli.main(["--config-file", str(tmp_path / "conf.toml")]) == 0


# IMPORTANT: See top module comment.
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
    parsed_settings = cli.parse_settings([*args, "-o", ch.as_posix(), "-c", "angular"])

    assert parsed_settings["output"] == str(ch.as_posix())
    assert parsed_settings["sections"] == ["feat", "fix"]
    assert parsed_settings["repository"] == "."
    assert parsed_settings["convention"] == "angular"


@pytest.mark.parametrize("is_pyproject", [True, False, None])
@pytest.mark.parametrize(
    ("sections", "sections_value"),
    [
        (None, None),
        ("", None),
        (",,", None),
        ("a, b, ", ["a", "b"]),
        ("a,  , ", ["a"]),
        ("a, b, c", ["a", "b", "c"]),
        (["a", "b", "c"], ["a", "b", "c"]),
        # Uncomment if None/null is once allowed as a value
        # ("none", None),
        # ("none, none, none", None),
    ],
)
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
        is_pyproject: Controls whether a `pyproject.toml` (`True`),
            a `.git-changelog.toml` (`False`) or a custom file (`None`) is being tested.
        sections: A `sections` config to override defaults.
        sections_value: The expectation for `sections` after reading the config file.
        parse_refs: An explicit override of the `parse_refs` of the config (if boolean)
            or skip writing the override into the test config file (`None`).
    """
    with chdir(str(tmp_path)):
        config_content: dict[str, Any] = {}

        if sections is not None:
            config_content["sections"] = sections

        if parse_refs is not None:
            config_content["parse_refs"] = parse_refs

        config_fname = "custom-file.toml" if is_pyproject is None else ".git-changelog.toml"
        config_fname = "pyproject.toml" if is_pyproject else config_fname
        tmp_path.joinpath(config_fname).write_text(
            tomli_w.dumps(
                config_content if not is_pyproject else {"tool": {"git-changelog": config_content}},
            ),
        )

        settings = cli.read_config(tmp_path / config_fname) if config_fname == "custom-file.toml" else cli.read_config()

        ground_truth: dict[str, Any] = cli.DEFAULT_SETTINGS.copy()
        ground_truth["sections"] = sections_value
        ground_truth["parse_refs"] = bool(parse_refs)

        assert settings == ground_truth


@pytest.mark.parametrize("value", [None, False, True])
def test_settings_warning(
    tmp_path: Path,
    value: bool,
) -> None:
    """Check warning on bump_latest.

    Parameters:
        tmp_path: A temporary path to write the settings file into.
    """
    with chdir(str(tmp_path)):
        args: list[str] = []
        if value is not None:
            (tmp_path / ".git-changelog.toml").write_text(
                tomli_w.dumps({"bump_latest": value}),
            )
        else:
            args = ["--bump-latest"]

        with pytest.warns(FutureWarning) as record:
            cli.parse_settings(args)

            solution = "is deprecated in favor of"  # Warning comes from CLI parsing.
            if value is not None:  # Warning is issued when parsing the config file.
                solution = "remove" if not value else "auto"

            assert len(record) == 1
            assert solution in str(record[0].message)

        # If setting is in config file AND passed by CLI, two FutureWarnings are issued.
        if (tmp_path / ".git-changelog.toml").exists():
            with pytest.warns(FutureWarning) as record:
                cli.parse_settings(["--bump-latest"])

                assert len(record) == 2


# IMPORTANT: See top module comment.
def test_show_version(capsys: pytest.CaptureFixture) -> None:
    """Show version.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    with pytest.raises(SystemExit):
        cli.main(["-V"])
    captured = capsys.readouterr()
    assert debug.get_version() in captured.out


# IMPORTANT: See top module comment.
def test_show_debug_info(capsys: pytest.CaptureFixture) -> None:
    """Show debug information.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    with pytest.raises(SystemExit):
        cli.main(["--debug-info"])
    captured = capsys.readouterr().out.lower()
    assert "python" in captured
    assert "system" in captured
    assert "environment" in captured
    assert "packages" in captured


# IMPORTANT: See top module comment.
def test_jinja_context(repo: GitRepo) -> None:
    """Render template with custom template variables.

    Parameters:
        repo: Temporary Git repository (fixture).
    """
    repo.path.joinpath("conf.toml").write_text(
        dedent(
            """[jinja_context]
            k1 = "ignored"
            k2 = "v2"
            k3 = "v3"
            """,
        ),
    )

    template = repo.path.joinpath(".custom_template.md.jinja")
    template.write_text("{% for key, val in jinja_context.items() %}{{ key }} = {{ val }}\n{% endfor %}")

    exit_code = cli.main(
        [
            "--config-file",
            str(repo.path / "conf.toml"),
            "-o",
            str(repo.path / "CHANGELOG.md"),
            "-t",
            f"path:{template}",
            "--jinja-context",
            "k1=v1",
            "-j",
            "k3=v3",
            str(repo.path),
        ],
    )

    assert exit_code == 0

    contents = repo.path.joinpath("CHANGELOG.md").read_text()
    assert contents == "k1 = v1\nk2 = v2\nk3 = v3\n"
