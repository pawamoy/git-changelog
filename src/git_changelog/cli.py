# Why does this file exist, and why not put this in `__main__`?
#
# You might be tempted to import things from `__main__` later,
# but that will cause problems: the code will get executed twice:
#
# - When you run `python -m git_changelog` python will execute
#   `__main__.py` as a script. That means there won't be any
#   `git_changelog.__main__` in `sys.modules`.
# - When you import `__main__` it will get executed again (as a module) because
#   there's no `git_changelog.__main__` in `sys.modules`.

"""Module that contains the command line application."""

import argparse
import sys
from typing import List, Optional

from git_changelog.build import Changelog
from git_changelog.config import Config


class Templates(tuple):
    """Helper to pick a template on the command line."""

    def __contains__(self, item: object) -> bool:
        if isinstance(item, str):
            return item.startswith("path:") or item.startswith("url:") or super(Templates, self).__contains__(item)
        return False


STYLES = ("angular", "basic")
REFS_PARSERS = ("github", "gitlab")
TEMPLATES = Templates(("angular", "keepachangelog"))


def get_parser() -> argparse.ArgumentParser:
    """
    Return the CLI argument parser.

    Returns:
        An argparse parser.
    """
    parser = argparse.ArgumentParser(
        add_help=False, prog="git-changelog", description="Command line tool for git-changelog Python package."
    )

    parser.add_argument("repository", metavar="REPOSITORY", help="The repository path, relative or absolute.")

    parser.add_argument(
        "-h", "--help", action="help", default=argparse.SUPPRESS, help="Show this help message and exit."
    )
    parser.add_argument(
        "-c",
        "--config",
        action="store",
        dest="config",
        default="pyproject.toml",
        help="Path to the config file to use. Default: pyproject.toml.",
    )
    parser.add_argument(
        "-o",
        "--output",
        action="store",
        dest="output",
        default=None,
        help="Output to given file. Default: stdout.",
    )
    parser.add_argument(
        "-r",
        "--refs",
        choices=REFS_PARSERS,
        default=None,
        dest="refs",
        help="The references to parse in the commit messages. Available: github, gitlab.",
    )
    parser.add_argument(
        "-s", "--style", choices=STYLES, default=None, dest="style", help="The commit style to match against."
    )
    parser.add_argument(
        "-t",
        "--template",
        choices=TEMPLATES,
        default=None,
        dest="template",
        help="The Jinja2 template to use. Prefix with 'path:' to specify the path "
        "to a custom template, or 'url:' to download a custom template.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="git-changelog 0.1.0",
        help="Show the current version of the program and exit.",
    )
    return parser


def main(args: Optional[List[str]] = None) -> int:
    """
    Run the main program.

    This function is executed when you type `git-changelog` or `python -m git_changelog`.

    Arguments:
        args: Arguments passed from the command line.

    Returns:
        An exit code.
    """
    parser = get_parser()
    opts = parser.parse_args(args=args)

    config = Config.from_file(
        opts.config,
        overrides={"output": opts.output, "refs": opts.refs, "style": opts.style, "template": opts.template},
    )

    changelog = Changelog(repository=config.repository, style=config.style, refs=config.refs)
    rendered = config.template.render(changelog=changelog)

    if config.output is sys.stdout:
        sys.stdout.write(rendered)
    else:
        with open(config.output, "w") as stream:
            stream.write(rendered)

    return 0
