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


class RefRe:
    BB = r'(?:^|[\s,])'  # blank before
    BA = r'(?:[\s,]|$)'  # blank after
    NP = r'(?:(?P<namespace>[-\w]+)/)?(?P<project>[-\w]+)'  # namespace and project
    ID = r'{symbol}(?P<ref>[1-9]\d*)'
    ONE_WORD = r'{symbol}(?P<ref>\w*[-a-z_ ][-\w]*)'
    MULTI_WORD = r'{symbol}(?P<ref>"\w[- \w]*")'
    COMMIT = r'(?P<ref>[0-9a-f]{{{min},{max}}})'
    COMMIT_RANGE = r'(?P<ref>[0-9a-f]{{{min},{max}}}\.\.\.[0-9a-f]{{{min},{max}}})'
    MENTION = r'@(?P<ref>\w[-\w]*)'


class Ref:
    def __init__(self, ref, url):
        self.ref = ref
        self.url = url

    def __str__(self):
        return self.ref + ': ' + self.url


class ProviderRefParser:
    REF = {}

    def get_refs(self, ref_type, text):
        return [
            Ref(
                ref=match.group().strip(),
                url=self.build_ref_url(ref_type, match.groupdict())
            ) for match in self.parse_refs(ref_type, text)
        ]

    def parse_refs(self, ref_type, text):
        if ref_type not in self.REF:
            refs = [k for k in self.REF.keys() if k.startswith(ref_type)]
            return [m for ref in refs for m in self.REF[ref].finditer(text)]
        return [m for m in self.REF[ref_type]['regex'].finditer(text)]

    def build_ref_url(self, ref_type, match_dict):
        return self.REF[ref_type]['url'].format(**match_dict)


class GitHub(ProviderRefParser):
    url = 'https://github.com'
    project_url = '{base_url}/{namespace}/{project}'
    tag_url = '{base_url}/{namespace}/{project}/releases/tag/{ref}'

    REF = dict(
        issues=dict(
            regex=re.compile(RefRe.BB + RefRe.NP + '?' + RefRe.ID.format(symbol='#'), re.I),
            url='{base_url}/{namespace}/{project}/issues/{ref}'),
        commits=dict(
            regex=re.compile(RefRe.BB + r'(?:{np}@)?{commit}{ba}'.format(
                np=RefRe.NP, commit=RefRe.COMMIT.format(min=7, max=40), ba=RefRe.BA), re.I),
            url='{base_url}/{namespace}/{project}/commit/{ref}'),
        commits_ranges=dict(
            regex=re.compile(RefRe.BB + r'(?:{np}@)?{commit_range}'.format(
                np=RefRe.NP, commit_range=RefRe.COMMIT_RANGE.format(min=7, max=40)), re.I),
            url='{base_url}/{namespace}/{project}/compare/{ref}'),
        mentions=dict(regex=re.compile(RefRe.BB + RefRe.MENTION, re.I), url='{base_url}/{ref}')
    )

    def __init__(self, namespace, project, url=url):
        self.namespace = namespace
        self.project = project
        self.url = url

    def build_ref_url(self, ref_type, match_dict):
        match_dict['base_url'] = self.url
        if not match_dict.get('namespace'):
            match_dict['namespace'] = self.namespace
        if not match_dict.get('project'):
            match_dict['project'] = self.project
        return super(GitHub, self).build_ref_url(ref_type, match_dict)

    def get_tag_url(self, tag=''):
        return self.tag_url.format(
            base_url=self.url, namespace=self.namespace, project=self.project, ref=tag)


