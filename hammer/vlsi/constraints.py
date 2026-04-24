import operator
from enum import Enum
from functools import reduce
from typing import Dict, NamedTuple, Optional, List, Any, Tuple, Union, cast
from hammer.utils import reverse_dict, get_or_else, add_dicts
from hammer.tech import MacroSize
from .units import TimeValue, VoltageValue, TemperatureValue, CapacitanceValue
from decimal import Decimal
import math
import string

class ILMStruct(NamedTuple('ILMStruct', [('dir', str), ('data_dir', str), ('module', str), ('lef', str), ('gds', str), ('netlist', str), ('sim_netlist', Optional[str]), ('sdcs', List[str])])):
    __slots__ = ()

    def to_setting(self) -> dict:
        pass

    @staticmethod
    def from_setting(ilm: dict) -> 'ILMStruct':
        pass

class SRAMParameters(NamedTuple('SRAMParameters', [('name', str), ('family', str), ('depth', int), ('width', int), ('mask', bool), ('vt', str), ('mux', int)])):
    __slots__ = ()

    @staticmethod
    def from_setting(d: dict) -> 'SRAMParameters':
        pass
Supply = NamedTuple('Supply', [('name', str), ('pins', Optional[List[str]]), ('tie', Optional[str]), ('weight', Optional[int]), ('voltage', Optional[str])])

class PinAssignmentError(ValueError):
    """Exception raised from parsing an invalid PinAssignment object."""

class PinAssignmentSemiAutoError(PinAssignmentError):
    """Exception raised from parsing a PinAssignment that requires semi-auto features without explicitly enabing
    them."""

class PinAssignmentPreplacedError(PinAssignmentError):
    """Exception raised from parsing a preplaced pin with extraneous information."""

    def __init__(self, pin: 'PinAssignment') -> None:
        self.pin = pin

    def __str__(self) -> str:
        return 'Pins {p} assigned as a preplaced pin with layers or side. Assuming pins are preplaced pins and ignoring layers and side.'.format(p=self.pin.pins)

class PinAssignment(NamedTuple('PinAssignment', [('pins', str), ('side', Optional[str]), ('layers', Optional[List[str]]), ('preplaced', bool), ('location', Optional[Tuple[float, float]]), ('width', Optional[float]), ('depth', Optional[float])])):
    __slots__ = ()

    def __new__(cls, pins: str, side: Optional[str]=None, layers: Optional[List[str]]=None, preplaced: Optional[bool]=None, location: Optional[Tuple[float, float]]=None, width: Optional[float]=None, depth: Optional[float]=None) -> 'PinAssignment':
        return super().__new__(cls, pins, side, layers, get_or_else(preplaced, False), location, width, depth)

    @staticmethod
    def create(pins: str, side: Optional[str]=None, layers: Optional[List[str]]=None, preplaced: Optional[bool]=None, location: Optional[Tuple[float, float]]=None, width: Optional[float]=None, depth: Optional[float]=None) -> 'PinAssignment':
        """
        Static method that works around the fact that mypy gets very confused at
        the custom constructor above that defines default arguments.
        """
        pass

    @staticmethod
    def from_dict(raw_assign: Dict[str, Any], semi_auto: bool=True) -> 'PinAssignment':
        pass

    def to_dict(self) -> dict:
        pass
BumpAssignment = NamedTuple('BumpAssignment', [('name', Optional[str]), ('no_connect', Optional[bool]), ('x', Decimal), ('y', Decimal), ('group', Optional[str]), ('custom_cell', Optional[str])])
BumpsDefinition = NamedTuple('BumpsDefinition', [('x', int), ('y', int), ('pitch_x', Decimal), ('pitch_y', Decimal), ('global_x_offset', Decimal), ('global_y_offset', Decimal), ('cell', str), ('assignments', List[BumpAssignment])])

class BumpsPinNamingScheme(Enum):
    A0 = 0
    A1 = 1
    A00 = 2
    A01 = 3
    Index = 4

    @classmethod
    def __mapping(cls) -> Dict[str, 'BumpsPinNamingScheme']:
        pass

    @staticmethod
    def from_str(input_str: str) -> 'BumpsPinNamingScheme':
        pass

    def __str__(self) -> str:
        return reverse_dict(BumpsPinNamingScheme.__mapping())[self]

    def sort_by_name(self, definition: BumpsDefinition, assignments: List[BumpAssignment]) -> List[BumpAssignment]:
        """
        Sort a list of bump assignments for a given bump definition by their name in a human-readable way.

        :param definition: The bumps definition
        :param assignments: The list of bump assignments which may or may not be equivalent to definition.assignments
        :return: A sorted list of bump assignments
        """
        pass

    def name_bump(self, definition: BumpsDefinition, assignment: BumpAssignment) -> str:
        pass
ClockPort = NamedTuple('ClockPort', [('name', str), ('period', Optional[TimeValue]), ('path', Optional[str]), ('uncertainty', Optional[TimeValue]), ('generated', Optional[bool]), ('source_path', Optional[str]), ('divisor', Optional[int]), ('group', Optional[str])])
OutputLoadConstraint = NamedTuple('OutputLoadConstraint', [('name', str), ('load', CapacitanceValue)])

