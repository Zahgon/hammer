import re
from decimal import Decimal
from typing import List, Optional, Tuple
__all__ = ['LEFUtils']

class LEFUtils:

    @staticmethod
    def get_sizes(source: str) -> List[Tuple[str, Decimal, Decimal]]:
        """
        Get the sizes of all macros in the given LEF source file.

        :param source: LEF file source, Unix line endings
        :return: List of all macros' sizes in the form of (macro name, width, height).
        """
        pass
