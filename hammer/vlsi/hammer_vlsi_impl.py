from abc import abstractmethod
import importlib
import importlib.resources as resources
import json
from typing import Iterable, Dict, Any
import inspect
import datetime
from statistics import mode
import os
import hammer.config as hammer_config
from hammer.utils import deepdict, coerce_to_grid, get_or_else
from hammer.tech import ExtraLibrary, RoutingDirection
from .constraints import *
from .units import VoltageValue, TimeValue

class HierarchicalMode(Enum):
    Flat = 1
    Leaf = 2
    Hierarchical = 3
    Top = 4

    @classmethod
    def __mapping(cls) -> Dict[str, 'HierarchicalMode']:
        pass

    @staticmethod
    def from_str(x: str) -> 'HierarchicalMode':
        pass

    def __str__(self) -> str:
        return reverse_dict(HierarchicalMode.__mapping())[self]

    def is_nonleaf_hierarchical(self) -> bool:
        """
        Helper function that returns True if this mode is a non-leaf hierarchical mode (i.e. any block with
        hierarchical sub-blocks).
        """
        pass

class FlowLevel(Enum):
    RTL = 1
    SYN = 2
    PAR = 3

    @classmethod
    def __mapping(cls) -> Dict[str, 'FlowLevel']:
        pass

    @staticmethod
    def from_str(x: str) -> 'FlowLevel':
        pass

    def __str__(self) -> str:
        return reverse_dict(FlowLevel.__mapping())[self]

    def is_gatelevel(self) -> bool:
        pass
PowerReport = NamedTuple('PowerReport', [('waveform_path', str), ('report_stem', Optional[str]), ('inst', Optional[str]), ('module', Optional[str]), ('levels', Optional[int]), ('start_time', Optional[TimeValue]), ('end_time', Optional[TimeValue]), ('interval_size', Optional[TimeValue]), ('interval_list', Optional[TimeValue]), ('toggle_signal', Optional[str]), ('num_toggles', Optional[int]), ('frame_count', Optional[int]), ('power_type', Optional[int]), ('output_formats', Optional[List[str]])])
import hammer.tech as hammer_tech

class HammerVLSISettings:
    """
    Static class which holds global hammer-vlsi settings.
    """

    @staticmethod
    def get_config() -> dict:
        """Export settings as a config dictionary."""
        pass

    @classmethod
    def load_builtins_and_core(cls, database: hammer_config.HammerDatabase) -> None:
        """
        Helper function that loads builtins and core into a HammerDatabase.
        """
        pass
from .hammer_tool import HammerTool, HammerToolStep

class DummyHammerTool(HammerTool):
    """
    This is a dummy implementation of HammerTool that does nothing.
    It has no config, and no particular sense of versioning.
    It is present for nop tools and as a testing aid.
    """

    def tool_config_prefix(self) -> str:
        pass

    def version_number(self, version: str) -> int:
        pass

    @property
    def steps(self) -> List[HammerToolStep]:
        pass

class HammerSRAMGeneratorTool(HammerTool):

    @property
    def input_parameters(self) -> List[SRAMParameters]:
        """
        Get the input sram parameters to be generated.

        :return: The input sram parameters to be generated.
        """
        pass

    @input_parameters.setter
    def input_parameters(self, value: List[SRAMParameters]) -> None:
        """Set the input sram parameters to be generated."""
        pass

    @property
    def output_libraries(self) -> List[ExtraLibrary]:
        """
        Get the list of the hammer tech libraries corresponding to generated srams.

        :return: The list of the hammer tech libraries corresponding to generated srams.
        """
        pass

    @output_libraries.setter
    def output_libraries(self, value: List[ExtraLibrary]) -> None:
        """Set the list of the hammer tech libraries corresponding to generated srams."""
        pass

    @property
    def steps(self) -> List[HammerToolStep]:
        pass

    def fill_outputs(self) -> bool:
        pass

    def export_config_outputs(self) -> Dict[str, Any]:
        pass

    def generate_all_srams_and_corners(self) -> bool:
        pass

    def generate_all_srams(self, corner: MMMCCorner) -> List[ExtraLibrary]:
        pass

    @abstractmethod
    def generate_sram(self, params: SRAMParameters, corner: MMMCCorner) -> ExtraLibrary:
        pass

