import os
import signal
import sys

from pathlib import Path
from typing import Any
from shellingham import ShellDetectionFailure
from shellingham import detect_shell


class Shell:
    """
    Represents the current shell.
    """

    _shell = None

    def __init__(self, name: str, path: str) -> None:
        self._name = name
        self._path = path

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> str:
        return self._path

    @classmethod
    def get(cls) -> "Shell":
        """
        Retrieve the current shell.
        """
        if cls._shell is not None:
            return cls._shell

        try:
            name, path = detect_shell(os.getpid())
        except (RuntimeError, ShellDetectionFailure):
            shell = None

            if os.name == "posix":
                shell = os.environ.get("SHELL")
            elif os.name == "nt":
                shell = os.environ.get("COMSPEC")

            if not shell:
                raise RuntimeError("Unable to detect the current shell.")

            name, path = Path(shell).stem, shell

        cls._shell = cls(name, path)

        return cls._shell

    def _get_activate_script(self) -> str:
        if "fish" == self._name:
            suffix = ".fish"
        elif "csh" == self._name:
            suffix = ".csh"
        elif "tcsh" == self._name:
            suffix = ".csh"
        else:
            suffix = ""

        return "activate" + suffix

    def _get_source_command(self) -> str:
        if "fish" == self._name:
            return "source"
        elif "csh" == self._name:
            return "source"
        elif "tcsh" == self._name:
            return "source"

        return "."

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self._name}", "{self._path}")'
