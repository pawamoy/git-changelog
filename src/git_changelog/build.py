"""The module responsible for building the data."""

import sys
from datetime import date
from subprocess import check_output  # noqa: S404 (we trust the commands we run)
from typing import Dict, List, Optional, Type, Union

from git_changelog.commit import AngularStyle, AtomStyle, BasicStyle, Commit, CommitStyle
from git_changelog.providers import GitHub, GitLab, ProviderRefParser


def bump(version: str, part: str = "patch") -> str:
    """
    Bump a version.

    Arguments:
        version: The version to bump.
        part: The part of the version to bump (major, minor, or patch).

    Return:
        The bumped version.
    """
    major, minor, patch = version.split(".", 2)
    prefix = ""
    if major[0] == "v":
        prefix = "v"
        major = major[1:]
    patch_parts = patch.split("-", 1)
    pre = ""
    if len(patch_parts) > 1:
        patch, pre = patch_parts
    else:
        patch = patch_parts[0]
    if part == "major" and major != "0":
        major = str(int(major) + 1)
        minor = patch = "0"
    elif part == "minor" or (part == "major" and major == "0"):
        minor = str(int(minor) + 1)
        patch = "0"
    elif part == "patch" and not pre:
        patch = str(int(patch) + 1)
    return prefix + ".".join((major, minor, patch))


class Section:
    """A list of commits grouped by section_type."""

    def __init__(self, section_type: str = "", commits: List[Commit] = None):
        """
        Initialization method.

        Arguments:
            section_type: The section section_type.
            commits: The list of commits.
        """
        self.type: str = section_type
        self.commits: List[Commit] = commits or []


class Version:
    """A class to represent a changelog version."""

    def __init__(
        self,
        tag: str = "",
        date: Optional[date] = None,
        sections: List[Section] = None,
        commits: List[Commit] = None,
        url: str = "",
        compare_url: str = "",
    ):
        """
        Initialization method.

        Arguments:
            tag: The version tag.
            date: The version date.
            sections: The version sections.
            commits: The version commits.
            url: The version URL.
            compare_url: The version 'compare' URL.
        """
        self.tag = tag
        self.date = date

        self.sections_list: List[Section] = sections or []
        self.sections_dict: Dict[str, Section] = {s.type: s for s in self.sections_list}
        self.commits: List[Commit] = commits or []
        self.url: str = url
        self.compare_url: str = compare_url
        self.previous_version: Union[Version, None] = None
        self.next_version: Union[Version, None] = None
        self.planned_tag: Optional[str] = None

    @property
    def typed_sections(self) -> List[Section]:
        """Typed-only sections."""
        return [s for s in self.sections_list if s.type]

    @property
    def untyped_section(self) -> Optional[Section]:
        """Untyped section."""
        return self.sections_dict.get("", None)

    @property
    def is_major(self) -> bool:
        """Is this version a major one?"""
        return self.tag.split(".", 1)[1].startswith("0.0")

    @property
    def is_minor(self) -> bool:
        """Is this version a minor one?"""
        return bool(self.tag.split(".", 2)[2])