class HammerSynthesisTool(HammerTool):

    @abstractmethod
    def fill_outputs(self) -> bool:
        pass

    def export_config_outputs(self) -> Dict[str, Any]:
        pass

    @property
    def input_files(self) -> List[str]:
        """
        Get the input collection of source RTL files (e.g. *.v).

        :return: The input collection of source RTL files (e.g. *.v).
        """
        pass

    @input_files.setter
    def input_files(self, value: List[str]) -> None:
        """Set the input collection of source RTL files (e.g. *.v)."""
        pass

    @property
    def output_files(self) -> List[str]:
        """
        Get the output collection of mapped (post-synthesis) RTL files.

        :return: The output collection of mapped (post-synthesis) RTL files.
        """
        pass

    @output_files.setter
    def output_files(self, value: List[str]) -> None:
        """Set the output collection of mapped (post-synthesis) RTL files."""
        pass

    @property
    def output_sdc(self) -> str:
        """
        Get the (optional) output post-synthesis SDC constraints file.

        :return: The (optional) output post-synthesis SDC constraints file.
        """
        pass

    @output_sdc.setter
    def output_sdc(self, value: str) -> None:
        """Set the (optional) output post-synthesis SDC constraints file."""
        pass

    @property
    def output_all_regs(self) -> str:
        """
        Get the path to output list of all registers in the design with output pin for gate level simulation.

        :return: The path to output list of all registers in the design with output pin for gate level simulation.
        """
        pass

    @output_all_regs.setter
    def output_all_regs(self, value: str) -> None:
        """Set the path to output list of all registers in the design with output pin for gate level simulation."""
        pass

    @property
    def output_seq_cells(self) -> str:
        """
        Get the path to output collection of all sequential standard cells in design.

        :return: The path to output collection of all sequential standard cells in design.
        """
        pass

    @output_seq_cells.setter
    def output_seq_cells(self, value: str) -> None:
        """Set the path to output collection of all sequential standard cells in design."""
        pass

    @property
    def sdf_file(self) -> str:
        """
        Get the output SDF file to be read for timing annotated gate level sims.

        :return: The output SDF file to be read for timing annotated gate level sims.
        """
        pass

    @sdf_file.setter
    def sdf_file(self, value: str) -> None:
        """Set the output SDF file to be read for timing annotated gate level sims."""
        pass

