import re
__all__ = ['VerilogUtils']

class VerilogUtils:

    @staticmethod
    def remove_comments(v: str) -> str:
        """
        Remove comments from the given Verilog file.

        :param v: Verilog source code
        :return: Source code without comments
        """
        pass

    @staticmethod
    def contains_module(v: str, module: str) -> bool:
        """
        Check if the given Verilog source contains the given module.

        :param v: Verilog source code
        :param module: Module to look for
        :return: True if the given module exists.
        """
        pass

    @staticmethod
    def remove_module(v: str, module: str) -> str:
        """
        Remove the given module from the given Verilog source file, if it exists.

        :param v: Verilog source code
        :param module: Module to remove
        :return: Verilog with given module definition removed, if it exists
        """
        pass
