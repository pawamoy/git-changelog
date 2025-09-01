# Module containing the parsing utilities for git providers.

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from re import Match, Pattern
from typing import ClassVar


class RefRe:
    """An enum helper to store parts of regular expressions for references."""

    BB = r"(?:^|[\s,])"  # blank before
    """Blank before the reference."""
    BA = r"(?:[\s,]|$)"  # blank after
    """Blank after the reference."""
    NP = r"(?:(?P<namespace>[-\w]+)/)?(?P<project>[-\w]+)"  # namespace and project
    """Namespace and project."""
    ID = r"{symbol}(?P<ref>[1-9]\d*)"
    """Issue or pull request ID."""
    ONE_WORD = r"{symbol}(?P<ref>\w*[-a-z_ ][-\w]*)"
    """One word reference."""
    MULTI_WORD = r'{symbol}(?P<ref>"\w[- \w]*")'
    """Multi word reference."""
    COMMIT = r"(?P<ref>[0-9a-f]{{{min},{max}}})"
    """Commit hash."""
    COMMIT_RANGE = r"(?P<ref>[0-9a-f]{{{min},{max}}}\.\.\.[0-9a-f]{{{min},{max}}})"
    """Commit range."""
    MENTION = r"@(?P<ref>\w[-\w]*)"
    """Mention."""


class Ref:
    """A class to represent a reference and its URL."""

    def __init__(self, ref: str, url: str) -> None:
        """Initialization method.

        Arguments:
            ref: The reference text.
            url: The reference URL.
        """
        self.ref: str = ref
        self.url: str = url

    def __str__(self):
        return self.ref + ": " + self.url


class RefDef:
    """A class to store a reference regular expression and URL building string."""

    def __init__(self, regex: Pattern, url_string: str):
        """Initialization method.

        Arguments:
            regex: The regular expression to match the reference.
            url_string: The URL string to format using matched groups.
        """
        self.regex = regex
        self.url_string = url_string


class ProviderRefParser(ABC):
    """A base class for specific providers reference parsers."""

    url: str
    """The base URL for the provider."""
    namespace: str
    """The namespace for the provider."""
    project: str
    """The project for the provider."""
    REF: ClassVar[dict[str, RefDef]] = {}
    """The reference definitions for the provider."""

    def __init__(self, namespace: str, project: str, url: str | None = None):
        """Initialization method.

        Arguments:
            namespace: The Bitbucket namespace.
            project: The Bitbucket project.
            url: The Bitbucket URL.
        """
        self.namespace: str = namespace
        self.project: str = project
        self.url: str = url or self.url

    def get_refs(self, ref_type: str, text: str) -> list[Ref]:
        """Find all references in the given text.

        Arguments:
            ref_type: The reference type.
            text: The text in which to search references.

        Returns:
            A list of references (instances of [Ref][git_changelog.Ref]).
        """
        return [
            Ref(ref=match.group().strip(), url=self.build_ref_url(ref_type, match.groupdict()))
            for match in self.parse_refs(ref_type, text)
        ]

    def parse_refs(self, ref_type: str, text: str) -> list[Match]:
        """Parse references in the given text.

        Arguments:
            ref_type: The reference type.
            text: The text to parse.

        Returns:
            A list of regular expressions matches.
        """
        if ref_type not in self.REF:
            refs = [key for key in self.REF if key.startswith(ref_type)]
            return [match for ref in refs for match in self.REF[ref].regex.finditer(text)]
        return list(self.REF[ref_type].regex.finditer(text))

    def build_ref_url(self, ref_type: str, match_dict: dict[str, str]) -> str:
        """Build the URL for a reference type and a dictionary of matched groups.

        Arguments:
            ref_type: The reference type.
            match_dict: The matched groups.

        Returns:
            The built URL.
        """
        return self.REF[ref_type].url_string.format(**match_dict)

    @abstractmethod
    def get_tag_url(self, tag: str) -> str:
        """Get the URL for a git tag.

        Arguments:
            tag: The git tag.

        Returns:
            The tag URL.
        """
        raise NotImplementedError

    @abstractmethod
    def get_compare_url(self, base: str, target: str) -> str:
        """Get the URL for a tag comparison.

        Arguments:
            base: The base tag.
            target: The target tag.

        Returns:
            The comparison URL.
        """
        raise NotImplementedError