class HammerPlaceAndRouteTool(HammerTool):

    @abstractmethod
    def fill_outputs(self) -> bool:
        pass

    def export_config_outputs(self) -> Dict[str, Any]:
        pass

    @property
    def input_files(self) -> List[str]:
        """
        Get the input post-synthesis netlist files.

        :return: The input post-synthesis netlist files.
        """
        pass

    @input_files.setter
    def input_files(self, value: List[str]) -> None:
        """Set the input post-synthesis netlist files."""
        pass

    @property
    def post_synth_sdc(self) -> Optional[str]:
        """
        Get the (optional) input post-synthesis SDC constraint file.

        :return: The (optional) input post-synthesis SDC constraint file.
        """
        pass

    @post_synth_sdc.setter
    def post_synth_sdc(self, value: Optional[str]) -> None:
        """Set the (optional) input post-synthesis SDC constraint file."""
        pass

    @property
    def output_ilms(self) -> List[ILMStruct]:
        """
        Get the (optional) output ILM information for hierarchical mode.

        :return: The (optional) output ILM information for hierarchical mode.
        """
        pass

    @output_ilms.setter
    def output_ilms(self, value: List[ILMStruct]) -> None:
        """Set the (optional) output ILM information for hierarchical mode."""
        pass

    @property
    def output_gds(self) -> str:
        """
        Get the path to the output GDS file.

        :return: The path to the output GDS file.
        """
        pass

    @output_gds.setter
    def output_gds(self, value: str) -> None:
        """Set the path to the output GDS file."""
        pass

    @property
    def output_netlist(self) -> str:
        """
        Get the path to the output netlist file.

        :return: The path to the output netlist file.
        """
        pass

    @output_netlist.setter
    def output_netlist(self, value: str) -> None:
        """Set the path to the output netlist file."""
        pass

    @property
    def output_physical_netlist(self) -> Optional[str]:
        """
        Get the (optional) path to the output physical netlist file.

        :return: The (optional) path to the output physical netlist file.
        """
        pass

    @output_physical_netlist.setter
    def output_physical_netlist(self, value: Optional[str]) -> None:
        """Set the (optional) path to the output physical netlist file."""
        pass

    @property
    def output_sim_netlist(self) -> str:
        """
        Get the path to the output simulation netlist file.

        :return: The path to the output simulation netlist file.
        """
        pass

    @output_sim_netlist.setter
    def output_sim_netlist(self, value: str) -> None:
        """Set the path to the output simulation netlist file."""
        pass

    @property
    def hcells_list(self) -> List[str]:
        """
        Get the list of cells to explicitly map hierarchically in LVS.

        :return: The list of cells to explicitly map hierarchically in LVS.
        """
        pass

    @hcells_list.setter
    def hcells_list(self, value: List[str]) -> None:
        """Set the list of cells to explicitly map hierarchically in LVS."""
        pass

    @property
    def output_all_regs(self) -> str:
        """
        Get the path to output list of all registers in the design with output pin for gate level simulation.

        :return: The path to output list of all registers in the design with output pin for gate level simulation.
        """
        pass

    @output_all_regs.setter
    def output_all_regs(self, value: str) -> None:
        """Set the path to output list of all registers in the design with output pin for gate level simulation."""
        pass

    @property
    def output_seq_cells(self) -> str:
        """
        Get the path to output collection of all sequential standard cells in design.

        :return: The path to output collection of all sequential standard cells in design.
        """
        pass

    @output_seq_cells.setter
    def output_seq_cells(self, value: str) -> None:
        """Set the path to output collection of all sequential standard cells in design."""
        pass

    @property
    def sdf_file(self) -> str:
        """
        Get the output SDF file to be read for timing annotated gate level sims.

        :return: The output SDF file to be read for timing annotated gate level sims.
        """
        pass

    @sdf_file.setter
    def sdf_file(self, value: str) -> None:
        """Set the output SDF file to be read for timing annotated gate level sims."""
        pass

    def create_power_straps_tcl(self) -> List[str]:
        """
        Create power straps TCL commands depending on the mode.
        """
        pass

    def generate_power_straps_tcl(self) -> List[str]:
        """
        Generate a TCL script to create power straps from the config/IR.
        :return: Power straps TCL script.
        """
        pass

    def specify_power_straps_by_tracks(self, layer_name: str, bottom_via_layer: str, blockage_spacing: Decimal, track_pitch: int, track_width: int, track_spacing: int, track_start: int, track_offset: Decimal, bbox: Optional[List[Decimal]], nets: List[str], add_pins: bool, layer_is_all_power: bool, antenna_trim_shape: str, pattern: str) -> List[str]:
        """
        Generate a list of TCL commands that will create power straps on a given layer by specifying the desired track consumption.
        This method assumes that power straps are built bottom-up, starting with standard cell rails.

        :param layer_name: The layer name of the metal on which to create straps.
        :param bottom_via_layer_name: The layer name of the lowest metal layer down to which to drop vias.
        :param blockage_spacing: The minimum spacing between the end of a strap and the beginning of a macro or blockage.
        :param track_pitch: The integer pitch between groups of power straps (i.e. from left edge of strap A to the next left edge of strap A) in units of the routing pitch.
        :param track_width: The desired number of routing tracks to consume by a single power strap.
        :param track_spacing: The desired number of USABLE routing tracks between power straps (e.g. between VDD and VSS). It is recommended to leave this at 0 except to fix DRC issues.
        :param track_start: The index of the first track to start using for power straps relative to the bounding box.
        :param bbox: The optional (2N)-point bounding box of the area to generate straps. By default the entire core area is used.
        :param nets: A list of power nets to create (e.g. ["VDD", "VSS"], ["VDDA", "VSS", "VDDB"], ... etc.).
        :param add_pins: True if pins are desired on this layer; False otherwise.
        :param layer_is_all_power: True if there will be no signal wires on this layer.
        :param antenna_trim_shape: Strategy for trimming strap antennae. {none/stripe}
        :return: A list of TCL commands that will generate power straps.
        """
        pass

    def specify_all_power_straps_by_tracks(self, layer_names: List[str], bottom_via_layer: str, ground_net: str, power_nets: List[str], power_weights: List[int], bbox: Optional[List[Decimal]], pin_layers: List[str], generate_rail_layer: bool) -> List[str]:
        """
        Generate a list of TCL commands that will create power straps on a given set of layers by specifying the desired per-track track consumption and utilization.
        This will build standard cell power strap rails first. Layer-specific parameters are read from the hammer config:
            - par.generate_power_straps_options.by_tracks.blockage_spacing
            - par.generate_power_straps_options.by_tracks.track_width
            - par.generate_power_straps_options.by_tracks.track_spacing
            - par.generate_power_straps_options.by_tracks.power_utilization
        These settings are all overridable by appending an underscore followed by the metal name (e.g. power_utilization_M3).

        :param layer_names: The list of metal layer names on which to create straps.
        :param bottom_via_layer: The layer the lowest-strap layer will via down to. Usually the stdcell rail layer
        :param ground_net: The name of the ground net in this design. Only 1 ground net is supported.
        :param power_nets: A list of power nets to create (not ground).
        :param power_weights: Specifies the power strap placement pattern for multiple-domain designs (e.g. ["VDDA", "VDDB"] with [2, 1] will produce 2 VDDA straps for ever 1 VDDB strap).
        :param bbox: The optional (2N)-point bounding box of the area to generate straps. By default the entire core area is used.
        :param pin_layers: A list of layers on which to place pins
        :return: A list of TCL commands that will generate power straps.
        """
        pass
    _hardmacro_power_straps = []

    def _get_power_straps_for_hardmacros(self, layer_name: str, pitch: Decimal, width: Decimal, spacing: Decimal, offset: Decimal, bbox: Optional[List[Decimal]], nets: List[str]) -> None:
        """
        Generates power strap information for hardmacros in the design.
        Also applies a set of checks per instance:
        - That master is specified and is in the list of power_straps_abutment_macros (if provided)
        - It is not a physical only cell
        - It does not fall outside the power strap bbox
        - No power obstructions on the relevant layer overlap it
        - All straps within a group can fully abut/overlap it

        :param layer_name: The layer name of the metal on which to create straps.
        :param pitch: The pitch between groups of power straps (i.e. from left edge of strap A to the next left edge of strap A).
        :param width: The width of each strap in a group.
        :param spacing: The spacing between straps in a group.
        :param offset: The offset to start the first group.
        :param bbox: The optional (2N)-point bounding box of the area to generate straps. By default the entire core area is used.
        :params nets: A list of power nets to create (e.g. ["VDD", "VSS"], ["VDDA", "VSS", "VDDB"], ... etc.).
        """
        pass

    def _dump_power_straps_for_hardmacros(self) -> None:
        """
        Postprocess the list of hardmacro power straps and dump it to a JSON file.
        All hardmacro instances conforming to the following will be checked and have power strap info dumped:
        - "master" is specified
        - "physical_only" is False
        - "top_layer" is specified
        For a given master, the following checks are made:
        - If power strap abutment checks are turned on, the offset of a majority of instances with
          conforming orientation is considered the desired one. Non-conforming instances are marked
          with a modified master name and the user is warned that abutment may fail.
        - If power strap abutment checks are turned off, the availability of top_layer + 1 is checked.
          If it is not available, the user is warned that the instance may not be connected to supplies.
        """
        pass
    _power_straps_last_index = -1

    def _power_straps_check_index(self, layer_name: str) -> None:
        pass

    def _get_by_tracks_metal_setting(self, key: str, layer_name: str) -> Any:
        """
        Return the metal setting used by the by_tracks power strap generation method.
        This will return the value from the provided key in the par.generate_power_straps.by_tracks namespace,
        which can be overridden for a specific metal layer by appending _<layer name>.

        :param key: The base key name (e.g. track_spacing). Do not include the namespace or metal override.
        :return: The value associated with the key, after applying any metal overrides
        """
        pass

    def _get_by_tracks_track_pitch(self, layer_name: str) -> int:
        """
        Returns the track pitch used by the by_tracks power rail generation method

        :param layer_name: The string name of the metal layer
        :return: The power strap group pitch in tracks
        """
        pass

    @abstractmethod
    def specify_power_straps(self, layer_name: str, bottom_via_layer_name: str, blockage_spacing: Decimal, pitch: Decimal, width: Decimal, spacing: Decimal, offset: Decimal, bbox: Optional[List[Decimal]], nets: List[str], add_pins: bool, antenna_trim_shape: str) -> List[str]:
        """
        Generate a list of TCL commands that will create power straps on a given layer.
        This is a low-level, cad-tool-specific API. It is designed to be called by higher-level methods, so calling this directly is not recommended.
        This method assumes that power straps are built bottom-up, starting with standard cell rails.

        :param layer_name: The layer name of the metal on which to create straps.
        :param bottom_via_layer_name: The layer name of the lowest metal layer down to which to drop vias.
        :param blockage_spacing: The minimum spacing between the end of a strap and the beginning of a macro or blockage.
        :param pitch: The pitch between groups of power straps (i.e. from left edge of strap A to the next left edge of strap A).
        :param width: The width of each strap in a group.
        :param spacing: The spacing between straps in a group.
        :param offset: The offset to start the first group.
        :param bbox: The optional (2N)-point bounding box of the area to generate straps. By default the entire core area is used.
        :param nets: A list of power nets to create (e.g. ["VDD", "VSS"], ["VDDA", "VSS", "VDDB"],  ... etc.).
        :param add_pins: True if pins are desired on this layer; False otherwise.
        :param antenna_trim_shape: Strategy for trimming strap antennae. {none/stripe}
        :return: A list of TCL commands that will generate power straps.
        """
        self._power_straps_check_index(layer_name)
        return []

    @abstractmethod
    def specify_std_cell_power_straps(self, blockage_spacing: Decimal, bbox: Optional[List[Decimal]], nets: List[str]) -> List[str]:
        """
        Generate a list of TCL commands that build the low-level standard cell power strap rails.
        This is a low-level, cad-tool-specific API. It is designed to be called by higher-level methods, so calling this directly is not recommended.
        This will create power straps based on the tapcells in the special cells list.
        The layer is set by technology.core.std_cell_rail_layer, which should be the highest metal layer in the std cell rails.
        This method should be called before any calls to specify_power_straps.

        :param blockage_spacing: The spacing to leave between the end of a stripe and a macro or routing blockage.
        :param bbox: The optional (2N)-point bounding box of the area to generate straps. By default the entire core area is used.
        :param nets: A list of power net names (e.g. ["VDD", "VSS"]).
        :return: A list of TCL commands that will generate power straps on rails.
        """
        layer_name = self.get_setting('technology.core.std_cell_rail_layer')
        self._power_straps_check_index(layer_name)
        return []

