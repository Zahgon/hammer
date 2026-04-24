import os
import sys
try:
    import yaml
except ImportError:
    try:
        sys.path.append('src/tools/pyyaml/lib3')
        import yaml
    except ImportError:
        if 'HAMMER_PYYAML_PATH' not in os.environ:
            print('pyyaml not found. Set $HAMMER_PYYAML_PATH to pyyaml/lib3', file=sys.stderr)
            sys.exit(1)
        else:
            sys.path.append(os.environ['HAMMER_PYYAML_PATH'])
            import yaml
import json

def convertArrays(o):
    """
    The YAML parser will take a list of substructures all named with an ints
    and create a python sub dict using those ints as keys. In JSON you can't
    have keys be anything other than strings even though that is valid in a
    python dict. This function recursively converts a python dict tree into
    one where any dicts where all the keys are ints are made into arrays. It
    makes sure the order is preserved.

    Adapted from https://raw.githubusercontent.com/vasil9v/yaml2json.py/c4cfa408bbab4f1a0cd3661d121237030f6bc0ca/yaml2json.py
    """
    pass

def compare(o1, o2):
    """
    Recursively compares each item in a python dict tree to make sure they are
    the same.

    Adapted from https://raw.githubusercontent.com/vasil9v/yaml2json.py/c4cfa408bbab4f1a0cd3661d121237030f6bc0ca/yaml2json.py
    """
    pass

def load_yaml(yamlStr: str) -> dict:
    """
    Load a YAML database as JSON.

    The input file is parsed as YAML and converted to a python dict tree, then
    that tree is converted to the JSON output. There is a check to make sure the
    two dict trees are structurally identical.

    :param yamlStr: A string containing the yaml database.
    :return: A dictionary object representing the yaml database.
    """
    pass
