# The module responsible for building the data.

from __future__ import annotations

import datetime
import os
import sys
import warnings
from subprocess import CalledProcessError, check_output
from typing import TYPE_CHECKING, ClassVar, Literal, Union
from urllib.parse import urlsplit, urlunsplit

from git_changelog._internal.commit import (
    AngularConvention,
    BasicConvention,
    Commit,
    CommitConvention,
    ConventionalCommitConvention,
)
from git_changelog._internal.providers import Bitbucket, GitHub, GitLab, ProviderRefParser
from git_changelog._internal.versioning import ParsedVersion, bump_pep440, bump_semver, parse_pep440, parse_semver

if TYPE_CHECKING:
    from pathlib import Path

    from git_changelog._internal.versioning import SemVerVersion

ConventionType = Union[str, CommitConvention, type[CommitConvention]]
"""The type of convention used for commits."""


# YORE: Bump 3: Remove block.
def bump(version: str, part: Literal["major", "minor", "patch"] = "patch", *, zerover: bool = True) -> str:
    """Bump a version. Deprecated, use [`bump_semver`][git_changelog.bump_semver] instead.

    Parameters:
        version: The version to bump.
        part: The part of the version to bump (major, minor, or patch).
        zerover: Keep major version at zero, even for breaking changes.

    Returns:
        The bumped version.
    """
    warnings.warn(
        "This function is deprecated in favor of `git_changelog.versioning.bump_semver`",
        DeprecationWarning,
        stacklevel=2,
    )
    return bump_semver(version, part, zerover=zerover)


# YORE: Bump 3: Remove block.
def parse_version(version: str) -> tuple[SemVerVersion, str]:
    """Parse a version. Deprecated, use [`bump_semver`][git_changelog.parse_semver] instead.

    Parameters:
        version: The version to parse.

    Returns:
        semver_version: The semantic version.
        prefix: The version prefix.
    """
    warnings.warn(
        "This function is deprecated in favor of `git_changelog.versioning.parse_semver`",
        DeprecationWarning,
        stacklevel=2,
    )
    return parse_semver(version)


