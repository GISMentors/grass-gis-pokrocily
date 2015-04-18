*******************
Úvod do skriptování
*******************

Na základní úrovni lze psát skripty v jakémkoliv programovacím či
skriptovacím jazyce, ze kterého můžete volat nástroje systému GRASS,
tzv. :skoleni:`moduly <grass-gis-zacatecnik/intro/moduly>`. Může to
být např. :wikipedia:`Perl`, :wikipedia:`Ruby <Ruby (programovací
jazyk)>`, :wikipedia:`Java <Java (programovací jazyk)>` či typicky
:wikipedia:`POSIX` a :wikipedia:`Python`. Cílem prvně uvedeného
standardu :wikipedia:`POSIX` bylo vytvořit jednotné rozhraní, které
mělo zajistit přenositelnost programů mezi jednotlivými unixovými
operačními systémy. V POSIX se píše rychle a efektivně, na druhou
stranu nejsou skripty přenositelné např. na Windows a budou fungovat
pouze v prostředí POSIX. Pod Windows tak bude potřebovat prostředí,
které bude POSIX emulovat, např. :wikipedia-en:`MinGW` či
:wikipedia-en:`Cygwin`. Z tohoto pohledu se jeví jako lepší volba
rozšířený a zároveň multiplatformní jazyk :program:`Python` s širokou
škálou knihoven z oblasti GIS.

.. tip:: Více informací k tomuto tématu najdete
   ve školení :skoleni:`GeoPython <geopython>`.

Kromě toho je Python šíroce podporován nejen systémem GRASS
(:doc:`../pygrass/index`, ale i QGISem (`pyQGIS
<http://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/>`_)
či proprietárním Esri :wikipedia:`ArcGIS` (`arcpy
<http://resources.arcgis.com/en/help/main/10.2/index.html#//000v000000v7000000>`_).

Nejprve si na jednoduchém skriptu ukážeme možnosti spuštění:

.. toctree::
   :maxdepth: 2

   spusteni

Poté si zkusíme naimplementovat mírně pokročilejší skript pro výpočet
:wikipedia-en:`normalizovaného vegetačního diferečního indexu <NDVI>`.
NDVI lze určit na základě viditelného červeného a blízkého
infračerveného kanálu satelitních dat.

    .. math::
        
         NDVI = (NIR - VIS) / (NIR  + VIS)

.. note:: Použijeme data :wikipedia:`Landsat` 8 z mapsetu
          `gismentors-lansat
          <http://training.gismentors.eu/geodata/grass/gismentors-landsat.zip>`_
          (985 MB). V případě Landsat 8 je červený kanál v pořadí
          *čtvrtý*, blízký infračernený *pátý*, viz
          :wikipedia-en:`wikipedia <Landsat_8#Operational_Land_Imager>`.

**Postup výpočtu**


#. Mapset *landsat* vložíme do :skoleni:`vyhledávací cesty
   <grass-gis-zacatecnik/intro/struktura-dat.html#vyhledavaci-cesta>`
   pomocí modulu :grasscmd:`g.mapsets`
#. Rastr :map:`ndvi` vypočteme pomocí nástoje :skoleni:`mapové algebry
   <grass-gis-zacatecnik/raster/rastrova-algebra>`
   :grasscmd:`r.mapcalc`
#. :skoleni:`Reklasifikaci
   <grass-gis-zacatecnik/raster/reklasifikace>` do třech tříd
   provedeme pomocí modulu :grasscmd:`r.recode` (jedná o data s
   :skoleni:`plovoucí desetinnou čárkou
   <grass-gis-zacatecnik/raster/index.html#typy-rastrovych-map>`,
   jinak by bylo vhodnější použít přímo :grasscmd:`r.reclass`).
#. Dále nastavíme :skoleni:`popisky
   <grass-gis-zacatecnik/raster/reklasifikace#r-recode>` jednotlivých
   kategorii pomocí modulu :grasscmd:`r.category`.
#. Nastavíme vhodnou :skoleni:`tabulku barev
   <grass-gis-zacatecnik/raster/tabulka-barev>` pro reklasifikovaná data
   :grasscmd:`r.colors`.
#. Nakonec vypíšeme pro jednotlivé kategorie NDVI jejich výměru v
   hektarech a to pomocí modulu :grasscmd:`r.report`

**Implementace**
   
.. toctree::
   :maxdepth: 2

   python
   posix
