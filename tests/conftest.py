"""Configuration for the pytest test suite."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from git_changelog.commit import AngularConvention
from tests.helpers import GitRepo

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture(name="repo")
def git_repo(tmp_path: Path, request: pytest.FixtureRequest) -> GitRepo:
    """Pytest fixture setting up a temporary Git repository.

    Parameters:
        tmp_path: Path to a temporary directory (pytest fixture).

    Yields:
        A Git repository wrapper instance.
    """
    repo = GitRepo(tmp_path)
    versions = getattr(request, "param", [])
    for version in versions:
        for section in AngularConvention.TYPES:
            repo.commit(f"{section}: Summary.")
        if version:
            repo.git("tag", version)
    return repo
