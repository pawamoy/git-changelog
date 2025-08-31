---
hide:
- navigation
---

# CLI reference

<style>
.doclink {
    display: inline;
    position: relative;
    top: -8px;
    font-size: .65rem;
}
p:has(> a.doclink) {
    line-height: 0.2;
}
</style>

```python exec="true" idprefix=""
import argparse
import sys

from git_changelog.cli import get_parser

parser = get_parser()

option_to_docs = {
    "bump": "#understand-the-relationship-with-semver",
    # YORE: Bump 3: Remove line.
    "bump_latest": "#understand-the-relationship-with-semver",
    "config_file": "#configuration-files",
    "convention": "#choose-the-commit-message-convention",
    "filter_commits": "#filter-commits",
    "in_place": "#update-changelog-in-place",
    "input": "#output-release-notes",
    "marker_line": "#update-changelog-in-place",
    "omit_empty_versions": "#",
    "output": "#output-a-changelog",
    "parse_refs": "#provider-specific-references",
    "parse_trailers": "#git-trailers",
    "provider": "#provider-specific-references",
    "release_notes": "#output-release-notes",
    "sections": "#choose-the-sections-to-render",
    "template": "#choose-a-changelog-template",
    "version_regex": "#update-changelog-in-place",
    "versioning": "#choose-a-versioning-scheme",
    "zerover": "#zerover",
}


def render_parser(parser: argparse.ArgumentParser, title: str, heading_level: int = 2) -> str:
    """Render the parser help documents as a string."""
    result = [f"{'#' * heading_level} {title}\n"]
    if parser.description and title != "pdm":
        result.append("> " + parser.description + "\n")

    for group in sorted(parser._action_groups, key=lambda g: g.title.lower(), reverse=True):
        if not any(
            bool(action.option_strings or action.dest) or isinstance(action, argparse._SubParsersAction)
            for action in group._group_actions
        ):
            continue

        result.append(f"{'#' * (heading_level + 1)} {group.title.title()}\n")
        for action in sorted(group._group_actions, key=lambda action: action.dest):
            if isinstance(action, argparse._SubParsersAction):
                for name, subparser in action._name_parser_map.items():
                    result.append(render_parser(subparser, name, heading_level + 1))
                continue

            opts = [f"`{opt}`" for opt in action.option_strings]
            docs = ""
            if action.dest in option_to_docs:
                docs = f"[(docs)](../usage/{option_to_docs[action.dest]}){{ .doclink }}\n\n"
            if not opts:
                line = f"{'#' * (heading_level + 2)} `{action.dest}`\n\n{docs}- "
            else:
                line = f"{'#' * (heading_level + 2)} `{action.dest}`\n\n{docs}- {', '.join(opts)}"
            if action.metavar:
                line += f" `{action.metavar}`"
            line += f": {action.help}"
            if action.default and action.default != argparse.SUPPRESS:
                if action.default is sys.stdout:
                    default = "sys.stdout"
                else:
                    default = action.default
                line += f" Default: `{default}`."
            result.append(line)
        result.append("")

    return "\n".join(result)


print(render_parser(parser, "git-changelog"))
```
