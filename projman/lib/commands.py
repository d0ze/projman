import subprocess
import os
from abc import ABCMeta, abstractmethod
from typing import List

from projman.lib.context import Context


class CommandArg(object):
    def __init__(self, name: str, type_, default):
        self.name = name
        self.type_ = type_
        self.default = default


class Command(metaclass=ABCMeta):

    def __init__(self, context: Context):
        self.context = context

    @abstractmethod
    def run(self):
        raise NotImplementedError("subclasses must implement this method")

    @classmethod
    def name(cls):
        return cls.__name__.lower()

    @staticmethod
    def args() -> List[CommandArg]:
        return []

    @staticmethod
    def run_bash(cmd):
        return subprocess.run(cmd,
                              shell=True,
                              universal_newlines=True,
                              stderr=subprocess.STDOUT,
                              check=True,
                              env=os.environ)

    def activate_virtualenv(self):
        print("==== activating virtual environment")
        activate_this_file = f"{self.context.venv_path}/bin/activate_this.py"

        exec(compile(open(activate_this_file, "rb").read(), activate_this_file, 'exec'),
             dict(__file__=activate_this_file))

    def create_virtualenv(self):
        print("==== creating virtual environment")
        self.run_bash(f"virtualenv -p python{self.context.python_version} {self.context.venv_path}")

    def install_dependencies(self, upgrade=False):
        print("==== installing dependencies...")
        for dep in self.context.dependencies:
            self.run_bash(f"pip install {dep}" + ("--upgrade" if upgrade else ""))

    @staticmethod
    def get(cmd):
        for class_ in Command.__subclasses__():
            if class_.name() == cmd:
                return class_
        else:
            raise RuntimeError(f"unknown command {cmd}")


class Init(Command):
    """
    Initialize the project structure and creates the virtual environment with the specified python version,
    installing every defined dependency
        --no-venv skip virtualenv creation
        --skip-install skip dependencies installation
    """

    def __init__(self, context: Context, no_venv: bool, skip_install: bool):
        super().__init__(context)
        self.no_venv = no_venv
        self.skip_install = skip_install

    def run(self):
        if not self.no_venv:
            self.create_virtualenv()
            self.activate_virtualenv()
        if not self.skip_install:
            self.install_dependencies()

    @staticmethod
    def args():
        return [
            CommandArg(name="no-venv", type_=bool, default=False),
            CommandArg(name="skip-install", type_=bool, default=False),
        ]


class Setup(Command):
    """
    Activates the project virtual environment
        --install : install project dependencies
    """

    def __init__(self, context: Context, install: bool):
        super().__init__(context)
        self.install = install

    def run(self):
        self.activate_virtualenv()
        if self.install:
            self.install_dependencies()


class Install(Command):
    """
    Installs the project dependencies
    """

    def run(self):
        self.install_dependencies(upgrade=True)


class Run(Command):
    """
    Runs a command
    """

    def __init__(self, context: Context, cmd: str):
        super().__init__(context)
        self.cmd = cmd

    def run(self):
        try:
            self.run_bash(self.context.commands[self.cmd])
        except KeyError:
            raise NotImplementedError(f"unknown command {self.cmd}")
