import re
from datetime import datetime
from typing import Dict, List, Pattern, Union

from .providers import ProviderRefParser, Ref


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

    def update_with_style(self, style: "CommitStyle"):
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


class CommitStyle:
    TYPES: Dict[str, str]
    TYPE_REGEX: Pattern
    BREAK_REGEX: Pattern

    def parse_commit(self, commit: Commit) -> Dict[str, Union[str, bool]]:
        raise NotImplementedError


class BasicStyle(CommitStyle):
    TYPES: Dict[str, str] = {
        "add": "Added",
        "fix": "Fixed",
        "change": "Changed",
        "remove": "Removed",
        "merge": "Merged",
        "doc": "Documented",
    }

    TYPE_REGEX: Pattern = re.compile(r"^(?P<type>(%s))" % "|".join(TYPES.keys()), re.I)
    BREAK_REGEX: Pattern = re.compile(r"^break(s|ing changes?)?[ :].+$", re.I | re.MULTILINE)
    DEFAULT_RENDER = [TYPES["add"], TYPES["fix"], TYPES["change"], TYPES["remove"]]

    def parse_commit(self, commit: Commit) -> Dict[str, Union[str, bool]]:
        commit_type = self.parse_type(commit.subject)
        message = "\n".join([commit.subject] + commit.body)
        is_major = self.is_major(message)
        is_minor = not is_major and self.is_minor(commit_type)
        is_patch = not any((is_major, is_minor))

        return dict(type=commit_type, is_major=is_major, is_minor=is_minor, is_patch=is_patch)

    def parse_type(self, commit_subject: str) -> str:
        type_match = self.TYPE_REGEX.match(commit_subject)
        if type_match:
            return self.TYPES.get(type_match.groupdict().get("type").lower())
        return ""

    def is_minor(self, commit_type: str) -> bool:
        return commit_type == self.TYPES["add"]

    def is_major(self, commit_message: str) -> bool:
        return bool(self.BREAK_REGEX.search(commit_message))


class AngularStyle(CommitStyle):
    TYPES: Dict[str, str] = {
        "build": "Build",
        "ci": "CI",
        "perf": "Performance Improvements",
        "feat": "Features",
        "fix": "Bug Fixes",
        "revert": "Reverts",
        "docs": "Docs",
        "style": "Style",
        "refactor": "Code Refactoring",
        "test": "Tests",
        "chore": "Chore",
    }
    SUBJECT_REGEX: Pattern = re.compile(
        r"^(?P<type>(%s))(?:\((?P<scope>.+)\))?: (?P<subject>.+)$" % ("|".join(TYPES.keys()))
    )
    BREAK_REGEX: Pattern = re.compile(r"^break(s|ing changes?)?[ :].+$", re.I | re.MULTILINE)
    DEFAULT_RENDER = [TYPES["feat"], TYPES["fix"], TYPES["revert"], TYPES["refactor"], TYPES["perf"]]

    def parse_commit(self, commit: Commit) -> Dict[str, Union[str, bool]]:
        subject = self.parse_subject(commit.subject)
        message = "\n".join([commit.subject] + commit.body)
        is_major = self.is_major(message)
        is_minor = not is_major and self.is_minor(subject["type"])
        is_patch = not any((is_major, is_minor))

        return dict(
            type=subject["type"],
            scope=subject["scope"],
            subject=subject["subject"],
            is_major=is_major,
            is_minor=is_minor,
            is_patch=is_patch,
        )

    def parse_subject(self, commit_subject: str) -> Dict[str, str]:
        subject_match = self.SUBJECT_REGEX.match(commit_subject)
        if subject_match:
            dct = subject_match.groupdict()
            dct["type"] = self.TYPES[dct["type"]]
            return dct
        return {"type": "", "scope": "", "subject": commit_subject}

    def is_minor(self, commit_type: str) -> bool:
        return commit_type == self.TYPES["feat"]

    def is_major(self, commit_message: str) -> bool:
        return bool(self.BREAK_REGEX.search(commit_message))


class AtomStyle(CommitStyle):
    TYPES: Dict[str, str] = {
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
