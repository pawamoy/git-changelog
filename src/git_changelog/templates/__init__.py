"""The subpackage containing the builtin templates."""

import os

from jinja2 import Environment, FileSystemLoader, Template
from jinja2.exceptions import TemplateNotFound


def get_path() -> str:
    """Get the path to the templates directory."""
    return os.path.dirname(os.path.abspath(__file__))


def get_env(path: str) -> Environment:
    """Get the Jinja environment."""
    return Environment(loader=FileSystemLoader(path))  # noqa: S701 (we are OK with not auto-escaping)


def get_custom_template(path: str) -> Template:
    """Get a custom templates' path."""
    try:
        return get_env(os.path.abspath(path)).get_template("changelog.md")
    except TemplateNotFound:
        raise FileNotFoundError


def get_template(name: str) -> Template:
    """Get a builtin template path."""
    return get_env(os.path.join(get_path(), name)).get_template("changelog.md")
