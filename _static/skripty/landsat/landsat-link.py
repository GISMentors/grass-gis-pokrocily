#!/usr/bin/env python

#%module
#% description: Links Landsat data and prepare cloud masks.
#%end
#%option G_OPT_M_DIR
#% description: Name of directory with input Landsat files
#%end
#%option 
#% key: nprocs
#% description: Number of processes
#% answer: 1
#%end

import os
import sys
import datetime
import copy
import grass.script as grass
from grass.pygrass.modules import Module, ParallelModuleQueue

def link_data(directory):
    link_module = Module('r.external', overwrite=True, quiet=True, run_=False)

    count = 0
    grass.message("Linking data...")
    for f in os.listdir(directory):
        if f.startswith('LT') and (f.endswith('.tif') or f.endswith('.TIF')):
            new_link = copy.deepcopy(link_module)
            queue.put(new_link(input=os.path.join(directory, f),
                               output=os.path.splitext(f)[0]))
            count += 1
    queue.wait()
    grass.message("...{} files linked".format(count))

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

def timestamp_data(directory, maps=None):
    mtl = process_mtl(directory)

    if maps is None:
        maps = grass.list_grouped('raster', pattern='*LT5*')[mapset]
    grass.message("Timestamping maps ({} maps)...".format(len(maps)))
    for name in maps:
        basename = name[name.find('LT'):].split('_')[0]
        starttime = datetime.datetime.strptime(mtl[basename]['date'], '%Y-%m-%d %H:%M:%S')
        endtime = starttime + datetime.timedelta(seconds=1)
        Module('r.timestamp', map=name, date='{start}/{end}'.format(start = starttime.strftime('%d %b %Y %H:%M:%S'),
                                                                    end = endtime.strftime('%d %b %Y %H:%M:%S')))

def main():
    link_data(opt['input'])
    timestamp_data(opt['input'])
        
if __name__ == "__main__":
    opt, flgs = grass.parser()
    mapset=grass.gisenv()['MAPSET']

    # queue for parallel jobs
    queue = ParallelModuleQueue(int(opt['nprocs']))

    sys.exit(main())
