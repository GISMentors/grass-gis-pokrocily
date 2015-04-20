*************************
Práce s externími formáty
*************************

GRASS používá nativně vlastní souborově orientovaný rastrový a
vektorový formát.

Od verze GRASS 7 nicméně umožňuje pracovat s daty v externích
rastrových a vektorových formátech *přímo* bez nutnosti konverze dat do
nativního formátu.

Data v externích formátech systém GRASS čte pomocí knihovny `GDAL
<http://gdal.org>`_. Z toho vyplívá, že v systému GRASS lze načíst
všechny datové formáty, které tato knihovna podporuje v režimu čtení.

Odbobně lze systém GRASS nastavit, aby ukládal nově vytvořená data v jiném formátu
než vlastním, tj. nativním. V tomto případě lze data zapisovat do
jakéholiv formátu, který knihovna GDAL podporuje v režimu zápisu.

Další informace lze najít na `wiki stránce o externích formátech
<http://grasswiki.osgeo.org/wiki/Working_with_external_data_in_GRASS_7>`_
projektu GRASS.

Připojení dat z wxGUI
=====================

Nástroje pro připojení externích dat a nastavení výstupního formátu
jsou dostupné z menu správce vrstev

.. figure:: images/link-menu.png

anebo z nástrojové lišty
            
.. figure:: images/link-tooltip.png
   :class: small
        
.. figure:: images/link-tool.png
   :width: 250px

Rastrová data
=============

Čtení
^^^^^

Pro připojení externích rastrových dat slouží modul
:grasscmd:`r.external`.

Příklad přípojení dat ve formátu JPEG
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   r.external input=/tmp/ortofoto.jpg output=ortofoto

Zápis
^^^^^

Nastavit externí výstupní rastrový formát umožňuje modul
:grasscmd:`r.external.out`.

Příklad nastavení výstupního formátu na GeoTIFF
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash
                
   r.external.out directory=/tmp/tif extension=tif format=GTiff
          
Vektorová data
==============

.. warning:: Práci s externími formáty pro vektorová data lze
   doporučit pouze při čtení pro účely vizualizace a jednorázovém
   zápisu mimo GRASS. Zcela zásadní rozdíl je v datových modelech, které jsou
   použity. GRASS používá striktně topologický formát, GDAL je
   postaven na OGC standardu Simple Features, tj. netopologickém
   datovém modelu. GRASS pro takováto data sestavuje
   tzv. pseudo-topologii. Pro standardní práci se systém GRASS nelze
   tuto cestu doporučit.

.. note:: Jako alternativa k nativnímu topologickému formátu se jeví
          :skoleni:`PostGIS Topology
          <postgis-pokrocily/kapitoly/8_topologie.html>`. Implementace
          podpory pro tento formát není nicméně v systému GRASS zcela
          dokončena a lze ji doporučit pouze pro testování, více na
          `wiki <http://grasswiki.osgeo.org/wiki/PostGIS_Topology>`_
          projektu.
   
Čtení
^^^^^

Pro připojení externích rastrových dat slouží modul
:grasscmd:`v.external`.

.. figure:: images/v.external.png

   Příklad připojení externím vektorových dat z GUI

Příklad přípojení dat z databáze PostGIS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   v.external input="PG:dbname=gismentors host=training.gismentors.eu user=skoleni password=XXX" \
   layer=ruian.obce_bod out=obce_pg

Příklad přípojení dat z `RÚIAN <http://freegis.fsv.cvut.cz/gwiki/RUIAN>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   v.external input=/vsicurl/http://vdp.cuzk.cz/vymenny_format/soucasna/20150331_OB_564567_UKSH.xml.gz \
   layer=AdresniMista
   
Zápis
^^^^^

Nastavit externí výstupní rastrový formát umožňuje modul
:grasscmd:`v.external.out`.

.. figure:: images/v.external.out.png

   Příklad nastavení výstupního formátu pro vektorová data

Příklad nastavení výstupního formátu na Esri Shapefile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash
                
   v.external.out output=/tmp/shp format="ESRI_Shapefile"
