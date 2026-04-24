import importlib.resources
import json
import numbers
import os
import re
from decimal import Decimal
from enum import Enum
from importlib import resources
from functools import lru_cache, reduce
from typing import Any, Callable, Dict, Iterable, List, NamedTuple, Optional, Set, Tuple, Union
from hammer.logging import HammerVLSILogging, HammerVLSILoggingContext
from hammer.utils import add_dicts, deepdict, topological_sort
from .yaml2json import load_yaml

class HammerJSONEncoder(json.JSONEncoder):

    def default(self, o):
        pass
_CONFIG_PATH_KEY = '_config_path'
_NEXT_FREE_INDEX_KEY = '_next_free_index'

def _get_next_free_index(d: dict) -> int:
    """
    Get the next free index in the given dictionary.
    Side effect: increments the next free index stored in the dictionary by 1.
    If the key does not exist, create it and set it to 2, and return 1.
    :param d: Dictionary to find the next free index in.
    :return: Next free index.
    """
    pass

class MetaDirective(NamedTuple('MetaDirective', [('action', Callable[[dict, str, Any], None]), ('target_settings', Callable[[str, Any], List[str]]), ('rename_target', Callable[[str, Any, str, str], Optional[Tuple[Any, str]]])])):
    __slots__ = ()

def deepsubst_cwd(config_dict: dict, path: str) -> str:
    """
    Prepend the current working directory (of the hammer runtime) to the beginning of the
    specified path.

    :param config_dict: The original config dict (not used by this method).
    :param path: The string path to which the CWD is to be prepended.
    :return: The path with CWD prepended.
    """
    pass

def deepsubst_local(config_dict: dict, path: str) -> str:
    """
    Prepend the directory containing the config file containing this setting to the
    beginning of the specified path.

    :param config_dict: The original config dict.
    :param path: The string path to which the local path is to be prepended.
    :return: The path with local path of the config prepended.
    """
    pass

def deepsubst_transclude(config_dict: dict, path: str) -> str:
    """
    Load the path given as the new value of this key

    :param config_dict: The original config dict (not used by this method).
    :param path: The string path to the file to be included
    :return: The contents of the file at path
    """
    pass
DeepSubstMetaDirectives = {'cwd': deepsubst_cwd, 'local': deepsubst_local, 'transclude': deepsubst_transclude}

@lru_cache(maxsize=2)
def get_meta_directives() -> Dict[str, MetaDirective]:
    """
    Get all meta directives available.
    :return: Meta directives indexed by action (e.g. "subst").
    """
    pass

def unpack(config_dict: dict, prefix: str='') -> dict:
    """
    Unpack the given config_dict, flattening key names recursively.
    >>> p = unpack({"one": 1, "two": 2}, prefix="snack")
    >>> p == {'snack.one': 1, 'snack.two': 2}
    True
    >>> p = unpack({"a": {"foo": 1, "bar": 2}})
    >>> p == {'a.foo': 1, 'a.bar': 2}
    True
    >>> p = unpack({"a.b": {"foo": 1, "bar": 2}})
    >>> p == {"a.b.foo": 1, "a.b.bar": 2}
    True
    >>> p = unpack({
    ...     "a": {
    ...         "foo": 1,
    ...         "bar": 2
    ...     },
    ...     "b": {
    ...         "baz": 3,
    ...         "boom": {"rocket": "chip", "hwacha": "vector"}
    ...     },
    ... })
    >>> p == {"a.foo": 1, "a.bar": 2, "b.baz": 3, "b.boom.rocket": "chip",
    ...     "b.boom.hwacha": "vector"}
    True
    """
    pass

def reverse_unpack(input_dict: dict) -> dict:
    """
    Reverse the effects of unpack(). Mainly useful for testing purposes.
    >>> p = reverse_unpack({"a.b": 1})
    >>> p == {"a": {"b": 1}}
    True
    :param input: Unpacked input_dict dictionary
    :return: Packed equivalent of input_dict
    """
    pass
