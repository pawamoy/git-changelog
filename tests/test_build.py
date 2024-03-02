"""Tests for the `build` module."""

from __future__ import annotations

import random
import shutil
import subprocess
import uuid
from typing import TYPE_CHECKING

import pytest

from git_changelog import Changelog
from git_changelog.commit import AngularConvention

if TYPE_CHECKING:
    from pathlib import Path


class GitRepo:
    """Test utility class to initalize and work with a git repository."""

    def __init__(self, repo: Path) -> None:
        """Initialization method.

        Initializes a new git repository under the given path.

        Arguments:
            repo: Path to the git repository.
        """
        self.path = repo
        self._git("init")
        self._git("config", "user.name", "dummy")
        self._git("config", "user.email", "dummy@example.com")
        self._git("remote", "add", "origin", "git@github.com:example/example")
        self.commit("chore: Initial repository creation")

    def commit(self, message: str) -> str:
        """Create, add and commit a new file into the git repository.

        Parameters:
            message: The commit message.

        Returns:
            The git commit hash.
        """
        with self.path.joinpath(str(uuid.uuid4())).open("a") as fh:
            fh.write(str(random.randint(0, 1)))  # noqa: S311
        self._git("add", "-A")
        self._git("commit", "-m", message)
        return self._git("rev-parse", "HEAD")

    def _git(self, *args: str) -> str:
        return subprocess.check_output(
            [shutil.which("git") or "git", "-C", str(self.path), *args],  # noqa: S603
            text=True,
        )


@pytest.fixture(name="repo")
def git_repo(tmp_path: Path) -> GitRepo:
    """Pytest fixture setting up a temporary Git repository.

    Parameters:
        tmp_path: Path to a temporary directory (pytest fixture).

    Yields:
        A Git repository wrapper instance.
    """
    return GitRepo(tmp_path)


@pytest.mark.parametrize(
    ("bump", "expected"),
    [("auto", "0.1.0"), ("major", "0.1.0"), ("minor", "0.1.0"), ("1.1.1", "1.1.1")],
)
def test_bump_with_semver_on_new_repo(repo: GitRepo, bump: str, expected: str) -> None:
    """Bump to user specified version (semver) on new git repo.

    Parameters:
        repo: GitRepo to a temporary repository.
    """
    changelog = Changelog(repo.path, convention=AngularConvention, bump=bump)

    assert len(changelog.versions_list) == 1
    tag = changelog.versions_list[0].tag
    assert tag == expected
