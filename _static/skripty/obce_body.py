#!/usr/bin/env python3

from grass.pygrass.vector import Vector

obce = Vector('obce_bod', mapset='ruian')
obce.open('r')

for prvek in obce:
    print ("{:<25}: {:.0f} {:.0f}".format(prvek.attrs['nazev'], prvek.x, prvek.y))
    
obce.close()
