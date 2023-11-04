"""Test version bumping."""

from __future__ import annotations

import pytest

from git_changelog.build import bump


@pytest.mark.parametrize(
    ("version", "bumped"),
    [
        ("0.0.1", "0.0.2"),
        ("0.1.0", "0.1.1"),
        ("0.1.1", "0.1.2"),
        ("1.0.0", "1.0.1"),
        ("1.0.1", "1.0.2"),
        ("1.1.0", "1.1.1"),
        ("1.1.1", "1.1.2"),
        ("v0.0.1", "v0.0.2"),
        ("v0.1.0", "v0.1.1"),
        ("v0.1.1", "v0.1.2"),
        ("v1.0.0", "v1.0.1"),
        ("v1.0.1", "v1.0.2"),
        ("v1.1.0", "v1.1.1"),
        ("v1.1.1", "v1.1.2"),
    ],
)
def test_bump_patch(version: str, bumped: str) -> None:
    """Test default and patch version bumping.

    Parameters:
        version: The base version.
        bumped: The expected, bumped version.
    """
    assert bump(version) == bump(version, "patch") == bumped


@pytest.mark.parametrize(
    ("version", "bumped"),
    [
        ("0.0.1", "0.1.0"),
        ("0.1.0", "0.2.0"),
        ("0.1.1", "0.2.0"),
        ("1.0.0", "1.1.0"),
        ("1.0.1", "1.1.0"),
        ("1.1.0", "1.2.0"),
        ("1.1.1", "1.2.0"),
        ("v0.0.1", "v0.1.0"),
        ("v0.1.0", "v0.2.0"),
        ("v0.1.1", "v0.2.0"),
        ("v1.0.0", "v1.1.0"),
        ("v1.0.1", "v1.1.0"),
        ("v1.1.0", "v1.2.0"),
        ("v1.1.1", "v1.2.0"),
    ],
)
def test_bump_minor(version: str, bumped: str) -> None:
    """Test minor version bumping.

    Parameters:
        version: The base version.
        bumped: The expected, bumped version.
    """
    assert bump(version, "minor") == bumped


@pytest.mark.parametrize(
    ("version", "bumped"),
    [
        ("0.0.1", "1.0.0"),
        ("0.1.0", "1.0.0"),
        ("0.1.1", "1.0.0"),
        ("1.0.0", "2.0.0"),
        ("1.0.1", "2.0.0"),
        ("1.1.0", "2.0.0"),
        ("1.1.1", "2.0.0"),
        ("v0.0.1", "v1.0.0"),
        ("v0.1.0", "v1.0.0"),
        ("v0.1.1", "v1.0.0"),
        ("v1.0.0", "v2.0.0"),
        ("v1.0.1", "v2.0.0"),
        ("v1.1.0", "v2.0.0"),
        ("v1.1.1", "v2.0.0"),
    ],
)
def test_bump_major_no_zerover(version: str, bumped: str) -> None:
    """Test major version bumping without zerover.

    Parameters:
        version: The base version.
        bumped: The expected, bumped version.
    """
    assert bump(version, "major", zerover=False) == bumped


@pytest.mark.parametrize(
    ("version", "bumped"),
    [
        ("0.0.1", "0.1.0"),
        ("0.1.0", "0.2.0"),
        ("0.1.1", "0.2.0"),
        ("1.0.0", "2.0.0"),
        ("1.0.1", "2.0.0"),
        ("1.1.0", "2.0.0"),
        ("1.1.1", "2.0.0"),
        ("v0.0.1", "v0.1.0"),
        ("v0.1.0", "v0.2.0"),
        ("v0.1.1", "v0.2.0"),
        ("v1.0.0", "v2.0.0"),
        ("v1.0.1", "v2.0.0"),
        ("v1.1.0", "v2.0.0"),
        ("v1.1.1", "v2.0.0"),
    ],
)
def test_bump_major_zerover(version: str, bumped: str) -> None:
    """Test major version bumping with zerover.

    Parameters:
        version: The base version.
        bumped: The expected, bumped version.
    """
    assert bump(version, "major", zerover=True) == bumped
