**************************************
Vypublikování skriptu jako WPS procesu
**************************************

V této kapitole si ukážeme jakým způsobem skript pro systém GRASS nebo
obecně jakýkoliv jeho nástroj vypublikovat jako webovou geoprocessingovou
službu dle standardu OGC `Web Processing Service
<http://www.opengeospatial.org/standards/wps>`_ (WPS).

Dále předpokládáme, že máme k dispozici server, na kterém je
zprovozněn `PyWPS <http://pywps.wald.intevation.org/>`_, který nám
umožní nástroj systému GRASS vypublikovat jako nový WPS proces.

V rámci následující ukázky implementuje skript pomocí :doc:`PyGRASS
<../pygrass/index>`, který pro vybrané PSČ vybere obce a k nim
sousedící obce opět dle PSČ. Poté skript upravíme tak, aby se z něm
stal WPS proces, který bude možno pomocí PyWPS vypublikovat jako WPS proces.

.. toctree::
   :maxdepth: 2

   grass-skript
   wps-proces

