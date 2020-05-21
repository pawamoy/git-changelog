"""Tests for the basic commit style."""

from git_changelog.commit import BasicStyle, Commit


def test_basic_style_breaking_change():
    """Breaking change (singular) is correctly identified."""
    subject = "Added a new breaking feature"
    body = ["BREAKING CHANGE: there is a breaking feature in this code"]
    commit = Commit(sha="aaaaaaa", subject=subject, body=body, author_date="1574340645", committer_date="1574340645")
    style = BasicStyle()
    commit_dict = style.parse_commit(commit)
    assert commit_dict["is_major"]
    assert not commit_dict["is_minor"]
    assert not commit_dict["is_patch"]


def test_basic_style_breaking_changes():
    """Breaking changes (plural) are correctly identified."""
    subject = "Added a new breaking feature"
    body = ["BREAKING CHANGES: there is a breaking feature in this code"]
    commit = Commit(sha="aaaaaaa", subject=subject, body=body, author_date="1574340645", committer_date="1574340645")
    style = BasicStyle()
    commit_dict = style.parse_commit(commit)
    assert commit_dict["is_major"]
    assert not commit_dict["is_minor"]
    assert not commit_dict["is_patch"]


def test_basic_style_feat():
    """Feature commit is correctly identified."""
    subject = "Added a new feature"
    commit = Commit(sha="aaaaaaa", subject=subject, author_date="1574340645", committer_date="1574340645")
    style = BasicStyle()
    commit_dict = style.parse_commit(commit)
    assert not commit_dict["is_major"]
    assert commit_dict["is_minor"]
    assert not commit_dict["is_patch"]


def test_basic_style_fix():
    """Bug fix commit is correctly identified."""
    subject = "Fixed a bug"
    commit = Commit(sha="aaaaaaa", subject=subject, author_date="1574340645", committer_date="1574340645")
    style = BasicStyle()
    commit_dict = style.parse_commit(commit)
    assert not commit_dict["is_major"]
    assert not commit_dict["is_minor"]
    assert commit_dict["is_patch"]
