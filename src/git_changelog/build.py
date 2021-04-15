"""The module responsible for building the data."""

import datetime
import sys
from subprocess import check_output  # noqa: S404 (we trust the commands we run)
from typing import Dict, List, Optional, Tuple, Type, Union

from semver import VersionInfo

from git_changelog.commit import AngularStyle, AtomStyle, BasicStyle, Commit, CommitStyle, ConventionalCommitStyle
from git_changelog.providers import GitHub, GitLab, ProviderRefParser

StyleType = Optional[Union[str, CommitStyle, Type[CommitStyle]]]


def bump(version: str, part: str = "patch") -> str:  # noqa: WPS231
    """
    Bump a version.

    Arguments:
        version: The version to bump.
        part: The part of the version to bump (major, minor, or patch).

    Returns:
        The bumped version.
    """
    prefix = ""
    if version[0] == "v":
        prefix = "v"
        version = version[1:]

    semver_version = VersionInfo.parse(version)
    if part == "major" and semver_version.major != 0:
        semver_version.bump_major()
    elif part == "minor" or (part == "major" and semver_version.major == 0):
        semver_version.bump_minor()
    elif part == "patch" and not semver_version.prerelease:
        semver_version.bump_patch()
    return prefix + str(semver_version)


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
        date: Optional[datetime.date] = None,
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
        self.sections_dict: Dict[str, Section] = {section.type: section for section in self.sections_list}
        self.commits: List[Commit] = commits or []
        self.url: str = url
        self.compare_url: str = compare_url
        self.previous_version: Union[Version, None] = None
        self.next_version: Union[Version, None] = None
        self.planned_tag: Optional[str] = None

    @property
    def typed_sections(self) -> List[Section]:
        """Return typed sections only.

        Returns:
            The typed sections.
        """
        return [section for section in self.sections_list if section.type]

    @property
    def untyped_section(self) -> Optional[Section]:
        """Return untyped section if any.

        Returns:
            The untyped section if any.
        """
        return self.sections_dict.get("", None)

    @property
    def is_major(self) -> bool:
        """Tell if this version is a major one.

        Returns:
            Whether this version is major.
        """
        return self.tag.split(".", 1)[1].startswith("0.0")

    @property
    def is_minor(self) -> bool:
        """Tell if this version is a minor one.

        Returns:
            Whether this version is minor.
        """
        return bool(self.tag.split(".", 2)[2])


class Changelog:
    """The main changelog class."""

    MARKER: str = "--GIT-CHANGELOG MARKER--"
    FORMAT: str = (
        r"%H%n"  # commit commit_hash  # noqa: WPS323
        r"%an%n"  # author name
        r"%ae%n"  # author email
        r"%ad%n"  # author date
        r"%cn%n"  # committer name
        r"%ce%n"  # committer email
        r"%cd%n"  # committer date
        r"%D%n"  # tag
        r"%s%n"  # subject
        r"%b%n" + MARKER  # body
    )
    STYLE: Dict[str, Type[CommitStyle]] = {
        "basic": BasicStyle,
        "angular": AngularStyle,
        "atom": AtomStyle,
        "conventional": ConventionalCommitStyle,
    }

    def __init__(  # noqa: WPS231
        self,
        repository: str,
        provider: Optional[ProviderRefParser] = None,
        style: StyleType = None,
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
                print(f"git-changelog: no such style available: {style}, using default style", file=sys.stderr)
                style = BasicStyle()
        elif style is None:
            style = BasicStyle()
        elif not isinstance(style, CommitStyle) and issubclass(style, CommitStyle):
            style = style()
        self.style: CommitStyle = style

        # get git log and parse it into list of commits
        self.raw_log: str = self.get_log()
        self.commits: List[Commit] = self.parse_commits()

        # apply dates to commits and group them by version
        dates = self.apply_versions_to_commits()
        v_list, v_dict = self.group_commits_by_version(dates)
        self.versions_list = v_list
        self.versions_dict = v_dict

        # guess the next version number based on last version and recent commits
        last_version = self.versions_list[0]
        if not last_version.tag and last_version.previous_version:
            last_tag = last_version.previous_version.tag
            major = minor = False  # noqa: WPS429
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

    def run_git(self, *args) -> str:
        """Run a git command in the chosen repository.

        Arguments:
            *args: Arguments passed to the git command.

        Returns:
            The git command output.
        """
        return check_output(["git", *args], cwd=self.repository).decode("utf8")  # noqa: S603,S607

    def get_remote_url(self) -> str:  # noqa: WPS615
        """Get the git remote URL for the repository.

        Returns:
            The origin remote URL.
        """
        git_url = self.run_git("config", "--get", "remote.origin.url").rstrip("\n")
        if git_url.startswith("git@"):
            git_url = git_url.replace(":", "/", 1).replace("git@", "https://", 1)
        if git_url.endswith(".git"):
            git_url = git_url[:-4]
        return git_url

    def get_log(self) -> str:
        """Get the `git log` output.

        Returns:
            The output of the `git log` command, with a particular format.
        """
        return self.run_git("log", "--date=unix", "--format=" + self.FORMAT)

    def parse_commits(self) -> List[Commit]:
        """Parse the output of 'git log' into a list of commits.

        Returns:
            The list of commits.
        """
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

    def apply_versions_to_commits(self) -> Dict[str, datetime.date]:
        """Iterate on the commits to apply them a date.

        Returns:
            A dictionary with versions as keys and dates as values.
        """
        versions_dates = {"": datetime.date.today()}
        version = None
        for commit in self.commits:
            if commit.version:
                version = commit.version
                versions_dates[version] = commit.committer_date.date()
            elif version:
                commit.version = version
        return versions_dates

    def group_commits_by_version(  # noqa: WPS231
        self, dates: Dict[str, datetime.date]
    ) -> Tuple[List[Version], Dict[str, Version]]:
        """Iterate on commits to group them by version.

        Arguments:
            dates: A dictionary with versions as keys and their dates as values.

        Returns:
            A tuple containing the versions as a list and the versions as a dictionary.
        """
        versions_list = []
        versions_dict = {}
        versions_types_dict: Dict[str, Dict[str, Section]] = {}
        next_version = None
        for commit in self.commits:
            if commit.version not in versions_dict:
                version = Version(tag=commit.version, date=dates[commit.version])
                versions_dict[commit.version] = version
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
                section = Section(section_type=commit.style["type"])
                versions_types_dict[commit.version][commit.style["type"]] = section
                versions_dict[commit.version].sections_list.append(section)
                versions_dict[commit.version].sections_dict = versions_types_dict[commit.version]
            versions_types_dict[commit.version][commit.style["type"]].commits.append(commit)
        if next_version is not None and self.provider:
            next_version.compare_url = self.provider.get_compare_url(
                base=versions_list[-1].commits[-1].hash, target=next_version.tag or "HEAD"
            )
        return versions_list, versions_dict
