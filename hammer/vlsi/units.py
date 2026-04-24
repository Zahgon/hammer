from abc import abstractmethod
import sys
from abc import ABC
from typing import Optional, TypeVar
from hammer.utils import get_or_else
_TT = TypeVar('_TT', bound='ValueWithUnit')

class ValueWithUnit(ABC):
    """Represents some particular value that has units (e.g. "10 ns", "2000 um", "25 C", etc).
    """
    _prefix_table = {'y': 1e-24, 'z': 1e-21, 'a': 1e-18, 'f': 1e-15, 'p': 1e-12, 'n': 1e-09, 'u': 1e-06, 'm': 0.001, 'c': 0.01, 'd': 0.1, '': 1, 'k': 1000.0, 'M': 1000000.0, 'G': 1000000000.0, 'T': 1000000000000.0, 'P': 1000000000000000.0, 'E': 1e+18, 'Z': 1e+21, 'Y': 1e+24}

    @property
    @abstractmethod
    def unit(self) -> str:
        """Get the base unit for values (e.g. "s", "m", "V", etc).
        Meant to be overridden by subclasses."""

    @property
    @abstractmethod
    def unit_type(self) -> str:
        """Get the base unit type for values. (e.g. for "s", this would be "time")
        Meant to be overridden by subclasses."""

    @property
    @abstractmethod
    def default_prefix(self) -> str:
        """Get the default prefix for values.
        (e.g. for time, specifying "n" would mean "0.25" would be interpreted as "0.25 ns".)
        Meant to be overridden by subclasses."""

    def __init__(self, value: str, prefix: Optional[str]=None) -> None:
        """
        Create a value from parsing the given string.
        :param value: Value encoded in the given string.
        :param prefix: If value does not have a prefix (e.g. "0.25"), then use
                       the given prefix, or the default prefix defined by the
                       class if one is not specified.
        """
        import re
        default_prefix = get_or_else(prefix, self.default_prefix)
        regex = '^(-?[\\d.]+) *(.*){}$'.format(re.escape(self.unit))
        match = re.search(regex, value)
        if match is None:
            try:
                num = str(float(value))
                self._value_prefix = default_prefix
            except ValueError:
                raise ValueError('Malformed {type} value {value}'.format(type=self.unit_type, value=value))
        else:
            num = match.group(1)
            self._value_prefix = match.group(2)
        if num.count('.') > 1 or len(self._value_prefix) > 1:
            raise ValueError('Malformed {type} value {value}'.format(type=self.unit_type, value=value))
        if self._value_prefix not in self._prefix_table:
            raise ValueError('Bad prefix for {value}'.format(value=value))
        self._value = float(num)
        self._prefix = self._prefix_table[self._value_prefix]

    @property
    def value_prefix(self) -> str:
        """Get the prefix string of this value."""
        pass

    @property
    def value(self) -> float:
        """Get the actual value of this value. (e.g. 10 ns -> 1e-9)"""
        pass

    def value_in_units(self, prefix: str, round_zeroes: bool=True) -> float:
        """Get this value in the given prefix. e.g. "ns", "mV", etc.
        """
        pass

    def str_value_in_units(self, prefix: str, round_zeroes: bool=True) -> str:
        """Get this value in the given prefix but including the units.
        e.g. return "5 ns".

        :param prefix: Prefix for the resulting value - e.g. "ns".
        :param round_zeroes: True to round 1.00000001 etc to 1 within 3 decimal places.
        """
        pass

    def eq(self: _TT, other: _TT) -> bool:
        """
        Compare equality of this value with another.
        The types must match.
        """
        pass

    def __eq__(self: _TT, other: object) -> bool:
        """
        Compare equality of this value with another.
        The types must match.
        """
        return self.eq(other)

    def ne(self: _TT, other: _TT) -> bool:
        """
        Compare inequality of this value with another.
        The types must match.
        """
        pass

    def __ne__(self: _TT, other: object) -> bool:
        """
        Compare inequality of this value with another.
        The types must match.
        """
        return self.ne(other)

    def __lt__(self: _TT, other: _TT) -> bool:
        """
        Check if self is less than other.
        The types must match.
        """
        if type(self) != type(other):
            raise TypeError('Types do not match')
        return self.value < other.value

    def __le__(self: _TT, other: _TT) -> bool:
        """
        Check if self is less than or equal to other.
        The types must match.
        """
        if type(self) != type(other):
            raise TypeError('Types do not match')
        return self.value <= other.value

    def __gt__(self: _TT, other: _TT) -> bool:
        """
        Check if self is greater than other.
        The types must match.
        """
        if type(self) != type(other):
            raise TypeError('Types do not match')
        return self.value > other.value

    def __ge__(self: _TT, other: _TT) -> bool:
        """
        Check if self is greater than or equal to other.
        The types must match.
        """
        if type(self) != type(other):
            raise TypeError('Types do not match')
        return self.value >= other.value

    def __add__(self: _TT, other: _TT) -> _TT:
        """
        Add other and self.
        The types must match.
        """
        if type(self) != type(other):
            raise TypeError('Types do not match')
        return type(self)(str(self.value + other.value), '')

    def __sub__(self: _TT, other: _TT) -> _TT:
        """
        Subtract other from self.
        The types must match.
        """
        if type(self) != type(other):
            raise TypeError('Types do not match')
        return type(self)(str(self.value - other.value), '')

    def __div__(self: _TT, other: float) -> _TT:
        """
        Divide self by a float or an integer.
        """
        raise NotImplementedError()

    def __truediv__(self: _TT, other: float) -> _TT:
        return type(self)(str(self.value / other), '')

    def __mul__(self: _TT, other: float) -> _TT:
        """
        Multiply self by a float or an integer.
        """
        return type(self)(str(self.value * other), '')

class TimeValue(ValueWithUnit):
    """Time value - e.g. "4 ns".
    Parses time values from strings.
    """

    @property
    def default_prefix(self) -> str:
        """Default prefix: ns"""
        pass

    @property
    def unit(self) -> str:
        pass

    @property
    def unit_type(self) -> str:
        pass

class VoltageValue(ValueWithUnit):
    """Voltage value - e.g. "0.95 V", "950 mV".
    """

    @property
    def default_prefix(self) -> str:
        """Default is plain volts (e.g. "0.1" -> 0.1 V)."""
        pass

    @property
    def unit(self) -> str:
        pass

    @property
    def unit_type(self) -> str:
        pass

class TemperatureValue(ValueWithUnit):
    """Temperature value in Celsius - e.g. "25 C", "125 C".
    Mainly used for specifying corners for MMMC.
    """

    @property
    def default_prefix(self) -> str:
        """Default is plain degrees Celsius (e.g. "25" -> "25 C")."""
        pass

    @property
    def unit(self) -> str:
        pass

    @property
    def unit_type(self) -> str:
        pass

class CapacitanceValue(ValueWithUnit):
    """Capacitance value - e.g. "5 fF", "10 nF".
    """

    @property
    def default_prefix(self) -> str:
        """Default prefix: fF"""
        pass

    @property
    def unit(self) -> str:
        pass

    @property
    def unit_type(self) -> str:
        pass
