"""Test providers references parsing."""

from __future__ import annotations

import git_changelog

text = """
This is the subject #1

This is the body. Related: #2. Also mentions #3 and #4.
Closes #5. closed #6, #7. FIX: #89 and #10.
Resolve        #1111.
Also support other projects references like shellm-org/shellm-data#19!!
Or fix pawamoy/git-changelog#1.
Don't match this one: #01.

Now some other references:

A merge request: !153!
A mention: @hello
A commit git-changelog@06abf793
A longer commit 3879fabda896da89954adec8
A commit range: 00000000...11111111
A snippet: $45
Some labels: ~18, ~bug, ~"multi word label"
Some milestones: %2, %version1, %"awesome version"
A Bitbucket PR: Pull request #1
A Bitbucket issue: Issue #1
"""


def test_github_issue_parsing() -> None:
    """GitHub issues are correctly parsed."""  # (first word *is* correctly capitalized)
    github = git_changelog.GitHub("pawamoy", "git-changelog")
    for ref in github.REF:
        assert github.get_refs(ref, text)


def test_gitlab_issue_parsing() -> None:
    """GitLab issues are correctly parsed."""  # (first word *is* correctly capitalized)
    gitlab = git_changelog.GitLab("pawamoy", "git-changelog")
    for ref in gitlab.REF:
        assert gitlab.get_refs(ref, text)


def test_bitbucket_issue_parsing() -> None:
    """Bitbucket issues are correctly parsed."""
    bitbucket = git_changelog.Bitbucket("pawamoy", "git-changelog")
    for ref in bitbucket.REF:
        assert bitbucket.get_refs(ref, text)


def test_forgejo_issue_parsing() -> None:
    """Forgejo issues are correctly parsed."""
    forgejo = git_changelog.Forgejo("pawamoy", "git-changelog")
    for ref in forgejo.REF:
        assert forgejo.get_refs(ref, text)


def test_forgejo_urls() -> None:
    """Forgejo URLs are correctly built."""
    forgejo = git_changelog.Forgejo("pawamoy", "git-changelog")

    assert forgejo.build_ref_url("issues", {"ref": "15"}) == "https://codeberg.org/pawamoy/git-changelog/issues/15"
    assert (
        forgejo.build_ref_url("commits", {"ref": "abcdef12"})
        == "https://codeberg.org/pawamoy/git-changelog/commit/abcdef12"
    )
    assert forgejo.build_ref_url("mentions", {"ref": "foo"}) == "https://codeberg.org/foo"
    assert forgejo.get_tag_url(tag="v1.0.0") == "https://codeberg.org/pawamoy/git-changelog/src/tag/v1.0.0"
    assert (
        forgejo.get_compare_url(base="v1.0.0", target="v1.1.0")
        == "https://codeberg.org/pawamoy/git-changelog/compare/v1.0.0...v1.1.0"
    )
