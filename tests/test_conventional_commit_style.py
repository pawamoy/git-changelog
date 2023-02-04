"""Tests for the conventional commit convention."""

from git_changelog.commit import Commit, ConventionalCommitConvention


def test_conventional_convention_breaking_change():
    """Breaking change (singular) is correctly identified."""
    subject = "feat: this is a new breaking feature"
    body = ["BREAKING CHANGE: there is a breaking feature in this code"]
    commit = Commit(
        commit_hash="aaaaaaa", subject=subject, body=body, author_date="1574340645", committer_date="1574340645"
    )
    convention = ConventionalCommitConvention()
    commit_dict = convention.parse_commit(commit)
    assert commit_dict["type"] == "Features"
    assert commit_dict["scope"] is None
    assert commit_dict["is_major"]
    assert not commit_dict["is_minor"]
    assert not commit_dict["is_patch"]


def test_conventional_convention_breaking_changes():
    """Breaking changes (plural) are correctly identified."""
    subject = "feat: this is a new breaking feature"
    body = ["BREAKING CHANGES: there is a breaking feature in this code"]
    commit = Commit(
        commit_hash="aaaaaaa", subject=subject, body=body, author_date="1574340645", committer_date="1574340645"
    )
    convention = ConventionalCommitConvention()
    commit_dict = convention.parse_commit(commit)
    assert commit_dict["type"] == "Features"
    assert commit_dict["scope"] is None
    assert commit_dict["is_major"]
    assert not commit_dict["is_minor"]
    assert not commit_dict["is_patch"]


def test_conventional_convention_subject_breaking_change():  # noqa: WPS118
    """Breaking change in the subject (!) are correctly identified."""
    subject = "feat!: this is a new breaking feature"
    body = ["There is a breaking feature in this code"]
    commit = Commit(
        commit_hash="aaaaaaa", subject=subject, body=body, author_date="1574340645", committer_date="1574340645"
    )
    convention = ConventionalCommitConvention()
    commit_dict = convention.parse_commit(commit)
    assert commit_dict["type"] == "Features"
    assert commit_dict["scope"] is None
    assert commit_dict["is_major"]
    assert not commit_dict["is_minor"]
    assert not commit_dict["is_patch"]


def test_conventional_convention_subject_breaking_change_with_scope():  # noqa: WPS118
    """Breaking change in the subject (!) with scope are correctly identified."""
    subject = "feat(scope)!: this is a new breaking feature"
    body = ["There is a breaking feature in this code"]
    commit = Commit(
        commit_hash="aaaaaaa", subject=subject, body=body, author_date="1574340645", committer_date="1574340645"
    )
    convention = ConventionalCommitConvention()
    commit_dict = convention.parse_commit(commit)
    assert commit_dict["type"] == "Features"
    assert commit_dict["scope"] == "scope"
    assert commit_dict["is_major"]
    assert not commit_dict["is_minor"]
    assert not commit_dict["is_patch"]


def test_conventional_convention_feat():
    """Feature commit is correctly identified."""
    subject = "feat: this is a new feature"
    commit = Commit(commit_hash="aaaaaaa", subject=subject, author_date="1574340645", committer_date="1574340645")
    convention = ConventionalCommitConvention()
    commit_dict = convention.parse_commit(commit)
    assert commit_dict["type"] == "Features"
    assert commit_dict["scope"] is None
    assert not commit_dict["is_major"]
    assert commit_dict["is_minor"]
    assert not commit_dict["is_patch"]


def test_conventional_convention_feat_with_scope():
    """Feature commit is correctly identified."""
    subject = "feat(scope): this is a new feature"
    commit = Commit(commit_hash="aaaaaaa", subject=subject, author_date="1574340645", committer_date="1574340645")
    convention = ConventionalCommitConvention()
    commit_dict = convention.parse_commit(commit)
    assert commit_dict["type"] == "Features"
    assert commit_dict["scope"] == "scope"
    assert not commit_dict["is_major"]
    assert commit_dict["is_minor"]
    assert not commit_dict["is_patch"]


def test_conventional_convention_fix():
    """Bug fix commit is correctly identified."""
    subject = "fix: this is a bug fix"
    commit = Commit(commit_hash="aaaaaaa", subject=subject, author_date="1574340645", committer_date="1574340645")
    convention = ConventionalCommitConvention()
    commit_dict = convention.parse_commit(commit)
    assert commit_dict["type"] == "Bug Fixes"
    assert commit_dict["scope"] is None
    assert not commit_dict["is_major"]
    assert not commit_dict["is_minor"]
    assert commit_dict["is_patch"]


def test_conventional_convention_fix_with_scope():
    """Bug fix commit is correctly identified."""
    subject = "fix(scope): this is a bug fix"
    commit = Commit(commit_hash="aaaaaaa", subject=subject, author_date="1574340645", committer_date="1574340645")
    convention = ConventionalCommitConvention()
    commit_dict = convention.parse_commit(commit)
    assert commit_dict["type"] == "Bug Fixes"
    assert commit_dict["scope"] == "scope"
    assert not commit_dict["is_major"]
    assert not commit_dict["is_minor"]
    assert commit_dict["is_patch"]