class GitLab(ProviderRefParser):
    url = 'https://gitlab.com'
    project_url = '{base_url}/{namespace}/{project}'
    tag_url = '{base_url}/{namespace}/{project}/tags/{ref}'

    REF = dict(
        issues=dict(
            regex=re.compile(
                RefRe.BB + RefRe.NP + '?' + RefRe.ID.format(symbol='#'), re.I),
            url='{base_url}/{namespace}/{project}/issues/{ref}'
        ),
        merge_requests=dict(
            regex=re.compile(
                RefRe.BB + RefRe.NP + '?' + RefRe.ID.format(symbol=r'!'), re.I),
            url='{base_url}/{namespace}/{project}/merge_requests/{ref}'
        ),
        snippets=dict(
            regex=re.compile(
                RefRe.BB + RefRe.NP + '?' + RefRe.ID.format(symbol=r'\$'), re.I),
            url='{base_url}/{namespace}/{project}/snippets/{ref}'
        ),
        labels_ids=dict(
            regex=re.compile(
                RefRe.BB + RefRe.NP + '?' + RefRe.ID.format(symbol=r'~'), re.I),
            url='{base_url}/{namespace}/{project}/issues?label_name[]={ref}'  # no label_id param?
        ),
        labels_one_word=dict(
            regex=re.compile(  # also matches label IDs
                RefRe.BB + RefRe.NP + '?' + RefRe.ONE_WORD.format(symbol=r'~'), re.I),
            url='{base_url}/{namespace}/{project}/issues?label_name[]={ref}'
        ),
        labels_multi_word=dict(
            regex=re.compile(
                RefRe.BB + RefRe.NP + '?' + RefRe.MULTI_WORD.format(symbol=r'~'), re.I),
            url='{base_url}/{namespace}/{project}/issues?label_name[]={ref}'
        ),
        milestones_ids=dict(
            regex=re.compile(  # also matches milestones IDs
                RefRe.BB + RefRe.NP + '?' + RefRe.ID.format(symbol=r'%'), re.I),
            url='{base_url}/{namespace}/{project}/milestones/{ref}'
        ),
        milestones_one_word=dict(
            regex=re.compile(
                RefRe.BB + RefRe.NP + '?' + RefRe.ONE_WORD.format(symbol=r'%'), re.I),
            url='{base_url}/{namespace}/{project}/milestones'  # cannot guess ID
        ),
        milestones_multi_word=dict(
            regex=re.compile(
                RefRe.BB + RefRe.NP + '?' + RefRe.MULTI_WORD.format(symbol=r'%'), re.I),
            url='{base_url}/{namespace}/{project}/milestones'  # cannot guess ID
        ),
        commits=dict(
            regex=re.compile(
                RefRe.BB + r'(?:{np}@)?{commit}{ba}'.format(
                    np=RefRe.NP, commit=RefRe.COMMIT.format(min=8, max=40), ba=RefRe.BA), re.I),
            url='{base_url}/{namespace}/{project}/commit/{ref}'
        ),
        commits_ranges=dict(
            regex=re.compile(
                RefRe.BB + r'(?:{np}@)?{commit_range}'.format(
                    np=RefRe.NP, commit_range=RefRe.COMMIT_RANGE.format(min=8, max=40)), re.I),
            url='{base_url}/{namespace}/{project}/compare/{ref}'
        ),
        mentions=dict(regex=re.compile(RefRe.BB + RefRe.MENTION, re.I), url='{base_url}/{ref}')
    )

    def __init__(self, namespace, project, url=url):
        self.namespace = namespace
        self.project = project
        self.url = url

    def build_ref_url(self, ref_type, match_dict):
        match_dict['base_url'] = self.url
        if 'namespace' in match_dict and match_dict['namespace'] is None:
            match_dict['namespace'] = self.namespace
        if 'project' in match_dict and match_dict['project'] is None:
            match_dict['project'] = self.project
        if ref_type.startswith('label'):
            match_dict['ref'] = match_dict['ref'].replace('"', '').replace(' ', '+')
        return super(GitLab, self).build_ref_url(ref_type, match_dict)

    def get_tag_url(self, tag=''):
        return self.tag_url.format(
            base_url=self.url, namespace=self.namespace, project=self.project, ref=tag)


class Commit:
    def __init__(
            self, hash, author_name='', author_email='', author_date='',
            committer_name='', committer_email='', committer_date='',
            ref='', subject='', body=None, url=''):
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

        if ref.startswith('tag: '):
            ref = ref.replace('tag: ', '')
        elif ref:
            ref = ''
        self.tag = self.version = ref

        self.text_refs = {}
        self.style = {}

    def update_with_style(self, style):
        self.style.update(style.parse_commit(self))

    def update_with_provider(self, provider):
        # set the commit url based on provider
        # FIXME: hardcoded 'commits'
        if 'commits' in provider.REF:
            self.url = provider.build_ref_url('commits', {'ref': self.hash})
        else:
            # use default "commit" url (could be wrong)
            self.url = '%s/%s/%s/commit/%s' % (
                provider.url, provider.namespace,
                provider.project, self.hash)

        # build commit text references from its subject and body
        for ref_type in provider.REF.keys():
            self.text_refs[ref_type] = provider.get_refs(
                ref_type, '\n'.join([self.subject] + self.body))

        if 'issues' in self.text_refs:
            self.text_refs['issues_not_in_subject'] = []
            for issue in self.text_refs['issues']:
                if issue.ref not in self.subject:
                    self.text_refs['issues_not_in_subject'].append(issue)


