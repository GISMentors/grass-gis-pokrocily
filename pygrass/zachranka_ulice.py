#!/usr/bin/env python

from grass.pygrass.vector import VectorTopo

zachranka = VectorTopo('adresnimista_zachranka', mapset='ruian_praha')
zachranka.open('r')
ulice = VectorTopo('ulice', mapset='ruian_praha')
ulice.open('r')

for z in zachranka:
    u = ulice.find['by_point'].geo(z, maxdist=1000.)
    print (u'{:10} {:1} {}'.format(z.attrs['kod'], z.attrs['ulicekod'] == u.attrs['kod'], u.attrs['nazev']))

zachranka.close()
ulice.close()
