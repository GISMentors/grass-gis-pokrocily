#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import types
from zipfile import ZipFile

gisbase = os.environ['GISBASE'] = "/usr/local/grass70"
os.environ['LD_LIBRARY_PATH'] = "/usr/local/grass70/lib"
sys.path.insert(0, os.path.join(os.environ["GISBASE"], "etc", "python"))

from grass.pygrass.modules import Module
from grass.pygrass.vector import VectorTopo

from pywps.Process import WPSProcess

class Process(WPSProcess):
     def __init__(self):
          WPSProcess.__init__(self,
                              identifier='obce_psc',
                              version="1.0",
                              title="Dotaz na obce podle PSČ",
                              abstract="Testovací služba školení GISMentors.",
                              grassLocation='gismentors',
                              storeSupported=True,
                              statusSupported=True)
          
          self.input_psc = self.addLiteralInput(identifier = "psc",
                                                title = "Zájmové PSČ",
                                                type = types.StringType)
         
          self.output = self.addComplexOutput(identifier = "output",
                                              title = "Output zipped shapefile",
                                              formats = [ {"mimeType":"application/x-zipped-shp"} ],
                                              asReference = True)

     def export(self, map_name):
          output_dir = os.path.join('/tmp', '{}_{}'.format(map_name, os.getpid()))
          os.mkdir(output_dir)
          
          output_file = '{}/{}.zip'.format(output_dir, map_name)
          
          logging.debug("Export started")          
          Module('v.out.ogr',
                 input=map_name,
                 output='{}/{}.shp'.format(output_dir, map_name),
                 overwrite=True)
          
          os.chdir(output_dir)
          with ZipFile(output_file, 'w') as shpzip:
               shpzip.write('{}.dbf'.format(map_name))
               shpzip.write('{}.shp'.format(map_name))
               shpzip.write('{}.shx'.format(map_name))
               shpzip.write('{}.prj'.format(map_name))
               logging.debug("Export finished")
          
          self.output.setValue(output_file)

     def execute(self):
          map_name = self.run()
          
          self.export(map_name)

     def run(self):
          logging.debug("Computation started")

          psc = self.input_psc.getValue()
          map_name = 'obce_psc_{}'.format(psc)

          obce = VectorTopo('obce', mapset='psc')
          obce.open('r')

          vystup = VectorTopo(map_name)
          vystup.open('w', tab_cols=[('cat',       'INTEGER PRIMARY KEY'),
                                     ('nazev',     'TEXT'),
                                     ('psc',       'INTEGER')])

          obec_id = None
          obce_psc = set()
          for prvek in obce.viter('areas'):
              if prvek.attrs['psc'] == psc:
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

          logging.debug("Computation finished")

          return map_name

if __name__ == "__main__":
     process = Process()
     process.execute()
