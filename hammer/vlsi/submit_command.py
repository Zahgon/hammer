import atexit
import subprocess
import termios
import sys
import os
import datetime
from abc import abstractmethod
from functools import reduce
from typing import Any, Dict, List, Tuple, NamedTuple, Optional
from hammer.config import HammerDatabase
from hammer.logging import HammerVLSILoggingContext
from hammer.utils import add_dicts, get_or_else
__all__ = ['HammerSubmitCommand', 'HammerLocalSubmitCommand', 'HammerLSFSettings', 'HammerLSFSubmitCommand', 'HammerSlurmSettings', 'HammerSlurmSubmitCommand']

class HammerSubmitCommand:

    @abstractmethod
    def submit(self, args: List[str], env: Dict[str, str], logger: HammerVLSILoggingContext, cwd: Optional[str]=None) -> Tuple[str, int]:
        """
        Submit the job to the job submission system. This function MUST block
        until the command is complete.

        :param args: Command-line to run; each item in the list is one token.
                     The first token should be the command to run.
        :param env: The environment variables to set for the command
        :param logger: The logging context
        :param cwd: Working directory (leave as None to use the current working directory).
        :return: Tuple of the command output and a return code
        """
        pass

    @abstractmethod
    def read_settings(self, settings: Dict[str, Any], tool_namespace: str) -> None:
        """
        Read the settings object (a Dict[str, Any]) into meaningful class variables.

        :param settings: A Dict[str, Any] comprising the settings for this command.
        :param tool_namespace: The namespace for the tool (useful for logging).
        """
        pass

    @staticmethod
    def get(tool_namespace: str, database: HammerDatabase) -> 'HammerSubmitCommand':
        """
        Get a concrete instance of a HammerSubmitCommand for a tool

        :param tool_namespace: The tool namespace to use when querying the
                               HammerDatabase (e.g. "synthesis" or "par").
        :param database: The HammerDatabase object with tool settings
        """
        pass

    @staticmethod
    def get_program_tag(args: List[str], program_name_length: int=14, arg_display_len: int=16) -> str:
        """
        Get a short "tag" of the program for easier display in the log.
        :param args: Arguments for subprocess
        :param program_name_length: Capture last 14 (default) characters of
                                    the command name.
        :param arg_display_len: How many characters of args to display after prog_name
        :return: Short tag of the program.
        """
        pass

class HammerLocalSubmitCommand(HammerSubmitCommand):

    def submit(self, args: List[str], env: Dict[str, str], logger: HammerVLSILoggingContext, cwd: Optional[str]=None) -> Tuple[str, int]:
        pass

    def read_settings(self, settings: Dict[str, Any], tool_namespace: str) -> None:
        pass

class HammerLSFSettings(NamedTuple('HammerLSFSettings', [('bsub_binary', str), ('num_cpus', Optional[int]), ('queue', Optional[str]), ('log_file', Optional[str]), ('extra_args', List[str])])):
    __slots__ = ()

    @staticmethod
    def from_setting(settings: Dict[str, Any]) -> 'HammerLSFSettings':
        pass

class HammerLSFSubmitCommand(HammerSubmitCommand):

    @property
    def settings(self) -> HammerLSFSettings:
        pass

    @settings.setter
    def settings(self, value: HammerLSFSettings) -> None:
        """
        Set the settings class variable

        :param value: The HammerLSFSettings NapedTuple to use
        """
        pass

    def read_settings(self, settings: Dict[str, Any], tool_namespace: str) -> None:
        pass

    def bsub_args(self) -> List[str]:
        pass

    def submit(self, args: List[str], env: Dict[str, str], logger: HammerVLSILoggingContext, cwd: Optional[str]=None) -> Tuple[str, int]:
        pass

class HammerSlurmSettings(NamedTuple('HammerSlurmSettings', [('srun_binary', str), ('num_cpus', Optional[int]), ('partition', Optional[str]), ('extra_args', Optional[List[str]])])):
    __slots__ = ()

    @staticmethod
    def from_setting(settings: Dict[str, Any]) -> 'HammerSlurmSettings':
        pass

class HammerSlurmSubmitCommand(HammerSubmitCommand):

    @property
    def settings(self) -> HammerSlurmSettings:
        pass

    @settings.setter
    def settings(self, value: HammerSlurmSettings) -> None:
        """
        Set the settings class variable

        :param value: The HammerSlurmSettings NamedTuple to use
        """
        pass

    def read_settings(self, settings: Dict[str, Any], tool_namespace: str) -> None:
        pass

    def srun_args(self) -> List[str]:
        pass

    def submit(self, args: List[str], env: Dict[str, str], logger: HammerVLSILoggingContext, cwd: Optional[str]=None) -> Tuple[str, int]:
        pass
