#!/usr/bin/env python3

from grass.pygrass.modules import Module

rast='dmt'

# set computational region
Module('g.region', raster=rast)

# compute & print statistics
Module('r.univar', map=rast)
