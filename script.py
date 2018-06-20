import os
import sys
from subprocess import check_output

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))


class GitLog:
    MARKER = '--PYCHOLOG MARKER--'
    FORMAT = (
        '%H%n'  # commit hash
        '%an%n'  # author name
        '%ae%n'  # author email
        '%ad%n'  # author date
        '%cn%n'  # committer name
        '%ce%n'  # committer email
        '%cd%n'  # committer date
        '%D%n'  # tag
        '%s%n'  # subject
        '%b%n' + MARKER  # body
    )

    COMMAND = ['git', 'log', '--tags', '--date=raw', '--format=' + FORMAT]

    def __init__(self, repository):
        self.repository = repository
        self.raw_log = self.get()
        self.commits = self.parse_commits()

    def get(self):
        # remove enclosing b-quotes (b'' or b"")
        return str(check_output(self.COMMAND, cwd=self.repository))[2:-1].replace("\\'", "'")

    def parse_commits(self):
        lines = self.raw_log.split('\\n')
        size = len(lines) - 1  # don't count last blank line
        commits = []
        pos = 0
        while pos < size:
            commit = Commit(
                commit_hash=lines[pos],
                author_name=lines[pos+1],
                author_email=lines[pos+2],
                author_date=lines[pos+3],
                committer_name=lines[pos+4],
                committer_email=lines[pos+5],
                committer_date=lines[pos+6],
                tag=lines[pos+7],
                subject=lines[pos+8],
                body=[lines[pos+9]]
            )
            commits.append(commit)
            nbl_index = 10
            while lines[pos+nbl_index] != self.MARKER:
                commit.body.append(lines[pos+nbl_index])
                nbl_index += 1
            pos += nbl_index + 1
        return commits


class Commit:
    def __init__(self, commit_hash,
                 author_name=None, author_email=None, author_date=None,
                 committer_name=None, committer_email=None, committer_date=None,
                 tag=None, subject=None, body=None):
        self.commit_hash = commit_hash
        self.author_name = author_name
        self.author_email = author_email
        self.author_date = author_date
        self.committer_name = committer_name
        self.committer_email = committer_email
        self.committer_date = committer_date
        self.tag = tag
        self.subject = subject
        self.body = body or []


if __name__ == '__main__':
    commits = GitLog('example2').commits
    template = env.get_template('changelog.md')
    rendered = template.render(commits=commits)
    with open('output.md', 'w') as stream:
        stream.write(rendered)
    for commit in commits:
        print(commit.subject)
    sys.exit(0)
