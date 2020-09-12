import logging
from pathlib import Path

import toml
from deepmerge import always_merger

log = logging.getLogger(__name__)

class MessageRef:
    def __init__(self, data):
        self.regex = data.get("regex")
        self.url = data.get("url")


class MessageRefs:
    def __init__(self, data):
        self.base_url = data.get("base_url")
        self.project_url = data.get("project_url")
        self.tag_url = data.get("tag_url")
        self.refs = {name: MessageRef(ref_data) for name, ref_data in data.items() if isinstance(ref_data, dict)}


class MessageRule:
    def __init__(self, data):
        self.regex = data.get("regex")
        self.multiline = data.get("multiline")
        self.find_all = data.get("find_all")
        self.ignore_case = data.get("ignore_case")


class CommitSection:
    def __init__(self, data):
        self.name = data.get("name")
        self.attr = data.get("attr")
        self.regex = data.get("regex")
        self.bool = data.get("bool")


class CommitStyle:
    def __init__(self, data):
        self.enable_sections = data.get("enable_sections", [])
        self.sections = {name: CommitSection(section_data) for name, section_data in data.get("sections", {}).items()}
        self.rules = {name: MessageRule(rule_data) for name, rule_data in data.get("rules", {}).items()}


class Config:
    def __init__(self, data):
        self.commit_style = CommitStyle(data.get("commit_style"))
        self.refs = MessageRefs(data.get("refs", {}))

    @staticmethod
    def from_file(filepath: str):
        data = toml.load(filepath)
        if filepath == "pyproject.toml":
            data = data["tool"]["git-changelog"]
        for config_section, user_data in data.items():
            if "base" in user_data:
                data[config_section] = Config.merge_into_base(config_section, user_data)
        return Config(data)        
                
    @staticmethod
    def merge_into_base(section_name, user_data):
        try:
            base_data = toml.load(Path(__file__).parent / section_name / (user_data["base"] + ".toml"))
        except Exception as error:
            log.error(f"Could not load base data '{user_data['base']} for section '{section_name}'")
            return user_data
        return always_merger.merge(base_data[section_name], user_data)


if __name__ == "__main__":
    config = Config.from_file("pyproject.toml")
    print(config)