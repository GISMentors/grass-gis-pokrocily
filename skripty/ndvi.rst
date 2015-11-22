Výpočet normalizovaného vegetačního diferečního indexu
======================================================

:wikipedia-en:`Normalizovaný vegetační difereční index <NDVI>` (NDVI)
lze určit na základě viditelného červeného a blízkého infračerveného
kanálu satelitních dat.

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
   <grass-gis-zacatecnik/rastrova_data/rastrova-algebra>`
   :grasscmd:`r.mapcalc`
#. :skoleni:`Reklasifikaci
   <grass-gis-zacatecnik/rastrova_data/reklasifikace>` do třech tříd
   provedeme pomocí modulu :grasscmd:`r.recode` (jedná o data s
   :skoleni:`plovoucí desetinnou čárkou
   <grass-gis-zacatecnik/intro/rastr.html#typy-rastrovych-map>`,
   jinak by bylo vhodnější použít přímo :grasscmd:`r.reclass`).
#. Dále nastavíme :skoleni:`popisky
   <grass-gis-zacatecnik/rastrova_data/reklasifikace#r-recode>` jednotlivých
   kategorií pomocí modulu :grasscmd:`r.category`
#. Nastavíme vhodnou :skoleni:`tabulku barev
   <grass-gis-zacatecnik/rastrova_data/tabulka-barev>` pro reklasifikovaná data
   :grasscmd:`r.colors`
#. Nakonec vypíšeme pro jednotlivé kategorie NDVI jejich percentuální pokrytí
   a to pomocí modulu :grasscmd:`r.stats`

**Implementace**
   
.. toctree::
   :maxdepth: 2

   ndvi-python
   ndvi-posix
