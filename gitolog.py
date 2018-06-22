import re
import sys
from subprocess import check_output
from datetime import datetime

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))


def bump(version, part='patch'):
    major, minor, patch = version.split('.', 2)
    patch = patch.split('-', 1)
    pre = ''
    if len(patch) > 1:
        patch, pre = patch
    if part == 'major':
        major = str(int(major) + 1)
        minor = patch = '0'
    elif part == 'minor':
        minor = str(int(minor) + 1)
        patch = '0'
    elif part == 'patch' and not pre:
        patch = str(int(patch) + 1)
    return '.'.join((major, minor, patch))


class Ref:
    BB = r'(?:^|[\s,])'
    BA = r'(?:[\s,]|$)'
    NP = r'(?:(?P<namespace>[-\w]+)/)?(?P<project>[-\w]+)'
    ID = r'(?P<ref>{symbol}[1-9]\d*)'
    ONE_WORD = r'(?P<ref>{symbol}\w[-\w]*)'
    MULTI_WORD = r'(?P<ref>{symbol}"\w[- \w]*")'
    COMMIT = r'(?P<ref>[0-9a-f]{{{min},{max}}})'
    COMMIT_RANGE = r'(?P<ref>[0-9a-f]{{{min},{max}}}\.\.\.[0-9a-f]{{{min},{max}}})'
    MENTION = r'(?P<ref>@\w[-\w]*)'


class ProviderRefParser:
    REF = {}

    @classmethod
    def parse_refs(cls, ref_type, text):
        return [m.groupdict() for m in cls.REF[ref_type].finditer(text)]


class GitHub(ProviderRefParser):
    REF = dict(
        issue=re.compile(Ref.BB + Ref.NP + '?' + Ref.ID.format(symbol='#'), re.I),
        commit=re.compile(Ref.BB + r'(?:{np}@)?{commit}{ba}'.format(
            np=Ref.NP, commit=Ref.COMMIT.format(min=7, max=40), ba=Ref.BA), re.I),
        commit_range=re.compile(Ref.BB + r'(?:{np}@)?{commit_range}'.format(
            np=Ref.NP, commit_range=Ref.COMMIT_RANGE.format(min=7, max=40)), re.I),
        mention=re.compile(Ref.BB + Ref.MENTION, re.I)
    )


class GitLab(ProviderRefParser):
    REF = dict(
        issue=re.compile(
            Ref.BB + Ref.NP + '?' + Ref.ID.format(symbol='#'), re.I),
        merge_request=re.compile(
            Ref.BB + Ref.NP + '?' + Ref.ID.format(symbol=r'!'), re.I),
        snippet=re.compile(
            Ref.BB + Ref.NP + '?' + Ref.ID.format(symbol=r'\$'), re.I),
        label_id=re.compile(
            Ref.BB + Ref.NP + '?' + Ref.ID.format(symbol=r'~'), re.I),
        label_one_word=re.compile(
            Ref.BB + Ref.NP + '?' + Ref.ONE_WORD.format(symbol=r'~'), re.I),
        label_multi_word=re.compile(
            Ref.BB + Ref.NP + '?' + Ref.MULTI_WORD.format(symbol=r'~'), re.I),
        milestone_id=re.compile(
            Ref.BB + Ref.NP + '?' + Ref.ID.format(symbol=r'%'), re.I),
        milestone_one_word=re.compile(
            Ref.BB + Ref.NP + '?' + Ref.ONE_WORD.format(symbol=r'%'), re.I),
        milestone_multi_word=re.compile(
            Ref.BB + Ref.NP + '?' + Ref.MULTI_WORD.format(symbol=r'%'), re.I),
        commit=re.compile(
            Ref.BB + r'(?:{np}@)?{commit}{ba}'.format(
                np=Ref.NP, commit=Ref.COMMIT.format(min=8, max=40), ba=Ref.BA), re.I),
        commit_range=re.compile(
            Ref.BB + r'(?:{np}@)?{commit_range}'.format(
                np=Ref.NP, commit_range=Ref.COMMIT_RANGE.format(min=8, max=40)), re.I),
        mention=re.compile(Ref.BB + Ref.MENTION, re.I)
    )


class Issue:
    def __init__(self, number='', url=''):
        self.number = number
        self.url = url


class Commit:
    def __init__(
            self, hash, author_name='', author_email='', author_date='',
            committer_name='', committer_email='', committer_date='',
            tag='', subject='', body=None, url='', style=None):
        self.hash = hash
        self.author_name = author_name
        self.author_email = author_email
        self.author_date = datetime.utcfromtimestamp(float(author_date))
        self.committer_name = committer_name
        self.committer_email = committer_email
        self.committer_date = datetime.utcfromtimestamp(float(committer_date))
        self.subject = subject
        self.body = body or []
        self.url = url

        if tag.startswith('tag: '):
            tag = tag.replace('tag: ', '')
        elif tag:
            tag = ''
        self.tag = self.version = tag

        self.type = ''
        self.issues = []

        if style:
            self.extra = style.parse_commit(self)


