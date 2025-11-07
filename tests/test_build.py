"""Tests for the `build` module."""

from __future__ import annotations

from time import sleep
from typing import TYPE_CHECKING, Literal

import pytest

from git_changelog import AngularConvention, BasicConvention, Changelog

if TYPE_CHECKING:
    from git_changelog import Version
    from tests.helpers import GitRepo


@pytest.mark.parametrize(
    ("versioning", "bump", "expected"),
    [
        ("semver", "auto", "0.0.1"),  # chore commit
        ("semver", "major", "1.0.0"),
        ("semver", "minor", "0.1.0"),
        ("semver", "patch", "0.0.1"),
        ("semver", "1.1.1", "1.1.1"),
        ("pep440", "auto", "0.0.1"),  # chore commit
        ("pep440", "major", "1.0.0"),
        ("pep440", "minor+dev", "0.1.0.dev0"),
        ("pep440", "micro+alpha+dev", "0.0.1a0.dev0"),
        ("pep440", "1.1.1", "1.1.1"),
    ],
)
def test_bump_with_semver_on_new_repo(
    repo: GitRepo,
    versioning: Literal["pep440", "semver"],
    bump: str,
    expected: str,
) -> None:
    """Bump to user specified version on new Git repo.

    Parameters:
        repo: GitRepo to a temporary repository.
        bump: The bump parameter value.
        expected: Expected version for the new changelog entry.
    """
    changelog = Changelog(repo.path, convention=AngularConvention, bump=bump, versioning=versioning, zerover=False)
    assert len(changelog.versions_list) == 1
    assert changelog.versions_list[0].planned_tag == expected


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
    assert expected_tag in (version.tag, version.planned_tag)
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
        expected_tag="",
        expected_prev_tag=None,
        expected_commits=[commit_e, commit_c, commit_d, commit_a, commit_b],
    )


def test_build_changelog_with_pep440_versions(repo: GitRepo) -> None:
    """Test parsing and grouping commits to PEP440 versions.

    Parameters:
        repo: GitRepo to a temporary repository.
    """
    repo.commit("feat: Feature")
    repo.tag("1.0.0")
    repo.commit("fix: Fix")
    repo.tag("1.0.0.post0")
    repo.commit("feat: Feat")
    changelog = Changelog(repo.path, convention=AngularConvention, versioning="pep440")
    assert len(changelog.versions_list) == 3
    assert changelog.versions_list[1].tag == "1.0.0.post0"


def test_ignore_nonsemver_tag(repo: GitRepo) -> None:
    """Test parsing and grouping commits to versions.

    Commit graph:
                 1.0.0
                   |
    main       A-B-C
                 |
               dummy

    Expected:
    - 1.0.0: C B A

    Parameters:
        repo: GitRepo to a temporary repository.
    """
    commit_a = repo.first_hash
    commit_b = repo.commit("fix: B")
    repo.tag("dummy")
    commit_c = repo.commit("feat: C")
    repo.tag("1.0.0")

    changelog = Changelog(repo.path, convention=AngularConvention)

    assert len(changelog.versions_list) == 1
    _assert_version(
        changelog.versions_list[0],
        expected_tag="1.0.0",
        expected_prev_tag=None,
        expected_commits=[commit_c, commit_b, commit_a],
    )


def test_untyped_commits(repo: GitRepo) -> None:
    """Test capture of untyped (i.e. uncategorizable) commits.

    Parameters:
        repo: GitRepo to a temporary repository.
    """
    commit_a = repo.first_hash
    commit_b = repo.commit("this commit is untyped and therefore does not have a section!")
    repo.tag("1.0.0")
    changelog = Changelog(repo.path, convention=AngularConvention)
    assert len(changelog.versions_list) == 1
    (version,) = changelog.versions_list
    assert len(version.sections_list) == 2
    typed_sections = changelog.versions_dict[version.tag].typed_sections
    assert len(typed_sections) == 1
    untyped = changelog.versions_dict[version.tag].untyped_section
    assert untyped is not None
    (typed,) = typed_sections
    assert len(untyped.commits) == 1
    assert len(typed.commits) == 1
    (untyped_commit,) = untyped.commits
    (typed_commit,) = typed.commits
    assert untyped_commit.hash == commit_b
    assert typed_commit.hash == commit_a


def test_sections_all_expands_to_all_types(repo: GitRepo) -> None:
    """Test that :all: expands to all available section types for the convention.

    Parameters:
        repo: GitRepo to a temporary repository.
    """
    repo.tag("1.0.0")
    changelog = Changelog(repo.path, convention=AngularConvention, sections=[":all:"])

    # AngularConvention.TYPES contains all available section types
    expected_sections = list(AngularConvention.TYPES.values())
    assert changelog.sections == expected_sections


def test_sections_all_with_basic_convention(repo: GitRepo) -> None:
    """Test that :all: works with BasicConvention.

    Parameters:
        repo: GitRepo to a temporary repository.
    """
    repo.tag("1.0.0")
    changelog = Changelog(repo.path, convention=BasicConvention, sections=[":all:"])

    # BasicConvention.TYPES contains all available section types
    expected_sections = list(BasicConvention.TYPES.values())
    assert changelog.sections == expected_sections


def test_sections_explicit_list_still_works(repo: GitRepo) -> None:
    """Test that explicit section list still works as before.

    Parameters:
        repo: GitRepo to a temporary repository.
    """
    repo.tag("1.0.0")
    changelog = Changelog(repo.path, convention=AngularConvention, sections=["feat", "fix"])

    # Should map to full section names
    assert changelog.sections == ["Features", "Bug Fixes"]
