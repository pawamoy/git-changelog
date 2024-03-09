"""Tests for the `build` module."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from git_changelog import Changelog
from git_changelog.commit import AngularConvention

if TYPE_CHECKING:
    from tests.helpers import GitRepo


@pytest.mark.parametrize(
    ("bump", "expected"),
    [("auto", "0.1.0"), ("major", "0.1.0"), ("minor", "0.1.0"), ("1.1.1", "1.1.1")],
)
def test_bump_with_semver_on_new_repo(repo: GitRepo, bump: str, expected: str) -> None:
    """Bump to user specified version (semver) on new git repo.

    Parameters:
        repo: GitRepo to a temporary repository.
        bump: The bump parameter value.
        expected: Expected version for the new changelog entry.
    """
    changelog = Changelog(repo.path, convention=AngularConvention, bump=bump)
    assert len(changelog.versions_list) == 1
    assert changelog.versions_list[0].tag == expected


@pytest.mark.parametrize("bump", ["auto", "major", "minor", "2.0.0"])
def test_no_bump_on_first_tag(repo: GitRepo, bump: str) -> None:
    """Ignore bump on new git repo without unreleased commits.

    Parameters:
        repo: GitRepo to a temporary repository.
        bump: The bump parameter value.
    """
    repo.tag("1.1.1")

    changelog = Changelog(repo.path, convention=AngularConvention, bump=bump)
    assert len(changelog.versions_list) == 1
    assert changelog.versions_list[0].tag == "1.1.1"
