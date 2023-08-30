#!/usr/bin/env python

#%module
#% description: Creates temporal dataset from Landsat data.
#%end
#%option G_OPT_M_DIR
#% description: Name of directory with input Landsat files
#%end
#%option G_OPT_STRDS_OUTPUT
#%end
#%option
#% key: band_filter
#% description: Band filter name
#% answer: sr_band
#%end
#%option
#% key: cfmask_filter
#% description: Cfmask filter name
#% answer: cfmask_piemont
#%end
#%option
#% key: separator
#% description: File name separator
#% answer: _
#%end
#%option
#% key: cloud_mask_value
#% description: Cfmask cloud value
#% answer: 4
#% type: integer
#%end
#%option
#% key: nprocs
#% description: Number of processes
#% answer: 4
#% type: integer
#%end

import os
import sys
import datetime
import copy
import xml.etree.ElementTree as et
import grass.script as grass
from grass.exceptions import CalledModuleError
from grass.pygrass.modules import Module, ParallelModuleQueue

# import GeoTIFF bands and cfmask files into GRASS
def import_data(directory, file_filter):
    # collect files to be imported
    files = []
    for f in os.listdir(directory):
        if f.endswith(".tif") and [x for x in file_filter if x in f]:
            files.append(f)

    # import selected files into GRASS
    imodule = 'r.external'
    ###imodule = 'r.in.gdal'
    import_module = Module(imodule, quiet=True, overwrite=True, run_=False)
    i = 0
    count = len(files)
    for f in files:
        i += 1
        grass.message("Importing <{0}> ({1}/{2})...".format(f, i, count))
        grass.percent(i, count, 2)
        new_import = copy.deepcopy(import_module)
        map_name = os.path.splitext(f)[0]
        queue.put(new_import(input=os.path.join(directory, f), output=map_name))
    queue.wait()

    # set color table for cfmask map
    # 0 clear
    # 1 water
    # 2 shadow
    # 3 snow
    # 4 cloud
    colors = """0 black
1 blue
2 grey
3 white
4 149 186 224"""
    color_module = Module('r.colors', rules='-', quiet=True, stdin_=colors, run_=False)
    cfmask_maps = grass.list_grouped('raster', pattern='*cfmask*')[mapset]
    for map_name in cfmask_maps:
        new_color = copy.deepcopy(color_module)
        queue.put(new_color(map=map_name))
    queue.wait()

# apply cloud mask based on cfmask file
def mask_data(band_filter, cfmask_filter, cloud_mask_value, file_separator):
    # do cleanup first
    Module('g.remove', type='raster', pattern='*_masked', flags='f', quiet=True)
    
    # find band1 raster maps first
    bands1 = grass.list_grouped('raster', pattern='*{}1*'.format(band_filter))[mapset]

    mapcalc_module = Module('r.mapcalc', quiet=True, overwrite=True, run_=False)
    color_module = Module('r.colors', color='grey.eq', quiet=True, run_=False)
    
    i = 0
    count = len(bands1)
    for b1 in bands1:
        i += 1
        basename = b1.split(file_separator)[0]
        grass.message("Processing <{0}> ({1}/{2})...".format(basename, i, count))
        grass.percent(i, count, 5)
        
        # set computational region based on first band (ignore NULL values)
        Module('g.region', raster=b1, zoom=b1)
        maskname = '{}{}{}'.format(basename, file_separator, cfmask_filter)
        mask = grass.find_file(maskname, element='raster')['fullname']

        # apply cloud mask if found
        if mask:
            Module('r.mask', flags='i', raster=maskname, maskcats=cloud_mask_value, overwrite=True, quiet=True)
        else:
            grass.warning("Mask missing for <{}>".format(basename))

        # get list of bands
        bands = grass.list_grouped('raster', pattern='{}{}{}*'.format(basename, file_separator, band_filter))[mapset]
        
        # create copy of bands with mask applied (using r.mapcalc)
        for b in bands:
            new_mapcalc = copy.deepcopy(mapcalc_module)
            queue.put(new_mapcalc(expression='{name}_masked={name}'.format(name=b)))
        queue.wait()

        # set color table to grey.eq for masked bands
        masked_bands = grass.list_grouped('raster', pattern='*_masked')[mapset]
        for b in masked_bands:
            new_color = copy.deepcopy(color_module)
            queue.put(new_color(map=b))
        queue.wait()

        # remove mask if applied
        if mask:
            Module('r.mask', flags='r', quiet=True)
        
    # remove non-mask raster maps
    #Module('g.remove', type='raster', pattern='*{}*,*{}*'.format(band_filter, cfmask_filter), flags='f', quiet=True)

# get date & time from xml metadata files
def process_metadata(directory):
    file_datetime = {}
    for f in os.listdir(directory):
        if not f.endswith(".xml"):
            continue

        try:
            tree = et.parse(os.path.join(directory, f))
            metadata_node = tree.getroot().find('{http://espa.cr.usgs.gov/v2}global_metadata')
            date = metadata_node.find('{http://espa.cr.usgs.gov/v2}acquisition_date').text
            grass_date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d %b %Y')
            time = metadata_node.find('{http://espa.cr.usgs.gov/v2}scene_center_time').text
            grass_time = time.split('.', 1)[0]
            file_datetime[f.rstrip('.xml')] = '{} {}'.format(grass_date, grass_time)
        except StandardError as e:
            grass.warning("XML metadata ({}) parsing failed: {}".format(f, e))

    return file_datetime

# set timestamp for masked raster bands
def timestamp_data(directory, file_separator):
    # process metadata first
    file_datetime = process_metadata(directory)

    timestamp_module = Module('r.timestamp', run_=False)
        
    maps = grass.list_grouped('raster', pattern='*_masked')[mapset]
  
    grass.message("Timestamping masked maps...")
    for name in maps:
        basename = name.split(file_separator)[0]
        try:
            grass_date = file_datetime[basename]
        except KeyError:
            grass.warning("No timestamp available for <{}>".format(basename))
        new_timestamp = copy.deepcopy(timestamp_module)
        queue.put(new_timestamp(map=name, date=grass_date))
    queue.wait()
    
# create spatial-temporal dataset and register masked bands
def create_strds(output):
    Module('t.create', output=output, title=output, description=output)
    map_file = grass.tempfile()
    Module('g.list', type='raster', mapset='.', separator='newline', pattern="*band1*_masked", output=map_file, overwrite=True)
    Module('t.register', input=output, file=map_file, separator='newline', quiet=True, overwrite=True)

# check if output spatial-temporal dataset exists
def check_strds(name):
    strds = grass.read_command('t.list', quiet=True).splitlines()
    if name + '@' + mapset not in strds:
        return
    
    if os.environ.get('GRASS_OVERWRITE', '0') == '1':
        grass.warning("Space time raster dataset <{}> is already exists "
                      "and will be overwritten.".format(name))
        Module('t.remove', inputs=name, quiet=True)
    else:
        grass.fatal("Space time raster dataset <{}> is already in the database. "
                    "Use the overwrite flag.".format(name))
    
def main():
    check_strds(opt['output'])
    import_data(opt['input'], [opt['band_filter'], opt['cfmask_filter']])
    mask_data(opt['band_filter'], opt['cfmask_filter'], opt['cloud_mask_value'], opt['separator'])
    timestamp_data(opt['input'], opt['separator'])
    create_strds(opt['output'])
    
if __name__ == "__main__":
    opt, flgs = grass.parser()
    mapset=grass.gisenv()['MAPSET']

    # queue for parallel jobs
    queue = ParallelModuleQueue(int(opt['nprocs']))

    # do the job
    sys.exit(main())
