"""Module containing the commit logic."""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Pattern

from git_changelog.providers import ProviderRefParser, Ref


class Commit:
    """A class to represent a commit."""

    def __init__(
        self,
        commit_hash: str,
        author_name: str = "",
        author_email: str = "",
        author_date: str | datetime = "",
        committer_name: str = "",
        committer_email: str = "",
        committer_date: str | datetime = "",
        refs: str = "",
        subject: str = "",
        body: list[str] | None = None,
        url: str = "",
    ):
        """
        Initialization method.

        Arguments:
            commit_hash: The commit hash.
            author_name: The author name.
            author_email: The author email.
            author_date: The authoring date (datetime or UTC timestamp).
            committer_name: The committer name.
            committer_email: The committer email.
            committer_date: The committing date (datetime or UTC timestamp).
            refs: The commit refs.
            subject: The commit message subject.
            body: The commit message body.
            url: The commit URL.
        """
        if not author_date:
            author_date = datetime.now()
        elif isinstance(author_date, str):
            author_date = datetime.utcfromtimestamp(float(author_date))
        if not committer_date:
            committer_date = datetime.now()
        elif isinstance(committer_date, str):
            committer_date = datetime.utcfromtimestamp(float(committer_date))

        self.hash: str = commit_hash
        self.author_name: str = author_name
        self.author_email: str = author_email
        self.author_date: datetime = author_date
        self.committer_name: str = committer_name
        self.committer_email: str = committer_email
        self.committer_date: datetime = committer_date
        self.subject: str = subject
        self.body: list[str] = body or []
        self.url: str = url

        tag = ""
        for ref in refs.split(","):
            ref = ref.strip()
            if ref.startswith("tag: "):
                tag = ref.replace("tag: ", "")
                break
        self.tag: str = tag
        self.version: str = tag

        self.text_refs: dict[str, list[Ref]] = {}
        self.style: dict[str, Any] = {}

    def update_with_style(self, style: "CommitStyle") -> None:
        """
        Apply the style-parsed data to this commit.

        Arguments:
            style: The style to use.
        """
        self.style.update(style.parse_commit(self))

    def update_with_provider(self, provider: ProviderRefParser, parse_refs: bool = True) -> None:  # noqa: WPS231
        """
        Apply the provider-parsed data to this commit.

        Arguments:
            provider: The provider to use.
            parse_refs: Whether to parse references for this provider.
        """
        # set the commit url based on provider
        # FIXME: hardcoded 'commits'
        if "commits" in provider.REF:
            self.url = provider.build_ref_url("commits", {"ref": self.hash})
        else:
            # use default "commit" url (could be wrong)
            self.url = f"{provider.url}/{provider.namespace}/{provider.project}/commit/{self.hash}"

        # build commit text references from its subject and body
        if parse_refs:
            for ref_type in provider.REF.keys():
                self.text_refs[ref_type] = provider.get_refs(ref_type, "\n".join([self.subject] + self.body))

            if "issues" in self.text_refs:
                self.text_refs["issues_not_in_subject"] = []
                for issue in self.text_refs["issues"]:
                    if issue.ref not in self.subject:
                        self.text_refs["issues_not_in_subject"].append(issue)


class CommitStyle(ABC):
    """A base class for a style of commit messages."""

    TYPES: dict[str, str]
    TYPE_REGEX: Pattern
    BREAK_REGEX: Pattern

    @abstractmethod
    def parse_commit(self, commit: Commit) -> dict[str, str | bool]:
        """
        Parse the commit to extract information.

        Arguments:
            commit: The commit to parse.

        Returns:
            A dictionary containing the parsed data.
        """  # noqa: DAR202,DAR401
        raise NotImplementedError


class BasicStyle(CommitStyle):
    """Basic commit message style."""

    TYPES: dict[str, str] = {
        "add": "Added",
        "fix": "Fixed",
        "change": "Changed",
        "remove": "Removed",
        "merge": "Merged",
        "doc": "Documented",
    }

    TYPE_REGEX: Pattern = re.compile(r"^(?P<type>(%s))" % "|".join(TYPES.keys()), re.I)  # noqa: WPS323
    BREAK_REGEX: Pattern = re.compile(r"^break(s|ing changes?)?[ :].+$", re.I | re.MULTILINE)
    DEFAULT_RENDER = [TYPES["add"], TYPES["fix"], TYPES["change"], TYPES["remove"]]

    def parse_commit(self, commit: Commit) -> dict[str, str | bool]:  # noqa: D102 (use parent docstring)
        commit_type = self.parse_type(commit.subject)
        message = "\n".join([commit.subject] + commit.body)
        is_major = self.is_major(message)
        is_minor = not is_major and self.is_minor(commit_type)
        is_patch = not any((is_major, is_minor))

        return {"type": commit_type, "is_major": is_major, "is_minor": is_minor, "is_patch": is_patch}

    def parse_type(self, commit_subject: str) -> str:
        """Parse the type of the commit given its subject.

        Arguments:
            commit_subject: The commit message subject.

        Returns:
            The commit type.
        """
        type_match = self.TYPE_REGEX.match(commit_subject)
        if type_match:
            return self.TYPES.get(type_match.groupdict()["type"].lower(), "")
        return ""

    def is_minor(self, commit_type: str) -> bool:
        """Tell if this commit is worth a minor bump.

        Arguments:
            commit_type: The commit type.

        Returns:
            Whether it's a minor commit.
        """
        return commit_type == self.TYPES["add"]

    def is_major(self, commit_message: str) -> bool:
        """Tell if this commit is worth a major bump.

        Arguments:
            commit_message: The commit message.

        Returns:
            Whether it's a major commit.
        """
        return bool(self.BREAK_REGEX.search(commit_message))


