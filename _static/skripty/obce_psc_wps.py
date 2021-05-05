#!/usr/bin/env python3

import os
import sys
import tempfile

from grass.pygrass.modules import Module
from grass.pygrass.vector import VectorTopo

from pywps import Process, LiteralInput, ComplexOutput, LOGGER, Format

class ObcePsc(Process):
     def __init__(self):
          inputs = [
               LiteralInput(
               identifier = "psc",
                    title = "Zájmové PSČ",
                    data_type="string"
               )
          ]
          outputs = [
               ComplexOutput(
                    title = "Output GML file",
                    supported_formats=[Format('application/gml+xml')]
                    as_reference=True
               )
          ]

          super().__init__(
               self._handler,
               identifier="obce_psc",
               version="1.0",
               title="Dotaz na obce podle PSČ",
               abstract="Testovací služba PyWPS.",
               inputs=inputs,
               outputs=outputs,
               grass_location="gismentors",
               store_supported=True,
               status_supported=True)

          os.environ['GRASS_SKIP_MAPSET_OWNER_CHECK'] = '1'
          os.environ['HOME'] = tempfile.gettempdir() # needed by G_home()

     def obce_psc(psc):
          obce = VectorTopo('obce')
          obce.open('r')

          vystup = VectorTopo('obce_psc_{}'.format(psc))
          vystup.open('w', tab_cols=[('cat',       'INTEGER PRIMARY KEY'),
                                     ('nazev',     'TEXT'),
                                     ('psc',       'INTEGER')])

          obec_id = None
          obce_psc = set()
          for prvek in obce.viter('areas'):
              if prvek.attrs is None:
                  continue
              if prvek.attrs['psc'] == psc:
                  if obec_id is None:
                      obec_id = prvek.id

                  for b in prvek.boundaries():
                      for n in b.read_area_ids():
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

              vystup.write(prvek.centroid(), attrs=(prvek.attrs['nazev'], prvek.attrs['psc']))

          vystup.table.conn.commit()

          vystup.close()
          obce.close()

     def _handler(self, request, response):
          psc = request.inputs['psc'][0].data

          LOGGER.debug("Computation started")
          map_name = 'obce_psc_{}'.format(psc)
          obce_psc(psc)
          LOGGER.debug("Computation finished")

          LOGGER.debug("Export started")
          os.chdir(self.workdir)
          Module('v.out.ogr',
                 input=map_name,
                 format='GML',
                 output='output.gml')
          
          response.outputs["output"].file = "output.gml"
          return response
