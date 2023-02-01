"""Test version bumping."""

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
def test_bump_patch(version, bumped):
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
def test_bump_minor(version, bumped):
    """Test minor version bumping.

    Parameters:
        version: The base version.
        bumped: The expected, bumped version.
    """
    assert bump(version, "minor") == bumped


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
def test_bump_major(version, bumped):
    """Test major version bumping.

    Parameters:
        version: The base version.
        bumped: The expected, bumped version.
    """
    assert bump(version, "major") == bumped
