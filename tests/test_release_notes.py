"""Tests for the release notes feature."""

from __future__ import annotations

from typing import TYPE_CHECKING

from git_changelog import get_release_notes

if TYPE_CHECKING:
    from pathlib import Path


def test_getting_release_notes(tmp_path: Path) -> None:
    """Get release notes from existing changelog.

    Parameters:
        tmp_path: Temporary directory (pytest fixture).
    """
    changelog_lines = [
        "# Changelog",
        "Header.",
        "<!-- insertion marker -->",
        "## [2.0.0](https://example.com)",
        "Contents 2.0.",
        "<!-- insertion marker -->",
        "## [1.0.0](https://example.com)",
        "Contents 1.0",
    ]
    changelog = tmp_path.joinpath("changelog.md")
    changelog.write_text("\n\n".join(changelog_lines))
    expected = "\n\n".join(changelog_lines[3:5])
    assert get_release_notes(input_file=changelog) == expected
