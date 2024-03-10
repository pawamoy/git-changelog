"""Helpers for writing tests."""

from __future__ import annotations

import random
import shutil
import subprocess
import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


class GitRepo:
    """Test utility class to initalize and work with a Git repository."""

    def __init__(self, repo: Path) -> None:
        """Initialization the Git repository wrapper.

        Initializes a new Git repository under the given path.

        Parameters:
            repo: Path to the git repository.
        """
        self.path = repo
        self.git("init")
        self.git("config", "user.name", "dummy")
        self.git("config", "user.email", "dummy@example.com")
        self.git("remote", "add", "origin", "git@github.com:example/example")
        self.commit("chore: Initial repository creation")

    def git(self, *args: str) -> str:
        """Run a Git command in the repository.

        Parameters:
            *args: Arguments passed to the Git command.

        Returns:
            The output of the command.
        """
        return subprocess.check_output(
            [shutil.which("git") or "git", "-C", str(self.path), *args],  # noqa: S603
            text=True,
        )

    def commit(self, message: str) -> str:
        """Create, add and commit a new file into the Git repository.

        Parameters:
            message: The commit message.

        Returns:
            The Git commit hash.
        """
        with self.path.joinpath(str(uuid.uuid4())).open("w") as fh:
            fh.write(str(random.randint(0, 1)))  # noqa: S311
        self.git("add", "-A")
        self.git("commit", "-m", message)
        return self.git("rev-parse", "HEAD")

    def tag(self, tagname: str) -> None:
        """Create a new tag in the GIt repository.

        Parameters:
            tagname: The name of the new tag.
        """
        self.git("tag", tagname)
