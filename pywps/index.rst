***********************
Publikování WPS procesu
***********************

V této kapitole si ukážeme způsob publikace Python skriptu pro GRASS
GIS jako webovou geoprocessingovou službu dle standardu OGC `Web
Processing Service <http://www.opengeospatial.org/standards/wps>`__
(WPS).

Dále předpokládáme, že máme k dispozici server, na kterém je
zprovozněn `PyWPS <https://pywps.org/>`__, který nám umožní nástroj
systému GRASS publikovat jako tzv. WPS proces.

V rámci následující ukázky implementujeme skript pomocí :doc:`PyGRASS
<../pygrass/index>`, který pro vybrané PSČ vybere dotčené obce a k nim
sousedící obce opět na základě PSČ. Poté skript upravíme tak, aby se z
něj stal WPS proces, který bude možno pomocí PyWPS publikovat.

.. toctree::
   :maxdepth: 2

   grass-skript
   wps-proces

