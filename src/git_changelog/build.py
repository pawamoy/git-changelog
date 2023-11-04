"""The module responsible for building the data."""

from __future__ import annotations

import datetime
import os
import sys
import warnings
from subprocess import CalledProcessError, check_output
from typing import TYPE_CHECKING, ClassVar, Literal, Type, Union
from urllib.parse import urlsplit, urlunsplit

from semver import VersionInfo

from git_changelog.commit import (
    AngularConvention,
    BasicConvention,
    Commit,
    CommitConvention,
    ConventionalCommitConvention,
)
from git_changelog.providers import Bitbucket, GitHub, GitLab, ProviderRefParser

if TYPE_CHECKING:
    from pathlib import Path

ConventionType = Union[str, CommitConvention, Type[CommitConvention]]


def bump(version: str, part: Literal["major", "minor", "patch"] = "patch", *, zerover: bool = True) -> str:
    """Bump a version.

    Arguments:
        version: The version to bump.
        part: The part of the version to bump (major, minor, or patch).
        zerover: Keep major version at zero, even for breaking changes.

    Returns:
        The bumped version.
    """
    prefix = ""
    if version[0] == "v":
        prefix = "v"
        version = version[1:]

    semver_version = VersionInfo.parse(version)
    if part == "major" and (semver_version.major != 0 or not zerover):
        semver_version = semver_version.bump_major()
    elif part == "minor" or (part == "major" and semver_version.major == 0):
        semver_version = semver_version.bump_minor()
    elif part == "patch" and not semver_version.prerelease:
        semver_version = semver_version.bump_patch()
    return prefix + str(semver_version)


class Section:
    """A list of commits grouped by section_type."""

    def __init__(self, section_type: str = "", commits: list[Commit] | None = None):
        """Initialization method.

        Arguments:
            section_type: The section section_type.
            commits: The list of commits.
        """
        self.type: str = section_type
        self.commits: list[Commit] = commits or []


