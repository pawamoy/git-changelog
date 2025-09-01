"""End-to-end tests."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING
from urllib.parse import urlsplit, urlunsplit

import pytest

from git_changelog import AngularConvention, Changelog, build_and_render, bump_semver, get_template

if TYPE_CHECKING:
    from pathlib import Path

    from tests.helpers import GitRepo

VERSIONS = ("0.1.0", "0.2.0", "0.2.1", "1.0.0", "1.1.0", "")
VERSIONS_V = ("v0.1.0", "v0.2.0", "v0.2.1", "v1.0.0", "v1.1.0", "")
KEEP_A_CHANGELOG = get_template("keepachangelog")


@pytest.mark.parametrize("repo", [VERSIONS, VERSIONS_V], indirect=True)
def test_bumping_latest(repo: GitRepo) -> None:
    """Bump latest version.

    Parameters:
        repo: Temporary Git repository (fixture).
    """
    changelog = Changelog(repo.path, convention=AngularConvention, bump="auto")
    # Features, no breaking changes: minor bumped.
    assert changelog.versions_list[0].planned_tag is not None
    assert changelog.versions_list[0].planned_tag.lstrip("v") == bump_semver(
        VERSIONS[-2],
        "minor",
    )
    rendered = KEEP_A_CHANGELOG.render(changelog=changelog)
    assert "Unreleased" not in rendered


@pytest.mark.parametrize("repo", [VERSIONS, VERSIONS_V], indirect=True)
def test_not_bumping_latest(repo: GitRepo) -> None:
    """Don't bump latest version.

    Parameters:
        repo: Temporary Git repository (fixture).
    """
    changelog = Changelog(repo.path, convention=AngularConvention, bump=None)
    assert changelog.versions_list[0].planned_tag is None
    rendered = KEEP_A_CHANGELOG.render(changelog=changelog)
    assert "Unreleased" in rendered


@pytest.mark.parametrize("repo", [VERSIONS, VERSIONS_V], indirect=True)
def test_rendering_custom_sections(repo: GitRepo) -> None:
    """Render custom sections.

    Parameters:
        repo: Temporary Git repository (fixture).
    """
    changelog = Changelog(repo.path, convention=AngularConvention, sections=["feat"])
    rendered = KEEP_A_CHANGELOG.render(changelog=changelog)
    for section_type, section_title in AngularConvention.TYPES.items():
        if section_type != "feat":
            assert section_title not in rendered


@pytest.mark.parametrize("repo", [VERSIONS, VERSIONS_V], indirect=True)
def test_rendering_in_place(repo: GitRepo, tmp_path: Path) -> None:
    """Render changelog in-place.

    Parameters:
        repo: Temporary Git repository (fixture).
        tmp_path: A temporary path to write the changelog into.
    """
    output = tmp_path.joinpath("changelog.md")
    _, rendered = build_and_render(
        str(repo.path),
        convention="angular",
        bump=None,
        output=output.as_posix(),
        template="keepachangelog",
    )
    assert len(re.findall("<!-- insertion marker -->", rendered)) == 2
    assert "Unreleased" in rendered
    latest_tag = "91.6.14"
    assert latest_tag not in rendered
    repo.git("tag", latest_tag)
    build_and_render(
        str(repo.path),
        convention="angular",
        bump="auto",
        output=output.as_posix(),
        template="keepachangelog",
        in_place=True,
    )
    rendered = output.read_text()
    assert len(re.findall("<!-- insertion marker -->", rendered)) == 1
    assert "Unreleased" not in rendered
    assert latest_tag in rendered
    repo.git("tag", "-d", latest_tag)


@pytest.mark.parametrize("repo", [VERSIONS, VERSIONS_V], indirect=True)
def test_no_duplicate_rendering(repo: GitRepo, tmp_path: Path) -> None:
    """Render changelog in-place, and check for duplicate entries.

    Parameters:
        repo: Temporary Git repository (fixture).
        tmp_path: A temporary path to write the changelog into.
    """
    output = tmp_path.joinpath("changelog.md")
    _, rendered = build_and_render(
        str(repo.path),
        convention="angular",
        bump="auto",
        output=output.as_posix(),
        template="keepachangelog",
    )

    # With automatic bumping, there's only one insertion marker
    assert len(re.findall("<!-- insertion marker -->", rendered)) == 1
    latest_tag = "1.2.0"
    assert latest_tag in rendered

    rendered = output.read_text()
    # The latest tag should appear exactly three times in the changelog
    assert rendered.count(latest_tag) == 3

    # Without tagging a new version, we should get an error
    with pytest.raises(ValueError, match=r"Version .* already in changelog"):
        build_and_render(
            str(repo.path),
            convention="angular",
            bump="auto",
            output=output.as_posix(),
            template="keepachangelog",
            in_place=True,
        )

    rendered = output.read_text()
    # The latest tag should still appear exactly three times in the changelog
    assert rendered.count(latest_tag) == 3


@pytest.mark.parametrize("repo", [VERSIONS, VERSIONS_V], indirect=True)
def test_removing_credentials_from_remotes(repo: GitRepo) -> None:
    """Remove credentials from remotes.

    Parameters:
        repo: Temporary Git repository (fixture).
    """
    credentials = [
        "ghp_abcdefghijklmnOPQRSTUVWXYZ0123456789",
        "ghs_abcdefghijklmnOPQRSTUVWXYZ0123456789",
        "github_pat_abcdefgOPQRS0123456789_abcdefghijklmnOPQRSTUVWXYZ0123456789abcdefgOPQRS0123456789A",
        "user:password",
    ]
    for creds in credentials:
        repo.git("remote", "set-url", "origin", f"https://{creds}@github.com:example/example")
        changelog = Changelog(repo.path)
        assert creds not in changelog.remote_url
        assert urlunsplit(urlsplit(changelog.remote_url)) == changelog.remote_url


@pytest.mark.parametrize("repo", [VERSIONS, VERSIONS_V], indirect=True)
def test_filter_commits_option(repo: GitRepo) -> None:
    """Filter commit by revision-range argument.

    Parameters:
        repo: Temporary Git repository (fixture).
    """
    is_tag_with_v = repo.git("tag").split("\n")[0].startswith("v")

    range = "1.0.0.."
    expected = ["", "1.1.0"]
    if is_tag_with_v:
        range = "v1.0.0.."
        expected = ["", "v1.1.0"]

    changelog = Changelog(repo.path, filter_commits=range)
    taglist = [version.tag for version in changelog.versions_list]

    assert taglist == expected

    err_msg = "Maybe the provided git-log revision-range is not valid"
    with pytest.raises(ValueError, match=err_msg):
        changelog = Changelog(repo.path, filter_commits="invalid")
