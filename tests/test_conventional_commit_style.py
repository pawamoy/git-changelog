"""Tests for the conventional commit convention."""

from __future__ import annotations

import pytest

from git_changelog import (
    Commit,
    ConventionalCommitConvention,
    ConventionalCommitConventionV0,
    ConventionalCommitConventionV1,
)


def test_conventional_convention_breaking_change() -> None:
    """Breaking change (singular) is correctly identified."""
    subject = "feat: this is a new breaking feature"
    body = ["BREAKING CHANGE: there is a breaking feature in this code"]
    commit = Commit(
        commit_hash="aaaaaaa",
        subject=subject,
        body=body,
        author_date="1574340645",
        committer_date="1574340645",
    )
    convention = ConventionalCommitConvention()
    commit_dict = convention.parse_commit(commit)
    assert commit_dict["type"] == "Features"
    assert commit_dict["scope"] is None
    assert commit_dict["is_major"]
    assert not commit_dict["is_minor"]
    assert not commit_dict["is_patch"]


def test_conventional_convention_breaking_changes() -> None:
    """Breaking changes (plural) are correctly identified."""
    subject = "feat: this is a new breaking feature"
    body = ["BREAKING CHANGES: there is a breaking feature in this code"]
    commit = Commit(
        commit_hash="aaaaaaa",
        subject=subject,
        body=body,
        author_date="1574340645",
        committer_date="1574340645",
    )
    convention = ConventionalCommitConvention()
    commit_dict = convention.parse_commit(commit)
    assert commit_dict["type"] == "Features"
    assert commit_dict["scope"] is None
    assert commit_dict["is_major"]
    assert not commit_dict["is_minor"]
    assert not commit_dict["is_patch"]


def test_conventional_convention_subject_breaking_change() -> None:
    """Breaking change in the subject (!) are correctly identified."""
    subject = "feat!: this is a new breaking feature"
    body = ["There is a breaking feature in this code"]
    commit = Commit(
        commit_hash="aaaaaaa",
        subject=subject,
        body=body,
        author_date="1574340645",
        committer_date="1574340645",
    )
    convention = ConventionalCommitConvention()
    commit_dict = convention.parse_commit(commit)
    assert commit_dict["type"] == "Features"
    assert commit_dict["scope"] is None
    assert commit_dict["is_major"]
    assert not commit_dict["is_minor"]
    assert not commit_dict["is_patch"]


def test_conventional_convention_subject_breaking_change_with_scope() -> None:
    """Breaking change in the subject (!) with scope are correctly identified."""
    subject = "feat(scope)!: this is a new breaking feature"
    body = ["There is a breaking feature in this code"]
    commit = Commit(
        commit_hash="aaaaaaa",
        subject=subject,
        body=body,
        author_date="1574340645",
        committer_date="1574340645",
    )
    convention = ConventionalCommitConvention()
    commit_dict = convention.parse_commit(commit)
    assert commit_dict["type"] == "Features"
    assert commit_dict["scope"] == "scope"
    assert commit_dict["is_major"]
    assert not commit_dict["is_minor"]
    assert not commit_dict["is_patch"]


def test_conventional_convention_feat() -> None:
    """Feature commit is correctly identified."""
    subject = "feat: this is a new feature"
    commit = Commit(
        commit_hash="aaaaaaa",
        subject=subject,
        author_date="1574340645",
        committer_date="1574340645",
    )
    convention = ConventionalCommitConvention()
    commit_dict = convention.parse_commit(commit)
    assert commit_dict["type"] == "Features"
    assert commit_dict["scope"] is None
    assert not commit_dict["is_major"]
    assert commit_dict["is_minor"]
    assert not commit_dict["is_patch"]


def test_conventional_convention_feat_with_scope() -> None:
    """Feature commit is correctly identified."""
    subject = "feat(scope): this is a new feature"
    commit = Commit(
        commit_hash="aaaaaaa",
        subject=subject,
        author_date="1574340645",
        committer_date="1574340645",
    )
    convention = ConventionalCommitConvention()
    commit_dict = convention.parse_commit(commit)
    assert commit_dict["type"] == "Features"
    assert commit_dict["scope"] == "scope"
    assert not commit_dict["is_major"]
    assert commit_dict["is_minor"]
    assert not commit_dict["is_patch"]


def test_conventional_convention_fix() -> None:
    """Bug fix commit is correctly identified."""
    subject = "fix: this is a bug fix"
    commit = Commit(
        commit_hash="aaaaaaa",
        subject=subject,
        author_date="1574340645",
        committer_date="1574340645",
    )
    convention = ConventionalCommitConvention()
    commit_dict = convention.parse_commit(commit)
    assert commit_dict["type"] == "Bug Fixes"
    assert commit_dict["scope"] is None
    assert not commit_dict["is_major"]
    assert not commit_dict["is_minor"]
    assert commit_dict["is_patch"]


def test_conventional_convention_fix_with_scope() -> None:
    """Bug fix commit is correctly identified."""
    subject = "fix(scope): this is a bug fix"
    commit = Commit(
        commit_hash="aaaaaaa",
        subject=subject,
        author_date="1574340645",
        committer_date="1574340645",
    )
    convention = ConventionalCommitConvention()
    commit_dict = convention.parse_commit(commit)
    assert commit_dict["type"] == "Bug Fixes"
    assert commit_dict["scope"] == "scope"
    assert not commit_dict["is_major"]
    assert not commit_dict["is_minor"]
    assert commit_dict["is_patch"]


