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


def test_one_release_branch_with_feat_branch(repo: GitRepo) -> None:
    r"""Test parsing and grouping commits to versions.

    Commit graph:
                   1.0.0
                     |
    main       A-B---D
                \   /
    feat         --C

    Expected:
    - 1.0.0: D B C A

    Parameters:
        repo: GitRepo to a temporary repository.
    """
    commit_a = repo.first_hash
    repo.branch("develop")
    commit_b = repo.commit("fix: B")
    repo.checkout("develop")
    commit_c = repo.commit("feat: C")
    repo.checkout("main")
    commit_d = repo.merge("develop")
    repo.tag("1.0.0")

    changelog = Changelog(repo.path, convention=AngularConvention)

    assert len(changelog.versions_list) == 1
    version = changelog.versions_list[0]
    assert version.tag == "1.0.0"
    assert len(version.commits) == 4
    hashes = [commit.hash for commit in version.commits]
    assert hashes == [commit_d, commit_b, commit_c, commit_a]


def test_one_release_branch_with_two_versions(repo: GitRepo) -> None:
    r"""Test parsing and grouping commits to versions.

    Commit graph:
                   1.1.0
               1.0.0 |
                 |   |
    main       A-B---D
                \   /
    feat         --C

    Expected:
    - 1.1.0: D C
    - 1.0.0: B A

    Parameters:
        repo: GitRepo to a temporary repository.
    """
    commit_a = repo.first_hash
    repo.branch("develop")
    commit_b = repo.commit("fix: B")
    repo.tag("1.0.0")
    repo.checkout("develop")
    commit_c = repo.commit("feat: C")
    repo.checkout("main")
    commit_d = repo.merge("develop")
    repo.tag("1.1.0")

    changelog = Changelog(repo.path, convention=AngularConvention)

    assert len(changelog.versions_list) == 2
    version = changelog.versions_list[0]
    assert version.tag == "1.1.0"
    hashes = [commit.hash for commit in version.commits]
    assert hashes == [commit_d, commit_c]

    version = changelog.versions_list[1]
    assert version.tag == "1.0.0"
    hashes = [commit.hash for commit in version.commits]
    assert hashes == [commit_b, commit_a]
