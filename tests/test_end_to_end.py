import random
import re
import shutil
import subprocess
from functools import partial

import pytest

from git_changelog import Changelog
from git_changelog.build import bump
from git_changelog.cli import build_and_render
from git_changelog.commit import AngularStyle
from git_changelog.templates import get_template

VERSIONS = ("0.1.0", "0.2.0", "0.2.1", "1.0.0", "1.1.0", "")
KEEP_A_CHANGELOG = get_template("keepachangelog")


def _git(*args) -> str:
    return subprocess.check_output([shutil.which("git") or "git", *args], text=True)


def _commit(repo, filename, section):
    with repo.joinpath(filename).open("a") as fh:
        fh.write(str(random.randint(0, 1)))
    _git("-C", repo, "add", "-A")
    _git("-C", repo, "commit", "-m", f"{section}: Commit with '{section}' type")


@pytest.fixture(scope="module")
def repo(tmp_path_factory):
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


def test_bumping_latest(repo):
    changelog = Changelog(repo, style=AngularStyle, bump_latest=True)
    # features, no breaking changes: minor bumped
    assert changelog.versions_list[0].planned_tag == bump(VERSIONS[-2], "minor")
    rendered = KEEP_A_CHANGELOG.render(changelog=changelog)
    assert "Unreleased" not in rendered


def test_not_bumping_latest(repo):
    changelog = Changelog(repo, style=AngularStyle, bump_latest=False)
    assert changelog.versions_list[0].planned_tag is None
    rendered = KEEP_A_CHANGELOG.render(changelog=changelog)
    assert "Unreleased" in rendered


def test_rendering_custom_sections(repo):
    changelog = Changelog(repo, style=AngularStyle, sections=["feat"])
    rendered = KEEP_A_CHANGELOG.render(changelog=changelog)
    for section_type, section_title in AngularStyle.TYPES.items():
        if section_type != "feat":
            assert section_title not in rendered


def test_rendering_in_place(repo):
    _, rendered = build_and_render(
        str(repo),
        style="angular",
        bump_latest=False,
        output=repo.joinpath("changelog.md").as_posix(),
        template="keepachangelog",
    )
    assert len(re.findall("<!-- insertion marker -->", rendered)) == 2
    assert "Unreleased" in rendered
    latest_tag = "91.6.14"
    assert latest_tag not in rendered
    _git("-C", repo, "tag", latest_tag)
    _, rendered = build_and_render(
        str(repo),
        style="angular",
        bump_latest=True,
        output=repo.joinpath("changelog.md").as_posix(),
        template="keepachangelog",
    )
    assert len(re.findall("<!-- insertion marker -->", rendered)) == 1
    assert "Unreleased" not in rendered
    assert latest_tag in rendered


# test in-place or not, builtin template
# test in-place or not, custom template
# test provider-refs and trailers parsing