class Changelog:
    """The main changelog class."""

    MARKER: str = "--GIT-CHANGELOG MARKER--"
    FORMAT: str = (
        "%H%n"  # commit commit_hash
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

    def __init__(
        self,
        repository: str,
        provider: Optional[ProviderRefParser] = None,
        style: Optional[Union[str, CommitStyle, Type[CommitStyle]]] = None,
    ):
        """
        Initialization method.

        Arguments:
            repository: The repository (directory) for which to build the changelog.
            provider: The provider to use (github.com, gitlab.com, etc.).
            style: The commit style to use (angular, atom, etc.).
        """
        self.repository: str = repository

        # set provider
        if not provider:
            remote_url = self.get_remote_url()
            split = remote_url.split("/")
            provider_url = "/".join(split[:3])
            namespace, project = "/".join(split[3:-1]), split[-1]
            if "github" in provider_url:
                provider = GitHub(namespace, project, url=provider_url)
            elif "gitlab" in provider_url:
                provider = GitLab(namespace, project, url=provider_url)
            self.remote_url: str = remote_url
        self.provider = provider

        # set style
        if isinstance(style, str):
            try:
                style = self.STYLE[style]()
            except KeyError:
                print("git-changelog: no such style available: %s, " "using default style" % style, file=sys.stderr)
                style = BasicStyle()
        elif style is None:
            style = BasicStyle()
        elif isinstance(style, CommitStyle):
            pass
        elif issubclass(style, CommitStyle):
            style = style()
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
            if self.provider:
                last_version.url = self.provider.get_tag_url(tag=planned_tag)
                last_version.compare_url = self.provider.get_compare_url(
                    base=last_version.previous_version.tag, target=last_version.planned_tag
                )

    def get_remote_url(self) -> str:
        """Get the git remote URL for the repository."""
        git_url = (
            check_output(  # noqa: S603,S607 (we trust the input, we don't want to to find git's absolute path)
                ["git", "config", "--get", "remote.origin.url"], cwd=self.repository
            )
            .decode("utf-8")
            .rstrip("\n")
        )
        if git_url.startswith("git@"):
            git_url = git_url.replace(":", "/", 1).replace("git@", "https://", 1)
        if git_url.endswith(".git"):
            git_url = git_url[:-4]
        return git_url

    def get_log(self) -> str:
        """Get the 'git log' output."""
        return check_output(  # noqa: S603,S607 (we trust the input, we don't want to to find git's absolute path)
            ["git", "log", "--date=unix", "--format=" + self.FORMAT], cwd=self.repository  # nosec
        ).decode("utf-8")

    def parse_commits(self) -> List[Commit]:
        """Parse the output of 'git log' into a list of commits."""
        lines = self.raw_log.split("\n")
        size = len(lines) - 1  # don't count last blank line
        commits = []
        pos = 0
        while pos < size:
            commit = Commit(
                commit_hash=lines[pos],
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

    def apply_versions_to_commits(self) -> Dict[str, date]:
        """Iterate on the commits to apply them a date."""
        versions_dates = {"": date.today()}
        version = None
        for commit in self.commits:
            if commit.version:
                version = commit.version
                versions_dates[version] = commit.committer_date.date()
            elif version:
                commit.version = version
        return versions_dates

    def group_commits_by_version(self, dates: Dict[str, date]):
        """Iterate on commits to group them by version."""
        versions_list = []
        versions_dict = {}
        versions_types_dict: Dict[str, Dict[str, Section]] = {}
        next_version = None
        for commit in self.commits:
            if commit.version not in versions_dict:
                version = versions_dict[commit.version] = Version(tag=commit.version, date=dates[commit.version])
                if self.provider:
                    version.url = self.provider.get_tag_url(tag=commit.version)
                if next_version:
                    version.next_version = next_version
                    next_version.previous_version = version
                    if self.provider:
                        next_version.compare_url = self.provider.get_compare_url(
                            base=version.tag, target=next_version.tag or "HEAD"
                        )
                next_version = version
                versions_list.append(version)
                versions_types_dict[commit.version] = {}
            versions_dict[commit.version].commits.append(commit)
            if "type" in commit.style and commit.style["type"] not in versions_types_dict[commit.version]:
                section = versions_types_dict[commit.version][commit.style["type"]] = Section(
                    section_type=commit.style["type"]
                )
                versions_dict[commit.version].sections_list.append(section)
                versions_dict[commit.version].sections_dict = versions_types_dict[commit.version]
            versions_types_dict[commit.version][commit.style["type"]].commits.append(commit)
        if next_version is not None and self.provider:
            next_version.compare_url = self.provider.get_compare_url(
                base=versions_list[-1].commits[-1].hash, target=next_version.tag or "HEAD"
            )
        return {"as_list": versions_list, "as_dict": versions_dict}
