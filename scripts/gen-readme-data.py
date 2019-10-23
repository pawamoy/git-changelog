#!/usr/bin/env python

import json

from git_changelog.cli import get_parser

# import argparse


parser = get_parser()

output = {"main_usage": parser.format_help(), "commands": []}

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

output["commands"] = list(sorted(output["commands"], key=lambda c: c["name"]))
json_output = json.dumps(output)
print(json_output)
