#!/usr/bin/env python

#%module
#% description: Vypocet NDVI
#%end
#%option G_OPT_R_INPUT
#% key: tm3
#% description: Treti kanal Landsat TM
#%end
#%option G_OPT_R_INPUT
#% key: tm4
#% description: Ctvrty kanal Landsat TM
#%end

import sys

from grass.pygrass.modules.shortcuts import general as g
from grass.pygrass.modules.shortcuts import raster as r

import grass.script as grass

def main():
    g.message("Pocitam NDVI...")

    # nastavit region
    g.region(rast=options['tm4'])
    
    # vypocitat NDVI
    r.mapcalc('ndvi = float({y} - {x}) / ({y} + {x})'.format(x=options['tm3'], y=options['tm4']), overwrite = True)
    
    # r.reclass podporuje pouze datovy typ CELL
    r.mapcalc('temp1 = 100 * ndvi', overwrite = True)
    g.message("Reklasifikuji data...")
    
    # reklasifikovat data
    reclass_rules = """-100 thru 5   = 1 bez vegetace, vodni plochy
5   thru 35  = 2 plochy s minimalni vegetaci
35  thru 100  = 3 plochy pokryte vegetaci"""
    r.reclass(overwrite = True, rules = '-',
              input = 'temp1', output = 'r_ndvi', stdin_ = reclass_rules)
    
# nastavit tabulku barev
    color_rules = """1 red
2 yellow
3 0 136 26"""
    r.colors(quiet = True,
             map = 'r_ndvi', rules = '-', stdin_ = color_rules)
    
    # vytiskout zakladni charakteristiku dat 
    r.report(map = 'r_ndvi', units = ['c', 'p', 'h'])

if __name__ == "__main__":
    options, flags = grass.parser()
    main()
