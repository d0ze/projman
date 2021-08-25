import json

from typing import Dict, List


class Context(object):
    def __init__(self,
                 python_version: str,
                 name: str,
                 dependencies: List[str],
                 commands: Dict,
                 venv: str):
        self.python_version = python_version
        self.name = name,
        self.dependencies = dependencies
        self.commands = commands
        self.venv_path = venv

    @staticmethod
    def load(projman_file_path) -> "Context":
        with open(projman_file_path, 'r') as fd:
            conf = json.loads(fd.read())
        return Context(**conf)
