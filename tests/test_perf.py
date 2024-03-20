"""Tests for the `build` module."""

from __future__ import annotations

from cProfile import Profile
from pstats import SortKey, Stats
from typing import TYPE_CHECKING

from git_changelog import Changelog
from git_changelog.commit import AngularConvention

if TYPE_CHECKING:
    from tests.helpers import GitRepo


def _create_and_merge_branch(repo: GitRepo, branch: str = "feat") -> None:
    repo.branch(branch)
    repo.checkout(branch)
    repo.commit(f"feat: {branch}")
    repo.checkout("main")
    repo.merge(branch)
    repo.git("branch", "-d", branch)


def test_perf(repo: GitRepo) -> None:
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
    for _ in range(15):
        _create_and_merge_branch(repo)

    with Profile() as profile:
        Changelog(repo.path, convention=AngularConvention)
        with open("perf_stats.txt", "w") as f:
            Stats(profile, stream=f).strip_dirs().sort_stats(SortKey.TIME).print_stats()
