"""Tests for the `cli` module."""

import pytest

from git_changelog import cli


def test_main():
    """Basic CLI test."""
    with pytest.raises(SystemExit):
        cli.main([])


def test_show_help(capsys):
    """
    Show help.

    Arguments:
        capsys: Pytest fixture to capture output.
    """
    with pytest.raises(SystemExit):
        cli.main(["-h"])
    captured = capsys.readouterr()
    assert "git-changelog" in captured.out


def test_get_version():
    """Get self version."""
    assert cli.get_version()
