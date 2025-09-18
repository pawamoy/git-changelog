"""Helpers for writing tests."""

from __future__ import annotations

import os
import random
import shutil
import subprocess
import uuid
from contextlib import contextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path


class GitRepo:
    """Test utility class to initalize and work with a Git repository."""

    _git_exec = shutil.which("git") or "git"

    def __init__(self, repo: Path) -> None:
        """Initialization the Git repository wrapper.

        Initializes a new Git repository under the given path.

        Parameters:
            repo: Path to the git repository.
        """
        self.path = repo
        self.path.mkdir(parents=True, exist_ok=True)
        self.git("init", "-b", "main")
        self.git("config", "user.name", "dummy")
        self.git("config", "user.email", "dummy@example.com")
        self.git("remote", "add", "origin", "git@github.com:example/example")
        self.first_hash = self.commit("chore: Initial repository creation")

    def git(self, *args: str) -> str:
        """Run a Git command in the repository.

        Parameters:
            *args: Arguments passed to the Git command.

        Returns:
            The output of the command.
        """
        return subprocess.check_output(  # noqa: S603
            [self._git_exec, "-C", str(self.path), *args],
            text=True,
        )

    def commit(self, message: str) -> str:
        """Create, add and commit a new file into the Git repository.

        Parameters:
            message: The commit message.

        Returns:
            The Git commit hash.
        """
        with self.path.joinpath(str(uuid.uuid4())).open("w", encoding="utf-8") as fh:
            fh.write(str(random.randint(0, 1)))  # noqa: S311
        self.git("add", "-A")
        self.git("commit", "-m", message)
        return self.git("rev-parse", "HEAD").rstrip()

    def tag(self, tagname: str) -> None:
        """Create a new tag in the GIt repository.

        Parameters:
            tagname: The name of the new tag.
        """
        self.git("tag", tagname)

    def branch(self, branchname: str) -> None:
        """Create a new branch in the Git repository.

        Parameters:
            branchname: The name of the new branch.
        """
        self.git("branch", branchname)

    def checkout(self, branchname: str) -> None:
        """Checkout a branch.

        Parameters:
            branchname: The name of the branch.
        """
        self.git("checkout", branchname)

    def merge(self, branchname: str) -> str:
        """Merge a branch into the current branch, creating a new merge commit.

        Parameters:
            branchname: The name of the branch to merge.

        Returns:
            The Git commit hash of the merge commit.
        """
        self.git("merge", "--no-ff", "--commit", "-m", f"merge: Merge branch '{branchname}'", branchname)
        return self.git("rev-parse", "HEAD").rstrip()

    @contextmanager
    def enter(self) -> Iterator[None]:
        """Context manager to enter the repository directory."""
        old_cwd = os.getcwd()
        os.chdir(self.path)
        try:
            yield
        finally:
            os.chdir(old_cwd)