class AngularStyle(CommitStyle):
    """Angular commit message style."""

    TYPES: dict[str, str] = {
        "build": "Build",
        "chore": "Chore",
        "ci": "Continuous Integration",
        "deps": "Dependencies",
        "doc": "Docs",
        "docs": "Docs",
        "feat": "Features",
        "fix": "Bug Fixes",
        "perf": "Performance Improvements",
        "ref": "Code Refactoring",
        "refactor": "Code Refactoring",
        "revert": "Reverts",
        "style": "Style",
        "test": "Tests",
        "tests": "Tests",
    }
    SUBJECT_REGEX: Pattern = re.compile(
        r"^(?P<type>(%s))(?:\((?P<scope>.+)\))?: (?P<subject>.+)$" % ("|".join(TYPES.keys()))  # noqa: WPS323 (%)
    )
    BREAK_REGEX: Pattern = re.compile(r"^break(s|ing changes?)?[ :].+$", re.I | re.MULTILINE)
    DEFAULT_RENDER = [TYPES["feat"], TYPES["fix"], TYPES["revert"], TYPES["refactor"], TYPES["perf"]]

    def parse_commit(self, commit: Commit) -> dict[str, str | bool]:  # noqa: D102 (use parent docstring)
        subject = self.parse_subject(commit.subject)
        message = "\n".join([commit.subject] + commit.body)
        is_major = self.is_major(message)
        is_minor = not is_major and self.is_minor(subject["type"])
        is_patch = not any((is_major, is_minor))

        return {
            "type": subject["type"],
            "scope": subject["scope"],
            "subject": subject["subject"],
            "is_major": is_major,
            "is_minor": is_minor,
            "is_patch": is_patch,
        }

    def parse_subject(self, commit_subject: str) -> dict[str, str]:
        """Parse the subject of the commit (`<type>[(scope)]: Subject`).

        Arguments:
            commit_subject: The commit message subject.

        Returns:
            The parsed data.
        """
        subject_match = self.SUBJECT_REGEX.match(commit_subject)
        if subject_match:
            dct = subject_match.groupdict()
            dct["type"] = self.TYPES[dct["type"]]
            return dct
        return {"type": "", "scope": "", "subject": commit_subject}

    def is_minor(self, commit_type: str) -> bool:
        """Tell if this commit is worth a minor bump.

        Arguments:
            commit_type: The commit type.

        Returns:
            Whether it's a minor commit.
        """
        return commit_type == self.TYPES["feat"]

    def is_major(self, commit_message: str) -> bool:
        """Tell if this commit is worth a major bump.

        Arguments:
            commit_message: The commit message.

        Returns:
            Whether it's a major commit.
        """
        return bool(self.BREAK_REGEX.search(commit_message))


class ConventionalCommitStyle(AngularStyle):
    """Conventional commit message style."""

    TYPES: dict[str, str] = AngularStyle.TYPES
    SUBJECT_REGEX: Pattern = re.compile(
        r"^(?P<type>(%s))(?:\((?P<scope>.+)\))?(?P<breaking>!)?: (?P<subject>.+)$"  # noqa: WPS323 (%)
        % ("|".join(TYPES.keys()))
    )

    def parse_commit(self, commit: Commit) -> dict[str, str | bool]:  # noqa: D102 (use parent docstring)
        subject = self.parse_subject(commit.subject)
        message = "\n".join([commit.subject] + commit.body)
        is_major = self.is_major(message) or subject.get("breaking") == "!"
        is_minor = not is_major and self.is_minor(subject["type"])
        is_patch = not any((is_major, is_minor))

        return {
            "type": subject["type"],
            "scope": subject["scope"],
            "subject": subject["subject"],
            "is_major": is_major,
            "is_minor": is_minor,
            "is_patch": is_patch,
        }


class AtomStyle(CommitStyle):
    """Atom commit message style."""

    TYPES: dict[str, str] = {
        ":art:": "",  # when improving the format/structure of the code
        ":racehorse:": "",  # when improving performance
        ":non-potable_water:": "",  # when plugging memory leaks
        ":memo:": "",  # when writing docs
        ":penguin:": "",  # when fixing something on Linux
        ":apple:": "",  # when fixing something on Mac OS
        ":checkered_flag:": "",  # when fixing something on Windows
        ":bug:": "",  # when fixing a bug
        ":fire:": "",  # when removing code or files
        ":green_heart:": "",  # when fixing the CI build
        ":white_check_mark:": "",  # when adding tests
        ":lock:": "",  # when dealing with security
        ":arrow_up:": "",  # when upgrading dependencies
        ":arrow_down:": "",  # when downgrading dependencies
        ":shirt:": "",  # when removing linter warnings
    }
