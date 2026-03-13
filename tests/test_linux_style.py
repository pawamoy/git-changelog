"""Tests for the basic commit convention."""

from __future__ import annotations

import pytest

from git_changelog import Commit, LinuxConvention


def test_linux_convention_breaking_change() -> None:
    """Breaking change (singular) is correctly identified."""
    subject = "foo: Added a new breaking feature"
    body = ["BREAKING CHANGE: there is a breaking feature in this code"]
    commit = Commit(
        commit_hash="aaaaaaa",
        subject=subject,
        body=body,
        author_date="1574340645",
        committer_date="1574340645",
    )
    convention = LinuxConvention()
    commit_dict = convention.parse_commit(commit)
    assert commit_dict["is_major"]
    assert not commit_dict["is_minor"]
    assert not commit_dict["is_patch"]


def test_linux_convention_breaking_changes() -> None:
    """Breaking changes (plural) are correctly identified."""
    subject = "bar: Added a new breaking feature"
    body = ["BREAKING CHANGES: there is a breaking feature in this code"]
    commit = Commit(
        commit_hash="aaaaaaa",
        subject=subject,
        body=body,
        author_date="1574340645",
        committer_date="1574340645",
    )
    convention = LinuxConvention()
    commit_dict = convention.parse_commit(commit)
    assert commit_dict["is_major"]
    assert not commit_dict["is_minor"]
    assert not commit_dict["is_patch"]


@pytest.mark.parametrize(
    ("subject", "expected_is_major", "expected_is_minor", "expected_is_patch", "expected_type"),
    [
        # Test all types
        ("baz: Added a new feature", False, True, False, "Added"),
        ("baz: Add a new feature", False, True, False, "Added"),
        ("baz: Fix a problem", False, False, True, "Fixed"),
        ("baz: Change implementation", False, False, True, "Changed"),
        ("baz: Remove config file", False, False, True, "Removed"),
        ("baz: Merge branch abc", False, False, True, "Merged"),
        ("baz: Document a new feature", False, False, True, "Documented"),
        ("foo: Implement new API endpoint", False, False, True, ""),
        # Missing space
        ("bar:Add support for new protocol", False, True, False, "Added"),
        # Without "scope:"
        ("Add support for new protocol", False, True, False, "Added"),
        ("Fix typo in documentation", False, False, True, "Fixed"),
        ("Implement new API endpoint", False, False, True, ""),
    ],
)
def test_linux_convention(
    subject: str,
    expected_is_major: bool,
    expected_is_minor: bool,
    expected_is_patch: bool,
    expected_type: str,
) -> None:
    """Commit messages are correctly identified."""
    commit = Commit(
        commit_hash="aaaaaaa",
        subject=subject,
        author_date="1574340645",
        committer_date="1574340645",
    )
    convention = LinuxConvention()
    commit_dict = convention.parse_commit(commit)
    assert commit_dict["is_major"] == expected_is_major
    assert commit_dict["is_minor"] == expected_is_minor
    assert commit_dict["is_patch"] == expected_is_patch
    assert commit_dict["type"] == expected_type
