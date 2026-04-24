from functools import reduce, partial
from typing import NamedTuple, List, Optional, Tuple, Dict, Set, Any
from pathlib import Path
import datetime
import importlib
import os
from hammer.utils import *
import hammer.config as hammer_config
import hammer.tech as hammer_tech
from hammer.tech import MacroSize
from .hammer_tool import HammerTool
from .hooks import HammerToolHookAction
from .hammer_vlsi_impl import HammerVLSISettings, HammerPlaceAndRouteTool, HammerSynthesisTool, HammerSignoffTool, HammerDRCTool, HammerLVSTool, HammerSRAMGeneratorTool, HammerPCBDeliverableTool, HammerSimTool, HammerPowerTool, HammerFormalTool, HammerTimingTool, HierarchicalMode, load_tool, PlacementConstraint, SRAMParameters, ILMStruct, FlowLevel
from hammer.logging import HammerVLSIFileLogger, HammerVLSILogging, HammerVLSILoggingContext
from .submit_command import HammerSubmitCommand
__all__ = ['HammerDriverOptions', 'HammerDriver']
HammerDriverOptions = NamedTuple('HammerDriverOptions', [('environment_configs', List[str]), ('project_configs', List[str]), ('log_file', str), ('obj_dir', str)])

class HammerDriver:

    @staticmethod
    def get_default_driver_options() -> HammerDriverOptions:
        """Get default driver options."""
        pass

    def __init__(self, options: HammerDriverOptions, extra_project_config: dict={}) -> None:
        """
        Create a hammer-vlsi driver, which is a higher level convenience function
        for quickly using hammer-vlsi. It imports and uses the hammer-vlsi blocks.

        Set up logging, databases, context, etc.

        :param options: Driver options.
        :param extra_project_config: An extra flattened config for the project. Optional.
        """
        file_logger = HammerVLSIFileLogger(options.log_file)
        HammerVLSILogging.add_callback(file_logger.callback)
        self.log = HammerVLSILogging.context()
        self.database = hammer_config.HammerDatabase()
        self.log.info('Loading hammer-vlsi libraries and reading settings')
        self.obj_dir = options.obj_dir
        self.options = options
        HammerVLSISettings.load_builtins_and_core(self.database)
        for config in options.environment_configs:
            if not os.path.exists(config):
                self.log.error('Environment config %s does not exist!' % config)
            config_str = Path(config).read_text()
            is_yaml = config.endswith('.yml')
            self.database.update_environment([hammer_config.load_config_from_string(config_str, is_yaml, str(Path(config).resolve().parent))])
        project_configs: List[dict] = []
        for config in options.project_configs:
            if not os.path.exists(config):
                self.log.error('Project config %s does not exist!' % config)
            config_str = Path(config).read_text()
            is_yaml = config.endswith('.yml')
            project_configs.append(hammer_config.load_config_from_string(config_str, is_yaml, str(Path(config).resolve().parent)))
        project_configs.append(extra_project_config)
        self.project_configs = []
        self.update_project_configs(project_configs)
        self.tech = None
        self.load_technology()
        self.tool_configs = {}
        self.tool_config_types = {}
        self.syn_tool = None
        self.par_tool = None
        self.drc_tool = None
        self.lvs_tool = None
        self.sram_generator_tool = None
        self.sim_tool = None
        self.power_tool = None
        self.formal_tool = None
        self.timing_tool = None
        self.post_custom_syn_tool_hooks = []
        self.post_custom_par_tool_hooks = []
        self.post_custom_drc_tool_hooks = []
        self.post_custom_lvs_tool_hooks = []
        self.post_custom_sram_generator_tool_hooks = []
        self.post_custom_sim_tool_hooks = []
        self.post_custom_power_tool_hooks = []
        self.post_custom_formal_tool_hooks = []
        self.post_custom_timing_tool_hooks = []
        self.post_custom_pcb_tool_hooks = []
        self._dump_history = False

    @property
    def project_config(self) -> dict:
        pass

    def update_project_configs(self, project_configs: List[dict]) -> None:
        """
        Update the project configs in the driver and database.
        """
        pass

    def load_technology(self, cache_dir: str='') -> None:
        pass

    def update_tool_configs(self) -> None:
        """
        Calls self.database.update_tools with self.tool_configs as a list.
        """
        pass

    def instantiate_tool_from_config(self, tool_type: str, required_type: Optional[type]=None) -> Optional[Tuple[HammerTool, str]]:
        """
        Create a new instance of the given tool using information from the config.
        :param tool_type: Tool type. e.g. if "par", then this will look in vlsi.core.par_tool
        :param required_type: (optional) Check that the instantiated tool is the given type.
        :return: Tuple of (tool instance, tool name) or
                 None if an error occurred.
        """
        pass

    def set_up_synthesis_tool(self, syn_tool: HammerSynthesisTool, name: str, run_dir: str='') -> bool:
        """
        Set up and store the given synthesis tool instance for use in this
        driver.
        :param syn_tool: Tool instance.
        :param name: Short name (e.g. "yosys") of the tool instance. Typically
                     obtained from the database.
        :param run_dir: Directory to use for the tool run_dir. Defaults to the
                        run_dir passed in the HammerDriver constructor.
        :return: True if setup was successful.
        """
        pass

    def load_synthesis_tool(self, run_dir: str='') -> bool:
        """
        Load the synthesis tool based on the given database.

        :param run_dir: Directory to use for the tool run_dir. Defaults to the run_dir passed in the HammerDriver
                        constructor.
        :return: True if synthesis tool loading was successful, False otherwise.
        """
        pass

    def set_up_par_tool(self, par_tool: HammerPlaceAndRouteTool, name: str, run_dir: str='') -> bool:
        """
        Set up and store the given place-and-route tool instance for use in this
        driver.
        :param par_tool: Tool instance.
        :param name: Short name (e.g. "yosys") of the tool instance. Typically
                     obtained from the database.
        :param run_dir: Directory to use for the tool run_dir. Defaults to the
                        run_dir passed in the HammerDriver constructor.
        :return: True if setup was successful.
        """
        pass

    def load_par_tool(self, run_dir: str='') -> bool:
        """
        Load the place and route tool based on the given database.

        :param run_dir: Directory to use for the tool run_dir. Defaults to the run_dir passed in the HammerDriver
                        constructor.
        :return: True if successful, false otherwise
        """
        pass

    def set_up_drc_tool(self, drc_tool: HammerDRCTool, name: str, run_dir: str='') -> bool:
        """
        Set up and store the given DRC tool instance for use in this
        driver.
        :param drc_tool: Tool instance.
        :param name: Short name (e.g. "calibre") of the tool instance. Typically
                     obtained from the database.
        :param run_dir: Directory to use for the tool run_dir. Defaults to the
                        run_dir passed in the HammerDriver constructor.
        :return: True if setup was successful.
        """
        pass

    def load_drc_tool(self, run_dir: str='') -> bool:
        """
        Loads a DRC tool on a given database

        :param run_dir: Directory to use for the tool run_dir. Defaults to the run_dir passed in the HammerDriver
                        constructor.
        :return: True if DRC tool loading was successful, False otherwise.
        """
        pass

    def set_up_lvs_tool(self, lvs_tool: HammerLVSTool, name: str, run_dir: str='') -> bool:
        """
        Set up and store the given LVS tool instance for use in this
        driver.
        :param lvs_tool: Tool instance.
        :param name: Short name (e.g. "calibre") of the tool instance. Typically
                     obtained from the database.
        :param run_dir: Directory to use for the tool run_dir. Defaults to the
                        run_dir passed in the HammerDriver constructor.
        :return: True if setup was successful.
        """
        pass

    def load_lvs_tool(self, run_dir: str='') -> bool:
        """
        Loads an LVS tool on a given database

        :param run_dir: Directory to use for the tool run_dir. Defaults to the run_dir passed in the HammerDriver
                        constructor.
        :return: True if LVS tool loading was successful, False otherwise.
        """
        pass

    def set_up_sram_generator_tool(self, sram_generator_tool: HammerSRAMGeneratorTool, name: str, run_dir: str='') -> bool:
        """
        Set up and store the given SRAM Generator tool instance for use in this
        driver.
        :param lvs_tool: Tool instance.
        :param name: Short name (e.g. "sram_generator") of the tool instance. Typically
                     obtained from the database.
        :param run_dir: Directory to use for the tool run_dir. Defaults to the
                        run_dir passed in the HammerDriver constructor.
        :return: True if setup was successful.
        """
        pass

    def load_sram_generator_tool(self, run_dir: str='') -> bool:
        """
        Loads an SRAM Generator tool on a given database

        :param run_dir: Directory to use for the tool run_dir. Defaults to the run_dir passed in the HammerDriver
                        constructor.
        :return: True if SRAM Generator tool loading was successful, False otherwise.
        """
        pass

    def set_up_sim_tool(self, sim_tool: HammerSimTool, name: str, run_dir: str='') -> bool:
        """
        Set up and store the given simulation tool instance for use in this
        driver.
        :param sim_tool: Tool instance.
        :param name: Short name (e.g. "vcs") of the tool instance. Typically
                     obtained from the database.
        :param run_dir: Directory to use for the tool run_dir. Defaults to the
                        run_dir passed in the HammerDriver constructor.
        :return: True if setup was successful.
        """
        pass

    def load_sim_tool(self, run_dir: str='') -> bool:
        """
        Load the simulation tool based on the given database.

        :param run_dir: Directory to use for the tool run_dir. Defaults to the run_dir passed in the HammerDriver
                        constructor.
        :return: True if simulation tool loading was successful, False otherwise.
        """
        pass

    def set_up_power_tool(self, power_tool: HammerPowerTool, name: str, run_dir: str='') -> bool:
        """
        Set up and store the given power tool instance for use in this
        driver.
        :param power_tool: Tool instance.
        :param name: Short name (e.g. "vcs") of the tool instance. Typically
                     obtained from the database.
        :param run_dir: Directory to use for the tool run_dir. Defaults to the
                        run_dir passed in the HammerDriver constructor.
        :return: True if setup was successful.
        """
        pass

    def load_power_tool(self, run_dir: str='') -> bool:
        """
        Loads a power tool on a given database

        :param run_dir: Directory to use for the tool run_dir. Defaults to the run_dir passed in the HammerDriver
                        constructor.
        :return: True if power tool loading was successful, False otherwise.
        """
        pass

    def set_up_formal_tool(self, formal_tool: HammerFormalTool, name: str, run_dir: str='') -> bool:
        """
        Set up and store the given formal tool instance for use in this
        driver.
        :param formal_tool: Tool instance.
        :param name: Short name (e.g. "conformal") of the tool instance. Typically
                     obtained from the database.
        :param run_dir: Directory to use for the tool run_dir. Defaults to the
                        run_dir passed in the HammerDriver constructor.
        :return: True if setup was successful.
        """
        pass

    def load_formal_tool(self, run_dir: str='') -> bool:
        """
        Loads a formal tool on a given database

        :param run_dir: Directory to use for the tool run_dir. Defaults to the run_dir passed in the HammerDriver
                        constructor.
        :return: True if formal tool loading was successful, False otherwise.
        """
        pass

    def set_up_timing_tool(self, timing_tool: HammerTimingTool, name: str, run_dir: str='') -> bool:
        """
        Set up and store the given timing tool instance for use in this
        driver.
        :param timing_tool: Tool instance.
        :param name: Short name (e.g. "tempus") of the tool instance. Typically
                     obtained from the database.
        :param run_dir: Directory to use for the tool run_dir. Defaults to the
                        run_dir passed in the HammerDriver constructor.
        :return: True if setup was successful.
        """
        pass

    def load_timing_tool(self, run_dir: str='') -> bool:
        """
        Loads a timing tool on a given database

        :param run_dir: Directory to use for the tool run_dir. Defaults to the run_dir passed in the HammerDriver
                        constructor.
        :return: True if timing tool loading was successful, False otherwise.
        """
        pass

    def set_up_pcb_tool(self, pcb_tool: HammerPCBDeliverableTool, name: str, run_dir: str='') -> bool:
        """
        Set up and store the given PCB deliverable tool instance for use in this
        driver.
        :param pcb_tool: Tool instance.
        :param name: Short name (e.g. "pcb") of the tool instance. Typically
                     obtained from the database.
        :param run_dir: Directory to use for the tool run_dir. Defaults to the
                        run_dir passed in the HammerDriver constructor.
        :return: True if setup was successful.
        """
        pass

    def load_pcb_tool(self, run_dir: str='') -> bool:
        """
        Load the PCB deliverable tool based on the given database.

        :param run_dir: Directory to use for the tool run_dir. Defaults to the run_dir passed in the HammerDriver
                        constructor.
        :return: True if successful, false otherwise
        """
        pass

    def set_post_custom_syn_tool_hooks(self, hooks: List[HammerToolHookAction]) -> None:
        """
        Set the extra list of hooks used for control flow (resume/pause) in run_synthesis.
        They will run after main/hook_actions.

        :param hooks: Hooks to run
        """
        pass

    def set_post_custom_par_tool_hooks(self, hooks: List[HammerToolHookAction]) -> None:
        """
        Set the extra list of hooks used for control flow (resume/pause) in run_par.
        They will run after main/hook_actions.

        :param hooks: Hooks to run
        """
        pass

    def set_post_custom_drc_tool_hooks(self, hooks: List[HammerToolHookAction]) -> None:
        """
        Set the extra list of hooks used for control flow (resume/pause) in run_drc.
        They will run after main/hook_actions.

        :param hooks: Hooks to run
        """
        pass

    def set_post_custom_lvs_tool_hooks(self, hooks: List[HammerToolHookAction]) -> None:
        """
        Set the extra list of hooks used for control flow (resume/pause) in run_lvs.
        They will run after main/hook_actions.

        :param hooks: Hooks to run
        """
        pass

    def set_post_custom_sim_tool_hooks(self, hooks: List[HammerToolHookAction]) -> None:
        """
        Set the extra list of hooks used for control flow (resume/pause) in run_sim.
        They will run after main/hook_actions.

        :param hooks: Hooks to run
        """
        pass

    def set_post_custom_power_tool_hooks(self, hooks: List[HammerToolHookAction]) -> None:
        """
        Set the extra list of hooks used for control flow (resume/pause) in run_power.
        They will run after main/hook_actions.

        :param hooks: Hooks to run
        """
        pass

    def set_post_custom_formal_tool_hooks(self, hooks: List[HammerToolHookAction]) -> None:
        """
        Set the extra list of hooks used for control flow (resume/pause) in run_formal.
        They will run after main/hook_actions.

        :param hooks: Hooks to run
        """
        pass

    def set_post_custom_timing_tool_hooks(self, hooks: List[HammerToolHookAction]) -> None:
        """
        Set the extra list of hooks used for control flow (resume/pause) in run_timing.
        They will run after main/hook_actions.

        :param hooks: Hooks to run
        """
        pass

    def run_synthesis(self, hook_actions: Optional[List[HammerToolHookAction]]=None, force_override: bool=False) -> Tuple[bool, dict]:
        """
        Run synthesis based on the given database.
        The output config dict returned does NOT have a copy of the input config settings.

        :param hook_actions: List of hook actions, or leave as None to use the hooks sets in set_synthesis_hooks.
                             Hooks from set_synthesis_hooks, if present, will be appended afterwards.
        :param force_override: Set to true to overwrite instead of append.
        :return: Tuple of (success, output config dict)
        """
        pass

    @staticmethod
    def synthesis_output_to_par_input(output_dict: dict) -> Optional[dict]:
        """
        Generate the appropriate inputs for running place-and-route from the
        outputs of synthesis run.
        Does not merge the results with any project dictionaries.
        :param output_dict: Dict containing synthesis.outputs.*
        :return: par.inputs.* settings generated from output_dict,
                 or None if output_dict was invalid
        """
        pass

    @staticmethod
    def synthesis_output_to_sim_input(output_dict: dict) -> Optional[dict]:
        """
        Generate the appropriate inputs for running gate level simulations from the
        outputs of synthesis run.
        Does not merge the results with any project dictionaries.
        :param output_dict: Dict containing synthesis.outputs.*
        :return: sim.inputs.* settings generated from output_dict,
                 or None if output_dict was invalid
        """
        pass

    @staticmethod
    def synthesis_output_to_power_input(output_dict: dict) -> Optional[dict]:
        """
        Generate the appropriate inputs for running post-synthesis power analysis from the
        outputs of synthesis run.
        Does not merge the results with any project dictionaries.
        :param output_dict: Dict containing synthesis.outputs.*
        :return: power.inputs.* settings generated from output_dict,
                 or None if output_dict was invalid
        """
        pass

    @staticmethod
    def synthesis_output_to_formal_input(output_dict: dict) -> Optional[dict]:
        """
        Generate the appropriate inputs for running formal tools from the
        outputs of synthesis run.
        Does not merge the results with any project dictionaries.
        :param output_dict: Dict containing synthesis.outputs.*
        :return: formal.inputs.* settings generated from output_dict,
                 or None if output_dict was invalid
        """
        pass

    @staticmethod
    def synthesis_output_to_timing_input(output_dict: dict) -> Optional[dict]:
        """
        Generate the appropriate inputs for running timing tools from the
        outputs of synthesis run.
        Does not merge the results with any project dictionaries.
        :param output_dict: Dict containing synthesis.outputs.*
        :return: timing.inputs.* settings generated from output_dict,
                 or None if output_dict was invalid
        """
        pass

    @staticmethod
    def par_output_to_sim_input(output_dict: dict) -> Optional[dict]:
        """
        Generate the appropriate inputs for running gate level simulations from the
        outputs of par run.
        Does not merge the results with any project dictionaries.
        :param output_dict: Dict containing par.outputs.*
        :return: sim.inputs.* settings generated from output_dict,
                 or None if output_dict was invalid
        """
        pass

    @staticmethod
    def par_output_to_power_input(output_dict: dict) -> Optional[dict]:
        """
        Generate the appropriate inputs for running power analysis from the
        outputs of par run.
        Does not merge the results with any project dictionaries.
        :param output_dict: Dict containing par.outputs.*
        :return: power.inputs.* settings generated from output_dict,
                 or None if output_dict was invalid
        """
        pass

    @staticmethod
    def par_output_to_formal_input(output_dict: dict) -> Optional[dict]:
        """
        Generate the appropriate inputs for running formal tools from the
        outputs of par run.
        Does not merge the results with any project dictionaries.
        :param output_dict: Dict containing par.outputs.*
        :return: formal.inputs.* settings generated from output_dict,
                 or None if output_dict was invalid
        """
        pass

    @staticmethod
    def par_output_to_timing_input(output_dict: dict) -> Optional[dict]:
        """
        Generate the appropriate inputs for running timing tools from the
        outputs of par run.
        Does not merge the results with any project dictionaries.
        :param output_dict: Dict containing par.outputs.*
        :return: timing.inputs.* settings generated from output_dict,
                 or None if output_dict was invalid
        """
        pass

    def run_par(self, hook_actions: Optional[List[HammerToolHookAction]]=None, force_override: bool=False) -> Tuple[bool, dict]:
        """
        Run place and route based on the given database.
        The output config dict returned does NOT have a copy of the input config settings.
        """
        pass

    @staticmethod
    def par_output_to_syn_input(output_dict: dict) -> Optional[dict]:
        """
        Generate the appropriate inputs for running the next level of synthesis from the
        outputs of par run in a hierarchical flow.
        Does not merge the results with any project dictionaries.
        :param output_dict: Dict containing par.outputs.*
        :return: vlsi.inputs.* settings generated from output_dict,
                 or None if output_dict was invalid
        """
        pass

    @staticmethod
    def par_output_to_drc_input(output_dict: dict) -> Optional[dict]:
        """
        Generate the appropriate inputs for running DRC from the
        outputs of par run.
        Does not merge the results with any project dictionaries.
        :param output_dict: Dict containing par.outputs.*
        :return: drc.inputs.* settings generated from output_dict,
                 or None if output_dict was invalid
        """
        pass

    @staticmethod
    def par_output_to_lvs_input(output_dict: dict) -> Optional[dict]:
        """
        Generate the appropriate inputs for running LVS from the
        outputs of par run.
        Does not merge the results with any project dictionaries.
        :param output_dict: Dict containing par.outputs.*
        :return: lvs.inputs.* settings generated from output_dict,
                 or None if output_dict was invalid
        """
        pass

    def run_drc(self, hook_actions: Optional[List[HammerToolHookAction]]=None, force_override: bool=False) -> Tuple[bool, dict]:
        """
        Run DRC on a given database.

        :param hook_actions: List of hook actions, or leave as None to use the hooks sets in set_drc_hooks.
                             Hooks from set_drc_hooks, if present, will be appended afterwards.
        :param force_override: Set to true to overwrite instead of append.
        :return: Tuple of (success, output config dict)
        """
        pass

    def run_lvs(self, hook_actions: Optional[List[HammerToolHookAction]]=None, force_override: bool=False) -> Tuple[bool, dict]:
        """
        Run LVS on a given database.

        :param hook_actions: List of hook actions, or leave as None to use the hooks sets in set_lvs_hooks.
                             Hooks from set_lvs_hooks, if present, will be appended afterwards.
        :param force_override: Set to true to overwrite instead of append.
        :return: Tuple of (success, output config dict)
        """
        pass

    def run_sram_generator(self, hook_actions: Optional[List[HammerToolHookAction]]=None, force_override: bool=False) -> Tuple[bool, dict]:
        """
        Run SRAM Generator on a given database.

        :param hook_actions: List of hook actions, or leave as None to use the hooks sets in set_sram_generator_hooks.
                             Hooks from set_sram_generator_hooks, if present, will be appended afterwards.
        :param force_override: Set to true to overwrite instead of append.
        :return: Tuple of (success, output config dict)
        """
        pass

    @staticmethod
    def sim_output_to_power_input(output_dict: dict) -> Optional[dict]:
        """
        Generate the inputs for dynamic power analysis from the
        outputs of simulations.
        Does not merge the results with any project dictionaries.
        :param output_dict: Dict containing sim.outputs.*
        :return: sim.inputs.* settings generated from output_dict,
                 or None if output_dict was invalid
        """
        pass

    def run_sim(self, hook_actions: Optional[List[HammerToolHookAction]]=None, force_override: bool=False) -> Tuple[bool, dict]:
        """
        Run simulation based on the given database.
        The output config dict returned does NOT have a copy of the input config settings.

        :param hook_actions: List of hook actions, or leave as None to use the hooks sets in set_simulation_hooks.
                             Hooks from set_simulation_hooks, if present, will be appended afterwards.
        :param force_override: Set to true to overwrite instead of append.
        :return: Tuple of (success, output config dict)
        """
        pass

    def run_power(self, hook_actions: Optional[List[HammerToolHookAction]]=None, force_override: bool=False) -> Tuple[bool, dict]:
        """
        Run power analysis based on the given database.
        The output config dict returned does NOT have a copy of the input config settings.

        :param hook_actions: List of hook actions, or leave as None to use the hooks sets in set_power_hooks.
                             Hooks from set_power_hooks, if present, will be appended afterwards.
        :param force_override: Set to true to overwrite instead of append.
        :return: Tuple of (success, output config dict)
        """
        pass

    def run_formal(self, hook_actions: Optional[List[HammerToolHookAction]]=None, force_override: bool=False) -> Tuple[bool, dict]:
        """
        Run formal verification based on the given database.
        The output config dict returned does NOT have a copy of the input config settings.

        :param hook_actions: List of hook actions, or leave as None to use the hooks sets in set_formal_hooks.
                             Hooks from set_formal_hooks, if present, will be appended afterwards.
        :param force_override: Set to true to overwrite instead of append.
        :return: Tuple of (success, output config dict)
        """
        pass

    def run_timing(self, hook_actions: Optional[List[HammerToolHookAction]]=None, force_override: bool=False) -> Tuple[bool, dict]:
        """
        Run timing analysis based on the given database.
        The output config dict returned does NOT have a copy of the input config settings.

        :param hook_actions: List of hook actions, or leave as None to use the hooks sets in set_timing_hooks.
                             Hooks from set_timing_hooks, if present, will be appended afterwards.
        :param force_override: Set to true to overwrite instead of append.
        :return: Tuple of (success, output config dict)
        """
        pass

    def run_pcb(self, hook_actions: Optional[List[HammerToolHookAction]]=None, force_override: bool=False) -> Tuple[bool, dict]:
        """
        Run the PCB deliverable generation tool

        :param hook_actions: List of hook actions, or leave as None to use the hooks sets in set_pcb_hooks.
                             Hooks from set_pcb_hooks, if present, will be appended afterwards.
        :param force_override: Set to true to overwrite instead of append.
        :return: Tuple of (success, output config dict)
        """
        pass

    def get_hierarchical_dependency_graph(self) -> Dict[str, Tuple[List[str], List[str]]]:
        """
        Return the dependency graph for this flow if it is hierarchical, or an empty dict if it is flat.
        The flow is the set of setps configured by the current input Hammer IR.

        :return: The dependency graph.
        """
        pass

    def get_hierarchical_settings(self) -> List[Tuple[str, dict]]:
        """
        Read settings from the database, determine leaf/hierarchical modules, an order of execution, and return an
        ordered list (from leaf to top) of modules and associated config snippets needed to run syn+par for that module
        hierarchically.

        :return: List of tuples of (module name, config snippet)
        """
        pass

    def _hierarchical_helper(self) -> Tuple[List[Tuple[str, dict]], Dict[str, Tuple[List[str], List[str]]]]:
        """
        Read settings from the database, determine leaf/hierarchical modules, an order of execution, and return an
        ordered list (from leaf to top) of modules and associated config snippets needed to run syn+par for that module
        hierarchically and the dependency graph. Do not call this method directly- use get_hierarchical_settings or
        get_hierarchial_dependency_graph instead.

        :return: Tuple of (List of tuples of (module name, config snippet), the dependency graph)
        """
        pass

    @property
    def dump_history(self) -> bool:
        pass

    @dump_history.setter
    def dump_history(self, new_dump_history: bool) -> None:
        pass
