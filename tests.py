import gitolog

text = """
This is the subject #1

This is the body. Related: #2. Also mentions #3 and #4.
Closes #5. closed #6, #7. FIX: #89 and #10.
Resolve        #1111.
Also support other projects references like shellm-org/shellm-data#19!!
Or fix pawamoy/gitolog#1.
Don't match this one: #01.

Now some other references:

A merge request: !153!
A mention: @hello
A commit gitolog@06abf793
A longer commit 3879fabda896da89954adec8
A commit range: 00000000...11111111
A snippet: $45
Some labels: ~18, ~bug, ~"multi word label"
Some milestones: %2, %version1, %"awesome version"
"""


def test_github_issue_parsing():
    for ref in gitolog.GitHub.REF.keys():
        print('Searching %s references for GitHub' % ref)
        matches = gitolog.GitHub.parse_refs(ref, text)
        for match in matches:
            print(match)
        print('')


def test_gitlab_issue_parsing():
    for ref in gitolog.GitLab.REF.keys():
        print('Searching %s references for GitLab' % ref)
        matches = gitolog.GitLab.parse_refs(ref, text)
        for match in matches:
            print(match)
        print('')


if __name__ == '__main__':
    test_github_issue_parsing()
    test_gitlab_issue_parsing()
