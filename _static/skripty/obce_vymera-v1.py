#!/usr/bin/env python3

from grass.pygrass.modules import Module
from subprocess import PIPE

mesto='pardubice'
nazev='Pardubice'

# atributovy dotaz
Module('v.extract', input='obce@ruian', output=mesto,
       where="nazev='{}'".format(nazev), overwrite=True, quiet=True)
# vypocet vymery
cat, area = Module('v.to.db', map=mesto,
                   option='area', flags='p', columns='area',
                   quiet=True, stdout_=PIPE).outputs.stdout.split('|')
# vypsani vysledku
print("{0}: {1:.2f} ha".format(nazev, float(area) / 1e4))
# odstraneni vytvorene mapy
Module('g.remove', type='vector', name=mesto, flags='f', quiet=True)
