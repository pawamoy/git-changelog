import os

from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound


def get_path():
    return os.path.dirname(os.path.abspath(__file__))


def get_env(path):
    return Environment(loader=FileSystemLoader(path))


def get_custom_template(path):
    try:
        return get_env(os.path.abspath(path)).get_template("changelog.md")
    except TemplateNotFound:
        raise FileNotFoundError


def get_template(name):
    return get_env(os.path.join(get_path(), name)).get_template("changelog.md")