__VARIABLE_EXPANSION_REGEX = '\\${([a-zA-Z_\\-\\d.]+)}'

def update_and_expand_meta(config_dict: dict, meta_dict: dict) -> dict:
    """
    Expand the meta directives for the given config dict and return a new
    dictionary containing the updated settings with respect to the base config_dict.

    :param config_dict: Base config.
    :param meta_dict: Dictionary with potentially new meta directives.
    :return: New dictionary with meta_dict updating config_dict.
    """
    pass

class HammerDatabase:
    """
    Define a database which is composed of a set of overridable configs.
    We need something like this in order to e.g. bind technology afterwards, since we never want technology to override project.
    If we just did an .update() with the technology config, we'd possibly lose the previously-bound project config.

    Terminology:
    - setting: a single key-value pair e.g. "vlsi.core.technology" -> "footech"
    - config: a single concrete dictionary of settings.
    - database: a collection of configs with a specific override hierarchy.

    Order of precedence (in increasing order):
    - builtins
    - core
    - tools
    - technology
    - environment
    - project
    - runtime (settings lazyally updated during the run a hammer run)
    """

    def __init__(self) -> None:
        self.builtins = []
        self.core = []
        self.tools = []
        self.technology = []
        self.environment = []
        self.project = []
        self._runtime = {}
        self.__config_cache = {}
        self.__config_cache_dirty = False
        self.__config_types = {}
        self.defaults = {}
        self.logger = HammerVLSILogging().context()

    @property
    def runtime(self) -> List[dict]:
        pass

    @staticmethod
    def internal_keys() -> List[str]:
        """Internal keys that shouldn't show up in any final config."""
        pass

    def get_config(self) -> dict:
        """
        Get the config of this database after all the overrides have been dealt with.
        """
        pass

    @property
    def get_config_types(self) -> dict:
        """
        Get the types for the configuration of a database.
        """
        pass

    def get_database_json(self) -> str:
        """Get the database (get_config) in JSON form as a string.
        """
        pass

    def get(self, key: str) -> Any:
        """Alias for get_setting()."""
        pass

    def get_suffix(self, key: str, suffix: str) -> Any:
        """Alias for get_setting_suffix()."""
        pass

    def __getitem__(self, key: str) -> Any:
        """Alias for get_setting()."""
        return self.get_setting(key)

    def __contains__(self, item: str) -> bool:
        """Alias for has_setting()."""
        return self.has_setting(item)

    def get_setting(self, key: str, nullvalue: Any=None, check_type: bool=True) -> Any:
        """
        Retrieve the given key.

        :param key: Desired key.
        :param nullvalue: Value to return out for nulls.
        :param check_type: Flag to enforce type checking
        :return: The given config
        """
        pass

    def get_setting_suffix(self, key: str, suffix: str, nullvalue: Any=None, check_type: bool=True) -> Any:
        """
        Retrieve a key, first trying with a suffix but returning base if found.

        :param key: Desired key.
        :param suffix: Required suffix to search for.
        :param nullvalue: Value to return out for nulls.
        :param check_type: Flag to enforce type checking
        :return: The given config
        """
        pass

    def set_setting(self, key: str, value: Any) -> None:
        """
        Set the given key. The setting will be placed into the runtime dictionary.

        :param key: Key
        :param value: Value for key
        """
        pass

    def has_setting(self, key: str) -> bool:
        """
        Check if the given key exists in the database.

        :param key: Desired key.
        :return: True if the given setting exists.
        """
        pass

    def get_setting_type(self, key: str, nullvalue: Any=None) -> Any:
        """
        Acquire the type of a given key.

        :param key: Desired key.
        :param nullvalue: Value to return for nulls.
        :return: Data type of key.
        """
        pass

    def set_setting_type(self, key: str, value: Any) -> None:
        """
        Set the given key type.

        :param key: Key
        :param value: Value for key
        """
        pass

    def has_setting_type(self, key: str) -> bool:
        """
        Check if the given key type exists in the database.

        :param key: Desired key.
        :return: True if the given setting exists.
        """
        pass

    def check_setting(self, key: str, cfg: Optional[dict]=None) -> bool:
        """
        Checks a setting for correct typing.
        """
        pass

    def get_settings_from_dict(self, key_default_dict: Dict[str, Any], key_prefix: str='', optional_keys: List[str]=[]) -> Dict[str, str]:
        """
        Gets input values for multiple keys.
        :param key_default_dict: Specify a dictionary of requested keys and default values.
        :param key_prefix: Specify a prefix for the given keys.
        :optional_keys: Specify optional keys where if no setting is provided a default value of None will be provided.
        :return: A dictionary of keys and corresponding input values.
        """
        pass

    def update_core(self, core_config: List[dict], core_config_types: List[dict]) -> None:
        """
        Update the core config with the given core config.
        """
        pass

    def update_tools(self, tools_config: List[dict], tool_config_types: List[dict]) -> None:
        """
        Update the tools config with the given tools config.
        """
        pass

    def update_technology(self, technology_config: List[dict], technology_config_types: List[dict]) -> None:
        """
        Update the technology config with the given technology config.
        """
        pass

    def update_environment(self, environment_config: List[dict]) -> None:
        """
        Update the environment config with the given environment config.
        """
        pass

    def update_project(self, project_config: List[dict]) -> None:
        """
        Update the project config with the given project config.
        """
        pass

    def update_builtins(self, builtins_config: List[dict]) -> None:
        """
        Update the builtins config with the given builtins config.
        """
        pass

    def update_defaults(self, default_configs: List[dict]) -> None:
        """
        Update the default configs with the given config list.
        This dict gets updated with each additional defaults config file.
        """
        pass

    def update_types(self, config_types: List[dict], check_type: bool=True) -> None:
        """
        Update the types config with the given types config.
        """
        pass

