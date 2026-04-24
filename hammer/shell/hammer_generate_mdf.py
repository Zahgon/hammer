import argparse
from collections import namedtuple
import json
import re
import sys
MEM_REGEX = 'name ([^\\s]+) depth (\\d+) width (\\d+) ports ((?:[^\\s]+?\\s?(?!mask_gran))+)\\s?(?:mask_gran (\\d+))?'
Mem = namedtuple('Mem', 'name depth width ports mask_gran')

def parseLine(line):
    """
    Parse a line using the given regex above or return None.
    """
    pass

def memToJSON(mem):
    pass

def run(args):
    pass

def main():
    pass
