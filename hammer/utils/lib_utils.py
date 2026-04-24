import re
import os
import gzip
from decimal import Decimal
from typing import List, Optional, Tuple
__all__ = ['LIBUtils']

class LIBUtils:

    @staticmethod
    def get_time_unit(source: str) -> Optional[str]:
        """
        Get the time unit from the given LIB source file.
        """
        pass

    @staticmethod
    def get_cap_unit(source: str) -> Optional[str]:
        """
        Get the load capacitance unit from the given LIB source file.
        """
        pass

    @staticmethod
    def get_headers(source: str) -> List[str]:
        """
        Get the header lines with the major info
        """
        pass