class Section:
    """A list of commits grouped by section_type."""

    def __init__(self, section_type: str = "", commits: list[Commit] | None = None):
        """Initialization method.

        Parameters:
            section_type: The section section_type.
            commits: The list of commits.
        """
        self.type: str = section_type
        """The section type."""
        self.commits: list[Commit] = commits or []
        """The list of commits."""


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

        Parameters:
            tag: The version tag.
            date: The version date.
            sections: The version sections.
            commits: The version commits.
            url: The version URL.
            compare_url: The version 'compare' URL.
        """
        self.tag = tag
        """The version tag."""
        self.date = date
        """The version date."""

        self.sections_list: list[Section] = sections or []
        """The version sections (list)."""
        self.sections_dict: dict[str, Section] = {section.type: section for section in self.sections_list}
        """The version sections (dict)."""
        self.commits: list[Commit] = commits or []
        """The version commits."""
        self.url: str = url
        """The version URL."""
        self.compare_url: str = compare_url
        """The version 'compare' URL."""
        self.previous_version: Version | None = None
        """The previous version."""
        self.next_version: Version | None = None
        """The next version."""
        self.planned_tag: str | None = None
        """The planned version tag."""

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

    def add_commit(self, commit: Commit) -> None:
        """Register the given commit and add it to the relevant section based on its message convention.

        Parameters:
            commit: The git commit.
        """
        self.commits.append(commit)
        commit.version = self.tag or "HEAD"
        commit_type: str = commit.convention.get("type")  # type: ignore[assignment]
        if commit_type not in self.sections_dict:
            section = Section(section_type=commit_type)
            self.sections_list.append(section)
            self.sections_dict[commit_type] = section
        self.sections_dict[commit_type].commits.append(commit)


class Changelog:
    """The main changelog class."""

    MARKER: ClassVar[str] = "--GIT-CHANGELOG MARKER--"
    """Marker for the changelog."""
    FORMAT: ClassVar[str] = (
        r"%H%n"  # commit commit_hash
        r"%an%n"  # author name
        r"%ae%n"  # author email
        r"%ad%n"  # author date
        r"%cn%n"  # committer name
        r"%ce%n"  # committer email
        r"%cd%n"  # committer date
        r"%D%n"  # tag
        r"%P%n"  # parent hashes
        r"%s%n"  # subject
        r"%b%n" + MARKER  # body
    )
    """Format string for the changelog."""
    CONVENTION: ClassVar[dict[str, type[CommitConvention]]] = {
        "basic": BasicConvention,
        "angular": AngularConvention,
        "conventional": ConventionalCommitConvention,
    }
    """Available commit message conventions."""

    def __init__(
        self,
        repository: str | Path,
        *,
        provider: ProviderRefParser | type[ProviderRefParser] | None = None,
        convention: ConventionType | None = None,
        parse_provider_refs: bool = False,
        parse_trailers: bool = False,
        sections: list[str] | None = None,
        # YORE: Bump 3: Remove line.
        bump_latest: bool = False,
        bump: str | None = None,
        zerover: bool = True,
        filter_commits: str | None = None,
        versioning: Literal["semver", "pep440"] = "semver",
    ):
        """Initialization method.

        Parameters:
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
        """The repository (directory) for which to build the changelog."""
        self.parse_provider_refs: bool = parse_provider_refs
        """Whether to parse provider-specific references in the commit messages."""
        self.parse_trailers: bool = parse_trailers
        """Whether to parse Git trailers in the commit messages."""
        self.zerover: bool = zerover
        """Whether to keep major version at zero, even for breaking changes."""
        self.filter_commits: str | None = filter_commits
        """The Git revision-range used to filter commits in git-log (e.g: `v1.0.1..`)."""

        # Set provider.
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
            """The remote URL of the repository."""
        self.provider = provider
        """The provider to use (github.com, gitlab.com, etc.)."""

        # Set convention.
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
        """The commit convention to use."""

        # Set sections.
        if sections and ":all:" in sections:
            # Expand :all: to all available section types
            sections = list(self.convention.TYPES.values())
        elif sections:
            sections = [self.convention.TYPES[section] for section in sections]
        else:
            sections = self.convention.DEFAULT_RENDER
        self.sections = sections
        """The sections to include in the changelog."""

        # Get version parser based on selected versioning scheme.
        version_parser, version_bumper = {
            "semver": (parse_semver, bump_semver),
            "pep440": (parse_pep440, bump_pep440),
        }[versioning]
        self.version_parser = version_parser
        """The version parser function."""
        self.version_bumper = version_bumper
        """The version bumper function."""

        # Get git log and parse it into list of commits.
        self.raw_log: str = self.get_log()
        """The raw Git log output."""
        self.commits: list[Commit] = self.parse_commits()
        """The list of parsed commits."""
        self.tag_commits: list[Commit] = [commit for commit in self.commits[1:] if commit.tag]
        """The list of tagged commits."""
        self.tag_commits.insert(0, self.commits[0])

        # Apply dates to commits and group them by version.
        v_list, v_dict = self._group_commits_by_version()
        self.versions_list = v_list
        """The list of versions."""
        self.versions_dict = v_dict
        """The dictionary of versions."""

        # YORE: Bump 3: Remove block.
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

    def run_git(self, *args: str) -> str:
        """Run a git command in the chosen repository.

        Parameters:
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
        git_url = self.run_git("config", "--default", "", "--get", remote).rstrip("\n")
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

        The commits build a Git commit graph by referencing their parent commits.
        Commits are ordered from newest to oldest.

        Returns:
            The list of commits.
        """
        lines = self.raw_log.split("\n")
        size = len(lines) - 1  # Don't count last blank line.
        pos = 0

        commits_map: dict[str, Commit] = {}

        while pos < size:
            # Build message body.
            nbl_index = 10
            body = []
            while lines[pos + nbl_index] != self.MARKER:
                body.append(lines[pos + nbl_index].strip("\r"))
                nbl_index += 1

            # Build commit object.
            commit = Commit(
                commit_hash=lines[pos],
                author_name=lines[pos + 1],
                author_email=lines[pos + 2],
                author_date=lines[pos + 3],
                committer_name=lines[pos + 4],
                committer_email=lines[pos + 5],
                committer_date=lines[pos + 6],
                refs=lines[pos + 7],
                parent_hashes=lines[pos + 8],
                commits_map=commits_map,
                subject=lines[pos + 9],
                body=body,
                parse_trailers=self.parse_trailers,
                version_parser=self.version_parser,
            )

            pos += nbl_index + 1

            # Expand commit object with provider parsing.
            if self.provider:
                commit.update_with_provider(self.provider, parse_refs=self.parse_provider_refs)

            # Set the commit url based on remote_url (could be wrong).
            elif self.remote_url:
                commit.url = self.remote_url + "/commit/" + commit.hash

            # Expand commit object with convention parsing.
            if self.convention:
                commit.update_with_convention(self.convention)

            commits_map[commit.hash] = commit

        return list(commits_map.values())

    def _group_commits_by_version(self) -> tuple[list[Version], dict[str, Version]]:
        """Group commits into versions.

        Commits are assigned to the version they were first released with.
        A commit is assigned to exactly one version.

        Returns:
            versions_list: The list of versions order descending by timestamp.
            versions_dict: A dictionary of versions with the tag name as keys.
        """
        versions_dict: dict[str, Version] = {}
        versions_list: list[Version] = []
        previous_versions: dict[str, str] = {}

        # Iterate in reversed order (oldest to newest tag) to assign commits to the first version they were released with.
        for tag_commit in reversed(self.tag_commits):
            # Create new version object.
            version = self._create_version(tag_commit)
            versions_dict[tag_commit.version] = version
            versions_list.insert(0, version)

            # Find all commits for this version by following the commit graph.
            version.add_commit(tag_commit)
            previous_parsed_version: ParsedVersion | None = None
            next_commits = tag_commit.parent_commits  # Always new: we can mutate it.
            while next_commits:
                next_commit = next_commits.pop(0)
                if next_commit.tag:
                    parsed_version, _ = self.version_parser(next_commit.tag)
                    if not previous_parsed_version or parsed_version > previous_parsed_version:
                        previous_parsed_version = parsed_version
                        previous_versions[version.tag] = next_commit.tag
                elif not next_commit.version:
                    version.add_commit(next_commit)
                    next_commits.extend(next_commit.parent_commits)

        self._assign_previous_versions(versions_dict, previous_versions)
        return versions_list, versions_dict

    def _create_version(self, commit: Commit) -> Version:
        date = commit.committer_date.date() if commit.version else datetime.date.today()  # noqa: DTZ011
        version = Version(tag=commit.version, date=date)
        if self.provider:
            version.url = self.provider.get_tag_url(tag=commit.version)
        return version

    def _assign_previous_versions(self, versions_dict: dict[str, Version], previous_versions: dict[str, str]) -> None:
        """Assign each version its previous version and create the compare URL.

        The previous version is defined as the version with the highest semantic version,
        that is found by following the commit graph.

        If no previous version is found, either because it is the first commit or
        due to the commit filter excluding it, the compare URL is created with the
        first commit (oldest).

        Parameters:
            versions_dict: A dictionary of versions with the tag name as keys.
            previous_versions: A dictonary with version and previous version.
        """
        for version in versions_dict.values():
            previous_version = previous_versions.get(version.tag, version.commits[-1].hash)
            version.previous_version = versions_dict.get(previous_version)
            if version.previous_version:
                version.previous_version.next_version = version
            if self.provider:
                version.compare_url = self.provider.get_compare_url(
                    base=previous_version,
                    target=version.tag or "HEAD",
                )

    def _bump(self, version: str) -> None:
        last_version = self.versions_list[0]
        if not last_version.tag:
            if last_version.previous_version:
                last_tag = last_version.previous_version.tag
            else:
                last_tag = self.version_bumper.initial
            version, *plus = version.split("+")
            if version == "auto":
                # Guess the next version number based on last version and recent commits.
                version = "patch"
                for commit in last_version.commits:
                    if commit.convention["is_major"]:
                        version = "major"
                        break
                    if commit.convention["is_minor"]:
                        version = "minor"
            version = "+".join((version, *plus))
            if version in self.version_bumper.strategies:
                # Bump version.
                last_version.planned_tag = self.version_bumper(last_tag, version, zerover=self.zerover)
            else:
                # user specified version
                try:
                    self.version_bumper(version)
                except ValueError as error:
                    raise ValueError(f"{error}; typo in bumping strategy? Check the CLI help and our docs") from error
                last_version.planned_tag = version
            # Update URLs.
            if self.provider:
                last_version.url = self.provider.get_tag_url(tag=last_version.planned_tag)
                last_version.compare_url = self.provider.get_compare_url(
                    base=last_version.previous_version.tag
                    if last_version.previous_version
                    else last_version.commits[-1].hash,
                    target=last_version.planned_tag,
                )
