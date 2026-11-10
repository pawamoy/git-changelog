"""Tests for choosing the repository URL used in changelog links."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from git_changelog import Changelog, main, parse_settings

if TYPE_CHECKING:
    from pathlib import Path

    from tests.helpers import GitRepo


@pytest.fixture(autouse=True)
def _clear_remote_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GIT_CHANGELOG_REMOTE", raising=False)
    monkeypatch.delenv("GIT_CHANGELOG_REMOTE_URL", raising=False)


def test_named_remote(repo: GitRepo) -> None:
    """Use an explicitly selected remote rather than the fork's origin."""
    repo.git("remote", "add", "upstream", "git@github.com:upstream/project.git")
    assert Changelog(repo.path, remote="upstream").remote_url == "https://github.com/upstream/project"


def test_named_remote_overrides_environment(repo: GitRepo, monkeypatch: pytest.MonkeyPatch) -> None:
    """An explicit remote name takes precedence over the environment."""
    monkeypatch.setenv("GIT_CHANGELOG_REMOTE", "missing")
    assert Changelog(repo.path, remote="origin").remote_url == "https://github.com/example/example"


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://github.com/upstream/project.git", "https://github.com/upstream/project"),
        ("git@github.com:upstream/project.git", "https://github.com/upstream/project"),
        ("https://gitlab.com/group/subgroup/project.git", "https://gitlab.com/group/subgroup/project"),
        ("https://user:secret@example.org/group/project.git", "https://example.org/group/project"),
    ],
)
def test_url_override_normalization(repo: GitRepo, url: str, expected: str) -> None:
    """Normalize supplied URLs with the same rules as Git remote URLs."""
    assert Changelog(repo.path, remote_url=url).remote_url == expected


def test_environment_url_without_git_remote(repo: GitRepo, monkeypatch: pytest.MonkeyPatch) -> None:
    """A URL override also works in a clone with no configured remote."""
    repo.git("remote", "remove", "origin")
    monkeypatch.setenv("GIT_CHANGELOG_REMOTE_URL", "https://github.com/upstream/project.git")
    assert Changelog(repo.path).remote_url == "https://github.com/upstream/project"


def test_explicit_url_overrides_environment(repo: GitRepo, monkeypatch: pytest.MonkeyPatch) -> None:
    """Prefer the explicit URL over an environment URL and remote name."""
    monkeypatch.setenv("GIT_CHANGELOG_REMOTE_URL", "https://github.com/environment/project")
    monkeypatch.setenv("GIT_CHANGELOG_REMOTE", "missing")
    assert (
        Changelog(repo.path, remote="missing", remote_url="https://github.com/explicit/project").remote_url
        == "https://github.com/explicit/project"
    )


def test_legacy_remote_environment(repo: GitRepo, monkeypatch: pytest.MonkeyPatch) -> None:
    """Preserve the existing remote-name environment variable."""
    repo.git("remote", "add", "upstream", "https://github.com/upstream/project.git")
    monkeypatch.setenv("GIT_CHANGELOG_REMOTE", "upstream")
    assert Changelog(repo.path).remote_url == "https://github.com/upstream/project"


@pytest.mark.parametrize("key", ["remote", "remote_url"])
def test_remote_configuration_and_cli_precedence(tmp_path: Path, key: str) -> None:
    """Read remote settings from TOML and allow command-line overrides."""
    config = tmp_path / "settings.toml"
    config.write_text(f'{key} = "configured"\n', encoding="utf8")
    assert parse_settings(["--config-file", str(config)])[key] == "configured"
    assert parse_settings(["--config-file", str(config), "--" + key.replace("_", "-"), "cli"])[key] == "cli"


@pytest.mark.parametrize("source", ["url", "name", "config", "environment"])
def test_cli_renders_links_using_override(
    repo: GitRepo, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, source: str
) -> None:
    """The CLI uses the supplied URL without modifying Git configuration."""
    output = tmp_path / "changelog.md"
    url = "https://github.com/upstream/project.git"
    config = tmp_path / "settings.toml"
    options = []
    if source == "url":
        options = ["--remote-url", url]
    elif source == "name":
        repo.git("remote", "add", "upstream", url)
        options = ["--remote", "upstream"]
    elif source == "config":
        config.write_text(f'remote_url = "{url}"\n', encoding="utf8")
    else:
        monkeypatch.setenv("GIT_CHANGELOG_REMOTE_URL", url)
    assert (
        main(
            [
                str(repo.path),
                "--config-file",
                str(config),
                *options,
                "--include-all",
                "--output",
                str(output),
            ]
        )
        == 0
    )
    rendered = output.read_text(encoding="utf8")
    assert "https://github.com/upstream/project/commit/" in rendered
    assert "https://github.com/example/example" not in rendered
    assert repo.git("config", "--get", "remote.origin.url").strip() == "git@github.com:example/example"