class DelayConstraint(NamedTuple('DelayConstraint', [('name', str), ('clock', str), ('direction', str), ('delay', TimeValue), ('corner', Optional[str])])):
    __slots__ = ()

    def __new__(cls, name: str, clock: str, direction: str, delay: TimeValue, corner: Optional[str]) -> 'DelayConstraint':
        if direction not in ('input', 'output'):
            raise ValueError(f'Invalid direction {direction} for a delay constraint')
        if corner is not None:
            if corner not in ('setup', 'hold'):
                raise ValueError(f'Invalid corner {corner} for a delay constraint')
        return super().__new__(cls, name, clock, direction, delay, corner)

    @staticmethod
    def from_dict(delay_src: Dict[str, Any]) -> 'DelayConstraint':
        pass

    def to_dict(self) -> dict:
        pass

class DecapConstraint(NamedTuple('DecapConstraint', [('target', str), ('density', Optional[Decimal]), ('capacitance', Optional[CapacitanceValue]), ('x', Optional[Decimal]), ('y', Optional[Decimal]), ('width', Optional[Decimal]), ('height', Optional[Decimal])])):
    __slots__ = ()

    def __new__(cls, target: str, density: Optional[Decimal], capacitance: Optional[CapacitanceValue], x: Optional[Decimal], y: Optional[Decimal], width: Optional[Decimal], height: Optional[Decimal]) -> 'DecapConstraint':
        if target not in ('capacitance', 'density'):
            raise ValueError('Invalid target {target}'.format(target=target))
        if target == 'density' and density is None:
            raise ValueError('Need to specify decap density')
        if density is not None:
            if density > Decimal(1) or density < Decimal(0):
                raise ValueError('Density must be between 0 and 1, inclusive')
        if target == 'capacitance' and capacitance is None:
            raise ValueError('Need to specify decap capacitance')
        all_none = all((x is None for x in (x, y, width, height)))
        all_specified = all((x is not None for x in (x, y, width, height)))
        if not (all_none or all_specified):
            raise ValueError('Decap x, y, width, and height must all be specified')
        return super().__new__(cls, target, density, capacitance, x, y, width, height)

    @staticmethod
    def from_dict(decap_src: Dict[str, Any]) -> 'DecapConstraint':
        pass

    def to_dict(self) -> dict:
        pass

class ObstructionType(Enum):
    Place = 1
    Route = 2
    Power = 3

    @classmethod
    def __mapping(cls) -> Dict[str, 'ObstructionType']:
        pass

    @staticmethod
    def from_str(input_str: str) -> 'ObstructionType':
        pass

    def __str__(self) -> str:
        return reverse_dict(ObstructionType.__mapping())[self]

class PlacementConstraintType(Enum):
    Dummy = 1
    SoftPlacement = 2
    HardPlacement = 3
    TopLevel = 4
    HardMacro = 5
    Hierarchical = 6
    Obstruction = 7
    Overlap = 8

    @classmethod
    def __mapping(cls) -> Dict[str, 'PlacementConstraintType']:
        pass

    @staticmethod
    def from_str(input_str: str) -> 'PlacementConstraintType':
        pass

    def __str__(self) -> str:
        return reverse_dict(PlacementConstraintType.__mapping())[self]

class Margins(NamedTuple('Margins', [('left', Decimal), ('bottom', Decimal), ('right', Decimal), ('top', Decimal)])):

    @staticmethod
    def from_dict(d: dict) -> 'Margins':
        pass

    @staticmethod
    def empty() -> 'Margins':
        pass

    def to_dict(self) -> dict:
        pass

class PlacementConstraint(NamedTuple('PlacementConstraint', [('path', str), ('type', PlacementConstraintType), ('x', Decimal), ('y', Decimal), ('width', Decimal), ('height', Decimal), ('master', Optional[str]), ('create_physical', Optional[bool]), ('orientation', Optional[str]), ('margins', Optional[Margins]), ('top_layer', Optional[str]), ('layers', Optional[List[str]]), ('obs_types', Optional[List[ObstructionType]])])):
    __slots__ = ()

    @staticmethod
    def _get_master(constraint_type: PlacementConstraintType, constraint: dict) -> Optional[str]:
        """
        A helper method to retrieve the master key from a constraint dict. This is broken out into its own function because it's
        used in multiple methods. The master key is mandatory for Hierarchical constraint, optional for HardMacro constraints,
        and disallowed otherwise.

        :param constraint_type: A PlacementConstraintType object describing the type of constraint
        :param constraint: A dict that may or may not contain a master key
        :return: The value pointed to by master or None, if allowed by the constraint type
        """
        pass

    @staticmethod
    def from_masters_and_dict(masters: List[MacroSize], constraint: dict) -> 'PlacementConstraint':
        """
        Create a PlacementConstraint tuple from a constraint dict and a list of masters. This method differs from from_dict by
        allowing the width and height to be auto-filled from a list of masters for the Hierarchical and HardMacro constraint types.

        :param masters: A list of MacroSize tuples containing cell macro definitions
        :param constraint: A dict containing information to be parsed into a PlacementConstraint tuple
        :return: A PlacementConstraint tuple
        """
        pass

    @staticmethod
    def from_dict(constraint: dict) -> 'PlacementConstraint':
        pass

    def to_dict(self) -> dict:
        pass

class MMMCCornerType(Enum):
    Setup = 1
    Hold = 2
    Extra = 3

    @staticmethod
    def from_string(input_str: str) -> 'MMMCCornerType':
        pass
MMMCCorner = NamedTuple('MMMCCorner', [('name', str), ('type', MMMCCornerType), ('voltage', VoltageValue), ('temp', TemperatureValue)])
