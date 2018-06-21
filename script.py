import re
import sys
from subprocess import check_output
from datetime import datetime

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))


class Issue:
    def __init__(self, number='', url=''):
        self.number = number
        self.url = url


class Commit:
    subject_regex = re.compile(
        r'^(?P<type>((add(ed|s)?)|(change[ds]?)|(fix(es|ed)?)|(remove[sd]?)|(merged?)))',
        re.IGNORECASE)
    body_regex = re.compile(r'(?P<issues>#\d+)')
    break_regex = re.compile(r'^break(s|ing changes)?[ :].+$')
    types = {
        'add': 'Added',
        'fix': 'Fixed',
        'change': 'Changed',
        'remove': 'Removed',
        'merge': 'Merged'
    }

    def __init__(
            self, hash, author_name='', author_email='', author_date='',
            committer_name='', committer_email='', committer_date='',
            tag='', subject='', body=None, url=''):
        self.hash = hash
        self.author_name = author_name
        self.author_email = author_email
        self.author_date = datetime.utcfromtimestamp(float(author_date))
        self.committer_name = committer_name
        self.committer_email = committer_email
        self.committer_date = datetime.utcfromtimestamp(float(committer_date))
        self.tag = self.version = tag.replace('tag: ', '')
        self.subject = subject
        self.body = body or []
        self.type = ''
        self.url = url
        self.issues = []

        self.has_breaking_change = None
        self.adds_feature = None

        self.parse_message()
        self.fix_type()

    def parse_message(self):
        subject_match = self.subject_regex.match(self.subject)
        if subject_match is not None:
            for group, value in subject_match.groupdict().items():
                setattr(self, group, value)
        body_match = self.body_regex.match('\n'.join(self.body))
        if body_match is not None:
            for group, value in body_match.groupdict().items():
                setattr(self, group, value)

    def fix_type(self):
        for k, v in self.types.items():
            if self.type.lower().startswith(k):
                self.type = v

    def build_issues(self, url):
        self.issues = [Issue(number=issue, url=url + issue)
                       if isinstance(issue, str) else issue
                       for issue in self.issues]

    @property
    def is_patch(self):
        return not any((self.is_minor, self.is_major))

    @property
    def is_minor(self):
        return self.type.lower() in ('add', 'adds', 'added') and not self.is_major

    @property
    def is_major(self):
        return bool(self.break_regex.match('\n'.join(self.body)))


class AngularCommit(Commit):
    subject_regex = re.compile(
        r'^(?P<type>(feat|fix|docs|style|refactor|test|chore))'
        r'(?P<scope>\(.+\))?: (?P<subject>.+)$')

    @property
    def is_minor(self):
        return self.type.lower() == 'feat' and not self.is_major

    def fix_type(self):
        pass


class Gitolog:
    MARKER = '--GITOLOG MARKER--'
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

    COMMAND = ['git', 'log', '--date=unix', '--format=' + FORMAT]
    DEFAULT_STYLE = 'basic'
    STYLE = {
        'basic': Commit,
        'angular': AngularCommit
    }

    def __init__(
            self, repository,
            project_url='', commit_url='', issue_url='', compare_url='',
            style=DEFAULT_STYLE):
        self.repository = repository
        self.project_url = project_url if project_url else self.get_url()

        if not commit_url:
            commit_url = self.project_url + '/commit/'
        if not issue_url:
            issue_url = self.project_url + '/issues/'
        if not compare_url:
            compare_url = self.project_url + '/compare/'

        self.commit_url = commit_url
        self.issue_url = issue_url
        self.compare_url = compare_url

        self.raw_log = self.get_log()
        self.commits = self.parse_commits()

        dates = self.apply_versions_to_commits()
        versions = self.group_commits_by_version(dates)
        self.versions_list = versions['as_list']
        self.versions_dict = versions['as_dict']

        if isinstance(style, str):
            try:
                style = self.STYLE[style]
            except KeyError:
                print('no such style available: %s' % style, file=sys.stderr)
                print('using default style: %s' % self.DEFAULT_STYLE, file=sys.stderr)
                style = self.STYLE[self.DEFAULT_STYLE]

        self.style = style

    def get_url(self):
        git_url = str(check_output(
            ['git', 'config', '--get', 'remote.origin.url'],
            cwd=self.repository))[2:-1].rstrip('\\n')
        if git_url.startswith('git@'):
            split = git_url.replace('git@', '', 1).split(':', 1)
            git_url = 'https://' + split[0] + '/' + split[1]
        return git_url

    def get_log(self):
        # remove enclosing b-quotes (b'' or b"")
        return str(check_output(self.COMMAND, cwd=self.repository))[2:-1].replace("\\'", "'")

    def parse_commits(self):
        lines = self.raw_log.split('\\n')
        size = len(lines) - 1  # don't count last blank line
        commits = []
        pos = 0
        while pos < size:
            commit = Commit(
                hash=lines[pos],
                author_name=lines[pos+1],
                author_email=lines[pos+2],
                author_date=lines[pos+3],
                committer_name=lines[pos+4],
                committer_email=lines[pos+5],
                committer_date=lines[pos+6],
                tag=lines[pos+7],
                subject=lines[pos+8],
                body=[lines[pos+9]],
                url=self.commit_url + lines[pos]
            )
            commits.append(commit)
            commit.build_issues(url=self.issue_url)
            nbl_index = 10
            while lines[pos+nbl_index] != self.MARKER:
                commit.body.append(lines[pos+nbl_index])
                nbl_index += 1
            pos += nbl_index + 1
        return commits

    def apply_versions_to_commits(self):
        versions_dates = {}
        version = None
        for commit in self.commits:
            if commit.version:
                version = commit.version
                versions_dates[version] = commit.committer_date.date()
            elif version:
                commit.version = version
        return versions_dates

    def group_commits_by_version(self, dates):
        versions_list = []
        versions_dict = {}
        versions_types_dict = {}
        next_version = None
        for commit in self.commits:
            if commit.version not in versions_dict:
                version = versions_dict[commit.version] = Version(
                    tag=commit.version, date=dates[commit.version])
                if next_version:
                    version.next_version = next_version
                    next_version.previous_version = version
                next_version = version
                versions_list.append(version)
                versions_types_dict[commit.version] = {}
            versions_dict[commit.version].commits.append(commit)
            if commit.type not in versions_types_dict[commit.version]:
                section = versions_types_dict[commit.version][commit.type] = Section(
                    type=commit.type)
                versions_dict[commit.version].sections_list.append(section)
                versions_dict[commit.version].sections_dict = versions_types_dict[commit.version]
            versions_types_dict[commit.version][commit.type].commits.append(commit)
        return {'as_list': versions_list, 'as_dict': versions_dict}


class Version:
    def __init__(self, tag='', date='', sections=None, commits=None, url=''):
        self.tag = tag
        self.date = date

        self.sections_list = sections or []
        self.sections_dict = {s.type: s for s in self.sections_list}
        self.commits = commits or []
        self.url = url
        self.previous_version = None
        self.next_version = None

    @property
    def typed_sections(self):
        return [s for s in self.sections_list if s.type]

    @property
    def untyped_section(self):
        return self.sections_dict.get('', None)


class Section:
    def __init__(self, type='', commits=None):
        self.type = type
        self.commits = commits or []


if __name__ == '__main__':
    gitolog = Gitolog('example2')
    template = env.get_template('changelog.md')
    rendered = template.render(gitolog=gitolog)
    with open('output.md', 'w') as stream:
        stream.write(rendered)
    sys.exit(0)
