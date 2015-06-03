#!/usr/bin/env python

from grass.pygrass.raster import RasterRow
from grass.pygrass.vector import Vector
from grass.pygrass.gis.region import Region
from grass.pygrass.utils import coor2pixel
from grass.pygrass.modules import Module

rast = 'dmt@PERMANENT'

Module('g.region', raster=rast)

region = Region()

dmt = RasterRow(rast)
dmt.open('r')

obce = Vector('obce_bod')
obce.open('r')

for o in obce:
    x, y = coor2pixel(o.coords(), region)
    value = dmt[int(x)][int(y)]
    print (u'{:40}: {:.0f}'.format(o.attrs['nazev'], value))

obce.close()
dmt.close()
