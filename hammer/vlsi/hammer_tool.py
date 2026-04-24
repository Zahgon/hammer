import inspect
import os
import re
import shlex
from abc import ABCMeta, abstractmethod
from functools import reduce
from typing import Any, Callable, Dict, Iterable, List, Optional, Set, Tuple, cast
from inspect import cleandoc
from pathlib import Path
import hammer.config as hammer_config
import hammer.tech as hammer_tech
from hammer.logging import HammerVLSILoggingContext
from hammer.tech import LibraryFilter, Stackup, RoutingDirection, Metal
from hammer.utils import add_lists, assert_function_type, get_or_else, optional_map, LEFUtils
from .constraints import *
from .hammer_vlsi_impl import HierarchicalMode
from .hooks import HammerStepFunction, HammerToolHookAction, HammerToolStep, HookLocation, HammerStartStopStep
from .submit_command import HammerSubmitCommand
from .units import TemperatureValue, TimeValue, VoltageValue, CapacitanceValue
__all__ = ['HammerTool']

def make_raw_hammer_tool_step(func: HammerStepFunction, name: str) -> HammerToolStep:
    pass

def check_hammer_step_function(func: HammerStepFunction) -> None:
    """Internal alias for checking HammerStepFunction signatures."""
    pass

class HammerTool(metaclass=ABCMeta):

    @property
    def env_vars(self) -> Dict[str, str]:
        """
        Get the list of environment variables required for this tool.
        Note to subclasses: remember to include variables from super().env_vars!

        :return: Mapping of environment variable -> contents of said variable.
        """
        pass

    def export_config_outputs(self) -> Dict[str, Any]:
        """
        Export the outputs of this tool to a config.
        By default, this just adds a flag to indicate that the output fragment
        is output-only/not complete.

        Warning: any subclasses must call this method in the base class
        so that all output configs get added correctly.

        :return: Config dictionary of the outputs of this tool.
        """
        pass

    @abstractmethod
    def tool_config_prefix(self) -> str:
        """
        Returns the config prefix that contains all tool specific settings.
        e.g. "synthesis.yosys".

        :return: A string that is the prefix for all tool specific settings.
        """
        pass

    def version(self) -> int:
        """
        Returns the version number of the current tool version, using version_number
        below.

        :return: The version number of the current tool.
        """
        pass

    @abstractmethod
    def version_number(self, version: str) -> int:
        """
        Based on the tool, figures out an integer value for the version number.

        :param version: The version number given by the tool vendor.
        :return: An integer representing the version suitable for comparisons.
        """
        pass

    def run(self, hook_actions: List[HammerToolHookAction]=[]) -> bool:
        """Run this tool.

        Perform some setup operations to set up the config and tool environment, runs the tool-specific actions defined
        in steps, and collects the outputs.

        :return: True if the tool finished successfully; false otherwise.
        """
        pass

    @property
    @abstractmethod
    def steps(self) -> List[HammerToolStep]:
        """
        List of steps defined for the execution of this tool.
        """
        pass

    @property
    def first_step(self) -> HammerToolStep:
        """
        The first non-persistent step after hooks resolution.

        :return: The first non-persistent step to be run.
        """
        pass

    @first_step.setter
    def first_step(self, step: HammerToolStep) -> None:
        """Set the first non-persistent step to be run."""
        pass

    @property
    def persistent_steps(self) -> List[HammerToolHookAction]:
        """
        List of persistent steps for this tool.

        :return: List of persistent hooks.
        """
        pass

    @persistent_steps.setter
    def persistent_steps(self, hooks: List[HammerToolHookAction]) -> None:
        """Set the List of persistent hooks."""
        pass

    def run_persistent_step(self, pst: HammerToolHookAction, target_step: HammerToolStep) -> bool:
        pass

    def do_pre_steps(self, first_step: HammerToolStep) -> bool:
        """
        Function to run before the list of steps executes.
        Intended to be overriden by subclasses.
        Note: if you override this, remember to call the superclass method too!

        :param first_step: First step to be taken.
        :return: True if successful, False otherwise.
        """
        pass

    def do_between_steps(self, prev: HammerToolStep, next: HammerToolStep) -> bool:
        """
        Function to run between the execution of two steps.
        Does not include pause hooks.
        Intended to be overridden by subclasses.

        :param prev: The step that just finished
        :param next: The next step about to run.
        :return: True if successful, False otherwise.
        """
        pass

    def do_post_steps(self) -> bool:
        """
        Function to run after the list of steps executes.
        Intended to be overridden by subclasses.

        :return: True if successful, False otherwise.
        """
        pass

    def fill_outputs(self) -> bool:
        """
        Fill the outputs of the tool.
        Note: if you override this, remember to call the superclass method too!

        :return: True if successful, False otherwise.
        """
        pass

    @property
    def _subprocess_env(self) -> dict:
        """
        Internal helper function to set the environment variables for
        self.run_executable().
        """
        pass

    @property
    def name(self) -> str:
        """
        Short name of the tool library.
        Typically the folder name (e.g. "dc", "yosys", etc).

        :return: Short name of the tool library.
        """
        pass

    @name.setter
    def name(self, value: str) -> None:
        """Set the Short name of the tool library."""
        pass

    @property
    def package(self) -> str:
        """
        Get the top-level package of this tool (e.g. "hammer.synthesis.nop")
        """
        pass

    @package.setter
    def package(self, package: str) -> None:
        pass

    @property
    def run_dir(self) -> str:
        """
        Get the location of the run dir, a writable temporary information for use by the tool.
        This should return an absolute path.

        :return: Path to the location of the library.
        """
        pass

    @run_dir.setter
    def run_dir(self, path: str) -> None:
        """Set the location of a writable directory which the tool can use to store temporary information."""
        pass

    @property
    def input_files(self) -> List[str]:
        """
        Input files for this tool library.
        The exact nature of the files will depend on the type of library.
        """
        pass

    @input_files.setter
    def input_files(self, value: List[str]) -> None:
        """
        Set the input files for this tool library.
        The exact nature of the files will depend on the type of library.
        """
        pass

    @property
    def hierarchical_mode(self) -> HierarchicalMode:
        """
        Input files for this tool library.
        The exact nature of the files will depend on the type of library.
        """
        pass

    @hierarchical_mode.setter
    def hierarchical_mode(self, value: HierarchicalMode) -> None:
        """
        Set the input files for this tool library.
        The exact nature of the files will depend on the type of library.
        """
        pass

    @property
    def technology(self) -> hammer_tech.HammerTechnology:
        """
        Get the technology library currently in use.

        :return: HammerTechnology instance
        """
        pass

    @technology.setter
    def technology(self, value: hammer_tech.HammerTechnology) -> None:
        """Set the HammerTechnology currently in use."""
        pass

    @property
    def submit_command(self) -> HammerSubmitCommand:
        """
        Get the submit command used by this tool

        :return HammerSubmitCommand instance
        """
        pass

    @submit_command.setter
    def submit_command(self, value: HammerSubmitCommand) -> None:
        """
        Set the submit command used by this tool

        :value: HammerSubmitCommand instance
        """
        pass

    @property
    def top_module(self) -> str:
        """
        Get the top-level module.

        :return: The top-level module.
        """
        pass

    @top_module.setter
    def top_module(self, value: str) -> None:
        """Set the top-level module."""
        pass

    @property
    def logger(self) -> HammerVLSILoggingContext:
        """Get the logger for this tool."""
        pass

    @logger.setter
    def logger(self, value: HammerVLSILoggingContext) -> None:
        """Set the logger for this tool."""
        pass

    def attr_getter(self, key: str, default: Any) -> Any:
        """Helper function for implementing the getter of a property with a default.
        If default is None, then raise a AttributeError."""
        pass

    def attr_setter(self, key: str, value: Any) -> None:
        """Helper function for implementing the setter of a property with a default."""
        pass

    def get_tool_hooks(self) -> List[HammerToolHookAction]:
        """
        Get any hooks specific to the tool.
        To be overridden by subclasses that need to implement persistent hooks.
        """
        pass

    def check_duplicates(self, lst: List[HammerToolStep]) -> Tuple[bool, Set[str]]:
        """Check that no two steps have the same name."""
        pass

    def run_steps(self, steps: List[HammerToolStep], hook_actions: List[HammerToolHookAction]=[]) -> bool:
        """
        Run the given steps, checking for errors/conditions between each step.

        :param steps: List of steps.
        :param hook_actions: List of hook actions.
        :return: Returns true if all the steps are successful.
        """
        pass

    @staticmethod
    def make_step_from_method(func: Callable[[], bool], name: str='') -> HammerToolStep:
        """
        Create a HammerToolStep from a method.

        :param func: Method for the given substep (e.g. self.elaborate)
        :param name: Name of the hook. If unspecified, defaults to func.__name__.
        :return: A HammerToolStep defining this step.
        """
        pass

    @staticmethod
    def make_steps_from_methods(funcs: List[Callable[[], bool]]) -> List[HammerToolStep]:
        """
        Create a series of HammerToolStep from the given list of bound methods.

        :param funcs: List of bound methods (e.g. [self.step1, self.step2])
        :return: List of HammerToolSteps
        """
        pass

    @staticmethod
    def make_step_from_function(func: HammerStepFunction, name: str='') -> HammerToolStep:
        """
        Create a HammerToolStep from a function.

        :param func: Class function for the given substep
        :param name: Name of the hook. If unspecified, defaults to func.__name__.
        :return: A HammerToolStep defining this step.
        """
        pass

    @staticmethod
    def make_replacement_hook(step: str, func: HammerStepFunction) -> HammerToolHookAction:
        """
        Create a hook action which replaces an existing step.

        :return: Hook action which replaces the given step.
        """
        pass

    @staticmethod
    def make_insertion_hook(step: str, location: HookLocation, func: HammerStepFunction) -> HammerToolHookAction:
        """
        Create a hook action is inserted relative to the given step.
        """
        pass

    @staticmethod
    def make_resume_pause_hook(step: str, location: HookLocation) -> HammerToolHookAction:
        """
        Create a hook action which will start/stop the execution of the tool at/after the given step.

        :param step: The target step that bounds of the steps to run.
        :param location: Encodes whether this hook will cause a resume/pause pre/post the target step.
        """
        pass

    @staticmethod
    def make_pre_pause_hook(step: str) -> HammerToolHookAction:
        """
        Create pause before the execution of the given step.
        Note that only one pause hook may be present.
        """
        pass

    @staticmethod
    def make_post_pause_hook(step: str) -> HammerToolHookAction:
        """
        Create pause before the execution of the given step.
        Note that only one pause hook may be present.
        """
        pass

    @staticmethod
    def make_pre_resume_hook(step: str) -> HammerToolHookAction:
        """
        Resume before the given step.
        Note that only one resume hook may be present.
        """
        pass

    @staticmethod
    def make_post_resume_hook(step: str) -> HammerToolHookAction:
        """
        Resume after the given step.
        Note that only one resume hook may be present.
        """
        pass

    @staticmethod
    def make_start_stop_hooks(start: HammerStartStopStep, stop: HammerStartStopStep) -> List[HammerToolHookAction]:
        """
        Helper function to create a HammerToolHookAction list which will run from/after and to/until the given steps.
        The inclusive ones take priority in the event that incompatible options are called.

        :param start: HammerStartStopStep that defines where to resume from
        :param stop: HammerStartStopStep that define where to pause at
        :return: HammerToolHookAction list for running from and to the given steps, inclusive.
        """
        pass

    @staticmethod
    def make_pre_insertion_hook(step: str, func: HammerStepFunction) -> HammerToolHookAction:
        """
        Create a hook action is inserted prior to the given step.
        """
        pass

    @staticmethod
    def make_post_insertion_hook(step: str, func: HammerStepFunction) -> HammerToolHookAction:
        """
        Create a hook action is inserted after the given step.
        """
        pass

    @staticmethod
    def make_removal_hook(step: str) -> HammerToolHookAction:
        """
        Helper function to remove a step by replacing it with an empty step.

        :return: Hook action which replaces the given step.
        """
        pass

    @staticmethod
    def make_persistent_hook(func: HammerStepFunction) -> HammerToolHookAction:
        """
        Helper function to always insert a step at the beginning.

        :return: Hook action which is inserted at the beginning of the list of steps
        """
        pass

    @staticmethod
    def make_pre_persistent_hook(step: str, func: HammerStepFunction) -> HammerToolHookAction:
        """
        Helper function to always insert a step at the beginning,
        when the steps to be executed are all before the given step.

        :return: Hook action which is inserted at the beginning of the list of steps
        """
        pass

    @staticmethod
    def make_post_persistent_hook(step: str, func: HammerStepFunction) -> HammerToolHookAction:
        """
        Helper function to always insert a step at the beginning,
        when the steps to be executed are all after the given step.

        :return: Hook action which is inserted at the beginning of the list of steps
        """
        pass

    def set_database(self, database: hammer_config.HammerDatabase) -> None:
        """Set the settings database for use by the tool."""
        pass

    def dump_database(self) -> str:
        """Dump the current database JSON in a temporary file in the run_dir and return the path.
        """
        pass

    def get_config(self) -> Tuple[List[dict], List[dict]]:
        """Get the config for this tool."""
        pass

    def get_setting(self, key: str, nullvalue: Any=None) -> Any:
        """
        Get a particular setting from the database.

        :param key: Key of the setting to receive.
        :param nullvalue: Value to return in case of null (leave as None to use the default).
        """
        pass

    def get_setting_suffix(self, key: str, suffix: str, nullvalue: Any=None) -> Any:
        """
        Get a particular setting from the database with a suffix.

        :param key: Key of the setting to receive.
        :param suffix: Suffix to search for on top of the base.
        :param nullvalue: Value to return in case of null (leave as None to use the default).
        """
        pass

    def set_setting(self, key: str, value: Any) -> None:
        """
        Set a runtime setting in the database.
        """
        pass

    def get_settings_from_dict(self, key_default_dict: Dict[str, Any], key_prefix: str='', optional_keys: List[str]=[]) -> Dict[str, str]:
        """
        Gets input values for multiple keys.
        """
        pass

    def create_enter_script(self, enter_script_location: str='', raw: bool=False) -> None:
        """
        Create the enter script inside the rundir which can be used to
        create an interactive environment with all the same variables
        used to launch this tool.

        :param enter_script_location: Location to create the enter script. Defaults to self.run_dir + "/enter"
        :param raw: Emit the raw string without shell escaping (without quotes!!!)
        """
        pass

    def check_input_files(self, extensions: List[str]) -> bool:
        """Verify that input files exist and have the specified extensions.

        :param extensions: List of extensions e.g. [".v", ".sv"]
        :return: True if all files exist and have the specified extensions.
        """
        pass

    def filter_for_mmmc(self, voltage: VoltageValue, temp: TemperatureValue) -> Callable[[hammer_tech.Library], bool]:
        """
        Selecting libraries that match given temp and voltage.
        """
        pass

    @staticmethod
    def replace_tcl_set(variable: str, value: str, tcl_path: str, quotes: bool=True) -> None:
        """
        Utility function to replaces a "set VARIABLE ..." line with set VARIABLE
        "value" in the given TCL script file.

        :param variable: Variable name to replace
        :param value: Value to replace it with (default quoted)
        :param tcl_path: Path to the TCL script.
        :param quotes: (optional) Set to False to disable quoting of the value.
        """
        pass

    def run_executable(self, args: List[str], cwd: Optional[str]=None) -> str:
        """
        Run an executable and log the command to the log while also capturing the output.

        :param args: Command-line to run; each item in the list is one token. The first token should be the command to run.
        :param cwd: Working directory (leave as None to use the current working directory).
        :return: Output from the command or an error message.
        """
        pass

    def handle_errors(self, output: str, code: int) -> bool:
        """
        Function to run on tool error (nonzero return code).
        Intended to be overridden by subclasses.

        :return: True if successful, False otherwise.
        """
        pass

    def get_clock_ports(self) -> List[ClockPort]:
        """
        Get the clock ports of the top-level module, as specified in vlsi.inputs.clocks.
        """
        pass

    def get_time_unit(self) -> TimeValue:
        """
        Return the library time value.
        """
        pass

    def get_cap_unit(self) -> CapacitanceValue:
        """
        Return the library capacitance value.
        """
        pass

    def get_all_supplies(self, key: str) -> List[Supply]:
        pass

    def get_all_power_nets(self) -> List[Supply]:
        pass

    def get_independent_power_nets(self) -> List[Supply]:
        pass

    def get_all_ground_nets(self) -> List[Supply]:
        pass

    def get_independent_ground_nets(self) -> List[Supply]:
        pass

    def _get_by_bump_dim_pitch(self) -> Dict[str, float]:
        """
        Return pitches in the x and y directions.
        """
        pass

    def get_bumps(self) -> Optional[BumpsDefinition]:
        pass

    def generate_visualization(self) -> None:
        """
        Generate an SVG visualizing the chip.
        Depending on mode, it will display floorplan (placement constraints for the current hierarchy)
        and/or bumps (overlaid on top of floorplan) and pad designators (if this tool is a PCBDeliverableTool).
        Call this from any custom hook (not used by any default flow).
        Note: visualizations generated within a PCBDeliverableTool are mirrored about the y-axis (assumption: flip-chip on PCB)
        """
        pass

    def get_pin_assignments(self) -> List[PinAssignment]:
        """
        Get a list of pin assignments in accordance with settings in the Hammer IR.
        :return: A potentially empty list of PinAssigments.
        """
        pass

    def get_gds_map_file(self) -> Optional[str]:
        """
        Get a GDS map in accordance with settings in the Hammer IR.
        Return a fully-resolved (i.e. already prepended path) path to the GDS map or None if none was specified.
        :return: Fully-resolved path to GDS map file or None.
        """
        pass

    def get_physical_only_cells(self) -> List[str]:
        """
        Get a list of physical only cells in accordance with settings in the Hammer IR.
        Return a list of cells which are physical only.
        :return: A list of physical only cells.
        """
        pass

    def get_dont_use_list(self) -> List[str]:
        """
        Get a "don't use" list in accordance with settings in the Hammer IR.
        Return a list of cells to mark as "don't use".
        :return: A list of cells to avoid using.
        """
        pass

    def get_placement_constraints(self) -> List[PlacementConstraint]:
        """
        Get a list of placement constraints as specified in the config.
        """
        pass

    def get_mmmc_corners(self) -> List[MMMCCorner]:
        """
        Get a list of MMMC corners as specified in the config.
        """
        pass

    def get_stackup(self) -> Stackup:
        """
        Get the stackup provided by the technology key
        """
        pass

    def get_input_ilms(self, full_tree=False) -> List[ILMStruct]:
        """
        Get a list of input ILM modules for hierarchical mode.
        :param full_tree: if true, obtains the full tree (up to the current level of hierarchy) from vlsi.inputs.ilms.
        Otherwise, obtains only children ilms from par.outputs.output_ilms
        """
        pass

    def get_output_load_constraints(self) -> List[OutputLoadConstraint]:
        """
        Get a list of output load constraints as specified in the config.
        """
        pass

    def get_delay_constraints(self) -> List[DelayConstraint]:
        """
        Get a list of input and output delay constraints as specified in
        the config.
        """
        pass

    def get_decap_constraints(self) -> List[DecapConstraint]:
        """
        Get a list of decapacitance constraints as specified in
        the config.
        """
        pass

    @property
    def header(self) -> str:
        """
        Header text for files.
        Intended to be overridden by subclasses if syntax- or vendor-specific headers are necessary.
        """
        pass

    def write_contents_to_path(self, content_to_write: str, target_path: str, append: bool=False) -> None:
        """
        Write or optionally append the given contents to the file located at target_path, if target_path is not empty.

        :param content_to_write: Content to write.
        :param target_path: Where to write the content.
        :param append: True if you want to append to the file, else overwrite it with a header + content_to_write.
        """
        pass

    @staticmethod
    def tcl_append(cmd: str, output_buffer: List[str], clean: bool=False) -> None:
        """
        Helper function to echo and run a command.

        :param cmd: TCL command to run
        :param output_buffer: Buffer in which to enqueue the resulting TCL lines
        :param clean: True if you want to trim the leading indendation from the string, False otherwise. See inspect.cleandoc() for what this does.
        >>>
        """
        pass

    @staticmethod
    def verbose_tcl_append(cmd: str, output_buffer: List[str], clean: bool=False) -> None:
        """
        Helper function to echo and run a command.

        :param cmd: TCL command to run
        :param output_buffer: Buffer in which to enqueue the resulting TCL lines
        :param clean: True if you want to trim the leading indendation from the string, False otherwise. See inspect.cleandoc() for what this does.
        """
        pass

    @staticmethod
    def block_tcl_append(cmds: str, output_buffer: List[str], clean: bool=False, verbose: bool=True) -> None:
        """
        Helper function to echo and run a command.

        :param cmd: TCL command to run
        :param output_buffer: Buffer in which to enqueue the resulting TCL lines
        :param clean: True if you want to trim the leading indendation from the string, False otherwise. See inspect.cleandoc() for what this does.
        """
        pass
