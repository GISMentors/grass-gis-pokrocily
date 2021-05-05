#!/usr/bin/env python3

from grass.pygrass.vector import VectorTopo

psc = '41115'

obce = VectorTopo('obce')
obce.open('r')

vystup = VectorTopo('obce_psc_{}'.format(psc))
vystup.open('w', tab_cols=[('cat',       'INTEGER PRIMARY KEY'),
                           ('nazev',     'TEXT'),
                           ('psc',       'INTEGER')])

obec_id = None
obce_psc = set()
for prvek in obce.viter('areas'):
    if prvek.attrs is None or prvek.attrs['psc'] == psc:
        if obec_id is None:
            obec_id = prvek.id
            
        for b in prvek.boundaries():
            for n in b.get_left_right():
                if n != -1 and n != obec_id:
                    obce_psc.add(n)
obce_psc.add(obec_id)

hranice = list()
for prvek in obce.viter('areas'):
    if prvek.id not in obce_psc:
        continue

    for b in prvek.boundaries():
        if b.id not in hranice:
            hranice.append(b.id)
            vystup.write(b, attrs=(None, None))

    vystup.write(prvek.get_centroid(), attrs=(prvek.attrs['nazev'], prvek.attrs['psc']))

vystup.table.conn.commit()

vystup.close()
obce.close()
