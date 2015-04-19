#!/usr/bin/env python

import numpy as np
from grass.pygrass.raster import RasterRow
from grass.pygrass.modules import Module

rast = 'dmt'

Module('g.region', raster=rast, res=100)

dmt = RasterRow(rast)
dmt.open('r')

min = max = None
count = ncount = 0
for row in dmt:
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

print ("min={:.2f} max={:.2f} count={} (no-data: {})".format(min, max, count, ncount))
