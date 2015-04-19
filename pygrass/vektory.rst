Přístup k vektorovým datům
==========================

K vektorovým datům lze přistupovat ve dvou režimech:

* *bez topologie* (ala jednoduché geoprvky, viz OGC standard `Simple
  Features <http://www.opengeospatial.org/standards/sfa>`_), tento
  přístup zajišťuje třída :pygrass-vector:`Vector`
* *včetně topologie*, viz třída :pygrass-vector:`VectorTopo`

Další informace v `dokumentaci PyGRASS
<http://grass.osgeo.org/grass70/manuals/libpython/pygrass_vector.html>`_.

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
          
Nalezení nejbližších prvků
--------------------------

Přístup k topologii
-------------------

