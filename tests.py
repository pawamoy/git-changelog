import gitolog

message = """
This is the subject #1

This is the body. Related: #2. Also mentions #3 and #4.
Closes #5. closed #6, #7. FIX: #89 and #10.
Resolve        #1111.
Also support other projects references like shellm-org/shellm-data#19!!
Or fix pawamoy/gitolog#1.
Don't match this one: #01.
"""


def test_github_issue_parsing():
    matches = gitolog.GitHub.parse_issues_refs(message)
    for match in matches:
        print(match)


def test_gitlab_issue_parsing():
    matches = gitolog.GitLab.parse_issues_refs(message)
    for match in matches:
        print(match)


if __name__ == '__main__':
    # test_github_issue_parsing()
    test_gitlab_issue_parsing()
