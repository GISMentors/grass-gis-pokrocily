#!/usr/bin/env python

from grass.pygrass.modules import Module

# pridat mapset do vyhledavaci cesty
Module('g.mapsets', mapset='landsat', operation='add', quiet=True)

# vstup
vis="LC81920252013215LGN00_B4"
nir="LC81920252013215LGN00_B5"
# vysledek
ndvi="ndvi"
r_ndvi= "r_{}".format(ndvi)

# vypocet NDIV
print ("VIS: {0} ; NIR: {1}".format(vis, nir))
Module('r.mapcalc',
       expression="$ndvi = float({nir} - {vis}) / ({nir} + {vis})".format(vis=vis, nir=nir),
       overwrite=True)

# reklasifikace (1,2,3)
print ("Reklasifikuji...")
# r.reclass umi reklasifikovat pouze celociselne rastry, proto pouzime
# r.recode
recode = """
 -1:0.05:1 
 0.05:0.35:2 
 0.35:1:3
"""
Module('r.recode', input=ndvi, output=r_ndvi,
       rules='-', overwrite=True, stdin_=recode)

# popisky
labels = """
1:bez vegetace, vodni plochy
2:plochy pokryte vegetaci
3:plochy pokryte vegetaci
"""
Module('r.category', map=r_ndvi,
       separator=':', rules='-', stdin_=labels)

# tabulka barev
colors = """
 1 red
 2 yellow
 3 0 136 26
"""
Module('r.colors', map=r_ndvi,
       rules='-', quiet=True, stdin_=colors)

# vypsat vysledek
print ("Generuji report...")
Module('r.report', map=r_ndvi,
       units='h')

print ("Hotovo!")
