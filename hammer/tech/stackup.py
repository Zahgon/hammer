from decimal import Decimal
from enum import Enum
from functools import partial
from typing import Any, List, Tuple, Optional
from pydantic import model_validator, ConfigDict, BaseModel
from hammer.utils import coerce_to_grid
from hammer.logging import HammerVLSILoggingContext

class RoutingDirection(str, Enum):
    """
    Represents a preferred routing direction for a metal layer.
    Note that this represents a *preferred* direction, not a DRC rule.
    """
    Vertical = 'vertical'
    Horizontal = 'horizontal'
    Redistribution = 'redistribution'

    def opposite(self) -> 'RoutingDirection':
        """
        Return the opposite routing direction.
        For Redistribution, this returns itself.
        :return: Opposite routing direction
        """
        pass

class WidthSpacingTuple(BaseModel):
    """
    A tuple of wire width limit and spacing for generating a piecewise linear rule
    for spacing based on wire width.

    width_at_least: Any wires larger than this must obey the minSpacing rule.
    min_spacing: The minimum spacing for this bin.
                 If a wire is wider than multiple entries, the worst-case (larger)
                 minSpacing wins.
    """
    width_at_least: Decimal
    min_spacing: Decimal

    @staticmethod
    def from_setting(grid_unit: Decimal, d: dict) -> 'WidthSpacingTuple':
        pass

    @staticmethod
    def from_list(grid_unit: Decimal, l: List[dict]) -> List['WidthSpacingTuple']:
        pass

