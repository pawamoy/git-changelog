"""Module containing the commit logic."""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from collections import defaultdict
from contextlib import suppress
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, ClassVar, Pattern

if TYPE_CHECKING:
    from git_changelog.providers import ProviderRefParser, Ref


def _clean_body(lines: list[str]) -> list[str]:
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


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
        *,
        parse_trailers: bool = False,
    ):
        """Initialization method.

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
            parse_trailers: Whether to parse Git trailers.
        """
        if not author_date:
            author_date = datetime.now()  # noqa: DTZ005
        elif isinstance(author_date, str):
            author_date = datetime.fromtimestamp(float(author_date), tz=timezone.utc)
        if not committer_date:
            committer_date = datetime.now()  # noqa: DTZ005
        elif isinstance(committer_date, str):
            committer_date = datetime.fromtimestamp(float(committer_date), tz=timezone.utc)

        self.hash: str = commit_hash
        self.author_name: str = author_name
        self.author_email: str = author_email
        self.author_date: datetime = author_date
        self.committer_name: str = committer_name
        self.committer_email: str = committer_email
        self.committer_date: datetime = committer_date
        self.subject: str = subject
        self.body: list[str] = _clean_body(body) if body else []
        self.url: str = url

        tag = ""
        for ref in refs.split(","):
            ref = ref.strip()  # noqa: PLW2901
            if ref.startswith("tag: "):
                tag = ref.replace("tag: ", "")
                break
        self.tag: str = tag
        self.version: str = tag

        self.text_refs: dict[str, list[Ref]] = {}
        self.convention: dict[str, Any] = {}

        self.trailers: dict[str, str] = {}
        self.body_without_trailers = self.body

        if parse_trailers:
            self._parse_trailers()

    def update_with_convention(self, convention: CommitConvention) -> None:
        """Apply the convention-parsed data to this commit.

        Arguments:
            convention: The convention to use.
        """
        self.convention.update(convention.parse_commit(self))

    def update_with_provider(
        self,
        provider: ProviderRefParser,
        parse_refs: bool = True,  # noqa: FBT001,FBT002
    ) -> None:
        """Apply the provider-parsed data to this commit.

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
            for ref_type in provider.REF:
                self.text_refs[ref_type] = provider.get_refs(
                    ref_type,
                    "\n".join([self.subject, *self.body]),
                )

            if "issues" in self.text_refs:
                self.text_refs["issues_not_in_subject"] = []
                for issue in self.text_refs["issues"]:
                    if issue.ref not in self.subject:
                        self.text_refs["issues_not_in_subject"].append(issue)

    def _parse_trailers(self) -> None:
        last_blank_line = -1
        for index, line in enumerate(self.body):
            if not line:
                last_blank_line = index
        with suppress(ValueError):
            trailers = self._parse_trailers_block(self.body[last_blank_line + 1 :])
            if trailers:
                self.trailers.update(trailers)
                self.body_without_trailers = self.body[:last_blank_line]

    def _parse_trailers_block(self, lines: list[str]) -> dict[str, str]:
        trailers = {}
        for line in lines:
            title, value = line.split(": ", 1)
            trailers[title] = value.strip()
        return trailers  # or raise ValueError due to split unpacking


class CommitConvention(ABC):
    """A base class for a convention of commit messages."""

    TYPES: ClassVar[dict[str, str]]
    TYPE_REGEX: ClassVar[Pattern]
    BREAK_REGEX: ClassVar[Pattern]
    DEFAULT_RENDER: ClassVar[list[str]]

    @abstractmethod
    def parse_commit(self, commit: Commit) -> dict[str, str | bool]:
        """Parse the commit to extract information.

        Arguments:
            commit: The commit to parse.

        Returns:
            A dictionary containing the parsed data.
        """
        raise NotImplementedError

    @classmethod
    def _format_sections_help(cls) -> str:
        reversed_map = defaultdict(list)
        for section_type, section_title in cls.TYPES.items():
            reversed_map[section_title].append(section_type)
        default_sections = cls.DEFAULT_RENDER
        default = "- " + "\n- ".join(f"{', '.join(reversed_map[title])}: {title}" for title in default_sections)
        additional = "- " + "\n- ".join(
            f"{', '.join(types)}: {title}" for title, types in reversed_map.items() if title not in default_sections
        )
        return re.sub(
            r"\n *",
            "\n",
            f"""
            {cls.__name__.replace('Convention', ' Convention').upper().strip()}

            Default sections:
            {default}

            Additional sections:
            {additional}
            """,
        )


class BasicConvention(CommitConvention):
    """Basic commit message convention."""

    TYPES: ClassVar[dict[str, str]] = {
        "add": "Added",
        "fix": "Fixed",
        "change": "Changed",
        "remove": "Removed",
        "merge": "Merged",
        "doc": "Documented",
    }

    TYPE_REGEX: ClassVar[Pattern] = re.compile(r"^(?P<type>(%s))" % "|".join(TYPES.keys()), re.I)
    BREAK_REGEX: ClassVar[Pattern] = re.compile(
        r"^break(s|ing changes?)?[ :].+$",
        re.I | re.MULTILINE,
    )
    DEFAULT_RENDER: ClassVar[list[str]] = [
        TYPES["add"],
        TYPES["fix"],
        TYPES["change"],
        TYPES["remove"],
    ]

    def parse_commit(self, commit: Commit) -> dict[str, str | bool]:  # noqa: D102
        commit_type = self.parse_type(commit.subject)
        message = "\n".join([commit.subject, *commit.body])
        is_major = self.is_major(message)
        is_minor = not is_major and self.is_minor(commit_type)
        is_patch = not any((is_major, is_minor))

        return {
            "type": commit_type,
            "is_major": is_major,
            "is_minor": is_minor,
            "is_patch": is_patch,
        }

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


class AngularConvention(CommitConvention):
    """Angular commit message convention."""

    TYPES: ClassVar[dict[str, str]] = {
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
    SUBJECT_REGEX: ClassVar[Pattern] = re.compile(
        r"^(?P<type>(%s))(?:\((?P<scope>.+)\))?: (?P<subject>.+)$" % ("|".join(TYPES.keys())),  # (%)
    )
    BREAK_REGEX: ClassVar[Pattern] = re.compile(
        r"^break(s|ing changes?)?[ :].+$",
        re.I | re.MULTILINE,
    )
    DEFAULT_RENDER: ClassVar[list[str]] = [
        TYPES["feat"],
        TYPES["fix"],
        TYPES["revert"],
        TYPES["refactor"],
        TYPES["perf"],
    ]

    def parse_commit(self, commit: Commit) -> dict[str, str | bool]:  # noqa: D102
        subject = self.parse_subject(commit.subject)
        message = "\n".join([commit.subject, *commit.body])
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


class ConventionalCommitConvention(AngularConvention):
    """Conventional commit message convention."""

    TYPES: ClassVar[dict[str, str]] = AngularConvention.TYPES
    DEFAULT_RENDER: ClassVar[list[str]] = AngularConvention.DEFAULT_RENDER
    SUBJECT_REGEX: ClassVar[Pattern] = re.compile(
        r"^(?P<type>(%s))(?:\((?P<scope>.+)\))?(?P<breaking>!)?: (?P<subject>.+)$" % ("|".join(TYPES.keys())),  # (%)
    )

    def parse_commit(self, commit: Commit) -> dict[str, str | bool]:  # noqa: D102
        subject = self.parse_subject(commit.subject)
        message = "\n".join([commit.subject, *commit.body])
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


class AtomConvention(CommitConvention):
    """Atom commit message convention."""

    TYPES: ClassVar[dict[str, str]] = {
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
