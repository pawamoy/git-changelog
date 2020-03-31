import re
from typing import Dict, List, Match, Pattern, Union


class RefRe:
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
    def __init__(self, ref: str, url: str):
        self.ref: str = ref
        self.url: str = url

    def __str__(self):
        return self.ref + ": " + self.url


class ProviderRefParser:
    url: str
    namespace: str
    project: str
    REF: Dict[str, Dict[str, Union[str, Pattern]]] = {}

    def get_refs(self, ref_type: str, text: str) -> List[Ref]:
        return [
            Ref(ref=match.group().strip(), url=self.build_ref_url(ref_type, match.groupdict()))
            for match in self.parse_refs(ref_type, text)
        ]

    def parse_refs(self, ref_type: str, text: str) -> List[Match]:
        if ref_type not in self.REF:
            refs = [k for k in self.REF.keys() if k.startswith(ref_type)]
            return [m for ref in refs for m in self.REF[ref]["regex"].finditer(text)]
        return [m for m in self.REF[ref_type]["regex"].finditer(text)]

    def build_ref_url(self, ref_type: str, match_dict: Dict[str, str]) -> str:
        return self.REF[ref_type]["url"].format(**match_dict)

    def get_tag_url(self, tag: str) -> str:
        raise NotImplementedError

    def get_compare_url(self, base: str, target: str) -> str:
        raise NotImplementedError


class GitHub(ProviderRefParser):
    url: str = "https://github.com"
    project_url: str = "{base_url}/{namespace}/{project}"
    tag_url: str = "{base_url}/{namespace}/{project}/releases/tag/{ref}"

    REF: Dict[str, Dict[str, Union[str, Pattern]]] = dict(
        issues=dict(
            regex=re.compile(RefRe.BB + RefRe.NP + "?" + RefRe.ID.format(symbol="#"), re.I),
            url="{base_url}/{namespace}/{project}/issues/{ref}",
        ),
        commits=dict(
            regex=re.compile(
                RefRe.BB
                + r"(?:{np}@)?{commit}{ba}".format(np=RefRe.NP, commit=RefRe.COMMIT.format(min=7, max=40), ba=RefRe.BA),
                re.I,
            ),
            url="{base_url}/{namespace}/{project}/commit/{ref}",
        ),
        commits_ranges=dict(
            regex=re.compile(
                RefRe.BB
                + r"(?:{np}@)?{commit_range}".format(
                    np=RefRe.NP, commit_range=RefRe.COMMIT_RANGE.format(min=7, max=40)
                ),
                re.I,
            ),
            url="{base_url}/{namespace}/{project}/compare/{ref}",
        ),
        mentions=dict(regex=re.compile(RefRe.BB + RefRe.MENTION, re.I), url="{base_url}/{ref}"),
    )

    def __init__(self, namespace: str, project: str, url: str = url):
        self.namespace: str = namespace
        self.project: str = project
        self.url: str = url

    def build_ref_url(self, ref_type: str, match_dict: Dict[str, str]) -> str:
        match_dict["base_url"] = self.url
        if not match_dict.get("namespace"):
            match_dict["namespace"] = self.namespace
        if not match_dict.get("project"):
            match_dict["project"] = self.project
        return super(GitHub, self).build_ref_url(ref_type, match_dict)

    def get_tag_url(self, tag: str = "") -> str:
        return self.tag_url.format(base_url=self.url, namespace=self.namespace, project=self.project, ref=tag)

    def get_compare_url(self, base: str, target: str) -> str:
        return self.build_ref_url("commits_ranges", {"ref": "%s...%s" % (base, target)})


