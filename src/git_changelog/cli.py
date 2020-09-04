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
            return item.startswith("path:") or super(Templates, self).__contains__(item)
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
        help='The Jinja2 template to use. Prefix with "path:" to specify the path '
        'to a directory containing a file named "changelog.md".',
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
    args = parser.parse_args(args=args)

    # get template
    if args.template.startswith("path:"):
        path = args.template.replace("path:", "", 1)
        try:
            template = templates.get_custom_template(path)
        except FileNotFoundError:
            print("git-changelog: no such directory, " "or missing changelog.md: %s" % path, file=sys.stderr)
            return 1
    else:
        template = templates.get_template(args.template)

    # build data
    changelog = Changelog(args.repository, style=args.style)

    # get rendered contents
    rendered = template.render(changelog=changelog)

    # write result in specified output
    if args.output is sys.stdout:
        sys.stdout.write(rendered)
    else:
        with open(args.output, "w") as stream:
            stream.write(rendered)

    return 0
