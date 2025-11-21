# The subpackage containing the builtin templates.

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

from jinja2 import Environment, Template

TEMPLATES_PATH = Path(__file__).parent
"""The path to the templates directory."""
JINJA_ENV = Environment()  # noqa: S701
"""The Jinja environment."""


def _filter_is_url(value: str) -> bool:
    return bool(urlparse(value).scheme)


def configure_env(env: Environment) -> None:
    """Configure the Jinja environment.

    Parameters:
        env: The environment to configure.
    """
    env.filters.update({"is_url": _filter_is_url})


def get_custom_template(path: str | Path) -> Template:
    """Get a custom template instance.

    Parameters:
        path: Path to the custom template.

    Returns:
        The Jinja template.
    """
    return JINJA_ENV.from_string(Path(path).read_text(encoding="utf8"))


def get_template(name: str) -> Template:
    """Get a builtin template instance.

    Parameters:
        name: The template name.

    Returns:
        The Jinja template.
    """
    return JINJA_ENV.from_string(TEMPLATES_PATH.joinpath(f"{name}.md.jinja").read_text(encoding="utf8"))


configure_env(JINJA_ENV)
