Landsat
=======

V této části si ukážeme především proces importu reálných dat do
systému GRASS, vytvoření časových značek a na jejich základě vytvoření
časoprostorového datasetu.

Jako vstupní data máme sadu snímků Landsat ve formátu TIFF. Ke každému
snímku je k dispozici maska, která definuje validního hodnoty. Maska obsahuje
hodnoty 1 a 2, přičemž hodnota 2 představuje oblačnost. Např.

.. code-block:: bash
                
   gdalinfo lndcal.LT51920262011306KIS00_20111102.tif -mm
   gdalinfo fmask.LT51920262011306KIS00_20111102.tif -noct -mm

Viz `Landsat Surface Reflectance Quality Assessment <http://landsat.usgs.gov/landsat_climate_data_records_quality_calibration.php>`__.

.. tip:: Existují užitečné utility, které usnadňují automatizované
         stažení dat Landsat. Patří mezi ně např. `landsat-util
         <https://pythonhosted.org/landsat-util/overview.html>`__,
         `gsutil
         <http://krstn.eu/landsat-batch-download-from-google/>`__ nebo
         `Landsat-Download
         <https://olivierhagolle.github.io/LANDSAT-Download/>`__.
         
Import vstupních dat
--------------------

V prvním kroku na základě vstupních dat vytvoříme novou lokaci:

.. code-block:: bash
                
   grass70 -c lndcal.LT51920262011306KIS00_20111102.tif /opt/grassdata/landsat

Před importem můžeme zkontrolovat souřadnicový systém lokace:

.. code-block:: bash

   g.proj -p

Pro dávkový import a vytvoření časoprostorového datasetu si napíšeme
jednoduchý skript v jazyku Python, který provede následující kroky:

#. naimportuje data včetně masek :lcode:`18`
#. aplikuje masky nad originalními daty :lcode:`34`
#. nastaví časovou značku (datum je uvedeno jako součást názvu
   souboru) :lcode:`59`
#. maskované rastry zaregistruje do výstupního časoprostorového
   datasetu :lcode:`73`

.. literalinclude:: ../_static/skripty/tgrass_landsat.py
   :language: python
   :linenos:
   :emphasize-lines: 18, 34, 59, 73
                
Skript je ke stažení `zde
<../_static/skripty/tgrass_landsat.py>`_. Příklad spuštění:

.. code-block:: bash

   grass_landsat.py input=~/geodata/sub101 out=landsat
      
Ve výsledném datasetu máme zaregistrována data od roku 1984 do 2014:

.. code-block:: bash

   t.info landsat

   ...
   | Start time:................. 1984-06-25 00:00:00
   | End time:................... 2014-12-29 00:00:00
   ...
   
Další verze skriptu je ke stažení `zde
<../_static/skripty/tgrass_landsat_foss4g2016.py>`_.
