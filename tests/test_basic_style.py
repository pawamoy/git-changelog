"""Tests for the basic commit convention."""

from __future__ import annotations

from git_changelog import BasicConvention, Commit


def test_basic_convention_breaking_change() -> None:
    """Breaking change (singular) is correctly identified."""
    subject = "Added a new breaking feature"
    body = ["BREAKING CHANGE: there is a breaking feature in this code"]
    commit = Commit(
        commit_hash="aaaaaaa",
        subject=subject,
        body=body,
        author_date="1574340645",
        committer_date="1574340645",
    )
    convention = BasicConvention()
    commit_dict = convention.parse_commit(commit)
    assert commit_dict["is_major"]
    assert not commit_dict["is_minor"]
    assert not commit_dict["is_patch"]


def test_basic_convention_breaking_changes() -> None:
    """Breaking changes (plural) are correctly identified."""
    subject = "Added a new breaking feature"
    body = ["BREAKING CHANGES: there is a breaking feature in this code"]
    commit = Commit(
        commit_hash="aaaaaaa",
        subject=subject,
        body=body,
        author_date="1574340645",
        committer_date="1574340645",
    )
    convention = BasicConvention()
    commit_dict = convention.parse_commit(commit)
    assert commit_dict["is_major"]
    assert not commit_dict["is_minor"]
    assert not commit_dict["is_patch"]


def test_basic_convention_feat() -> None:
    """Feature commit is correctly identified."""
    subject = "Added a new feature"
    commit = Commit(
        commit_hash="aaaaaaa",
        subject=subject,
        author_date="1574340645",
        committer_date="1574340645",
    )
    convention = BasicConvention()
    commit_dict = convention.parse_commit(commit)
    assert not commit_dict["is_major"]
    assert commit_dict["is_minor"]
    assert not commit_dict["is_patch"]


def test_basic_convention_fix() -> None:
    """Bug fix commit is correctly identified."""
    subject = "Fixed a bug"
    commit = Commit(
        commit_hash="aaaaaaa",
        subject=subject,
        author_date="1574340645",
        committer_date="1574340645",
    )
    convention = BasicConvention()
    commit_dict = convention.parse_commit(commit)
    assert not commit_dict["is_major"]
    assert not commit_dict["is_minor"]
    assert commit_dict["is_patch"]
