#!/usr/bin/env python3

from grass.pygrass.vector import VectorTopo

zachranka = VectorTopo('adresnimista_zachranka', mapset='ruian_praha')
zachranka.open('r')
ulice = VectorTopo('ulice', mapset='ruian_praha')
ulice.open('r')

zu = VectorTopo('zachranka_ulice')
cols = [('cat',       'INTEGER PRIMARY KEY'),
        ('kod',       'INTEGER'),
        ('ulice',     'TEXT'),
        ('nespravny', 'INTEGER')]
zu.open('w', tab_cols=cols)

seznam = []
for z in zachranka:
    u = ulice.find['by_point'].geo(z, maxdist=1000.)
    if u is None:
        continue
    nespravny = z.attrs['ulicekod'] != u.attrs['kod']
    print ('{:10} {:1} {}'.format(z.attrs['kod'], nespravny, u.attrs['nazev']))
    zu.write(z, (z.attrs['kod'], u.attrs['nazev'], nespravny))
    if u.cat not in seznam:
        zu.write(u, (None, u.attrs['nazev'], None))
        seznam.append(u.cat)

zu.table.conn.commit() # nutne pro zapis atributu !!!

zu.close()
zachranka.close()
ulice.close()
