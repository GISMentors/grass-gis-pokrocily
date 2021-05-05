#!/usr/bin/env python3

import os
import sys
import tempfile

from grass.pygrass.modules import Module

from pywps import Process, LiteralInput, ComplexOutput, LOGGER, Format

class ObcePsc(Process):
     def __init__(self):
          inputs = [
               LiteralInput(
                    identifier="psc",
                    title="Zájmové PSČ",
                    data_type="string"
               )
          ]
          outputs = [
               ComplexOutput(
                    identifier="output",
                    title="Vystupni GML soubor",
                    supported_formats=[Format('application/gml+xml')],
                    as_reference=True
               )
          ]

          super().__init__(
               self._handler,
               identifier="obce_psc",
               version="1.0",
               title="Dotaz na obce dle PSC",
               abstract="Testovaci sluzba PyWPS.",
               inputs=inputs,
               outputs=outputs,
               grass_location="gismentors",
               store_supported=True,
               status_supported=True)

          os.environ['GRASS_SKIP_MAPSET_OWNER_CHECK'] = '1'
          os.environ['HOME'] = tempfile.gettempdir() # needed by G_home()

     def obce_psc(self, psc):
          map_name = 'obce_psc_{}'.format(psc)
          
          Module('v.extract', input='obce', output='obce1',
                 where="psc = '{}'".format(psc))
          Module('v.select', ainput='obce', binput='obce1',
                 output=map_name,
                 operator='overlap', overwrite=True)

          return map_name
          
     def _handler(self, request, response):
          psc = request.inputs['psc'][0].data

          LOGGER.debug("Computation started")

          map_name = self.obce_psc(psc)
          LOGGER.debug("Computation finished")

          LOGGER.debug("Export started")
          os.chdir(self.workdir)
          Module('v.out.ogr',
                 input=map_name,
                 format='GML',
                 output='output.gml')
          
          response.outputs["output"].file = "output.gml"
          return response
