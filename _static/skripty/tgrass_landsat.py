#!/usr/bin/env python

#%module
#% description: Create temporal dataset from Landsat data
#%end
#%option G_OPT_M_DIR
#% description: Name of directory with input Landsat files
#%end
#%option G_OPT_STRDS_OUTPUT
#%end

import os
import sys
import datetime
import grass.script as grass
from grass.exceptions import CalledModuleError

def import_data(directory):
    files = []
    for f in os.listdir(directory):
        if f.endswith(".tif"):
            files.append(f)

    count = len(files)
    i = 0
    for f in files:
        i += 1
        grass.message("Importing <{0}> ({1}/{2})...".format(f, i, count))
        grass.percent(i, count, 5)
        grass.run_command('r.in.gdal', input=os.path.join(directory, f),
                          output=os.path.splitext(f)[0], quiet=True, overwrite=True)
    grass.percent(0, 0, 0)
    
def mask_data():
    bands1 = grass.list_grouped('raster', pattern='lndcal*.1$')[mapset]
    count = len(bands1)
    i = 0
    for b1 in bands1:
        i += 1
        oname = b1.split('.')[1]
        grass.message("Processing <{0}> ({1}/{2})...".format(oname, i, count))
        grass.percent(i, count, 5)
        grass.run_command('g.region', raster=b1)
        mask = grass.find_file('fmask.' + oname, element='raster')['fullname']
        if mask:
            grass.run_command('r.mask', raster='fmask.' + oname, maskcats=1, overwrite=True, quiet=True)
        else:
            grass.warning("Mask missing for <{0}>".format(oname))
        bands = grass.list_grouped('raster', pattern='lndcal.{0}.*'.format(oname))[mapset]
        for b in bands:
            n = b.split('.')[-1]
            grass.mapcalc('{0}.{1}={2}'.format(oname, n, b), quiet=True, overwrite=True)
        if mask:
            grass.run_command('r.mask', flags='r', quiet=True)
        
    grass.run_command('g.remove', type='raster', pattern='fmask*,lndcal*', flags='f', quiet=True)
    grass.percent(0, 0, 0)
    
def timestamp_data():
    maps = grass.list_grouped('raster')[mapset]
    grass.message("Timestamping maps...")
    count = len(maps)
    i = 0
    for name in maps:
        i += 1
        grass.percent(i, count, 5)
        date = name.split('_')[-1].split('.')[0]
        grass_date = datetime.datetime.strptime(date, '%Y%m%d').strftime('%d %b %Y')
        grass.run_command('r.timestamp', map=name, date=grass_date)

    grass.percent(0, 0, 0)

def create_strds(output):
    grass.run_command('t.create', output=output, title=output, description=output)
    map_file = grass.tempfile()
    grass.run_command('g.list', type='raster', mapset='.', separator='newline', output=map_file, overwrite=True)
    grass.run_command('t.register', input=output, file=map_file, separator='newline', quiet=True, overwrite=True)

def check_strds(name):
    strds = grass.read_command('t.list', quiet=True).splitlines()
    if name + '@' + mapset not in strds:
        return
    
    if os.environ.get('GRASS_OVERWRITE', '0') == '1':
        grass.warning("Space time raster dataset <{}> is already exists "
                      "and will be overwritten.".format(name))
        grass.run_command('t.remove', inputs=name, quiet=True)
    else:
        grass.fatal("Space time raster dataset <{}> is already in the database. "
                    "Use the overwrite flag.".format(name))
    
def main():
    check_strds(opt['output'])
    import_data(opt['input'])
    mask_data()
    timestamp_data()
    create_strds(opt['output'])
    
if __name__ == "__main__":
    opt, flgs = grass.parser()
    mapset=grass.gisenv()['MAPSET']
    sys.exit(main())