class Version:
    """A class to represent a changelog version."""

    def __init__(
        self,
        tag: str = "",
        date: datetime.date | None = None,
        sections: list[Section] | None = None,
        commits: list[Commit] | None = None,
        url: str = "",
        compare_url: str = "",
    ):
        """Initialization method.

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

        self.sections_list: list[Section] = sections or []
        self.sections_dict: dict[str, Section] = {section.type: section for section in self.sections_list}
        self.commits: list[Commit] = commits or []
        self.url: str = url
        self.compare_url: str = compare_url
        self.previous_version: Version | None = None
        self.next_version: Version | None = None
        self.planned_tag: str | None = None

    @property
    def typed_sections(self) -> list[Section]:
        """Return typed sections only.

        Returns:
            The typed sections.
        """
        return [section for section in self.sections_list if section.type]

    @property
    def untyped_section(self) -> Section | None:
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

    MARKER: ClassVar[str] = "--GIT-CHANGELOG MARKER--"
    FORMAT: ClassVar[str] = (
        r"%H%n"  # commit commit_hash
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
    CONVENTION: ClassVar[dict[str, type[CommitConvention]]] = {
        "basic": BasicConvention,
        "angular": AngularConvention,
        "conventional": ConventionalCommitConvention,
    }

    def __init__(
        self,
        repository: str | Path,
        *,
        provider: ProviderRefParser | type[ProviderRefParser] | None = None,
        convention: ConventionType | None = None,
        parse_provider_refs: bool = False,
        parse_trailers: bool = False,
        sections: list[str] | None = None,
        bump_latest: bool = False,
        bump: str | None = None,
        zerover: bool = True,
        filter_commits: str | None = None,
    ):
        """Initialization method.

        Arguments:
            repository: The repository (directory) for which to build the changelog.
            provider: The provider to use (github.com, gitlab.com, etc.).
            convention: The commit convention to use (angular, etc.).
            parse_provider_refs: Whether to parse provider-specific references in the commit messages.
            parse_trailers: Whether to parse Git trailers in the commit messages.
            sections: The sections to render (features, bug fixes, etc.).
            bump_latest: Deprecated, use `bump="auto"` instead. Whether to try and bump latest version to guess new one.
            bump: Whether to try and bump to a given version.
            zerover: Keep major version at zero, even for breaking changes.
            filter_commits: The Git revision-range used to filter commits in git-log (e.g: `v1.0.1..`).
        """
        self.repository: str | Path = repository
        self.parse_provider_refs: bool = parse_provider_refs
        self.parse_trailers: bool = parse_trailers
        self.zerover: bool = zerover
        self.filter_commits: str | None = filter_commits

        # set provider
        if not isinstance(provider, ProviderRefParser):
            remote_url = self.get_remote_url()
            split = remote_url.split("/")
            provider_url = "/".join(split[:3])
            namespace, project = "/".join(split[3:-1]), split[-1]
            if callable(provider):
                provider = provider(namespace, project, url=provider_url)
            elif "github" in provider_url:
                provider = GitHub(namespace, project, url=provider_url)
            elif "gitlab" in provider_url:
                provider = GitLab(namespace, project, url=provider_url)
            elif "bitbucket" in provider_url:
                provider = Bitbucket(namespace, project, url=provider_url)
            else:
                provider = None
            self.remote_url: str = remote_url
        self.provider = provider

        # set convention
        if isinstance(convention, str):
            try:
                convention = self.CONVENTION[convention]()
            except KeyError:
                print(  # noqa: T201
                    f"git-changelog: no such convention available: {convention}, using default convention",
                    file=sys.stderr,
                )
                convention = BasicConvention()
        elif convention is None:
            convention = BasicConvention()
        elif not isinstance(convention, CommitConvention) and issubclass(convention, CommitConvention):
            convention = convention()
        self.convention: CommitConvention = convention

        # set sections
        sections = (
            [self.convention.TYPES[section] for section in sections] if sections else self.convention.DEFAULT_RENDER
        )
        self.sections = sections

        # get git log and parse it into list of commits
        self.raw_log: str = self.get_log()
        self.commits: list[Commit] = self.parse_commits()

        # apply dates to commits and group them by version
        dates = self._apply_versions_to_commits()
        v_list, v_dict = self._group_commits_by_version(dates)
        self.versions_list = v_list
        self.versions_dict = v_dict

        # TODO: remove at some point
        if bump_latest:
            warnings.warn(
                "`bump_latest=True` is deprecated in favor of `bump='auto'`",
                DeprecationWarning,
                stacklevel=1,
            )
            if bump is None:
                bump = "auto"
        if bump:
            self._bump(bump)

        # fix a single, initial version to 0.1.0
        self._fix_single_version()

    def run_git(self, *args: str) -> str:
        """Run a git command in the chosen repository.

        Arguments:
            *args: Arguments passed to the git command.

        Returns:
            The git command output.
        """
        return check_output(["git", *args], cwd=self.repository).decode("utf8")  # noqa: S603,S607

    def get_remote_url(self) -> str:
        """Get the git remote URL for the repository.

        Returns:
            The origin remote URL.
        """
        remote = "remote." + os.environ.get("GIT_CHANGELOG_REMOTE", "origin") + ".url"
        git_url = self.run_git("config", "--get", remote).rstrip("\n")
        if git_url.startswith("git@"):
            git_url = git_url.replace(":", "/", 1).replace("git@", "https://", 1)
        if git_url.endswith(".git"):
            git_url = git_url[:-4]

        # Remove credentials from the URL.
        if git_url.startswith(("http://", "https://")):
            # (addressing scheme, network location, path, query, fragment identifier)
            urlparts = list(urlsplit(git_url))
            urlparts[1] = urlparts[1].split("@", 1)[-1]
            git_url = urlunsplit(urlparts)

        return git_url

    def get_log(self) -> str:
        """Get the `git log` output.

        Returns:
            The output of the `git log` command, with a particular format.
        """
        if self.filter_commits:
            try:
                return self.run_git("log", "--date=unix", "--format=" + self.FORMAT, self.filter_commits)
            except CalledProcessError as e:
                raise ValueError(
                    f"An error ocurred. Maybe the provided git-log revision-range is not valid: '{self.filter_commits}'",
                ) from e

        # No revision-range provided. Call normally
        return self.run_git("log", "--date=unix", "--format=" + self.FORMAT)

    def parse_commits(self) -> list[Commit]:
        """Parse the output of 'git log' into a list of commits.

        Returns:
            The list of commits.
        """
        lines = self.raw_log.split("\n")
        size = len(lines) - 1  # don't count last blank line
        commits = []
        pos = 0
        while pos < size:
            # build body
            nbl_index = 9
            body = []
            while lines[pos + nbl_index] != self.MARKER:
                body.append(lines[pos + nbl_index].strip("\r"))
                nbl_index += 1

            # build commit
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
                body=body,
                parse_trailers=self.parse_trailers,
            )

            pos += nbl_index + 1

            # expand commit object with provider parsing
            if self.provider:
                commit.update_with_provider(self.provider, parse_refs=self.parse_provider_refs)

            # set the commit url based on remote_url (could be wrong)
            elif self.remote_url:
                commit.url = self.remote_url + "/commit/" + commit.hash

            # expand commit object with convention parsing
            if self.convention:
                commit.update_with_convention(self.convention)

            commits.append(commit)

        return commits

    def _apply_versions_to_commits(self) -> dict[str, datetime.date]:
        versions_dates = {"": datetime.date.today()}  # noqa: DTZ011
        version = None
        for commit in self.commits:
            if commit.version:
                version = commit.version
                versions_dates[version] = commit.committer_date.date()
            elif version:
                commit.version = version
        return versions_dates

    def _group_commits_by_version(
        self,
        dates: dict[str, datetime.date],
    ) -> tuple[list[Version], dict[str, Version]]:
        versions_list = []
        versions_dict = {}
        versions_types_dict: dict[str, dict[str, Section]] = {}
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
                            base=version.tag,
                            target=next_version.tag or "HEAD",
                        )
                next_version = version
                versions_list.append(version)
                versions_types_dict[commit.version] = {}
            versions_dict[commit.version].commits.append(commit)
            if "type" in commit.convention and commit.convention["type"] not in versions_types_dict[commit.version]:
                section = Section(section_type=commit.convention["type"])
                versions_types_dict[commit.version][commit.convention["type"]] = section
                versions_dict[commit.version].sections_list.append(section)
                versions_dict[commit.version].sections_dict = versions_types_dict[commit.version]
            versions_types_dict[commit.version][commit.convention["type"]].commits.append(commit)
        if next_version is not None and self.provider:
            next_version.compare_url = self.provider.get_compare_url(
                base=versions_list[-1].commits[-1].hash,
                target=next_version.tag or "HEAD",
            )
        return versions_list, versions_dict

    def _bump(self, version: str) -> None:
        last_version = self.versions_list[0]
        if not last_version.tag and last_version.previous_version:
            last_tag = last_version.previous_version.tag
            if version == "auto":
                # guess the next version number based on last version and recent commits
                version = "patch"
                for commit in last_version.commits:
                    if commit.convention["is_major"]:
                        version = "major"
                        break
                    if commit.convention["is_minor"]:
                        version = "minor"
            if version in {"major", "minor", "patch"}:
                # bump version (don't fail on non-semver versions)
                try:
                    last_version.planned_tag = bump(last_tag, version, zerover=self.zerover)  # type: ignore[arg-type]
                except ValueError:
                    return
            else:
                # user specified version
                last_version.planned_tag = version
            # update URLs
            if self.provider:
                last_version.url = self.provider.get_tag_url(tag=last_version.planned_tag)
                last_version.compare_url = self.provider.get_compare_url(
                    base=last_version.previous_version.tag,
                    target=last_version.planned_tag,
                )

    def _fix_single_version(self) -> None:
        last_version = self.versions_list[0]
        if len(self.versions_list) == 1 and last_version.planned_tag is None:
            planned_tag = "0.1.0"
            last_version.tag = planned_tag
            last_version.url += planned_tag
            last_version.compare_url = last_version.compare_url.replace("HEAD", planned_tag)
