#!/usr/bin/env python3

from grass.pygrass.vector import VectorTopo

okresy = VectorTopo('okresy', mapset='ruian')
okresy.open('r')

for o in okresy.viter('areas'):
    sousede = set()
    for b in o.boundaries():
        for n in b.read_area_ids():
            if n != -1 and n != o.id:
                sousede.add(n)
    
    print('{:20}: {}'.format(o.attrs['nazev'], len(sousede)))

okresy.close()
