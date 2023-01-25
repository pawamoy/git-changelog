"""
git-changelog package.

Automatic Changelog generator using Jinja2 templates.
"""

from __future__ import annotations

from git_changelog.build import GitHub, GitLab

__all__: list[str] = ["GitHub", "GitLab"]  # noqa: WPS410 (the only __variable__ we use)