class GitHub(ProviderRefParser):
    """A parser for the GitHub references."""

    url: str = "https://github.com"
    """The base URL for the provider."""
    project_url: str = "{base_url}/{namespace}/{project}"
    """The project URL for the provider."""
    tag_url: str = "{base_url}/{namespace}/{project}/releases/tag/{ref}"
    """The tag URL for the provider."""

    commit_min_length = 8
    """The minimum length of a commit hash."""
    commit_max_length = 40
    """The maximum length of a commit hash."""

    REF: ClassVar[dict[str, RefDef]] = {
        "issues": RefDef(
            regex=re.compile(RefRe.BB + RefRe.NP + "?" + RefRe.ID.format(symbol="#"), re.I),
            url_string="{base_url}/{namespace}/{project}/issues/{ref}",
        ),
        "commits": RefDef(
            regex=re.compile(
                RefRe.BB
                + r"(?:{np}@)?{commit}{ba}".format(
                    np=RefRe.NP,
                    commit=RefRe.COMMIT.format(min=commit_min_length, max=commit_max_length),
                    ba=RefRe.BA,
                ),
                re.I,
            ),
            url_string="{base_url}/{namespace}/{project}/commit/{ref}",
        ),
        "commits_ranges": RefDef(
            regex=re.compile(
                RefRe.BB
                + r"(?:{np}@)?{commit_range}".format(
                    np=RefRe.NP,
                    commit_range=RefRe.COMMIT_RANGE.format(min=commit_min_length, max=commit_max_length),
                ),
                re.I,
            ),
            url_string="{base_url}/{namespace}/{project}/compare/{ref}",
        ),
        "mentions": RefDef(regex=re.compile(RefRe.BB + RefRe.MENTION, re.I), url_string="{base_url}/{ref}"),
    }
    """The reference definitions for the provider."""

    def build_ref_url(self, ref_type: str, match_dict: dict[str, str]) -> str:
        match_dict["base_url"] = self.url
        if not match_dict.get("namespace"):
            match_dict["namespace"] = self.namespace
        if not match_dict.get("project"):
            match_dict["project"] = self.project
        return super().build_ref_url(ref_type, match_dict)

    def get_tag_url(self, tag: str = "") -> str:
        return self.tag_url.format(base_url=self.url, namespace=self.namespace, project=self.project, ref=tag)

    def get_compare_url(self, base: str, target: str) -> str:
        return self.build_ref_url("commits_ranges", {"ref": f"{base}...{target}"})


class GitLab(ProviderRefParser):
    """A parser for the GitLab references."""

    url: str = "https://gitlab.com"
    """The base URL for the provider."""
    project_url: str = "{base_url}/{namespace}/{project}"
    """The project URL for the provider."""
    tag_url: str = "{base_url}/{namespace}/{project}/tags/{ref}"
    """The tag URL for the provider."""

    commit_min_length = 8
    """The minimum length of a commit hash."""
    commit_max_length = 40
    """The maximum length of a commit hash."""

    REF: ClassVar[dict[str, RefDef]] = {
        "issues": RefDef(
            regex=re.compile(RefRe.BB + RefRe.NP + "?" + RefRe.ID.format(symbol="#"), re.I),
            url_string="{base_url}/{namespace}/{project}/issues/{ref}",
        ),
        "merge_requests": RefDef(
            regex=re.compile(RefRe.BB + RefRe.NP + "?" + RefRe.ID.format(symbol=r"!"), re.I),
            url_string="{base_url}/{namespace}/{project}/merge_requests/{ref}",
        ),
        "snippets": RefDef(
            regex=re.compile(RefRe.BB + RefRe.NP + "?" + RefRe.ID.format(symbol=r"\$"), re.I),
            url_string="{base_url}/{namespace}/{project}/snippets/{ref}",
        ),
        "labels_ids": RefDef(
            regex=re.compile(RefRe.BB + RefRe.NP + "?" + RefRe.ID.format(symbol=r"~"), re.I),
            url_string="{base_url}/{namespace}/{project}/issues?label_name[]={ref}",  # no label_id param?
        ),
        "labels_one_word": RefDef(
            regex=re.compile(  # also matches label IDs
                RefRe.BB + RefRe.NP + "?" + RefRe.ONE_WORD.format(symbol=r"~"),
                re.I,
            ),
            url_string="{base_url}/{namespace}/{project}/issues?label_name[]={ref}",
        ),
        "labels_multi_word": RefDef(
            regex=re.compile(RefRe.BB + RefRe.NP + "?" + RefRe.MULTI_WORD.format(symbol=r"~"), re.I),
            url_string="{base_url}/{namespace}/{project}/issues?label_name[]={ref}",
        ),
        "milestones_ids": RefDef(
            regex=re.compile(  # also matches milestones IDs
                RefRe.BB + RefRe.NP + "?" + RefRe.ID.format(symbol=r"%"),
                re.I,
            ),
            url_string="{base_url}/{namespace}/{project}/milestones/{ref}",
        ),
        "milestones_one_word": RefDef(
            regex=re.compile(RefRe.BB + RefRe.NP + "?" + RefRe.ONE_WORD.format(symbol=r"%"), re.I),
            url_string="{base_url}/{namespace}/{project}/milestones",  # cannot guess ID
        ),
        "milestones_multi_word": RefDef(
            regex=re.compile(RefRe.BB + RefRe.NP + "?" + RefRe.MULTI_WORD.format(symbol=r"%"), re.I),
            url_string="{base_url}/{namespace}/{project}/milestones",  # cannot guess ID
        ),
        "commits": RefDef(
            regex=re.compile(
                RefRe.BB
                + r"(?:{np}@)?{commit}{ba}".format(
                    np=RefRe.NP,
                    commit=RefRe.COMMIT.format(min=commit_min_length, max=commit_max_length),
                    ba=RefRe.BA,
                ),
                re.I,
            ),
            url_string="{base_url}/{namespace}/{project}/commit/{ref}",
        ),
        "commits_ranges": RefDef(
            regex=re.compile(
                RefRe.BB
                + r"(?:{np}@)?{commit_range}".format(
                    np=RefRe.NP,
                    commit_range=RefRe.COMMIT_RANGE.format(min=commit_min_length, max=commit_max_length),
                ),
                re.I,
            ),
            url_string="{base_url}/{namespace}/{project}/compare/{ref}",
        ),
        "mentions": RefDef(regex=re.compile(RefRe.BB + RefRe.MENTION, re.I), url_string="{base_url}/{ref}"),
    }
    """The reference definitions for the provider."""

    def build_ref_url(self, ref_type: str, match_dict: dict[str, str]) -> str:
        match_dict["base_url"] = self.url
        if not match_dict.get("namespace"):
            match_dict["namespace"] = self.namespace
        if not match_dict.get("project"):
            match_dict["project"] = self.project
        if ref_type.startswith("label"):
            match_dict["ref"] = match_dict["ref"].replace('"', "").replace(" ", "+")
        return super().build_ref_url(ref_type, match_dict)

    def get_tag_url(self, tag: str = "") -> str:
        return self.tag_url.format(base_url=self.url, namespace=self.namespace, project=self.project, ref=tag)

    def get_compare_url(self, base: str, target: str) -> str:
        return self.build_ref_url("commits_ranges", {"ref": f"{base}...{target}"})


