from decimal import Decimal
from functools import reduce
import os
import re
import shutil
from subprocess import Popen, PIPE
from textwrap import dedent as dd
from typing import List, Optional, Dict, Set, Union
from hammer.utils import add_dicts
from hammer.vlsi import HasSDCSupport, HammerSynthesisTool, HammerPlaceAndRouteTool, HammerDRCTool, PlacementConstraintType, TimeValue, TCLTool, HammerTool
import hammer.tech as hammer_tech

class OpenROADTool(HasSDCSupport, TCLTool, HammerTool):
    """ Mix-in trait with functions useful for OpenROAD-flow tools."""

    @property
    def env_vars(self) -> Dict[str, str]:
        """
        Get the list of environment variables required for this tool.
        Note to subclasses: remember to include variables from
        super().env_vars!
        """
        pass

    def validate_openroad_installation(self) -> None:
        """
        make sure OPENROAD env-var is set, and klayout is in the path (since
        klayout is not installed with OPENROAD as of version 1.1.0. this
        should be called in steps that actually run tools or touch filepaths
        """
        pass

    def openroad_flow_path(self) -> str:
        """return the root of the OpenROAD-flow installation"""
        pass

    def openroad_flow_makefile_path(self) -> str:
        """drive OpenROAD-flow's top-level Makefile from hammer"""
        pass

    def syn_rundir_path(self) -> str:
        pass

    def syn_objects_path(self) -> str:
        """where the intermediate synthesis output objects are located"""
        pass

    def syn_results_path(self) -> str:
        """where the intermediate synthesis final results are located"""
        pass

    def design_config_path(self) -> str:
        """
        the initial design_config is written by the synthesis step. any other
        tool must refer to this design_config
        """
        pass

    def par_rundir_path(self) -> str:
        pass

    def par_objects_path(self) -> str:
        """where the intermediate par output objects are located"""
        pass

    def par_results_path(self) -> str:
        """where the intermediate par final results are located"""
        pass

    def version_number(self, version: str) -> int:
        """get OPENROAD-flow's version from one of its header files"""
        pass

    def setup_openroad_rundir(self) -> bool:
        """
        OpenROAD expects several files/dirs in the current run_dir, so we
        symlink them in from the OpenROAD-flow installation
        """
        pass

class OpenROADSynthesisTool(HammerSynthesisTool, OpenROADTool):
    """ Mix-in trait with functions for OpenROAD-flow synthesis tools."""

    def _clock_period_value(self) -> str:
        """this string is used in the makefile fragment used by OpenROAD"""
        pass

    def _floorplan_bbox(self) -> str:
        """this string is used in the makefile fragment used by OpenROAD"""
        pass

    def create_design_config(self) -> bool:
        """
        the design-config is the main configuration for the OpenROAD built-in
        scripts. initially, we are using OpenROAD's tool scripts as-is, so
        we need to create a design-config that their scripts understand. the
        synthesis tool is the only tool that will write this
        """
        pass

class OpenROADPlaceAndRouteTool(HammerPlaceAndRouteTool, OpenROADTool):
    """ Mix-in trait with functions for OpenROAD-flow par tools."""

    def specify_power_straps(self, layer_name: str, bottom_via_layer_name: str, blockage_spacing: Decimal, pitch: Decimal, width: Decimal, spacing: Decimal, offset: Decimal, bbox: Optional[List[Decimal]], nets: List[str], add_pins: bool, antenna_trim_shape: str) -> List[str]:
        pass

    def specify_std_cell_power_straps(self, blockage_spacing: Decimal, bbox: Optional[List[Decimal]], nets: List[str]) -> List[str]:
        pass

class OpenROADDRCTool(HammerDRCTool, OpenROADTool):
    """ Mix-in trait with functions for OpenROAD-flow drc tools."""

    @property
    def post_synth_sdc(self) -> Optional[str]:
        pass

    def globally_waived_drc_rules(self) -> List[str]:
        pass

    def drc_results_pre_waived(self) -> Dict[str, int]:
        pass
