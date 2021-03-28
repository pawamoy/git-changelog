"""Module containing the parsing utilities for git providers."""

import re
from abc import ABC, abstractmethod
from typing import Dict, List, Match, Pattern


class RefRe:
    """An enum helper to store parts of regular expressions for references."""

    BB = r"(?:^|[\s,])"  # blank before
    BA = r"(?:[\s,]|$)"  # blank after
    NP = r"(?:(?P<namespace>[-\w]+)/)?(?P<project>[-\w]+)"  # namespace and project
    ID = r"{symbol}(?P<ref>[1-9]\d*)"
    ONE_WORD = r"{symbol}(?P<ref>\w*[-a-z_ ][-\w]*)"
    MULTI_WORD = r'{symbol}(?P<ref>"\w[- \w]*")'
    COMMIT = r"(?P<ref>[0-9a-f]{{{min},{max}}})"
    COMMIT_RANGE = r"(?P<ref>[0-9a-f]{{{min},{max}}}\.\.\.[0-9a-f]{{{min},{max}}})"
    MENTION = r"@(?P<ref>\w[-\w]*)"


class Ref:
    """A class to represent a reference and its URL."""

    def __init__(self, ref: str, url: str) -> None:
        """
        Initialization method.

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
        """
        Initialization method.

        Arguments:
            regex: The regular expression to match the reference.
            url_string: The URL string to format using matched groups.
        """
        self.regex = regex
        self.url_string = url_string


class ProviderRefParser(ABC):
    """A base class for specific providers reference parsers."""

    url: str
    namespace: str
    project: str
    REF: Dict[str, RefDef] = {}

    def get_refs(self, ref_type: str, text: str) -> List[Ref]:
        """
        Find all references in the given text.

        Arguments:
            ref_type: The reference type.
            text: The text in which to search references.

        Returns:
            A list of references (instances of [Ref][git_changelog.providers.Ref]).
        """
        return [
            Ref(ref=match.group().strip(), url=self.build_ref_url(ref_type, match.groupdict()))
            for match in self.parse_refs(ref_type, text)
        ]

    def parse_refs(self, ref_type: str, text: str) -> List[Match]:
        """
        Parse references in the given text.

        Arguments:
            ref_type: The reference type.
            text: The text to parse.

        Returns:
            A list of regular expressions matches.
        """
        if ref_type not in self.REF:
            refs = [key for key in self.REF.keys() if key.startswith(ref_type)]
            return [match for ref in refs for match in self.REF[ref].regex.finditer(text)]
        return list(self.REF[ref_type].regex.finditer(text))

    def build_ref_url(self, ref_type: str, match_dict: Dict[str, str]) -> str:
        """
        Build the URL for a reference type and a dictionary of matched groups.

        Arguments:
            ref_type: The reference type.
            match_dict: The matched groups.

        Returns:
            The built URL.
        """
        return self.REF[ref_type].url_string.format(**match_dict)

    @abstractmethod
    def get_tag_url(self, tag: str) -> str:
        """
        Get the URL for a git tag.

        Arguments:
            tag: The git tag.

        Returns:
            The tag URL.
        """  # noqa: DAR202,DAR401
        raise NotImplementedError

    @abstractmethod
    def get_compare_url(self, base: str, target: str) -> str:
        """
        Get the URL for a tag comparison.

        Arguments:
            base: The base tag.
            target: The target tag.

        Returns:
            The comparison URL.
        """  # noqa: DAR202,DAR401
        raise NotImplementedError


class GitHub(ProviderRefParser):
    """A parser for the GitHub references."""

    url: str = "https://github.com"
    project_url: str = "{base_url}/{namespace}/{project}"
    tag_url: str = "{base_url}/{namespace}/{project}/releases/tag/{ref}"

    commit_min_length = 8
    commit_max_length = 40

    REF: Dict[str, RefDef] = {
        "issues": RefDef(
            regex=re.compile(RefRe.BB + RefRe.NP + "?" + RefRe.ID.format(symbol="#"), re.I),
            url_string="{base_url}/{namespace}/{project}/issues/{ref}",
        ),
        "commits": RefDef(
            regex=re.compile(
                RefRe.BB
                + r"(?:{np}@)?{commit}{ba}".format(
                    np=RefRe.NP, commit=RefRe.COMMIT.format(min=commit_min_length, max=commit_max_length), ba=RefRe.BA
                ),
                re.I,
            ),
            url_string="{base_url}/{namespace}/{project}/commit/{ref}",
        ),
        "commits_ranges": RefDef(
            regex=re.compile(
                RefRe.BB
                + r"(?:{np}@)?{commit_range}".format(
                    np=RefRe.NP, commit_range=RefRe.COMMIT_RANGE.format(min=commit_min_length, max=commit_max_length)
                ),
                re.I,
            ),
            url_string="{base_url}/{namespace}/{project}/compare/{ref}",
        ),
        "mentions": RefDef(regex=re.compile(RefRe.BB + RefRe.MENTION, re.I), url_string="{base_url}/{ref}"),
    }

    def __init__(self, namespace: str, project: str, url: str = url):
        """
        Initialization method.

        Arguments:
            namespace: The GitHub namespace.
            project: The GitHub project.
            url: The GitHub URL.
        """
        self.namespace: str = namespace
        self.project: str = project
        self.url: str = url  # noqa: WPS601 (shadowing but uses class' as default)

    def build_ref_url(self, ref_type: str, match_dict: Dict[str, str]) -> str:  # noqa: D102 (use parent docstring)
        match_dict["base_url"] = self.url
        if not match_dict.get("namespace"):
            match_dict["namespace"] = self.namespace
        if not match_dict.get("project"):
            match_dict["project"] = self.project
        return super().build_ref_url(ref_type, match_dict)

    def get_tag_url(self, tag: str = "") -> str:  # noqa: D102,WPS615
        return self.tag_url.format(base_url=self.url, namespace=self.namespace, project=self.project, ref=tag)

    def get_compare_url(self, base: str, target: str) -> str:  # noqa: D102 (use parent docstring)
        return self.build_ref_url("commits_ranges", {"ref": f"{base}...{target}"})


class GitLab(ProviderRefParser):
    """A parser for the GitLab references."""

    url: str = "https://gitlab.com"
    project_url: str = "{base_url}/{namespace}/{project}"
    tag_url: str = "{base_url}/{namespace}/{project}/tags/{ref}"

    commit_min_length = 8
    commit_max_length = 40

    REF: Dict[str, RefDef] = {
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
                RefRe.BB + RefRe.NP + "?" + RefRe.ONE_WORD.format(symbol=r"~"), re.I
            ),
            url_string="{base_url}/{namespace}/{project}/issues?label_name[]={ref}",
        ),
        "labels_multi_word": RefDef(
            regex=re.compile(RefRe.BB + RefRe.NP + "?" + RefRe.MULTI_WORD.format(symbol=r"~"), re.I),
            url_string="{base_url}/{namespace}/{project}/issues?label_name[]={ref}",
        ),
        "milestones_ids": RefDef(
            regex=re.compile(  # also matches milestones IDs
                RefRe.BB + RefRe.NP + "?" + RefRe.ID.format(symbol=r"%"), re.I
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
                    np=RefRe.NP, commit=RefRe.COMMIT.format(min=commit_min_length, max=commit_max_length), ba=RefRe.BA
                ),
                re.I,
            ),
            url_string="{base_url}/{namespace}/{project}/commit/{ref}",
        ),
        "commits_ranges": RefDef(
            regex=re.compile(
                RefRe.BB
                + r"(?:{np}@)?{commit_range}".format(
                    np=RefRe.NP, commit_range=RefRe.COMMIT_RANGE.format(min=commit_min_length, max=commit_max_length)
                ),
                re.I,
            ),
            url_string="{base_url}/{namespace}/{project}/compare/{ref}",
        ),
        "mentions": RefDef(regex=re.compile(RefRe.BB + RefRe.MENTION, re.I), url_string="{base_url}/{ref}"),
    }

    def __init__(self, namespace: str, project: str, url: str = url):
        """
        Initialization method.

        Arguments:
            namespace: The GitLab namespace.
            project: The GitLab project.
            url: The GitLab URL.
        """
        self.namespace: str = namespace
        self.project: str = project
        self.url: str = url  # noqa: WPS601 (shadowing but uses class' as default)

    def build_ref_url(self, ref_type: str, match_dict: Dict[str, str]) -> str:  # noqa: D102 (use parent docstring)
        match_dict["base_url"] = self.url
        if not match_dict.get("namespace"):
            match_dict["namespace"] = self.namespace
        if not match_dict.get("project"):
            match_dict["project"] = self.project
        if ref_type.startswith("label"):
            match_dict["ref"] = match_dict["ref"].replace('"', "").replace(" ", "+")
        return super().build_ref_url(ref_type, match_dict)

    def get_tag_url(self, tag: str = "") -> str:  # noqa: D102,WPS615
        return self.tag_url.format(base_url=self.url, namespace=self.namespace, project=self.project, ref=tag)

    def get_compare_url(self, base: str, target: str) -> str:  # noqa: D102 (use parent docstring)
        return self.build_ref_url("commits_ranges", {"ref": f"{base}...{target}"})
