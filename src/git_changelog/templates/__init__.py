"""The subpackage containing the builtin templates."""

from pathlib import Path
from typing import Union

import httpx
from jinja2 import Environment, FileSystemLoader, Template
from jinja2.exceptions import TemplateNotFound


def get_path() -> Path:
    """Get the path to the templates directory."""
    return Path(__file__).parent


def get_env(path: Union[Path, str]) -> Environment:
    """Get the Jinja environment."""
    return Environment(loader=FileSystemLoader(str(path)))  # noqa: S701 (we are OK with not auto-escaping)


def get_local_template(path: str) -> Template:
    """Get a local template."""
    template_path = Path(path)
    try:
        return get_env(template_path.parent).get_template(template_path.name)
    except TemplateNotFound:
        raise FileNotFoundError


def get_online_template(url: str) -> Template:
    """Get an online template."""
    return Environment().from_string(httpx.get(url).text)


def get_template(name: str) -> Template:
    """Get a builtin template path."""
    return get_env(get_path()).get_template(name)