class Bitbucket(ProviderRefParser):
    """A parser for the Bitbucket references."""

    url: str = "https://bitbucket.org"
    """The base URL for the provider."""
    project_url: str = "{base_url}/{namespace}/{project}"
    """The project URL for the provider."""
    tag_url: str = "{base_url}/{namespace}/{project}/commits/tag/{ref}"
    """The tag URL for the provider."""

    commit_min_length = 8
    """The minimum length of a commit hash."""
    commit_max_length = 40
    """The maximum length of a commit hash."""

    REF: ClassVar[dict[str, RefDef]] = {
        "issues": RefDef(
            regex=re.compile(RefRe.BB + RefRe.NP + "?issue\\s*" + RefRe.ID.format(symbol="#"), re.I),
            url_string="{base_url}/{namespace}/{project}/issues/{ref}",
        ),
        "merge_requests": RefDef(
            regex=re.compile(RefRe.BB + RefRe.NP + "?pull request\\s*" + RefRe.ID.format(symbol=r"#"), re.I),
            url_string="{base_url}/{namespace}/{project}/pull-request/{ref}",
        ),
        "commits": RefDef(
            regex=re.compile(
                RefRe.BB
                + r"(?:{np}@)?{commit}{ba}".format(
                    np=RefRe.NP,
                    commit=RefRe.COMMIT.format(min=commit_min_length, max=commit_max_length),
                    ba=RefRe.BA,
                ),
                re.I,
            ),
            url_string="{base_url}/{namespace}/{project}/commits/{ref}",
        ),
        "commits_ranges": RefDef(
            regex=re.compile(
                RefRe.BB
                + r"(?:{np}@)?{commit_range}".format(
                    np=RefRe.NP,
                    commit_range=RefRe.COMMIT_RANGE.format(min=commit_min_length, max=commit_max_length),
                ),
                re.I,
            ),
            url_string="{base_url}/{namespace}/{project}/branches/compare/{ref}#diff",
        ),
        "mentions": RefDef(
            regex=re.compile(RefRe.BB + RefRe.MENTION, re.I),
            url_string="{base_url}/{ref}",
        ),
    }
    """The reference definitions for the provider."""

    def build_ref_url(self, ref_type: str, match_dict: dict[str, str]) -> str:
        match_dict["base_url"] = self.url
        if not match_dict.get("namespace"):
            match_dict["namespace"] = self.namespace
        if not match_dict.get("project"):
            match_dict["project"] = self.project
        return super().build_ref_url(ref_type, match_dict)

    def get_tag_url(self, tag: str = "") -> str:
        return self.tag_url.format(base_url=self.url, namespace=self.namespace, project=self.project, ref=tag)

    def get_compare_url(self, base: str, target: str) -> str:
        return self.build_ref_url("commits_ranges", {"ref": f"{target}..{base}"})
