"""
git-changelog package.

Automatic Changelog generator using Jinja2 templates.
"""

from typing import List

from git_changelog.build import GitHub, GitLab

__all__: List[str] = ["GitHub", "GitLab"]
