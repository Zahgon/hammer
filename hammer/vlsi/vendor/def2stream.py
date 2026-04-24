import pya
import re
import json
import copy
import sys
import os
errors = 0

def expand_cfg_layers(cfg):
    pass

def read_cfg():
    pass
rect_pat = re.compile('\n  \\s*\\-\\ LAYER\\ (?P<layer>\\S+)  # The layer name\n  (?:                           # Non-capturing group\n  \\s+\\+\\ MASK\\ (?P<mask>\\d+)    # Mask, None if absent\n  )?\n  (?P<opc>                      # OPC, None if absent\n  \\s+\\+\\ OPC\n  )?\n  \\s+RECT\\\n   \\(\\ (?P<xlo>\\d+)\\ (?P<ylo>\\d+)\\ \\)\\   # rect lower-left pt\n  \\(\\ (?P<xhi>\\d+)\\ (?P<yhi>\\d+)\\ \\)\\ ; # rect upper-right pt\n  ', re.VERBOSE)

def read_fills(top):
    pass
tech = pya.Technology()
tech.load(tech_file)
layoutOptions = tech.load_layout_options
if len(layer_map) > 0:
    layoutOptions.lefdef_config.map_file = layer_map
main_layout = pya.Layout()
print('[INFO] Reporting cells prior to loading DEF ...')
for i in main_layout.each_cell():
    print("[INFO] '{0}'".format(i.name))
print('[INFO] Reading DEF ...')
main_layout.read(in_def, layoutOptions)
top_cell_index = main_layout.cell(design_name).cell_index()
print('[INFO] Clearing cells...')
for i in main_layout.each_cell():
    if i.cell_index() != top_cell_index:
        if not i.name.startswith('VIA_'):
            i.clear()
cntr = 0
layout_cell_names = set()
print('[INFO] Merging GDS/OAS files...')
for fil in in_files.split():
    print('\t{0}'.format(fil))
    print('[INFO] Uniquefying duplicate cell names...')
    new_layout = pya.Layout()
    new_layout.read(fil)
    for i in new_layout.each_cell():
        if i.name in layout_cell_names:
            cntr += 1
            i.name = f'{i.name}_unique{cntr}'
        else:
            layout_cell_names.add(i.name)
    new_layout.write('tmp.gds')
    main_layout.read('tmp.gds')
print("[INFO] Copying toplevel cell '{0}'".format(design_name))
top_only_layout = pya.Layout()
top_only_layout.dbu = main_layout.dbu
top = top_only_layout.create_cell(design_name)
top.copy_tree(main_layout.cell(design_name))
read_fills(top)
print('[INFO] Checking for missing cell from GDS/OAS...')
missing_cell = False
regex = None
if 'GDS_ALLOW_EMPTY' in os.environ:
    print('[INFO] Found GDS_ALLOW_EMPTY variable.')
    regex = os.getenv('GDS_ALLOW_EMPTY')
for i in top_only_layout.each_cell():
    if i.is_empty():
        missing_cell = True
        if regex is not None and re.match(regex, i.name):
            print("[WARNING] LEF Cell '{0}' ignored. Matches GDS_ALLOW_EMPTY.".format(i.name))
        else:
            print("[ERROR] LEF Cell '{0}' has no matching GDS/OAS cell. Cell will be empty.".format(i.name))
            errors += 1
if not missing_cell:
    print('[INFO] All LEF cells have matching GDS/OAS cells')
print('[INFO] Checking for orphan cell in the final layout...')
orphan_cell = False
for i in top_only_layout.each_cell():
    if i.name != design_name and i.parent_cells() == 0:
        orphan_cell = True
        print("[ERROR] Found orphan cell '{0}'".format(i.name))
        errors += 1
if not orphan_cell:
    print('[INFO] No orphan cells')
if seal_file:
    top_cell = top_only_layout.top_cell()
    print('[INFO] Reading seal GDS/OAS file...')
    print('\t{0}'.format(seal_file))
    top_only_layout.read(seal_file)
    for cell in top_only_layout.top_cells():
        if cell != top_cell:
            print("[INFO] Merging '{0}' as child of '{1}'".format(cell.name, top_cell.name))
            top.insert(pya.CellInstArray(cell.cell_index(), pya.Trans()))
print('Removing zero-length paths...')
for cell in top_only_layout.each_cell():
    for layer_idx in top_only_layout.layer_indexes():
        for shape in cell.each_shape(layer_idx):
            if shape.is_path():
                path = shape.path
                paths = [(p.x, p.y) for p in path.each_point()]
                paths_unique = set(paths)
                if len(paths_unique) < len(paths):
                    polygon = path.polygon()
                    print(f'\tlayer_index: {layer_idx},', shape)
                    shape.delete()
print("[INFO] Writing out GDS/OAS '{0}'".format(out_file))
top_only_layout.write(out_file)
sys.exit(errors)
