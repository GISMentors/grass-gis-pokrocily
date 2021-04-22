#!/usr/bin/env python3

import numpy as np
from grass.pygrass.raster import RasterRow
from grass.pygrass.modules import Module

from grass.pygrass.gis.region import Region

name = 'dmt@PERMANENT'

reg = Region()
reg.from_rast(name)
reg.set_current()

rast = RasterRow(name)
rast.open('r')

min = max = None
count = ncount = 0
for row in rast:
    for value in row:
        if np.isnan(value):
            ncount += 1
        else:
            if min is None:
                min = max = value
            else:
                if min > value:
                    min = value
                elif max < value:
                    max = value
        count += 1

rast.close()

print("min={:.2f} max={:.2f} count={} (no-data: {})".format(
    min, max, count, ncount)
)
