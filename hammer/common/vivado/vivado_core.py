from typing import Dict, List, Optional
import os
import shutil
from abc import ABCMeta
from hammer.utils import deepdict
from hammer.vlsi import HammerTool

class VivadoCommon(HammerTool, metaclass=ABCMeta):

    @property
    def env_vars(self) -> Dict[str, str]:
        pass

    def append(self, cmd: str) -> None:
        pass

    def setup_workspace(self) -> bool:
        pass

    def get_file_contents(self, file_name: str, file_params: Optional[Dict[str, str]]) -> str:
        pass

    def append_file(self, file_name: str, file_params: Optional[Dict[str, str]]) -> None:
        pass

    def generate_board_defs(self) -> bool:
        pass

    def generate_paths_and_src_defs(self) -> bool:
        pass

    def generate_project_defs(self) -> bool:
        pass

    def generate_run_script(self, script_name: str, file_params: Dict[str, str]) -> str:
        pass
