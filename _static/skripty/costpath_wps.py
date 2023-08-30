#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import types
import logging
from zipfile import ZipFile
from subprocess import PIPE

gisbase = os.environ['GISBASE'] = "/usr/lib/grass72"
os.environ['LD_LIBRARY_PATH'] = "/usr/lib/grass72/lib"
sys.path.insert(0, os.path.join(os.environ["GISBASE"], "etc", "python"))

import grass.script as grass
from grass.pygrass.modules import Module

from pywps.Process import WPSProcess

class Process(WPSProcess):
    def __init__(self):

          WPSProcess.__init__(self,
                              identifier='costpath',
                              version="1.0",
                              title="Nalezeni optimalni trasy cesty",
                              abstract="Viz. http://training.gismentors.eu/grass-gis-zacatecnik/rastrova_data/analyza-nakladu.html",
                              grassLocation='gismentors_pywps',
                              storeSupported=True,
                              statusSupported=True)

          self.start = self.addLiteralInput(identifier = "start",
                                            title = "Souradnice pocatku (X,Y)",
                                            type = types.StringType)

          self.end = self.addLiteralInput(identifier = "end",
                                          title = "Souradnice konce (X,Y)",
                                          type = types.StringType)

          self.output = self.addComplexOutput(identifier = "output",
                                              title = "Vysledna cesta ve formatu ESRI Shapefile",
                                              formats = [ {"mimeType":"application/x-zipped-shp"} ],
                                              asReference = True)

          self.output_file = None # to be defined by descendant
          self.output_dir = None
          
          os.environ['GRASS_SKIP_MAPSET_OWNER_CHECK'] = '1'
          os.environ['HOME'] = '/tmp' # needed by G_home()
          
    def __del__(self):
        if self.output_dir:
            shutil.rmtree(self.output_dir)

    def execute(self):
        sx, sy = self.start.getValue().split(',')
        sp='{}|{}|1'.format(sx, sy)
        ex, ey = self.end.getValue().split(',')
        ep='{}|{}|1'.format(ex, ey)
        map_name = 'cesta'
        resolution = 25
        offset = 1e4
        
        logging.debug("Computation started")          

        Module('v.in.ascii',
               input='-',
               output='startp',
               stdin_=sp)
        Module('v.in.ascii',
               input='-',
               output='endp',
               stdin_=ep)

        Module('g.region',
               res=resolution,
               vector=['startp', 'endp'])
        Module('g.region',
               n='n+{}'.format(offset),
               s='s-{}'.format(offset),
               e='e+{}'.format(offset),
               w='w-{}'.format(offset))

        Module('r.cost',
               flags='k',
               input='rychlost_cas@cost_path_wps',
               output='rychlost_naklady',
               start_points='startp')
        Module('r.drain',
               flags='n',
               input='rychlost_naklady',
               output='cesta',
               start_points='endp')
        Module('r.to.vect',
               flags='s',
               input='cesta',
               output=map_name,
               type='line')

        logging.debug("Computation finished")          

        self.export(map_name)

    def export(self, map_name):
        self.output_dir = os.path.join('/tmp', '{}_{}'.format(map_name, os.getpid()))
        os.mkdir(self.output_dir)
        self.output_file = '{}/{}.zip'.format(self.output_dir, map_name)
          
        logging.debug("Export started")          
        Module('v.out.ogr',
               input=map_name,
               flags='sm',
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
