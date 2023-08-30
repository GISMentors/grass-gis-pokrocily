Přístup k rastrovým datům
=========================

Přístup k rastrovým datům umožňuje PyGRASS ve třech režimech:

* :pygrass-raster:`RasterRow` (náhodné čtení po řádcích, sekvenční zápis)
* :pygrass-raster:`RasterRowIO` (čtení po řádcích z vyrovnávací paměti, sekvenční zápis)
* :pygrass-raster:`RasterSegment` (náhodné čtení a zápis po dlaždicích)

Další informace v :grasscmd:`dokumentaci PyGRASS
<libpython/pygrass_raster>`.

.. warning:: GRASS při čtení rastrových dat vždy data převzorkuje podle
   aktuálního výpočetního regionu. Manipulaci s regionem má
   v PyGRASS na starost třída :pygrass-gis:`Region
   <region.Region>` anebo lze přímo použít modul
   :grasscmd:`g.region`.
   
Statistika rastrových dat
-------------------------

V následující ukázce vypíšeme statistiku rastru:

#. Před načtením dat je nastaven výpočetní region (řádek :lcode:`11-13`).
#. Rastrová data jsou načtena pomocí třídy :pygrass-raster:`RasterRow`
   (řádek :lcode:`15-16`).
#. Jednotlivé řádky a sloupce rastru jsou procházeny cyklem ``for``
   (řádky :lcode:`20-21`).
#. Na konci skriptu nezapomeneme rastrovou mapu korektně uzavřít
   :lcode:`34`.
       
.. literalinclude:: ../_static/skripty/rastr_stats_pygrass.py
   :language: python
   :linenos:
   :emphasize-lines: 11-13, 15-16, 20-21, 34

Skript ke stažení `zde <../_static/skripty/rastr_stats_pygrass.py>`__.
                     
Výpis může vypadat následovně:

::

   min=53.80 max=1530.51 count=138116 (no-data: 59244)
               
.. note:: Tento skript berte jako **ilustrační**, rozhodně jej *nelze
   považovat za optimální cestu* pro zjištění extremních hodnot v
   rastru. Porovnejte s modulem :grasscmd:`r.univar` a verzí skriptu
   založené na knihovně `NumPy <https://numpy.org>`__
   (:lcode:`17-18`).
 
   .. literalinclude:: ../_static/skripty/rastr_stats_pygrass_numpy.py
      :language: python
      :linenos:
      :emphasize-lines: 17-18

   Skript ke stažení `zde <../_static/skripty/rastr_stats_pygrass_numpy.py>`__.
   
Dotazování na rastrová data
---------------------------

Skript vypisuje *pro definiční body obcí v ČR jejich nadmořské výšky*
odvozené z digitálního modelu terénu (rastrová mapa :map:`dmt`).

#. Před načtením rastrových dat na řádcích :lcode:`10-12` je na
   základě rastrové mapy :map:`dmt` nastaven výpočetní region.
#. Rastrová mapa :map:`dmt` je načtena třídou
   :pygrass-raster:`RasterRow` (řádka :lcode:`14-15`).
#. Jelikož se jedná u vstupní vektorové mapy o data bodová, tak stačí
   mapu otevřít bez topologie (řádky :lcode:`17-18`).
#. Souřadnice definičních bodů obcí jsou převedeny na souřadnice rastru
   funkcí ``coor2pixel`` (řádek :lcode:`21`)

.. literalinclude:: ../_static/skripty/obce_dmt.py
   :language: python
   :linenos:
   :emphasize-lines: 10-12, 14-15, 17-18, 21

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

      v.what.rast -p map=obce_bod@ruian raster=dmt@PERMANENT