class CommitStyle:
    def parse_commit(self, commit):
        raise NotImplementedError


class DefaultStyle(CommitStyle):
    TYPES = {
        'add': 'Added',
        'fix': 'Fixed',
        'change': 'Changed',
        'remove': 'Removed',
        'merge': 'Merged',
        'doc': 'Documented'
    }

    TYPE_REGEX = re.compile(r'^(?P<type>(%s))' % '|'.join(TYPES.keys()), re.I)
    BREAK_REGEX = re.compile(r'^break(s|ing changes)?[ :].+$', re.I)

    def parse_commit(self, commit):
        commit_type = self.parse_type(commit.subject)
        message = '\n'.join([commit.subject] + commit.body)
        is_major = self.is_major(message)
        is_minor = not is_major and self.is_minor(commit_type)
        is_patch = not any((is_major, is_minor))

        return dict(
            type=commit_type,
            is_major=is_major,
            is_minor=is_minor,
            is_patch=is_patch
        )

    def parse_type(self, commit_subject):
        type_match = self.TYPE_REGEX.match(commit_subject)
        if type_match:
            return self.TYPES.get(type_match.groupdict().get('type').lower())
        return ''

    def is_minor(self, commit_type):
        return commit_type == self.TYPES['add']

    def is_major(self, commit_message):
        return bool(self.BREAK_REGEX.match(commit_message))


class AngularStyle(CommitStyle):
    TYPES = {
        # 'build': 'Build',
        # 'ci': 'CI',
        'perf': 'Performance Improvements',
        'feat': 'Features',
        'fix': 'Bug Fixes',
        'revert': 'Reverts',
        # 'docs': 'Docs',
        # 'style': '',
        'refactor': 'Code Refactoring',
        # 'test': '',
        # 'chore': '',
    }
    SUBJECT_REGEX = re.compile(
        r'^(?P<type>(%s))(?:\((?P<scope>.+)\))?: (?P<subject>.+)$' % ('|'.join(TYPES.keys())))
    BREAK_REGEX = re.compile(r'^break(s|ing changes)?[ :].+$', re.I)

    def parse_commit(self, commit):
        subject = self.parse_subject(commit.subject)
        message = '\n'.join([commit.subject] + commit.body)
        is_major = self.is_major(message)
        is_minor = not is_major and self.is_minor(subject['type'])
        is_patch = not any((is_major, is_minor))

        return dict(
            type=subject['type'],
            scope=subject['scope'],
            subject=subject['subject'],
            is_major=is_major,
            is_minor=is_minor,
            is_patch=is_patch
        )

    def parse_subject(self, commit_subject):
        subject_match = self.SUBJECT_REGEX.match(commit_subject)
        if subject_match:
            dct = subject_match.groupdict()
            dct['type'] = self.TYPES[dct['type']]
            return dct
        return {'type': '', 'scope': '', 'subject': commit_subject}

    @staticmethod
    def is_minor(commit_type):
        return commit_type == 'feat'

    def is_major(self, commit_message):
        return bool(self.BREAK_REGEX.match(commit_message))