class HammerSignoffTool(HammerTool):

    @abstractmethod
    def fill_outputs(self) -> bool:
        pass

    @abstractmethod
    def signoff_results(self) -> int:
        """
        Return the number of issues raised by the signoff tool (0 = all checks pass).
        Individual tools extending HammerSignoffTool should implement their own *_results methods that provide tool-specific information,
        and then pass a meaningful count of issues to their implementation of this method.

        :return: The number of signoff issues raised by the tool
        """
        pass

class HammerDRCTool(HammerSignoffTool):

    def export_config_outputs(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def fill_outputs(self) -> bool:
        pass

    @abstractmethod
    def globally_waived_drc_rules(self) -> List[str]:
        """
        Get the list of waived DRC rule names.

        :return: The list of waived DRC rule names.
        """
        pass

    def drc_rules_to_run(self) -> List[str]:
        """
        Return a list of the specific DRC rules to run. If empty, run all rules (the default).

        :return: A list of DRC rules to run or an empty list if running all rules
        """
        pass

    def get_drc_decks(self) -> List[hammer_tech.DRCDeck]:
        """ Get all DRC decks for this tool. """
        pass

    def get_additional_drc_text(self) -> str:
        """ Get the additional custom DRC command text to add after the boilerplate commands at the top of the DRC run file. """
        pass

    @abstractmethod
    def drc_results_pre_waived(self) -> Dict[str, int]:
        """ Return a Dict mapping the DRC check name to an error count (pre-waivers). """
        pass

    def signoff_results(self) -> int:
        """ Return the count of unwaived DRC errors. """
        pass

    def drc_results(self) -> Dict[str, int]:
        """ Return a Dict mapping the DRC check name to an error count (with waivers). """
        pass

    @property
    def layout_file(self) -> str:
        """
        Get the path to the input layout file (e.g. a *.gds).

        :return: The path to the input layout file (e.g. a *.gds).
        """
        pass

    @layout_file.setter
    def layout_file(self, value: str) -> None:
        """Set the path to the input layout file (e.g. a *.gds)."""
        pass

class HammerLVSTool(HammerSignoffTool):

    def export_config_outputs(self) -> Dict[str, Any]:
        pass

    def get_input_ilms(self, full_tree=True) -> List[ILMStruct]:
        pass

    @abstractmethod
    def fill_outputs(self) -> bool:
        pass

    @abstractmethod
    def globally_waived_erc_rules(self) -> List[str]:
        """
        Get the list of waived ERC rule names.

        :return: The list of waived ERC rule names.
        """
        pass

    @abstractmethod
    def erc_results_pre_waived(self) -> Dict[str, int]:
        """ Return a Dict mapping the ERC check name to an error count (pre-waivers). """
        pass

    def signoff_results(self) -> int:
        """ Return the count of unwaived ERC errors and LVS errors. """
        pass

    def erc_results(self) -> Dict[str, int]:
        """ Return a Dict mapping the ERC check name to an error count (with waivers). """
        pass

    @abstractmethod
    def lvs_results(self) -> List[str]:
        """ Return the LVS issue descriptions for each issue. An empty list means LVS passes. """
        pass

    def get_lvs_decks(self) -> List[hammer_tech.LVSDeck]:
        """ Get all the LVS decks for this tool. """
        pass

    def get_additional_lvs_text(self) -> str:
        """ Get the additional custom LVS command text to add after the boilerplate commands at the top of the LVS run file. """
        pass

    @property
    def layout_file(self) -> str:
        """
        Get the path to the input layout file (e.g. a *.gds).

        :return: The path to the input layout file (e.g. a *.gds).
        """
        pass

    @layout_file.setter
    def layout_file(self, value: str) -> None:
        """Set the path to the input layout file (e.g. a *.gds)."""
        pass

    @property
    def schematic_files(self) -> List[str]:
        """
        Get the path to the input SPICE or Verilog schematic files (e.g. *.v or *.spi).

        :return: The path to the input SPICE or Verilog schematic files (e.g. *.v or *.spi).
        """
        pass

    @schematic_files.setter
    def schematic_files(self, value: List[str]) -> None:
        """Set the path to the input SPICE or Verilog schematic files (e.g. *.v or *.spi)."""
        pass

    @property
    def hcells_list(self) -> List[str]:
        """
        Get the list of cells to explicitly map hierarchically in LVS.

        :return: The list of cells to explicitly map hierarchically in LVS.
        """
        pass

    @hcells_list.setter
    def hcells_list(self, value: List[str]) -> None:
        """Set the list of cells to explicitly map hierarchically in LVS."""
        pass

class HammerSimTool(HammerTool):

    def export_config_outputs(self) -> Dict[str, Any]:
        pass

    @property
    def level(self) -> FlowLevel:
        """Return the flow level."""
        pass

    @property
    def benchmarks(self) -> List[str]:
        """Return the benchmarks to run."""
        pass

    @property
    def top_module(self) -> str:
        """
        Get the top RTL module.

        :return: The top RTL module.
        """
        pass

    @top_module.setter
    def top_module(self, value: str) -> None:
        """Set the top RTL module."""
        pass

    @property
    def input_files(self) -> List[str]:
        """
        Get the paths to input verilog files.

        :return: The paths to input verilog files.
        """
        pass

    @input_files.setter
    def input_files(self, value: List[str]) -> None:
        """Set the paths to input verilog files."""
        pass

    @property
    def all_regs(self) -> str:
        """
        Get the path to list of all registers in the design with output pin.

        :return: The path to list of all registers in the design with output pin.
        """
        pass

    @all_regs.setter
    def all_regs(self, value: str) -> None:
        """Set the path to list of all registers in the design with output pin."""
        pass

    @property
    def seq_cells(self) -> str:
        """
        Get the path to collection of all sequential standard cells in design.

        :return: The path to collection of all sequential standard cells in design.
        """
        pass

    @seq_cells.setter
    def seq_cells(self, value: str) -> None:
        """Set the path to collection of all sequential standard cells in design."""
        pass

    @property
    def sdf_file(self) -> Optional[str]:
        """
        Get the optional SDF file needed for timing annotated gate level sims.

        :return: The optional SDF file needed for timing annotated gate level sims.
        """
        pass

    @sdf_file.setter
    def sdf_file(self, value: Optional[str]) -> None:
        """Set the optional SDF file needed for timing annotated gate level sims."""
        pass

    @property
    def output_waveforms(self) -> List[str]:
        """
        Get the paths to output waveforms.

        :return: The paths to output waveforms.
        """
        pass

    @output_waveforms.setter
    def output_waveforms(self, value: List[str]) -> None:
        """Set the paths to output waveforms."""
        pass

    @property
    def output_saifs(self) -> List[str]:
        """
        Get the paths to output activity files.

        :return: The paths to output activity files.
        """
        pass

    @output_saifs.setter
    def output_saifs(self, value: List[str]) -> None:
        """Set the paths to output activity files."""
        pass

    @property
    def output_top_module(self) -> str:
        """
        Get the top RTL module.

        :return: The top RTL module.
        """
        pass

    @output_top_module.setter
    def output_top_module(self, value: str) -> None:
        """Set the top RTL module."""
        pass

    @property
    def output_tb_name(self) -> str:
        """
        Get the sim testbench name.

        :return: The sim testbench name.
        """
        pass

    @output_tb_name.setter
    def output_tb_name(self, value: str) -> None:
        """Set the sim testbench name."""
        pass

    @property
    def output_tb_dut(self) -> str:
        """
        Get the sim DUT instance name.

        :return: The sim DUT instance name.
        """
        pass

    @output_tb_dut.setter
    def output_tb_dut(self, value: str) -> None:
        """Set the sim DUT instance name."""
        pass

    @property
    def output_level(self) -> str:
        """
        Get the simulation flow level.

        :return: The simulation flow level.
        """
        pass

    @output_level.setter
    def output_level(self, value: str) -> None:
        """Set the simulation flow level."""
        pass

class HammerPowerTool(HammerTool):

    @property
    def level(self) -> FlowLevel:
        """Return the flow level."""
        pass

    def get_power_report_configs(self) -> List[PowerReport]:
        """
        Get the power report config settings
        """
        pass

    @property
    def flow_database(self) -> str:
        """
        Get the path to syn or par database for power analysis.

        :return: The path to syn or par database for power analysis.
        """
        pass

    @flow_database.setter
    def flow_database(self, value: str) -> None:
        """Set the path to syn or par database for power analysis."""
        pass

    @property
    def input_files(self) -> List[str]:
        """
        Get the paths to RTL input files or design netlist.

        :return: The paths to RTL input files or design netlist.
        """
        pass

    @input_files.setter
    def input_files(self, value: List[str]) -> None:
        """Set the paths to RTL input files or design netlist."""
        pass

    @property
    def spefs(self) -> List[str]:
        """
        Get the list of spef files for power anlaysis.

        :return: The list of spef files for power anlaysis.
        """
        pass

    @spefs.setter
    def spefs(self, value: List[str]) -> None:
        """Set the list of spef files for power anlaysis."""
        pass

    @property
    def sdc(self) -> Optional[str]:
        """
        Get the (optional) input SDC constraint file.

        :return: The (optional) input SDC constraint file.
        """
        pass

    @sdc.setter
    def sdc(self, value: Optional[str]) -> None:
        """Set the (optional) input SDC constraint file."""
        pass

    @property
    def waveforms(self) -> List[str]:
        """
        Get the list of waveform dump files for dynamic power analysis.

        :return: The list of waveform dump files for dynamic power analysis.
        """
        pass

    @waveforms.setter
    def waveforms(self, value: List[str]) -> None:
        """Set the list of waveform dump files for dynamic power analysis."""
        pass

    @property
    def saifs(self) -> List[str]:
        """
        Get the list of activity files for dynamic power analysis.

        :return: The list of activity files for dynamic power analysis.
        """
        pass

    @saifs.setter
    def saifs(self, value: List[str]) -> None:
        """Set the list of activity files for dynamic power analysis."""
        pass

    @property
    def top_module(self) -> str:
        """
        Get the top RTL module.

        :return: The top RTL module.
        """
        pass

    @top_module.setter
    def top_module(self, value: str) -> None:
        """Set the top RTL module."""
        pass

    @property
    def tb_name(self) -> str:
        """
        Get the testbench name.

        :return: The testbench name.
        """
        pass

    @tb_name.setter
    def tb_name(self, value: str) -> None:
        """Set the testbench name."""
        pass

    @property
    def tb_dut(self) -> str:
        """
        Get the DUT instance name.

        :return: The DUT instance name.
        """
        pass

    @tb_dut.setter
    def tb_dut(self, value: str) -> None:
        """Set the DUT instance name."""
        pass

class HammerFormalTool(HammerTool):

    @property
    def check(self) -> str:
        """
        Get the formal verification check type to run.

        :return: The formal verification check type to run.
        """
        pass

    @check.setter
    def check(self, value: str) -> None:
        """Set the formal verification check type to run."""
        pass

    @property
    def input_files(self) -> List[str]:
        """
        Get the input collection of implementation design files.

        :return: The input collection of implementation design files.
        """
        pass

    @input_files.setter
    def input_files(self, value: List[str]) -> None:
        """Set the input collection of implementation design files."""
        pass

    @property
    def reference_files(self) -> List[str]:
        """
        Get the input collection of reference design files.

        :return: The input collection of reference design files.
        """
        pass

    @reference_files.setter
    def reference_files(self, value: List[str]) -> None:
        """Set the input collection of reference design files."""
        pass

    @property
    def top_module(self) -> str:
        """
        Get the top RTL module.

        :return: The top RTL module.
        """
        pass

    @top_module.setter
    def top_module(self, value: str) -> None:
        """Set the top RTL module."""
        pass

    @property
    def post_synth_sdc(self) -> Optional[str]:
        """
        Get the (optional) input post-synthesis SDC constraint file.

        :return: The (optional) input post-synthesis SDC constraint file.
        """
        pass

    @post_synth_sdc.setter
    def post_synth_sdc(self, value: Optional[str]) -> None:
        """Set the (optional) input post-synthesis SDC constraint file."""
        pass

class HammerTimingTool(HammerTool):

    @property
    def max_paths(self) -> FlowLevel:
        """Return the max paths to report."""
        pass

    @property
    def input_files(self) -> List[str]:
        """
        Get the input collection of design files.

        :return: The input collection of design files.
        """
        pass

    @input_files.setter
    def input_files(self, value: List[str]) -> None:
        """Set the input collection of design files."""
        pass

    @property
    def top_module(self) -> str:
        """
        Get the top RTL module.

        :return: The top RTL module.
        """
        pass

    @top_module.setter
    def top_module(self, value: str) -> None:
        """Set the top RTL module."""
        pass

    @property
    def post_synth_sdc(self) -> Optional[str]:
        """
        Get the (optional) input post-synthesis SDC constraint file.

        :return: The (optional) input post-synthesis SDC constraint file.
        """
        pass

    @post_synth_sdc.setter
    def post_synth_sdc(self, value: Optional[str]) -> None:
        """Set the (optional) input post-synthesis SDC constraint file."""
        pass

    @property
    def spefs(self) -> Optional[List]:
        """
        Get the (optional) list of SPEF files.

        :return: The (optional) list of SPEF files.
        """
        pass

    @spefs.setter
    def spefs(self, value: Optional[List]) -> None:
        """Set the (optional) list of SPEF files."""
        pass

    @property
    def sdf_file(self) -> Optional[str]:
        """
        Get the (optional) input SDF file.

        :return: The (optional) input SDF file.
        """
        pass

    @sdf_file.setter
    def sdf_file(self, value: Optional[str]) -> None:
        """Set the (optional) input SDF file."""
        pass

    @property
    def def_file(self) -> Optional[str]:
        """
        Get the (optional) input DEF file.

        :return: The (optional) input DEF file.
        """
        pass

    @def_file.setter
    def def_file(self, value: Optional[str]) -> None:
        """Set the (optional) input DEF file."""
        pass

class HasUPFSupport(HammerTool):
    """Mix-in trait with functions useful for tools with UPF style power constraints"""

    @property
    def upf_power_specification(self) -> str:
        pass

class HasCPFSupport(HammerTool):
    """Mix-in trait with functions useful for tools with CPF style power
    constraints"""

    @property
    def cpf_power_specification(self) -> str:
        pass

class HasSDCSupport(HammerTool):
    """Mix-in trait with functions useful for tools with SDC-style
    constraints."""

    @property
    def sdc_clock_constraints(self) -> str:
        """Generate TCL fragments for top module clock constraints."""
        pass

    @property
    def sdc_pin_constraints(self) -> str:
        """Generate a fragment for I/O pin constraints."""
        pass

    @property
    @abstractmethod
    def post_synth_sdc(self) -> Optional[str]:
        """
        Get the (optional) input post-synthesis SDC constraint file.

        :return: The (optional) input post-synthesis SDC constraint file.
        """
        pass

class TCLTool(HammerTool):
    """Mix-in trait for tools which consume a flat TCL file as input"""

    @property
    def output(self) -> List[str]:
        """
        Buffered output to be put in <name>.tcl
        """
        pass

    def verbose_append(self, cmd: str, clean: bool=False) -> None:
        pass

    def append(self, cmd: str, clean: bool=False) -> None:
        pass

    def block_append(self, cmds: str, clean: bool=True, verbose: bool=True) -> bool:
        pass

class MentorTool(HammerTool):
    """ Mix-in trait with functions useful for Mentor-Graphics-based tools. """

    @property
    def env_vars(self) -> Dict[str, str]:
        """
        Get the list of environment variables required for this tool.
        Note to subclasses: remember to include variables from super().env_vars!
        """
        pass

    def version_number(self, version: str) -> int:
        """
        Assumes versions look like NAME-YYYY.MM-SPMINOR.
        Assumes less than 100 minor versions.
        """
        pass

class MentorCalibreTool(MentorTool):
    """ Mix-in trait for Mentor's Calibre tool suite. """

    @property
    def env_vars(self) -> Dict[str, str]:
        """
        Get the list of environment variables required for this tool.
        Note to subclasses: remember to include variables from super().env_vars!
        """
        pass

def load_tool(tool_module: str) -> HammerTool:
    """
    Load the given tool.
    See the hammer-vlsi README for how it works.

    :param tool_module: The tool module e.g. "hammer.synthesis.yosys"
    :return: HammerTool of the given tool
    """
    pass

class HammerPCBDeliverableTool(HammerTool):

    @abstractmethod
    def fill_outputs(self) -> bool:
        pass

    @property
    def naming_scheme(self) -> BumpsPinNamingScheme:
        """
        Get the desired bump naming scheme.
        """
        pass

    @property
    def output_footprints(self) -> List[str]:
        """
        Get the list of the PCB footprint files for the project.

        :return: The list of the PCB footprint files for the project.
        """
        pass

    @output_footprints.setter
    def output_footprints(self, value: List[str]) -> None:
        """Set the list of the PCB footprint files for the project."""
        pass

    @property
    def output_schematic_symbols(self) -> List[str]:
        """
        Get the list of the PCB schematic symbol files for the project.

        :return: The list of the PCB schematic symbol files for the project.
        """
        pass

    @output_schematic_symbols.setter
    def output_schematic_symbols(self, value: List[str]) -> None:
        """Set the list of the PCB schematic symbol files for the project."""
        pass
