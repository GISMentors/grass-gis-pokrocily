Přístup k rastrovým datům
=========================

Přístup k rastrovým datům umožňuje PyGRASS ve třech režimech:

* :pygrass-raster:`RasterRow` (náhodné čtení po řádcích, sekvenční zápis)
* :pygrass-raster:`RasterRowIO` (čtení po řádcích z vyrovnávací paměti, sekvenční zápis)
* :pygrass-raster:`RasterSegment` (náhodné čtení a zápis po dlaždicích)

Další informace v `dokumentaci PyGRASS
<http://grass.osgeo.org/grass70/manuals/libpython/pygrass_raster.html>`_.

.. warning:: GRASS při čtení rastrových dat vždy data převzorkuje podle
             aktuálního výpočetního regionu. Manipulaci s regionem má
             v PyGRASS na starost třída :pygrass-gis:`Region
             <region.Region>` anebo lze přímo použít modul
             :grasscmd:`g.region`.
   
Statistika rastrových dat, převzorkování
----------------------------------------

V následující ukázce vypíšeme statistiku převzorkovaného rastru:

#. Před načtením dat je změněn aktuální region na prostorové rozlišení
   1km (řádek :lcode:`9`).
#. Rastrová data jsou načtena pomocí třídy :pygrass-raster:`RasterRow`
   (řádek :lcode:`11-12`).
#. Jednotlivé řádky a sloupce rastru jsou procházeny cyklem ``for``
   (řádky :lcode:`16-17`).
#. Na konci skriptu nezapomeneme rastrovou mapu korektně uzavřít
   :lcode:`30`.
       
.. literalinclude:: ../_static/skripty/dmt.py
   :language: python
   :linenos:
   :emphasize-lines: 9, 11-12, 16-17, 30

Skript ke stažení `zde <../_static/skripty/dmt.py>`_.
                     
.. important:: Rastrová data budou v tomto případě převzorkována
               metodou :wikipedia-en:`nejblížšího souseda <Nearest
               neighbour interpolation>`.

Výpis může vypadat následovně:

::

   min=53.80 max=1530.51 count=138116 (no-data: 59244)
               
.. note:: Tento skript berte jako ilustrační, rozhodně jej nelze
          považovat za optimální cestu pro zjištění extremních hodnot
          v rastru (viz porovnání s modulem :grasscmd:`r.univar`).
                         
Dotazování na rastrová data
---------------------------

Skript vypisuje *pro definiční body obcí v ČR jejich nadmořské výšky*
odvozené z digitálního modelu terénu (rastrová mapa :map:`dmt`).

#. Před načtením rastrových dat na řádku :lcode:`11` je podle rastrové
   mapy :map:`dmt` nastaven výpočetní region.
#. Rastrová mapa :map:`dmt` je načtena třídou
   :pygrass-raster:`RasterRow` (řádka :lcode:`15-16`).
#. Jelikož se jedná u vstupní vektorové mapy o data bodová, tak stačí
   mapu otevřít bez topologie (řádky :lcode:`18-19`).
#. Souřadnice definičních bodů obcí jsou převedeny na souřadnice rastru
   funkcí ``coor2pixel`` (řádek :lcode:`22`)

.. literalinclude:: ../_static/skripty/obce_dmt.py
   :language: python
   :linenos:
   :emphasize-lines: 11, 15-16, 18-19, 22

Skript ke stažení `zde <../_static/skripty/obce_dmt.py>`_.
                     
Výpis může vypadat následovně:

::

   ...
   Kopidlno                                : 225
   Neratov                                 : 223
   Podhorní Újezd a Vojice                 : 336
   ...

.. note:: Rychlost implementace můžete porovnat s modulem
   :grasscmd:`v.what.rast`.

   .. code-block:: bash

      v.what.rast -p map=obce_bod@ruian raster=dmt
