#!/usr/bin/env python3

from grass.pygrass.raster import RasterRow
from grass.pygrass.vector import Vector
from grass.pygrass.gis.region import Region
from grass.pygrass.utils import coor2pixel

name = 'dmt@PERMANENT'

reg = Region()
reg.from_rast(name)
reg.set_current()

dmt = RasterRow(name)
dmt.open('r')

obce = Vector('obce_bod')
obce.open('r')

for o in obce:
    x, y = coor2pixel(o.coords(), region)
    value = dmt[int(x)][int(y)]
    print ('{:40}: {:.0f}'.format(o.attrs['nazev'], value))

obce.close()
dmt.close()
