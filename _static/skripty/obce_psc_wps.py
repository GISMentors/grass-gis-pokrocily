#!/usr/bin/env python

import os
import logging
from zipfile import ZipFile

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
         
         self.psc = self.addLiteralInput(identifier = "psc",
                                         title = "Zájmové PSČ",
                                         type = types.StringType)
         
         self.output = self.addComplexOutput(identifier = "output",
                                             title = "Output zipped shapefile",
                                             formats = [ {"mimeType":"application/x-zipped-shp"} ],
                                             asReference = True)

    def export(self, map_name):
        self.output_file = '{}/{}.zip'.format(self.output_dir, map_name)
        
        logging.debug("Export started")          
        Module('v.out.ogr',
               input=map_name,
               output='{}/{}.shp'.format(self.output_dir, map_name),
               overwrite=True)
        
        os.chdir(self.output_dir)
        with ZipFile(self.output_file, 'w') as shpzip:
            shpzip.write('{}.dbf'.format(map_name))
            shpzip.write('{}.shp'.format(map_name))
            shpzip.write('{}.shx'.format(map_name))
            shpzip.write('{}.prj'.format(map_name))
            logging.debug("Export finished")
          
        self.output.setValue(self.output_file)

    def execute(self):
        map_name = self.run()
        self.export(map_name)

    def run(self):
        logging.debug("Computation started")
        
        value = self.psc.getValue()
        map_name = 'obce_psc_{}'.format(psc)
        
        obce = VectorTopo('obce@psc')
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
                    vystup.write(b, (None, None))

            vystup.write(prvek.get_centroid(), (prvek.attrs['nazev'], prvek.attrs['psc']))

        vystup.table.conn.commit()

        vystup.close()
        obce.close()

        logging.debug("Computation finished")
        
        return map_name

if __name__ == "__main__":
     process = Process()
     process.execute()
