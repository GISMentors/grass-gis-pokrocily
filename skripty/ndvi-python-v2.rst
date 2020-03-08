NDVI - Pokročilejší verze skriptu
---------------------------------

Pokročilejší verze skriptu je rozšířena o:

* uživatelské rozhraní, řádky :lcode:`3-19`
* vstupní parametry (:option:`mapset`, :option:`output_postfix` a
  :option:`classes`), viz řádky :lcode:`6-19`
* uživatelské rozhraní je zpracováno funkcí ``parse()`` (řádek
  :lcode:`102`), která je součástí balíčku ``grass.script`` (řádek
  :lcode:`24`)
* hodnoty parametrů jsou na řádku :lcode:`102` uloženy do proměnné
  ``options``, přepínače do proměnné ``flags``, ty jsou dále použity
  na řádcích :lcode:`30-31,57`
* celý kód je vložen do funkce ``main()`` (řádek :lcode:`29`)
    
.. literalinclude:: ../_static/skripty/ndvi-v2.py
   :language: python
   :linenos:
   :emphasize-lines: 3-19, 24, 29, 30-31, 57, 102

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

Příklad parametru :option:`output_postfix`

.. literalinclude:: ndvi-v2.py
   :language: python
   :lines: 10-15

který definuje jeho

* název (``key``)
* popisek (``description``)
* výchozí hodnotu (``answer``)
* a typ parametru (``type``)

U dalších parametrů jsou použity tzv. `standardizované volby
<http://grass.osgeo.org/programming7/parser__standard__options_8c.html>`__,
např. ``G_OPT_M_MAPSET`` definuje parametr pro volbu mapsetu. V našem
případě nastavíme parametr skriptu jako povinný (``required: yes``) a
doplníme výchozí volbu (mapset :mapset:`landsat`), viz
:numref:`wxgui-ndvi-v2-0`.

.. literalinclude:: ndvi-v2.py
   :language: python
   :lines: 6-9

Ve výsledku se skript chová jako standardní modul systému GRASS,
přepínačem :option:`--help` obdržíme informace o jeho syntaxi.

.. code-block:: bash

   ndvi-v2.py --help

::
      
    Description:
     Creates reclassified NDVI.

    Usage:
     ndvi-v2.py mapset=name [output_postfix=string] [classes=name] [--help]
       [--verbose] [--quiet] [--ui]

    Flags:
     --h   Print usage summary
     --v   Verbose module output
     --q   Quiet module output
     --ui  Force launching GUI dialog

    Parameters:
              mapset   Name of mapset (default: current search path)
                        '.' for current mapset
                       default: landsat
      output_postfix   Postfix for output maps
                       default: ndvi
             classes   Name of input file
        
           
Poznámky k vypisování informačních zpráv
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nahradili jsme funkci ``print()`` pro vypisování zpráv o průběhu
funkcí ``message()`` z balíčku ``grass.script``. 

.. literalinclude:: ../_static/skripty/ndvi-v1.py
   :language: python
   :lines: 27

přepsáno na
      
.. literalinclude:: ../_static/skripty/ndvi-v2.py
   :language: python
   :lines: 53

Díky tomu budou fungovat globální přepínače :option:`--quiet` a
:option:`--verbose` pro tichý, resp. upovídaný mód.  Např. při použítí
volby :option:`--quiet` se vypíše pouze výsledný report, ostatní
zprávy o průběhu výpočtu budou skryty.

.. code-block:: bash

   ndvi-v2.py mapset=landsat --q

::
      
    --------------------------------------------------------------------------------
    Trida 1 (bez vegetace, vodni plochy  ):   0.28%
    Trida 2 (plochy s minimalni vegetaci ):  30.24%
    Trida 3 (plochy pokryte vegetaci     ):  21.00%
    Trida * (no data                     ):  48.49%
    --------------------------------------------------------------------------------

Poznámky k hledání vstupních rastrových dat
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pro nalezení rastrových map končících na *B4* a *B5* použijeme funkci
:pygrass-gis:`glist <Mapset.glist>` třídy :pygrass-gis:`Mapset`. Třída
:pygrass-gis:`Mapset` je součástí balíčku ``pygrass.gis``.

.. literalinclude:: ndvi-v2.py
   :language: python
   :lines: 27, 36-40

.. note:: Blokem ``try/except`` zachytíme chybu v případě, že rastrové mapy
          nebudou nalezeny. Potom zavoláme funkci ``fatal()`` z
          knihovny ``grass.script``, která skript ukončí.
      
Poznámky ke spuštění modulu
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pokud skript spustíme bez parametrů mělo by vyskočit grafické okno
podobné ostatním modulům systému GRASS.

.. figure:: images/wxgui-ndvi-v2-0.png
        
   Vygenerovaný grafický dialog skriptu.

.. note:: **Spuštění skriptu s parametrem classes**

   Mějme soubor `classes.txt` s odlišným rozdělením tříd:

   .. literalinclude:: ../_static/skripty/classes.txt

   Soubor ke stažení `zde <../_static/skripty/classes.txt>`_.
   
   Spuštění skriptu bude vypadat následovně

   .. code-block:: bash
                
      ndvi-v2.py map=landsat classes=classes.txt

   s výsledkem:

   ::
      
        --------------------------------------------------------------------------------
        Trida 1 (bez vegetace, vodni plochy  ):   0.68%
        Trida 2 (plochy s minimalni vegetaci ):  38.43%
        Trida 3 (plochy pokryte vegetaci     ):  12.39%
        Trida * (no data                     ):  48.49%
       --------------------------------------------------------------------------------
   
