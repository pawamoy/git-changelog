# SPDX-License-Identifier: ISC
#
# ISC License
#
# Copyright (c) 2020, Timothée Mazzucotelli and contributors
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""Configuration for the pytest test suite."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from git_changelog._internal.commit import AngularConvention
from tests.helpers import GitRepo

if TYPE_CHECKING:
    from pathlib import Path

    from pytest_gitconfig import GitConfig


@pytest.fixture(name="gitconfig", scope="session")
def _default_gitconfig(default_gitconfig: GitConfig) -> GitConfig:
    default_gitconfig.set({"user.name": "dummy"})
    default_gitconfig.set({"user.email": "dummy@example.com"})
    return default_gitconfig


@pytest.fixture(name="repo")
def git_repo(tmp_path: Path, request: pytest.FixtureRequest, gitconfig: GitConfig) -> GitRepo:  # noqa: ARG001
    """Pytest fixture setting up a temporary Git repository.

    Parameters:
        tmp_path: Path to a temporary directory (pytest fixture).
        request: Pytest fixture request object.
        gitconfig: Git configuration fixture.

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