class Style:
    def parse_commit(self, commit):
        raise NotImplementedError


class DefaultStyle(Style):
    TYPES = {
        'add': 'Added',
        'fix': 'Fixed',
        'change': 'Changed',
        'remove': 'Removed',
        'merge': 'Merged',
        'doc': 'Documented'
    }

    TYPE_REGEX = re.compile(r'^(?P<type>(%s))' % '|'.join(TYPES.keys()), re.I)
    CLOSED = ('close', 'fix')
    ISSUE_REGEX = re.compile(r'(?P<issues>((%s)\w* )?(#\d+,? ?)+)' % '|'.join(CLOSED))
    BREAK_REGEX = re.compile(r'^break(s|ing changes)?[ :].+$')

    def __init__(self, issue_url):
        self.issue_url = issue_url

    def parse_commit(self, commit):
        commit_type = self.parse_type(commit.subject)
        message = '\n'.join([commit.subject] + commit.body)
        is_major = self.is_major(message)
        is_minor = not is_major or self.is_minor(commit_type)
        is_patch = not any((is_major, is_minor))
        issues = self.parse_issues(message)

        info = dict(
            type=commit_type,
            issues=issues,
            related_issues=[],
            closed_issues=[],
            is_major=is_major,
            is_minor=is_minor,
            is_patch=is_patch
        )

        for issue in issues:
            {True: info['closed_issues'],  # on-the-fly dict.gets are fun
             False: info['related_issues']}.get(issue.closed).append(issue)

    def parse_type(self, commit_subject):
        type_match = self.TYPE_REGEX.match(commit_subject)
        if type_match is not None:
            return self.TYPES.get(type_match.groupdict().get('type').lower())

    def parse_issues(self, commit_message):
        issues = []
        issue_match = self.ISSUE_REGEX.match(commit_message)
        if issue_match is not None:
            issues_found = issue_match.groupdict().get('issues')
            for issue in issues_found:
                closed = False
                numbers = issue
                for close_word in self.CLOSED:
                    if issue.lower().startswith(close_word):
                        closed = True
                        numbers = issue.split(' ', 1)[1]
                        break
                numbers = numbers.replace(',', '').replace(' ', '').lstrip('#').split('#')
                for number in numbers:
                    url = self.issue_url.format(number)
                    issue = Issue(number=number, url=url, closed=closed)
                    issues.append(issue)
        return issues

    def is_minor(self, commit_type):
        return commit_type == self.TYPES['add']

    def is_major(self, commit_message):
        return bool(self.BREAK_REGEX.match(commit_message))


class AngularStyle(Style):
    SUBJECT_REGEX = re.compile(
        r'^(?P<type>(feat|fix|docs|style|refactor|test|chore))'
        r'(?P<scope>\(.+\))?: (?P<subject>.+)$')

    def parse_commit(self, commit):
        pass

    @staticmethod
    def is_minor(commit_type):
        return commit_type == 'feat'


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
    STYLE = {
        'angular': AngularStyle
    }

    def __init__(
            self, repository,
            project_url='', commit_url='', issue_url='', compare_url='', version_url='',
            style=DefaultStyle):
        self.repository = repository
        self.project_url = project_url if project_url else self.get_url()

        if not commit_url:
            commit_url = self.project_url + '/commit/'
        if not issue_url:
            issue_url = self.project_url + '/issues/'
        if not compare_url:
            compare_url = self.project_url + '/compare/'
        if not version_url:
            version_url = self.project_url + '/releases/tag/'

        self.commit_url = commit_url
        self.issue_url = issue_url
        self.compare_url = compare_url
        self.version_url = version_url

        self.raw_log = self.get_log()
        self.commits = self.parse_commits()

        dates = self.apply_versions_to_commits()
        versions = self.group_commits_by_version(dates)
        self.versions_list = versions['as_list']
        self.versions_dict = versions['as_dict']

        if not self.versions_list[0].tag and len(self.versions_list) > 1:
            last_tag = self.versions_list[1].tag
            major = minor = False
            for commit in self.versions_list[0].commits:
                if commit.is_major:
                    major = True
                    break
                elif commit.is_minor:
                    minor = True
            if major:
                planned_tag = bump(last_tag, 'major')
            elif minor:
                planned_tag = bump(last_tag, 'minor')
            else:
                planned_tag = bump(last_tag, 'patch')
            self.versions_list[0].planned_tag = planned_tag

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
        versions_dates = {'': None}
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
