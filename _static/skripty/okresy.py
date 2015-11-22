#!/usr/bin/env python

from grass.pygrass.vector import VectorTopo

okresy = VectorTopo('okresy_polygon', mapset='ruian')
okresy.open('r')

for o in okresy.viter('areas'):
    sousede = set()
    for b in o.boundaries():
        for n in b.get_left_right():
            if n != -1 and n != o.id:
                sousede.add(n)
    
    print (u'{:20}: {}'.format(o.attrs['nazev'], len(sousede)))

okresy.close()
