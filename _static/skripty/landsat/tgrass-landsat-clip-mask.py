#!/usr/bin/env python

#%module
#% description: Creates temporal dataset from Landsat data for current region.
#%end
#%option G_OPT_M_DIR
#% description: Name of directory with input Landsat files
#% answer: /mnt/repository/landsat/data
#%end
#%option G_OPT_STRDS_OUTPUT
#%end
#%option 
#% key: cloud_cover
#% description: Cloud cover (%)
#% answer: 5
#%end
#%option 
#% key: nprocs
#% description: Number of processes
#% answer: 1
#%end

import os
import sys
import copy
import datetime
from subprocess import PIPE

import grass.script as grass
from grass.pygrass.modules import Module, ParallelModuleQueue

def filter_data(cloud_cover=5):
    # filter scenes based on cloud cover
    maps = grass.list_grouped('raster', pattern='*_MTLFmask')['PERMANENT']
    filtered = []
    grass.message("Filtering...")
    for name in maps:
        stats = Module('r.stats', input=name, flags='pN', quiet=True, stdout_=PIPE, separator=':')
        for line in stats.outputs.stdout.splitlines():
            k, v = line.split(':')
            if k == '4':
                v = float(v.rstrip('%'))
                if v <= cloud_cover:
                    filtered.append(name.rstrip('_MTLFmask'))
    
    grass.message("{} from {} scenes selected".format(len(filtered), len(maps)))

    return filtered
    
def clip_mask_data(maps):
    mapcalc_module = Module('r.mapcalc', overwrite=True, quiet=True, run_=False)
    colors_module = Module('r.colors', color='grey', quiet=True, run_=False)

    grass.message("Clipping/Masking ({} maps)...".format(len(maps)))
    for name in maps:
        grass.message('Clipping {}...'.format(name))
        band1 = '{}_B1'.format(name)
        Module('g.copy', raster=['{}_MTLFmask'.format(name),'{}_MTLFmask'.format(name)], quiet=True)
        Module('r.mask', flags='i', raster='{}_MTLFmask'.format(name), maskcats="2 4", quiet=True)
        bands = grass.list_grouped('raster', pattern='{}_B*'.format(name))['PERMANENT']
        for band in bands:
            new_mapcalc = copy.deepcopy(mapcalc_module)
            queue.put(new_mapcalc(expression='clip_{name}={name}'.format(name=band)))
        queue.wait()
        Module('r.mask', flags='r', quiet=True)
        Module('g.remove', quiet=True, flags='f', type='raster', name='{}_MTLFmask'.format(name))

    grass.message("Setting up color table ({} maps)...".format(len(maps)))
    bands = grass.list_grouped('raster', pattern='clip_*')[mapset]
    for name in bands:
        new_colors = copy.deepcopy(colors_module)
        queue.put(new_colors(map=name))
    queue.wait()

    return bands

def process_mtl(directory):
    mtl = {}
    for fname in os.listdir(directory):
        if 'MTL' not in fname:
            continue
        with open(os.path.join(directory, fname)) as f:
            fbase = fname.rstrip('_MTL.txt')
            mtl[fbase] = {}
            for line in f.readlines():
                if 'DATE_ACQUIRED' in line:
                    mtl[fbase]['date'] = line.split('=', 1)[1].strip()
                if 'SCENE_CENTER_TIME' in line:
                    mtl[fbase]['date'] += ' ' + line.replace('"', '').split('=', 1)[1].strip().split('.')[0]
                if 'CLOUD_COVER' in line:
                    mtl[fbase]['cloud'] = float(line.split('=', 1)[1].strip())
    return mtl

def create_strds(directory, output, bands):
    def map_timestamps(directory, bands):
        tmpfile = grass.tempfile()
        mtl = process_mtl(directory)
        with open(tmpfile, 'w') as f:
            for band in bands:
                basename = band[band.find('LT'):].split('_')[0]
                starttime = datetime.datetime.strptime(mtl[basename]['date'], '%Y-%m-%d %H:%M:%S')
                endtime = starttime + datetime.timedelta(seconds=1)
                f.write('{}|{}|{}{}'.format(band, starttime, endtime, os.linesep))
        return tmpfile

    grass.message("Creating spatial-temporal dataset...")

    Module('t.create', output=output, title=output, description=output)
    map_file = map_timestamps(directory, bands)
    Module('t.register', input=output, file=map_file, quiet=True, overwrite=True)

def check_strds(name):
    strds = grass.read_command('t.list', quiet=True).splitlines()
    if name + '@' + mapset not in strds:
        return
    
    if os.environ.get('GRASS_OVERWRITE', '0') == '1':
        grass.warning("Space time raster dataset <{}> is already exists "
                      "and will be overwritten.".format(name))
        Module('t.remove', inputs=name, quiet=True)
    else:
        grass.fatal("Space time raster dataset <{}> is already in the database. "
                    "Use the overwrite flag.".format(name))
    
def main():
    check_strds(opt['output'])
    maps = filter_data(int(opt['cloud_cover']))
    bands = clip_mask_data(maps)
    create_strds(opt['input'], opt['output'], bands)
    
if __name__ == "__main__":
    opt, flgs = grass.parser()
    mapset=grass.gisenv()['MAPSET']

    # queue for parallel jobs
    queue = ParallelModuleQueue(8)

    sys.exit(main())
