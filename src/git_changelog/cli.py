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

from git_changelog import templates
from git_changelog.build import Changelog

STYLES = ("angular", "atom", "basic")


class Templates(tuple):
    """Helper to pick a template on the command line."""

    def __contains__(self, item: object) -> bool:
        if isinstance(item, str):
            return item.startswith("path:") or item.startswith("url:") or super(Templates, self).__contains__(item)
        return False


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
        help="Path to the config file to use. Default: pyproject.toml."
    )
    parser.add_argument(
        "-o",
        "--output",
        action="store",
        dest="output",
        default=sys.stdout,
        help="Output to given file. Default: stdout.",
    )
    parser.add_argument(
        "-s", "--style", choices=STYLES, default="basic", dest="style", help="The commit style to match against."
    )
    parser.add_argument(
        "-t",
        "--template",
        choices=Templates(("angular", "keepachangelog")),
        default="keepachangelog",
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

    config = Config.from_file(opts.config)

    # get template
    if opts.template.startswith("path:"):
        path = opts.template.replace("path:", "", 1)
        try:
            template = templates.get_local_template(path)
        except FileNotFoundError:
            print(f"git-changelog: no such file: {path}", file=sys.stderr)
            return 1
    elif opts.template.startswith("url:"):
        try:
            url = opts.template.replace("url:", "", 1)
            template = templates.get_online_template(url)
        except Exception:
            print(f"git-changelog: could not fetch template at: {url}", file=sys.stderr)
            return 1
    else:
        template = templates.get_template(opts.template)

    # build data
    changelog = Changelog(opts.repository, style=opts.style)

    # get rendered contents
    rendered = template.render(changelog=changelog)

    # write result in specified output
    if opts.output is sys.stdout:
        sys.stdout.write(rendered)
    else:
        with open(opts.output, "w") as stream:
            stream.write(rendered)

    return 0
