Python
======

Základní verze skriptu
----------------------

Začneme verzí skriptu *bez vstupní parametrů*, názvy vstupních a
výstupních rastrových map jsou uvedeny na řádcích :lcode:`10-14`.

Na řádku :lcode:`3` importuje z knihovny :doc:`../pygrass/index` třídu
:class:`Module`, která nám umožní z prostředí jazyka Python spouštěn
moduly GRASS jako je :grasscmd:`g.mapsets` (viz řádek :lcode:`7`) a
další.

.. literalinclude:: ndvi-v1.py
   :language: python
   :linenos:
   :emphasize-lines: 3, 7, 10-14, 18-20, 31-32, 40-41, 49-50, 54

Poznámky k volání modulů
^^^^^^^^^^^^^^^^^^^^^^^^                     

Moduly systému GRASS se volají se stejnými parametry jako z příkazové
řádky. Například pro volání na řádku :lcode:`7`:

.. literalinclude:: ndvi-v1.py
   :language: python
   :lines: 7

by korespondující zápis pro příkazovou řádku vypadal následovně:

.. code-block:: bash

   g.mapsets mapset=landsat operation=add --quiet
           
Jednotlivé parametry modulu se zadávaní jako argumenty třídy
:class:`Module`. Vyjímkou jsou globální přepínače jako je
:option:`--quiet`, :option:`--overwrite` a další, ty se zadávají jako
parametr s hodnotou ``True``, v tomto případě tedy ``quiet=True``.

.. note:: **Zkracování názvů parametrů**

   Při volání modulů z příkazové řádky lze názvy parametrů libovolně
   zkracovat, pouze z tou podmínkou aby byly jednoznačné, ve výše
   uvedeném případě bude následnující volání v pořádku i když méně
   čitelné.

   .. code-block:: bash

      g.mapsets landsat o=add --q

   Podobné zkracování názvů parametrů **není** při použití třídy
   :class:`Module` z knihovny :doc:`../pygrass/index` možné.
   
Vstup
~~~~~

Některé moduly přijímají vstup ze souboru, např. :grasscmd:`r.recode`
s parametrem :option:`rules` (řádky :lcode:`26-32`). Místo fyzického
vytvoření vstupního souboru na disku lze použít *standardní vstup*,
konktrétně argument ``stdin_`` s hodnotou řetězce, který má být na
vstupu. V tomto případě musí parameter modulu :option:`rules` nabývat
hodnoty ``-``.

.. literalinclude:: ndvi-v1.py
   :language: python
   :lines: 26-32

Zpracování výstupu
~~~~~~~~~~~~~~~~~~

U modulů, které svůj výstup zapisují na *standardní výstup*, lze
jejich výstup zachytit přes argument ``stdout_=PIPE``. Obsah výstupu
je potom uložen jako řetězec v atributu třídy :class:`Module``
``outputs.stdout``, viz řádek :lcode:`54,57`.

.. literalinclude:: ndvi-v1.py
   :language: python
   :lines:  4, 54, 57-58

Pokročilejší verze skriptu
--------------------------

.. literalinclude:: ndvi-v2.sh
   :language: bash
   :linenos:
