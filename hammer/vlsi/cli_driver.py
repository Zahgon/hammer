import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
import importlib.resources
import ruamel.yaml
import hammer.config
from .hammer_vlsi_impl import HammerTool, HammerVLSISettings
from .hooks import HammerToolHookAction, HammerStartStopStep
from .driver import HammerDriver, HammerDriverOptions
from .hammer_build_systems import BuildSystems
from functools import reduce
from textwrap import dedent
from typing import List, Dict, Tuple, Any, Callable, Optional, Union, cast
from hammer.utils import add_dicts, deeplist, deepdict, get_or_else, check_function_type
from hammer.config import HammerJSONEncoder
KEY_DIR = tempfile.mkdtemp()
KEY_PATH = os.path.join(KEY_DIR, 'key-history.json')

def parse_optional_file_list_from_args(args_list: Any, append_error_func: Callable[[str], None]) -> List[str]:
    """Parse a possibly null list of files, validate the existence of each file, and return a list of paths (possibly
    empty)."""
    pass

def get_nonempty_str(arg: Any) -> Optional[str]:
    """Either get the non-empty string from the given arg or None if it is not a non-empty string."""
    pass

def dump_config_to_json_file(output_path: str, config: dict) -> None:
    """
    Helper function to dump the given config to the given output path while overwriting it if it already exists.
    :param output_path: Output path (e.g. "obj/output.log")
    :param config: Config dictionary to dump
    """
    pass

def dump_config_to_yaml_file(output_path: str, config: dict) -> None:
    """
    Helper function to dump the given config in YAML form
    to the given output path while overwriting it if it already exists.
    :param output_path: Output path
    :param config: Config dictionary to dump
    """
    pass

def add_key_history(config: dict, history: dict) -> Any:
    """
    Generates a YAML file with comments indicating what files modified said keys.
    """
    pass
CLIActionConfigType = Callable[[HammerDriver, Callable[[str], None]], Optional[dict]]
CLIActionStringType = Callable[[HammerDriver, Callable[[str], None]], Optional[str]]
CLIActionType = Union[CLIActionConfigType, CLIActionStringType]

def is_config_action(func: CLIActionType) -> bool:
    """Return True if the given function is a CLIActionConfigType."""
    pass

def is_string_action(func: CLIActionType) -> bool:
    """Return True if the given function is a CLIActionConfigType."""
    pass

def check_CLIActionType_type(func: CLIActionType) -> None:
    """
    Check that the given CLIActionType obeys its function type signature.
    Raises TypeError if the function is of the incorrect type.
    """
    pass

class CLIDriver:
    """
    Helper class for projects to easily write/customize a CLI driver for hammer without needing to rewrite/copy all the
    argparse and plumbing.
    """

    def __init__(self) -> None:
        self.syn_rundir = ''
        self.par_rundir = ''
        self.drc_rundir = ''
        self.lvs_rundir = ''
        self.sram_generator_rundir = ''
        self.sim_rundir = ''
        self.power_rundir = ''
        self.formal_rundir = ''
        self.timing_rundir = ''
        self.pcb_rundir = ''
        self.synthesis_action: CLIActionConfigType
        if hasattr(self, 'sram_generator_action'):
            check_CLIActionType_type(self.sram_generator_action)
        else:
            self.sram_generator_action = self.create_sram_generator_action([])
        if hasattr(self, 'pcb_action'):
            check_CLIActionType_type(self.pcb_action)
        else:
            self.pcb_action = self.create_pcb_action([])
        if hasattr(self, 'synthesis_action'):
            check_CLIActionType_type(self.synthesis_action)
        else:
            self.synthesis_action = self.create_synthesis_action([])
        if hasattr(self, 'par_action'):
            check_CLIActionType_type(self.par_action)
        else:
            self.par_action = self.create_par_action([])
        if hasattr(self, 'drc_action'):
            check_CLIActionType_type(self.drc_action)
        else:
            self.drc_action = self.create_drc_action([])
        if hasattr(self, 'lvs_action'):
            check_CLIActionType_type(self.lvs_action)
        else:
            self.lvs_action = self.create_lvs_action([])
        if hasattr(self, 'synthesis_par_action'):
            check_CLIActionType_type(self.synthesis_par_action)
        else:
            self.synthesis_par_action = self.create_synthesis_par_action(self.synthesis_action, self.par_action)
        if hasattr(self, 'sim_action'):
            check_CLIActionType_type(self.sim_action)
        else:
            self.sim_action = self.create_sim_action([])
        if hasattr(self, 'synthesis_sim_action'):
            check_CLIActionType_type(self.synthesis_sim_action)
        else:
            self.synthesis_sim_action = self.create_synthesis_sim_action(self.synthesis_action, self.sim_action)
        if hasattr(self, 'par_sim_action'):
            check_CLIActionType_type(self.par_sim_action)
        else:
            self.par_sim_action = self.create_par_sim_action(self.par_action, self.sim_action)
        if hasattr(self, 'power_action'):
            check_CLIActionType_type(self.power_action)
        else:
            self.power_action = self.create_power_action([])
        if hasattr(self, 'formal_action'):
            check_CLIActionType_type(self.formal_action)
        else:
            self.formal_action = self.create_formal_action([])
        if hasattr(self, 'timing_action'):
            check_CLIActionType_type(self.timing_action)
        else:
            self.timing_action = self.create_timing_action([])
        self.hierarchical_synthesis_actions = {}
        self.hierarchical_par_actions = {}
        self.hierarchical_synthesis_par_actions = {}
        self.hierarchical_drc_actions = {}
        self.hierarchical_lvs_actions = {}
        self.hierarchical_sim_actions = {}
        self.hierarchical_power_actions = {}
        self.hierarchical_formal_actions = {}
        self.hierarchical_timing_actions = {}
        self.hierarchical_auto_action = None

    def action_map(self) -> Dict[str, CLIActionType]:
        """Return the mapping of valid actions -> functions for each action of the command-line driver."""
        pass

    @staticmethod
    def dump_action(driver: HammerDriver, append_error_func: Callable[[str], None]) -> Optional[dict]:
        """
        Just dump the parsed project configuration as the output.
        """
        pass

    @staticmethod
    def info_action(driver: HammerDriver, append_error_func: Callable[[str], None]) -> Optional[dict]:
        """
        Return the descripion of any key.
        """
        pass

    @staticmethod
    def dump_macrosizes_action(driver: HammerDriver, append_error_func: Callable[[str], None]) -> Optional[str]:
        """
        Dump macro size information.
        """
        pass

    def get_extra_synthesis_hooks(self) -> List[HammerToolHookAction]:
        """
        Return a list of extra synthesis hooks in this project.
        To be overridden by subclasses.
        """
        pass

    def get_extra_par_hooks(self) -> List[HammerToolHookAction]:
        """
        Return a list of extra place and route hooks in this project.
        To be overridden by subclasses.
        """
        pass

    def get_extra_drc_hooks(self) -> List[HammerToolHookAction]:
        """
        Return a list of extra design-rule-check hooks in this project.
        To be overridden by subclasses.
        """
        pass

    def get_extra_lvs_hooks(self) -> List[HammerToolHookAction]:
        """
        Return a list of extra layout-vs-schematic hooks in this project.
        To be overridden by subclasses.
        """
        pass

    def get_extra_sram_generator_hooks(self) -> List[HammerToolHookAction]:
        """
        Return a list of extra SRAM generation hooks in this project.
        To be overriden by subclasses.
        """
        pass

    def get_extra_sim_hooks(self) -> List[HammerToolHookAction]:
        """
        Return a list of extra simulation hooks in this project.
        To be overridden by subclasses.
        """
        pass

    def get_extra_power_hooks(self) -> List[HammerToolHookAction]:
        """
        Return a list of extra power hooks in this project.
        To be overridden by subclasses.
        """
        pass

    def get_extra_formal_hooks(self) -> List[HammerToolHookAction]:
        """
        Return a list of extra formal hooks in this project.
        To be overridden by subclasses.
        """
        pass

    def get_extra_timing_hooks(self) -> List[HammerToolHookAction]:
        """
        Return a list of extra timing hooks in this project.
        To be overridden by subclasses.
        """
        pass

    def get_extra_pcb_hooks(self) -> List[HammerToolHookAction]:
        """
        Return a list of extra PCB deliverable hooks in this project.
        To be overridden by subclasses.
        """
        pass

    def create_synthesis_action(self, custom_hooks: List[HammerToolHookAction], pre_action_func: Optional[Callable[[HammerDriver], None]]=None, post_load_func: Optional[Callable[[HammerDriver], None]]=None, post_run_func: Optional[Callable[[HammerDriver], None]]=None) -> CLIActionConfigType:
        pass

    def create_par_action(self, custom_hooks: List[HammerToolHookAction], pre_action_func: Optional[Callable[[HammerDriver], None]]=None, post_load_func: Optional[Callable[[HammerDriver], None]]=None, post_run_func: Optional[Callable[[HammerDriver], None]]=None) -> CLIActionConfigType:
        pass

    def create_drc_action(self, custom_hooks: List[HammerToolHookAction], pre_action_func: Optional[Callable[[HammerDriver], None]]=None, post_load_func: Optional[Callable[[HammerDriver], None]]=None, post_run_func: Optional[Callable[[HammerDriver], None]]=None) -> CLIActionConfigType:
        pass

    def create_lvs_action(self, custom_hooks: List[HammerToolHookAction], pre_action_func: Optional[Callable[[HammerDriver], None]]=None, post_load_func: Optional[Callable[[HammerDriver], None]]=None, post_run_func: Optional[Callable[[HammerDriver], None]]=None) -> CLIActionConfigType:
        pass

    def create_sim_action(self, custom_hooks: List[HammerToolHookAction], pre_action_func: Optional[Callable[[HammerDriver], None]]=None, post_load_func: Optional[Callable[[HammerDriver], None]]=None, post_run_func: Optional[Callable[[HammerDriver], None]]=None) -> CLIActionConfigType:
        pass

    def create_power_action(self, custom_hooks: List[HammerToolHookAction], pre_action_func: Optional[Callable[[HammerDriver], None]]=None, post_load_func: Optional[Callable[[HammerDriver], None]]=None, post_run_func: Optional[Callable[[HammerDriver], None]]=None) -> CLIActionConfigType:
        pass

    def create_formal_action(self, custom_hooks: List[HammerToolHookAction], pre_action_func: Optional[Callable[[HammerDriver], None]]=None, post_load_func: Optional[Callable[[HammerDriver], None]]=None, post_run_func: Optional[Callable[[HammerDriver], None]]=None) -> CLIActionConfigType:
        pass

    def create_timing_action(self, custom_hooks: List[HammerToolHookAction], pre_action_func: Optional[Callable[[HammerDriver], None]]=None, post_load_func: Optional[Callable[[HammerDriver], None]]=None, post_run_func: Optional[Callable[[HammerDriver], None]]=None) -> CLIActionConfigType:
        pass

    def create_sram_generator_action(self, custom_hooks: List[HammerToolHookAction], pre_action_func: Optional[Callable[[HammerDriver], None]]=None, post_load_func: Optional[Callable[[HammerDriver], None]]=None, post_run_func: Optional[Callable[[HammerDriver], None]]=None) -> CLIActionConfigType:
        pass

    def create_pcb_action(self, custom_hooks: List[HammerToolHookAction], pre_action_func: Optional[Callable[[HammerDriver], None]]=None, post_load_func: Optional[Callable[[HammerDriver], None]]=None, post_run_func: Optional[Callable[[HammerDriver], None]]=None) -> CLIActionConfigType:
        pass

    def create_action(self, action_type: str, extra_hooks: Optional[List[HammerToolHookAction]], pre_action_func: Optional[Callable[[HammerDriver], None]]=None, post_load_func: Optional[Callable[[HammerDriver], None]]=None, post_run_func: Optional[Callable[[HammerDriver], None]]=None) -> CLIActionConfigType:
        """
        Create an action function for the action_map.

        :param action_type: Either "syn"/"synthesis" or "par"
        :param extra_hooks: List of hooks to pass to the run function.
        :param pre_action_func: Optional function to call before doing anything.
        :param post_load_func: Optional function to call after loading the tool.
        :param post_run_func: Optional function to call after running the tool.
        :return: Action function.
        """
        pass

    def synthesis_to_par_action(self, driver: HammerDriver, append_error_func: Callable[[str], None]) -> Optional[dict]:
        """Create a full config to run the output."""
        pass

    def synthesis_to_sim_action(self, driver: HammerDriver, append_error_func: Callable[[str], None]) -> Optional[dict]:
        """Create a full config to run the output."""
        pass

    def par_to_sim_action(self, driver: HammerDriver, append_error_func: Callable[[str], None]) -> Optional[dict]:
        """Create a full config to run the output."""
        pass

    def hier_par_to_syn_action(self, driver: HammerDriver, append_error_func: Callable[[str], None]) -> Optional[dict]:
        """ Create a full config to run the output. """
        pass

    def par_to_drc_action(self, driver: HammerDriver, append_error_func: Callable[[str], None]) -> Optional[dict]:
        """ Create a full config to run the output. """
        pass

    def par_to_lvs_action(self, driver: HammerDriver, append_error_func: Callable[[str], None]) -> Optional[dict]:
        """ Create a full config to run the output. """
        pass

    def syn_to_power_action(self, driver: HammerDriver, append_error_func: Callable[[str], None]) -> Optional[dict]:
        """Create a full config to run the output."""
        pass

    def par_to_power_action(self, driver: HammerDriver, append_error_func: Callable[[str], None]) -> Optional[dict]:
        """Create a full config to run the output."""
        pass

    def sim_to_power_action(self, driver: HammerDriver, append_error_func: Callable[[str], None]) -> Optional[dict]:
        """Create a full config to run the output."""
        pass

    def synthesis_to_formal_action(self, driver: HammerDriver, append_error_func: Callable[[str], None]) -> Optional[dict]:
        """Create a full config to run the output."""
        pass

    def par_to_formal_action(self, driver: HammerDriver, append_error_func: Callable[[str], None]) -> Optional[dict]:
        """Create a full config to run the output."""
        pass

    def synthesis_to_timing_action(self, driver: HammerDriver, append_error_func: Callable[[str], None]) -> Optional[dict]:
        """Create a full config to run the output."""
        pass

    def par_to_timing_action(self, driver: HammerDriver, append_error_func: Callable[[str], None]) -> Optional[dict]:
        """Create a full config to run the output."""
        pass

    def create_synthesis_par_action(self, synthesis_action: CLIActionConfigType, par_action: CLIActionConfigType) -> CLIActionConfigType:
        """
        Create a parameterizable synthesis_par action for the CLIDriver.

        :param synthesis_action: synthesis action
        :param par_action: par action
        :return: Custom synthesis_par action
        """
        pass

    def create_synthesis_sim_action(self, synthesis_action: CLIActionConfigType, sim_action: CLIActionConfigType) -> CLIActionConfigType:
        """
        Create a parameterizable synthesis_sim action for the CLIDriver.

        :param synthesis_action: synthesis action
        :param sim_action: sim action
        :return: Custom synthesis_sim action
        """
        pass

    def create_par_sim_action(self, par_action: CLIActionConfigType, sim_action: CLIActionConfigType) -> CLIActionConfigType:
        """
        Create a parameterizable par_sim action for the CLIDriver.

        :param par_action: par action
        :param sim_action: sim action
        :return: Custom par_sim action
        """
        pass

    @property
    def all_hierarchical_actions(self) -> Dict[str, CLIActionConfigType]:
        """
        Return a list of hierarchical actions if the given project configuration is a hierarchical design.
        Set when the driver is first created in args_to_driver.
        Create syn/synthesis-[block], par-[block], and /syn_par-[block].

        :return: Dictionary of actions to use (could be empty).
        """
        pass

    def get_extra_hierarchical_synthesis_hooks(self, driver: HammerDriver) -> Dict[str, List[HammerToolHookAction]]:
        """
        Return a list of extra hierarchical synthesis hooks in this project.
        To be overridden by subclasses.

        :return: Dictionary of (module name, list of hooks)
        """
        pass

    def get_extra_hierarchical_par_hooks(self, driver: HammerDriver) -> Dict[str, List[HammerToolHookAction]]:
        """
        Return a list of extra hierarchical place and route hooks in this project.
        To be overridden by subclasses.

        :return: Dictionary of (module name, list of hooks)
        """
        pass

    def get_extra_hierarchical_drc_hooks(self, driver: HammerDriver) -> Dict[str, List[HammerToolHookAction]]:
        """
        Return a list of extra hierarchical DRC hooks in this project.
        To be overridden by subclasses.

        :return: Dictionary of (module name, list of hooks)
        """
        pass

    def get_extra_hierarchical_lvs_hooks(self, driver: HammerDriver) -> Dict[str, List[HammerToolHookAction]]:
        """
        Return a list of extra hierarchical LVS hooks in this project.
        To be overridden by subclasses.

        :return: Dictionary of (module name, list of hooks)
        """
        pass

    def get_extra_hierarchical_sim_hooks(self, driver: HammerDriver) -> Dict[str, List[HammerToolHookAction]]:
        """
        Return a list of extra hierarchical sim hooks in this project.
        To be overridden by subclasses.

        :return: Dictionary of (module name, list of hooks)
        """
        pass

    def get_extra_hierarchical_power_hooks(self, driver: HammerDriver) -> Dict[str, List[HammerToolHookAction]]:
        """
        Return a list of extra hierarchical power hooks in this project.
        To be overridden by subclasses.

        :return: Dictionary of (module name, list of hooks)
        """
        pass

    def get_extra_hierarchical_formal_hooks(self, driver: HammerDriver) -> Dict[str, List[HammerToolHookAction]]:
        """
        Return a list of extra hierarchical formal hooks in this project.
        To be overridden by subclasses.

        :return: Dictionary of (module name, list of hooks)
        """
        pass

    def get_extra_hierarchical_timing_hooks(self, driver: HammerDriver) -> Dict[str, List[HammerToolHookAction]]:
        """
        Return a list of extra hierarchical timing hooks in this project.
        To be overridden by subclasses.

        :return: Dictionary of (module name, list of hooks)
        """
        pass

    def get_hierarchical_synthesis_action(self, module: str) -> CLIActionConfigType:
        """
        Get the action associated with hierarchical synthesis for the given module (in hierarchical flows).
        """
        pass

    def set_hierarchical_synthesis_action(self, module: str, action: CLIActionConfigType) -> None:
        """
        Set the action associated with hierarchical synthesis for the given module (in hierarchical flows).
        """
        pass

    def get_hierarchical_par_action(self, module: str) -> CLIActionConfigType:
        """
        Get the action associated with hierarchical par for the given module (in hierarchical flows).
        """
        pass

    def set_hierarchical_par_action(self, module: str, action: CLIActionConfigType) -> None:
        """
        Set the action associated with hierarchical par for the given module (in hierarchical flows).
        """
        pass

    def set_hierarchical_drc_action(self, module: str, action: CLIActionConfigType) -> None:
        """
        Set the action associated with hierarchical drc for the given module (in hierarchical flows).
        """
        pass

    def get_hierarchical_drc_action(self, module: str) -> CLIActionConfigType:
        """
        Get the action associated with hierarchical drc for the given module (in hierarchical flows).
        """
        pass

    def set_hierarchical_lvs_action(self, module: str, action: CLIActionConfigType) -> None:
        """
        Set the action associated with hierarchical lvs for the given module (in hierarchical flows).
        """
        pass

    def get_hierarchical_lvs_action(self, module: str) -> CLIActionConfigType:
        """
        Get the action associated with hierarchical lvs for the given module (in hierarchical flows).
        """
        pass

    def get_hierarchical_synthesis_par_action(self, module: str) -> CLIActionConfigType:
        """
        Get the action associated with hierarchical syn_par for the given module (in hierarchical flows).
        """
        pass

    def set_hierarchical_synthesis_par_action(self, module: str, action: CLIActionConfigType) -> None:
        """
        Set the action associated with hierarchical syn_par for the given module (in hierarchical flows).
        """
        pass

    def set_hierarchical_sim_action(self, module: str, action: CLIActionConfigType) -> None:
        """
        Set the action associated with hierarchical sim for the given module (in hierarchical flows).
        """
        pass

    def get_hierarchical_sim_action(self, module: str) -> CLIActionConfigType:
        """
        Get the action associated with hierarchical sim for the given module (in hierarchical flows).
        """
        pass

    def set_hierarchical_power_action(self, module: str, action: CLIActionConfigType) -> None:
        """
        Set the action associated with hierarchical power for the given module (in hierarchical flows).
        """
        pass

    def get_hierarchical_power_action(self, module: str) -> CLIActionConfigType:
        """
        Get the action associated with hierarchical power for the given module (in hierarchical flows).
        """
        pass

    def set_hierarchical_formal_action(self, module: str, action: CLIActionConfigType) -> None:
        """
        Set the action associated with hierarchical formal for the given module (in hierarchical flows).
        """
        pass

    def get_hierarchical_formal_action(self, module: str) -> CLIActionConfigType:
        """
        Get the action associated with hierarchical formal for the given module (in hierarchical flows).
        """
        pass

    def set_hierarchical_timing_action(self, module: str, action: CLIActionConfigType) -> None:
        """
        Set the action associated with hierarchical timing for the given module (in hierarchical flows).
        """
        pass

    def get_hierarchical_timing_action(self, module: str) -> CLIActionConfigType:
        """
        Get the action associated with hierarchical timing for the given module (in hierarchical flows).
        """
        pass

    def valid_actions(self) -> List[str]:
        """Get the list of valid actions for the command-line driver."""
        pass

    @staticmethod
    def get_full_config(driver: HammerDriver, output: dict) -> dict:
        """
        Get the full configuration by combining the project config from the
        driver with the given output dict (i.e. it contains only
        "synthesis.output.blah") that we want to combine with the project
        config.
        :param driver: HammerDriver that has the full project config.
        :param output: Output dict containing specific settings we want to add
                       to the full project config.
        :return: Full project config combined with the output dict
        """
        pass

    def args_to_driver(self, args: dict, default_options: Optional[HammerDriverOptions]=None) -> Tuple[HammerDriver, List[str]]:
        """Parse command line arguments and environment variables for the command line front-end to hammer-vlsi.

        :return: HammerDriver and a list of errors."""
        pass

    @staticmethod
    def generate_build_inputs(driver: HammerDriver, append_error_func: Callable[[str], None]) -> Optional[dict]:
        """
        Generate the build tool artifacts for this flow, specified by the "vlsi.core.build_system" key.
        The flow is the set of steps configured by the current HammerIR input.

        :param driver: The HammerDriver object which has parsed the configs specified by -p
        :param append_error_func: The function to use to append an error
        :return: The diplomacy graph
        """
        pass

    def run_main_parsed(self, args: dict) -> int:
        """
        Given a parsed dictionary of arguments, find and run the given action.

        :return: Return code (0 for success)
        """
        pass

    def main(self, args: Optional[List[str]]=None) -> None:
        """
        Main function to call from your entry point script.
        Parses command line arguments.
        :param args: Custom command-line arguments.  If not given, sys.argv[1:] will be used.
        Example:
        >>> if __name__ == '__main__':
        >>>   CLIDriver().main()
        """
        pass
