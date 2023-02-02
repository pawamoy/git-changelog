"""End-to-end tests."""

import random
import re
import shutil
import subprocess  # noqa: S404
from functools import partial
from pathlib import Path
from typing import Iterator

import pytest

from git_changelog import Changelog
from git_changelog.build import bump
from git_changelog.cli import build_and_render
from git_changelog.commit import AngularStyle
from git_changelog.templates import get_template

VERSIONS = ("0.1.0", "0.2.0", "0.2.1", "1.0.0", "1.1.0", "")
KEEP_A_CHANGELOG = get_template("keepachangelog")


def _git(*args) -> str:
    return subprocess.check_output([shutil.which("git") or "git", *args], text=True)  # noqa: S603


def _commit(repo, filename, section):
    with repo.joinpath(filename).open("a") as fh:
        fh.write(str(random.randint(0, 1)))  # noqa: S311
    _git("-C", repo, "add", "-A")
    _git("-C", repo, "commit", "-m", f"{section}: Commit with '{section}' type")


@pytest.fixture(scope="module", name="repo")
def git_repo(tmp_path_factory) -> Iterator[Path]:
    """Pytest fixture setting up a temporary Git repository.

    Parameters:
        tmp_path_factory: Utility to create temporary directories.

    Yields:
        The path to a temporary Git repository.
    """
    tmp_path = tmp_path_factory.mktemp("git_changelog")
    git = partial(_git, "-C", str(tmp_path))
    commit = partial(_commit, tmp_path, "dummy")
    git("init")
    git("config", "user.name", "dummy")
    git("config", "user.email", "dummy@example.com")
    git("remote", "add", "origin", "git@github.com:example/example")
    for version in VERSIONS:
        for section in AngularStyle.TYPES.keys():
            commit(section)
            commit(section)
        if version:
            git("tag", version)
    yield tmp_path
    shutil.rmtree(tmp_path)

def test_rendering_custom_sections(repo):
    """Render custom sections.

    Parameters:
        repo: Path to a temporary repository.
    """
    changelog = Changelog(repo, style=AngularStyle, sections=["feat"])
    rendered = KEEP_A_CHANGELOG.render(changelog=changelog)
    for section_type, section_title in AngularStyle.TYPES.items():
        if section_type != "feat":
            assert section_title not in rendered