def load_config_from_string(contents: str, is_yaml: bool, path: str='unspecified') -> dict:
    """
    Load config from a string by loading it and unpacking it.

    :param contents: Contents of the config.
    :param is_yaml: True if the contents are yaml.
    :param path: Path to the folder/package where the config file is located.
    :return: Loaded config dictionary, unpacked.
    """
    pass

def load_config_from_defaults(package: str, types: bool=False) -> Tuple[List[dict], List[dict]]:
    """
    Load config from a package's defaults.

    :param package: Package name
    :param types: True if the types file(s) is to also be read
    :return: Loaded config dictionary
    """
    pass

def combine_configs(configs: Iterable[dict]) -> dict:
    """
    Combine the given list of *unpacked* configs into a single config.
    Later configs in the list will override the earlier configs.

    :param configs: List of configs.
    :param handle_meta: Handle meta configs?
    :return: A loaded config dictionary.
    """
    pass

class NamedType(Enum):
    STR = 'str'
    INT = 'int'
    FLOAT = 'float'
    BOOL = 'bool'
    LIST = 'list'
    DICT = 'dict'
    ANY = 'Any'

class ConfigType(NamedTuple):
    """
    Class for a parsed configuration type.

    :param primary: the outermost type on a configuration.
    :param optional: if the type is an Optional type.
    :param secondary: the type within the type, i.e. what is in a list.
    :param tertiary_k: the key type stored in a dictionary.
    :param tertiary_v: the value type stored in a dictionary.
    """
    primary: NamedType
    optional: bool = False
    secondary: NamedType = NamedType.ANY
    tertiary_k: NamedType = NamedType.ANY
    tertiary_v: NamedType = NamedType.ANY
PRIMARY_REGEX = re.compile('(\\w+)')
INNER_REGEX = re.compile('\\w+\\[(.+)\\]')
DICT_REGEX = re.compile('\\w+\\[(\\w+), (\\w+)\\]')

def parse_setting_type(setting_type: str) -> ConfigType:
    """
    Parses a configuration type.
    :param setting_type: The string form of a setting configuration.
    :return: A configuration type dataclass with info about the type.
    """
    pass
