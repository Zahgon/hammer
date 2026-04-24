from .driver import HammerDriver
import os
import sys
import textwrap
from typing import List, Dict, Tuple, Callable

def build_noop(driver: HammerDriver, append_error_func: Callable[[str], None]) -> dict:
    """
    Do nothing, just return the dependency graph.

    :param driver: The HammerDriver
    :return: The dependency graph
    """
    pass

def build_makefile(driver: HammerDriver, append_error_func: Callable[[str], None]) -> dict:
    """
    Build a Makefile include in the obj_dir called hammer.d. This is intended to be dynamically
    created and included into a top-level Makefile.

    The Makefile will contain targets for the following hammer actions, as well as any necessary
    bridge actions (xyz-to-abc):
        - pcb
        - syn
        - par
        - drc
        - lvs
        - sim-rtl
        - sim-syn
        - sim-par
        - power-rtl
        - power-syn
        - power-par
        - formal-syn
        - formal-par
        - timing-syn
        - timing-par

    For hierarchical flows, the syn, par, drc, lvs, sim, power, formal, and timing actions will all be suffixed with the name
    of the hierarchical modules (e.g. syn-Top, syn-SubModA, par-SubModA, etc.). The appropriate
    dependencies and bridge actions are automatically generated from the hierarchy provided in the
    Hammer IR.

    For actions that can be run at multiple points in the flow such as sim, the name of the target
    will include the action it is being run after (e.g. sim-syn, sim-par, etc.). With no suffix
    an rtl level simulation will be run.

    Additionally, "redo" steps are created (e.g. redo-par for flat designs or redo-par-Top for
    hierarchical), which allow the user to bypass the normal Makefile dependencies and force a
    rerun of a particular task. This is useful when the user wants to change an input Hammer IR file
    knowing it will not affect intermediate steps in the design.

    An example use case for integrating this file into a top flow is provided below. Be sure to use
    real tabs if copying this snippet!

    ```
    TOP ?= MyTop
    OBJ_DIR ?= $(abspath build-$(TOP))
    INPUT_CONFS ?= foo.yaml bar.yaml baz.yaml

    HAMMER_EXEC ?= ./mychip-vlsi.py

    .PHONY: all
    all: drc-$(TOP) lvs-$(TOP)

    GENERATED_CONF = $(OBJ_DIR)/input.yaml

    $(GENERATED_CONF):
        echo "synthesis.inputs.top_module: $(TOP)" > $@
        echo "pcb.inputs.top_module: $(TOP)" >> $@

    $(OBJ_DIR)/hammer.d: $(GENERATED_CONF)
        $(HAMMER_EXEC) -e env.yaml $(foreach x,$(INPUT_CONFS) $(GENERATED_CONF), -p $(x)) --obj_dir $(OBJ_DIR) build

    include $(OBJ_DIR)/hammer.d
    ```

    The generated Makefile has a few variables that are set if absent. This allows the user to override them without
    modifying hammer.d. They are listed as follows:
        - HAMMER_EXEC: This sets the actual python executable containing the HammerDriver main() function. It is set to
          the executable used to generate the Makefile by default.
        - HAMMER_DEPENDENCIES: The list of dependences to use for the initial syn and pcb targets. It is set to the set
          of all input configurations, environment settings, and input files by default.
        - HAMMER_*_DEPENDENCIES: There is a version of this variable for each action. It allows the user to have more
          fine grained depencies compared to the blunt HAMMER_DEPENDENCIES. It is set as a dependency for the respective
          action. Often used with clearing the global HAMMER_DEPENDENCIES.
        - HAMMER_EXTRA_ARGS: This is passed to the Hammer executable for all targets. This is unset by default.
          Its primary uses are for adding additional configuration files with -p, --to_step/until_step, and/or --from_step/
          after_step options. An example use is "make redo-par-Top HAMMER_EXTRA_ARGS="-p patch.yaml --from_step placement".

    :param driver: The HammerDriver
    :return: The dependency graph
    """
    pass
BuildSystems = {'make': build_makefile, 'none': build_noop}
