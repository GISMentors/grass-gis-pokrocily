Přístup k vektorovým datům
==========================

K vektorovým datům lze přistupovat ve dvou režimech:

* *bez topologie* (ala jednoduché geoprvky, viz OGC standard `Simple
  Features <http://www.opengeospatial.org/standards/sfa>`_), tento
  přístup zajišťuje třída :pygrass-vector:`Vector`
* *včetně topologie*, viz třída :pygrass-vector:`VectorTopo`

Další informace v `dokumentaci PyGRASS
<http://grass.osgeo.org/grass70/manuals/libpython/pygrass_vector.html>`_.

Průchod vektorovými prvky bez topologie
---------------------------------------

Skript vypisuje souřadnice definičních bodů z mapy :map:`obce_bod` 
mapsetu :mapset:`ruian` spolu s jejich názvy.

#. Nejprve na řádku :lcode:`5` vytvoříme instaci třídy
   :pygrass-vector:`Vector` odkazující na zvolenou vektorovou mapu,
   kterou na následujícím řádku otevřeme v režimu čtení
#. Jednotlivé prvky procházíme sekvenčne v cyklu ``for`` na řádku :lcode:`8`
     
.. literalinclude:: obce_body.py
   :language: python
   :linenos:
   :emphasize-lines: 5-6, 8
          
Přístup k topologii
-------------------

Přístup k topologii vektorových prvků zajišťuje třída
:pygrass-vector:`VectorTopo`.

.. tip:: Základní informace o :skoleni:`topologickém formátu
         <grass-gis-zacatecnik/vector/index.html#topologicky-model>`.

V nasledující ukázce vypíšeme pro každý okres jeho počet sousedním
okresů.
         
.. literalinclude:: okresy.py
   :language: python
   :linenos:

.. warning:: Tento skript je funkční pouze na verzi GRASS 7.0.1 a vyšší.
                   
Nalezení nejbližších prvků, zápis nových prvků
----------------------------------------------

K nalezení nejbližších prvků je vyžadován přístup k topologii. V
následujícím příkladě budeme hledat nejbližší ulici k dané
záchrance. Dále zkontrolujeme, zda je záchrance přiřazen korektní kód
ulice.

Záchranky jsou společně s nejbližšími ulicemi zapsány do nové
vektorové mapy :map:`zachranka_ulice` (řádky
:lcode:`10,15,24,26`). Atributová tabulka pro výstupní vektorovou mapu
je definována na řádcích :lcode:`11-14`.

.. literalinclude:: zachranka_ulice.py
   :language: python
   :linenos:
   :emphasize-lines: 10-15, 24, 26, 29

.. warning:: Velmi důležitý řádek je :lcode:`29`, kde dochází k zápisu
             atributů do atributové tabulky. Bez jeho volání by se
             **nezapsaly** do výstupní vektorové mapy žádné atributy!