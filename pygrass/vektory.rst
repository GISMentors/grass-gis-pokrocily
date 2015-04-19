Přístup k vektorovým datům
==========================

K vektorovým datům lze přistupovat ve dvou režimech:

* *bez topologie* (ala jednoduché geoprvky, viz OGC standard `Simple
  Features <http://www.opengeospatial.org/standards/sfa>`_), tento
  přístup zajišťuje třída :pygrass-vector:`Vector`
* *včetně topologie*, viz třída :pygrass-vector:`VectorTopo`

Další informace v `dokumentaci PyGRASS
<http://grass.osgeo.org/grass70/manuals/libpython/pygrass_vector.html>`_.

.. todo:: pridat priklad pro vytvoreni nove vrstvy

Jednoduchý příklad
------------------

Skript vypisuje souřadnice definičních bodů z mapy :map:`obce_bod` z
mapsetu :mapset:`ruian` spolu s jejich názvy.

#. Nejprve na řádku :lcode:`5` vytvoříme instaci třídy
   :pygrass-vector:`Vector` odkazující na zvolenou vektorovou mapu,
   kterou na následujícím řádku otevřeme v režimu čtení
#. Jednotlivé prvky procházíme sekvenčne v cyklu na řádku :lcode:`8`
     
.. literalinclude:: obce_body.py
   :language: python
   :linenos:
   :emphasize-lines: 5-6, 8

.. todo:: přidat atributový filter
          
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

.. warning:: Tento skript je funkční na verzi GRASS 7.0.1 a vyšší
                   
Nalezení nejbližších prvků
--------------------------

K nalezení nejbližších prvků je vyžadován přístup k topologii. V
následujícím příkladě budeme hledat nejbližší ulici k dané
záchrance. Dále zkontrolujeme, zda je záchrance přiřazen korektní kód
ulice.

.. literalinclude:: zachranka_ulice.py
   :language: python
   :linenos:


