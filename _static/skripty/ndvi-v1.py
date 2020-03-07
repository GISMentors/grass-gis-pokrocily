#!/usr/bin/env python

from grass.pygrass.modules import Module
from subprocess import PIPE

# vstup
vis="LC81920252013215LGN00_B4@landsat"
nir="LC81920252013215LGN00_B5@landsat"
# vysledek
ndvi="ndvi"
r_ndvi= "r_{}".format(ndvi)

# 0. nastavit vypocetni region
Module('g.region', raster=vis)

# 1. vypocet NDVI
print("VIS: {0} ; NIR: {1}".format(vis, nir))
Module('r.mapcalc',
       expression="{o} = float({n} - {v}) / ({n} + {v})".format(o=ndvi, v=vis, n=nir),
       overwrite=True)

# 2. reklasifikace (1,2,3)
print("Reklasifikuji...")
# r.reclass umi reklasifikovat pouze celociselne rastry, proto pouzime
# r.recode
recode = """
 -1:0.05:1 
 0.05:0.35:2 
 0.35:1:3
"""
Module('r.recode', input=ndvi, output=r_ndvi,
       rules='-', overwrite=True, stdin_=recode)

# 3. tabulka barev
colors = """
 1 red
 2 yellow
 3 0 136 26
"""
Module('r.colors', map=r_ndvi,
       rules='-', quiet=True, stdin_=colors)

# 4. vypsat vysledek
print("Generuji report...")
report = Module('r.stats', flags='pl', input=r_ndvi, separator=':', stdout_=PIPE)

print('-' * 80)
for trida, label, procento in map(
        lambda x: x.split(':'), report.outputs.stdout.splitlines()
):
    print ("Trida {0} ({1:28s}): {2:>7}".format(trida, label, procento))
print('-' * 80)
