# Module containing the commit logic.

from __future__ import annotations

import re
import sys
import warnings
from abc import ABC, abstractmethod
from collections import defaultdict
from contextlib import suppress
from datetime import datetime, timezone
from re import Pattern
from typing import TYPE_CHECKING, Any, Callable, ClassVar, SupportsIndex, overload

if sys.version_info < (3, 13):
    from typing_extensions import deprecated
else:
    from warnings import deprecated

if TYPE_CHECKING:
    from collections.abc import ItemsView, Iterable, KeysView, ValuesView

    from git_changelog._internal.providers import ProviderRefParser, Ref
    from git_changelog._internal.versioning import ParsedVersion


def _clean_body(lines: list[str]) -> list[str]:
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def _is_valid_version(version: str, version_parser: Callable[[str], tuple[ParsedVersion, str]]) -> bool:
    try:
        version_parser(version)
    except ValueError:
        return False
    return True


# YORE: Bump 3: Remove block.
class _Trailers(list[tuple[str, str]]):
    def __init__(self, values: Iterable[tuple[str, str]] | None = None):
        super().__init__(values or ())

    @property
    def _dict(self) -> dict[str, str]:
        return dict(iter(self))

    def __contains__(self, key: str | tuple[str, str]) -> bool:  # type: ignore[override]
        if isinstance(key, str):
            warnings.warn(
                "Checking membership of a string in trailers will stop being supported in version 3.",
                DeprecationWarning,
                stacklevel=2,
            )
            return key in (title for title, _ in self)
        return super().__contains__(key)

    @deprecated("Trailers are now a list of 2-tuples.", category=DeprecationWarning, stacklevel=2)
    def items(self) -> ItemsView:
        return self._dict.items()

    @deprecated("Trailers are now a list of 2-tuples.", category=DeprecationWarning, stacklevel=2)
    def keys(self) -> KeysView:
        return self._dict.keys()

    @deprecated("Trailers are now a list of 2-tuples.", category=DeprecationWarning, stacklevel=2)
    def values(self) -> ValuesView:
        return self._dict.values()

    @deprecated("Trailers are now a list of 2-tuples.", category=DeprecationWarning, stacklevel=2)
    def get(self, key: str, default: str | None = None) -> str | None:
        return self._dict.get(key, default)

    @overload
    def __getitem__(self, key: str) -> str: ...

    @overload
    def __getitem__(self, key: SupportsIndex) -> tuple[str, str]: ...

    @overload
    def __getitem__(self, key: slice) -> list[tuple[str, str]]: ...

    def __getitem__(self, key: str | SupportsIndex | slice) -> str | tuple[str, str] | list[tuple[str, str]]:
        if isinstance(key, str):
            warnings.warn(
                "Getting a trailer with a string key will stop being supported in version 3. Instead, use an integer index, or iterate.",
                DeprecationWarning,
                stacklevel=2,
            )
            return self._dict[key]
        return super().__getitem__(key)

    @overload
    def __setitem__(self, key: str, value: str) -> None: ...

    @overload
    def __setitem__(self, key: SupportsIndex, value: tuple[str, str]) -> None: ...

    @overload
    def __setitem__(self, key: slice, value: Iterable[tuple[str, str]]) -> None: ...

    def __setitem__(
        self,
        key: str | SupportsIndex | slice,
        value: str | tuple[str, str] | Iterable[tuple[str, str]],
    ) -> None:
        if isinstance(key, str):
            warnings.warn(
                "Setting a trailer with a string key will stop being supported in version 3. Instead, append a 2-tuple.",
                DeprecationWarning,
                stacklevel=2,
            )
            self.append((key, value))  # type: ignore[arg-type]
            return
        super().__setitem__(key, value)  # type: ignore[assignment,index]


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
        parent_hashes: str | list[str] = "",
        commits_map: dict[str, Commit] | None = None,
        version_parser: Callable[[str], tuple[ParsedVersion, str]] | None = None,
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
                ref = ref.replace("tag: ", "")  # noqa: PLW2901
                if version_parser is None or _is_valid_version(ref, version_parser):
                    tag = ref
                    break
        self.tag: str = tag
        self.version: str = tag

        if isinstance(parent_hashes, str):
            parent_hashes = parent_hashes.split()
        self.parent_hashes = parent_hashes
        self._commits_map = commits_map

        self.text_refs: dict[str, list[Ref]] = {}
        self.convention: dict[str, Any] = {}

        # YORE: Bump 3: Replace `_Trailers()` with `[]` within line.
        self.trailers: list[tuple[str, str]] = _Trailers()
        self.body_without_trailers = self.body

        if parse_trailers:
            self._parse_trailers()

    @property
    def parent_commits(self) -> list[Commit]:
        """Parent commits of this commit."""
        if not self._commits_map:
            return []
        return [
            self._commits_map[parent_hash] for parent_hash in self.parent_hashes if parent_hash in self._commits_map
        ]

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
                self.trailers.extend(trailers)
                self.body_without_trailers = self.body[:last_blank_line]

    def _parse_trailers_block(self, lines: list[str]) -> list[tuple[str, str]]:
        trailers = []
        for line in lines:
            title, value = line.split(": ", 1)
            trailers.append((title, value.strip()))
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
            #### {cls.__name__[: -(len("Convention"))].strip()}

            *Default sections:*

            {default}

            *Additional sections:*

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

    TYPE_REGEX: ClassVar[Pattern] = re.compile(rf"^(?P<type>({'|'.join(TYPES.keys())}))", re.I)
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

    def parse_commit(self, commit: Commit) -> dict[str, str | bool]:
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
        rf"^(?P<type>({'|'.join(TYPES.keys())}))(?:\((?P<scope>.+)\))?: (?P<subject>.+)$",
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

    def parse_commit(self, commit: Commit) -> dict[str, str | bool]:
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
        rf"^(?P<type>({'|'.join(TYPES.keys())}))(?:\((?P<scope>.+)\))?(?P<breaking>!)?: (?P<subject>.+)$",
    )

    def parse_commit(self, commit: Commit) -> dict[str, str | bool]:
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