def test_conventional_convention_alias() -> None:
    """The unversioned convention keeps the original class and bump behavior."""
    assert ConventionalCommitConvention is ConventionalCommitConventionV0

    # Build changes continue to warrant patch releases for existing callers.
    commit = Commit("aaaaaaa", subject="build: Drop support for Python 3.9")

    parsed = ConventionalCommitConvention().parse_commit(commit)

    assert parsed["type"] == "Build"
    assert parsed["is_patch"]


@pytest.mark.parametrize(
    ("subject", "expected_type", "expected_bump"),
    [
        ("fix: Correct a bug", "Bug Fixes", "patch"),
        ("FIX(parser): Correct a bug", "Bug Fixes", "patch"),
        ("feat: Add a feature", "Features", "minor"),
        ("FeAt(parser): Add a feature", "Features", "minor"),
        ("fix!: Remove an API", "Bug Fixes", "major"),
        ("FEAT(parser)!: Remove an API", "Features", "major"),
        ("ci: Speed up CI", "Continuous Integration", None),
        ("chore: Clean up files", "Chore", None),
        ("build: Update dependencies", "Build", None),
        ("docs: Update the guide", "Docs", None),
        ("perf: Speed up parsing", "Performance Improvements", None),
        ("refactor: Simplify parsing", "Code Refactoring", None),
        ("revert: Undo a commit", "Reverts", None),
        ("style: Adjust whitespace", "Style", None),
        ("test: Add tests", "Tests", None),
        ("custom: Update something", "custom", None),
        ("CUSTOM(parser)!: Remove an API", "custom", "major"),
        ("not a conventional commit", "", None),
        ("fix:Missing space", "", None),
        ("feat:", "", None),
        ("feat: ", "", None),
    ],
)
def test_conventional_v1_commit_types(subject: str, expected_type: str, expected_bump: str | None) -> None:
    """V1 selects bumps by type, accepts custom types, and ignores invalid subjects."""
    commit = Commit("aaaaaaa", subject=subject)

    parsed = ConventionalCommitConventionV1().parse_commit(commit)

    assert parsed["type"] == expected_type
    assert parsed["is_major"] == (expected_bump == "major")
    assert parsed["is_minor"] == (expected_bump == "minor")
    assert parsed["is_patch"] == (expected_bump == "patch")


def test_conventional_v1_preserves_scope_and_description() -> None:
    """Case-insensitive type matching preserves the displayed scope and description."""
    commit = Commit("aaaaaaa", subject="FiX(MyAPI): Keep This Description")

    parsed = ConventionalCommitConventionV1().parse_commit(commit)

    assert parsed["type"] == "Bug Fixes"
    assert parsed["scope"] == "MyAPI"
    assert parsed["subject"] == "Keep This Description"


@pytest.mark.parametrize("parse_trailers", [False, True])
@pytest.mark.parametrize(
    ("body", "expected_major"),
    [
        (["BREAKING CHANGE: Remove an API"], True),
        (["BREAKING-CHANGE: Remove an API"], True),
        (["Explain the change.", "", "BREAKING CHANGE: Remove an API"], True),
        (["Reviewed-by: Someone", "BREAKING-CHANGE: Remove an API"], True),
        (["Refs #123", "BREAKING CHANGE: Remove an API"], True),
        (["Reviewed-by: Someone", "continued value", "BREAKING CHANGE: Remove an API"], True),
        (["BREAKING CHANGE: Remove an API", "continued description", "Refs #123"], True),
        (["breaking change: Remove an API"], False),
        (["breaking-change: Remove an API"], False),
        (["BREAKING CHANGES: Remove an API"], False),
        (["BREAKING CHANGE Remove an API"], False),
        (["BREAKING CHANGE:Remove an API"], False),
        (["BREAKING CHANGE: "], False),
        (["This mentions BREAKING CHANGE: in prose."], False),
        (["An ordinary body paragraph.", "BREAKING CHANGE: Still in the body"], False),
    ],
)
def test_conventional_v1_breaking_footers(body: list[str], expected_major: bool, parse_trailers: bool) -> None:
    """Only valid uppercase footers mark a change as breaking, regardless of trailer parsing."""
    commit = Commit("aaaaaaa", subject="custom: Update behavior", body=body, parse_trailers=parse_trailers)

    parsed = ConventionalCommitConventionV1().parse_commit(commit)

    assert parsed["is_major"] == expected_major
    assert not parsed["is_minor"]
    assert not parsed["is_patch"]


@pytest.mark.parametrize("subject", ["fix: Correct a bug", "feat: Add a feature", "docs: Update the guide"])
def test_conventional_v1_breaking_footer_takes_precedence(subject: str) -> None:
    """A breaking footer overrides the bump associated with any valid type."""
    commit = Commit("aaaaaaa", subject=subject, body=["BREAKING CHANGE: Remove an API"])

    parsed = ConventionalCommitConventionV1().parse_commit(commit)

    assert parsed["is_major"]
    assert not parsed["is_minor"]
    assert not parsed["is_patch"]
