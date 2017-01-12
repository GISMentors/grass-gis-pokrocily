#!/usr/bin/env python

#%module
#% description: Creates DMT from input XYZ data.
#%end
# overwrite: yes
#%option G_OPT_M_DIR
#% required: yes
#%end
#%option
#% key: pattern
#% type: string
#% description: File name pattern to filter files in input directory
#%end
#%option G_OPT_R_ELEV
#%end
#%option
#% key: nprocs
#% description: Number of processes
#% answer: 1
#% type: integer
#%end

import os
import sys
from copy import deepcopy

from grass.script.core import parser, message, fatal, overwrite

from grass.pygrass.modules import Module, ParallelModuleQueue
from grass.exceptions import CalledModuleError

def import_files(directory, pattern):
    maps = []
    if pattern:
        from glob import glob
        files = glob('{dir}{sep}{pat}'.format(
            dir=directory, sep=os.path.sep, pat=pattern)
        )
    else:
        files = map(lambda x: os.path.join(directory, x),
                    os.listdir(directory)
        )

    import_module = Module('v.in.ascii', separator='space', z=3, flags='tbz',
                           overwrite=overwrite(), quiet=True, run_=False)
    try:
        for f in files:
            basename = os.path.basename(f)
            mapname = os.path.splitext(basename)[0]
            maps.append(mapname)
            message("Importing <{}>...".format(f))
            import_task = deepcopy(import_module)
            queue.put(import_task(input=f, output=mapname))
        queue.wait()
    except CalledModuleError:
        return 1

    return maps

def main():
    import_files(options['input'], options['pattern'])
    
    return 0

if __name__ == "__main__":
    options, flags = parser()

    print overwrite()
    # queue for parallel jobs
    queue = ParallelModuleQueue(int(options['nprocs']))

    sys.exit(main())
