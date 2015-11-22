*******************
Úvod do skriptování
*******************

Na základní úrovni je možné psát vlastní nástroje pro systém GRASS v
libovolném programovacím či skriptovacím jazyce, ze kterého lze volat
nástroje systému GRASS, tzv. :skoleni:`moduly
<grass-gis-zacatecnik/intro/moduly>`. Může to být
např. :wikipedia:`Perl`, :wikipedia:`Ruby <Ruby (programovací
jazyk)>`, :wikipedia:`Java <Java (programovací jazyk)>` či typicky
:wikipedia:`POSIX` (shell), :wikipedia:`Python` a řada dalších.

.. note:: Cílem standardu :wikipedia:`POSIX` bylo vytvořit jednotné
          rozhraní, které mělo zajistit přenositelnost programů mezi
          jednotlivými unixovými operačními systémy. V POSIX se píše
          rychle a efektivně, na druhou stranu nejsou skripty
          přenositelné např. na Windows a budou fungovat pouze v
          prostředí POSIX. Pod Windows tak budete potřebovat
          prostředí, které bude POSIX emulovat,
          např. :wikipedia-en:`MinGW` či :wikipedia-en:`Cygwin`. Z
          tohoto pohledu se jeví jako lepší volba rozšířený a zároveň
          multiplatformní jazyk Python s širokou škálou knihoven z
          oblasti GIS.

Nejširší podporu má systém GRASS nicméně pro programovací jazyk **Python**
včetně vlastního rozhraní :doc:`PyGRASS <../pygrass/index>`. Kromě
toho je Python šíroce podporován nejen systémem GRASS, ale i QGISem
(`pyQGIS
<http://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/>`_)
či proprietárním Esri :wikipedia:`ArcGIS` (`arcpy
<http://resources.arcgis.com/en/help/main/10.2/index.html#//000v000000v7000000>`_).

.. tip:: Více informací k programování v jazyku Python pro oblast GIS
         najdete ve specializovaném školení :skoleni:`GeoPython
         <geopython>`.

Nejprve si na ukážeme možnosti *spuštění uživatelského skriptu*:

.. toctree::
   :maxdepth: 2

   spusteni

Poté si naimplementujeme vlastní skript, nejprve v jazyku Python a poté
i pro POSIX.

.. toctree::
   :maxdepth: 2

   ndvi

