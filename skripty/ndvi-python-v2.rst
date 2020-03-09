\NDVI - Pokročilejší verze skriptu
---------------------------------

Pokročilejší verze skriptu je rozšířena o:

* uživatelské rozhraní, řádky :lcode:`3-23`
* vstupní parametry (:option:`red`, :option:`nir`, :option:`aoi` a
  :option:`classes`), viz řádky :lcode:`6-23`
* uživatelské rozhraní je zpracováno funkcí ``parse()`` (řádek
  :lcode:`97`), která je součástí balíčku ``grass.script`` (řádek
  :lcode:`28`)
* hodnoty parametrů jsou na řádku :lcode:`97` uloženy do proměnné
  ``options``, přepínače do proměnné ``flags``, ty jsou dále použity
  na řádcích :lcode:`33-35,57,75`
* celý kód je vložen do funkce ``main()`` (řádek :lcode:`32`)
    
.. literalinclude:: ../_static/skripty/ndvi-v2.py
   :language: python
   :linenos:
   :emphasize-lines: 3-23, 28, 32, 33-35, 57, 75, 97

Výsledná verze skriptu ke stažení `zde
<../_static/skripty/ndvi-v2.py>`_.

.. _wxgui-ndvi-v2-0:

.. figure:: images/wxgui-ndvi-v2-0.png

   Příklad spuštění pokročilé verze skriptu v GUI, výběr vstupních
   parametru v dialogu nástroje.

.. figure:: images/wxgui-ndvi-v2-1.png

   Výsledek je vypsán do záložky :item:`Command output` v dialogu
   nástroje.

Poznámky k uživatelskému rozhraní
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Parametry jsou definovány pomocí tzv. `standardizovaných voleb
<http://grass.osgeo.org/programming7/parser__standard__options_8c.html>`__,
např. ``G_OPT_R_MAP`` definující parametr pro volbu rastrové mapy. V
našem případě změníme potřebné vlastnosti (``key``, ``description``) a
zvolíme výchozí hodnotu parametru pro snažší testování (``answer``).

.. literalinclude:: ndvi-v2.py
   :language: python
   :lines: 6-10

Ve výsledku se skript chová jako standardní modul systému GRASS,
přepínačem :option:`--help` obdržíme informace o jeho syntaxi.

.. code-block:: bash

   ndvi-v2.py --help

::
      
    Creates reclassified NDVI based on given AOI.
    Usage:
     ndvi-v2.py red=name nir=name aoi=name [classes=name]
    [--help]
       [--verbose] [--quiet] [--ui]
    Parameters:
          red   Name of red channel
                default: LC81920252013215LGN00_B4@landsat
          nir   Name of nir channel
                default: LC81920252013215LGN00_B5@landsat
          aoi   Name of vector map
                default: obce@ruian_praha
      classes   Name of input file
  
Poznámky k vypisování informačních zpráv
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nahradili jsme funkci ``print()`` pro vypisování zpráv o průběhu
funkcí ``message()`` z balíčku ``grass.script``. 

.. literalinclude:: ../_static/skripty/ndvi-v1.py
   :language: python
   :lines: 18

přepsáno na
      
.. literalinclude:: ../_static/skripty/ndvi-v2.py
   :language: python
   :lines: 48

Díky tomu budou fungovat globální přepínače :option:`--quiet` a
:option:`--verbose` pro tichý, resp. upovídaný mód.  Např. při použítí
volby :option:`--quiet` se vypíše pouze výsledný report, ostatní
zprávy o průběhu výpočtu budou skryty.

.. code-block:: bash

   ndvi-v2.py red=LC81920252013215LGN00_B4@landsat nir=LC81920252013215LGN00_B5@landsat aoi=obce@ruian_praha --q

::
      
   Trida 1: 1.30%
   Trida 2: 72.33%
   Trida 3: 26.37%

Poznámky ke spuštění modulu
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pokud skript spustíme bez parametrů mělo by vyskočit grafické okno
podobné ostatním modulům systému GRASS.

.. figure:: images/wxgui-ndvi-v2-0.png
        
   Vygenerovaný grafický dialog skriptu.

Mějme soubor `classes.txt` s odlišným rozdělením tříd:

.. literalinclude:: ../_static/skripty/classes.txt

Soubor ke stažení `zde <../_static/skripty/classes.txt>`_.

   Spuštění skriptu bude vypadat následovně
   
.. code-block:: bash
   
   ndvi-v2.py red=LC81920252013215LGN00_B4@landsat nir=LC81920252013215LGN00_B5@landsat aoi=obce@ruian_praha classes=classes.txt

s výsledkem:

::

   Trida 1: 4.70%
   Trida 2: 79.37%
   Trida 3: 15.93%