class Metal(BaseModel):
    """
    A metal layer and some basic info about it.

    name: Metal layer name (e.g. M1, M2).
    index: The order in the stackup (lower is closer to the substrate).
    direction: The preferred routing direction of this metal layer, or
               RoutingDirection.Redistribution for non-routing top-level
               redistribution metals like Aluminium.
    min_width: The minimum wire width for this layer.
    max_width: The maximum wire width for this layer.
    pitch: The minimum cross-mask pitch for this layer (NOT same-mask pitch
           for multiple-patterned layers). Width of routing grid for a given layer.
           To route denser wires on chip, multiple masks are required.
           During fabrication, the masks are applied separately with some spatial offsets
           to achieve denser line patterning. For more information on multiple-patterning,
           check https://en.wikipedia.org/wiki/Multiple_patterning
    offset: The routing track offset from the origin for the first track in this layer.
            (0 = first track is on an axis).
    power_strap_widths_and_spacings: A list of WidthSpacingTuples that specify the minimum
                                     spacing rules for an infinitely long wire of variying width.
    power_strap_width_table: A list of allowed metal widths in the technology.
                             Widths smaller than the last number must be quantized to a value in the table.
    grid_unit: The fixed-point decimal value of a minimum grid unit (e.g. 1nm = 0.001).
               For most technologies, this comes from the technology plugin and is the same for all layers.
    """
    name: str
    index: int
    direction: RoutingDirection
    min_width: Decimal
    max_width: Optional[Decimal] = None
    pitch: Decimal
    offset: Decimal
    power_strap_widths_and_spacings: List[WidthSpacingTuple]
    power_strap_width_table: List[Decimal] = []
    grid_unit: Decimal
    model_config = ConfigDict(use_enum_values=True)

    @model_validator(mode='before')
    @classmethod
    def widths_must_snap_to_grid(cls, values):
        pass

    @staticmethod
    def from_setting(grid_unit: Decimal, d: dict) -> 'Metal':
        """
        Return a Metal object from a dict with keys "name", "index", "direction", "min_width", "max_width", "pitch", "offset", "power_strap_widths_and_spacings", and "power_strap_width_table"

        :param grid_unit: The manufacturing grid unit in um
        :param d: A dict containing the keys "name", "index", "direction", "min_width", "max_width", "pitch", "offset", "power_strap_widths_and_spacings", and "power_strap_width_table"
        """
        pass

    @staticmethod
    def power_strap_widths_from_list(grid_unit: Decimal, l: List[Any]) -> List[Decimal]:
        """
        Read and cocerce wire widths from the technology LEF width table.
        """
        pass

    def get_spacing_for_width(self, width: Decimal) -> Decimal:
        """
        Get the minimum spacing for a provided width.

        :param width: Width to calculate minimum spacing for.
        :return: Minimum spacing for `width`
        """
        pass

    def min_spacing_and_max_width_from_pitch(self, pitch: Decimal) -> Tuple[Decimal, Decimal]:
        """
        Derive the minimum spacing and maximally-sized wire for a
        desired pitch.

        Use this when the wire width is unknown, but you know the pitch.
        This calculation essentially plots the wire width on the X axis
        and the minimum pitch on the Y axis.

        You'll see discontinuites at the width-spacing table entries.
        If the desired pitch falls on a sloped line (i.e. > min width for
        entry N but less than min width for entry N+1), pick that spacing.
        If the desired pitch falls on a vertical line, pick the maximum width
        entry for N, which is the entry for N+1 minus delta (2 grid units),
        and then the spacing will be larger than the min spacing.

        :param pitch: Desired pitch
        :return: Tuple of (minimum spacing, maximally-sized wire)
        """
        pass

    def min_spacing_from_pitch(self, pitch: Decimal) -> Decimal:
        """
        Derive the minimum spacing for a maximally-sized wire given a
        desired pitch.
        See min_spacing_and_max_width_from_pitch for details.

        :param pitch: Desired pitch
        :return: Minimum spacing for said pitch.
        """
        pass

    def max_width_from_pitch(self, pitch: Decimal) -> Decimal:
        """
        Derive the maximum wire width for a maximally-sized wire given a
        desired pitch.
        See min_spacing_and_max_width_from_pitch for details.

        :param pitch: Desired pitch
        :return: Maximum wire width for said pitch.
        """
        pass

    def quantize_to_width_table(self, width: Decimal, layer: str, logger: Optional[HammerVLSILoggingContext]) -> Decimal:
        """
        Compare a desired width to the width table, if specified for a technology.
        Will return the allowable width smaller than or equal to the desired width,
        except if the desired width is greater than or equal to the last width in the width table.
        Issues a logger warning for the user if the returned width was quantized.
        """
        pass

    def get_width_spacing_start_twt(self, tracks: int, logger: Optional[HammerVLSILoggingContext]) -> Tuple[Decimal, Decimal, Decimal]:
        """
        This method will return the maximum width a wire can be in order
        to consume a given number of routing tracks.
        This assumes the neighbors of the wide wire are minimum-width routes.
        i.e. T W T
        T = thin / min-width
        W = wide
        See min_spacing_and_max_width_from_pitch for an explanation of the calculation.

        :param tracks: Number of routing tracks to consume
        :return: Returns tuple of (width, spacing, start)
        """
        pass

    def get_width_spacing_start_twwt(self, tracks: int, logger: Optional[HammerVLSILoggingContext], force_even: bool=False) -> Tuple[Decimal, Decimal, Decimal]:
        """
        This method will return the maximum width a wire can be in order
        to consume a given number of routing tracks.
        This assumes that the wires are in the following configuration.
        i.e. T W W T
        T = thin / min-width
        W = wide
        See min_spacing_and_max_width_from_pitch for an explanation of the calculation.

        :param tracks: Number of routing tracks to consume
        :param force_even: Forces the width of the wire to be an even multiple of the unit grid
        :return: Returns tuple of (width, spacing, start)
        """
        pass

class Stackup(BaseModel):
    """
    A stackup is a list of metals with a meaningful keyword name (for now).

    TODO: add vias, etc when we need them
    """
    grid_unit: Decimal
    name: str
    metals: List[Metal]

    @staticmethod
    def from_setting(grid_unit: Decimal, d: dict) -> 'Stackup':
        pass

    def get_metal(self, name: str) -> Metal:
        """
        Get a given metal layer by name.

        :param name: Name of the metal layer
        :return: A metal layer object
        """
        pass

    def get_metals_below_layer(self, name: str) -> List[Metal]:
        """
        Get all the metals below the specified metal layer.

        :param index: Index of the metal layer
        :return: A list of metal layer objects
        """
        pass

    def get_metals_incl_layer(self, name: str) -> List[Metal]:
        """
        Get all the metals including the specified metal layer.

        :param index: Index of the metal layer
        :return: A list of metal layer objects
        """
        pass

    def get_metal_by_index(self, index: int) -> Metal:
        """
        Get a given metal layer by index.
        If index is given as -1, return the highest metal layer (by index).

        :param index: Index of the metal layer
        :return: A metal layer object
        """
        pass
