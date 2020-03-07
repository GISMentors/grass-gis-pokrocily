Ukázka skriptu (NDVI)
=====================

V následující úkázce se zaměříme na :wikipedia-en:`normalizovaný
vegetační difereční index <NDVI>` (NDVI), který lze určit na základě
viditelného červeného a blízkého infračerveného kanálu satelitních
dat.

.. math::
        
   NDVI = (NIR - VIS) / (NIR  + VIS)

.. note:: Použijeme data :wikipedia:`Landsat` 8 z mapsetu
   `gismentors-lansat
   <http://training.gismentors.eu/geodata/grass/gismentors-landsat.zip>`_
   (985 MB). V případě Landsat 8 je červený kanál v pořadí
   *čtvrtý*, blízký infračernený *pátý*, viz
   :wikipedia-en:`wikipedia <Landsat_8#Operational_Land_Imager>`.

**Postup výpočtu**


#. Rastrovou vrstvu :map:`ndvi` vypočteme pomocí nástoje
   :skoleni:`mapové algebry
   <grass-gis-zacatecnik/rastrova_data/rastrova-algebra.html>`
   :grasscmd:`r.mapcalc`
#. :skoleni:`Reklasifikaci
   <grass-gis-zacatecnik/rastrova_data/reklasifikace.html>` do třech
   tříd (1:bez vegetace, vodni plochy; 2:plochy s minimalni vegetaci;
   3:plochy pokryte vegetaci) provedeme pomocí modulu
   :grasscmd:`r.recode` (jedná o data s :skoleni:`plovoucí desetinnou
   čárkou <grass-gis-zacatecnik/intro/rastr.html#raster-types>`, jinak
   by bylo vhodnější použít přímo :grasscmd:`r.reclass`).
#. Nastavíme vhodnou :skoleni:`tabulku barev
   <grass-gis-zacatecnik/rastrova_data/tabulka-barev.html>` pro
   reklasifikovaná data :grasscmd:`r.colors`
#. Nakonec vypíšeme pro jednotlivé kategorie NDVI jejich percentuální
   pokrytí, a to pomocí modulu :grasscmd:`r.stats`
..
   #. Dále nastavíme :skoleni:`popisky
   <grass-gis-zacatecnik/rastrova_data/reklasifikace.html#r-recode>`
   jednotlivých kategorií pomocí modulu :grasscmd:`r.category`

.. tip:: Namísto obecného modulu mapové algebry :grasscmd:`r.mapcalc`
   bychom mohli použít specializovaný :grasscmd:`i.vi`.
         
**Implementace**
   
.. toctree::
   :maxdepth: 1

   ndvi-python

..
   ndvi-posix
