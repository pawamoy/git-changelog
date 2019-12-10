import sys
from datetime import datetime, date as date_type
from subprocess import check_output  # nosec
from typing import List, Dict, Union, Type

from .providers import GitHub, GitLab, ProviderRefParser, Ref
from .style import AngularStyle, AtomStyle, BasicStyle, CommitStyle


def bump(version: str, part: str = "patch") -> str:
    major, minor, patch = version.split(".", 2)
    patch = patch.split("-", 1)
    pre = ""
    if len(patch) > 1:
        patch, pre = patch
    else:
        patch = patch[0]
    if part == "major":
        major = str(int(major) + 1)
        minor = patch = "0"
    elif part == "minor":
        minor = str(int(minor) + 1)
        patch = "0"
    elif part == "patch" and not pre:
        patch = str(int(patch) + 1)
    return ".".join((major, minor, patch))


class Commit:
    def __init__(
        self,
        hash: str,
        author_name: str = "",
        author_email: str = "",
        author_date: str = "",
        committer_name: str = "",
        committer_email: str = "",
        committer_date: str = "",
        refs: str = "",
        subject: str = "",
        body: List[str] = None,
        url: str = "",
    ):
        self.hash: str = hash
        self.author_name: str = author_name
        self.author_email: str = author_email
        self.author_date: datetime = datetime.utcfromtimestamp(float(author_date))
        self.committer_name: str = committer_name
        self.committer_email: str = committer_email
        self.committer_date: datetime = datetime.utcfromtimestamp(float(committer_date))
        self.subject: str = subject
        self.body: List[str] = body or []
        self.url: str = url

        tag = ""
        for ref in refs.split(","):
            ref = ref.strip()
            if ref.startswith("tag: "):
                tag = ref.replace("tag: ", "")
                break
        self.tag: str = tag
        self.version: str = tag

        self.text_refs: Dict[str, List[Ref]] = {}
        self.style: Dict[str, Union[str, bool]] = {}

    def update_with_style(self, style: CommitStyle):
        self.style.update(style.parse_commit(self))

    def update_with_provider(self, provider: ProviderRefParser):
        # set the commit url based on provider
        # FIXME: hardcoded 'commits'
        if "commits" in provider.REF:
            self.url = provider.build_ref_url("commits", {"ref": self.hash})
        else:
            # use default "commit" url (could be wrong)
            self.url = "%s/%s/%s/commit/%s" % (provider.url, provider.namespace, provider.project, self.hash)

        # build commit text references from its subject and body
        for ref_type in provider.REF.keys():
            self.text_refs[ref_type] = provider.get_refs(ref_type, "\n".join([self.subject] + self.body))

        if "issues" in self.text_refs:
            self.text_refs["issues_not_in_subject"] = []
            for issue in self.text_refs["issues"]:
                if issue.ref not in self.subject:
                    self.text_refs["issues_not_in_subject"].append(issue)


class Section:
    def __init__(self, type: str = "", commits: List[Commit] = None):
        self.type: str = type
        self.commits: List[Commit] = commits or []


class Version:
    def __init__(self,
                 tag: str = "",
                 date: date_type = "",
                 sections: List[Section] = None,
                 commits: List[Commit] = None,
                 url: str = "", compare_url: str = ""):
        self.tag: str = tag
        self.date: date_type = date

        self.sections_list: List[Section] = sections or []
        self.sections_dict: Dict[str, Section] = {s.type: s for s in self.sections_list}
        self.commits: List[Commit] = commits or []
        self.url: str = url
        self.compare_url: str = compare_url
        self.previous_version: Union[Version, None] = None
        self.next_version: Union[Version, None] = None

    @property
    def typed_sections(self) -> List[Section]:
        return [s for s in self.sections_list if s.type]

    @property
    def untyped_section(self) -> Section:
        return self.sections_dict.get("", None)

    @property
    def is_major(self) -> bool:
        return self.tag.split(".", 1)[1].startswith("0.0")

    @property
    def is_minor(self) -> bool:
        return bool(self.tag.split(".", 2)[2])