class AtomStyle(CommitStyle):
    TYPES = {
        ':art:': '',  # when improving the format/structure of the code
        ':racehorse:': '',  # when improving performance
        ':non-potable_water:': '',  # when plugging memory leaks
        ':memo:': '',  # when writing docs
        ':penguin:': '',  # when fixing something on Linux
        ':apple:': '',  # when fixing something on Mac OS
        ':checkered_flag:': '',  # when fixing something on Windows
        ':bug:': '',  # when fixing a bug
        ':fire:': '',  # when removing code or files
        ':green_heart:': '',  # when fixing the CI build
        ':white_check_mark:': '',  # when adding tests
        ':lock:': '',  # when dealing with security
        ':arrow_up:': '',  # when upgrading dependencies
        ':arrow_down:': '',  # when downgrading dependencies
        ':shirt:': '',  # when removing linter warnings
    }


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
    STYLE = {
        'angular': AngularStyle
    }

    def __init__(self, repository, provider=None, style=DefaultStyle()):
        self.repository = repository

        # set provider
        if not provider:
            remote_url = self.get_remote_url()
            split = remote_url.split('/')
            provider_url = '/'.join(split[:3])
            namespace, project = split[3], split[4]
            if 'github' in provider_url:
                provider = GitHub(namespace, project, url=provider_url)
            elif 'gitlab' in provider_url:
                provider = GitLab(namespace, project, url=provider_url)
            self.remote_url = remote_url
        self.provider = provider

        # set style
        if isinstance(style, str):
            try:
                style = self.STYLE[style]
            except KeyError:
                print('no such style available: %s' % style, file=sys.stderr)
                print('using default style', file=sys.stderr)
                style = DefaultStyle()
        self.style = style

        # get git log and parse it into list of commits
        self.raw_log = self.get_log()
        self.commits = self.parse_commits()

        # apply dates to commits and group them by version
        dates = self.apply_versions_to_commits()
        versions = self.group_commits_by_version(dates)
        self.versions_list = versions['as_list']
        self.versions_dict = versions['as_dict']

        # guess the next version number based on last version and recent commits
        if not self.versions_list[0].tag and len(self.versions_list) > 1:
            last_tag = self.versions_list[1].tag
            major = minor = False
            for commit in self.versions_list[0].commits:
                if commit.style['is_major']:
                    major = True
                    break
                elif commit.style['is_minor']:
                    minor = True
            if major:
                planned_tag = bump(last_tag, 'major')
            elif minor:
                planned_tag = bump(last_tag, 'minor')
            else:
                planned_tag = bump(last_tag, 'patch')
            self.versions_list[0].planned_tag = planned_tag

    def get_remote_url(self):
        git_url = str(check_output(
            ['git', 'config', '--get', 'remote.origin.url'],
            cwd=self.repository))[2:-1].rstrip('\\n')
        if git_url.startswith('git@'):
            git_url = git_url.replace(':', '/', 1).replace('git@', 'https://', 1)
        return git_url

    def get_log(self):
        # remove enclosing b-quotes (b'' or b"")
        return str(check_output(
            ['git', 'log', '--date=unix', '--format=' + self.FORMAT],
            cwd=self.repository))[2:-1].replace("\\'", "'")

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
                ref=lines[pos+7],
                subject=lines[pos+8],
                body=[lines[pos+9]]
            )

            # append body lines
            nbl_index = 10
            while lines[pos+nbl_index] != self.MARKER:
                commit.body.append(lines[pos+nbl_index])
                nbl_index += 1
            pos += nbl_index + 1

            # expand commit object with provider parsing
            if self.provider:
                commit.update_with_provider(self.provider)

            elif self.remote_url:
                # set the commit url based on remote_url (could be wrong)
                commit.url = self.remote_url + '/commit/' + commit.hash

            # expand commit object with style parsing
            if self.style:
                commit.update_with_style(self.style)

            commits.append(commit)

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
                version.url = self.provider.get_tag_url(tag=commit.version)
                if next_version:
                    version.next_version = next_version
                    next_version.previous_version = version
                    next_version.compare_url = self.provider.build_ref_url(
                        # FIXME: hardcoded 'commits_ranges'
                        'commits_ranges', {'ref': '%s...%s' % (
                            version.tag, next_version.tag or 'HEAD')})
                next_version = version
                versions_list.append(version)
                versions_types_dict[commit.version] = {}
            versions_dict[commit.version].commits.append(commit)
            if 'type' in commit.style \
                    and commit.style['type'] not in versions_types_dict[commit.version]:
                section = versions_types_dict[commit.version][commit.style['type']] = Section(
                    type=commit.style['type'])
                versions_dict[commit.version].sections_list.append(section)
                versions_dict[commit.version].sections_dict = versions_types_dict[commit.version]
            versions_types_dict[commit.version][commit.style['type']].commits.append(commit)
        next_version.compare_url = self.provider.build_ref_url(
            # FIXME: hardcoded 'commits_ranges'
            'commits_ranges', {'ref': '%s...%s' % (
                versions_list[-1].commits[-1].hash, next_version.tag or 'HEAD')})
        return {'as_list': versions_list, 'as_dict': versions_dict}


class Version:
    def __init__(self, tag='', date='', sections=None, commits=None, url='', compare_url=''):
        self.tag = tag
        self.date = date

        self.sections_list = sections or []
        self.sections_dict = {s.type: s for s in self.sections_list}
        self.commits = commits or []
        self.url = url
        self.compare_url = compare_url
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
    gitolog = Gitolog('example3', style=AngularStyle())
    template = env.get_template('angular/changelog.md')
    rendered = template.render(gitolog=gitolog)
    with open('output.md', 'w') as stream:
        stream.write(rendered)
    sys.exit(0)
