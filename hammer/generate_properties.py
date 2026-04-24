import argparse
import os
import re
import sys
from collections import namedtuple
from typing import Dict
InterfaceVar = namedtuple('InterfaceVar', 'name type desc')
Interface = namedtuple('Interface', 'module filename inputs outputs')

def isinstance_check(t: str) -> str:
    pass

def generate_from_list(template: str, lst) -> list:
    pass
file_cache = {}

def get_full_filename(filename: str) -> str:
    pass

def generate_interface(interface: Interface) -> None:
    pass

def main(args) -> int:
    pass
if __name__ == '__main__':
    sys.exit(main(sys.argv))
