#!/usr/bin/env python3

#%module
#% description: Creates reclassified NDVI based on given AOI.
#%end
#%option G_OPT_M_MAPSET
#% required: yes
#% answer: landsat
#%end
#%option G_OPT_V_MAP
#% key: aoi
#% answer: obce@ruian_praha
#%end
#%option G_OPT_F_INPUT
#% key: classes
#% required: no
#%end

import sys
from subprocess import PIPE

from grass.script import parser, fatal

from grass.pygrass.modules import Module
from grass.pygrass.gis import Mapset
from grass.pygrass.messages import Messenger

def main():
    mapset = options['mapset']
    aoi = options['aoi']
    if '@' in aoi:
        aoi_name = aoi.split('@')[0]
    else:
        aoi_name = aoi
    
    try:
        vis = Mapset(mapset).glist('raster', pattern='*B4')[0] + '@' + mapset
        nir = Mapset(mapset).glist('raster', pattern='*B5')[0] + '@' + mapset
    except IndexError:
        fatal("Nelze najit vstupni kanaly")
    ndvi = "ndvi_{}".format(aoi_name)
    r_ndvi= "r_ndvi_{}".format(aoi_name)

    msgr = Messenger()
    
    # 0. nastavit vypocetni region
    Module('g.region', align=vis, vector=aoi)
    
    # 1. vypocet NDVI
    msgr.message("VIS: {0} ; NIR: {1}".format(vis, nir))
    Module('r.mapcalc',
           expression="{o} = float({n} - {v}) / ({n} + {v})".format(o=ndvi, v=vis, n=nir),
           overwrite=True)
    
    # 2. reklasifikace (1,2,3)
    msgr.message("Reklasifikuji...")
    # r.reclass umi reklasifikovat pouze celociselne rastry, proto pouzime
    # r.recode
    if not options['classes']:
        recode = """
        -1:0.05:1 
        0.05:0.35:2 
        0.35:1:3
        """
        kwargs = {
            'rules' : '-',
            'stdin_' : recode
        }
    else:
        kwargs = {
            'rules' : options['classes']
        }
    Module('r.recode', input=ndvi, output=r_ndvi,
           overwrite=True, **kwargs)
    
    # 3. tabulka barev
    if options['classes']:
        colors = """
        1 red
        2 yellow
        3 0 136 26
        """
        Module('r.colors', map=r_ndvi,
               rules='-', quiet=True, stdin_=colors)
    
    # 4. vypsat vysledek
    msgr.message("Generuji report...")
    report = Module('r.stats', flags='pl', input=r_ndvi, separator=':', stdout_=PIPE)
    
    msgr.message('-' * 80)
    for line in report.outputs.stdout.splitlines():
        trida, popisek, procento = line.split(':')
        msgr.message("Trida {}: {}".format(trida, procento))
    msgr.message('-' * 80)
        
    return 0

if __name__ == "__main__":
    options, flags = parser()
    sys.exit(main())