class Changelog:
    MARKER: str = "--GITOLOG MARKER--"
    FORMAT: str = (
        "%H%n"  # commit hash
        "%an%n"  # author name
        "%ae%n"  # author email
        "%ad%n"  # author date
        "%cn%n"  # committer name
        "%ce%n"  # committer email
        "%cd%n"  # committer date
        "%D%n"  # tag
        "%s%n"  # subject
        "%b%n" + MARKER  # body
    )
    STYLE: Dict[str, Type[CommitStyle]] = {"basic": BasicStyle, "angular": AngularStyle, "atom": AtomStyle}

    def __init__(self,
                 repository: str,
                 provider: str = None,
                 style: Union[str, CommitStyle, Type[CommitStyle]] = None):
        self.repository: str = repository

        # set provider
        if not provider:
            remote_url = self.get_remote_url()
            split = remote_url.split("/")
            provider_url = "/".join(split[:3])
            namespace, project = split[3], split[4]
            if "github" in provider_url:
                provider = GitHub(namespace, project, url=provider_url)
            elif "gitlab" in provider_url:
                provider = GitLab(namespace, project, url=provider_url)
            self.remote_url: str = remote_url
        self.provider: ProviderRefParser = provider

        # set style
        if isinstance(style, str):
            try:
                style = self.STYLE[style]()
            except KeyError:
                print("git-changelog: no such style available: %s, " "using default style" % style, file=sys.stderr)
                style = BasicStyle()
        elif style is None:
            style = BasicStyle()
        elif issubclass(style, CommitStyle):
            style = style()
        elif isinstance(style, CommitStyle):
            pass
        self.style: CommitStyle = style

        # get git log and parse it into list of commits
        self.raw_log: str = self.get_log()
        self.commits: List[Commit] = self.parse_commits()

        # apply dates to commits and group them by version
        dates = self.apply_versions_to_commits()
        versions = self.group_commits_by_version(dates)
        self.versions_list: List[Version] = versions["as_list"]
        self.versions_dict: Dict[str, Version] = versions["as_dict"]

        # guess the next version number based on last version and recent commits
        last_version = self.versions_list[0]
        if not last_version.tag and last_version.previous_version:
            last_tag = last_version.previous_version.tag
            major = minor = False
            for commit in last_version.commits:
                if commit.style["is_major"]:
                    major = True
                    break
                elif commit.style["is_minor"]:
                    minor = True
            if major:
                planned_tag = bump(last_tag, "major")
            elif minor:
                planned_tag = bump(last_tag, "minor")
            else:
                planned_tag = bump(last_tag, "patch")
            last_version.planned_tag = planned_tag
            last_version.url = self.provider.get_tag_url(tag=planned_tag)
            last_version.compare_url = self.provider.get_compare_url(
                base=last_version.previous_version.tag, target=last_version.planned_tag
            )

    def get_remote_url(self) -> str:
        git_url = (
            check_output(["git", "config", "--get", "remote.origin.url"], cwd=self.repository)  # nosec
            .decode("utf-8")
            .rstrip("\n")
        )
        if git_url.startswith("git@"):
            git_url = git_url.replace(":", "/", 1).replace("git@", "https://", 1)
        if git_url.endswith(".git"):
            git_url = git_url[:-4]
        return git_url

    def get_log(self) -> str:
        return check_output(
            ["git", "log", "--date=unix", "--format=" + self.FORMAT], cwd=self.repository  # nosec
        ).decode("utf-8")

    def parse_commits(self) -> List[Commit]:
        lines = self.raw_log.split("\n")
        size = len(lines) - 1  # don't count last blank line
        commits = []
        pos = 0
        while pos < size:
            commit = Commit(
                hash=lines[pos],
                author_name=lines[pos + 1],
                author_email=lines[pos + 2],
                author_date=lines[pos + 3],
                committer_name=lines[pos + 4],
                committer_email=lines[pos + 5],
                committer_date=lines[pos + 6],
                refs=lines[pos + 7],
                subject=lines[pos + 8],
                body=[lines[pos + 9]],
            )

            # append body lines
            nbl_index = 10
            while lines[pos + nbl_index] != self.MARKER:
                commit.body.append(lines[pos + nbl_index])
                nbl_index += 1
            pos += nbl_index + 1

            # expand commit object with provider parsing
            if self.provider:
                commit.update_with_provider(self.provider)

            elif self.remote_url:
                # set the commit url based on remote_url (could be wrong)
                commit.url = self.remote_url + "/commit/" + commit.hash

            # expand commit object with style parsing
            if self.style:
                commit.update_with_style(self.style)

            commits.append(commit)

        return commits

    def apply_versions_to_commits(self) -> Dict[str, date_type]:
        versions_dates = {"": None}
        version = None
        for commit in self.commits:
            if commit.version:
                version = commit.version
                versions_dates[version] = commit.committer_date.date()
            elif version:
                commit.version = version
        return versions_dates

    def group_commits_by_version(self, dates: Dict[str, date_type]):
        versions_list = []
        versions_dict = {}
        versions_types_dict = {}
        next_version = None
        for commit in self.commits:
            if commit.version not in versions_dict:
                version = versions_dict[commit.version] = Version(tag=commit.version, date=dates[commit.version])
                version.url = self.provider.get_tag_url(tag=commit.version)
                if next_version:
                    version.next_version = next_version
                    next_version.previous_version = version
                    next_version.compare_url = self.provider.get_compare_url(
                        base=version.tag, target=next_version.tag or "HEAD"
                    )
                next_version = version
                versions_list.append(version)
                versions_types_dict[commit.version] = {}
            versions_dict[commit.version].commits.append(commit)
            if "type" in commit.style and commit.style["type"] not in versions_types_dict[commit.version]:
                section = versions_types_dict[commit.version][commit.style["type"]] = Section(type=commit.style["type"])
                versions_dict[commit.version].sections_list.append(section)
                versions_dict[commit.version].sections_dict = versions_types_dict[commit.version]
            versions_types_dict[commit.version][commit.style["type"]].commits.append(commit)
        if next_version is not None:
            next_version.compare_url = self.provider.get_compare_url(
                base=versions_list[-1].commits[-1].hash, target=next_version.tag or "HEAD"
            )
        return {"as_list": versions_list, "as_dict": versions_dict}
