from git_changelog.commit import AngularStyle, Commit


def test_angular_style_breaking_change():
    subject = "feat: this is a new breaking feature"
    body = ["BREAKING CHANGE: there is a breaking feature in this code"]
    commit = Commit(hash="aaaaaaa", subject=subject, body=body, author_date="1574340645", committer_date="1574340645")
    style = AngularStyle()
    commit_dict = style.parse_commit(commit)
    assert commit_dict["is_major"]
    assert not commit_dict["is_minor"]
    assert not commit_dict["is_patch"]


def test_angular_style_breaking_changes():
    subject = "feat: this is a new breaking feature"
    body = ["BREAKING CHANGES: there is a breaking feature in this code"]
    commit = Commit(hash="aaaaaaa", subject=subject, body=body, author_date="1574340645", committer_date="1574340645")
    style = AngularStyle()
    commit_dict = style.parse_commit(commit)
    assert commit_dict["is_major"]
    assert not commit_dict["is_minor"]
    assert not commit_dict["is_patch"]


def test_angular_style_feat():
    subject = "feat: this is a new feature"
    commit = Commit(hash="aaaaaaa", subject=subject, author_date="1574340645", committer_date="1574340645")
    style = AngularStyle()
    commit_dict = style.parse_commit(commit)
    assert not commit_dict["is_major"]
    assert commit_dict["is_minor"]
    assert not commit_dict["is_patch"]


def test_angular_style_fix():
    subject = "fix: this is a bug fix"
    commit = Commit(hash="aaaaaaa", subject=subject, author_date="1574340645", committer_date="1574340645")
    style = AngularStyle()
    commit_dict = style.parse_commit(commit)
    assert not commit_dict["is_major"]
    assert not commit_dict["is_minor"]
    assert commit_dict["is_patch"]
