import logging
import sys
from pathlib import Path
from typing import TextIO, Union

import toml
from deepmerge import always_merger
from jinja2 import Template

log = logging.getLogger(__name__)
CONFIG_PATH = Path(__file__).parent


class DataConfig:
    @classmethod
    def from_data(cls, data):
        return cls(**data)


class FileConfig(DataConfig):
    item_name = ""

    @classmethod
    def from_file(cls, filepath: str):
        data = toml.load(filepath)
        if filepath == "pyproject.toml":
            data = data["tool"]["git-changelog"]
        return cls.from_data(data[cls.item_name])


class BuiltinConfig(FileConfig):
    @classmethod
    def builtin(cls, name):
        return cls.from_file(CONFIG_PATH / f"{cls.item_name}" / f"{name}.toml")


class MessageRef(DataConfig):
    def __init__(self, regex, url):
        self.regex = regex
        self.url = url


class MessageRefs(BuiltinConfig):
    item_name = "refs"

    def __init__(self, refs):
        self.refs = refs

    @staticmethod
    def from_data(data):
        return MessageRefs(
            refs={
                name: MessageRef.from_data(ref_data) for name, ref_data in data.items() if isinstance(ref_data, dict)
            },
        )


class URLs(BuiltinConfig):
    def __init__(self, base_url, project_url, tag_url, compare_url):
        self.base_url = base_url
        self.project_url = project_url
        self.tag_url = tag_url
        self.compare_url = compare_url


class MessageRule(DataConfig):
    def __init__(self, regex, multiline=False, find_all=False, ignore_case=True):
        self.regex = regex
        self.multiline = multiline
        self.find_all = find_all
        self.ignore_case = ignore_case


class CommitSection(DataConfig):
    def __init__(self, name, attr, regex=None, non_empty=None):
        self.name = name
        self.attr = attr
        self.regex = regex
        self.non_empty = non_empty


class CommitStyle(BuiltinConfig):
    item_name = "style"

    def __init__(self, rules, sections, enable_sections):
        self.rules = rules
        self.sections = sections
        self.enable_sections = enable_sections

    @staticmethod
    def from_data(data):
        enable_sections = data.get("enable_sections", [])
        sections = {
            name: CommitSection.from_data(section_data) for name, section_data in data.get("sections", {}).items()
        }
        rules = {name: MessageRule.from_data(rule_data) for name, rule_data in data.get("rules", {}).items()}
        return CommitStyle(enable_sections=enable_sections, sections=sections, rules=rules)


class Config:
    def __init__(
        self,
        template: Template,
        style: CommitStyle,
        refs: MessageRefs,
        urls: URLs,
        repository: str = ".",
        output: Union[str, TextIO] = sys.stdout,
    ):
        self.repository = repository
        self.output = output
        self.template = template
        self.style = style
        self.urls = urls
        self._refs = refs

    @property
    def refs(self):
        return self._refs.refs

    @staticmethod
    def from_data(data):
        output = data.get("output")
        if output == "-":
            output = sys.stdout
        style = CommitStyle.from_data(data.get("style"))
        refs = MessageRefs.from_data(data.get("refs", {}))
        urls = URLs.from_data(data.get("urls", {}))
        template = Config.get_template(data.get("template"))
        return Config(template=template, style=style, refs=refs, urls=urls, output=output)

    @staticmethod
    def from_file(filepath: str, overrides=None):
        data = toml.load(filepath)
        if filepath == "pyproject.toml":
            data = data["tool"]["git-changelog"]

        Config.override(data, overrides)

        for config_section, user_data in data.items():
            if "base" in user_data:
                data[config_section] = Config.merge_into_base(config_section, user_data)
        return Config.from_data(data)

    @staticmethod
    def override(data, overrides):
        if overrides["style"]:
            data["style"] = {"base": overrides["style"]}
        if overrides["refs"]:
            data["refs"] = {"base": overrides["refs"]}
        if overrides["urls"]:
            data["urls"] = {"base": overrides["urls"]}
        if overrides["output"]:
            data["output"] = overrides["output"]
        if overrides["template"]:
            data["template"] = overrides["template"]

    @staticmethod
    def merge_into_base(section_name, user_data):
        try:
            base_data = toml.load(CONFIG_PATH / section_name / (user_data["base"] + ".toml"))
        except Exception as error:
            log.error(f"Could not load base data '{user_data['base']} for section '{section_name}'")
            return user_data
        return always_merger.merge(base_data[section_name], user_data)

    @staticmethod
    def get_template(template):
        if template.startswith("path:"):
            path = template.replace("path:", "", 1)
            template = templates.get_local_template(path)
        elif template.startswith("url:"):
            url = template.replace("url:", "", 1)
            template = templates.get_online_template(url)
        else:
            template = templates.get_template(template)
        return template
