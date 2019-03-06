#!/usr/bin/env python

import json
# import argparse

from git_changelog.cli import get_parser

parser = get_parser()

output = {
    "main_usage": parser.format_help(),
    "commands": []
}

# subparser_actions = [
#     action for action in parser._actions
#     if isinstance(action, argparse._SubParsersAction)
# ]
#
# for subparser_action in subparser_actions:
#     for choice, subparser in subparser_action.choices.items():
#         output["commands"].append({
#             "name": choice,
#             "usage": subparser.format_help()
#         })

json_output = json.dumps(output)
print(json_output)
