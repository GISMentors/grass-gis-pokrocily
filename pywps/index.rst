****************************
Publikování jako WPS procesu
****************************

V této kapitole si ukážeme jakým způsobem vypublikovat libovolný
skript pro systém GRASS nebo obecně jakýkoliv jeho nástroj jako
webovou geoprocessingovou službu dle standardu OGC `Web Processing
Service <http://www.opengeospatial.org/standards/wps>`_ (WPS).

Dále předpokládáme, že máme k dispozici server, na kterém je
zprovozněn `PyWPS <http://pywps.wald.intevation.org/>`_, který nám
umožní nástroj systému GRASS vypublikovat jako nový WPS proces.

V rámci následující ukázky implementujeme uživatelský skript pomocí
:doc:`PyGRASS <../pygrass/index>`, který pro vybrané PSČ vybere
dotčené obce a k nim sousedící obce opět dle PSČ. Poté skript upravíme
tak, aby se z něj stal WPS proces, který bude možno pomocí PyWPS
vypublikovat.

.. toctree::
   :maxdepth: 2

   grass-skript
   wps-proces

