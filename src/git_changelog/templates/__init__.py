import os

from jinja2 import Environment, FileSystemLoader, Template
from jinja2.exceptions import TemplateNotFound


def get_path() -> str:
    return os.path.dirname(os.path.abspath(__file__))


def get_env(path: str) -> Environment:
    return Environment(loader=FileSystemLoader(path))  # nosec


def get_custom_template(path: str) -> Environment:
    try:
        return get_env(os.path.abspath(path)).get_template("changelog.md")
    except TemplateNotFound:
        raise FileNotFoundError


def get_template(name: str) -> Template:
    return get_env(os.path.join(get_path(), name)).get_template("changelog.md")
