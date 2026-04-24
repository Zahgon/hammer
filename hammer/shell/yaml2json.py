"""
Convert YAML file to JSON with identical structure (as a python dict)
Adapted from https://raw.githubusercontent.com/vasil9v/yaml2json.py/c4cfa408bbab4f1a0cd3661d121237030f6bc0ca/yaml2json.py
"""
import sys
import yaml
import json
from hammer.config.yaml2json import convertArrays, compare

def load(f):
    pass

def save(f, b):
    pass

def yaml2json():
    """
    Main function, first arg is the input file, optional second one is the output
    file. If no output file is specified then the output is written to stdout.
    The input file is parsed as YAML and converted to a python dict tree, then
    that tree is converted to the JSON output. There is a check to make sure the
    two dict trees are structurally identical.
    """
    pass

def main():
    pass
