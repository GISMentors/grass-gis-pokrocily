#!/usr/bin/env python3

import numpy as np
from grass.pygrass.raster import RasterRow
from grass.pygrass.gis.region import Region

name = 'dmt100'

reg = Region()
reg.from_rast(name)
reg.set_current()

with RasterRow(name) as rast:
    array = np.array(rast)

print("min={:.2f} max={:.2f} count={} (no-data: {})".format(
      array.min(), array.max(), array.size,
      np.count_nonzero(np.isnan(array))))
