#!/usr/bin/env python

from grass.pygrass.vector import VectorTopo

psc = '41115'

obce = VectorTopo('obce')
obce.open('r')

print ("Seznam obci s PSC {}:".format(psc))
obce_psc = set()
for prvek in obce.viter('areas'):
    if prvek.attrs['psc'] != psc:
        continue
    obce_psc.add(prvek.id)
    print (u"{0}: {1}".format(psc, prvek.attrs['nazev']))
    
sousede = set()
for prvek in obce.viter('areas'):
    if prvek.id not in obce_psc:
        continue

    for b in prvek.boundaries():
        for n in b.get_left_right():
            if n != -1 and n != prvek.id:
               sousede.add(n)

print ("Seznam sousednich obce:")
for prvek in obce.viter('areas'):
    if prvek.id not in sousede or \
       prvek.attrs['psc'] == psc:
        continue
    
    print (u"{0}: {1}".format(prvek.attrs['psc'], prvek.attrs['nazev']))

obce.close()
