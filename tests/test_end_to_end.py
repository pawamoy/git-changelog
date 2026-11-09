"""End-to-end tests."""

from __future__ import annotations

import re
from functools import partial
from typing import TYPE_CHECKING
from urllib.parse import urlsplit, urlunsplit

import pytest

from git_changelog import AngularConvention, Changelog, build_and_render, bump_semver, get_template

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Literal

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
    assert rendered.endswith("\n"), "file end with empty line"
    assert not rendered.endswith("\n\n"), "file end with a single empty line"
    assert len(re.findall("\n<!-- insertion marker -->\n", rendered)) == 2
    assert "<!-- insertion marker -->\n## Unreleased\n" in rendered
    assert "<!-- insertion marker -->\n## [" in rendered, "no empty line between marker and release"
    assert len(re.findall("\n\n## \\[", rendered)) == 4, "empty line before each release"
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
    rendered = output.read_text(encoding="utf8")
    assert rendered.endswith("\n"), "file end with empty line"
    assert not rendered.endswith("\n\n"), "file end with a single empty line"
    assert len(re.findall("\n<!-- insertion marker -->\n", rendered)) == 1
    assert "\n## Unreleased\n" not in rendered
    assert latest_tag in rendered
    repo.git("tag", "-d", latest_tag)


@pytest.mark.parametrize("repo", [VERSIONS, VERSIONS_V], indirect=True)
def test_rendering_in_place_missing_file(repo: GitRepo, tmp_path: Path) -> None:
    """Render changelog in-place into a file that doesn't exist yet.

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
        in_place=True,
    )
    assert output.exists()
    assert rendered == output.read_text(encoding="utf8")
    # The full changelog was rendered, header and insertion marker included.
    assert rendered.startswith("# Changelog")
    assert len(re.findall("<!-- insertion marker -->", rendered)) == 2


@pytest.mark.parametrize("repo", [VERSIONS, VERSIONS_V], indirect=True)
def test_rendering_debian_prepend(repo: GitRepo, tmp_path: Path) -> None:
    """Render changelog in-place.

    Parameters:
        repo: Temporary Git repository (fixture).
        tmp_path: A temporary path to write the changelog into.
    """
    output = tmp_path.joinpath("changelog")
    _, rendered = build_and_render(
        str(repo.path),
        convention="angular",
        bump=None,
        output=output.as_posix(),
        template="debian",
        jinja_context={
            "debian_package_name": "my-pkg-name",
            "debian_version_suffix": "+dfsg-1",
        },
    )
    assert re.match(r"my-pkg-name \(1.1.0\+\d+\+dfsg-1\) UNRELEASED; urgency=medium\n\n", rendered)
    assert re.findall(r"\n\nmy-pkg-name", rendered), "empty line between each release"
    assert rendered.endswith("\n"), "file end with empty line"
    assert not rendered.endswith("\n\n"), "file end with a single empty line"

    latest_tag = "91.6.14"
    assert latest_tag not in rendered
    repo.git("tag", latest_tag)
    build_and_render(
        str(repo.path),
        convention="angular",
        bump="auto",
        output=output.as_posix(),
        template="debian",
        in_place=True,
        jinja_context={
            "debian_package_name": "my-pkg-name",
            "debian_version_suffix": "+dfsg-2",
        },
    )
    rendered = output.read_text(encoding="utf8")
    assert rendered.endswith("\n"), "file end with empty line"
    assert not rendered.endswith("\n\n"), "file end with a single empty line"
    assert "UNRELEASED" not in rendered
    assert re.match(r"my-pkg-name \(91.6.14\+dfsg-2\) unstable; urgency=medium\n\n", rendered)
    assert latest_tag in rendered
    repo.git("tag", "-d", latest_tag)


@pytest.mark.parametrize("repo", [("",)], indirect=True)
def test_rendering_debian_no_previous_version(repo: GitRepo, tmp_path: Path) -> None:
    """Render changelog in-place.

    Parameters:
        repo: Temporary Git repository (fixture).
        tmp_path: A temporary path to write the changelog into.
    """
    output = tmp_path.joinpath("changelog")
    _, rendered = build_and_render(
        str(repo.path),
        convention="angular",
        bump=None,
        output=output.as_posix(),
        template="debian",
        jinja_context={
            "debian_package_name": "my-pkg-name",
            "debian_version_suffix": "+dfsg-1",
        },
    )
    assert re.match(r"my-pkg-name \(0.0.0\+\d+\+dfsg-1\) UNRELEASED;", rendered)


@pytest.mark.parametrize("repo", [VERSIONS, VERSIONS_V], indirect=True)
def test_rendering_rpmbuild_prepend(repo: GitRepo, tmp_path: Path) -> None:
    """Render changelog in-place.

    Parameters:
        repo: Temporary Git repository (fixture).
        tmp_path: A temporary path to write the changelog into.
    """
    output = tmp_path.joinpath("changelog")
    _, rendered = build_and_render(
        str(repo.path),
        convention="angular",
        bump=None,
        output=output.as_posix(),
        template="rpmbuild",
        jinja_context={
            "rpm_release": "1",
        },
    )
    assert rendered.endswith("\n"), "file end with empty line"
    assert not rendered.endswith("\n\n"), "file end with a single empty line"
    assert re.match(r"\* .* dummy <dummy@example.com> - 1.1.0\+\d+-1\n", rendered)
    latest_tag = "91.6.14"
    assert latest_tag not in rendered
    repo.git("tag", latest_tag)
    build_and_render(
        str(repo.path),
        convention="angular",
        bump="auto",
        output=output.as_posix(),
        template="rpmbuild",
        in_place=True,
        jinja_context={
            "rpm_release": "2",
        },
    )
    rendered = output.read_text(encoding="utf8")
    assert rendered.endswith("\n"), "file end with empty line"
    assert not rendered.endswith("\n\n"), "file end with a single empty line"
    assert re.match(r"\* .* dummy <dummy@example.com> - 91.6.14-2\n", rendered)
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

    rendered = output.read_text(encoding="utf8")
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

    rendered = output.read_text(encoding="utf8")
    # The latest tag should still appear exactly three times in the changelog
    assert rendered.count(latest_tag) == 3


@pytest.mark.parametrize("template", ["debian", "rpmbuild"])
@pytest.mark.parametrize("prefix", ["", "v"])
@pytest.mark.parametrize("versioning", ["semver", "pep440"])
def test_prepend_without_duplicate_releases(
    repo: GitRepo, tmp_path: Path, template: str, prefix: str, versioning: Literal["semver", "pep440"]
) -> None:
    """Match existing releases when the template removes the tag prefix."""
    # Record a tagged release using a template that omits the v prefix.
    repo.commit("feat: First feature")
    repo.tag(f"{prefix}1.0.0")
    output = tmp_path / "changelog"
    render = partial(
        build_and_render,
        str(repo.path),
        template=template,
        convention="angular",
        output=str(output),
        versioning=versioning,
    )
    render(in_place=True)

    # Add a release without regenerating the already documented feature.
    repo.commit("fix: Second feature")
    render(bump=f"{prefix}1.0.1", in_place=True)

    rendered = output.read_text(encoding="utf8")
    assert rendered.count("feat: First feature") == 1
    assert rendered.count("fix: Second feature") == 1


@pytest.mark.parametrize("prefix", ["", "v"])
@pytest.mark.parametrize("versioning", ["semver", "pep440"])
def test_prepend_debian_revision(
    repo: GitRepo, tmp_path: Path, prefix: str, versioning: Literal["semver", "pep440"]
) -> None:
    """Match a complete Debian version extracted with a custom regex."""
    repo.commit("feat: First feature")
    repo.tag(f"{prefix}2.2.6-13")
    output = tmp_path / "changelog"
    render = partial(
        build_and_render,
        str(repo.path),
        template="debian",
        convention="angular",
        output=str(output),
        versioning=versioning,
    )
    render(in_place=True)

    # The regex includes the Debian revision, as in issue #140.
    repo.commit("fix: Second feature")
    render(
        bump=f"{prefix}2.2.7-1",
        in_place=True,
        version_regex=r"^[\w.+-]+ \((?P<version>[^)\s]+)\)(?!.*UNRELEASED)",
    )

    rendered = output.read_text(encoding="utf8")
    assert rendered.count("debian-package-name (2.2.6-13)") == 1
    assert rendered.count("debian-package-name (2.2.7-1)") == 1
    assert rendered.count("feat: First feature") == 1
    assert rendered.count("fix: Second feature") == 1


@pytest.mark.parametrize("template", ["debian", "rpmbuild"])
@pytest.mark.parametrize("versioning", ["semver", "pep440"])
@pytest.mark.parametrize("tagged", [False, True])
def test_prepend_already_documented_version(
    repo: GitRepo, tmp_path: Path, template: str, versioning: Literal["semver", "pep440"], tagged: bool
) -> None:
    """Reject an already documented tag or planned tag despite a missing prefix."""
    repo.commit("feat: Already documented")
    if tagged:
        repo.tag("v1.0.0")
    output = tmp_path / "changelog"
    render = partial(
        build_and_render,
        str(repo.path),
        template=template,
        convention="angular",
        output=str(output),
        versioning=versioning,
        bump=None if tagged else "v1.0.0",
    )
    render()
    original = output.read_text(encoding="utf8")

    # Both an existing tag and a planned tag must match the prefixless version.
    with pytest.raises(ValueError, match=r"Version 1\.0\.0 already in changelog"):
        render(in_place=True)

    assert output.read_text(encoding="utf8") == original


@pytest.mark.parametrize("tagged", [False, True])
def test_in_place_distinct_semver_builds(repo: GitRepo, tmp_path: Path, tagged: bool) -> None:
    """Keep distinct builds when matching existing and planned releases."""
    # A custom template preserves build metadata while removing the tag prefix.
    template = tmp_path / "template.jinja"
    template.write_text(
        "{% if not in_place %}# Changelog\n\n{% endif %}<!-- insertion marker -->\n"
        "{% for version in changelog.versions_list %}"
        "## [{{ (version.tag or version.planned_tag).lstrip('v') }}]\n"
        "{% for commit in version.commits %}- {{ commit.subject }}\n{% endfor %}"
        "{% endfor %}",
        encoding="utf8",
    )
    repo.commit("feat: First build")
    repo.tag("v1.0.0+build1")
    output = tmp_path / "changelog"
    render = partial(
        build_and_render, str(repo.path), template=f"path:{template}", convention="angular", output=str(output)
    )
    render()

    # Exercise the release boundary with a tag, and the duplicate guard with a planned tag.
    repo.commit("fix: Second build")
    if tagged:
        repo.tag("v1.0.0+build2")
        repo.commit("fix: Next release")
    render(bump="v1.0.1" if tagged else "v1.0.0+build2", in_place=True)

    rendered = output.read_text(encoding="utf8")
    assert rendered.count("## [1.0.0+build1]") == 1
    assert rendered.count("## [1.0.0+build2]") == 1
    assert rendered.count("feat: First build") == 1
    assert rendered.count("fix: Second build") == 1
    if tagged:
        assert rendered.count("## [1.0.1]") == 1
        assert rendered.count("fix: Next release") == 1


@pytest.mark.parametrize("bump", ["v1.0RC1", "v1.0rc2"])
def test_in_place_normalized_pep440_version(repo: GitRepo, tmp_path: Path, bump: str) -> None:
    """Match equivalent PEP 440 spellings when detecting existing releases."""
    repo.commit("feat: First feature")
    repo.tag("v1.0RC1")
    repo.commit("fix: Second feature")
    output = tmp_path / "changelog"
    original = "# Changelog\n\n<!-- insertion marker -->\n## [1.0rc1]\n\n- feat: First feature\n"
    output.write_text(original, encoding="utf8")

    # The changelog uses the normalized spelling of the prerelease tag.
    render = partial(
        build_and_render,
        str(repo.path),
        template="keepachangelog",
        convention="angular",
        output=str(output),
        versioning="pep440",
        bump=bump,
        in_place=True,
    )
    if bump == "v1.0RC1":
        with pytest.raises(ValueError, match=r"Version 1\.0rc1 already in changelog"):
            render()
        assert output.read_text(encoding="utf8") == original
    else:
        render()

        rendered = output.read_text(encoding="utf8")
        assert rendered.count("First feature") == 1
        assert rendered.count("Second feature") == 1


@pytest.mark.parametrize("versioning", ["semver", "pep440"])
def test_prepend_unparseable_version(repo: GitRepo, tmp_path: Path, versioning: Literal["semver", "pep440"]) -> None:
    """Keep rendering when the changelog version does not follow the selected scheme."""
    repo.commit("feat: First feature")
    repo.tag("v1.0.0")
    repo.commit("fix: Second feature")
    output = tmp_path / "changelog"
    legacy_entry = "debian-package-name (legacy) unstable; urgency=medium\n\n  * Legacy release\n"
    output.write_text(legacy_entry, encoding="utf8")

    # An unmatched legacy version previously allowed all releases to be prepended.
    build_and_render(
        str(repo.path),
        template="debian",
        convention="angular",
        output=str(output),
        versioning=versioning,
        bump="v1.0.1",
        in_place=True,
    )

    rendered = output.read_text(encoding="utf8")
    assert rendered.endswith(legacy_entry)
    assert rendered.count("feat: First feature") == 1
    assert rendered.count("fix: Second feature") == 1


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
