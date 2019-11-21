from git_changelog.build import Commit
from git_changelog.style import AngularStyle


def test_angular_style_feat():
    subject = "feat: this is a new feature"
    commit = Commit("aaaaaaa", subject=subject, author_date="1574340645", committer_date="1574340645",)
    style = AngularStyle()
    commit_dict = style.parse_commit(commit)
    assert not commit_dict["is_major"]
    assert commit_dict["is_minor"]
    assert not commit_dict["is_patch"]


def test_angular_style_fix():
    subject = "fix: this is a bug fix"
    commit = Commit("aaaaaaa", subject=subject, author_date="1574340645", committer_date="1574340645",)
    style = AngularStyle()
    commit_dict = style.parse_commit(commit)
    assert not commit_dict["is_major"]
    assert not commit_dict["is_minor"]
    assert commit_dict["is_patch"]
