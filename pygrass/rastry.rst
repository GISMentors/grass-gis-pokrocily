Přístup k rastrovým datům
=========================

Přístup k rastrovým datům umožňuje :program:`PyGRASS` hned v několika formách:

* :pygrass-raster:`RasterRow` (náhodné čtení po řádcích, sekvenční zápis)
* :pygrass-raster:`RasterRowIO` (čtení po řádcích z vyrovnávací paměti, sekvenční zápis)
* :pygrass-raster:`RasterSegment` (náhodné čtení a zápis po dlaždicích)

.. note:: Dokumentace zmiňuje ve verzi 7.0.0 třídu
          :pygrass-raster:`RasterNumPy`, ta byla nicméně odstraněna a
          není dále podporována.
    
Další informace v `dokumentaci PyGRASS
<http://grass.osgeo.org/grass70/manuals/libpython/pygrass_raster.html>`_.

.. warning:: GRASS při čtení rastrových dat vždy data převzorkuje do
             aktuálního výpočetního regionu. Manipulaci s regionem má
             v PyGRASS na starots třída :pygrass-gis:`Region <region.Region>`.
   
Statistika rastrových dat, převzorkování
----------------------------------------

V následující ukázce vypíšeme statistiku převzorkovaného rastru:

* před načtením dat je změněn aktuální region na prostorové rozlišení
  100m (řádek :lcode:`9`)
* rastrová data jsou načtena pomocí třídy :pygrass-raster:`RasterRow`
  (řádek :lcode:`11`)

.. literalinclude:: dmt.py
   :language: python
   :linenos:
   :emphasize-lines: 9, 11

.. important:: Rastrová data budou v tomto případě převzorkována
               metodou :wikipedia-en:`nejblížšího souseda <Nearest
               neighbour interpolation>`.
                        
Dotazování na rastrová data
---------------------------

Skript vypisuje pro definiční body obcí v ČR jejich nadmořské výšky
odvozené z digitálního modelu terénu (rastrová mapa :map:`dmt`).

* Před načtením rastrových dat na řádku :lcode:`11` je podle nich
  nastaven výpočetní region
* Rastrová mapa :map:`dmt` je načtena třídou
  :pygrass-raster:`RasterRow` (řádka :lcode:`15-16`)
* Souřadnice definičních bodů obcí jsou převedeny na souřadnice rastru
  funkcí ``coor2pixel`` (řádek :lcode:`22`)

.. literalinclude:: obce_dmt.py
   :language: python
   :linenos:
   :emphasize-lines: 11, 15-16, 22
