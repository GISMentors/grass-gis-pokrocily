NDVI - Základní verze skriptu
-----------------------------

Začneme verzí skriptu *bez vstupních parametrů*, názvy vstupních a
výstupních rastrových map jsou uvedeny na řádcích :lcode:`7-12`.

Na řádku :lcode:`3` se importuje z knihovny :doc:`../pygrass/index`
třída :pygrass-modules:`Module`, která nám umožní z prostředí jazyka
Python spouštět moduly systému GRASS jako je
např. :grasscmd:`g.region` (viz řádek :lcode:`15`).

.. note:: Spouštět moduly systému GRASS z jazyka Python umožňuje také
   knihovna :grasscmd:`GRASS Python Scripting Library
   <libpython/script_intro>`. V našem případě budeme striktně používat
   knihovnu PyGRASS.
          
.. literalinclude:: ../_static/skripty/ndvi-v1.py
   :language: python
   :linenos:
   :emphasize-lines: 3, 7-9, 11-12, 15, 19-21, 32-33, 41-42, 46

Skript je ke stažení `zde <../_static/skripty/ndvi-v1.py>`__.

.. figure:: images/wxgui-ndvi-v1.png
   :class: middle

   Příklad spuštění skriptu v GUI a vizualizace výsledku v mapovém okně.

.. tip:: Namísto funkce ``print(...)`` zkuste použít

   .. code-block:: python

      from grass.pygrass.messages import Messenger

      msgr = Messanger()
      msgr.message('...')

.. _pygrass-module:
      
Poznámky k volání modulů
^^^^^^^^^^^^^^^^^^^^^^^^                     

Moduly systému GRASS se volají ve skriptech se stejnými parametry jako z příkazové
řádky. Například pro volání na řádku :lcode:`15`:

.. literalinclude:: ../_static/skripty/ndvi-v1.py
   :language: python
   :lines: 15

by korespondující zápis pro příkazovou řádku vypadal následovně:

.. code-block:: bash

   g.region align=LC81920252013215LGN00_B4@landsat vector=obce@ruian_praha
           
Jednotlivé parametry modulu se zadávaní jako argumenty třídy
:pygrass-modules:`Module`. Vyjímkou jsou globální přepínače (tj. ty,
které jsou uvozeny dvěma pomlčkami) jako je :option:`--quiet`,
:option:`--overwrite` a další. Ty se zadávají jako argument s hodnotou
``True``, např. ``overwrite=True``. Běžné přepínače (uvozeny jednou
pomlčkou) se předávají jako hodnota argumentu :option:`flags`.

.. noteadvanced:: **Zkracování názvů parametrů**

   Při volání modulů z příkazové řádky lze názvy parametrů libovolně
   zkracovat, pouze s tou podmínkou, aby byly jednoznačné. V níže
   uvedeném případě bude následnující volání v pořádku i když méně
   čitelné.

   .. code-block:: bash

      g.region al=LC81920252013215LGN00_B4@landsat v=obce@ruian_praha

   Podobné zkracování názvů parametrů **není** při použití třídy
   :pygrass-modules:`Module` z knihovny :doc:`../pygrass/index` možné.

   **Shortcuts**

   PyGRASS umožňuje emulovat způsob volání modulů z příkazové řádky
   pomocí tzv. "shortcuts". Příklad volání modulu
   :grasscmd:`g.region` (řádek :lcode:`15`):

   .. code-block:: python

      from grass.pygrass.modules.shortcuts import general as g

      g.region(raster=vis)

Vstup
~~~~~

Některé moduly přijímají vstup ze souboru, např. :grasscmd:`r.recode`
s parametrem :option:`rules` (řádky :lcode:`32-33`). Místo fyzického
vytvoření vstupního souboru na disku lze použít *standardní vstup*,
konktrétně argument ``stdin_`` s hodnotou řetězce, který má být na
vstupu. V tomto případě musí parameter modulu :option:`rules` nabývat
hodnoty ``-``.

.. literalinclude:: ../_static/skripty/ndvi-v1.py
   :language: python
   :lines: 27-33

Zpracování výstupu
~~~~~~~~~~~~~~~~~~

U modulů, které svůj výstup zapisují na *standardní výstup*, lze
jejich výstup zachytit přes argument ``stdout_=PIPE``. Obsah výstupu
je potom uložen jako řetězec v atributu třídy :pygrass-modules:`Module`
``outputs.stdout``, viz řádek :lcode:`45`.

.. literalinclude:: ../_static/skripty/ndvi-v1.py
   :language: python
   :lines:  4, 46, 49-50
