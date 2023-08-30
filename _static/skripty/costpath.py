#!/usr/bin/env python

#%module
#% description: Nastroj pro vyhledani optimalni trasy.
#%end

#%option G_OPT_M_COORDS
#% key: start
#% description: Souradnice pocatecniho bodu
#% required: yes
#%end

#%option G_OPT_M_COORDS
#% key: end
#% description: Souradnice koncoveho bodu
#% required: yes
#%end

#%option G_OPT_V_OUTPUT
#%end

import grass.script as gscript
from grass.pygrass.modules import Module

def main():
    sx, sy = option['start'].split(',')
    sp='{}|{}|1'.format(sx, sy)
    ex, ey = option['end'].split(',')
    ep='{}|{}|1'.format(ex, ey)
    resolution = 25
    offset = 1e4

    Module('v.in.ascii',
           input='-',
           output='startp',
           stdin_=sp,
           overwrite=True)
    Module('v.in.ascii',
           input='-',
           output='endp',
           stdin_=ep,
           overwrite=True)
    
    Module('g.region',
           res=resolution,
           vector=['startp', 'endp'])
    Module('g.region',
           n='n+{}'.format(offset),
           s='s-{}'.format(offset),
           e='e+{}'.format(offset),
           w='w-{}'.format(offset))
    
    Module('r.cost',
           flags='k',
           input='rychlost_cas',
           output='rychlost_naklady',
           start_points='startp',
           overwrite=True)
    Module('r.drain',
           flags='n',
           input='rychlost_naklady',
           output=option['output'],
           start_points='endp')
    Module('r.to.vect',
           flags='s',
           input=option['output'],
           output=option['output'],
           type='line')

if __name__ == "__main__":
    option, flag = gscript.parser()
    main()
