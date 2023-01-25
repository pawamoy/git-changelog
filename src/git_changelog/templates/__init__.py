"""The subpackage containing the builtin templates."""

from __future__ import annotations

import os

from jinja2 import Environment, FileSystemLoader, Template


def get_path() -> str:
    """Get the path to the templates directory.

    Returns:
        The path to the templates directory.
    """
    return os.path.dirname(os.path.abspath(__file__))


def get_env(path: str) -> Environment:
    """Get the Jinja environment.

    Arguments:
        path: The path to give to the Jinja file system loader.

    Returns:
        The Jinja environment.
    """
    return Environment(loader=FileSystemLoader(path))  # noqa: S701 (we are OK with not auto-escaping)


def get_custom_template(path: str) -> Template:
    """Get a custom templates' path.

    Arguments:
        path: Path to the directory containing templates.

    Returns:
        The Jinja template.
    """
    return get_env(os.path.abspath(path)).get_template("changelog.md")


def get_template(name: str) -> Template:
    """Get a builtin template path.

    Arguments:
        name: The template name.

    Returns:
        The Jinja template.
    """
    return get_env(os.path.join(get_path(), name)).get_template("changelog.md")
