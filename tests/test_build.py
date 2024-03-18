"""Tests for the `build` module."""

from __future__ import annotations

from time import sleep
from typing import TYPE_CHECKING

import pytest

from git_changelog import Changelog
from git_changelog.commit import AngularConvention

if TYPE_CHECKING:
    from git_changelog.build import Version
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
    _assert_version(
        changelog.versions_list[0],
        expected_tag="1.0.0",
        expected_prev_tag=None,
        expected_commits=[commit_d, commit_b, commit_c, commit_a],
    )


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
    _assert_version(
        changelog.versions_list[0],
        expected_tag="1.1.0",
        expected_prev_tag="1.0.0",
        expected_commits=[commit_d, commit_c],
    )
    _assert_version(
        changelog.versions_list[1],
        expected_tag="1.0.0",
        expected_prev_tag=None,
        expected_commits=[commit_b, commit_a],
    )


def test_two_release_branches(repo: GitRepo) -> None:
    r"""Test parsing and grouping commits to versions.

    Commit graph:
                   1.1.0
               1.0.0 |
                 |   |
    main       A-B---D-----G
                \     \   /
    develop      --C---E-F
                       |
                     2.0.0
    Expected:
    - Unreleased: G F
    - 2.0.0: E C
    - 1.1.0: D
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
    commit_d = repo.commit("fix: C")
    repo.tag("1.1.0")
    repo.checkout("develop")
    # Git timestamp only has second precision,
    # so we delay to ensure git-log lists it before commit C.
    sleep(1)
    commit_e = repo.merge("main")
    repo.tag("2.0.0")
    commit_f = repo.commit("feat: F")
    repo.checkout("main")
    commit_g = repo.merge("develop")

    changelog = Changelog(repo.path, convention=AngularConvention)

    assert len(changelog.versions_list) == 4
    versions = iter(changelog.versions_list)
    _assert_version(next(versions), expected_tag="", expected_prev_tag="2.0.0", expected_commits=[commit_g, commit_f])
    _assert_version(
        next(versions),
        expected_tag="2.0.0",
        expected_prev_tag="1.1.0",
        expected_commits=[commit_e, commit_c],
    )
    _assert_version(next(versions), expected_tag="1.1.0", expected_prev_tag="1.0.0", expected_commits=[commit_d])
    _assert_version(next(versions), expected_tag="1.0.0", expected_prev_tag=None, expected_commits=[commit_b, commit_a])


def _assert_version(
    version: Version,
    expected_tag: str,
    expected_prev_tag: str | None,
    expected_commits: list[str],
) -> None:
    assert version.tag == expected_tag
    if expected_prev_tag:
        assert version.previous_version is not None, f"Expected previous version '{expected_prev_tag}', but was None"
        assert version.previous_version.tag == expected_prev_tag
    else:
        assert version.previous_version is None
    hashes = [commit.hash for commit in version.commits]
    assert hashes == expected_commits


def test_no_remote_url(repo: GitRepo) -> None:
    """Test parsing and grouping commits to versions without a git remote.

    Parameters:
        repo: GitRepo to a temporary repository.
    """
    repo.git("remote", "remove", "origin")
    commit_a = repo.first_hash
    repo.tag("1.0.0")

    changelog = Changelog(repo.path, convention=AngularConvention)

    assert len(changelog.versions_list) == 1
    _assert_version(
        changelog.versions_list[0],
        expected_tag="1.0.0",
        expected_prev_tag=None,
        expected_commits=[commit_a],
    )


def test_merge_into_unreleased(repo: GitRepo) -> None:
    r"""Test parsing and grouping commits to versions.

    Commit graph:
    main       A---C---E
                \ / \ /
    feat         B   D

    Expected:
    - Unreleased: E D C B A

    Parameters:
        repo: GitRepo to a temporary repository.
    """
    commit_a = repo.first_hash
    repo.branch("feat/1")
    repo.checkout("feat/1")
    commit_b = repo.commit("feat: B")
    repo.checkout("main")
    commit_c = repo.merge("feat/1")
    repo.branch("feat/2")
    repo.checkout("feat/2")
    commit_d = repo.commit("feat: D")
    repo.checkout("main")
    commit_e = repo.merge("feat/2")

    changelog = Changelog(repo.path, convention=AngularConvention)

    assert len(changelog.versions_list) == 1
    version = changelog.versions_list[0]
    _assert_version(
        version,
        expected_tag="0.1.0",
        expected_prev_tag=None,
        expected_commits=[commit_e, commit_c, commit_d, commit_a, commit_b],
    )