class GitLab(ProviderRefParser):
    url: str = "https://gitlab.com"
    project_url: str = "{base_url}/{namespace}/{project}"
    tag_url: str = "{base_url}/{namespace}/{project}/tags/{ref}"

    REF: Dict[str, Dict[str, Union[str, Pattern]]] = dict(
        issues=dict(
            regex=re.compile(RefRe.BB + RefRe.NP + "?" + RefRe.ID.format(symbol="#"), re.I),
            url="{base_url}/{namespace}/{project}/issues/{ref}",
        ),
        merge_requests=dict(
            regex=re.compile(RefRe.BB + RefRe.NP + "?" + RefRe.ID.format(symbol=r"!"), re.I),
            url="{base_url}/{namespace}/{project}/merge_requests/{ref}",
        ),
        snippets=dict(
            regex=re.compile(RefRe.BB + RefRe.NP + "?" + RefRe.ID.format(symbol=r"\$"), re.I),
            url="{base_url}/{namespace}/{project}/snippets/{ref}",
        ),
        labels_ids=dict(
            regex=re.compile(RefRe.BB + RefRe.NP + "?" + RefRe.ID.format(symbol=r"~"), re.I),
            url="{base_url}/{namespace}/{project}/issues?label_name[]={ref}",  # no label_id param?
        ),
        labels_one_word=dict(
            regex=re.compile(  # also matches label IDs
                RefRe.BB + RefRe.NP + "?" + RefRe.ONE_WORD.format(symbol=r"~"), re.I
            ),
            url="{base_url}/{namespace}/{project}/issues?label_name[]={ref}",
        ),
        labels_multi_word=dict(
            regex=re.compile(RefRe.BB + RefRe.NP + "?" + RefRe.MULTI_WORD.format(symbol=r"~"), re.I),
            url="{base_url}/{namespace}/{project}/issues?label_name[]={ref}",
        ),
        milestones_ids=dict(
            regex=re.compile(  # also matches milestones IDs
                RefRe.BB + RefRe.NP + "?" + RefRe.ID.format(symbol=r"%"), re.I
            ),
            url="{base_url}/{namespace}/{project}/milestones/{ref}",
        ),
        milestones_one_word=dict(
            regex=re.compile(RefRe.BB + RefRe.NP + "?" + RefRe.ONE_WORD.format(symbol=r"%"), re.I),
            url="{base_url}/{namespace}/{project}/milestones",  # cannot guess ID
        ),
        milestones_multi_word=dict(
            regex=re.compile(RefRe.BB + RefRe.NP + "?" + RefRe.MULTI_WORD.format(symbol=r"%"), re.I),
            url="{base_url}/{namespace}/{project}/milestones",  # cannot guess ID
        ),
        commits=dict(
            regex=re.compile(
                RefRe.BB
                + r"(?:{np}@)?{commit}{ba}".format(np=RefRe.NP, commit=RefRe.COMMIT.format(min=8, max=40), ba=RefRe.BA),
                re.I,
            ),
            url="{base_url}/{namespace}/{project}/commit/{ref}",
        ),
        commits_ranges=dict(
            regex=re.compile(
                RefRe.BB
                + r"(?:{np}@)?{commit_range}".format(
                    np=RefRe.NP, commit_range=RefRe.COMMIT_RANGE.format(min=8, max=40)
                ),
                re.I,
            ),
            url="{base_url}/{namespace}/{project}/compare/{ref}",
        ),
        mentions=dict(regex=re.compile(RefRe.BB + RefRe.MENTION, re.I), url="{base_url}/{ref}"),
    )

    def __init__(self, namespace: str, project: str, url: str = url):
        self.namespace: str = namespace
        self.project: str = project
        self.url: str = url

    def build_ref_url(self, ref_type: str, match_dict: Dict[str, str]) -> str:
        match_dict["base_url"] = self.url
        if not match_dict.get("namespace"):
            match_dict["namespace"] = self.namespace
        if not match_dict.get("project"):
            match_dict["project"] = self.project
        if ref_type.startswith("label"):
            match_dict["ref"] = match_dict["ref"].replace('"', "").replace(" ", "+")
        return super(GitLab, self).build_ref_url(ref_type, match_dict)

    def get_tag_url(self, tag: str = "") -> str:
        return self.tag_url.format(base_url=self.url, namespace=self.namespace, project=self.project, ref=tag)

    def get_compare_url(self, base: str, target: str) -> str:
        return self.build_ref_url("commits_ranges", {"ref": "%s...%s" % (base, target)})
