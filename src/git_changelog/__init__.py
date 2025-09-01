"""git-changelog package.

Automatic Changelog generator using Jinja2 templates.
"""

from __future__ import annotations

from git_changelog._internal.cli import get_parser, main

__all__: list[str] = ["get_parser", "main"]
